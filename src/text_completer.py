from typing import List
import requests

class TextCompleter:
    def __init__(self, api_token):
        """Initialize the text completer"""
        self.api_token = api_token
        
        # Configure the generator
        self.generator = {
            "url": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
            "config": {
                "max_new_tokens": 5,  # Max generation length
                "min_new_tokens": 1,  # Min generation length
                "stop": [], # Stop tokens
                "num_return_sequences": 1, # Number of return sequences
                "do_sample": True,
                "temperature": 0.3,
                "top_p": 0.7,
                "return_full_text": False,
                "repetition_penalty": 1.2,
                "length_penalty": 1,
                "eos_token_id": [50256],
            }
        }
        self.max_after_cursor_tokens = 8000  # Max tokens for after cursor
        self.max_before_cursor_tokens = 8000  # Max tokens for before cursor
        self.max_history_tokens = 8000  # Max total tokens for history documents

    def _call_generator_api(self, prompt: str) -> str:
        """Call the generation model API"""
        headers = {"Authorization": f"Bearer {self.api_token}"}
        
        try:
            response = requests.post(
                self.generator["url"],
                headers=headers,
                json={
                    "inputs": prompt,
                    "parameters": self.generator["config"]
                }
            )
            
            if response.status_code == 200:
                response_json = response.json()
                if isinstance(response_json, list) and len(response_json) > 0:
                    return response_json[0].get("generated_text", "")
            
            raise Exception(f"API call failed with status code {response.status_code}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return ""

    def complete_text(self, before_cursor, after_cursor, history_docs=None, completion_length="short"):
        """Generate text based on different completion lengths
        
        Args:
            before_cursor: Text before the cursor
            after_cursor: Text after the cursor
            history_docs: Optional list of historical documents
            completion_length: Length of completion ('short', 'medium', 'long')
        """
        completion_params = {
            "short": {"max_new_tokens": 5, "min_new_tokens": 1, "stop": [".", ",", ";", ":"], "length_penalty": 1.5},
            "medium": {"max_new_tokens": 20, "min_new_tokens": 5, "stop": ["."], "length_penalty": 1.0},
            "long": {"max_new_tokens": 50, "min_new_tokens": 20, "stop": [], "length_penalty": 0.5}
        }
        
        params = completion_params.get(completion_length, completion_params["short"])
        self.generator["config"].update(params)
        
        prompt = self._build_prompt(before_cursor, after_cursor, history_docs)
        
        completion = self._call_generator_api(prompt)
        return completion.strip()

    def _build_prompt(self, before_cursor: str, after_cursor: str, history_docs: List[str] = None) -> str:
        """Build the prompt text
        
        Args:
            before_cursor: Text before the cursor
            after_cursor: Text after the cursor
            history_docs: List of historical documents
        """
        # If the before text is too long, keep the last part
        before_cursor = self._truncate_text_to_tokens(before_cursor, self.max_before_cursor_tokens, keep_start=False)
        
        # If the after text is too long, keep the first part
        after_cursor = self._truncate_text_to_tokens(after_cursor, self.max_after_cursor_tokens, keep_start=True)

        if (not history_docs) or (len(history_docs) == 0):
            prompt = f"{after_cursor}\n\n{before_cursor}"
        else:
            # Combine historical documents
            history = "\n\n".join(history_docs)
            # If the history is too long, truncate using tokenizer
            history = self._truncate_text_to_tokens(history, self.max_history_tokens)
            prompt = f"""{history}\n\n{after_cursor}\n\n{before_cursor}"""
        
        return prompt

    def _truncate_text_to_tokens(self, text: str, max_tokens: int, keep_start: bool = True) -> str:
        """Truncate text to a specified number of tokens"""
        # Split the entire text into words (tokens) by spaces
        tokens = text.split()
        
        # Decide truncation method based on keep_start parameter
        if keep_start:
            # Keep the first part of the text
            truncated_text = ' '.join(tokens[:max_tokens])
        else:
            # Keep the last part of the text
            truncated_text = ' '.join(tokens[-max_tokens:])
        
        return truncated_text 