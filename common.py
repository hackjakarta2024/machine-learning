# example output for course generation
ex_output = [
        {
            "description": "Computer science is the study of computation and information. It encompasses a wide range of topics, from theoretical foundations to practical applications.",
            "material": "Computer science is a rapidly growing field, with new applications being developed all the time. It is a challenging and rewarding field that offers a wide range of career opportunities.",
            "quiz": {
                "choices": [
                    "The study of hardware",
                    "The study of software",
                    "The study of computation and information"
                ],
                "correct_answer": "The study of computation and information",
                "question": "What is the main focus of computer science?"
            },
            "source": [
                "https://en.wikipedia.org/wiki/Computer_science",
                "https://www.mtu.edu/cs/what/"
            ],
            "summary": "Computer science is a vast and rapidly growing field that offers a wide range of career opportunities. It is a challenging and rewarding field that is essential for the modern world.",
            "title": "Computer Science",
            "topic": "Computer Science"
        },
        {
            "description": "Software engineering is the application of engineering principles to the development of software systems.",
            "material": "Software engineering is a complex and challenging field, but it is also a rewarding one. Software engineers play a vital role in the development of the software that we use every day.",
            "quiz": {
                "choices": [
                    "To develop software that is efficient",
                    "To develop software that is reliable",
                    "To develop software that is user-friendly"
                ],
                "correct_answer": "To develop software that is efficient, reliable, and user-friendly",
                "question": "What is the main goal of software engineering?"
            },
            "source": [
                "https://en.wikipedia.org/wiki/Software_engineering",
                "https://www.mtu.edu/cs/what/"
            ],
            "summary": "Software engineering is a critical field that is responsible for the development of the software that we use every day. It is a challenging and rewarding field that offers a wide range of career opportunities.",
            "title": "Software Engineering",
            "topic": "Computer Science"
        },
        {
            "description": "Data science is the study of data and how it can be used to solve problems.",
            "material": "Data science is a rapidly growing field, with new applications being developed all the time. It is a challenging and rewarding field that offers a wide range of career opportunities.",
            "quiz": {
                "choices": [
                    "To collect data",
                    "To analyze data",
                    "To use data to solve problems"
                ],
                "correct_answer": "To use data to solve problems",
                "question": "What is the main goal of data science?"
            },
            "source": [
                "https://en.wikipedia.org/wiki/Data_science",
                "https://www.mtu.edu/cs/what/"
            ],
            "summary": "Data science is a critical field that is responsible for the development of the software that we use every day. It is a challenging and rewarding field that offers a wide range of career opportunities.",
            "title": "Data Science",
            "topic": "Computer Science"
        }]


stem_topics = [
    "Physics",
    "Mathematics",
    "Chemistry",
    "Biology",
    "Computer Science",
    "Astronomy",
    "Earth Sciences",
    "Engineering",
    "Environmental Science",
    "Material Science"
]

safe = [
    {
        "category": "HARM_CATEGORY_DANGEROUS",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]

config = {
    "temperature": 0.5,
}

topic_json_format = '''{
    "courseTopic": [
        {"interestTopic1": "recommendedTopic1"},
        {"interestTopic2": "recommendedTopic2"},
        {"interestTopic3": "recommendedTopic3"},
        ...
    ]
}'''