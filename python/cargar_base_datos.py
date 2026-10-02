import csv
import sqlite3

# Rutas de los archivos
archivo_csv = "data/security_logs.csv"
archivo_db = "data/security.db"

# Conectar con la base de datos
conexion = sqlite3.connect(archivo_db)

# Crear un cursor para ejecutar instrucciones SQL
cursor = conexion.cursor()

# Eliminar la tabla anterior para evitar duplicar registros
cursor.execute("DROP TABLE IF EXISTS security_logs")

# Crear la tabla de eventos de seguridad
cursor.execute("""
    CREATE TABLE security_logs (
        timestamp TEXT,
        user TEXT,
        source_ip TEXT,
        event_type TEXT,
        status TEXT
    )
""")

# Leer el archivo CSV
with open(archivo_csv, mode="r", encoding="utf-8") as archivo:
    lector = csv.DictReader(archivo)

    for fila in lector:
        cursor.execute("""
            INSERT INTO security_logs
            (timestamp, user, source_ip, event_type, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            fila["timestamp"],
            fila["user"],
            fila["source_ip"],
            fila["event_type"],
            fila["status"]
        ))

# Guardar los cambios
conexion.commit()

# Cerrar la conexión
conexion.close()

print("Base de datos actualizada correctamente: data/security.db")