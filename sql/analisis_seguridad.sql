-- ============================================
-- ANÁLISIS DE EVENTOS DE SEGURIDAD
-- ============================================


-- ============================================
-- 1. CANTIDAD TOTAL DE EVENTOS
-- ============================================

SELECT COUNT(*) AS total_eventos
FROM security_logs;


-- ============================================
-- 2. LOGIN EXITOSOS Y FALLIDOS
-- ============================================

SELECT status, COUNT(*) AS cantidad
FROM security_logs
WHERE event_type = 'LOGIN'
GROUP BY status;


-- ============================================
-- 3. LOGIN FALLIDOS POR USUARIO E IP
-- ============================================

SELECT user, source_ip, COUNT(*) AS intentos_fallidos
FROM security_logs
WHERE event_type = 'LOGIN'
AND status = 'FAILED'
GROUP BY user, source_ip
ORDER BY intentos_fallidos DESC;


-- ============================================
-- 4. TIPOS DE EVENTOS REGISTRADOS
-- ============================================

SELECT event_type, COUNT(*) AS cantidad
FROM security_logs
GROUP BY event_type
ORDER BY cantidad DESC;


-- ============================================
-- 5. IDENTIFICAR IPs CON MÚLTIPLES LOGIN FALLIDOS
-- ============================================

SELECT source_ip, COUNT(*) AS intentos_fallidos
FROM security_logs
WHERE event_type = 'LOGIN'
AND status = 'FAILED'
GROUP BY source_ip
HAVING COUNT(*) >= 3
ORDER BY intentos_fallidos DESC;


-- ============================================
-- 6. USUARIOS CON MÚLTIPLES LOGIN FALLIDOS
-- ============================================

SELECT user, COUNT(*) AS intentos_fallidos
FROM security_logs
WHERE event_type = 'LOGIN'
AND status = 'FAILED'
GROUP BY user
HAVING COUNT(*) >= 3
ORDER BY intentos_fallidos DESC;