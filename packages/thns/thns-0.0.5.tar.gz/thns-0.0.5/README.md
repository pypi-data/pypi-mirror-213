[![pipeline status](https://gitlab.com/0bs1d1an/thns/badges/master/pipeline.svg)](https://gitlab.com/0bs1d1an/thns/commits/master)

# Telegram HTTP notification script

This script will notify you of any or selected HTTP requests made to your server, using the Telegram API.
It basically performs a `tail -F` on a specified web server access log file (only Nginx is supported for now).
Then for each new request it sends a Telegram message to your specified channel.

## Rationale

During a red teaming operation I was tasked with writing a script similar to this one, as part of a phishing campaign we launched for our intial entry.
The goal of this script was to keep track of people that clicked on our link, downloaded our malicious payload, and submitted a form with their personal details.
We wanted to instantly know when such events happened, so that we could move on to the next flag using their compromised box.
I decided to make this script more general-purpose and further maintain it here. :-)

## Features

- [X] Continuously read the access log, even when the log file is rotated;
- [X] Can only match specified requests (e.g. only /robots.txt, /wp-login.php);
- [X] Can add the user agent to the message;
- [X] Can ignore specified IPs (e.g. 127.0.0.1, ::1);
- [X] Can ignore specified HTTP status codes (e.g. 301, 302);
- [X] Can look up geo location of the requesting IP;
- [X] Can post the location on the map;
- [X] Can silently push Telegram messages.

## How to set it up

TL;DR - basically 4 steps:

1. Create your own Telegram bot;
1. Create a new (private) channel and add your bot to that channel;
1. Either hardcode your bot key, chat ID, and web server log file in this script, or use the script arguments;
1. Consider either editing and installing the systemd / OpenRC service script, or running the script in a `screen` session to run it in the background.

Detailed explanation: 

First, you will need to create your own [Telegram bot](https://core.telegram.org/bots), which is basically just an API key without any logic (unless you really want to create a [full fledged bot](https://python-telegram-bot.org/)).
Once you've created your bot using the [@BotFather](https://telegram.me/BotFather) it will also tell your the bot key (API key).
You can either hardcode the bot key in this script, or provide it as an argument (-k) when running this script.

Second, create a Telegram (private) channel and write down the chat ID.
If you have trouble finding the chat ID, you can use [@username_to_id_bot](https://telegram.me/username_to_id_bot) and paste the invite link in there.
It will tell you the channel's chat ID, which you can also hardcode into the script if you want, or provide it as an argument (-c) when running this script.
Don't forget to also explicitely add the bot to the channel.

Third, either hardcode the web server's access log file location as well, or provide it as an argument (-l) when running this script.

Finally, run the script.
You could use the thns.service systemd script if you use systemd.
Edit the script and install it like described in the Install section below.
Or, you could also quickly run the script in a `screen` session to run it in the background so that you can leave your shell.
See the Example section for an example on how to do this.
Now you can safely logout and the script will remain in the background.
To attach again, login to your server again and run `screen -r thns`.

## Install

Using Pip:

```
# python3 -m pip install thns
```

Or, using setup.py:

```
# python3 setup.py install
```

If you use systemd, you can also add the service script.
Edit the script with your own arguments and install it like so:

```
# cp thns.service /etc/systemd/system/
# systemctl daemon-reload
# systemctl enable --now thns.service
```

For OpenRC, edit the init script and then install it like so:

```
# cp thns.init /etc/init.d/
# rc-update add thns
# rc-service thns start
```

Installing the service script remains a manual step for now.
I don't know if there's any way to make this part of the pip package (please reach out to me if you know how to).
You could also reach out to your local OS package manager and ask them to make an OS package for this. ;-)

## Usage

You can use thns in two ways:

* When installed as a package, call the installed script: `thns --help`;
* When Git cloned, call the package directly from the root of the Git repository: `python -m thns --help`.

```
usage: thns [-h] [-c TELEGRAM_CHAT_ID] [-g] [-iI IGNORE_IPS [IGNORE_IPS ...]]
            [-iH IGNORE_HTTP_STATUS_CODES [IGNORE_HTTP_STATUS_CODES ...]]
            [-k TELEGRAM_BOT_KEY] [-l LOG_FILE] [-m]
            [-r MATCH_REQUESTS [MATCH_REQUESTS ...]] [-s] [-u]

Get Telegram notifications when requests are being made to your web server

optional arguments:
  -h, --help            show this help message and exit
  -c TELEGRAM_CHAT_ID, --chat-id TELEGRAM_CHAT_ID
                        Specify the Telegram chat ID to post to.
  -g, --geo             Include geographical information.
  -iI IGNORE_IPS [IGNORE_IPS ...], --ignore-ips IGNORE_IPS [IGNORE_IPS ...]
                        Ignore (multiple) IP addresses (e.g. 127.0.0.1 ::1).
  -iH IGNORE_HTTP_STATUS_CODES [IGNORE_HTTP_STATUS_CODES ...], --ignore-http-status-codes IGNORE_HTTP_STATUS_CODES [IGNORE_HTTP_STATUS_CODES ...]
                        Ignore (multiple) HTTP status codes (e.g. 301 302).
  -k TELEGRAM_BOT_KEY, --bot-key TELEGRAM_BOT_KEY
                        Specify the Telegram bot key.
  -l LOG_FILE, --log-file LOG_FILE
                        Specify the (Nginx) log file.
  -m, --map             Post a map pointer.
  -r MATCH_REQUESTS [MATCH_REQUESTS ...], --match-requests MATCH_REQUESTS [MATCH_REQUESTS ...]
                        Match (multiple) specific HTTP requests (e.g. /
                        /robots.txt).
  -s, --silent          Send Telegram messages silently.
  -u, --user-agent      Include the user agent string.
```

## Example

If you've edited and installed the systemd / OpenRC service script (see the Install section), you can start / stop it like any other service:

```
# systemcl start thnd.service  # systemd
# rc-service thns start        # OpenRC
```

You could also use `screen` to quickly run it in the background.
For example:

```
$ screen -S thns -d -m python3 -m thns -m -s -l /var/log/nginx/access.log -c "-1234567890123" -k "123456789:1234567890abcdefghijklmnopqrstuvwxyz" -iI 127.0.0.1 ::1
```

Then watch your Telegram channel fill:

![Example](example/example.jpg)

