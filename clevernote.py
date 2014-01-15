import sys
import json
import os.path
import urllib2

from evernote.api.client import EvernoteClient

CLEVERNOTE_CONSUMER_KEY = ''
CLEVERNOTE_CONSUMER_SECRET = ''
CLEVERNOTE_CALLBACK_URL = ''

CONFIG_FILENAME = os.path.expanduser('.cnrc')

config = None

def load_config():
    global config
    if config is None:
        if os.path.exists(CONFIG_FILENAME):
            try:
                config = json.load(open(CONFIG_FILENAME,'r'))
            except Exception as e:
                print("Problem loading config file %s: %s" % (CONFIG_FILENAME, e))
                sys.exit(1)
        else:
            config = {}
            save_config()


def save_config():
    global config
    json.dump(config, open(CONFIG_FILENAME,'w')
             , sort_keys=True
             , indent=4
             , separators=(',', ': ')
             )


def cmd_login(args):
    """login - Log in to Evernote; you'll be prompted for username and password"""

    load_config()
    if 'dev_token' in config:
        access_token = config['dev_token']
    elif 'access_token' in config:
        access_token = config['access_token']
    else:
        client = EvernoteClient(
            consumer_key=CLEVERNOTE_CONSUMER_KEY,
            consumer_secret=CLEVERNOTE_CONSUMER_SECRET,
            sandbox=True # Default: True
            )
        request_token = client.get_request_token(CLEVERNOTE_CALLBACK_URL)
        request_url = client.get_authorize_url(request_token)
        verifier_json = json.loads(urllib2.urlopen(request_url).read())
        access_token = client.get_access_token(
             request_token['oauth_token'],
             request_token['oauth_token_secret'],
             #request.GET.get('oauth_verifier', '')
             verifier_json['oauth_verifier']
             )
        client = EvernoteClient(token=access_token)
        config['access_token'] = access_token
    print("Logged in.")


def cmd_logout(args):
    """logout - Nuke your persistent Evernote credentials."""
    
    load_config()
    if 'access_token' in config:
        del config['access_token']
        save_config()
    print("Logged out.")


def get_client():
    load_config()
    if 'dev_token' in config:
        access_token = config['dev_token']
    elif 'access_token' in config:
        access_token = config['access_token']
    else:
        print("You need to log in first.")
        sys.exit(1)
    return EvernoteClient(token=access_token)


def cmd_notebooks(args):
    """notebooks - Show the list of existing notebooks"""

    client = get_client()
    noteStore = client.get_note_store()
    notebooks = noteStore.listNotebooks()

    print("Notebooks:")
    for n in notebooks:
        print(n.name)


def cmd_userinfo(args):
    """userinfo - Show your settings and information."""

    client = get_client()
    userStore = client.get_user_store()
    user = userStore.getUser()
    for field in [ 'name', 'username', 'email', 'timezone', 'privilege', 'active', 'created', 'updated', 'deleted', 'attributes' ]:
        value = str(getattr(user, field, ''))
        print("%s: %s" % (field.capitalize(), value))



def main():
    from cmdpy import CmdfileClient
    CmdfileClient(cmdmodule='clevernote').execute(sys.argv[1:])

