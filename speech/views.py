from django.shortcuts import render
from django.http import JsonResponse
import speech_recognition as sr
import random
import spacy

# Load spaCy English model for NLP analysis
nlp = spacy.load("en_core_web_sm")

# Sample sentences for testing
SENTENCES = [
    "You know New York, you need New York, you know you need unique New York.",
    "Susie works in a shoeshine shop. Where she shines she sits, and where she sits she shines.",
    "How can a clam cram in a clean cream can?",
    "We surely shall see the sun shine soon.",
    "Give papa a cup of proper coffee in a copper coffee cup.",
    "How much wood would a woodchuck chuck if a woodchuck could chuck wood?"
]

# Home Page View
def home(request):
    return render(request, 'speech/home.html')

# Start Test View (Displays a Random Sentence)
def start_test(request):
    sentence = random.choice(SENTENCES)  # Pick a random sentence
    return render(request, 'speech/test.html', {'sentence': sentence})

# Record Speech View
def record_speech(request):
    if request.method == "GET":  # Changed to GET method
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)  # Reduce noise
            audio = recognizer.listen(source)

        try:
            spoken_text = recognizer.recognize_google(audio)  # Convert to text
            return JsonResponse({"text": spoken_text})
        except sr.UnknownValueError:
            return JsonResponse({"error": "Could not understand the speech"})
        except sr.RequestError:
            return JsonResponse({"error": "Error connecting to speech recognition service"})

    return JsonResponse({"error": "Invalid request method"})

# Speech Evaluation View
def evaluate_speech(request):
    if request.method == "GET":  # Changed to GET method
        spoken_text = request.GET.get("text", "").strip()

        if not spoken_text:
            return JsonResponse({"error": "No speech detected"})

        # NLP Analysis using spaCy
        doc = nlp(spoken_text)
        fluency = len([token for token in doc if token.is_alpha]) / len(doc) * 100
        grammar = 100 if len(list(doc.sents)) > 0 else 50  # Simplified grammar check
        vocabulary = len(set([token.lemma_ for token in doc if token.is_alpha])) / len(doc) * 100
        pronunciation = 80  # Placeholder score (actual phoneme analysis requires advanced ML)
        interaction = 90  # Placeholder

        # Prepare response
        result = {
            "fluency": round(fluency, 2),
            "grammar": round(grammar, 2),
            "vocabulary": round(vocabulary, 2),
            "pronunciation": pronunciation,
            "interaction": interaction,
            "message": "Speech evaluated successfully!"
        }
        return JsonResponse(result)

    return JsonResponse({"error": "Invalid request method"})
