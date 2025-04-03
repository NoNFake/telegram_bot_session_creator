from pyrobot import LOGGER, PROXY
import random as rnd

def get_proxies():
    try:

        with open(PROXY, 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
        return proxies
    except FileNotFoundError:
        LOGGER.error("Proxy file not found")
        return None
    

def get_random_proxy():
    proxies = get_proxies()
    if proxies:
        rnd_proxy = rnd.choice(proxies)

        if '@' in rnd_proxy:


            parts = rnd_proxy.split('@')
            auth_parts = parts[0].split(':')
            address_parts = parts[1].split(':')
            
            # Extract proxy details
            username = auth_parts[0]
            password = auth_parts[1]
            server = address_parts[0]
            port = int(address_parts[1])
        else:
            parts = rnd_proxy.split(':')
            server = parts[0]
            port = int(parts[1])
            username = parts[2]
            password = parts[3]

        return {
            'scheme': 'socks5',
            'hostname': server,
            'port': port,
            'username': username,
            'password': password
        }

    return None
