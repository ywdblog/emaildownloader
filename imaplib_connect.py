#!/usr/bin/env python
#-*- coding:utf-8 -*-

import imaplib
import configparser
import os


def readconf():
    config = configparser.ConfigParser()
    path = os.path.dirname(os.path.realpath(__file__))
    file = os.path.join(path, '.pymotw')
    config.read([os.path.expanduser(file)])
    #config["env"]={'path':path}

    options = {'path': path, 'account': []}

    for section in config.sections():
        account = {}
        account['hostname'] = config.get(section, 'hostname')
        account['port'] = config.get(section, 'port')
        account['username'] = config.get(section, 'username')
        account['password'] = config.get(section, 'password')
        options['account'].append(account)

    return options



def open_connection(verbose=False,hostname='',port='',username='',password=''):
    
    # Read the config file
    if verbose:
        print('Connecting to', hostname)
    try:
        connection = imaplib.IMAP4_SSL(hostname, port)
    except Exception as err:
        print(err, "connecterror")
        return False
    if verbose:
        print('Logging in as', username)
    try:
        connection.login(username, password)
    except Exception as err:
        print(err, "autherror")
        return False
    return connection
