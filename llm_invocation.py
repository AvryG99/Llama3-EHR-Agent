from langchain_community.llms import Ollama

def invoke_llm(prompt: str) -> str:
    llm = Ollama(model="llama3")
    response = llm.invoke(prompt)
    return response
