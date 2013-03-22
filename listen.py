#!/usr/bin/env python
# Original script written by Stuart Colville: http://muffinresearch.co.uk/archives/2010/10/15/fake-smtp-server-with-python/
"""A noddy fake smtp server."""

import smtpd
import asyncore
import time
import os
import errno


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class FakeSMTPServer(smtpd.SMTPServer):
    """A Fake smtp server"""

    def __init__(*args, **kwargs):
        print "Running fake smtp server"
        smtpd.SMTPServer.__init__(*args, **kwargs)

    def process_message(*args, **kwargs):
        mail = open(os.path.join("mails", str(time.time()) + ".eml"), "w")
        print "New mail from " + args[2]
        mail.write(args[4])
        mail.close


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=25,
                    help="port to listen on. Default 25.")
    args = parser.parse_args()

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    mkdir_p('mails')

    smtp_server = FakeSMTPServer(('localhost', args.port), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()
