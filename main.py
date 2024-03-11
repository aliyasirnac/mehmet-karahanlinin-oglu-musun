import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import pyaudio

def play_mp3(filename):
    sound = AudioSegment.from_file(filename, format="mp3")
    play(sound)

def detect_sneeze(recorded_audio):
    sneeze_count = 0
    threshold = 0.5  # Ses eşik değeri
    for sample in recorded_audio:
        if np.max(sample) > threshold:
            sneeze_count += 1
        else:
            sneeze_count = 0
        if sneeze_count == 3:
            return True
    return False

def record_audio(duration):
    fs = 44100  # Örnek oranı
    frames = []
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    input=True,
                    frames_per_buffer=1024)

    print("Recording...")

    for _ in range(int(fs / 1024 * duration)):
        data = stream.read(1024)
        frames.append(np.frombuffer(data, dtype=np.float32))

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return np.concatenate(frames)

if __name__ == "__main__":
    duration = 10  # Kayıt süresi
    recorded_audio = record_audio(duration)

    if detect_sneeze(recorded_audio):
        print("Sneeze detected!")
        play_mp3("ses.mp3")  # Sizinkine uygun bir MP3 ses dosyasının adını buraya yazın
