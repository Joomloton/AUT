import yaml
from genie.testbed import load
from getpass import getpass

# Función para cargar el testbed
def load_testbed(testbed_path):
    with open(testbed_path, 'r') as stream:
        testbed_dict = yaml.safe_load(stream)
    testbed = load(testbed_dict)
    return testbed

# Función para seleccionar un dispositivo
def select_device(testbed):
    devices = list(testbed.devices.keys())
    for index, device in enumerate(devices, start=1):
        print(f"{index}. {device}")
    
    device = None
    while not device:
        try:
            choice = int(input("\nIngrese el número del dispositivo que desea administrar o '0' para salir: "))
            if choice == 0:
                return None
            device_name = devices[choice - 1]
            device = testbed.devices[device_name]
        except (ValueError, IndexError):
            print("Selección no válida. Por favor, ingrese un número de la lista.")
    
    return device

# Función para conectar al dispositivo
def connect_device(device):
    if not device.is_connected():
        try:
            # Conectar al dispositivo
            device.connect(learn_hostname=True, log_stdout=False)
            return True
        except Exception as e:
            print(f"Error al conectar al dispositivo: {e}")
            return False
    return True

# Función para ejecutar comandos en el dispositivo
def execute_command(device, command):
    try:
        output = device.execute(command)
        print(f"\nSalida del comando '{command}':\n{output}")
    except Exception as e:
        print(f"Error al ejecutar el comando: {e}")

# Función principal
def main():
    testbed_path = 'testbed.yaml'
    testbed = load_testbed(testbed_path)

    while True:
        print("\nDispositivos disponibles:")
        device = select_device(testbed)
        if not device:
            print("Terminando programa...")
            break
        
        if not connect_device(device):
            continue  # Intentar seleccionar y conectar a otro dispositivo
        
        # Menú de comandos
        commands = {
            '1': 'show ip interface brief',
            '2': 'show version',
            '3': 'show running-config',
            '4': 'show interfaces',
            '5': 'cambiar dispositivo',
            '6': 'salir'
        }
        
        while True:
            print("\nComandos disponibles:")
            for key, cmd in commands.items():
                print(f"{key}. {cmd}")
            
            cmd_choice = input("\nIngrese el número del comando que desea ejecutar: ")
            
            if cmd_choice == '6':
                print("Terminando sesión con el dispositivo...")
                break
            elif cmd_choice == '5':
                print("Cambiando dispositivo...")
                device.disconnect()
                break
            elif cmd_choice in commands:
                execute_command(device, commands[cmd_choice])
            else:
                print("Opción no válida, por favor intente de nuevo.")
        
        if cmd_choice == '6':
            break

    # Asegurarse de desconectar de todos los dispositivos al final
    for device in testbed.devices.values():
        if device.is_connected():
            device.disconnect()

# Ejecuta el programa principal
if __name__ == '__main__':
    main()
