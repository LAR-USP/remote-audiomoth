import pyaudio
import wave
import socket
import time

class AudioRecorder(object):
    def __init__(self, host, port, rate, record_interval, record_time, retry_conn = 5):
        self.HOST = host
        self.PORT = port
        self.ri = record_interval
        self.rt = record_time
        self.retry_conn = retry_conn
        self.audio_counter = 0

        ### Audio configs
        self.RATE = rate

    def create_socket(self):
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.HOST,self.PORT))
                return s
            except socket.error as exc:
                print('Receiver not found. Saving locally/Adding audio to queue (%s)' % exc)
                time.sleep(self.retry_conn)

    def audio_to_wav(self, frames, sample_size, CHANNELS, FORMAT):
        audio_file = '../data/audiomoth-{}-bkp.wav'.format(self.audio_counter)
        wf = wave.open(audio_file, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(sample_size)
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    def record(self, CHUNK = 1024, CHANNELS=2, FORMAT=pyaudio.paInt16):
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")

        frames = []
        for i in range(0, int(self.RATE / CHUNK * self.rt)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()
        self.audio_to_wav(frames, p.get_sample_size(FORMAT), CHANNELS, FORMAT)
        self.audio_counter += 1
        return True

    def send_audio(self):
        s = self.create_socket()
        audio_file = '../data/audiomoth-{}-bkp.wav'.format(self.audio_counter-1)
        with open(audio_file, 'rb') as f:
            s.sendfile(f)
        s.close()

    def activate(self):
        while True:
            if self.record():
                self.send_audio()
            time.sleep(self.ri)

if __name__ == '__main__':
    AR = AudioRecorder('localhost', 19123, 44100, 1, 5)
    AR.activate()
