import numpy as np
import struct
import intvalpy as ip

def read_bin_files(filepath: str) -> np.ndarray:
    with open(filepath, 'rb') as f:
        header = f.read(256)
        side, mode, frame_count = struct.unpack('<BBH', header[:4])

        point_dtype = np.dtype('<8H')
        frames = []

        for i in range(frame_count):

            frame_header = f.read(16)
            if len(frame_header) < 16:
                break

            raw_data = f.read(1024 * 16)
            if len(raw_data) < 1024 * 16:
                break

            frame = np.frombuffer(raw_data, dtype=point_dtype)
            frames.append(frame)

    frames = np.array(frames)
    volts = frames / 16384.0 - 0.5

    return volts


def get_avg(data):
    avg = [[0] * 8] * 1024

    for i in range(len(data)):
        avg = np.add(avg, data[i])

    return np.divide(avg, len(data))

def scalar_to_interval(x, rad):
    return ip.Interval(x-rad, x+rad)