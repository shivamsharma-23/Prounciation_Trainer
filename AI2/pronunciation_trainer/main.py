__all__ = ['evaluate_pronunciation']

from audio_utils import transcribe_audio
from word_matcher import get_word_accuracy

def evaluate_pronunciation(audio_file_path, expected_text):
    """
    Evaluate pronunciation by comparing speech with expected text
    """
    # Convert speech to text
    spoken_text = transcribe_audio(audio_file_path)
    
    # Compare and get accuracy
    results = get_word_accuracy(expected_text, spoken_text)
    
    # Calculate overall accuracy
    total_accuracy = sum(r['accuracy'] for r in results) / len(results)
    
    return {
        'spoken_text': spoken_text,
        'word_results': results,
        'total_accuracy': total_accuracy
    }

# Example usage
if __name__ == "__main__":
    audio_file = "path/to/your/audio.wav"
    expected_text = "hello world"
    
    result = evaluate_pronunciation(audio_file, expected_text)
    print(f"Spoken text: {result['spoken_text']}")
    print(f"Overall accuracy: {result['total_accuracy']:.2f}%")
    
    for word in result['word_results']:
        print(f"Word: {word['expected']} -> {word['spoken']} (Accuracy: {word['accuracy']:.2f}%)")