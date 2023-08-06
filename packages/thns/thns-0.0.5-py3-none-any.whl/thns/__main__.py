#!/usr/bin/env python3

""" thns """

import argparse
import json
import os
import re
import requests
import time
# from pprint import pprint


def get_args():
    """ Get arguments """

    parser = argparse.ArgumentParser(
        description='Get Telegram notifications when requests are being ' +
        'made to your web server')
    parser.add_argument(
        '-c', '--chat-id',
        # Replace to hardcode your chat ID
        default="-1234567890123",
        dest='telegram_chat_id',
        help='Specify the Telegram chat ID to post to.')
    parser.add_argument(
        '-g', '--geo',
        action='store_true',
        default=None,
        dest='get_location',
        help='Include geographical information.')
    parser.add_argument(
        '-iI', '--ignore-ips',
        # Add IPs to hardcode the IPs you do not want to send messages for
        default=[],
        help='Ignore (multiple) IP addresses (e.g. 127.0.0.1 ::1).',
        nargs='+')
    parser.add_argument(
        '-iH', '--ignore-http-status-codes',
        # Add HTTP status codes to hardcode the HTTP status codes you do not
        # want to send messages for
        default=[],
        help='Ignore (multiple) HTTP status codes (e.g. 301 302).',
        nargs='+')
    parser.add_argument(
        '-k', '--bot-key',
        # Replace to hardcode your bot key
        default="123456789:1234567890abcdefghijklmnopqrstuvwxyz",
        dest='telegram_bot_key',
        help='Specify the Telegram bot key.')
    parser.add_argument(
        '-l', '--log-file',
        # Replace to hardcode your web server's log file
        default="/var/log/nginx/access.log",
        help='Specify the (Nginx) log file.')
    parser.add_argument(
        '-m', '--map',
        action='store_true',
        default=None,
        dest="map_pointer",
        help='Post a map pointer.')
    parser.add_argument(
        '-r', '--match-requests',
        # Add documents to hardcode the documents you want to send messages for
        default=[],
        help='Match (multiple) specific HTTP requests (e.g. / /robots.txt).',
        nargs='+')
    parser.add_argument(
        '-s', '--silent',
        action='store_true',
        default=None,
        help='Send Telegram messages silently.')
    parser.add_argument(
        '-u', '--user-agent',
        action='store_true',
        default=None,
        dest='post_ua',
        help='Include the user agent string.')

    return parser.parse_args()


def tail(logfile):
    '''
    Continuously read logfile for new lines. This will also load the new
    logfile in case the current logfile is rotated by logrotate. In other
    words, its function is similar to `Tail -F`
    '''

    # Open the file
    current_logfile = open(logfile, "r")

    # Seek the end of the file
    current_logfile.seek(0, os.SEEK_END)

    # Save the current inode of the logfile
    current_inode = os.fstat(current_logfile.fileno()).st_ino

    # Start first loop
    while True:

        # Start second loop, which we break if no new line
        while True:

            # Read line from current logfile
            line = current_logfile.readline()

            # If no new line, break
            if not line:
                break

            # Else, yield new line
            else:
                yield line

        try:
            # Once broken out of the second loop, compare inode of potential
            # new log file
            if os.stat(logfile).st_ino != current_inode:

                # If new inode, then continue with this new log file
                new = open(logfile, "r")
                current_logfile.close()
                current_logfile = new
                current_logfile.seek(0, os.SEEK_END)
                current_inode = os.fstat(current_logfile.fileno()).st_ino
                continue

        except IOError:
            pass

        # Sleep for 1 second, and repeat cycle
        time.sleep(1)


def main():
    """ Main function """

    args = get_args()
    loglines = tail(args.log_file)

    # Loop over each log file line
    for line in loglines:

        # Get the originating IP, request, HTTP status code, and user agent
        # from each new line
        src_addr = line.split()[0]
        request = re.sub(r' HTTP/.*', '', line.split("\"")[1])
        http_code = line.split("\"")[2].split()[0]
        ua = line.split("\"")[5]

        # Do not proceed if 'line' matches any stuff we excluded
        if (src_addr not in args.ignore_ips) \
                and (http_code not in args.ignore_http_status_codes):

            # If client requests any document (in 'args.match_requests'),
            # then proceed
            if (request.split()[1] in args.match_requests) \
                    or (not args.match_requests):

                # If 'args.get_location' or 'args.map_pointer', get location
                # stuff first
                if args.get_location or args.map_pointer:
                    try:
                        whois = requests.get(
                                'https://ipinfo.io/' + src_addr).json()
                        country = whois['country']
                        region = whois['region']
                        city = whois['city']
                        org = whois['org']
                        latitude = whois['loc'].split(",")[0]
                        longitude = whois['loc'].split(",")[1]
                        client = src_addr + " (" + country + ", " + region + \
                            ", " + city + ", " + org + ")"
                    except Exception:
                        client = src_addr
                        latitude = None
                        longitude = None
                else:
                    client = src_addr

                # If 'args.post_ua'
                if args.post_ua:
                    user_agent = ", using " + ua
                else:
                    user_agent = str()

                # Telegram API end point
                telegram_api = "https://api.telegram.org/bot" + \
                    args.telegram_bot_key

                # Post message
                text = client + " requested " + request + " (" + \
                    http_code + ")" + user_agent
                data = {'chat_id': args.telegram_chat_id,
                        'text': text,
                        'disable_web_page_preview': 1,
                        'disable_notification': args.silent}
                payload = json.dumps(data)
                headers = {'Content-type': 'application/json'}
                requests.post(
                    telegram_api + "/sendMessage",
                    data=payload,
                    headers=headers)

                # If 'args.map_pointer' and 'latitude' and 'longitude', post
                # location on the map as well
                if args.map_pointer and latitude and longitude:
                    data = {'chat_id': args.telegram_chat_id,
                            'latitude': latitude,
                            'longitude': longitude,
                            'disable_notification': args.silent}
                    payload = json.dumps(data)
                    headers = {'Content-type': 'application/json'}
                    requests.post(
                        telegram_api + "/sendLocation",
                        data=payload,
                        headers=headers)

        # In the case that a following request cannot be looked up for geo
        # stuff, we throw away our old information, to avoid reusing the
        # previously looked up geo stuff
        whois = None
        country = None
        region = None
        city = None
        org = None
        latitude = None
        longitude = None


if __name__ == '__main__':
    main()
