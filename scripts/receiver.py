import socket

class AudioReceiver(object):
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        self.audio_counter = 0
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.HOST, self.PORT))
        self.s.listen(1)

    def save(self, conn):
        audio_file = '../data/audiomoth-{}.wav'.format(self.audio_counter)
        with open(audio_file,'wb') as f:
            try:
                while True:
                    l = conn.recv(1024)
                    if not l: break
                    f.write(l)

                print('Saved: {}'.format(audio_file))
                self.audio_counter += 1

            except Exception as e:
                print('Error: {}'.format(e))

    def listen(self):
        while True:
            conn, addr = self.s.accept()
            self.save(conn)

if __name__ == '__main__':
    AR = AudioReceiver('localhost', 19123)
    AR.listen()
