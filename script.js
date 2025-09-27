document.addEventListener('DOMContentLoaded', () => {
    const screens = document.querySelectorAll('.screen');
    const beginAdventureBtn = document.getElementById('beginAdventureBtn');
    const confirmAdventureBtn = document.getElementById('confirmAdventureBtn');

    let currentScreen = 1;

    function showScreen(screenNumber) {
        screens.forEach((screen, index) => {
            if (index + 1 === screenNumber) {
                screen.classList.add('active');
            } else {
                screen.classList.remove('active');
            }
        });
        currentScreen = screenNumber;
    }

    beginAdventureBtn.addEventListener('click', () => {
        showScreen(2);
    });

    const weavingText = document.querySelector('.weaving-text');
    const weavingIcon = document.querySelector('.weaving-icon');

    const weavingMessages = [
        "Okay, an Urban Explorer! My favorite.",
        "Analyzing today's weather...",
        "Scanning real-time traffic data...",
        "Searching Reddit for this week's hidden gems...",
        "Cross-referencing Google reviews for the best spots...",
        "Weaving your custom adventure now..."
    ];

    function startWeavingAnimation() {
        let messageIndex = 0;
        weavingIcon.innerHTML = document.querySelector('.adventure-card.selected .adventure-icon').innerHTML;
        const interval = setInterval(() => {
            if (messageIndex < weavingMessages.length) {
                weavingText.textContent = weavingMessages[messageIndex];
                messageIndex++;
            } else {
                clearInterval(interval);
                showScreen(4);
            }
        }, 1500);
    }

    confirmAdventureBtn.addEventListener('click', () => {
        showScreen(3);
        startWeavingAnimation();
    });

    const adventureCarousel = document.querySelector('.adventure-carousel');

    const adventures = [
        {
            icon: '🏛️',
            title: 'The Culture Vulture',
            description: 'A journey through art, history, and the city\'s creative soul.'
        },
        {
            icon: '🧭',
            title: 'The Urban Explorer',
            description: 'Discover hidden alleys, street art, and the city\'s best-kept secrets.'
        },
        {
            icon: '🍜',
            title: 'The Foodie\'s Quest',
            description: 'A delicious tour of the city\'s most amazing culinary delights.'
        },
        {
            icon: '🌙',
            title: 'The Mystic\'s Path',
            description: 'Uncover the city\'s haunted history and mysterious legends.'
        },
        {
            icon: '🌿',
            title: 'The Nature Seeker',
            description: 'Escape the concrete jungle and find serene green spaces.'
        }
    ];

    function createAdventureCards() {
        adventures.forEach(adventure => {
            const card = document.createElement('div');
            card.classList.add('adventure-card');
            card.innerHTML = `
                <div class="adventure-icon">${adventure.icon}</div>
                <h3>${adventure.title}</h3>
                <p>${adventure.description}</p>
            `;
            card.addEventListener('click', () => {
                document.querySelectorAll('.adventure-card').forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                confirmAdventureBtn.classList.remove('hidden');
            });
            adventureCarousel.appendChild(card);
        });
    }

    const itineraryTimeline = document.querySelector('.itinerary-timeline');
    const fab = document.querySelector('.fab');

    const itinerary = [
        {
            time: '10:00 AM',
            title: 'The Hidden Canvas',
            location: 'Graffiti Alley',
            insight: "I've analyzed recent Reddit threads and this alley is buzzing right now with new art from a local collective. Google reviews say to 'go to the very end for the best mural,' and warn that it gets crowded after noon, so we'll beat the rush.",
            weather: '☀️',
            travel: '🚶 15 min',
            cost: 'FREE'
        },
        {
            time: '12:30 PM',
            title: 'The Fuel Stop',
            location: '"The Daily Grind" Coffee Roasters',
            insight: "This spot is a true hidden gem with a 4.9-star rating. My summary of 50+ reviews: The coffee is 'phenomenal,' but the real secret is the 'unbelievable almond croissant.' It's the perfect place to recharge before our next stop.",
            weather: '☀️',
            travel: '🚶 10 min',
            cost: '$'
        }
    ];

    function createItinerary() {
        itineraryTimeline.innerHTML = ''; // Clear previous itinerary
        itinerary.forEach((stop, index) => {
            const stopElement = document.createElement('div');
            stopElement.classList.add('itinerary-stop', index % 2 === 0 ? 'left' : 'right');
            stopElement.innerHTML = `
                <div class="stop-content">
                    <h4>${stop.time}: ${stop.title}</h4>
                    <p><em>${stop.location}</em></p>
                    <div class="key-info">
                        <span>${stop.weather}</span>
                        <span>${stop.travel}</span>
                        <span>${stop.cost}</span>
                    </div>
                    <blockquote class="ai-insight">"${stop.insight}"</blockquote>
                    <button class="map-btn">🗺️ Open in Maps</button>
                    <button class="reviews-btn">💬 Read Reviews</button>
                </div>
            `;
            itineraryTimeline.appendChild(stopElement);
        });

        // Add event listeners to new buttons
        document.querySelectorAll('.map-btn').forEach(btn => {
            btn.addEventListener('click', () => alert('Opening in Maps...'));
        });
        document.querySelectorAll('.reviews-btn').forEach(btn => {
            btn.addEventListener('click', () => alert('Showing reviews...'));
        });
    }

    fab.addEventListener('click', () => {
        alert('Shuffling itinerary... (not implemented in mockup)');
    });
    
    function startWeavingAnimation() {
        let messageIndex = 0;
        weavingIcon.innerHTML = document.querySelector('.adventure-card.selected .adventure-icon').innerHTML;
        const interval = setInterval(() => {
            if (messageIndex < weavingMessages.length) {
                weavingText.textContent = weavingMessages[messageIndex];
                messageIndex++;
            } else {
                clearInterval(interval);
                createItinerary(); // Create the itinerary before showing the screen
                showScreen(4);
            }
        }, 1500);
    }


    createAdventureCards();

    // Initially show the first screen
    showScreen(1);
});