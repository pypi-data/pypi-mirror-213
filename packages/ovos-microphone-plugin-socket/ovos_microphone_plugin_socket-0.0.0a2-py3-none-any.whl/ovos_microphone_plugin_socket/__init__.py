# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import socket
from dataclasses import dataclass, field
from queue import Queue
from threading import Thread
from typing import Optional

from ovos_plugin_manager.templates.microphone import Microphone


@dataclass
class SocketMicrophone(Microphone):
    host: str = '0.0.0.0'
    port: int = 50000
    timeout: float = 5.0
    clients: dict = None
    sock: socket.socket = None
    backlog: int = 5
    on_call: bool = False

    _thread: Optional[Thread] = None
    _queue: "Queue[Optional[bytes]]" = field(default_factory=Queue)
    _is_running: bool = False

    def init_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.backlog)

    def on_new_client(self, client, addr):
        self.on_call = True
        print("Listening to incoming stream from ", addr)
        while self._is_running:
            try:
                data = client.recv(self.chunk_size)
                if data:
                    self._queue.put_nowait(data)
                    client.send(b'ACK')  # Send an ACK
            except KeyboardInterrupt:
                print("server closed by user")
                break
            except ConnectionResetError as e:
                print("client disconnected")
                break
            except Exception as e:
                print(e)
                break
        client.close()
        self.on_call = False

    def _run(self):
        self._is_running = True
        while self._is_running:
            if self.on_call:
                client, address = self.sock.accept()
                client.send(b'busy')  # Send an ACK
                client.close()
            else:
                client, address = self.sock.accept()
                thread = Thread(target=self.on_new_client,
                                args=(client, address),
                                daemon=True).start()
                self.clients[address] = thread

    def start(self):
        self.clients = {}
        self.init_socket()
        self._is_running = True
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()

    def read_chunk(self) -> Optional[bytes]:
        assert self._is_running, "Not running"
        if self.on_call:
            return self._queue.get(timeout=self.timeout)
        return b"0" * self.chunk_size  # silence

    def stop(self):
        assert self.sock is not None, "Not started"
        self._is_running = False
        while not self._queue.empty():
            self._queue.get()
        self._queue.put_nowait(None)
        self.sock.close()
