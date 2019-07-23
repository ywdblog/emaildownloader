#!/usr/bin/env python
#-*- coding:utf-8 -*-

import imaplib_connect
import imap_utf7
import re
import os
import sys
import concurrent.futures
import socket
socket.setdefaulttimeout(10)

list_response_pattern = re.compile(
    r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)'
)


def parse_list_response(line):
    match = list_response_pattern.match(line.decode('utf-8'))
    flags, delimiter, mailbox_name = match.groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)


def fetch_thread(i, mailboxfolder, mailbox_name, account):
    global c
    try:
        typ, msg_data = c.fetch(str(i+1), '(RFC822)')
        file = os.path.join(mailboxfolder, str(i) + ".eml")
        with open(file, 'wb') as f:
            f.write(msg_data[0][1])
    except Exception as err:
        c = imaplib_connect.open_connection(False, **account)
        c.select(mailbox_name, readonly=False)

        print(err, "curl")
        return (False, i)
    return (True, i)


def done(fn):
    print(fn.cancelled(), fn.done())


options = imaplib_connect.readconf()
for account in options['account']:
    with imaplib_connect.open_connection(False, **account) as c:
        path = options['path']
        usernamepath = os.path.join(path, account["username"])
        if os.path.isdir(usernamepath) == False:
            os.mkdir(usernamepath)

        typ, data = c.list()
        for line in data:
            flags, delimiter, mailbox_name = parse_list_response(line)

            # 输入参数是bytes类型，返回str类型
            try:
                mailbox_name_utf8 = imap_utf7.decode(
                    mailbox_name.encode("UTF-7"))
            except Exception as err:
                #mailbox_name_utf8 = "INBOX"
                continue 

            mailboxfolder = os.path.join(usernamepath, mailbox_name_utf8)
            if os.path.isdir(mailboxfolder) == False:
                os.mkdir(mailboxfolder)

            try:
                #连接可能会断开，所以选择重新连接
                typ2, data2 = c.select(mailbox_name, readonly=False)
            except Exception as err:
                c = imaplib_connect.open_connection(False, **account)
                typ2, data2 = c.select(mailbox_name, readonly=False)
                print("连接已断开，选择重新连接")

            num_msgs = int(data2[0])
            print(mailbox_name_utf8, num_msgs)
            if (num_msgs <= 0):
                continue
            ex = concurrent.futures.ThreadPoolExecutor(max_workers=5)
            #ex.submit返回Future对象
            wait_for = [
                ex.submit(fetch_thread, i, mailboxfolder,
                          mailbox_name, account)
                for i in range(num_msgs)
            ]

            for i in range(num_msgs):
                wait_for[i].arg = i
                wait_for[i].add_done_callback(done)

            try:
                for f in concurrent.futures.as_completed(wait_for):
                    print('main: result: {}'.format(f.result(timeout=10)))
            except concurrent.futures.TimeoutError as err:
                print(err, "TimeoutError")
            except Exception as err:
                pass

            #ex.shutdown()
