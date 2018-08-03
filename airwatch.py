import requests
import json

class AirWatchApi:

    def __init__(self, config, options):
        self.auth = (config['username'], config['password'])
        self.host = config['host']
        self.debug = options['debug']
        self.headers = {
            'Content-Type': 'text/xml',
            'Accept': 'application/json',
            'aw-tenant-code': config['tenant_code']
        }
        self.lookup_limit = config['lookup_limit']

    def get_list(self, name):
        return requests.get('https://%s/api/mdm/%s/search?pagesize=%s' % (self.host, name, self.lookup_limit),
                            auth=self.auth, headers=self.headers).json()

    def get_item(self, name, pk, namespace):
        return requests.get('https://%s/api/mdm/%s/%s/%s?pagesize=%s' % (self.host, name, pk, namespace, self.lookup_limit),
                            auth=self.auth, headers=self.headers).json()
