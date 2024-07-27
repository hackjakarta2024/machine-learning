## Cold Start Course Recommendation and Generation API

```/initcourse``` ```method: POST ```
- ```JSON:```
```
{"userId": "your_user_id", "age": 25, "interestTopic": ["Astronomy"]}
```
Response:
```
[
    {
        "description": "Astrophysics delves into the physical nature and processes of celestial objects and phenomena.",
        "material": "Using principles of physics and chemistry, astrophysicists explore stars, galaxies, black holes, and the universes origins and fate. They study topics like dark matter, dark energy, and the formation of planets and stars.",
        "quiz": {
            "choices": [
                "Mapping the positions of stars and galaxies",
                "Understanding the physical nature of celestial objects",
                "Predicting astronomical events like eclipses"
            ],
            "correct_answer": "Understanding the physical nature of celestial objects",
            "question": "What is the primary focus of astrophysics?"
        },
        "source": [
            "https://en.wikipedia.org/wiki/Astrophysics"
        ],
        "summary": "Astrophysics applies physics and chemistry to understand the universe, from the smallest particles to the largest structures.",
        "title": "Astrophysics: Unraveling the Cosmos",
        "topic": "Astronomy"
    },
    {
        "description": "Cosmology investigates the origin, evolution, and ultimate fate of the universe as a whole.",
        "material": "Cosmologists study the Big Bang, the expansion of the universe, and the nature of space-time. They explore fundamental questions about the universes beginning, composition, and future.",
        "quiz": {
            "choices": [
                "The life cycle of stars",
                "The formation of galaxies",
                "The origin and evolution of the universe"
            ],
            "correct_answer": "The origin and evolution of the universe",
            "question": "What is the main concern of cosmology?"
        },
        "source": [
            "https://en.wikipedia.org/wiki/Astrophysics"
        ],
        "summary": "Cosmology seeks to understand the universes past, present, and future on the largest scales.",
        "title": "Cosmology: The Universes Grand Story",
        "topic": "Astronomy"
    },
    {
        "description": "Observational astronomy involves collecting and analyzing data from telescopes and other instruments.",
        "material": "Astronomers use various telescopes, both on Earth and in space, to observe celestial objects across the electromagnetic spectrum. They gather data to study the properties and behavior of stars, galaxies, and other phenomena.",
        "quiz": {
            "choices": [
                "Computer simulations",
                "Mathematical modeling",
                "Telescope observations"
            ],
            "correct_answer": "Telescope observations",
            "question": "What is the primary method used in observational astronomy?"
        },
        "source": [
            "https://en.wikipedia.org/wiki/Astrophysics"
        ],
        "summary": "Observational astronomy uses telescopes and instruments to gather data about the universe, providing the basis for our understanding of celestial objects.",
        "title": "Observational Astronomy: Witnessing the Cosmos",
        "topic": "Astronomy"
    },
    {
        "description": "Planetary science focuses on the study of planets, moons, asteroids, comets, and other objects within our solar system.",
        "material": "Planetary scientists investigate the formation, composition, and evolution of these objects. They explore topics like planetary atmospheres, geology, and the potential for life beyond Earth.",
        "quiz": {
            "choices": [
                "Distant galaxies and black holes",
                "The properties of stars",
                "Objects within our solar system"
            ],
            "correct_answer": "Objects within our solar system",
            "question": "What is the main focus of planetary science?"
        },
        "source": [
            "https://en.wikipedia.org/wiki/Astrophysics"
        ],
        "summary": "Planetary science delves into the diverse worlds within our solar system, from planets and moons to asteroids and comets.",
        "title": "Planetary Science: Exploring Our Solar System",
        "topic": "Astronomy"
    },
    {
        "description": "Stellar astronomy investigates the properties and life cycles of stars.",
        "material": "Astronomers study the birth, evolution, and death of stars, including their energy production, composition, and ultimate fate. They explore topics like stellar nucleosynthesis, supernovae, and the formation of neutron stars and black holes.",
        "quiz": {
            "choices": [
                "The large-scale structure of the universe",
                "The properties and life cycles of stars",
                "The search for extraterrestrial life"
            ],
            "correct_answer": "The properties and life cycles of stars",
            "question": "What is the primary focus of stellar astronomy?"
        },
        "source": [
            "https://en.wikipedia.org/wiki/Astrophysics"
        ],
        "summary": "Stellar astronomy seeks to understand the fascinating lives of stars, from their birth to their explosive deaths.",
        "title": "Stellar Astronomy: Unveiling the Stars",
        "topic": "Astronomy"
    }
]
```
## FYP Course Recommendation and Generation API
```/recommendation``` ```method: POST ```

- ```JSON:```
```
{"userId": "0fe2feab-30f7-4c07-b646-218cb18142b8"}
```
Response:
```
[
    {
        "description": "Planetary science focuses on the study of planets, moons, asteroids, comets, and other objects within our solar system.",
        "material": "Planetary scientists investigate the formation, composition, and evolution of these objects. They explore topics like planetary atmospheres, geology, and the potential for life beyond Earth.",
        "quiz": {
            "choices": [
                "Distant galaxies and black holes",
                "The properties of stars",
                "Objects within our solar system"
            ],
            "correct_answer": "Objects within our solar system",
            "question": "What is the main focus of planetary science?"
        },
        "source": [
            "https://en.wikipedia.org/wiki/Astrophysics"
        ],
        "summary": "Planetary science delves into the diverse worlds within our solar system, from planets and moons to asteroids and comets.",
        "title": "Planetary Science: Exploring Our Solar System",
        "topic": "Astronomy"
    },
    {
        "description": "Stellar astronomy investigates the properties and life cycles of stars.",
        "material": "Astronomers study the birth, evolution, and death of stars, including their energy production, composition, and ultimate fate. They explore topics like stellar nucleosynthesis, supernovae, and the formation of neutron stars and black holes.",
        "quiz": {
            "choices": [
                "The large-scale structure of the universe",
                "The properties and life cycles of stars",
                "The search for extraterrestrial life"
            ],
            "correct_answer": "The properties and life cycles of stars",
            "question": "What is the primary focus of stellar astronomy?"
        },
        "source": [
            "https://en.wikipedia.org/wiki/Astrophysics"
        ],
        "summary": "Stellar astronomy seeks to understand the fascinating lives of stars, from their birth to their explosive deaths.",
        "title": "Stellar Astronomy: Unveiling the Stars",
        "topic": "Astronomy"
    }
]
```
