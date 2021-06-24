import random
from collections import Counter
items = [random.randint(0, 50) for i in range(7)]
a, b, c, d, e, f, g = map(int, input().split())
k = [a, b, c, d, e, f, g]

doubles = Counter(k)
print(doubles, Counter(k))
if max(k) > 50:
    print('Числа не должны превышать 50')
else:
    counter = 0
    for i in items:
        for j in k:
            if j == i:
                counter += 1
    print(counter)
    print(*items)
    print(*k)