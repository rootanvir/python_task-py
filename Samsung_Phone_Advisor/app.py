from fastapi import FastAPI
from pydantic import BaseModel
from response_composer import ResponseComposer
from samsung_scraper import SamsungScraper
from multi_agent_system import MultiAgentSystem


app = FastAPI(title="Samsung Phone Advisor API")

# Input model for /ask endpoint
class Question(BaseModel):
    question: str

# Initialize agents and composer once at startup
scraper = SamsungScraper()
agents = MultiAgentSystem(scraper.db_config)
composer = ResponseComposer()

@app.post("/ask")
def ask_question(q: Question):
    question_text = q.question.lower()

    # Extract phone names (very simple, improve regex if needed)
    import re
    phone_names = re.findall(r"galaxy\s\S+", question_text, re.IGNORECASE)

    if len(phone_names) < 1:
        return {"answer": " Please provide at least one phone model."}
    elif len(phone_names) == 1:
        # Only one phone → return specs
        phone_list = agents.agent1(phone_names[0])
        if not phone_list:
            return {"answer": f"Could not find {phone_names[0]} in database."}
        phone_data = phone_list[0]
        rag_data = {"phone1": phone_data[0], "phone2": "N/A"}
        answer = composer.compose_response(rag_data, phone_data, "Specifications retrieved.")
        return answer
    else:
        # Two phones → comparison
        phone1_list = agents.agent1(phone_names[0])
        phone2_list = agents.agent1(phone_names[1])
        if not phone1_list or not phone2_list:
            return {"answer": "One or both phones not found in the database."}

        phone1_data = phone1_list[0]
        phone2_data = phone2_list[0]

        rag_data = {"phone1": phone1_data[0], "phone2": phone2_data[0]}
        comparison_text = agents.agent2(phone1_list, phone2_list)

        answer = composer.compose_response(rag_data, phone1_data, comparison_text)
        return answer
