# app.py
from flask import Flask, render_template, request, jsonify
import openai
import speech_recognition as sr

app = Flask(__name__)

openai.api_key = "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"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def api():
    try:
        user_input = request.json['input']
        print(f"Received question: {user_input}")

        # Call OpenAI API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=100,
        )
        ai_response = response.choices[0].text.strip()


        print(f"AI Response: {ai_response}")

        return jsonify({"success": True, "message": ai_response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "Error processing the question."})

def get_audio_input():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return None
    except sr.RequestError as e:
        print(f"Error fetching results from Google Speech Recognition service: {e}")
        return None

def main(user_input):
    print(f"User: {user_input}")
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_input,
        max_tokens=100,
    )
    print(f"AI: {response.choices[0].text.strip()}")
    return response.choices[0].text.strip()

if __name__ == "__main__":
    app.run(debug=True)
