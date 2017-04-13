import threading
import wave
import pyaudio
import audioop
import atexit
import numpy as np

class Recorder(object):
    def __init__(self, rate=4000, chunksize=1024):
        self.rate = rate
        self.chunksize = chunksize
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunksize,
                                  stream_callback=self.new_frame)
        self.lock = threading.Lock()
        self.stop = False
        self.frames = []
        atexit.register(self.close)

    def new_frame(self, data, frame_count, time_info, status):
        data = np.fromstring(data, 'int16')
        with self.lock:
            self.frames.append(data)
            if self.stop:
                return None, pyaudio.paComplete
        return None, pyaudio.paContinue

    def get_frames(self):
        with self.lock:
            frames = self.frames
            self.frames = []
            return frames

    def start(self):
        self.stream.start_stream()

    def close(self):
        with self.lock:
            self.stop = True
        self.stream.close()
        self.p.terminate()
#     CHUNK = 1024
#     FORMAT = pyaudio.paInt16
#     CHANNELS = 2
#     RATE = 44100
#     WAVE_OUTPUT_FILENAME = "apt.wav"
#
#     def __init__(self):
#         super(Recorder, self).__init__()
#         self.p = pyaudio.PyAudio()
#
#         self.stream = self.p.open(format=self.FORMAT,
#                         channels=self.CHANNELS,
#                         rate=self.RATE,
#                         input=True,
#                         frames_per_buffer=self.CHUNK)
#
#         self.wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
#         self.wf.setnchannels(self.CHANNELS)
#         self.wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
#         self.wf.setframerate(self.RATE)
#         self.rms = 0.0
#
#     def run(self):
#         print("* recording")
#         try:
#             while True:
#                 frames = []
#                 data = self.stream.read(self.CHUNK)
#                 self.rms = audioop.rms(data,2)
#                 frames.append(data)
#                 self.wf.writeframes(b''.join(frames))
#         finally:
#             # clean up
#             print("* done recording")
#             self.stream.close()
#             self.p.terminate()
#             self.wf.close()
#
#
# if __name__ == '__main__':
#     Recorder().run()