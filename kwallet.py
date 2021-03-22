from subprocess import getstatusoutput as cmd

class DynamicAttribute(type):
    """
    this allows the inheriting class to
    return an initialized instance of itself
    with the first argument passed to the constructor
    having a value of whatever attribute you try to access
    """
    def __getattr__(cls, key):
        try:
            return KDEWallet(key)
        except AttributeError:
            raise AttributeError(f"type object '{cls.__class__.__name__}' has no attribute '{key}'")


class KDEWallet(metaclass=DynamicAttribute):
    def __init__(s, wallet='kdewallet', folder=None):
        s.wallet = wallet
        s.folder = folder
        errs = {f'Wallet {wallet} not found', f'The folder {folder} does not exist!'}
        res = cmd(f"kwallet-query -l '{wallet}' -f '{folder or 'Passwords'}'")
        if res[0] != 0 or res[1] in errs:
            raise AttributeError(res[1])

    def __getattr__(s, key):
        try:
            return s[key]
        except Exception as e:
            raise e


    def __getitem__(s, key):
        if folder := s.isfolder(key, s.wallet):
            if key != s.folder:
                return KDEWallet(s.wallet, key)
        if s.isentry(key, s.folder, s.wallet):
            return s.get_entry(key, s.folder, s.wallet)
        raise AttributeError


    def __class_getitem__(cls, key):
        """
        this is a continuation of what the above metaclass is doing but
        we're just doing it with bracket syntax here
        """
        return cls(key)

    def __setattr__(s, key, val):
        if key not in {'folder', 'wallet', 'entry'}:
            if s.isentry(key, s.folder, s.wallet):
                s.set_entry(key, val, s.folder, s.wallet)
        super().__setattr__(key, val)

    def get_entries(s, wallet=None, folder=None):
        """
        return a list of possibe entries from a wallet folder combination
        the default wallet is 'kdewallet' and the defualt folder is 'Passwords'
        """
        folder = folder or s.folder or 'Passwords'
        wallet = wallet or s.wallet
        res = cmd(f"kwallet-query -l '{wallet}' -f '{folder}'")
        if res[0] != 0 or res[1].endswith('does not exist!'):
            raise AttributeError(res[1])
        return res[1].split('\n')

    def get_entry(s, entry, folder=None, wallet=None):
        """
        return the value that is stored under the specified entry
        """
        folder = folder or s.folder or 'Passwords'
        wallet = wallet or s.wallet
        res = cmd(f"kwallet-query -r '{entry}' -f '{folder}' '{wallet}'")
        if res[0] != 0 or res[1].startswith('Failed to read entry'):
            raise AttributeError(res[1])
        return res[1]

    def set_entry(s, entry, val, folder=None, wallet=None):
        folder = folder or s.folder or 'Passwords'
        wallet = wallet or s.wallet
        if not s.isentry(entry, folder, wallet):
            raise AttributeError(f'The entry {entry} does not exist in the folder {folder}')
        cmd(f"echo '{val}' | kwallet-query -w '{entry}' -f '{folder}' '{wallet}'")


    @staticmethod
    def iswallet(wallet):
        """
        given a string determine if this its a valid wallet
        """
        try:
            KDEWallet(wallet)
        except AttributeError:
            return False
        else:
            return True

    @staticmethod
    def isfolder(folder, wallet='kdewallet'):
        """
        given a folder and optionally a wallet determine if the pair is Valid
        """
        try:
            KDEWallet(wallet, folder)
        except AttributeError as e:
            return False
        else:
            return True

    @staticmethod
    def isentry(entry, folder='Passwords', wallet='kdewallet'):
        """
        given an entry and optionally folder and wallet determine if they are valid
        """
        try:
            KDEWallet(wallet, folder).get_entry(entry)
        except AttributeError:
            return False
        else:
            return True
