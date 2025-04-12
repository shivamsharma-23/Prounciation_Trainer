import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest
from audio_utils import transcribe_audio
from unittest.mock import patch

def test_evaluate_pronunciation():
    # Mock the dependencies
    mock_spoken_text = "hello world"
    mock_results = ("hello world", "hello world")
    
    with patch('main.transcribe_audio', return_value=mock_spoken_text), \
         patch('main.get_word_accuracy', return_value=mock_results):
        
        # Test transcription and evaluation
        result = evaluate_pronunciation("dummy_audio.wav", "hello world")
        
        print("\nTest Results:")
        print(f"Transcribed text: {result['spoken_text']}")
        print(f"Overall accuracy: {result['total_accuracy']:.2f}%")
        print("\nWord-by-word analysis:")
        for word in result['word_results']:
            print(f"Expected: {word['expected']} | Spoken: {word['spoken']} | Accuracy: {word['accuracy']:.2f}%")
        
        # Test the function with only audio file
        result = transcribe_audio("dummy_audio.wav")
        
        # Verify results
        assert isinstance(result, str)
        assert result == "hello world"

def test_transcribe_real_audio():
    """Test with a real audio file"""
    # Test with actual audio file
    audio_file = "d:\\AI2\\pronunciation_trainer\\test_data\\test_hello_world.wav"
    expected_text = "hello world"
    
    result = evaluate_pronunciation(audio_file, expected_text)
    
    print("\nReal Audio Test Results:")
    print(f"Audio file: {audio_file}")
    print(f"Transcribed text: {result['spoken_text']}")
    print(f"Overall accuracy: {result['total_accuracy']:.2f}%")
    print("\nWord-by-word analysis:")
    for word in result['word_results']:
        print(f"Expected: {word['expected']} | Spoken: {word['spoken']} | Accuracy: {word['accuracy']:.2f}%")
    
    # Basic validation
    assert isinstance(result, str)
    print(f"\nTranscribed text: {result}")