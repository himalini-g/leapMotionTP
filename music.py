
#Code modified from https://people.csail.mit.edu/hubert/pyaudio/



###########################################################################
######################### Playing a WAV file ##############################
###########################################################################
# music cite
# - background music: https://www.youtube.com/watch?v=kxqJuc1HHbg
# - gun shot sounds: https://drive.google.com/file/d/1ajEoSZ8J6kF9iDSjSDvNIfn4yDYYGVZc/view
# code cite:
# https://drive.google.com/drive/folders/1pGZPirg1UYeJh5bS_GGU7pYp17XZpujq



"""PyAudio Example: Play a WAVE file."""

import pyaudio
import wave, time
import sys
from array import array
from struct import pack

def play(file):
    CHUNK = 1024

    wf = wave.open(file, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels= wf.getnchannels(),
                    rate=wf.getframerate(),
                    output = True)

    data = wf.readframes(CHUNK)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()