.. image:: https://ipfs.io/ipfs/QmeByEj99cRBRHZnNMGov98DXctf4cUMfX4ywsPD1QYpWY

=======
thangar
=======

.. image:: https://badge.fury.io/py/thangar.svg
    :target: https://pypi.org/project/thangar

Hangar of Telegram accounts.

Have you ever had more accounts than Telegram client allows to store at the
same time? I have. So I build this little script which does:

1. kind of "park" new accounts,
2. store secret tokens in database,
3. show last service message from Telegram to let you log in through normal client.

Try it out yourself!

Installation
------------

::

    python -m pip install thangar

Usage
-----

::

    export API_ID=...  # get from https://my.telegram.org/apps
    export API_HASH=...  # ^^
    thangar [OPTIONS] COMMAND [ARG]

Example
-------

::

	% thangar track

							  Accounts
	┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
	┃ Id         ┃ Name           ┃ Phone       ┃ Username     ┃
	┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
	│ 1234567890 │ Oskar Sharipov │ +7123456789 │ oskar        │
	│ 1297676593 │ Oskar Again    │ +3456776543 │ oskar2       │
	│ 1578935718 │ Bobby          │ +1212123421 │ FlamingoSays │
	└────────────┴────────────────┴─────────────┴──────────────┘

Use "``thangar --help``" for more information.

Tip
---

Export environment variables in a ``~/.zshenv`` or other shell file!
