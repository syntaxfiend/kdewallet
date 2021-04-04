This is a simple project that wraps the `kwallet-query` command.
It was made to be flexible you can use whichever syntax suites your fancy
the way that kde structures their password storage is
wallet name -> folder name -> entry name  
so for example we'll assume we have two wallets each having two folders with two entries  


this module can be used in 3 ways here's a quick overview
```
from kdewallet import KDEWallet
my_pw = KDEWallet.wallet.folder.entry
my_pw = KDEWallet[wallet][folder][entry]

# these are the more procedural style options
my_pw = KDEWallet(wallet, folder).get_entry(entry)
my_pw = KDEWallet(wallet).get_entry(entry, folder=folder)

# setting is supported as well
KDEWallet.wallet.folder.entry = 'really secure'
```

For a more detailed example we'll assume we have two wallets just like this.
```
work       # wallet 1
  servera  # folder 1
    root   # entry 1 in folder 1
    userx  # etnry 2 in folder 1

  serverb
    userz
    usery

personal  # wallet 2
  gmail   # folder 1 in wallet 2
    frank # entry 1  
    maddy

  banking     # etc
    evil bank
    meh credit union
```

so given that setup of data some examples of how you might use this would be as follows
```
from kdewallet import KDEWallet
my_wallet = KDEWallet(wallet='work')
my_pw = my_wallet.get_entry(entry='root', folder='servera')
function_that_needs_password(my_pw)
other_pw = my_wallet.get_entry('frank', 'gmail', 'personal')
function_that_needs_password(other_pw)
```

This could use a bit more work still, but the core tests are passing
most functionality seems to be working well enough for now. Not sure why I went mad with the
alternate syntax styles but ya gotta have fun sometimes I guess.

Currently my todos for this project are:
- find if there is a more secure way to pass pw to kwallet-query than printf
- add defult wallet/folder support to object access
- make it clearer whats happening with properties
- write more rigorous tests

