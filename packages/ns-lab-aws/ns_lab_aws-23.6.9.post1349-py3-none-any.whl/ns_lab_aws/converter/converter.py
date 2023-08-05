import math

def convert_bytes(size_bytes):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    index = int(math.floor(math.log(size_bytes, 1024)))
    size = round(size_bytes / (1024 ** index), 2)
    unit = units[index]
    return size, unit