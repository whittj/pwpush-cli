#/usr/bin/env python3
#Written by James Whittington

import requests
import json
import argparse
import getpass
import sys


class main():
    def __init__(self):
        """
        Parse arguments.
        """
        parser = argparse.ArgumentParser(description=' Password Pusher cli client.  Easy sharing of passwords securily')
        parser.add_argument('-p', metavar='Password', type=str, help='Password to share securily')
        parser.add_argument('-d', metavar='[Days live]', type=str, help='Number of days you want the secret to be available.')
        parser.add_argument('-v', metavar='[Total views]', type=str, help='Number of views you want the secret to be available.')
        args = parser.parse_args()

        expire_after_days = None
        expire_after_views = None

        if args.d:
            expire_after_days = args.d
        if args.v:
            expire_after_views = args.v

        if args.p == None:
            args.p = self.get_password()

        self.encode(args.p, expire_after_days, expire_after_views)

    def get_password(self):
        if not sys.stdin.isatty():
            data = sys.stdin.readline()
            password = data[0].rstrip()
        else:
            password = getpass.getpass()
        return password

    def encode(self, payload, expire_after_days = 7, expire_after_views = 5):
        """
        Send password, days and views to pwpush.  Parse output and return working URL.
        """
        message = 'password[payload]={}&password[expire_after_days]={}&password[expire_after_views]={}'.format(payload, expire_after_days, expire_after_views)
        r = requests.post('https://pwpush.com/p.json', data = message)
        if r.status_code > 200 and r.status_code < 299:
            reponse = json.loads(r.text)
            url = 'https://pwpush.com/p/{}'.format(reponse['url_token'])
            print(url)
            return 0
        else:
            print('Something went wrong with pwpush.  Error {}'.format(r.status_code))
            return 1

if __name__ == '__main__':
    main = main()
