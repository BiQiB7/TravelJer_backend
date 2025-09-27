import express from "express";
import { chromium, Browser, Page } from "playwright";
import { promises as fs } from "fs";
import path from "path";
import axios from "axios";
import pdf from "pdf-parse";

const app = express();
const port = 5002;

app.use(express.json());

interface ScrapeResult {
  url: string;
  text: string;
  links: string[];
  scrapedSubPages?: ScrapeResult[];
}

async function readPdfFromUrl(url: string): Promise<string> {
  try {
    const response = await axios.get(url, {
      responseType: "arraybuffer",
    });
    const data = await pdf(response.data);
    return data.text;
  } catch (error) {
    const errorMessage =
      error instanceof Error ? error.message : "An unknown error occurred";
    console.error(`Failed to read PDF from ${url}: ${errorMessage}`);
    throw new Error(`Failed to read PDF from ${url}: ${errorMessage}`);
  }
}

async function scrapePage(
  browser: Browser,
  url: string,
  currentDepth: number,
  maxDepth: number,
  visited: Set<string>,
  include_patterns?: string[],
  exclude_patterns?: string[],
  max_num?: number
): Promise<ScrapeResult | null> {

  if (currentDepth > maxDepth || visited.has(url)) {
    return null;
  }
  visited.add(url);

  let page: Page | null = null;
  try {
    console.log(`[${currentDepth}] Scraping: ${url}`);
    page = await browser.newPage();

    await page.route("**/*", (route: any) => {
      const resourceType = route.request().resourceType();
      if (["image", "stylesheet", "font"].includes(resourceType)) {
        route.abort();
      } else {
        route.continue();
      }
    });
// "networkidle"
// "domcontentloaded"
    await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
    console.log(`[${currentDepth}] Successfully loaded: ${url}`);

    const pageData = await page.evaluate(() => {
      const links = Array.from(document.querySelectorAll("a")).map((a: HTMLAnchorElement) => a.href);
      const uniqueLinks = [...new Set(links)].filter(link => link);
      const text = document.body.innerText;
      return { text, links: uniqueLinks };
    });

    let filteredLinks = pageData.links;
    if (include_patterns && include_patterns.length > 0) {
      filteredLinks = filteredLinks.filter((link: string) =>
        include_patterns.some((pattern) => new RegExp(pattern).test(link))
      );
    } else if (exclude_patterns && exclude_patterns.length > 0) {
      filteredLinks = filteredLinks.filter(
        (link: string) => !exclude_patterns.some((pattern) => new RegExp(pattern).test(link))
      );
    }

    const result: ScrapeResult = {
      url,
      text: pageData.text,
      links: filteredLinks,
    };

    if (currentDepth < maxDepth) {
      result.scrapedSubPages = [];
      let linksToScrape = filteredLinks.filter(
        (link: string) => link.startsWith("http") && !visited.has(link)
      );

      if (max_num !== undefined && max_num > 0) {
        linksToScrape = linksToScrape.slice(0, max_num);
      }

      for (const link of linksToScrape) {
        if (link.endsWith(".pdf")) {
          try {
            const pdfText = await readPdfFromUrl(link);
            result.scrapedSubPages.push({
              url: link,
              text: pdfText,
              links: [],
            });
          } catch (error) {
            console.error(`Skipping PDF ${link} due to error:`, error);
          }
        } else {
          const subPageResult = await scrapePage(
            browser,
            link,
            currentDepth + 1,
            maxDepth,
            visited,
            include_patterns,
            exclude_patterns,
            max_num
          );
          if (subPageResult) {
            result.scrapedSubPages.push(subPageResult);
          }
        }
      }
    }

    return result;
  } catch (error) {
    console.error(`Error scraping ${url}:`, error);
    return {
      url,
      text: `Failed to scrape: ${error instanceof Error ? error.message : "Unknown error"}`,
      links: [],
    };
  } finally {
    if (page) {
      await page.close();
    }
  }
}

app.post("/scrape", async (req: express.Request, res: express.Response) => {
  const {
    url,
    depth = 1,
    include_patterns,
    exclude_patterns,
    max_num,
  } = req.body;

  if (!url) {
    return res.status(400).send("Please provide a URL to scrape.");
  }

  let browser: Browser | null = null;
  try {
    browser = await chromium.launch();
    const visited = new Set<string>();
    const result = await scrapePage(
      browser,
      url,
      1,
      depth,
      visited,
      include_patterns,
      exclude_patterns,
      max_num
    );

    if (result) {
      try {
        const timeId = new Date().toISOString().replace(/:/g, "-");
        const dirPath = path.join(process.cwd(), "temp", timeId);
        await fs.mkdir(dirPath, { recursive: true });
        const filePath = path.join(dirPath, "result.json");
        await fs.writeFile(filePath, JSON.stringify(result, null, 2));
        console.log(`Scraping result saved to ${filePath}`);
      } catch (fileError) {
        console.error("Failed to write scraping result to file:", fileError);
      }
    }

    res.json(result);
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : "An unknown error occurred";
    console.error("Error during scraping process:", errorMessage);
    res.status(500).json({ error: "Failed to scrape the URL.", details: errorMessage });
  } finally {
    if (browser) {
      await browser.close();
    }
  }
});

app.post(
  "/read-pdf",
  async (req: express.Request, res: express.Response) => {
    const { url } = req.body;
    console.log("huehue")

    if (!url) {
      return res.status(400).send("Please provide a URL to a PDF file.");
    }

    try {
      const pdfText = await readPdfFromUrl(url);
      res.send({ text: pdfText });
    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : "An unknown error occurred";
      res
        .status(500)
        .json({ error: "Failed to read the PDF.", details: errorMessage });
    }
  }
);

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});