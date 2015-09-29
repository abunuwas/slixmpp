#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Slixmpp: The Slick XMPP Library
    Copyright (C) 2015 Emmanuel Gil Peyrot
    This file is part of Slixmpp.

    See the file LICENSE for copying permission.
"""

import logging
from getpass import getpass
from argparse import ArgumentParser

import slixmpp
from slixmpp.exceptions import XMPPError
from slixmpp import asyncio

log = logging.getLogger(__name__)


class AnswerConfirm(slixmpp.ClientXMPP):

    """
    A basic client demonstrating how to confirm or deny an HTTP request.
    """

    def __init__(self, jid, password, trusted):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.trusted = trusted
        self.api.register(self.confirm, 'xep_0070', 'get_confirm')

    def confirm(self, jid, id, url, method):
        log.info('Received confirm request %s from %s to access %s using '
                 'method %s' % (id, jid, url, method))
        if jid not in self.trusted:
            log.info('Denied')
            return False
        log.info('Confirmed')
        return True


if __name__ == '__main__':
    # Setup the command line arguments.
    parser = ArgumentParser()
    parser.add_argument("-q","--quiet", help="set logging to ERROR",
                        action="store_const",
                        dest="loglevel",
                        const=logging.ERROR,
                        default=logging.INFO)
    parser.add_argument("-d","--debug", help="set logging to DEBUG",
                        action="store_const",
                        dest="loglevel",
                        const=logging.DEBUG,
                        default=logging.INFO)

    # JID and password options.
    parser.add_argument("-j", "--jid", dest="jid",
                        help="JID to use")
    parser.add_argument("-p", "--password", dest="password",
                        help="password to use")

    # Other options.
    parser.add_argument("-t", "--trusted", nargs='*',
                        help="List of trusted JIDs")

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    if args.jid is None:
        args.jid = input("Username: ")
    if args.password is None:
        args.password = getpass("Password: ")

    xmpp = AnswerConfirm(args.jid, args.password, args.trusted)
    xmpp.register_plugin('xep_0070')

    # Connect to the XMPP server and start processing XMPP stanzas.
    xmpp.connect()
    xmpp.process()