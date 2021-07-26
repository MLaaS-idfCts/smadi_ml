import bluetooth as bt
import requests
import const

try:
    from bluetooth.ble import DiscoveryService
except ImportError:
    DiscoveryService = None


def bluetooth_classic_scan(timeout=10):
    """
    This scan finds ONLY Bluetooth classic (non-BLE) devices in *pairing mode*
    """
    return bt.discover_devices(duration=timeout, flush_cache=True, lookup_names=True)


def bluetooth_low_energy_scan(timeout=10):
    """
    currently Linux only
    """
    if DiscoveryService is None:
        return None

    svc = DiscoveryService()
    return svc.discover(timeout)


def scan(scansec=5) -> set:
    ret_list = set()
    dev_classic = bluetooth_classic_scan(scansec)
    if dev_classic:
        for d in dev_classic:
            ret_list.add(d)

    dev_ble = bluetooth_low_energy_scan(scansec)
    if dev_ble:
        for u, n in dev_ble.items():
            ret_list.add((u, n))
    return ret_list


def long_scan(timeout=300) -> list:
    ret_list = set()
    scan_long = timeout // (2 * 5)
    for i in range(scan_long):
        ret_list.update(scan())
    return list(ret_list)


def send_report1_request(mac: str, device_name: str) -> bool:
    requests.post(url=const.SERVER_ENDPOINT, data={
        'mac': mac,
        'device_name': device_name
    })


def bluetooth_loop():
    already_sent = set()
    while True:
        scan_results = long_scan()
        for mac, device_name in scan_results:
            if mac not in already_sent:
                is_sent = send_report1_request(mac, device_name)
                if is_sent:
                    already_sent.add(mac)


if __name__ == '__main__':
    bluetooth_loop()
