import subprocess
import sys
import os
from datetime import datetime
import time

# Opcional: Colores en la terminal (pip install colorama)
try:
    from colorama import init, Fore, Style
    init()
    HAS_COLORS = True
except ImportError:
    HAS_COLORS = False

# Lista de scripts a ejecutar (rutas relativas o absolutas)
SCRIPTS = [
    "skic_tablas.py",
    "andrea_tablas.py",
    "edith_tablas.py",
    "federico_tablas.py",
    "fernando_tablas.py",
    "cdc_tablas.py"
]

LOG_FILE = "script_runner.log"

def log_message(message, level="INFO"):
    """Registra mensajes en consola y en el archivo LOG_FILE."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] {level}: {message}\n"
    
    # Escribe en el archivo de log
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry)
    
    # Colores en terminal (si está disponible)
    if HAS_COLORS:
        if level == "ERROR":
            print(Fore.RED + log_entry.strip())
        elif level == "SUCCESS":
            print(Fore.GREEN + log_entry.strip())
        else:
            print(Fore.CYAN + log_entry.strip())
        print(Style.RESET_ALL, end="")
    else:
        print(log_entry.strip())

def ejecutar_scripts():
    start_time_total = time.time()
    log_message(f"Iniciando procesamiento de archivos")
    log_message("=" * 60)
    
    for script in SCRIPTS:
        script_path = os.path.abspath(script)
        if not os.path.exists(script_path):
            log_message(f"El archivo {script} no existe", "ERROR")
            continue
        
        log_message(f"Ejecutando {script}...")
        start_time = time.time()
        
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8"
            )
            
            # Mostrar salida del script
            if result.stdout:
                log_message(f"Salida de {script}:\n{result.stdout}")
            if result.stderr:
                log_message(f"Advertencias en {script}:\n{result.stderr}", "WARNING")
            
            elapsed_time = time.time() - start_time
            log_message(f"{script} completado en {elapsed_time:.2f} segundos", "SUCCESS")
            
        except subprocess.CalledProcessError as e:
            log_message(f"Error en {script}: {e.stderr}", "ERROR")
        except Exception as e:
            log_message(f"Error inesperado en {script}: {str(e)}", "ERROR")
    
    total_time = time.time() - start_time_total
    log_message("=" * 60)
    log_message(f"Procesamiento completado en {total_time:.2f} segundos", "SUCCESS")

if __name__ == "__main__":
    ejecutar_scripts()