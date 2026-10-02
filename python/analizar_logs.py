import csv
from collections import Counter

# Ruta del archivo de registros
archivo_logs = "data/security_logs.csv"

# Leer los registros
eventos = []

with open(archivo_logs, mode="r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        eventos.append(fila)

# Contar intentos de login fallidos por usuario e IP
intentos_fallidos = Counter(
    (evento["user"], evento["source_ip"])
    for evento in eventos
    if evento["event_type"] == "LOGIN"
    and evento["status"] == "FAILED"
)

print("=== INTENTOS DE LOGIN FALLIDOS ===")

for (usuario, ip), cantidad in intentos_fallidos.items():
    print(f"{usuario} | IP: {ip} | {cantidad} intentos fallidos")

# Crear lista de alertas
alertas = []

for (usuario, ip), cantidad in intentos_fallidos.items():

    # Regla de detección del proyecto
    if cantidad >= 3:

        alerta = {
            "user": usuario,
            "source_ip": ip,
            "failed_attempts": cantidad,
            "alert_type": "MULTIPLE_FAILED_LOGINS"
        }

        alertas.append(alerta)

print("\n=== ALERTAS DE SEGURIDAD ===")

for alerta in alertas:
    print(
        f"ALERTA: {alerta['user']} | "
        f"IP: {alerta['source_ip']} | "
        f"Intentos fallidos: {alerta['failed_attempts']}"
    )

# Guardar las alertas en un archivo CSV
with open("data/alerts.csv", mode="w", newline="", encoding="utf-8") as archivo:

    campos = [
        "user",
        "source_ip",
        "failed_attempts",
        "alert_type"
    ]

    escritor = csv.DictWriter(archivo, fieldnames=campos)

    escritor.writeheader()
    escritor.writerows(alertas)

print("\nArchivo de alertas generado: data/alerts.csv")