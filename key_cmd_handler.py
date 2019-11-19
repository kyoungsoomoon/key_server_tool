from datetime import datetime
from key_common import *
import requests

def get_keys_handler(**args): 
    keyServerReq = args['baseURL']
    if args['last_updated']:
        keyServerReq += f"&ts={args['last_updated']}"
    print(keyServerReq)
    r = requests.get(url=keyServerReq)
    return r.text

def get_pkeys_handler(**args):
    keyServerReq = args['baseURL'] + f"&pub_id={args['pub_id']}"
    if args['last_updated']:
        keyServerReq += f"&ts={args['last_updated']}"
    print(keyServerReq)
    r = requests.get(url=keyServerReq)
    return r.text

def create_token_handler(**args):
    keyServerReq = args['baseURL'] + f"&role_id={args['role_id']}&secret_id={args['secret_id']}"
    print(keyServerReq)
    r = requests.get(url=keyServerReq)
    return r.text

def revoke_token_handler(**args):
    keyServerReq = args['baseURL'] + f"&token_revoke={args['token_revoke']}"
    print(keyServerReq)
    r = requests.get(url=keyServerReq)
    return r.text

def get_handler(**args):
    keyServerReq = args['baseURL']
    print(keyServerReq)
    r = requests.get(url=keyServerReq)
    return r.text

def get_pub_handler(**args):
    keyServerReq = args['baseURL'] + f"&pub_id={args['pub_id']}"
    print(keyServerReq)
    r = requests.get(url=keyServerReq)
    return r.text

def put_ckeys_handler(**args):
    keyServerReq = args['baseURL']
    print(keyServerReq)
    r = requests.post(url=keyServerReq, data = args['keys_to_upload'])
    return r.text

def put_pkeys_handler(**args):
    keyServerReq = args['baseURL'] + f"&pub_id={args['pub_id']}"
    print(keyServerReq)
    r = requests.post(url=keyServerReq, data = args['keys_to_upload'])
    return r.text

def delete_expired_keys_handler(**args):
    return None

def write_tv_token_handler(**args):
    r = requests.get(url=args['baseURL'])
    return r.text

cmd_handlers = { 
    GET_KEYS_CMD            : get_keys_handler,
    GET_PKEYS_CMD           : get_pkeys_handler,
    PUT_PKEYS_CMD           : put_pkeys_handler,
    CREATE_TOKEN_CMD        : create_token_handler,
    REVOKE_TOKEN_CMD        : revoke_token_handler,
    CREATE_PUB_CMD          : get_pub_handler,
    DELETE_PUB_CMD          : get_pub_handler,
    GET_CKEYS_CMD           : get_keys_handler,
    PUT_CKEYS_CMD           : put_ckeys_handler,
    DEL_EXPIRED_KEYS_CMD    : delete_expired_keys_handler,
    WRITE_TV_TOKEN_CMD      : write_tv_token_handler, 
}