import random
import os

if not os.path.exists("datos"):
    os.makedirs("datos")

sample_sizes = [10, 50, 100, 500, 1000, 5000, 10000] #, 50000, 100000, 300000, 500000, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000]

for size in sample_sizes:
    file_path = os.path.join("datos", f"input_{size}.txt")
    with open(file_path, "w") as f:
        for _ in range(size):
            f.write(f"{random.randint(1, 1000)}\n")
        
        # Segunda mitad: números aleatorios en orden decreciente
        decreciente = [random.randint(1, 1000) for _ in range(size)]
        decreciente.sort(reverse=True)
        for num in decreciente:
            f.write(f"{num}\n")

    print(f"Generated {file_path} with {size} samples.")
