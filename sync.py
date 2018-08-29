import sys
reload(sys)
sys.setdefaultencoding('utf8')
import yaml

from airwatch import AirWatchApi
from device42 import Device42Api

with open('config.yaml', 'r') as cfg:
    config = yaml.load(cfg.read())

device42 = config['device42']
airwatch = config['airwatch']
options = config['options']

airwatch_api = AirWatchApi(airwatch, options)
device42_api = Device42Api(device42, options)


class Integration:
    def __init__(self):
        self.computers = airwatch_api.get_list('devices')

    def get_computers(self):
        devices = []
        for computer in self.computers['Devices']:
            device = {}
            if computer['Id']:
                device.update({
                    'name': computer['DeviceFriendlyName'],
                    'new_name': computer['DeviceFriendlyName'],
                    'type': 'physical',
                    'serial_no': computer['SerialNumber'] if computer['SerialNumber'] else '',
                    'uuid': computer['Udid'] if computer['Udid'] else '',
                    'hardware': computer['Model'] if computer['Model'] else '',
                    'manufacturer': computer['Platform'] if computer['Platform'] else '',
                    'asset_no': computer['AssetNumber'] if computer['AssetNumber'] else ''                  
                })

                network = airwatch_api.get_item('devices', computer['Id']['Value'], 'network')
                software = airwatch_api.get_item('devices', computer['Id']['Value'], 'apps')['DeviceApps']


            if computer['Id']:
                devices.append({
                    'device': {k: v for (k, v) in device.items() if str(v) != str(-1)},
                    'computer': computer,
                    'software': software,
                    'network': network
                })

        return devices

    @staticmethod
    def get_device_network(device):
        macs = []
        ips = []
        
        if device['computer']['MacAddress']:
            macs.append({
                'macaddress': device['computer']['MacAddress'],
            })

        if 'IPAddress' in device['network']:
            if 'WifiIPAddress' in device['network']['IPAddress']:
                ips.append({
                    'ipaddress': device['network']['IPAddress']['WifiIPAddress'],
                })
                if 'WifiMacAddress' in device['network']['WifiInfo']:
                    macs.append({
                        'macaddress': device['network']['WifiInfo']['WifiMacAddress'],
                    })

            if 'EthernetIPAddress' in device['network']['IPAddress']:
                ips.append({
                    'ipaddress': device['network']['IPAddress']['EthernetIPAddress'],
                })

            if not options['no_cellular_ips']:
                if 'CellularIPAddress' in device['network']['IPAddress']:
                    ips.append({
                        'ipaddress': device['network']['IPAddress']['CellularIPAddress'],
                    })

        return macs, ips

    @staticmethod
    def get_device_software(applications):
        software = []
        for item in applications:
            software.append({
                'software': item['ApplicationName'],
                'version': item['Version'],
            })

        return software


def main():
    integration = Integration()

    devices = integration.get_computers()
    data = {
        'devices': []
    }
    for device in devices:
        macs, ips = integration.get_device_network(device)
        software = integration.get_device_software(device['software'])

        if options['no_ips']:
            ips = []

        data['devices'].append({
            'device': device['device'],
            'macs': macs,
            'ips': ips,
            'software': software
        })

    return data    


if __name__ == '__main__':
    elements = main()
    for element in elements['devices']:
        print device42_api.bulk(element)
    print '\n Finished'
