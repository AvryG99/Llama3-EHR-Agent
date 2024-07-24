import json
from verification_agent import VerificationAgent
import os 
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent import LLMQueryAgent
def save_to_memory(question: str, generated_code: str):
    memory_file = 'longterm_memory.json'
    memory_data = []

    if os.path.exists(memory_file):
        with open(memory_file, 'r') as file:
            memory_data = json.load(file)

    memory_data.append({"question": question, "generated_code": generated_code})

    with open(memory_file, 'w') as file:
        json.dump(memory_data, file, indent=4)

def benchmark(question):
    agent = LLMQueryAgent(question)
    result, output, code = agent.run()
    expected_output = "Emily Jones, John Doe"
    verifier = VerificationAgent(expected_output)
    verification_response = verifier.verify_output(output)
    
    return output, verification_response, code

if __name__ == "__main__":
    question = "Who are all the patients were prescripted to use Lisinopril?"
    output, verification_response, code = benchmark(question)

    print(f"Output: {output}")
    print(f"Verification Response: {verification_response}")
    print('Do you want to save this record to Long-term memory?')
    user_answer = input()
    if user_answer.lower() == 'yes':
        save_to_memory(question, code)
