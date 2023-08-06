# haveibeenpwned-asyncio

v0.0.4

Library to query and check haveibeenpwned with the aiohttp library.

NB: I have added async to sync methods if you are not writing async code. Every query function has an
corresponding synchronous call -> example query_account_sync()

## Install
```bash
pip install haveibeenpwned-asyncio
# or
poetry add haveibeenpwned-asyncio
```

## Usage
See example.py for more uses

Ex:
```python
import os
from haveibeenpwned_asyncio import haveIbeenPwnedPasswords, haveIbeenPwnedAccount, haveIbeenPwnedPastes
import asyncio

if __name__ == "__main__":
    # Validation Class, inherits from Indentity Class
    loop = asyncio.get_event_loop()
    passwords = ["P@ssw0rd"]
    accounts = ["admin@gmail.com", "test@test.com", "test@gmail.com"]

    test_passwords = haveIbeenPwnedPasswords(
                passwords=passwords, semaphore_max=10
            )
    print(loop.run_until_complete(test_passwords.query_passwords()))
    print(test_passwords.query_passwords_sync())

    test_acc = haveIbeenPwnedAccount(
        accounts=accounts,
        semaphore_max=10,
        api_key=os.getenv("HAVEIBEENPWNED_API_KEY", None),
    )
    print(loop.run_until_complete(test_acc.query_accounts()))
    print(test_acc.query_accounts_sync())

    test_pastes = haveIbeenPwnedPastes(
        accounts=accounts,
        semaphore_max=5,
        api_key=os.getenv("HAVEIBEENPWNED_API_KEY", None),
    )
    print(loop.run_until_complete(test_pastes.query_accounts()))
    print(test_pastes.query_accounts_sync())

```

## API Key
Some of the endpoints (breachedAccount) require authentication in the v3 of the API.
This is to prevent script kiddies and abuse of the api, see blog post: 
https://www.troyhunt.com/authentication-and-the-have-i-been-pwned-api/

To get an API key follow: https://haveibeenpwned.com/API/Key

Usage:
```python
# Could use env variables
haveIbeenPwnedAccount(
            accounts=accounts,
            semaphore_max=10,
            api_key=os.getenv("HAVEIBEENPWNED_API_KEY", None))

# or 

haveIbeenPwnedAccount(
            accounts=accounts,
            semaphore_max=10,
            api_key='xxxxxxxxx')
```

## CLI
Includes a CLI interface using pythong click library

```bash
(.venv) goose@pop-os:~/Development/haveibeenpwned_asyncio$ haveibeenpwned_async --help
Usage: haveibeenpwned_async [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  accounts
  passwords
  pastes


```

## Speed
Check the file run_test_speed.py. This will give you an idea of the speedup asyncio does with multiple IO bound network calls

## TODO:
* Add API key to github actions for pytest to pass on breachedAccount

## Donations
Please feel free to buy me a cup of coffee as I pay a monthly $3 to test the library against haveibeenpwned's 
monthly billed API key

buymeacoffee.com/crypticg00se                

