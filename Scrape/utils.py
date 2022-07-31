import os


def get_api_key(service_name):
    api_dir = r"C:\Users\SOUMEN\Resources\API"
    service_dir = os.path.join(api_dir, service_name)
    service_api_file = os.path.join(service_dir, "api_key.txt")
    with open(service_api_file, 'rb') as f:
        api_key = f.read().decode("utf-8")
    return api_key
