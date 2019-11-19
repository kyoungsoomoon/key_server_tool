import sys
import os
import requests
import bottle
import json
import key_cmd_handler as cmdh
from pathlib import Path
from key_common import *

app = bottle.Bottle()

keyServerURL = "ec2-3-229-122-80.compute-1.amazonaws.com"
REQUIRED_FIELDS = ('token', 'cmd')
cmdList= [GET_KEYS_CMD, GET_PKEYS_CMD, PUT_PKEYS_CMD, GET_CKEYS_CMD, PUT_CKEYS_CMD, CREATE_TOKEN_CMD, REVOKE_TOKEN_CMD, CREATE_PUB_CMD, DELETE_PUB_CMD, WRITE_TV_TOKEN_CMD]

def validate_request(token, cmd, pub_id, last_updated, role_id, secret_id, keys_to_upload):
    if not token or not cmd:
        return False

    if cmd == GET_PKEYS_CMD or cmd == PUT_PKEYS_CMD or cmd == CREATE_PUB_CMD or cmd == DELETE_PUB_CMD:
        if not pub_id:
            return False

    if cmd == CREATE_TOKEN_CMD:
        if not role_id or not secret_id:
            return False
        
    return True

def get_params_from_request(request, basic=False):
    try:
        if request.forms.get("token"):
            token       = request.forms.get("token")
        else:
            token       = request.query.token
        cmd             = request.forms.get("command_list")
        pub_id          = request.forms.get("pub_id")
        last_updated    = request.forms.get("last_updated")
        role_id         = request.forms.get("role_id")
        secret_id       = request.forms.get("secret_id")
        keys_to_upload  = request.forms.get("keys_to_upload")
        token_revoke    = request.forms.get("token_revoke")

        print(f"token={token}, cmd={cmd}, pub_id={pub_id}, ts={last_updated}, role_id={role_id}, secret_id={secret_id}, keys_to_upload={keys_to_upload}, token_revoke={token_revoke}")

        return token, cmd, pub_id, last_updated, role_id, secret_id, keys_to_upload, token_revoke
    except Exception as e:
        print('error parsing key request params: {}'.format(e))
    return None, None, None, None, None, None, None, None

@app.route('/admin', method='GET')
def admin_menu():
    token = bottle.request.query.token if bottle.request.query.token else None

    bottle.TEMPLATE_PATH.insert(0,os.path.dirname(Path(__file__)) + '/views/')
    
    return bottle.template('admin_menu', token=token, cmd=None, cmdList=cmdList, pub_id=None, last_updated=None, role_id=None, secret_id=None, keys_to_upload=None, token_revoke=None) 

@app.route('/admin/output', method='GET')
def admin_menu():
    token = bottle.request.query.token
    if not token:
        return bottle.HTTPError(status=401)

    with open("output.xml", "r") as f:
        output = f.read()
    bottle.response.set_header("Content-Type", "text/xml")

    return output

@app.route('/admin', method='POST')
def admin_cmd():
    token, cmd, pub_id, last_updated, role_id, secret_id, keys_to_upload, token_revoke = get_params_from_request(bottle.request)

    # validate the request
    if not validate_request(token, cmd, pub_id, last_updated, role_id, secret_id, keys_to_upload):
        return bottle.HTTPError(status=401)

    print("token={}, cmd={}, pub_id_{}".format(token, cmd, pub_id))

    baseURL = "http://" + keyServerURL + f"/key?token={token}&cmd={cmd}"
    res = cmdh.cmd_handlers[cmd](baseURL=baseURL, pub_id=pub_id, last_updated=last_updated, role_id=role_id, secret_id=secret_id, keys_to_upload=keys_to_upload, token_revoke=token_revoke)
    with open("output.xml", "w") as f:
        f.write(res)

    return bottle.template('admin_menu', token=token, cmd=cmd, cmdList=cmdList, pub_id=pub_id, last_updated=last_updated, role_id=role_id, secret_id=secret_id, keys_to_upload=keys_to_upload, token_revoke=token_revoke) 

def main():
    ec2DomainNameURL = "http://169.254.169.254/latest/meta-data/public-hostname"
    r = requests.get(url = ec2DomainNameURL)
    print(r.text)
    ec2DomainName = r.text
    app.run(host=r.text, port=80, debug=True)

if __name__ == '__main__':
    main()

