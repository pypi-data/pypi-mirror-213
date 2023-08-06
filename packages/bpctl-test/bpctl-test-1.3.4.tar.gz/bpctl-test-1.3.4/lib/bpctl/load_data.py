from config import *
import os
import yaml
import base64


class BasicInformation:
    def __init__(self):
        self.bp_config_json = self.get_config_file_content()

    def get_config_file_content(self):
        if os.environ.get('BPCONFIG'):
            #TODO: needs to be review and validate
            bp_config_file_path_with_name = os.environ.get('BPCONFIG')
        else:
            bp_config_file_path_with_name = os.path.join(BP_CONFIG_PATH, BP_CONFIG_PATH_FILE_NAME)
        with open(bp_config_file_path_with_name, 'r') as file:
            file_content = file.read()
        return yaml.safe_load(file_content)

    def get_current_context_user(self):
        if 'current-context' in self.bp_config_json:
            username = self.bp_config_json['current-context'].split('@')[0]
        else:
            username = self.bp_config_json['users'][0]['name']
        return username

    def get_current_context_bp_name(self):
        if 'current-context' in self.bp_config_json:
            bp_name = self.bp_config_json['current-context'].split('@')[1]
        else:
            bp_name = self.bp_config_json['bps']['bp'][0]['name']
        return bp_name

    def store_updated_config_json(self):
        if os.environ.get('BPCONFIG'):
            #TODO: needs to be review and validate
            print("This feature coming soon")
            quit()
        else:
            bp_config_file_path_with_name = os.path.join(BP_CONFIG_PATH, BP_CONFIG_PATH_FILE_NAME)
        with open(bp_config_file_path_with_name, 'w') as file:
            yaml.dump(self.bp_config_json, file, allow_unicode=False)
        return True


class GetUserInformation(BasicInformation):
    def __init__(self):
        super(GetUserInformation, self).__init__()

    def get_username_and_password(self):
        bp_user = self.get_current_context_user()
        for user in self.bp_config_json['users']:
            if user['name'] == bp_user:
                return base64.b64decode(user['user']['username']).decode("utf-8"),\
                       base64.b64decode(user['user']['credential']).decode("utf-8")
        raise Exception('Invalid BP Config file')

    def get_username_and_access_token(self):
        bp_user = self.get_current_context_user()
        for user in self.bp_config_json['users']:
            if user['name'] == bp_user:
                return base64.b64decode(user['user']['username']).decode("utf-8"), \
                       base64.b64decode(user['user']['token']).decode("utf-8")
        raise Exception('Invalid BP Config file')

    def set_access_token(self, access_token):
        bp_user = self.get_current_context_user()
        for user in self.bp_config_json['users']:
            if user['name'] == bp_user:
                user['user']['token'] = base64.b64encode(access_token.encode('utf-8')).decode("utf-8")
                self.store_updated_config_json()
            else:
                raise Exception("User not in bp/config")


class GetBPInformation(BasicInformation):
    def __init__(self):
        super(GetBPInformation, self).__init__()

    def bp_url(self):
        bp_name = self.get_current_context_bp_name()
        for bp in self.bp_config_json['bps']:
            if bp['name'] == bp_name:
                return bp['bp']['server']
        raise Exception('Invalid BP Config file')
