import sys
from concurrent.futures import ThreadPoolExecutor
import os
from material_docente import util

class Entrenamientos:

    def __init__(self, e, s):
        self.e = e
        self.s = s

    @classmethod
    def from_file(cls, pathFile):
        with open(pathFile, 'r') as f:
            lines = f.readlines()
        
        n = len(lines) // 2
        e = [int(x) for x in lines[:n]]
        s = [int(x) for x in lines[n:]]
        return cls(e, s)
        
    def EntrenoODescanso(self):

        N = len(self.e)+1
        g = [[0] * N for _ in range(N)]
        k = 0 
        opt = [0]*N

        for i in range(1,N):
            for j in range(1,N):
                if i>j:
                    continue
                if j==i:
                    g[i][j] = self.e[i-1]
                else:
                    g[i][j] = g[i][j-1] + (self.e[j-1] if self.e[j-1]< self.s[j-i] else self.s[j-i])

        for i in range(1,N):
            opt_j = [0]*N
            mayor_opt = 0
            for j in range(0,N):

                if j == 0:
                    opt_j[j] = g[1][j]
                else:
                    opt_j[j] = opt[i-j+1] + g[i-j+1][i]

                if opt_j[j]>=mayor_opt:
                    mayor_opt = opt_j[j]
                    k = j

        for i in range(1,N):
            opt_k = [0]*N
            mayor_opt = 0
            for j in range(1,i+1):
        
                if j != i:
                    opt_k[j] = opt[i-j-2] + g[i-j][i]
                else:
                    opt_k[j]= g[1][j]

                if opt_k[j]>=mayor_opt:
                    mayor_opt = opt_k[j]
                    k = j
            opt[i] = opt_k[k]


        return self.reconstruccion(opt, k+1)

    def reconstruccion(self, opt, k):

        rec = []
        while len(rec)<len(opt)-1:
        
            dia = len(opt)-1 -k -1
            for i in range(0,k):
                rec.append('E')
            rec.append('D')
            k=dia

        rec = rec[::-1]
        del rec[0]
        return rec

def calcular_entrenamiento_descanso(e, s):
    entrenamientos = Entrenamientos(e, s)
    return entrenamientos.EntrenoODescanso()

def get_args_for_size(n):
    file_path = os.path.join("datos", f"input_{n}.txt")
    with open(file_path, 'r') as f:
        lines = f.readlines()
    e = [int(x) for x in lines[:n]]
    s = [int(x) for x in lines[n:]]
    return (e, s)

def run_measurement_for_n(n):
    print(f"[Hilo para N={n}] ==> Iniciando medición...")

    avg_times = util.time_algorithm(
        algorithm=calcular_entrenamiento_descanso,
        sizes=[n],
        get_args=get_args_for_size,
    )

    time = avg_times[n]
    print(f"[Hilo para N={n}] ==> Medición completada. Tiempo: {time:.6f}s")
    return (n, time)

if __name__ == "__main__":
    
    if len(sys.argv) > 1 and sys.argv[1] == '--medir':

        sizes_to_test = [10, 50, 100, 500, 1000, 5000, 10000] #, 50000, 100000, 300000, 500000, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000 ,7000000]#, 50000000]
        n_threads = 1

        print("Lanzando threads de mediciones...")
        with ThreadPoolExecutor(n_threads) as executor:
            results = executor.map(run_measurement_for_n, sizes_to_test)
            completed_tasks = list(results)
            print(f"Completado: {completed_tasks}")

        all_results = dict(completed_tasks)
        
        final_filename = "mediciones.txt"
        with open(final_filename, 'w') as f:
            for size in sorted(all_results.keys()):
                f.write(f"{size},{all_results[size]}\n")
        
        print(f"Mediciones guardadas en '{final_filename}'.")

    elif len(sys.argv) > 1:
        archivo_rivales = sys.argv[1]
        try:
            entrenamientos = Entrenamientos.from_file(archivo_rivales)
            entreno_descanso= entrenamientos.EntrenoODescanso()
            print(f"\nLas deciciones de los dias son: {entreno_descanso}")
        except FileNotFoundError:
            print(f"Error: El archivo '{archivo_rivales}' no fue encontrado.")
        except Exception as e:
            print(f"Ocurrió un error procesando el archivo: {e}")
    
    else:
        print("Modo de uso inválido.")
        print(f"  Para ejecutar con un archivo: python {sys.argv[0]} <ruta_al_archivo>")
        print(f"  Para correr las mediciones:   python {sys.argv[0]} --medir")
        sys.exit(1)
