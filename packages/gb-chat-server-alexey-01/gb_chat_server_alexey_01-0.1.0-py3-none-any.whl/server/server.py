from socket import *
import json
import select
import argparse
import logging
import log.server_log_config
import hmac
import binascii
import dis
import os
from server_db import add_users, add_contact, get_contact, del_contact, get_users, get_hash


server_log = logging.getLogger('server_1')


class ServerVerifier(type):
    """
    Class for check methods
    """
    def __init__(self, clsname, bases, clsdict):
        list_methods = []
        for key, value in clsdict.items():
            try:
                gen = dis.get_instructions(value)
            except Exception:
                pass
            else:
                for instruct in gen:
                    if (instruct.opname == 'LOAD_GLOBAL') and (instruct.argval not in list_methods):
                        list_methods.append(instruct.argval)
                    elif (instruct.opname == 'LOAD_ATTR') and (instruct.argval not in list_methods):
                        list_methods.append(instruct.argval)
        if 'connect' in list_methods:
            raise TypeError('Call connect for socket')
        if not ('SOCK_STREAM' in list_methods and 'AF_INET' in list_methods):
            raise TypeError('There is no use of sockets for work on TCPs')

        super().__init__(clsname, bases, clsdict)


class Sock:
    """
    Class for create socked
    """
    def __init__(self):
        self._values = {}

    def __set__(self, instance, value):
        if not value or not value > 0:
            value = 7777
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Server(metaclass=ServerVerifier):
    """
    Main class for server
    """

    port = Sock()

    def __init__(self, addr, port_numb):
        self.addr = addr
        self.port = port_numb
        self.clients = []
        self.messages = []
        self.users = get_users()

    def main_server(self):
        """
        Main function for class server
        :return: messages list
        """
        print(f'Server start with port number {self.port}')
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((self.addr, self.port))
        s.settimeout(0.2)
        self.sock = s
        self.sock.listen()

        while True:
            try:
                client, cl_addr = self.sock.accept()
            except OSError as e:
                pass
            else:
                self.clients.append(client)
                server_log.info(f'connected from {cl_addr}')
            finally:
                wait = 1
                r = []
                w = []
                try:
                    r, w, e = select.select(self.clients, self.clients, [], wait)
                except:
                    pass

                messages = self.read_request(r, self.clients, self.messages)
                # print(messages)

                if messages:
                    for msg in self.messages:
                        if msg:
                            self.write_response(msg, w, self.clients)
                            self.messages.remove(msg)

    def send_message(self, client, response):
        """
        Function for sending messages
        :param client: str
        :param response: str
        :return: None
        """
        message_json = json.dumps(response).encode('utf-8')
        try:
            client.send(message_json)
            server_log.info(f'message {response} sent {client}')
        except Exception:
            pass

    def autorize_user(self, message, sock):
        """
        Function for check authorizations user
        :param message: str
        :param sock: str
        :return: None or Raise Error
        """
        print(message['user']['account_name'])
        if message['user']['account_name'] in self.users:
            message_auth = {
                'response': 511
            }
            random_str = binascii.hexlify(os.urandom(64))
            message_auth['data'] = random_str.decode('ascii')
            hash_new = get_hash(message['user']['account_name'])
            hash_main = hmac.new(hash_new.encode('utf-8'), random_str, 'MD5')
            digest = hash_main.digest()
            try:
                self.send_message(sock, message_auth)
                data = json.loads(sock.recv(1024).decode('utf-8'))
                print(data)
                server_log.info(f'from {sock} receiving {data}')
            except Exception:
                sock.close()
                return
            client_digest = binascii.a2b_base64(data['data'])
            # print('==============================')
            # print(client_digest)
            # print(digest)
            # print('===============================')
            if hmac.compare_digest(digest, client_digest):
                print('---OK---')
                return
            else:
                print('===BAD===')
                sock.close()
                raise ConnectionError

    def read_request(self, clients, all_clients, messages):
        """
        Functon for receiving and processing messages
        :param clients: str
        :param all_clients: list
        :param messages: list
        :return: dict
        """
        responses = {}

        for sock in clients:
            try:
                data = json.loads(sock.recv(1024).decode('utf-8'))
                responses[sock] = data
                print(data)
                server_log.info(f'from {sock} receiving {data}')

                # OLD CODE
                if 'action' in data and data['action'] == 'presence':
                    self.autorize_user(data, sock)
                    response = {
                        "response": 200,
                        "alert": "OK"
                    }

                    client_ip, client_port = sock.getpeername()
                    print(f"{data['user']['account_name']} - {client_ip}")
                    add_users(data['user']['account_name'], client_ip)

                    server_log.info(f'response {response}')
                    self.send_message(sock, response)
                    return messages

                elif 'action' in data and data['action'] == 'add_contact':
                    print("ADDING CONTACT")
                    add_contact(data['user']['account_name'], data['user_login'])
                    response = {
                        "response": 201,
                        "alert": "OK"
                    }
                    server_log.info(f'response {response}')
                    self.send_message(sock, response)
                    return messages

                elif 'action' in data and data['action'] == 'del_contact':
                    print("DELETING CONTACT")
                    del_contact(data['user']['account_name'], data['user_login'])
                    response = {
                        "response": 201,
                        "alert": "OK"
                    }
                    server_log.info(f'response {response}')
                    self.send_message(sock, response)
                    return messages

                elif 'action' in data and data['action'] == 'message':
                    if data['destination']:
                        add_contact(data['user']['account_name'], data['destination'])
                    self.messages.append(data)

                elif 'action' in data and data['action'] == 'get_contacts':
                    contacts_list = get_contact(data['user']['account_name'])
                    response = {
                        "response": 202,
                        "alert": contacts_list
                    }
                    server_log.info(f'response {response}')
                    self.send_message(sock, response)
                    return messages

                # NEW CODE
                return messages
            except:
                all_clients.remove(sock)

        return messages

    def write_response(self, message, w_clients, all_clients):
        """
        Function for processing response from clients
        :param message: str
        :param w_clients: list
        :param all_clients: list
        :return:
        """
        for sock in all_clients:
            try:
                answ = json.dumps(message).encode('utf-8')
                sock.send(answ)
                server_log.info(f'message {message} sent')
            except:
                self.sock.close()
                self.all_clients.remove(sock)


def main():
    """
    Main function. Enter point. Parsing arguments of command line.
    :return: start server
    """
    server_log.info('start program')
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=7777, type=int)
    parser.add_argument('-a', '--addr', default='localhost')
    args = parser.parse_args()

    addr = args.addr
    port = args.port

    server = Server(addr, port)
    server.main_server()


if __name__ == '__main__':
    main()
