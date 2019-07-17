#!/usr/bin/env python
#-*- coding:utf-8 -*-

import imaplib_connect
import imap_utf7
import re
import os
import sys
import concurrent.futures

list_response_pattern = re.compile(
    r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)'
)


def parse_list_response(line):
    match = list_response_pattern.match(line.decode('utf-8'))
    flags, delimiter, mailbox_name = match.groups()
    mailbox_name = mailbox_name.strip('"')
    return (flags, delimiter, mailbox_name)


def fetch_thread(i, mailboxfolder):
    try:
        typ, msg_data = c.fetch(str(i+1), '(RFC822)')
        print(type(msg_data))
        file = os.path.join(mailboxfolder, str(i) + ".eml")
        with open(file, 'wb') as f:
            f.write(msg_data[0][1])
    except Exception as err:
        print(err)
        return (False, i)
    return (True, i)


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
            mailbox_name_utf8 = imap_utf7.decode(mailbox_name.encode("UTF-7"))

            mailboxfolder = os.path.join(usernamepath, mailbox_name_utf8)
            print(type(mailboxfolder))
            if os.path.isdir(mailboxfolder) == False:
                os.mkdir(mailboxfolder)

            #选择夹子
            typ2, data2 = c.select(mailbox_name, readonly=False)

            num_msgs = int(data2[0])
            if (num_msgs <= 0):
                continue
            ex = concurrent.futures.ThreadPoolExecutor(max_workers=2)
            wait_for = [
			    ex.submit(fetch_thread, i, mailboxfolder)
			    for i in range(num_msgs)
			]

            try:
                for f in concurrent.futures.as_completed(wait_for,timeout=10):
                    print ('main: result: {}'.format(f.result()))
            except concurrent.futures.TimeoutError as err:
                print (err)
                



 
