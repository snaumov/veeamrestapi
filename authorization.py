import requests
from configparser import ConfigParser


class Authorize:

    cfg = ConfigParser()
    cfg.read('config.ini')

    def __init__(self):
        self.bem_address = self.cfg['bem_settings']['address']
        self.username = self.cfg['bem_settings']['username']
        self.password = self.cfg['bem_settings']['password']

    class AuthorizeError(Exception):
        pass

    def get_authorize_token(self):
        try:
            r = requests.post(self.bem_address + '/api/sessionMngr/?v=latest', auth=(self.username, self.password))
            if r.status_code != 201:
                raise self.AuthorizeError('Authorization failed')
            return {'session_id': r.headers['X-RestSvcSessionId']}
        except self.AuthorizeError as e:
            print(e.args)
            return None

    def list_of_available_api(self):

        r = requests.get(self.bem_address + '/api/')
        return r.text



#debug

if __name__ == "__main__":
    new_auth = Authorize()
    print(new_auth.list_of_available_api())


