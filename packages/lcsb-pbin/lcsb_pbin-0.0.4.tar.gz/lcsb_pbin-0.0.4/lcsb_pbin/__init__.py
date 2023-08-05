#!/usr/bin/env python

from requests.auth import HTTPBasicAuth

from pbincli.api import PrivateBin
from pbincli.format import Paste
from pbincli.utils import PBinCLIError

FORMATTER = ("plaintext", "syntaxhighlighting", "markdown")
EXPIRE = ("5min", "10min", "1hour", "1day", "1week", "1month")



def paste(
    server,
    text,
    attachment,
    username,
    password,
    paste_password=None,
    formatter="plaintext",
    opendiscussion=False,
    burnafterreading=False,
    expire="1day",
    file=None,
    debug=False,
):
    """
    Send a Paste to the LCSB - privatebin.
    Only people with correct credentials can actually paste data as it is protected
    with basic auth.
    server: address of the privatebin server: https://privatebin.lcsb.uni.lu/
    text: the paste data
    username: username for basic auth
    password: password for basic auth
    paste_password: put password to protect paste - default: None
    formatter: paster format to use: plaintext, syntaxhighlighting, markdown - default: plaintext
    opendiscussion: if you want to allow comments - default: False
    burnafterreading: burn the paste after it has been seen once - default False
    expire: paste expiration time, it can be 5min, 10min, 1hour, 1day, 1week, 1month - default 1day
    debug:" print response status code - default False
    return: the privatebin link
    """
    if formatter not in FORMATTER:
        raise KeyError(f"'formatter' should be one of: {', '.join(FORMATTER)}")
    if expire not in EXPIRE:
        raise KeyError(f"'expire' should be one of: {', '.join(EXPIRE)}")
    if opendiscussion and burnafterreading:
        raise KeyError("Cannot burn the paste after reading if this would be an opendiscussion: set only one option to True.")

    def monkey_post(self, request):
        result = self.session.post(
            url = self.server,
            headers = self.headers,
            proxies = self.proxy,
            auth=HTTPBasicAuth(username, password),
            data = request)
        try:
            return result.json()
        except ValueError:
            PBinCLIError("Unable parse response as json. Received (size = {}):\n{}".format(len(result.text), result.text))
    PrivateBin.post = monkey_post

    client = PrivateBin({
        'server': server,
        'proxy': None,
        'no_check_certificate': True,
        'no_insecure_warning': True
    })

    paste = Paste()
    version = 2
    paste.setVersion(version)
    #paste.setCompression('zlib')
    paste.setText(text or '')

    if attachment:
        paste.setAttachment(attachment)

    paste.setCompression('zlib')
    paste.setText(text)
    if paste_password:
        paste.setPassword(paste_password)
    if file:
        paste.setAttachment(file)
    paste.encrypt(
        formatter,
        burnafterreading and 1 or 0,
        opendiscussion and 1 or 0,
        expire
        )
    data = paste.getJSON()
    try:
        result = client.post(data)
    except Exception:
        raise
    finally:
        client.session.close()
    if debug:
        print(f"Request data:\t{data}")
        print(f"Response:\t{result}")
    if result['status']:
        raise RuntimeError("Something went wrong…\nError:\t\t{}".format(result['message']))
    passphrase = paste.getHash()
    if debug:
        print("Paste uploaded!\nPasteID:\t{}\nPassword:\t{}\nDelete token:\t{}\n\nLink:\t\t{}?{}#{}".format(
            result['id'],
            passphrase,
            result['deletetoken'],
            server,
            result['id'],
            passphrase))
    return f"{server}?{result['id']}#{passphrase}"
