from itertools import combinations, product

list_1 = ["A", "B", "C", "D", "E"]
list_2 = ["1", "2", "3", "4", "5"]

def itertools_combinations():
    result = list(combinations(list_1, 3))
    print(result)

def itertools_product():
    combs = list(product(list_1, list_2, repeat=2))
    print(len(combs))
    for comb in combs:
        print(comb)


# itertools_product()
itertools_combinations()