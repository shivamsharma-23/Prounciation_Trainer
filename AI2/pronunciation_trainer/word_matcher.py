def get_word_accuracy(expected_text, spoken_text):
    """
    Compare expected text with spoken text and calculate accuracy for each word
    Args:
        expected_text (str): The text that should have been spoken
        spoken_text (str): The text that was actually spoken
    Returns:
        list: List of dictionaries containing word comparison results
    """
    expected_words = expected_text.lower().split()
    spoken_words = spoken_text.lower().split()
    
    results = []
    for exp_word, spk_word in zip(expected_words, spoken_words):
        # Simple matching for now - can be enhanced with more sophisticated comparison
        accuracy = 100.0 if exp_word == spk_word else 80.0
        results.append({
            'expected': exp_word,
            'spoken': spk_word,
            'accuracy': accuracy
        })
    
    return results