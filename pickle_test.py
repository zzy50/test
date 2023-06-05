import pickle
import npy_append_array

PICKLE_PATH = "test.bin"

def generate_list():
    for i in range(0, 100, 4):
        yield [i, i+1, i+2, i+3] 


for list1 in generate_list():
    # print(list1)
    with open(PICKLE_PATH, "a+b") as abf:
        print(abf.tell())
        pickle.dump(list1, abf, pickle.HIGHEST_PROTOCOL)


with open(PICKLE_PATH, "rb") as rbf:
    loaded_list = pickle.load(rbf)
    print(loaded_list)

