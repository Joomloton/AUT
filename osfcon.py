from genie.testbed import load

# Cargar el testbed desde el archivo YAML
testbed = load('testbed.yaml')

# Función para configurar OSPF en un dispositivo
def configure_ospf(device, ospf_process_id, router_id, networks):
    device.configure([
        f"router ospf {ospf_process_id}",
        f"router-id {router_id}"
    ] + [
        f"network {network[0]} {network[1]} area {network[2]}" for network in networks
    ])

# Función para configurar las interfaces de un dispositivo
def configure_interfaces(device, interface_configs):
    for interface, ip_address, netmask in interface_configs:
        device.configure([
            f"interface {interface}",
            f"ip address {ip_address} {netmask}",
            "no shutdown"
        ])

# Datos para la configuración de OSPF
ospf_configs = {
    'RT-01': {
        'ospf_process_id': 1,
        'router_id': '1.1.1.1',
        'networks': [('172.16.10.0', '0.0.0.255', '0')],
        'interfaces': [('Se4/0', '172.16.10.1', '255.255.255.0')]
    },
    'RT-02': {
        'ospf_process_id': 1,
        'router_id': '2.2.2.2',
        'networks': [('172.16.10.0', '0.0.0.255', '0')],
        'interfaces': [('Se4/1', '172.16.10.2', '255.255.255.0')]
    }
}

# Ejecutar la configuración en cada dispositivo
for device_name, ospf_config in ospf_configs.items():
    # Conectar al dispositivo
    device = testbed.devices[device_name]
    device.connect(log_stdout=False)

    # Configurar las interfaces y OSPF
    configure_interfaces(device, ospf_config['interfaces'])
    configure_ospf(device, ospf_config['ospf_process_id'], ospf_config['router_id'], ospf_config['networks'])

    # Guardar la configuración y desconectar
    device.execute('write memory')
    device.disconnect()
