# Text-Autocompleter

## Overview
`Text-Autocompleter` is a toy implementation of a text autocompletion module designed to generate personalized text completions based on the user's existing documents and cursor position. The system utilizes Hugging Face's Mistral-7B-Instruct-v0.2 model for text generation and can provide completions with different lengths and contextual settings.

## Features
- **Text completion**: Generate text completions based on text before and after the cursor.
- **Historical context**: Optionally incorporate historical documents for personalized completions.
- **Flexible context and completion lengths**: Supports short, medium, and long completion lengths.
- **Cursor position handling**: Allows splitting text based on cursor positions (e.g., sentence middle or sentence end).

## Project Structure
- `src/`: Contains the main implementation files.
  - `text_completer.py`: The core module for text completion using the Hugging Face API.
  - `text_processors.py`: Utility functions for processing text, including splitting paragraphs and generating context samples.
- `main.py`: Runs the experiment to test different configurations of text completion.
- `toy_example.py`: A simple example to demonstrate text completion with historical documents.
- `requirements.txt`: Lists the required dependencies for the project.
- `setup.py`: Installs the required dependencies.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/text-autocompleter.git
   cd text-autocompleter



# 文本补全系统评测框架

本项目旨在构建一个全面的文本补全系统评测框架，通过多维度的测试场景来评估系统性能。

## 核心评测场景

评测场景分为 5 大类，每类包含多个细分场景，以确保测试的全面性：

### 1. 文本类型（内容领域）
- 新闻（BBC News）
- 学术论文（待添加）
- 小说/文学（待添加）

**评测目标**：验证系统在不同语言风格和写作需求下的适应能力

### 2. 光标位置
- 句中插入
- 句尾补全
- 段落中间补全
- 段落结尾补全

**评测目标**：
- 测试句子级和段落级的补全能力
- 验证补全内容的上下文连贯性

### 3. 上下文长度
- 短上下文（<50 tokens）
- 中等上下文（50-200 tokens）
- 长上下文（>500 tokens）

**评测目标**：
- 验证不同长度上下文下的理解能力
- 测试信息利用的充分性

### 4. 补全长度
- 短补全（1-2词）(方法：限制max_new_tokens=5, 并且遇到任何标点时停止)
- 中等补全（1句）(方法：限制max_new_tokens=20, min_new_tokens=5, 并且遇到句号时停止)
- 长补全（1段）(方法：限制max_new_tokens=50, min_new_tokens=20) 可以设置stopingcritaria使其不要生成下一段，但是暂时还没有实现这一功能。

**评测目标**：
- 确保各种长度补全的合理性
- 验证长文本补全的连贯性

### 5. 额外信息利用
- 无额外资料
- 有历史文档参考