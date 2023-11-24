import yaml
from getpass import getpass

# Función para agregar dispositivos
def add_device():
    device = {}
    device['name'] = input('Enter the device name: ')
    device['os'] = input('Enter the device OS (e.g., ios, nxos): ')
    device['type'] = input('Enter the device type (e.g., router, switch): ')
    device['ip'] = input('Enter the management IP: ')
    device['protocol'] = input('Enter the protocol for connection (ssh/telnet): ')
    if device['protocol'] == 'ssh':
        device['username'] = input('Enter the username: ')
        device['password'] = getpass('Enter the password: ')
    return device

# Solicita al usuario el número de dispositivos
num_devices = int(input('How many devices do you want to add to the testbed? '))

# Crea una lista vacía para almacenar la información de los dispositivos
devices_list = []

# Agrega dispositivos a la lista
for _ in range(num_devices):
    devices_list.append(add_device())

# Estructura del testbed
testbed = {
    'testbed': {
        'name': 'MyTestbed',
        'credentials': {
            'default': {
                'username': '',
                'password': ''
            }
        }
    },
    'devices': {}
}

# Llenar el testbed con los dispositivos
for device in devices_list:
    testbed['devices'][device['name']] = {
        'os': device['os'],
        'type': device['type'],
        'connections': {
            'cli': {
                'protocol': device['protocol'],
                'ip': device['ip']
            }
        }
    }
    if device['protocol'] == 'ssh':
        testbed['devices'][device['name']]['credentials'] = {
            'username': device['username'],
            'password': device['password']
        }

# Guardar el testbed en un archivo YAML
with open('testbed.yaml', 'w') as file:
    yaml.dump(testbed, file, sort_keys=False)

print('testbed.yaml has been created successfully.')
