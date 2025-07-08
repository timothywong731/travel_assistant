# AI Travel Assistant

## 🧠 Overview

This is a GenAI-powered **Travel Assistant** that responds to natural language travel queries via an API. 
The API returns a structured travel advice.

---

## 📌 Requirements

- Python 3.10+
- FastAPI
- OpenAI API Key
- Pydantic
- Langgraph
- Seed data (provided as `.json`)
- The full list of dependencies can be found in `pyproject.toml`

---

## 💪🏽 Features

- **Multi-agent framework**: The API is powered by a multi-agent system comprising of several agents in a hierarchical design. This allows agents to refine interim information before responding to end-users.

- **ReACT Agents**: Each agent in the system leverages the [ReACT prompting strategy](https://www.ibm.com/think/topics/react-agent), enabling them to reason, take actions, and iteratively observe outcomes. This approach allows agents to refine their responses step by step, resulting in more accurate and context-aware travel recommendations.

- **Grounding on verified facts**: All travel recommendations are based strictly on the provided seed data (e.g., hotels, flights, experiences) rather than relying on the AI's general knowledge. This ensures that responses are accurate, up-to-date, and verifiable.

- **Unit Testing**: Comprehensive unit tests are included for core components such as API endpoints, data validation, and agent logic. Tests ensure correct handling of user queries, proper use of seed data, and robust error handling. Example tests cover both typical and edge-case scenarios to maintain reliability and code quality.

- **Guardrails and validation**: Implements input validation guardrails to ensure safe, relevant, and high-quality outputs. The system censors unethical, unsafe, or inappropriate topics (eg. gambling) in user queries, ensuring that responses adhere to responsible AI use and content guidelines. 

- **Easy extensibility**: Modular architecture allows for straightforward addition of new agents or new data sources.

- **Developer-friendly setup**: This project uses the [Poetry](https://python-poetry.org/) framework for managing dependencies and packaging. Poetry simplifies dependency resolution, virtual environment management, and project configuration. This ensures a reproducible and maintainable development environment.


## 🚨 Limitations & Potential Improvements

- **Seed data dependency**: Recommendations are limited to the scope of the provided seed data. The system does not fetch live data (e.g., prices, availability, weather). All responses are based on static seed data. 

- **Limited personalisation**: User preferences are only considered as described in the query; there is no persistent user profile or learning. Future systems can include user preferences (e.g. search history) for more personalised recommendations, enabling the assistant to tailor suggestions based on past interactions and user profiles.

- **Guardrails and Input validation**: Current input validation is basic and may not catch all ambiguous or malformed queries. Future improvements could include more sophisticated input checking, potentially leveraging AI models to better understand and validate user input before processing.

- **Hallucination**: While the system uses Retrieval-Augmented Generation (RAG) to ground responses in seed data, it may not fully prevent LLM hallucinations. The model could still generate information not present in the seed files, especially if queries are ambiguous or outside the scope of available data. Ongoing improvements to grounding techniques and stricter data validation are recommended to further minimise hallucinations.

- **Output validation**: The current system could benefit from additional output validation steps. For example, implementing checks to verify specific details such as airport codes and flight numbers in recommendations would help ensure that the information provided is valid and corresponds to the available seed data. This would further reduce the risk of hallucinated or incorrect responses from the LLM.

- **Tool portability and integration**: Current tools are tightly coupled to specific agents and use cases. For improved production readiness, consider adopting a Model Context Protocol (MCP) to enable better tool integration and portability. This would allow tools (e.g., flight lookup, booking records, search history) to be reused across different agents and workflows, making it easier to extend the system and add new capabilities without duplicating logic.



## 🔒 Security

No security measures are currently implemented. If this API is exposed to the internet, it could be vulnerable to unauthorised access and attacks. To mitigate these risks, it is recommended to add authentication mechanisms such as OAuth or API keys to ensure that only authorised users or services can invoke the API. Implementing HTTPS and rate limiting are also advised to further enhance security.


## 📌 Quickstart

To install and run the app, run the following command:

```bash
# Set up poetry for virtual environment
pip install poetry

# Install dependencies using the poetry framework
poetry install

# Run the app
poetry run uvicorn main:app --reload
```

To verify that the app in running correctly, users can go to the link given in terminal or go to `http://127.0.0.1:8000/health` via browser. The following response is expected:

```json
{"status":"healthy"}
```



### Example Request

Users can provide a natural language query in the POST request payload by including the question or request as the value of the "query" field in the JSON body. For example, you might ask for travel recommendations or information using everyday language:

```json
POST /travel-assistant
Content-Type: application/json

{
  "query": "I'm looking for a beach destination in July. I depart from London."
}
```

The API would run and return a response with the following body:

```json
{
    "destination": "Montego Bay",
    "reason": "Beautiful beaches with excellent summer weather.",
    "budget": "Moderate to High",
    "tips": [
        "Visit Doctor’s Cave Beach for a classic experience.",
        "Explore the Martha Brae River by bamboo raft.",
        "Try local jerk chicken at Scotchies."
    ],
    "hotel": {
        "name": "Secrets Wild Orchid",
        "city": "Montego Bay",
        "price_per_night": 340.0,
        "rating": 4.7
    },
    "flight": {
        "airline": "Virgin Atlantic",
        "from_airport": "LHR",
        "to_airport": "MBJ",
        "price": 1200.0,
        "duration": "PT9H",
        "date": "2023-07-07"
    },
    "experience": {
        "name": "Catamaran Cruise & Snorkeling",
        "city": "Montego Bay",
        "price": 85.0,
        "duration": "PT4H"
    }
}
```


# Further Issues

- The `price` field in the seed data is obfuscated for privacy or licensing reasons, but this field is required in the API response. Currently, the GenAI model may not process or infer the correct price, so returned prices may be inaccurate or placeholder values.

