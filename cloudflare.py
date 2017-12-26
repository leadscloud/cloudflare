import requests
import json
import datetime

'''
https://api.cloudflare.com/#
'''


class CloudFlare(object):
    def __init__(self, email, token):
        self.EMAIL = email
        self.TOKEN = token
        self.headers = {"X-Auth-Email": email, "X-Auth-Key": token, "Content-Type": "application/json"}
        self.s = requests.session()

    class APIError(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return self.value

    def api_call(self, method, endpoint, params=None):
        url = 'https://api.cloudflare.com/client/v4/' + endpoint
        method = method.lower()
        requests_method = getattr(self.s, method)
        response = requests_method(url, headers=self.headers, data=json.dumps(params) if params else None)
        data = response.text
        try:
            data = json.loads(data)
        except ValueError:
            raise self.APIError('JSON parse failed.')
        if data['result'] == 'error':
            raise self.APIError(data['msg'])
        return data

    def get(self, zone_id='', endpoint='', params=None):
        return self.api_call('GET', 'zones/' + zone_id + '/' + endpoint, params)

    def post(self, zone_id='', endpoint='', params=None):
        return self.api_call('POST', 'zones/' + zone_id + '/' + endpoint, params)

    def put(self, zone_id='', endpoint='', params=None):
        return self.api_call('PUT', 'zones/' + zone_id + '/' + endpoint, params)

    def delete(self, zone_id='', endpoint='', params=None):
        return self.api_call('DELETE', 'zones/' + zone_id + '/' + endpoint, params)

    def create_zones(self, z):
        data = {
            "name": z,
            "jump_start": False
        }
        return self.post(params=data)

    def delete_zones(self, zone_id):
        return self.delete(zone_id=zone_id)

    def list_zones(self):
        return self.get()

    def get_zone_by_name(self, z):
        data = self.list_zones()
        for item in data['result']:
            if z.strip() == item['name']:
                return item

    def get_zone_id(self, name):
        zone = self.get_zone_by_name(name)
        return zone['id']

    def rec_new(self, zone, _type, name, content, proxied=True, ttl=120):
        zone_id = self.get_zone_id(zone)
        data = {
            "type": _type,
            "name": name,
            "content": content,
            "proxiable": True,
            "proxied": proxied,
            "ttl": ttl
        }
        return self.post(zone_id, 'dns_records', data)

    def get_dns(self, z, name):
        # zone_id = self.get_zone_id(z)
        recs = self.rec_list(z)
        for dns in recs['result']:
            if dns['name'] == name if name == z else name + "." + z:
                return dns

    def rec_list(self, z):
        _id = self.get_zone_id(z)
        return self.get(_id, 'dns_records')

    def rec_detail(self, z, name):
        dns = self.get_dns(z, name)
        return self.get(dns['zone_id'], 'dns_records/' + dns['id'])

    def rec_delete(self, z):
        _id = self.get_zone_id(z)
        return self.delete(_id, 'dns_records/' + _id)

    def rec_edit(self, z, _type, name, content, proxied=True, ttl=120):
        dns = self.get_dns(z, name)
        data = {
            "id": dns['id'],
            "type": _type,
            "name": name,
            "content": content,
            "proxiable": True,
            "proxied": proxied,
            "ttl": ttl,
            "locked": False,
            "zone_id": dns['zone_id'],
            "zone_name": z
        }
        return self.put(dns['zone_id'], 'dns_records/' + dns['id'], data)


if __name__ == '__main__':
    domain = 'roadheadersforsale.com'
    ip = '45.55.11.23'
    cfapi = CloudFlare('brickell7342@lanthy.com', '71a97bbd95e40128e0fc139ccb')
    result = cfapi.create_zones(domain)
    result = cfapi.list_zones()
    # print(result)
    # result = cfapi.delete_zones('67426de7c48a62608479390faa')
    # print(result)
    result = cfapi.rec_new(domain, 'A', '@', ip)
    result = cfapi.rec_new(domain, 'A', 'www', ip)
    # result = cfapi.rec_edit('roadheadersforsale.org', 'A', 'en', '45.55.11.23')
    # result = cfapi.rec_list('grindingmill.org')
    print(result)
