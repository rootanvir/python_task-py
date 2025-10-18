import re
from samsung_scraper import SamsungScraper
from samsung_advisor import SamsungAdvisor
from rag_module import RAGModule
from multi_agent_system import MultiAgentSystem
from response_composer import ResponseComposer
import requests


def demo_data_collection():
    print("\n Demo: Data Collection from GSMArena\n")
    scraper = SamsungScraper()
    print("→ Scraping Samsung phones from GSMArena...")
    # scraper.scrape_to_csv()  # Uncomment if you want actual scraping
    scraper.close_driver()
    print("Data scraping demo complete.\n")


def demo_move_csv_to_postgresql():
    print("\n Demo: Move CSV Data to PostgreSQL\n")
    scraper = SamsungScraper()
    scraper.csv_to_postgresql()
    scraper.close_driver()
    print(" CSV data successfully loaded into PostgreSQL.\n")


def demo_user_interaction():
    print("\n Demo: User Interaction (Natural Questions)\n")
    advisor = SamsungAdvisor()

    q1 = "What are the specs of Samsung Galaxy F17?"
    q2 = "Compare Galaxy M17 and F17 for photography."
    q3 = "Which Samsung phone has the best battery under $1000?"

    print(f" {q1}")
    print(advisor.get_specs("Galaxy F17"), "\n")

    print(f" {q2}")
    advisor.compare_phones("Galaxy M17", "Galaxy F17")

    print(f" {q3}")
    print(advisor.best_battery_under(1000))
    print("\n User interaction demo complete.\n")


def demo_rag_module():
    print("\n Demo: RAG Module (Retrieval-Augmented Generation)\n")
    scraper = SamsungScraper()
    rag = RAGModule(scraper.db_config)

    q1 = "What is the price of Galaxy M17?"
    q2 = "Compare Galaxy S25 Edge and Galaxy M17 for battery."

    print(f"{q1}")
    print(rag.answer(q1), "\n")

    print(f" {q2}")
    print(rag.answer(q2))
    scraper.close_driver()
    print("\n RAG module demo complete.\n")


def demo_multi_agent_system():
    print("\n Demo: Multi-Agent System + Response Composer\n")
    scraper = SamsungScraper()
    agents = MultiAgentSystem(scraper.db_config)
    composer = ResponseComposer()

    question_text = "Compare Galaxy S25 Edge and Galaxy M36"
    print(f"🧩 {question_text}")

    phone_names = re.findall(r"Galaxy\s\S+", question_text, re.IGNORECASE)
    if len(phone_names) != 2:
        print(" Could not parse two phone names from the question.")
        return

    phone1_list = agents.agent1(phone_names[0])
    phone2_list = agents.agent1(phone_names[1])

    if not phone1_list or not phone2_list:
        print(" One or both phones not found in the database.")
        return

    phone1_data = phone1_list[0]
    phone2_data = phone2_list[0]
    rag_data = {"phone1": phone1_data[0], "phone2": phone2_data[0]}

    # Agent 2 handles performance, camera, RAM, and recommendation internally
    comparison_text = agents.agent2(phone1_list, phone2_list)

    # Compose final answer (RAG + multi-agent)
    final_answer = composer.compose_response(rag_data, phone1_data, comparison_text)

    print("\n Answer:\n")
    print(final_answer)

    print("\n Multi-Agent system demo complete.\n")
    
    
    
def demo_response_composition_paragraph():
    print("\nDemo: Response Composition (Natural Answer)\n")

    scraper = SamsungScraper()
    rag = RAGModule(scraper.db_config)
    agents = MultiAgentSystem(scraper.db_config)

    # Hardcoded demo phones
    phone1_name = "Galaxy S25 Edge"
    phone2_name = "Galaxy M36"

    # Get RAG specs (as string)
    specs1_text = rag.answer(f"What are the specs of {phone1_name}?")
    specs2_text = rag.answer(f"What are the specs of {phone2_name}?")

    # Get DB rows for agent2 analysis
    phone1_list = agents.agent1(phone1_name)
    phone2_list = agents.agent1(phone2_name)

    if not phone1_list or not phone2_list:
        print(" One or both phones not found in the database.")
        scraper.close_driver()
        return

    # Multi-agent comparison (performance, camera, battery, etc.)
    comparison_text = agents.agent2(phone1_list, phone2_list)

    # Compose a clean, natural paragraph answer
    final_answer = (
        f"{phone1_name} has {specs1_text}. "
        f"Compared to {phone2_name}, {comparison_text} "
        f"Based on this analysis, {phone1_name if 'outperforms' in comparison_text else phone2_name} "
        f"is the recommended choice for photography, performance, and long usage."
    )

    print("\nFinal Answer:\n")
    print(final_answer)
    scraper.close_driver()

def ask_question(question_text):
    db_config = {
            "dbname": "phonesdb",
            "user": "postgres",
            "password": "1234",
            "host": "localhost",
            "port": "5432"
    }

    rag = RAGModule(db_config=db_config)
    agents = MultiAgentSystem(db_config=db_config)

    phone_names = re.findall(r"Galaxy\s\S+", question_text, re.IGNORECASE)
    if len(phone_names) != 2:
        return "Please provide exactly two Samsung models to compare."

    specs_text = rag.answer(phone_names[0])

    phone1_list = agents.agent1(phone_names[0])
    phone2_list = agents.agent1(phone_names[1])
    if not phone1_list or not phone2_list:
        return "One or both phones not found in the database."

    comparison_text = agents.agent2(phone1_list, phone2_list)

    final_answer = f"{specs_text}\nCompared to {phone_names[1]}, {comparison_text}"
    return final_answer




if __name__ == "__main__":
    print("\n==============================")
    print("Samsung Phone Advisor - Demo Menu")
    print("==============================\n")

    print("1  Demo Data Collection")
    print("2  Move CSV Data to PostgreSQL")
    print("3  Demo User Interaction")
    print("4  Demo RAG Module")
    print("5  Demo Multi-Agent System")
    print("6  Response Composition ")
    print("7  API ")
    print("0  Exit\n")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        demo_data_collection()
    elif choice == "2":
        demo_move_csv_to_postgresql()
    elif choice == "3":
        demo_user_interaction()
    elif choice == "4":
        demo_rag_module()
    elif choice == "5":
        demo_multi_agent_system()
    elif choice == "6":
        demo_response_composition_paragraph()
    elif choice == "7":
        ask_question("Compare Galaxy S25 Edge and Galaxy M17")
    else:
        print("Exiting program...")
