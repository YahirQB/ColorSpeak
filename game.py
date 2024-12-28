import matplotlib.pyplot as plt
import random
import speech_recognition as sr
import pyttsx3

# List of colors and their names
COLORS = [
    ("red", (255, 0, 0)),
    ("green", (0, 255, 0)),
    ("blue", (0, 0, 255)),
    ("yellow", (255, 255, 0)),
    ("purple", (128, 0, 128)),
    ("orange", (255, 165, 0)),
    ("pink", (255, 192, 203)),
    ("black", (0, 0, 0)),
    ("white", (255, 255, 255)),
    ("brown", (165, 42, 42)),
    ("gray", (128, 128, 128)),
    ("gold", (255, 215, 0)),
    ("silver", (192, 192, 192)),
    ("crimson", (220, 20, 60)),
    ("mint", (189, 252, 201)),
]

def display_color(rgb):
    """Display a square of the given color."""
    plt.imshow([[rgb]])
    plt.axis('off')
    plt.show()

def get_audio_input(prompt):
    """Capture audio input from the user."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you repeat?")
            speak("Sorry, I didn't catch that. Could you repeat?")
            return get_audio_input(prompt)
        except sr.RequestError:
            print("There was an error with the speech recognition service.")
            speak("There was an error with the speech recognition service.")
            return ""

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def main():
    print("Say 'let's go' to begin.")
    speak("Say 'let's go' to begin.")

    score = 0
    max_guesses = 3
    questions_per_round = 3  # Number of questions in one round

    while True:
        command = get_audio_input("Waiting for your command...")
        if command == "let's go":
            print("Starting the game...")
            speak("You are allowed a maximum of 3 guesses per question.")
            break

    while True:
        for question in range(questions_per_round):
            color_name, rgb = random.choice(COLORS)
            display_color(rgb)

            for guess in range(max_guesses):
                speak("What is the name of this color?")
                response = get_audio_input("What is the name of this color?").lower()
                if color_name in response:
                    print("Correct!")
                    speak("Correct!")
                    score += 1
                    break
                else:
                    print(f"Incorrect. You have {max_guesses - guess - 1} guesses left.")
                    speak(f"Incorrect. You have {max_guesses - guess - 1} guesses left.")
                    print(f"You said: {response}")
                    if guess == max_guesses - 1:
                        print(f"The answer was {color_name}.")
                        speak(f"The answer was {color_name}.")

            print(f"Your current score: {score}")
            speak(f"Your current score is {score}.")

        # End of the round, ask if the user wants to continue
        speak("Do you want to play another round? Say yes or no.")
        command = get_audio_input("Do you want to play another round?").lower()

        if command != "yes":
            print(f"Thanks for playing! Your final score is: {score}")
            speak(f"Thanks for playing! Your final score is {score}.")
            break

if __name__ == "__main__":
    main()
