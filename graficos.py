import numpy as np
import os
import scipy as sp
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()

x = []
results = {}

try:
    with open("mediciones.txt", "r") as f:
        for line in f:
            if line.strip():
                size, time = line.strip().split(',')
                size = int(size)
                time = float(time)
                x.append(size)
                results[size] = time
except FileNotFoundError:
    print("El archivo 'mediciones.txt' no se encontró. Asegúrate de ejecutar el tp1.py con --medir primero.")
    exit(1)

x = np.array(x)
y_reales = np.array([results[n] for n in x])

f = lambda x, c1, c2: c1 * x * np.log(x) + c2
f2 = lambda x, c1, c2: c1 * x * x + c2

c, pcov = sp.optimize.curve_fit(f, x, y_reales)
c2, pcov2 = sp.optimize.curve_fit(f2, x, y_reales)

y_predichos = f(x, c[0], c[1])
y_predichos2 = f2(x, c2[0], c2[1])
r = np.abs(y_predichos - y_reales)
r2 = np.abs(y_predichos2 - y_reales)

plt.figure(figsize=(10, 6))

plt.scatter(x, y_reales, color='blue', label='Tiempos medidos', zorder=5)

x_smooth = np.linspace(min(x), max(x), 500)
y_smooth = f(x_smooth, c[0], c[1])
y_smooth2 = f2(x_smooth, c2[0], c2[1])

plt.plot(x_smooth, y_smooth, color='red', linestyle='--', label=rf'Ajuste O(n log n): ${c[0]:.2e} \cdot n \log(n) + {c[1]:.2e}$')
plt.plot(x_smooth, y_smooth2, color='blue', linestyle='--', label=rf'Ajuste O(n²): ${c[0]:.2e} \cdot n² + {c[1]:.2e}$')

plt.title('Complejidad del Algoritmo (Ajuste por Cuadrados Mínimos)')
plt.xlabel('Tamaño de entrada (N)')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.legend()
plt.grid(True)

os.makedirs("Informe/img", exist_ok=True)
plt.savefig("Informe/img/tiempos.png", dpi=300)

plt.figure(figsize=(10, 6))
plt.plot(x, r, color='red', linestyle='--', marker='o', label=rf'Error O(n log n)')
plt.plot(x, r2, color='blue', linestyle='--', marker='o', label=rf'Error O(n²)')

plt.title('Error del ajuste')
plt.xlabel('Tamaño de entrada (N)')
plt.ylabel('Diferencias')
plt.legend()
plt.grid(True)

os.makedirs("Informe/img", exist_ok=True)
plt.savefig("Informe/img/error.png", dpi=300)


plt.show() # Descomentar si se quiere ver en una ventana interactiva
