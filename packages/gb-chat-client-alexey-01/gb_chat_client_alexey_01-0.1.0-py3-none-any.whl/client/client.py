from socket import *
import json
import argparse
from time import time
from threading import Thread
import hashlib
import hmac
import binascii
import log.client_log_config
import logging
import dis
from client_db import add_users
import sys
from PyQt5.QtWidgets import QApplication
from main_window import ClientMainWindow


client_log = logging.getLogger('client')


class ClientVerifier(type):
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
        if ('accept' or 'listen') in list_methods:
            raise TypeError('Call accept or listen for socket')
        elif 'socket' in list_methods:
            raise TypeError('Create socket in class')
        if 'get_message' not in list_methods and 'send_message' not in list_methods:
            raise TypeError('There is no use of sockets for work on TCP')

        super().__init__(clsname, bases, clsdict)


def processing_presence(username):
    """
    Function for create presence message
    :param username: str
    :return: dict
    """
    client_log.info('message presence complete')
    return {
        'action': 'presence',
        'time': time(),
        'type': 'status',
        'text': 'Hello!',
        'user': {
            'account_name': username,
            'status': 'I am here!'
        }
    }


def send_message(s, message):
    """
    Function for sending messages to clients
    :param s: str
    :param message: dict
    :return: None
    """
    message_json = json.dumps(message).encode('utf-8')
    try:
        if message['action'] == 'message':
            add_users(message['destination'], message['text'])
    except Exception:
        pass
    s.send(message_json)
    client_log.info('message sent')


def processing_answer(message_raw):
    """
    Function for processing message from server
    :param message_raw: dict
    :return: str
    """
    try:
        if message_raw['response'] == 200 and message_raw['alert']:
            client_log.info(f"processing answer {message_raw['response']} {message_raw['alert']}")
            return f"{message_raw['response']} {message_raw['alert']}"
        else:
            client_log.warning('Bad server answer')
            raise ConnectionError
    except Exception:
        client_log.warning('Bad server answer')
        print('ErrorServerAnswer')
        raise ConnectionError
        # return 'Bad server answer'


def get_message(client):
    """
    Function for receiving and processing message from server
    :param client: str
    :return:
    """
    message_in = client.recv(1024)
    message_raw = json.loads(message_in.decode('utf-8'))
    try:
        if message_raw['action'] == 'message':
            add_users(message_raw['user']['account_name'], message_raw['text'])
    except Exception:
        pass
    client_log.info(f'get message from {client}')

    return message_raw


class Read(Thread, metaclass=ClientVerifier):
    """
    Class for receiving message from server
    """
    def __init__(self, client):
        self.client = client
        super().__init__()

    def run(self):
        while True:
            try:
                data = get_message(self.client)
                print(data)
                if data['response'] == 202:
                    print(f'Contact list: {data["alert"]}')
                print(f"Message from {data['user']['account_name']} - {data['text']}")
            except Exception:
                pass


class Send(Thread, metaclass=ClientVerifier):
    """
    Class input messages from user and for sending messages to server
    """
    def __init__(self, client, username):
        self.client = client
        self.username = username
        super().__init__()

    def run(self):
        while True:
            # to_name = input('Enter destination name')
            print('Enter your message, "q" for quit, "a" - for add contact, "c" - view contacts ,"d" - delete contact:')
            txt = input()
            if txt == 'q':
                return
            elif txt == 'a':
                contact = input('Enter contact: ')
                message = {
                    'action': 'add_contact',
                    'time': time(),
                    'user_login': contact,
                    'user': {
                        'account_name': self.username,
                }
            }
                send_message(self.client, message)
                client_log.info(f'{message} sent to {self.client}')
            elif txt == 'c':
                message = {
                    'action': 'get_contacts',
                    'time': time(),
                    'user': {
                        'account_name': self.username,
                }
            }
                send_message(self.client, message)
                client_log.info(f'{message} sent to {self.client}')
            elif txt == 'd':
                contact = input('Enter contact: ')
                message = {
                    'action': 'del_contact',
                    'time': time(),
                    'user_login': contact,
                    'user': {
                        'account_name': self.username,
                    }
                }
                send_message(self.client, message)
                client_log.info(f'{message} sent to {self.client}')
            else:
                to_name = input('Enter destination name')
                message = {
                    'action': 'message',
                    'time': time(),
                    'type': 'message',
                    'destination': to_name,
                    'text': txt,
                    'user': {
                        'account_name': self.username,
                        'status': 'I am here!'
                }
            }
                send_message(self.client, message)
                client_log.info(f'{message} sent to {self.client}')


def main():
    """
    Main function server. Enter point.
    :return: start client application
    """
    user_name = input("Enter Username ")
    passwd = input("Enter password")
    client_log.info(f'start program with username {user_name}')
    parser = argparse.ArgumentParser()
    parser.add_argument('addr')
    parser.add_argument('-p', '--port', default=7777, type=int)
    parser.add_argument('-r', '--receive', default=1, type=int)
    parser.add_argument('-s', '--send', default=1, type=int)
    args = parser.parse_args()

    addr = args.addr if args.addr else 'localhost'
    port = args.port
    arg_send = args.send
    arg_receive = args.receive

    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.connect((addr, port))
        client_log.info(f'{s}')

        passwd_b = passwd.encode('utf-8')
        salt = user_name.lower().encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha256', passwd_b, salt, 10000)
        passwd_hash_str = binascii.hexlify(passwd_hash)

        message = processing_presence(user_name)
        send_message(s, message)

        message_in = get_message(s)
        print(message_in)

        if message_in['response'] == 400:
            raise ConnectionError
        elif message_in['response'] == 511:
            message_data = message_in['data']
            hash_main = hmac.new(passwd_hash_str, message_data.encode('utf-8'), 'MD5')
            digest = hash_main.digest()
            dat = binascii.b2a_base64(digest).decode('ascii')
            my_message = {
                'response': 511,
                'data': dat
            }
            send_message(s, my_message)
            message_in = get_message(s)

        answ = processing_answer(message_in)
    except Exception:
        pass
    else:
        reading = Read(s)
        # reading = Thread(target=read_serv, args=(s,))
        reading.daemon = True
        if arg_receive == 1:
            if arg_send != 1:
                reading.daemon = False
            reading.start()

        sending = Send(s, user_name)
        # sending.daemon = True
        # if arg_send == 1:
            # sending.start()

    client_app = QApplication(sys.argv)
    main_window = ClientMainWindow(s, user_name)
    client_app.exec_()


if __name__ == '__main__':
    main()
