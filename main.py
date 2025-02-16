import csv
from src.text_completer import TextCompleter
from dotenv import load_dotenv
import os
import argparse
from src.text_processors import get_test_batch, get_context_samples, split_by_cursor_position

def run_experiments(n_batches: int = 1):
    # Load environment variables
    load_dotenv()
    api_token = os.getenv("HF_API_TOKEN")
    if not api_token:
        raise ValueError("HF_API_TOKEN environment variable not found")
    
    completer = TextCompleter(api_token)
    
    # Open CSV file to write results
    with open('experiments.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["BATCH", "CONTEXT LENGTH", "CURSOR POSITION", "COMPLETION LENGTH", "WITH HISTORY", "BEFORE CURSOR", "AFTER CURSOR", "GENERATED TEXT", "HIDDEN MASKET TEXT"])
        
        # Perform two batch tests
        for batch in range(n_batches):
            print(f"\nBatch {batch + 1}")
            print("=" * 80)
            
            # Get test data
            history_docs, test_content = get_test_batch(batch * 4)
            if not test_content:
                print(f"Batch {batch + 1} did not find a suitable test article")
                continue
                
            # Test different context lengths
            for context_length in ["no", "short", "medium", "long"]:
                context_paragraphs = get_context_samples(test_content, context_length)
                if not context_paragraphs:
                    print("Insufficient number of paragraphs")
                    continue
                
                # Test different cursor positions
                for cursor_position in ["sentence_middle", "sentence_end"]:
                    before, after, hidden_original = split_by_cursor_position(context_paragraphs, cursor_position)
                    
                    # Process before and after text
                    before_cursor = ("..." if len(before) > 200 else "") + (before[-200:] if len(before) > 200 else before)
                    after_cursor =  (after[:200] if len(after) > 200 else after) + ("..." if len(after) > 200 else "")
                    
                    # Test different completion lengths
                    for completion_length in ["short", "medium", "long"]:
                        # Test with and without historical documents
                        for with_history in [True, False]:
                            history = history_docs if with_history else None
                            generated_text = completer.complete_text(before, after, history_docs=history, completion_length=completion_length)
                            
                            # Write to CSV
                            writer.writerow([batch + 1, context_length, cursor_position, completion_length, with_history, before_cursor, after_cursor, generated_text, hidden_original])
                            
                            # Print test case details
                            print("\nTest Parameters:")
                            print(f"- Context Length: {context_length}")
                            print(f"- Cursor Position: {cursor_position}")
                            print(f"- Completion Length: {completion_length}")
                            print(f"- With History: {with_history}")
                            
                            print("\nBefore Cursor:")
                            print(before_cursor)
                            
                            print("\nGenerated Text:")
                            print(f"[{generated_text}]")
                            
                            print("\nAfter Cursor:")
                            print(after_cursor)
                            
                            print("-" * 80)

if __name__ == "__main__":
    # Set up command line argument parser
    parser = argparse.ArgumentParser(description='Run text completion experiments')
    parser.add_argument('--n_batches', type=int, default=1,
                      help='Number of batches to run (default: 1)')
    
    args = parser.parse_args()
    run_experiments(n_batches=args.n_batches)