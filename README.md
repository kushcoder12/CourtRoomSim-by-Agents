# AI Courtroom Simulation

A sophisticated AI simulation of a courtroom debate between opposing sides in a legal case. This project leverages multiple AI language models to simulate a judge and two opposing counsel in a structured courtroom proceeding.

## Overview

This simulation focuses on a case regarding the rights of book authors versus LLM companies in the use of copyrighted literary works for AI training. The system features:

- AI-powered Judge that evaluates legal arguments
- Two opposing counsels (one for book authors, one for LLM companies)
- Document-based context retrieval for informed arguments
- Structured courtroom proceedings (opening statements, rebuttals, closing arguments)
- Scoring system for evaluating legal reasoning, evidence, and persuasiveness
- Final verdict based on cumulative scores

## Requirements

- Python 3.8+
- PyTorch
- Transformers library (Hugging Face)
- LangChain
- FAISS vector database

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/courtroomsim.git
cd courtroomsim
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Prepare your document files and models (see below)

## Project Structure

```
courtroomsim/
├── app/                    # Main application package
│   ├── models/             # Model handling components
│   │   ├── model_loader.py # Loading AI models
│   │   └── document_indexer.py # Document processing
│   ├── utils/              # Utility functions
│   │   └── text_processing.py # Text cleaning and processing
│   ├── config.py           # Configuration settings
│   ├── lawyers.py          # Counsel agents
│   ├── judge.py            # Judge agent
│   └── simulation.py       # Main simulation orchestrator
├── data/                   # Data directory
│   └── inputs/             # Input documents
├── main.py                 # Entry point script
└── requirements.txt        # Project dependencies
```

## Data Preparation

The simulation requires two text documents:

1. A document supporting book authors' rights (`for_motion.txt`)
2. A document supporting LLM companies' rights (`against_motion.txt`)

Place these in the `data/inputs/` directory or specify custom paths when running the simulation.

## Models

The simulation requires three transformer models from Hugging Face:

1. Judge model: A language model for evaluating arguments
2. Lawyer "for" model: A language model for the book authors' counsel
3. Lawyer "against" model: A language model for the LLM companies' counsel

You can use models like:
- DeepSeek
- Qwen
- Llama 2/3
- Mistral
- Other similar LLMs

## Usage

Run the simulation with custom paths:

```bash
python main.py \
  --judge_model /path/to/judge/model \
  --lawyer_for_model /path/to/lawyer/for/model \
  --lawyer_against_model /path/to/lawyer/against/model \
  --for_motion_doc data/inputs/for_motion.txt \
  --against_motion_doc data/inputs/against_motion.txt \
  --output courtroom_transcript.txt
```

## Output

The simulation generates a transcript file containing:
- Opening statements from both sides
- Two rounds of rebuttals
- Closing arguments
- Judge's evaluations
- Score summary
- Final verdict

## Example Configuration

For large-scale models, you may need advanced configuration. Here's an example:

```bash
# Using DeepSeek-r1 for Judge and Qwen models for lawyers
python main.py \
  --judge_model models/deepseek-r1-distill-qwen-1.5b \
  --lawyer_for_model models/qwen-1.5b \
  --lawyer_against_model models/qwen-0.5b-instruct-gptq-int8 \
  --output courtroom_transcript.txt
```

## Custom Case Descriptions

You can provide a custom case description:

```bash
python main.py \
  --case_description "This case concerns the rights of musicians versus streaming platforms..." \
  [other arguments...]
```

## License

[MIT License](LICENSE)

## Acknowledgements

This project was inspired by legal AI applications and the potential for AI to simulate complex human interactions like courtroom proceedings. 