import numpy as np
from npy_append_array import NpyAppendArray

NUMPY_PATH = "test.npy"

def generate_array():
    for i in range(0, 1600, 16):
        arr = np.array(
            [
                [i, i+1, i+2, i+3],
                [i+4, i+5, i+6, i+7],
                [i+8, i+9, i+10, i+11],
                [i+12, i+13, i+14, i+15],
            ]
            )
        yield arr


init_numpy = True
for pred in generate_array():
    if init_numpy:
        np.save(NUMPY_PATH, pred)
        npaa = NpyAppendArray(NUMPY_PATH)
        init_numpy = False
    npaa.append(pred)


loaded_arr = np.load(NUMPY_PATH)
print(loaded_arr.shape)
print()