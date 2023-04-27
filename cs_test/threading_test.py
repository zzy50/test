import threading
from queue import Queue
from easydict import EasyDict
from time import sleep

image_q = Queue(2)
batches = [
    list(range(1, 31)),
    list(range(31, 61)),
    list(range(61, 91)),
    list(range(91, 121)),
    list(range(121, 151)),
    list(range(151, 181)),
    list(range(181, 211)),
    list(range(211, 241)),
    list(range(241, 271)),
    list(range(271, 301)),
    ]
args = EasyDict({
    "batches": batches,
    "preprocess": "preprocess",
    "inference": "inference"
    })

def image_preprocess(args: EasyDict, image_q: Queue):
    # print(args.preprocess)
    for batch in args.batches:
        image_q.put(batch)
        print(f"\n[PUT] batch {batch}")
        sleep(1)
    image_q.put("end")
    print(f"\n[PUT] batch end")

def inference(args: EasyDict, image_q: Queue):
    # print(args.inference)
    while True:
        batch = image_q.get()
        print(f"\n[GET] batch {batch}")
        if isinstance(batch, str):
            break
        for image in batch:
            str(image)
            print(f"image {image}")
            sleep(1)

print()
print()
print()

t1 = threading.Thread(target=image_preprocess, args=(args, image_q), daemon=True)
t2 = threading.Thread(target=inference, args=(args, image_q), daemon=True)

t1.start()
t2.start()
t1.join()
t2.join()