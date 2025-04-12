import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import pyttsx3
import pronouncing
import pandas as pd
import random
from difflib import SequenceMatcher

class PronunciationTrainerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Pronunciation Trainer")
        self.root.geometry("1000x600")
        
        # Initialize speech components and score
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.total_score = 0
        self.attempts = 0
        
        # Language and Score
        self.header_frame = tk.Frame(root)
        self.header_frame.pack(fill='x', padx=10, pady=5)
        
        self.language_label = tk.Label(self.header_frame, text="Language: English", anchor='w')
        self.language_label.pack(side='left')
        
        self.score_label = tk.Label(self.header_frame, text="Score: 0/0 (0%)", anchor='e')
        self.score_label.pack(side='right')
        
        # Main content
        self.content_frame = tk.Frame(root, bg='white')
        self.content_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Sentence display
        self.sentence_text = tk.Text(self.content_frame, height=4, wrap='word', font=('Arial', 14))
        self.sentence_text.pack(fill='x', padx=5, pady=5)
        
        # Pronunciation accuracy
        self.accuracy_frame = tk.Frame(self.content_frame)
        self.accuracy_frame.pack(fill='x', padx=5, pady=5)
        
        self.accuracy_label = tk.Label(self.accuracy_frame, text="85%", font=('Arial', 16, 'bold'))
        self.accuracy_label.pack(side='left')
        
        # IPA pronunciation guide
        self.ipa_text = tk.Text(self.content_frame, height=2, wrap='word')
        self.ipa_text.pack(fill='x', padx=5, pady=5)
        
        # User pronunciation
        self.user_text = tk.Text(self.content_frame, height=2, wrap='word', fg='blue')
        self.user_text.pack(fill='x', padx=5, pady=5)
        
        # Control buttons
        self.button_frame = tk.Frame(self.content_frame)
        self.button_frame.pack(fill='x', padx=5, pady=5)
        
        self.play_btn = ttk.Button(self.button_frame, text="▶ Play", width=10, command=self.play_pronunciation)
        self.play_btn.pack(side='left', padx=5)
        
        self.record_btn = ttk.Button(self.button_frame, text="🎤 Record", width=10, command=self.record_pronunciation)
        self.record_btn.pack(side='left', padx=5)
        
        self.next_btn = ttk.Button(self.button_frame, text="Next ➜", width=10, command=self.load_random_sentence)
        self.next_btn.pack(side='right', padx=5)
        
    def update_score(self, accuracy):
        self.attempts += 1
        if accuracy >= 85:
            self.total_score += 1
        percentage = (self.total_score / self.attempts) * 100 if self.attempts > 0 else 0
        self.score_label.config(text=f"Score: {self.total_score}/{self.attempts} ({percentage:.1f}%)")
    
    def record_pronunciation(self):
        with sr.Microphone() as source:
            self.user_text.delete(1.0, tk.END)
            self.user_text.insert(tk.END, "Listening...")
            self.root.update()
            
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio)
                
                self.user_text.delete(1.0, tk.END)
                self.user_text.insert(tk.END, text)
                
                # Calculate accuracy
                target = self.sentence_text.get(1.0, tk.END).strip()
                accuracy = SequenceMatcher(None, text.lower(), target.lower()).ratio() * 100
                self.accuracy_label.config(text=f"{accuracy:.1f}%")
                
                # Update score based on accuracy
                self.update_score(accuracy)
                
                # Enable next button after attempt
                self.next_btn.config(state='normal')
                
            except sr.UnknownValueError:
                self.user_text.delete(1.0, tk.END)
                self.user_text.insert(tk.END, "Could not understand audio")
            except Exception as e:
                self.user_text.delete(1.0, tk.END)
                self.user_text.insert(tk.END, f"Error: {str(e)}")
    
    def load_random_sentence(self):
        df = pd.read_csv('d:\\AI2\\pronunciation_trainer\\data_en.csv')
        sentence = random.choice(df['text'].tolist())
        self.sentence_text.delete(1.0, tk.END)
        self.sentence_text.insert(tk.END, sentence)
        self.show_pronunciation_guide(sentence)
        self.next_btn.config(state='disabled')  # Disable until recording attempt

    def show_pronunciation_guide(self, sentence):
        ipa_text = ""
        for word in sentence.lower().split():
            pronunciations = pronouncing.phones_for_word(word)
            if pronunciations:
                ipa_text += f"/{pronunciations[0]}/ "
        self.ipa_text.delete(1.0, tk.END)
        self.ipa_text.insert(tk.END, ipa_text)
    
    def play_pronunciation(self):
        sentence = self.sentence_text.get(1.0, tk.END).strip()
        self.engine.say(sentence)
        self.engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    app = PronunciationTrainerGUI(root)
    root.mainloop()