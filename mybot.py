import pprint
import zulip
import sys
import re
import json
import os
import httplib2
import aftership

p = pprint.PrettyPrinter()
BOTMAIL = "cheese-bot@shehacks.zulipchat.com"


class Courier(object):
    def __init__(self):
        self.client = zulip.Client(site="https://shehacks.zulipchat.com/api")
        self.api = aftership.APIv4('c82e624d-909f-4954-a99c-2f7a993a40d2')
        self.subscribe_all()
        print("done init")

    def subscribe_all(self):
        json = self.client.get_streams()["streams"]
        streams = [{"name": stream["name"]} for stream in json]
        self.client.add_subscriptions(streams)

    def process(self, msg):
        print(msg)
        content = msg["content"].split()
        sender_mail = msg["sender_email"]
        ttype = msg["type"]
        stream_name = msg["display_recipient"]
        stream_topic = msg["subject"]
        if sender_mail == BOTMAIL:
            return

        if content[0].lower() == "courier" or content[0].lower() == "@**Courier**":
            if content[1] == "track":
                sendingone = ""
                a = self.api.trackings.get(content[2], content[3])
                if 'meta' in a and a['meta']['message'] == 'Tracking does not exist.':
                    self.api.trackings.post(tracking=dict(
                        content[2], content[3], title="Title"))
                    a = self.api.trackings.get(content[2], content[3])
                a = a["tracking"]["checkpoints"]
                for check in a:
                    sendingone = sendingone + \
                        str(check['checkpoint_time']) + \
                        "\n" + check['message'] + "\n"
                print("done")
                self.client.send_message({
                    "type": "stream",
                    "subject": msg["subject"],
                    "to": msg["display_recipient"],
                    "content": sendingone
                })
        else:
            return


def main():
    bot = Courier()
    bot.client.call_on_each_message(bot.process)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("msmsmsmms")
        sys.exit(0)
