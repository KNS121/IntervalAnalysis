import struct
import numpy as np

filepath1 = "0.225_lvl_side_a_fast_data.bin"
filepath2 = "-0.205_lvl_side_a_fast_data.bin"


def read_files(filepath):


    try:

        with open(filepath, 'rb') as f:

            header = f.read(256)
            side, mode, count_frame = struct.unpack('<BBH', header[:4])


            point_dtype = np.dtype('<8H') # unsigned short
            frames = []

            for i in range(count_frame):
                # header of kadr
                frame_header = f.read(16)

                #check correct kadr
                if len(frame_header) < 16:
                    print("incorrect kadr")
                    break

                point_of_stop, timestamp = struct.unpack('<HL', frame_header[:6])

                frame_data = np.frombuffer(f.read(1024 * 16), dtype=point_dtype)

                frames.append(frame_data)

            frames = np.array(frames)
            Volt_array = frames / 16384.0 - 0.5

        return Volt_array

    except:
        return print("Incorrect file")



print(read_files(filepath1))