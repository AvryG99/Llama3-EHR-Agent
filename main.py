from agent import LLMQueryAgent

def main(question):
    agent = LLMQueryAgent(question)
    result, output = agent.run()
    return result, output
if __name__ == "__main__":
    question = "What is the list of patients in Medical Record?"
    result, output = main(question)
