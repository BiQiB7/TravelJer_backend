# Use an official Node.js runtime as a parent image
FROM node:18

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install app dependencies
RUN npm install

# Install Playwright browsers
RUN npx playwright install --with-deps

# Bundle app source
COPY . .

# Build TypeScript code
RUN npm run build

# Expose the port the app runs on
EXPOSE 5002

# Define the command to run the app
CMD [ "npm", "run", "serve" ]