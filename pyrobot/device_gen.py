import random as rnd


def generate_device():
    """
    generate_device()['device_model']
    generate_device()['system_version']
    generate_device()['app_version']
    
    """
    # Generate a random device

    prfix = ['Pro Max', 'Pro', '']
    device = {
        'device_model': f'iPhone {rnd.randint(11, 16)} {prfix[rnd.randint(0, 2)]}',
        'system_version': f'{rnd.randint(10, 15)}.{rnd.randint(0, 4)}.{rnd.randint(0, 9)}',
        'app_version': f'{rnd.randint(7, 9)}.{rnd.randint(4, 9)}.{rnd.randint(2, 5)}',
    }
    return device


# print(generate_device()['device_model'])