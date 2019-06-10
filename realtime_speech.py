"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""

import pyaudio
import wave
import numpy as np

__Author__ = "Amir Mohammad"

def online_recording():
    from aubio import pitch
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording ...")
    frames = []
    # Pitch
    tolerance = 0.8
    downsample = 1
    win_s = 4096 // downsample # fft size
    hop_s = 512  // downsample # hop size
    pitch_o = pitch("yin", win_s, hop_s, RATE)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)


    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        buffer = stream.read(CHUNK)
        frames.append(buffer)

        # Convert buffer to numpy data array
        # signal = np.fromstring(buffer, dtype=np.int16)
        signal = np.fromstring(buffer, dtype='f')
        # Detect Pitch
        pitch = pitch_o(signal)[0]
        confidence = pitch_o.get_confidence()

        print("{} / {}".format(pitch,confidence))


    print("====== Done recording ======")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()



def test_microphone():
    CHUNK = 2**11
    RATE = 44100


    p=pyaudio.PyAudio()
    stream=p.open(format=pyaudio.paInt16,channels=1,rate=RATE,input=True,
                  frames_per_buffer=CHUNK)

    for i in range(int(10*44100/1024)): #go for a few seconds

        data = np.fromstring(stream.read(CHUNK),dtype=np.int16)
        peak=np.average(np.abs(data))*2
        bars="#"*int(50*peak/2**16)

        print("%04d %05d %s"%(i,peak,bars))

    stream.stop_stream()
    stream.close()
    p.terminate()
