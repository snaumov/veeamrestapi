import requests
from authorization import Authorize
from bs4 import BeautifulSoup as bs
import time



class Restore:

    restore_authorize = Authorize()

    class RestoreError(Exception):
        pass

    def __init__(self):
        self.auth_token = self.restore_authorize.get_authorize_token()
        self.headers = {'X-RestSvcSessionId': self.auth_token['session_id'], 'Content-Type': 'application/xml'}




    def get_vmrestorepoints(self):
        try:
            r = requests.get(self.restore_authorize.bem_address + '/api/vmRestorePoints', headers=self.headers)
            if r.status_code not in (200, 201):
                raise self.RestoreError('incorrect_status_code', r.status_code)
            bs_xml = bs(r.text, 'lxml')

            links = bs_xml.find_all('link', rel="Alternate")

            restore_point_list_temp = []
            for link in links:
                name, date = link['name'].split('@')
                restore_point_list_temp.append({'href': link['href'].strip('?format=Entity'), 'name': name, 'date': date})

            #reformating a bit
            restore_point_list = {}
            for point in restore_point_list_temp:
                if point['name'] in restore_point_list.keys():
                    restore_point_list[point['name']][point['date']] = point['href']
                else:
                    restore_point_list[point['name']] = {point['date']: point['href']}

            return restore_point_list
        except self.RestoreError as e:
            print(e.args)
            return None

    def start_restore_task(self, href):
        try:
            r = requests.post(href + '?action=restore', headers=self.headers)
            if r.status_code not in (200, 201, 202):
                raise self.RestoreError('can\'t create restore task', r.status_code)

            print(bs(r.text, 'xml').Task['Href'])
            #checking if the previous request has been successful and the restore session has been created

            while True:
                r1 = requests.get(bs(r.text, 'xml').Task['Href'], headers=self.headers)
                print(r1.text)
                try:
                    if bs(r1.text, 'xml').Task.State.string == 'Sinished':
                        return bs(r1.text, 'xml').find('Link', Rel='Related')['Href']
                    else:
                        print(bs(r1.text, 'xml').Task.State.string)
                        time.sleep(10)
                        continue
                except Exception as e:
                    print(e.args)
                    return None


        except self.RestoreError as e:
            print(e.args)
            return None

    def get_restore_status(self, href):
        try:
            while True:
                r = requests.get(href, headers=self.headers)
                if r.status_code != 200:
                    raise self.RestoreError('can\'t get restore task status', r.status_code)
                if bs(r.text, 'xml').State.string == 'Stopped':
                    return bs(r.text, 'xml').Result.string
                else:
                    print(bs(r.text, 'xml').State.string)
                    time.sleep(10)
                    continue

        except self.RestoreError as e:
            print(e.args)
            return None

    def get_all_tasks(self):
        try:
            r = requests.get(self.restore_authorize.bem_address + '/api/tasks', headers=self.headers)
            return r.text
        except self.RestoreError as e:
            print(e.args)
            return None







#debug

if __name__ == "__main__":
    new_restore_session = Restore()
    print(new_restore_session.start_restore_task('http://172.17.13.22:9399/api/vmRestorePoints/a7930811-84d1-434a-9831-b592fac77aac'))
    while True:
        print(new_restore_session.get_all_tasks())
    





