OpenAI Test
===

The objective of this repository is to test the openai recommendations based on different user queries.
Given user queries and a prompt, the script will return a csv containing the results for all the queries for that prompt.

# Installation

## Prerequisites

* Python>=9

## Setup

```bash
bash ./install.sh
source venv/bin/activate
```

# Run tests

In order to run tests, you will need to populate the user_queries.csv files located in the src directory.
Each row of the file contains a user query to be tested.

For each query, the script will test a prompt that you can define using the prompt.txt file located in the src directory.

Modify it as you like. Two elements to take into account when editing the file:
* The `%QUERY%` string should not be deleted. You may place it wherever you want. It will be replaced by the user query.
* The `%PRODUCTS%` string should not be deleted. You may place it wherever you want. It will be replaced by the actual recommended products.

To run the script, you will first need an openai key. To use it, run the following command in the terminal:
```bash
export OPENAI_API_KEY=<YOUR_API_KEY>
```

Go to the src directory:
```bash
cd src/
```

Then, run the script:
```bash
python3 test_chat.py <NAME_OF_THE_RESULTS_FILE.csv>
```
