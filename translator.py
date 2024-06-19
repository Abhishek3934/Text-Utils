from googletrans import Translator
from PyDictionary import PyDictionary
from gtts import gTTS
from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

translator = Translator()
dictionary = PyDictionary()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    target_lang = request.form['target_lang']
    
    try:
        translated_text = translator.translate(text, dest=target_lang).text
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('error.html', error_message=error_message)
    
    return render_template('result.html', text=text, translated_text=translated_text)

@app.route('/pronounce', methods=['POST'])
def pronounce():
    word = request.form['word']
    language = request.form['language']
    
    try:
        tts = gTTS(word, lang=language, slow=False)
        tts.save("pronunciation.mp3")
        return send_file("pronunciation.mp3", as_attachment=True)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('error.html', error_message=error_message)

@app.route('/meaning', methods=['POST'])
def meaning():
    word = request.form['word']
    
    try:
        meaning = dictionary.meaning(word)
        return render_template('meaning.html', word=word, meaning=meaning)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('error.html', error_message=error_message)

@app.route('/detect_language', methods=['POST'])
def detect_language():
    text = request.form['text']
    
    try:
        detected_lang = translator.detect(text).lang
        return f"The detected language is: {detected_lang}"
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('error.html', error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
