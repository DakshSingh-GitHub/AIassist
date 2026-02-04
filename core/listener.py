import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import tempfile
import os

SAMPLE_RATE = 16000
DURATION = 5  # seconds


def listen_text():
    return input("🧠 You: ").strip()


def listen_voice():
    print("🎙️ Listening...")

    try:
        recording = sd.rec(
            int(DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16"
        )
        sd.wait()
    except Exception as e:
        print(f"🤖 Assistant: Microphone error ({e})")
        return ""

    # Save audio temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        wav.write(tmp.name, SAMPLE_RATE, recording)
        audio_path = tmp.name

    r = sr.Recognizer()

    try:
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
            print(f"🗣️ You (voice): {text}")
            return text

    except sr.UnknownValueError:
        print("🤖 Assistant: I couldn’t understand that.")
        return ""

    except sr.RequestError:
        print("🤖 Assistant: Speech service unavailable.")
        return ""

    finally:
        os.remove(audio_path)


def listener(mode="text"):
    if mode == "voice":
        return listen_voice()
    return listen_text()
