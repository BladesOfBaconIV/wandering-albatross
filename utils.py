
import json
import re

from socket import socket
from typing import Dict

def load_config() -> Dict[str, str]:
    """
    Load the config file into a dict
    """
    with open("./config.json", 'r') as config_json:
        config = json.loads(config_json.read())
    return config


def send_str(socket: socket, message: str) -> None:
    """
    Send a string to a socket (handles encoding)
    """
    socket.send(message.encode())


def get_response(socket: socket, buffer_size=1024) -> str:
    """
    Gets a response (up to buffer_size) from a socket (handles decoding)
    """
    return socket.recv(buffer_size).decode()