import threading
import pyaudio
import atexit
import numpy


# On creation, records audio through the microphone
class Recorder(object):
    def __init__(self, rate=4000, chunksize=1024):
        # Initialize audio variables and pyaudio
        self.rate = rate
        self.chunksize = chunksize
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = self.pyaudio_instance.open(format=pyaudio.paInt16,
                                                 channels=1,
                                                 rate=self.rate,
                                                 input=True,
                                                 frames_per_buffer=self.chunksize,
                                                 stream_callback=self.new_frame)
        self.frames = []

        # Initialize multithreading routines
        self.lock = threading.Lock()
        self.stop = False
        atexit.register(self.close)

    # Callback method when a new audio frame is recorded
    def new_frame(self, data, frame_count, time_info, status):
        data = numpy.fromstring(data, 'int16')
        with self.lock:
            self.frames.append(data)
            if self.stop:
                return None, pyaudio.paComplete
        return None, pyaudio.paContinue

    # Return filled audio frames, and re-initialize audio frames
    def get_frames(self):
        with self.lock:
            frames = self.frames
            self.frames = []
            return frames

    def start(self):
        self.stream.start_stream()

    # Stop recording, close the stream, terminate pyaudio
    def close(self):
        with self.lock:
            self.stop = True
        self.stream.close()
        self.pyaudio_instance.terminate()
