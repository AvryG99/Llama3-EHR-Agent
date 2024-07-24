# LLM-Powered Code Generation and Verification System

## Overview

This repository contains a sophisticated system designed to generate, execute, and verify Python code using a large language model (LLM). The core functionality includes querying an LLM to generate SQL-based Python scripts, executing those scripts, and verifying the correctness of the outputs against expected results. The project leverages a combination of agents, including a primary LLM agent for code generation, a verification agent to validate outputs, and a long-term memory system for improving future queries based on past successful code generations.

## Features

- **Code Generation**: Generates Python code snippets based on natural language queries.
- **Code Execution**: Executes the generated Python code and captures the output.
- **Output Verification**: Verifies the correctness of the code output using an LLM-based verification agent.
- **Long-Term Memory**: Stores past successful queries and their generated code to enhance future code generation.
- **Logging**: Maintains detailed logs of all interactions, including queries, generated code, execution results, and verification outcomes.

## Project Structure


markdown
Copy code
# LLM-Powered Code Generation and Verification System

## Overview

This repository contains a sophisticated system designed to generate, execute, and verify Python code using a large language model (LLM). The core functionality includes querying an LLM to generate SQL-based Python scripts, executing those scripts, and verifying the correctness of the outputs against expected results. The project leverages a combination of agents, including a primary LLM agent for code generation, a verification agent to validate outputs, and a long-term memory system for improving future queries based on past successful code generations.

## Features

- **Code Generation**: Generates Python code snippets based on natural language queries.
- **Code Execution**: Executes the generated Python code and captures the output.
- **Output Verification**: Verifies the correctness of the code output using an LLM-based verification agent.
- **Long-Term Memory**: Stores past successful queries and their generated code to enhance future code generation.
- **Logging**: Maintains detailed logs of all interactions, including queries, generated code, execution results, and verification outcomes.

## Project Structure

```
your_project/
|-- init.py
|-- agent.py
|-- main.py
|-- llm_invocation.py
|-- prompt_generation.py
|-- test/
| |-- init.py
| |-- benchmark.py
| |-- verification_agent.py
|-- logs/
|-- result/
|-- longterm_memory.json
```


## Components

### `agent.py`
The primary agent responsible for querying the LLM, generating Python code, executing it, and verifying the results. It also handles logging and interaction with the long-term memory.

### `main.py`
The main entry point of the application, initializing the LLM agent and processing a sample query to demonstrate functionality.

### `llm_invocation.py`
Contains functions to interact with the LLM, sending prompts and receiving responses.

### `prompt_generation.py`
Generates prompts for querying the LLM based on user-provided questions.

### `test/benchmark.py`
A benchmarking script to test the system's performance. It runs queries through the LLM agent and uses the verification agent to check results.

### `test/verification_agent.py`
An agent dedicated to verifying the output of the generated code against expected results using the LLM.

## Getting Started

### Prerequisites
- Python 3.8+
- Local Llama3:8B via Ollama

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your_username/your_project.git
    cd your_project
    ```

2. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. To run the main application:
    ```bash
    python main.py
    ```

2. To run the benchmark tests:
    ```bash
    python -m test.benchmark
    ```

---

This repository aims to showcase the power of LLMs in generating and verifying code, providing a robust framework for future enhancements and applications in various domains.
