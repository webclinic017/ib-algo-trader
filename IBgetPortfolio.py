from __future__ import (absolute_import, division, print_function,)
#                        unicode_literals)

import collections
import sys

if sys.version_info.major == 2:
    import Queue as queue
    import itertools
    map = itertools.imap

else:  # >= 3
    import queue


import ib.opt
import ib.ext.Contract


class IbManager(object):
    def __init__(self, timeout=20, **kwargs):
        self.q = queue.Queue()
        self.timeout = 20

        self.con = ib.opt.ibConnection(**kwargs)
        self.con.registerAll(self.watcher)

        self.msgs = {
            ib.opt.message.error: self.errors,
            ib.opt.message.updatePortfolio: self.acct_update,
            ib.opt.message.accountDownloadEnd: self.acct_update,
        }

        # Skip the registered ones plus noisy ones from acctUpdate
        self.skipmsgs = tuple(self.msgs.keys()) + (
            ib.opt.message.updateAccountValue,
            ib.opt.message.updateAccountTime)

        for msgtype, handler in self.msgs.items():
            self.con.register(handler, msgtype)

        self.con.connect()

    def watcher(self, msg):
        if isinstance(msg, ib.opt.message.error):
            if msg.errorCode > 2000:  # informative message
                print('-' * 10, msg)

        elif not isinstance(msg, self.skipmsgs):
            print('-' * 10, msg)

    def errors(self, msg):
        if msg.id is None:  # something is very wrong in the connection to tws
            self.q.put((True, -1, 'Lost Connection to TWS'))
        elif msg.errorCode < 1000:
            self.q.put((True, msg.errorCode, msg.errorMsg))

    def acct_update(self, msg):
        self.q.put((False, -1, msg))

    def get_account_update(self):
        self.con.reqAccountUpdates(True, 'DU958186')

        portfolio = list()
        while True:
            try:
                err, mid, msg = self.q.get(block=True, timeout=self.timeout)
            except queue.Empty:
                err, mid, msg = True, -1, "Timeout receiving information"
                break

            if isinstance(msg, ib.opt.message.accountDownloadEnd):
                break

            if isinstance(msg, ib.opt.message.updatePortfolio):
                c = msg.contract
                ticker = '%s-%s-%s' % (c.m_symbol, c.m_secType, c.m_exchange)

                entry = collections.OrderedDict(msg.items())

                # Don't do this if contract object needs to be referenced later
                entry['contract'] = ticker  # replace object with the ticker

                portfolio.append(entry)

        # return list of contract details, followed by:
        #   last return code (False means no error / True Error)
        #   last error code or None if no error
        #   last error message or None if no error
        # last error message

        return portfolio, err, mid, msg


ibm = IbManager(clientId=100)

portfolio, err, errid, errmsg = ibm.get_account_update()

if portfolio:
    print(','.join(portfolio[0].keys()))

for p in portfolio:
    print(','.join(map(str, p.values())))

sys.exit(0)  # Ensure ib thread is terminated