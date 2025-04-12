import speech_recognition as sr
import pyttsx3
import pronouncing
import pandas as pd
import random
from difflib import SequenceMatcher

def calculate_similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() * 100

def get_random_sentence():
    df = pd.read_csv('d:\\AI2\\pronunciation_trainer\\data_en.csv')
    return random.choice(df['text'].tolist())

def test_real_time_pronunciation():
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()
    
    while True:
        print("\nChoose an option:")
        print("1. Enter your own text")
        print("2. Practice with provided text")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == '3':
            print("Exiting...")
            break
            
        # Get the target sentence based on choice
        if choice == '1':
            target_sentence = input("\nEnter the sentence to practice: ")
        elif choice == '2':
            target_sentence = get_random_sentence()
            print(f"\nHere's your practice sentence: {target_sentence}")
        else:
            print("Invalid choice. Please try again.")
            continue
            
        # Show pronunciation guide
        print("\nCorrect Pronunciation Guide:")
        for word in target_sentence.lower().split():
            pronunciations = pronouncing.phones_for_word(word)
            if pronunciations:
                print(f"Word: {word}")
                print(f"IPA: /{pronunciations[0]}/")
        
        # Play correct pronunciation
        print("\nPlaying correct pronunciation...")
        engine.say(target_sentence)
        engine.runAndWait()
        
        print("\nNow, repeat the sentence...")
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        
        try:
            spoken_text = recognizer.recognize_google(audio)
            print(f"\nYou said: {spoken_text}")
            
            # Calculate pronunciation accuracy
            accuracy = calculate_similarity(spoken_text, target_sentence)
            print(f"\nPronunciation accuracy: {accuracy:.1f}%")
            
            if accuracy >= 85:
                print("Excellent pronunciation! 👍")
            elif accuracy >= 70:
                print("Good pronunciation. Keep practicing!")
            else:
                print("Try again. Listen carefully to the correct pronunciation:")
                engine.say(target_sentence)
                engine.runAndWait()
            
            # Show word-by-word comparison
            print("\nWord-by-word analysis:")
            target_words = target_sentence.lower().split()
            spoken_words = spoken_text.lower().split()
            
            for t_word, s_word in zip(target_words, spoken_words):
                word_accuracy = calculate_similarity(t_word, s_word)
                status = "✓" if word_accuracy > 80 else "✗"
                print(f"{status} Expected: {t_word} | You said: {s_word}")
                
        except sr.UnknownValueError:
            print("Could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_real_time_pronunciation()