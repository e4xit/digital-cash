##############
# Networking #
##############

import socketserver
import socket
import my_logger
import validation
import globalconfig
import miner

from utils import serialize, deserialize


def prepare_message(command, data):
    return {
        "command": command,
        "data": data,
    }


class TCPHandler(socketserver.BaseRequestHandler):

    def respond(self, command, data):
        response = prepare_message(command, data)
        return self.request.sendall(serialize(response))

    def handle(self):
        message_bytes = self.request.recv(1024 * 4).strip()
        message = deserialize(message_bytes)
        command = message["command"]
        data = message["data"]

        my_logger.logger.info(f"received {command}")

        if command == "ping":
            self.respond(command="pong", data="")

        if command == "block":
            # node is a shared variable here between mining and node
            if data.prev_id == globalconfig.node.blocks[-1].id:
                globalconfig.node.handle_block(data)
                # Interrupt mining thread
                miner.mining_interrupt.set()

        if command == "tx":
            validation.Node.handle_tx(data)

        if command == "balance":
            balance = validation.Node.fetch_balance(data)
            self.respond(command="balance-response", data=balance)

        if command == "utxos":
            utxos = validation.Node.fetch_utxos(data)
            self.respond(command="utxos-response", data=utxos)


def external_address(node):
    i = int(node[-1])
    port = validation.PORT + i
    return ('localhost', port)


def serve():
    my_logger.logger.info("Starting server")
    server = socketserver.TCPServer(("0.0.0.0", validation.PORT), TCPHandler)
    server.serve_forever()


def send_message(address, command, data, response=False):
    message = prepare_message(command, data)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(address)
        s.sendall(serialize(message))
        if response:
            return deserialize(s.recv(5000))
