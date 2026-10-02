import sqlite3

# Conectar con la base de datos
conexion = sqlite3.connect("data/security.db")

# Crear un cursor para ejecutar SQL
cursor = conexion.cursor()


# ============================================
# CONSULTA 1: Total de eventos
# ============================================

cursor.execute("""
    SELECT COUNT(*) AS total_eventos
    FROM security_logs;
""")

resultado = cursor.fetchone()

print("=== TOTAL DE EVENTOS ===")
print(f"Total de eventos: {resultado[0]}")


# ============================================
# CONSULTA 2: LOGIN exitosos y fallidos
# ============================================

cursor.execute("""
    SELECT status, COUNT(*) AS cantidad
    FROM security_logs
    WHERE event_type = 'LOGIN'
    GROUP BY status;
""")

resultados_login = cursor.fetchall()

print("\n=== RESULTADO DE LOGIN ===")

for status, cantidad in resultados_login:
    print(f"{status}: {cantidad}")


# ============================================
# CONSULTA 3: LOGIN fallidos por usuario e IP
# ============================================

cursor.execute("""
    SELECT user, source_ip, COUNT(*) AS intentos_fallidos
    FROM security_logs
    WHERE event_type = 'LOGIN'
    AND status = 'FAILED'
    GROUP BY user, source_ip
    ORDER BY intentos_fallidos DESC;
""")

resultados_fallidos = cursor.fetchall()

print("\n=== LOGIN FALLIDOS POR USUARIO E IP ===")

for usuario, ip, cantidad in resultados_fallidos:
    print(f"{usuario} | IP: {ip} | Fallos: {cantidad}")


# ============================================
# CONSULTA 4: Detectar IPs sospechosas
# ============================================

cursor.execute("""
    SELECT source_ip, COUNT(*) AS intentos_fallidos
    FROM security_logs
    WHERE event_type = 'LOGIN'
    AND status = 'FAILED'
    GROUP BY source_ip
    HAVING COUNT(*) >= 3
    ORDER BY intentos_fallidos DESC;
""")

ips_sospechosas = cursor.fetchall()

print("\n=== IPs CON MÚLTIPLES LOGIN FALLIDOS ===")

for ip, cantidad in ips_sospechosas:
    print(f"IP: {ip} | Intentos fallidos: {cantidad}")


# Cerrar la conexión
conexion.close()