import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import evaluate_pronunciation

def manual_test():
    # Test case 1: Basic test
    audio_file = "d:\\AI2\\pronunciation_trainer\\test_data\\test_hello_world.wav"
    expected_text = "hello world"
    
    print("Testing with:", audio_file)
    print("Expected text:", expected_text)
    
    try:
        result = evaluate_pronunciation(audio_file, expected_text)
        print("\nResults:")
        print(f"Spoken text: {result['spoken_text']}")
        print(f"Overall accuracy: {result['total_accuracy']:.2f}%")
        print("\nWord-by-word results:")
        for word in result['word_results']:
            print(f"Word: {word['expected']} -> {word['spoken']} (Accuracy: {word['accuracy']:.2f}%)")
    except Exception as e:
        print("Error occurred:", str(e))

if __name__ == "__main__":
    manual_test()