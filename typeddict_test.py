from typing import TypedDict
import numpy as np
from numpy.typing import NDArray


class Batch(TypedDict):
    id: int
    name: str
    age: int
    coord: NDArray


batch = Batch()
batch["id"] = 123
batch["name"] = "James"
batch["age"] = 31
batch["coord"] = np.array([0, 0, 0])

print(batch)