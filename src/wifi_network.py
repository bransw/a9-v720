import os
import subprocess
import argparse
import time

def print_list(name_of_list, list):
    print(name_of_list)
    for i, item in enumerate(list, start=1):
        print(f"{i}. {item}")

def get_os():
    if os.name == 'nt':
        return 'Windows'
    elif os.name == 'posix':
        return 'Linux'
    else:
        return 'Unknown'

def list_wifi_connections_windows(prefix):
    result = subprocess.run(['netsh', 'wlan', 'show', 'networks'], capture_output=True, text=True)
    networks = result.stdout.split('\n\n')
    wifi_list = []
    for network in networks:
        if 'SSID' in network:
            ssid = network.split('SSID')[1].split('\n')[0].strip()
            ssid = ssid.split(':')[1].strip() if ':' in ssid else ssid
            if ssid.startswith('Nax_'):
                wifi_list.append(ssid)
    return wifi_list

def list_wifi_connections_linux():
    result = subprocess.run(['nmcli', '-f', 'SSID', 'dev', 'wifi'], capture_output=True, text=True)
    networks = result.stdout.split('\n')
    wifi_list = [network.split(':')[1].strip() for network in networks if ':' in network]
    wifi_list = [ssid for ssid in wifi_list if ssid.startswith('Nax_')]
    return wifi_list

def list_wifi_connection(ssid_prefix):

    os_type = get_os()
    if os_type == 'Windows':
        wifi_list = list_wifi_connections_windows(ssid_prefix)
    elif os_type == 'Linux':
        wifi_list = list_wifi_connections_linux(ssid_prefix)
    else:
        print("Unsupported operating system.")
        return
    #print_list("Available WiFi networks:", wifi_list)
    return wifi_list


def wait_for_wifi_connection(ssid_prefix, timeout=120):
    """
    Ожидает, пока сеть Wi-Fi с заданным SSID не станет активной.

    :param ssid: SSID искомой сети Wi-Fi.
    :param timeout: Максимальное время ожидания в секундах.
    :return: True, если сеть подключена, иначе False.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        list_wifi = list_wifi_connection(ssid_prefix)
        if len(list_wifi)>0:
            print("*")
            return list_wifi[0]
        time.sleep(5) # Пауза перед следующей проверкой
        print("*", end="")
    return None

def select_and_connect(wifi_list):
    print("Available WiFi networks:")
    for i, ssid in enumerate(wifi_list, start=1):
        print(f"{i}. {ssid}")
    selection = int(input("Select a network by number: ")) - 1
    selected_ssid = wifi_list[selection]
    # Here you would add the code to connect to the selected network
    # This part is highly dependent on the OS and might require additional tools or commands
    return selected_ssid

def list_wifi_adapters_windows():
    result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True)
    interfaces = result.stdout.split('\n\n')
    adapter_list = []
    for interface in interfaces:
        if 'Name' in interface:
            name = interface.split('Name')[1].split('\n')[0].strip()
            name = name[2:]
            adapter_list.append(name)
    return adapter_list

def connect_to_wifi_windows(adapter, ssid, password):
    # This is a simplified example. Actual implementation might require additional steps.
    command = f'netsh wlan connect name="{ssid}" interface="{adapter}"'
    subprocess.run(command, shell=True)

def list_wifi_adapters_linux():
    result = subprocess.run(['nmcli', 'device', 'wifi'], capture_output=True, text=True)
    devices = result.stdout.split('\n')
    adapter_list = []
    for device in devices:
        if 'wifi' in device:
            adapter = device.split(':')[1].strip()

            adapter_list.append(adapter)
    return adapter_list

def connect_to_wifi_linux(adapter, ssid, password):
    # This is a simplified example. Actual implementation might require additional steps.
    command = f'nmcli device wifi connect {ssid} password {password} ifname {adapter}'
    subprocess.run(command, shell=True)

def connect_to_wifi(adapter, ssid, password):

    os_type = get_os()
    if os_type == 'Windows':
        connect_to_wifi_windows(adapter, ssid, password)
    elif os_type == 'Linux':
        connect_to_wifi_linux(adapter, ssid, password)
    else:
        print("Unsupported operating system.")

    return

def select_adapter():

    os_type = get_os()
    if os_type == 'Windows':
        adapters = list_wifi_adapters_windows()
    elif os_type == 'Linux':
        adapters = list_wifi_adapters_linux()
    else:
        print("Unsupported operating system.")
        return

    print("Available WiFi adapters:")
    for i, adapter in enumerate(adapters, start=1):
        print(f"{i}. {adapter}")

    adapter_selection = int(input("Select an adapter by number: ")) - 1
    return adapters[adapter_selection]

def main():

    adapter = select_adapter();
    print("Selected adapter =", adapter)

    ssid = wait_for_wifi_connection('Nax', 180)
    print("Found ssid =", ssid)
    password = ''

    connect_to_wifi(adapter, ssid, password)



if __name__ == "__main__":
    main()


