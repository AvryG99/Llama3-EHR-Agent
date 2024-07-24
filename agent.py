import os
import re
import datetime
import io
import contextlib
import json
from llm_invocation import invoke_llm
from prompt_generation import generate_prompt
import pyodbc
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class LLMQueryAgent:
    def __init__(self, question: str):
        self.question = question
        self.log_file = "logs/log.txt"
        self.result_folder = "result"
        self.memory_file = 'longterm_memory.json'
        self.max_attempts = 3

        if not os.path.exists(os.path.dirname(self.log_file)):
            os.makedirs(os.path.dirname(self.log_file))
        if not os.path.exists(self.result_folder):
            os.makedirs(self.result_folder)

    def get_past_memory(self) -> str:
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as file:
                memory_data = json.load(file)
                # Find the most related question
                related_memory = max(memory_data, key=lambda x: self.calculate_similarity(x["question"], self.question))
                return related_memory["generated_code"]
        return ""

    def calculate_similarity(self, past_question: str, current_question: str) -> float:
        vectorizer = TfidfVectorizer()

        documents = [past_question, current_question]

        tfidf_matrix = vectorizer.fit_transform(documents)

        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        return similarity_matrix[0][0]

    def get_python_code(self) -> tuple[str, str]:
        past_code = self.get_past_memory()
        prompt = generate_prompt(self.question)
        if past_code:
            prompt += f"\nHere is a similar code that was generated successfully in the past:\n{past_code}"
        response = invoke_llm(prompt)
        print(response)
        code = self.extract_code(response)
        return code, response

    def extract_code(self, response: str) -> str:
        code_match = re.search(r'```(?:Python|python|)\n(.*?)\n```', response, re.DOTALL)
        if code_match:
            return code_match.group(1)
        return ""

    def try_execute_code(self, code: str) -> tuple[bool, str, str]:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output = io.StringIO()
        output_str = ""
        try:
            exec(code)
            with contextlib.redirect_stdout(output):
                exec(code)

            output_str = output.getvalue()
            output.close()

            filename = os.path.join(self.result_folder, f"generated_script_{timestamp}.py")
            with open(filename, "w") as file:
                file.write(code)
            return True, filename, output_str
        except Exception as e:
            return False, str(e), output_str

    def debug_code(self, code: str) -> tuple[bool, str, str, int]:
        attempts = 0
        while attempts < self.max_attempts:
            success, result, output = self.try_execute_code(code)
            if success:
                return True, result, output, attempts + 1
            else:
                attempts += 1
                new_prompt = f'''The following code has an error:\n{code}\nError message: {result}
                                Please return the full code only (From connecting to database to create a query and to creating the connection string and print out the result).
                                No additional explanation.
                            '''
                response = invoke_llm(new_prompt)
                print(response)
                code = self.extract_code(response)
        output = f"Error: {result}"
        return False, result, output, attempts

    def save_to_log(self, question: str, output: str, attempts: int, code_path: str, status: str, stage: str):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as log_file:
            log_file.write("=" * 50 + "\n")
            log_file.write(f"Time: {timestamp}\n")
            log_file.write(f"Question: {question}\n")
            log_file.write(f"Answer: {output}\n")
            log_file.write(f"Code Iterations: {attempts}\n")
            log_file.write(f"Python Code Directory: {code_path}\n")
            log_file.write(f"Status: {status}\n")
            log_file.write(f"Stage: {stage}\n")
            log_file.write("=" * 50 + "\n")

    def run(self) -> tuple[str, str]:
        code, initial_response = self.get_python_code()
        success, result, output, attempts = self.debug_code(code)
        status = "Success" if success else "Fail"
        code_path = result if success else None
        self.save_to_log(self.question, output, attempts, code_path, status, "Final")
        if success:
            return result, output, code
