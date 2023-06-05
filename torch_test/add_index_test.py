import torch

# x = torch.ones(5, 3)
# t = torch.tensor([[1, 2, 3],
#                   [4, 5, 6],
#                   [7, 8, 9]], 
#                   dtype=torch.float)
# index = torch.tensor([0, 4, 2])

# x.index_add_(dim=0, index=index, source=t)
# print("index_add_'s result:\n", x)
"""
before:
tensor([[  1.,   1.,   1.],
        [  1.,   1.,   1.],
        [  1.,   1.,   1.],
        [  1.,   1.,   1.],
        [  1.,   1.,   1.]])

after:   
tensor([[  2.,   3.,   4.],
        [  1.,   1.,   1.],
        [  8.,   9.,  10.],
        [  1.,   1.,   1.],
        [  5.,   6.,   7.]])
"""

x = torch.zeros(30, 7)
t = torch.range(1, 30).view(30, 1)

index = torch.tensor([6])
x.index_add_(dim=1, index=index, source=t)
print("index_add_'s result:\n", x)
