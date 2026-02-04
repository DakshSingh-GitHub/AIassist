import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import tempfile
import os

SAMPLE_RATE = 16000
MAX_DURATION = 6  # seconds
SILENCE_THRESHOLD = 0.01


def normalize_audio(audio):
    peak = np.max(np.abs(audio))
    if peak == 0:
        return audio
    return audio / peak


def trim_silence(audio, threshold=SILENCE_THRESHOLD):
    mask = np.abs(audio) > threshold
    if not np.any(mask):
        return audio
    start = np.argmax(mask)
    end = len(mask) - np.argmax(mask[::-1])
    return audio[start:end]


def listen_text():
    return input("🧠 You: ").strip()


def listen_voice():
    print("🎙️ Listening... (normal voice is fine)")

    try:
        recording = sd.rec(
            int(MAX_DURATION * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32"
        )
        sd.wait()
    except Exception as e:
        print(f"🤖 Assistant: Microphone error ({e})")
        return ""

    audio = recording.flatten()

    # 🔉 Gentle normalization (NOT aggressive)
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak * 0.8   # boost softly

    # 🚫 DO NOT hard-trim silence anymore
    # Let recognizer handle it

    audio_int16 = np.int16(audio * 32767)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        wav.write(tmp.name, SAMPLE_RATE, audio_int16)
        audio_path = tmp.name

    r = sr.Recognizer()

    # 🎯 VERY IMPORTANT tuning
    r.energy_threshold = 150          # LOWER
    r.dynamic_energy_threshold = True
    r.pause_threshold = 0.8           # allow pauses
    r.phrase_threshold = 0.1          # accept short speech
    r.non_speaking_duration = 0.6

    try:
        with sr.AudioFile(audio_path) as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            print(f"🗣️ You (voice): {text}")
            return text

    except sr.UnknownValueError:
        print("🤖 Assistant: I couldn't understand that.")
        return ""

    except sr.RequestError:
        print("🤖 Assistant: Speech service unavailable.")
        return ""

    finally:
        os.remove(audio_path)

def listener(mode="text"):
    """
    Unified listener: text or voice
    """
    if mode == "voice":
        return listen_voice()
    return listen_text()
