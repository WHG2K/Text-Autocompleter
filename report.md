# Personalized Text Autocompletion System

## 1. Introduction

The task at hand is to design and implement a personalized text autocompletion system that assists users in their writing by suggesting text completions based on the current editing context and cursor position. The system is intended to enhance writing efficiency by providing intelligent, context-sensitive suggestions, similar to tools like Cursor and Copilot, but focused on pure text (rather than code).

### 1.1 Project Scope

The system should:
- Automatically generate personalized text completions based on the user’s current position in a text.
- Consider various writing contexts such as:
  - Cursor position: whether the cursor is in the middle of a sentence or at its end.
  - Context length: how much of the preceding text is used to generate completions.
  - Completion length: how long the generated text should be.
  - Historical documents: the system can leverage past written documents to personalize suggestions.
  
### 1.2 Task Objective

The objective is to create a system that intelligently predicts what a user is most likely to write next based on the immediate context, past writing history, and predefined configurations.

---

## 2. System Design

### 2.1 Approach and Methodology

The core idea is to use a pre-trained language model to generate text completions based on the current position in the document, along with historical context. This project follows a modular design, where different aspects of the system (e.g., context length, cursor position, historical documents) are handled as configurable parameters to allow flexibility.

#### 2.1.1 Pre-trained Model Selection

The system uses a large pre-trained language model like Mistral-7B-Instruct-v0.2 from Hugging Face, which is fine-tuned for text generation tasks. This model is chosen for its high quality in understanding and generating coherent text sequences.

#### 2.1.2 Data Input

The input to the model is a combination of:
- The text preceding the cursor position (context).
- The cursor position (e.g., middle of the sentence or at the end).
- Historical documents (optional) to further personalize completions.

---

## 3. Evaluation Design

### 3.1 Dataset

The dataset used for evaluation is the BBC News dataset from Hugging Face, specifically `RealTimeData/bbc_news_alltime`. This dataset contains articles from BBC News, making it a good source of diverse, real-world text.

- [Dataset Link on Hugging Face](https://huggingface.co/datasets/RealTimeData/bbc_news_alltime)

This dataset will be used to test the autocompletion system by simulating different writing scenarios.

### 3.2 Experiment Setup

The evaluation involves testing the system under different conditions, which include:
- **Cursor position**: Testing both "sentence_middle" and "sentence_end" positions.
- **Context length**: Evaluating short, medium, and long context lengths.
- **Completion length**: Generating completions with varying lengths—short, medium, and long.
- **Use of historical documents**: Whether or not to use historical documents in the generation process.

Each test case simulates a scenario where the system generates completions for a batch of text, where each batch consists of 3 historical documents and 1 document to test. Given the 4 conditions (context length, cursor position, completion length, historical documents), each batch will involve 48 test cases (4*2*3*2=48).

### 3.3 Result Generation

The experiments will generate results in a CSV file (e.g., `experiments.csv`), which will contain the results for all test cases. For the chosen evaluation parameters (`n_batches=20`), the experiment will generate 20 batches of 48 cases each, totaling 960 results.

---

## 4. Evaluation Metrics

The evaluation focuses on measuring:
- **Accuracy**: How well the generated completions match what the user is likely to write.
- **Coherence**: The generated text’s consistency with the surrounding text.
- **Relevance**: How relevant the suggestions are to the current document and context.

These metrics will be quantified based on human evaluations as well as automated text similarity measures.

---

## 5. Implementation Details

The implementation follows a modular approach, with distinct components for:
1. **Text Input Handling**: Managing document input and cursor positions.
2. **Text Generation**: Using the pre-trained model for generating text completions.
3. **Evaluation and Results Logging**: Running experiments and saving the results.

The system is designed to be easily configurable with respect to the different parameters such as context length, cursor position, and completion length.

---

## 6. Future Work and Improvements

### 6.1 Model Improvements

While the current implementation uses a pre-trained model, there may be future work aimed at fine-tuning the model on more specific writing tasks to further improve its accuracy and relevance for text completions.

### 6.2 User Interface

An interactive interface for real-time text autocompletion could be developed in the future to allow users to experience the system more directly.

---

## 7. Conclusion

This report outlines the design and implementation of a personalized text autocompletion system that aids users in writing by generating relevant and coherent completions based on their immediate context and past writing history. The system was evaluated using a news dataset and tested across a range of scenarios, with future work directed at further improving the model and user experience.