from config import *
from load_data import GetBPInformation, GetUserInformation
from sys import stderr
import requests
import os


class BaseBPCtl(object):
    def __init__(self, args):
        self.args = args

    def get_login_url(self):
        bp_host_url = GetBPInformation().bp_url()
        return bp_host_url + '/' + USER_LOGIN_URI

    def get_logout_url(self):
        bp_host_url = GetBPInformation().bp_url()
        return bp_host_url + '/' + USER_LOGOUT_URI

    def get_bp_manifest_url(self):
        bp_host_url = GetBPInformation().bp_url()
        return bp_host_url + '/' + BP_MANIFEST_APPLY_URI

    def get_request(self, url, headers=None):
        try:
            response = requests.get(url=url, headers=headers)
            if response.status_code in [200, 201]:
                if self.args.debug:
                    print(response.json())
            else:
                print(f'GET Request: {url} status code: ' + str(response.status_code), file=stderr)
        except Exception as e:
            print(f'GET Request: {url} : '+str(e), file=stderr)
            raise Exception(e)
        return response

    def post_request(self, url, request_data, headers=None):
        try:
            if headers is None:
                headers = self.get_user_headers()
            response = requests.post(url=url, headers=headers, data=request_data)
            if response.status_code in [200, 201]:
                if self.args.debug:
                    print(response.json())
            else:
                if self.args.debug:
                    print(f'POST Request: {url} status code: ' + str(response.status_code), file=stderr)
                    print(response.json())
        except Exception as e:
            print(f'POST Request: {url} : '+str(e), file=stderr)
            raise Exception(e)
        return response

    def get_user_headers(self):
        username, token = GetUserInformation().get_username_and_access_token()
        headers = {'Authorization': 'Bearer '+token, 'Content-Type': 'application/json'}
        return headers

    def validate_file(self, file_name):
        '''
        validate file name and path.
        '''
        if not self.valid_path(file_name):
            print(INVALID_PATH_MSG % (file_name))
            return False
        else:
            if not self.valid_filetype(file_name):
                print(INVALID_FILETYPE_MSG % (file_name))
                return False
        return True

    def valid_filetype(self, file_name):
        # validate file type
        flag = file_name.endswith(BP_YAML)
        if flag is False:
            flag = file_name.endswith(BP_YML)
        return flag

    def valid_path(self, path):
        # validate file path
        return os.path.exists(path)