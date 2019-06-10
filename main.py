import pyaudio # for install pyaudio check this link : https://stackoverflow.com/questions/20023131/cannot-install-pyaudio-gcc-error
import wave
import wave
import numpy as np

from realtime_speech import online_recording, test_microphone
from base1 import change_voice
from last import play_voice, real_time_speeching_and_shifting

__Author__ = "Amir Mohammad"


'''
The project does not follow a specific architecture, but the naming of the functions is correct,
which is clearly what each function performs.
'''


# command for create virtualenv : virtualenv -p python3.6 venv
# command for run in terminal :
# python -c 'import main; main.level_1()'

def level_1():
    test_microphone()


def level_2():
    change_voice()


def level_3():
    online_recording()
    change_voice('output.wav')
    # play_voice()


def level_4():
    real_time_speeching_and_shifting()
