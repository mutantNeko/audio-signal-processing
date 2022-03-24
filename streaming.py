import pyaudio
import struct
import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
import time

#############################################
from pynput.keyboard import Key, Controller, Listener
from collections import deque
from array import array

keyboard = Controller()

i = 0
############################################

CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

############################################

phSize = int(0.25 * RATE)

queue = deque(maxlen=phSize)
############################################

p = pyaudio.PyAudio()

chosen_device_index = -1
for x in range(0, p.get_device_count()):
    info = p.get_device_info_by_index(x)

    if info["name"] == "pulse":
        chosen_device_index = info["index"]


def callback(in_data, frame_count, time_info, status):
    data = struct.unpack(str(CHUNK) + "h", in_data)
    queue.extend(data)
    return (in_data, pyaudio.paContinue)


stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input_device_index=chosen_device_index,
    input=True,
    frames_per_buffer=CHUNK,
    stream_callback=callback,
)

stream.start_stream()


plt.ion()
fig, ax = plt.subplots(2, 1)

x = np.arange(0, phSize)
y = np.zeros(phSize)
(line,) = ax[0].plot(x, y)
(line2,) = ax[1].plot(x, y)
fig.canvas.draw()
ax[0].set_ylim([-(2 ** 13), (2 ** 13) - 1])
ax[1].set_ylim([-(2 ** 13), (2 ** 13) - 1])


def getChunk(key):
    if key == Key.space:
        time.sleep(1)
        line2.set_ydata(queue)


keyboard_thread = Listener(on_press=getChunk)
keyboard_thread.start()

while stream.is_active():
    try:
        line.set_ydata(queue)
        fig.canvas.draw()
        fig.canvas.flush_events()
    except:
        pass
