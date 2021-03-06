import unittest
from neatrader.model import Option, Security, OptionChain, Quote
from datetime import datetime


class TestOptionChain(unittest.TestCase):
    def test_search(self):
        security = Security('TSLA')
        o1 = Option('call', security, 500, datetime(2020, 4, 1))
        o1.theta = -2.02
        o1.delta = 0.83
        o2 = Option('put', security, 300, datetime(2020, 4, 20))
        o2.theta = -0.16
        o2.delta = -0.34

        chain = OptionChain(security, datetime.now())
        chain.add_option(o1)
        chain.add_option(o2)

        result = chain.search(theta=-2, delta=0.8)
        assert o1.strike == result.strike
        result = chain.search(theta=-1, delta=-0.5)
        assert o2.strike == result.strike

    def test_otm(self):
        security = Security('TSLA')
        security.add_quote(Quote(420, datetime.now()))
        o1 = Option('call', security, 500, datetime(2020, 4, 20))
        o2 = Option('put', security, 300, datetime(2020, 4, 20))
        o3 = Option('call', security, 100, datetime(2020, 4, 20))  # ITM

        chain = OptionChain(security, datetime.now())
        chain.add_option(o1)
        chain.add_option(o2)
        chain.add_option(o3)

        calls, puts = chain.otm(datetime(2020, 4, 20)).values()
        assert 1 == len(calls)
        assert 1 == len(puts)

    def test_iv(self):
        security = Security('TSLA')
        security.add_quote(Quote(420, datetime.now()))
        o1 = Option('call', security, 700, datetime(2020, 4, 20))
        o3 = Option('call', security, 500, datetime(2020, 4, 20))
        o2 = Option('put', security, 400, datetime(2020, 4, 20))
        o1.iv = 5
        o1.price = 2
        o2.iv = 2
        o2.price = 4
        o3.iv = 0.5
        o3.price = 10

        chain = OptionChain(security, datetime.now())
        chain.add_option(o1)
        chain.add_option(o2)
        chain.add_option(o3)

        expected = (5 * 2 + 2 * 4 + 0.5 * 10) / (2 + 4 + 10)
        result = chain.iv(datetime(2020, 4, 20))
        assert expected == result
