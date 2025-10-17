class ResponseComposer:
    def __init__(self):
        pass

    def compose_response(self, rag_data, agent1_data, comparison_text):
        """
        Compose a concise, human-readable answer from the DB specs and comparison.
        """

        phone1 = rag_data.get("phone1", "Unknown Phone 1")
        phone2 = rag_data.get("phone2", "Unknown Phone 2")

        display = agent1_data[2] if len(agent1_data) > 2 else "N/A"
        battery = agent1_data[3] if len(agent1_data) > 3 else "N/A"
        camera = agent1_data[4] if len(agent1_data) > 4 else "N/A"

        answer = (
            f"{phone1} has a {display} display, {battery} battery, and {camera} camera. "
            f"Compared to {phone2}, {comparison_text}"
        )

        return {"answer": answer}
