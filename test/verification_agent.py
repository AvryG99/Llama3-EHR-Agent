import os 
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm_invocation import invoke_llm

class VerificationAgent:
    def __init__(self, expected_output: str):
        self.expected_output = expected_output

    def verify_output(self, actual_output: str) -> bool:
        examples =  '''
                    Example 1:
                    -Actual output: [(Emily, Johnson), (Nicky, Tom)]
                    -Expected output: Emily Johnson, Nicky Tom
                    -> The result should be correct no matter the data types

                    Example 2:
                    -Actual output: [(1, Amoxicillin), (3, Lisinopril)]
                    -Expected output: Lisinopril, Amoxicillin
                    -> The result should be correct no matter the data types

                    Example 3:
                    --Actual output: [(95 mg/dL)]
                    -Expected output: 75 mg/dL
                    -> The result should be incorrect no matter the data types
                    '''
        prompt = f'''The following is the expected output for a query:\n{self.expected_output}\n
                    The actual output is:\n{actual_output}\n
                    Does the information of the actual output match the expected output?
                    The data type of actual output should be a tuple and the expected output is a string.
                    The difference between data types won't affect the result.
                    If the datatypes are different but the content is correct, the result is still correct.
                    Here is the examples for: {examples}
                '''
        response = invoke_llm(prompt)
        return response
