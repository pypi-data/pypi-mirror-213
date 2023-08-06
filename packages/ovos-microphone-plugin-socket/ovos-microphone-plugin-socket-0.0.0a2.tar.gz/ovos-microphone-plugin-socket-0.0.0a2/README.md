## Description

OpenVoiceOS Microphone Remote Socket plugin

Will expose a socket, remote clients can connect by running client.py

There is no protection at all, be careful running this

A secure HiveMind implementation wil be made later

## Install

`pip install ovos-microphone-plugin-socket`


## Usage

in remote device (microphone) run

other mic plugins can be used as reference, this example uses pyaudio

```python
import socket

import pyaudio


class AudioStreamer:
    def __init__(self, host='0.0.0.0', port=50000, backlog=5, chunk=1024,
                 channels=1, rate=16000, pa=None):
        self.rate = rate
        self.channels = channels
        if pa is None:
            self.pa = pyaudio.PyAudio()

        # Socket Initialization
        self.host = host
        self.port = port
        self.backlog = backlog
        self.chunk = chunk
        self.stream = self.pa.open(format=pyaudio.paInt16,
                                   channels=self.channels,
                                   rate=self.rate,
                                   input=True,
                                   frames_per_buffer=self.chunk)

    def init_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print("client connected")
        except ConnectionRefusedError:
            print("can not connect to server, verify host and port")
            raise

    def run(self):
        self.init_socket()
        print("streaming audio")

        # Main Functionality
        while True:
            try:
                data = self.stream.read(self.chunk)
                self.sock.send(data)
                ans = self.sock.recv(self.chunk).decode("utf-8")
                if "busy" in ans:
                    print("server is busy")
                    break

            except BrokenPipeError:
                print("server connection crashed")
                break
            except ConnectionResetError:
                print("server reset connection")
                break
            except KeyboardInterrupt:
                print("closing connection")
                break

    def close(self):
        self.stream.close()
        self.pa.terminate()
        print("Client has stopped running")


if __name__ == "__main__":
    receiver = AudioStreamer()
    receiver.run()
    receiver.close()
```