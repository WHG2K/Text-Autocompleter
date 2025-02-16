from src.text_completer import TextCompleter
from dotenv import load_dotenv
import os
import argparse

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Text completion with different completion lengths')
    parser.add_argument('--completion_length', type=str, choices=['short', 'medium', 'long'],
                      default='medium', help='Specify completion length (short/medium/long)')
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    api_token = os.getenv("HF_API_TOKEN")
    if not api_token:
        raise ValueError("HF_API_TOKEN environment variable not found")
    
    completer = TextCompleter(api_token)
    
    # Provide historical documents (AI in Healthcare)
    history_docs = [
        """Artificial Intelligence has revolutionized healthcare diagnostics through advanced medical imaging analysis. 
        Deep learning algorithms have demonstrated remarkable accuracy in detecting various conditions, from cancer to 
        cardiovascular diseases. These AI systems can analyze X-rays, MRIs, and CT scans with precision that sometimes 
        exceeds human capabilities. For example, in mammography screening, AI-assisted systems have shown a significant 
        reduction in false positives while maintaining high sensitivity in detecting early-stage breast cancer.""",
        
        """The integration of AI in electronic health records (EHR) has transformed patient care management. 
        Machine learning algorithms can now predict patient risks, recommend personalized treatment plans, and 
        identify potential drug interactions. These systems analyze vast amounts of patient data, including medical 
        history, genetic information, and lifestyle factors, to provide comprehensive health insights. Healthcare 
        providers can use these AI-driven insights to make more informed decisions and improve patient outcomes.""",
        
        """AI-powered robotic surgery represents another breakthrough in medical technology. These systems combine 
        computer vision, machine learning, and precision robotics to assist surgeons in performing complex procedures. 
        The AI components can analyze real-time surgical data, provide guidance for optimal instrument placement, and 
        even predict potential complications during surgery. This has led to increased precision, reduced recovery 
        times, and improved surgical outcomes across various specialties."""
    ]
    
    # Provide before_cursor and after text (AI generated)
    before_cursor = """The impact of these advancements has been profound, leading to new applications 
    in various industries. One of the most notable """
    
    after_cursor = """This has resulted in increased efficiency and productivity, as well as the 
    creation of new job opportunities in the tech sector."""
    
    # Print historical documents
    print("\nHISTORICAL DOCUMENTS:")
    print("=" * 80)
    for i, doc in enumerate(history_docs, 1):
        print(f"\nDocument {i}:")
        print(doc[:200] + "..." if len(doc) > 200 else doc)
    
    # Print before cursor
    print("\nBEFORE CURSOR:")
    print("=" * 80)
    print(before_cursor)
    
    # Generate and print the completion
    generated_text = completer.complete_text(before_cursor, after_cursor, history_docs=history_docs, completion_length=args.completion_length)
    print("\nGENERATED TEXT:")
    print("=" * 80)
    print(f"<<{generated_text}>>")
    
    # Print after cursor
    print("\nAFTER CURSOR:")
    print("=" * 80)
    print(after_cursor)