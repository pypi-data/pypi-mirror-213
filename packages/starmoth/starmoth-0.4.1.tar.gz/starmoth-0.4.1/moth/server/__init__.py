from typing import Callable, Dict, List, Optional
import zmq
import time
from moth.driver import ModelDriver
from moth.message import (
    HandshakeMsg,
    ClassificationResultMsg,
    HandshakeResponseMsg,
    HeartbeatMsg,
    Msg,
    ObjectDetectionResultMsg,
    parse_message,
)
from moth.message.exceptions import MothMessageError


class IdentityPool:
    def __init__(self):
        self._ids = []

    def add_identity(self, name: str, token: str):
        self._ids.append((name, token))

    def validate_handshake(self, identity: str, msg: HandshakeMsg) -> bool:
        if identity != msg.name:
            return False

        id_ = [i for i in self._ids if i[1] == msg.handshake_token]
        if len(id_) != 1:
            return False

        if id_[0][0] == identity and id_[0][1] == msg.handshake_token:
            return True


class MessageHandler:
    def onMessage(self, msg: Msg):
        pass


class Server:
    HEARTBEAT_TIMEOUT = 5
    HEARTBEAT_INTERVAL = 1

    def __init__(self, port=7171):
        self.port = port
        self._stop = False
        self._driver_factory = None
        self._drivers: Dict[str, ModelDriver] = {}
        self._models: Dict[str, Dict[str, str]] = {}
        self._on_model_change_handler: Optional[
            Callable[[List[Dict[str, str]]], None]
        ] = None
        self._heartbeats: Dict[str, float] = {}

    def driver_factory(self, func: Callable[[HandshakeMsg], ModelDriver]):
        """
        Annotation to provide driver factory function.
        For every incoming model connection, this factory is called to get a driver for
        that model.
        """
        self._driver_factory = func
        return func

    def start(self):
        context = zmq.Context()
        socket = context.socket(zmq.ROUTER)
        socket.bind(f"tcp://*:{self.port}")
        self._recv_loop(socket)

    def stop(self):
        self._stop = True

    def _recv_loop(self, socket):
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        last_heartbeat = time.time()
        print("Server listening...")
        while not self._stop:
            # handle input
            events = dict(poll.poll(1000))
            if events:
                identity = socket.recv()
                msg_bytes = socket.recv()

                try:
                    message = parse_message(msg_bytes)
                    if isinstance(message, HandshakeMsg) and self._driver_factory:
                        driver = self._driver_factory(message)
                        identity_str = identity.decode("utf-8")
                        model = {
                            "id": identity_str,
                            "taskType": message.task_type,
                        }
                        self._drivers[identity] = driver
                        self._models[identity] = model
                        self._heartbeats[identity] = time.time()
                        if self._on_model_change_handler:
                            self._on_model_change_handler(
                                list(self._models.values())
                            )  # Pass the list of current drivers
                        print(f"MUT connected: {identity_str}")
                        # Send a handshake response
                        socket.send(identity, zmq.SNDMORE)
                        socket.send(HandshakeResponseMsg().serialize_envelope())

                    if isinstance(message, ClassificationResultMsg):
                        if identity in self._drivers:
                            self._drivers[identity].on_model_result(message)

                    if isinstance(message, ObjectDetectionResultMsg):
                        if identity in self._drivers:
                            self._drivers[identity].on_model_result(message)

                    if isinstance(message, HeartbeatMsg):
                        self._heartbeats[identity] = time.time()

                except MothMessageError as err:
                    print(err)
                except Exception as err:
                    print(err)

            # Check if we need to send heartbeats
            if last_heartbeat + Server.HEARTBEAT_INTERVAL < time.time():
                last_heartbeat = time.time()
                for identity in self._drivers:
                    socket.send(identity, zmq.SNDMORE)
                    socket.send(HeartbeatMsg().serialize_envelope())

            disconnected = []
            for identity in self._drivers:
                next_prompt = self._drivers[identity].next_model_prompt()
                if next_prompt is not None:
                    socket.send(identity, zmq.SNDMORE)
                    socket.send(next_prompt.serialize_envelope())
                # Check heartbeat status
                if identity in self._heartbeats:
                    if self._heartbeats[identity] + Server.HEARTBEAT_TIMEOUT < time.time():
                        # Mark as diconnected
                        disconnected.append(identity)

            # Remove disconnected models
            for identity in disconnected:
                self._drivers.pop(identity)
                self._models.pop(identity)
                self._heartbeats.pop(identity)
                if self._on_model_change_handler:
                    self._on_model_change_handler(list(self._models.values()))
                print(f"MUT disconnected: {identity.decode('utf-8')}")

        socket.close()

    def on_model_change(self, func: Callable[[List[Dict[str, str]]], None]):
        """
        Annotation to provide a function that is called when the list of connected models changes.
        """
        self._on_model_change_handler = func
        return func
