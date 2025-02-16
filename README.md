# Text-Autocompleter

## Overview
`Text-Autocompleter` is a toy implementation of a text autocompletion module designed to generate personalized text completions based on the user's existing documents and cursor position. The system utilizes Hugging Face's Mistral-7B-Instruct-v0.2 model.

## Project Structure
- `src/`: Contains the main implementation files.
  - `text_completer.py`: The core module for text completion using the Hugging Face API.
  - `text_processors.py`: Utility functions for processing text, including splitting paragraphs and generating context samples.
- `main.py`: Runs the experiment to test different configurations of text completion.
- `toy_example.py`: A simple example to demonstrate text completion with historical documents.
- `requirements.txt`: Lists the required dependencies for the project.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/WHG2K/Text-Autocompleter
   cd Text-Autocompleter
   ```

2. **Install required dependencies**
    ```bash
   pip install -r requirements.txt
   ```

3. **Load the environment variables**: since the project uses the Hugging Face API, you need to set the `HF_API_TOKEN` environment variable to be your own Hugging Face API token. Create a `.env` file in the root directory and add your Hugging Face API token:
    ```bash
    HF_API_TOKEN=<your_hugging_face_api_token>
    ```

## Usage

### 1. **Run the toy example**:
To see a quick demonstration of text completion, use the `toy_example.py`:
```bash
python toy_example.py
```
You can modify the --completion_length argument to test different completion lengths (`short`, `medium`, or `long`). The default value is `medium`. For example, to test the short completion length, use:
```bash
python toy_example.py --completion_length short
```

### 2. **Run the experiment**:
The dataset used for the main experiment is [https://huggingface.co/datasets/RealTimeData/bbc_news_alltime](https://huggingface.co/datasets/RealTimeData/bbc_news_alltime). To run the experiment, use the `main.py` file by specifying the number of batches with the `--n_batches` argument (optional, default is 1).
```bash
python main.py --n_batches <number_of_batches>
```
Each batch contains:
- **3 historical documents** and **1 test document**.
- The experiment tests four variables:
  - **Context length**: "no", "short", "medium", or "long"
  - **Cursor position**: "sentence_middle" or "sentence_end"
  - **Completion length**: "short", "medium", or "long"
  - **Use of historical documents**: whether to include the historical documents in the context

Therefore, for each batch, the experiment will run **48 API calls** (4 context lengths * 2 cursor positions * 3 completion lengths * 2 historical document usage options).

The `--n_batches` argument controls how many batches to run, allowing you to scale up the experiment. The `experiments_0.csv` is the result of the experiment under `n_batches=20`, which corresponds to **960 entries** (20 batches * 48 API calls per batch).