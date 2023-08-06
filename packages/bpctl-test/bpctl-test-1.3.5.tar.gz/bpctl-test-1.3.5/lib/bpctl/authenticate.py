from base import BaseBPCtl
from load_data import GetUserInformation


class UserAuthenticate(BaseBPCtl):
    def __init__(self, args):
        super(UserAuthenticate, self).__init__(args)

    def login(self):
        login_url = self.get_login_url()
        get_user_info = GetUserInformation()
        username, password = GetUserInformation().get_username_and_password()
        request_data = {'email': username, 'password': password}
        if self.args.debug:
            print(request_data)
        response = self.post_request(url=login_url, request_data=request_data, headers={})
        if response.status_code == 200:
            print('Login success')
            get_user_info.set_access_token(response.json()['access'])
        elif response.status_code == 401:
            print('Invalid Credentials')
        else:
            print('Login response code: '+str(response.status_code))
