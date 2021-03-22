import unittest
from kwallet import KDEWallet as KW
from subprocess import getstatusoutput as cmd
"""
these tests assume
you have two wallets setup
one like this
    wallet name: test
    folder name: test
    entry name : test

and one like This
    wallet name: onetest
    folder name: twotest
    entry name : threetest
"""
bw = 'bad wallet name'
gw = 'test'
bf = 'bad folder name'
gf = 'test'
be = 'bad entry'
ge = 'test'
bv = 'this is not what is stored in kdewallet'
gv = 'success'
AE = AttributeError

class WalletInitTests(unittest.TestCase):
    """
    each level of testing assumes the previous level passed
    so entry is not tested until folder is and folder not until wallet is
    """

    def test_wallet(s):
        s.assertRaises(AE, KW, bw)
        s.assertIsInstance(KW(gw), KW)

    def test_folder(s):
        s.assertRaises(AE, KW, gw, bf)
        s.assertRaises(AE, KW, bw, gf)
        s.assertRaises(AE, KW, bw, bf)
        s.assertIsInstance(KW(gw, gf), KW)

class WalletAccessTests(unittest.TestCase):
    def test_access(s):
        with s.assertRaises(AE) as err:
            KW.devnull
        with s.assertRaises(AE):
            KW.test.devnull
        with s.assertRaises(AE):
            KW.test.test.devnull

        s.assertIsInstance(KW.test, KW)
        s.assertIsInstance(KW.test.test, KW)
        s.assertIsInstance(KW['test'], KW)
        s.assertIsInstance(KW['test']['test'], KW)
        s.assertIsInstance(KW['test'].test, KW)
        s.assertIsInstance(KW.test['test'], KW)

        s.assertEqual(KW.test.test.test, gv)
        s.assertEqual(KW.test.test['test'], gv)
        s.assertEqual(KW.test['test'].test, gv)
        s.assertEqual(KW.test['test']['test'],gv)
        s.assertEqual(KW['test'].test.test, gv)
        s.assertEqual(KW['test'].test['test'],gv)
        s.assertEqual(KW['test']['test'].test, gv)
        s.assertEqual(KW['test']['test']['test'], gv)

        with s.assertRaises(AE):
            KW[bw]
        with s.assertRaises(AE):
            KW[gw][bf]
        with s.assertRaises(AE):
            KW[gw][gf][be]



class WalletSetTests(unittest.TestCase):
    def setUp(s):
        cmd(f"echo '{gv}' | kwallet-query -w '{ge}' -f '{gf}' '{gw}'")

    def tearDown(s):
        cmd(f"echo '{gv}' | kwallet-query -w '{ge}' -f '{gf}' '{gw}'")

    def test_set(s):
        new_val = 'whooptie dooptie'
        s.assertEqual(KW.test.test.test, gv)
        KW.test.test.test = new_val
        s.assertEqual(KW['test'].test.test, new_val)

        with s.assertRaises(AE):
            KW('test').set_entry('yamosh', 'fake_val', folder='test')

class WalletExtraTests(unittest.TestCase):
    def test_get_entries(s):
        with s.assertRaises(AE):
            KW('test').get_entries(folder=bf)
        s.assertEqual(KW.test.get_entries(folder=gf), ['test','test3'])

    def test_iswallet(s):
        s.assertFalse(KW.iswallet(bw))
        s.assertTrue(KW.iswallet(gw))

    def test_isentry(s):
        s.assertFalse(KW.isentry(be, gf, gw))
        s.assertTrue(KW.isentry(ge, gf, gw))

def suite():
    suite = unittest.TestSuite()
    for c in (WalletInitTests, WalletAccessTests, WalletSetTests, WalletExtraTests):
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(c))
    return suite

if __name__ == '__main__':
   unittest.TextTestRunner(verbosity=2).run(suite())
