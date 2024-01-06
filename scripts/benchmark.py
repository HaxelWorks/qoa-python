import qoa
from time import perf_counter
import numpy as np
import os
SRC = r"C:\Users\axel1\Cache\fma_qoa"
FILES = os.listdir(SRC)
FILES = filter(lambda x: x.endswith(".qoa"), FILES)
FILES = map(lambda x: os.path.join(SRC, x), FILES)
FILES = list(FILES)


times = []
for i, file in enumerate(FILES):
    start = perf_counter()
    array = qoa.read(file)
    end = perf_counter()
    times.append(end - start)
    if i % 10 == 0:
        print(f"{i}/{len(FILES)}")

print(f"mean: {np.mean(times)}")
print(f"std: {np.std(times)}")
print(f"min: {np.min(times)}")
print(f"max: {np.max(times)}")

