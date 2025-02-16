from datasets import load_dataset
import random
from typing import List, Tuple

def get_news_content(idx: int) -> str:
    """Get the content of a news article from the RealTimeData/bbc_news_alltime dataset by index."""
    dataset = load_dataset("RealTimeData/bbc_news_alltime", "2024-01")
    article = dataset["train"][idx]
    return article['content']

def split_into_paragraphs(text: str) -> List[str]:
    """Split text into paragraphs."""
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    return paragraphs

def get_context_samples(text: str, context_length: str = "no") -> List[str]:
    """Get sample paragraphs based on context length."""
    # Check if context_length is valid
    valid_context_lengths = ["no", "short", "medium", "long"]
    if context_length not in valid_context_lengths:
        raise ValueError(f"Invalid context length: {context_length}. Must be one of {valid_context_lengths}")
    
    paragraphs = split_into_paragraphs(text)
    n = len(paragraphs)
    
    if context_length == "no":
        if n < 2:
            return paragraphs
        start_idx = random.randint(0, n - 2)
        return paragraphs[start_idx:start_idx + 2]
    
    elif context_length == "short":
        if n < 4:
            return paragraphs
        start_idx = random.randint(0, n - 4)
        return paragraphs[start_idx:start_idx + 4]
    
    elif context_length == "medium":
        if n < 8:
            return paragraphs
        start_idx = random.randint(0, n - 8)
        return paragraphs[start_idx:start_idx + 8]
    
    else:  # long
        return paragraphs

def split_by_cursor_position(paragraphs: List[str], cursor_position: str = "sentence_middle") -> Tuple[str, str, str]:
    """Split paragraphs into before and after cursor, and return the hidden original part."""
    # Check if cursor_position is valid
    valid_cursor_positions = ["sentence_middle", "sentence_end"]
    if cursor_position not in valid_cursor_positions:
        raise ValueError(f"Invalid cursor position: {cursor_position}. Must be one of {valid_cursor_positions}")
    
    n = len(paragraphs)
    split_idx = n // 2
    
    after_cursor = "\n".join(paragraphs[(split_idx+1):])
    
    mid_paragraph = paragraphs[split_idx - 1]
    
    if cursor_position == "sentence_middle":
        positions = []
        for i, char in enumerate(mid_paragraph[:-1]):
            if char not in ".!?" and mid_paragraph[i+1] not in ".!?":
                positions.append(i)
        
        if not positions:
            print("No suitable position found")
            return "", after_cursor.lstrip(), (mid_paragraph + "\n" + paragraphs[split_idx]).lstrip()
            
        split_pos = random.choice(positions)
        mid_before = mid_paragraph[:split_pos + 1]
        hidden_original = mid_paragraph[split_pos + 1:] + "\n" + paragraphs[split_idx]
        
    else:  # sentence_end
        positions = [i for i, char in enumerate(mid_paragraph) if char == '.']
        
        if not positions:
            print("No period found")
            return "", after_cursor.lstrip(), (mid_paragraph + "\n" + paragraphs[split_idx]).lstrip()
            
        split_pos = random.choice(positions)
        mid_before = mid_paragraph[:split_pos + 1]
        hidden_original = mid_paragraph[split_pos + 1:] + "\n" + paragraphs[split_idx]
    
    before_paragraphs = paragraphs[:split_idx - 1]
    before_cursor = "\n".join(before_paragraphs + [mid_before])
    
    return before_cursor.lstrip(), after_cursor.lstrip(), hidden_original.lstrip()

def get_test_batch(start_idx: int) -> Tuple[List[str], str]:
    """Get a batch of test data."""
    dataset = load_dataset("RealTimeData/bbc_news_alltime", "2024-01")
    
    # Get 3 historical articles
    history_docs = []
    for i in range(3):
        article = dataset["train"][start_idx + i]
        history_docs.append(article['content'])
    
    # Get the test article
    test_content = dataset["train"][start_idx + 3]['content']
    return history_docs, test_content

if __name__ == "__main__":
    # Perform two batch tests
    for batch in range(2):
        print(f"\n\nBatch {batch + 1}:")
        print("=" * 80)
        
        # Get test data
        history_docs, test_content = get_test_batch(batch * 4)
        if not test_content:
            print(f"Batch {batch + 1} did not find a suitable test article")
            continue
            
        # Print historical documents
        print("\nHistorical Documents:")
        print("-" * 40)
        for i, doc in enumerate(history_docs):
            print(f"\nHistorical Document {i}:")
            print(doc[:200] + "...")  # Only show the first 200 characters
        
        # Test different context lengths
        print("\nTest Article:")
        print("-" * 40)
        print(test_content[:200] + "...")  # Only show the first 200 characters
        
        for context_length in ["no", "short", "medium", "long"]:
            print(f"\n{context_length.upper()} CONTEXT:")
            print("=" * 80)
            
            context_paragraphs = get_context_samples(test_content, context_length)
            if not context_paragraphs:
                print("Insufficient number of paragraphs")
                continue
            
            # Display the selected paragraphs
            print("\nSelected Paragraphs:")
            print("-" * 40)
            for j, p in enumerate(context_paragraphs):
                print(f"\nParagraph {j}:")
                print(p)
            
            # Test different cursor positions
            for cursor_position in ["sentence_middle", "sentence_end"]:
                print(f"\n{cursor_position.upper()} CURSOR POSITION:")
                print("-" * 40)
                
                before, after, hidden_original = split_by_cursor_position(context_paragraphs, cursor_position)
                print("\nBEFORE CURSOR:")
                print(before)
                print("\nAFTER CURSOR:")
                print(after)
                print("\nHIDDEN ORIGINAL:")
                print(hidden_original)
                
            print("=" * 80) 