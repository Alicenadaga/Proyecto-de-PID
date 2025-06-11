from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Variables globales
carga_actual = 0
voltaje_actual = "0.0"
estacion_ocupada = False

# Crear la base de datos y las tablas si no existen
def crear_bd():
    conn = sqlite3.connect("cargas.db")
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            tarjeta TEXT PRIMARY KEY,
            nombre TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS cargas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tarjeta TEXT,
            nombre TEXT,
            fecha TEXT,
            en_proceso INTEGER DEFAULT 1
        )
    ''')

    conn.commit()
    conn.close()

def agregar_columna_si_no_existe():
    conn = sqlite3.connect("cargas.db")
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE cargas ADD COLUMN en_proceso INTEGER DEFAULT 1")
        conn.commit()
        print("✅ Columna 'en_proceso' agregada.")
    except sqlite3.OperationalError:
        print("⚠️ La columna 'en_proceso' ya existe.")
    conn.close()

crear_bd()
agregar_columna_si_no_existe()

@app.route("/", methods=["GET", "POST"])
def index():
    global estacion_ocupada
    nombre = None
    error = None
    tarjeta = None

    if request.method == "POST":
        tarjeta = request.form["tarjeta"]
        conn = sqlite3.connect("cargas.db")
        c = conn.cursor()
        c.execute("SELECT nombre FROM usuarios WHERE tarjeta = ?", (tarjeta,))
        fila = c.fetchone()

        if fila:
            if estacion_ocupada:
                error = "⚠️ Estación ocupada. Inténtalo más tarde."
            else:
                nombre = fila[0]
                c.execute("INSERT INTO cargas (tarjeta, nombre, fecha, en_proceso) VALUES (?, ?, ?, ?)",
                          (tarjeta, nombre, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))
                estacion_ocupada = True
                conn.commit()
        else:
            error = "Tarjeta no válida ❌"

        conn.close()

    return render_template("index.html", nombre=nombre, error=error, tarjeta=tarjeta)

@app.route("/registros")
def registros():
    conn = sqlite3.connect("cargas.db")
    c = conn.cursor()
    c.execute("SELECT tarjeta, nombre, fecha FROM cargas ORDER BY fecha DESC")
    filas = c.fetchall()
    conn.close()
    return render_template("registros.html", registros=filas)

@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    mensaje = None
    if request.method == "POST":
        tarjeta = request.form["tarjeta"]
        nombre = request.form["nombre"]

        conn = sqlite3.connect("cargas.db")
        c = conn.cursor()
        c.execute("SELECT * FROM usuarios WHERE tarjeta = ?", (tarjeta,))
        if c.fetchone():
            mensaje = "❌ Esa tarjeta ya está registrada."
        else:
            c.execute("INSERT INTO usuarios (tarjeta, nombre) VALUES (?, ?)", (tarjeta, nombre))
            conn.commit()
            mensaje = "✅ Usuario registrado correctamente."
        conn.close()

    return render_template("registrar.html", mensaje=mensaje)

@app.route("/registro-auto", methods=["POST"])
def registro_auto():
    tarjeta = request.form["tarjeta"]
    conn = sqlite3.connect("cargas.db")
    c = conn.cursor()
    nombre = "Usuario_" + tarjeta[-4:]

    c.execute("SELECT * FROM usuarios WHERE tarjeta = ?", (tarjeta,))
    if not c.fetchone():
        c.execute("INSERT INTO usuarios (tarjeta, nombre) VALUES (?, ?)", (tarjeta, nombre))
        conn.commit()
        print("Registrado:", tarjeta, nombre)
    else:
        print("Tarjeta ya registrada.")

    conn.close()
    return "", 204

@app.route("/actualizar-carga", methods=["POST"])
def actualizar_carga():
    global carga_actual
    carga = request.form.get("valor")
    if carga:
        carga_actual = int(carga)
    return "", 204

@app.route("/leer-carga")
def leer_carga():
    return str(carga_actual)

@app.route("/actualizar-voltaje", methods=["POST"])
def actualizar_voltaje():
    global voltaje_actual
    voltaje_actual = request.form["volt"]
    return "OK"

@app.route("/leer-voltaje")
def leer_voltaje():
    return voltaje_actual

@app.route("/estado-estacion")
def estado_estacion():
    return "ocupada" if estacion_ocupada else "disponible"

@app.route("/liberar-estacion")
def liberar_estacion():
    global estacion_ocupada, carga_actual, voltaje_actual
    estacion_ocupada = False
    carga_actual = 0
    voltaje_actual = "0.0"

    conn = sqlite3.connect("cargas.db")
    c = conn.cursor()
    c.execute("UPDATE cargas SET en_proceso = 0 WHERE en_proceso = 1")
    conn.commit()
    conn.close()
    return "", 204

@app.route("/historial/<tarjeta>")
def historial(tarjeta):
    conn = sqlite3.connect("cargas.db")
    c = conn.cursor()
    c.execute("SELECT nombre FROM usuarios WHERE tarjeta = ?", (tarjeta,))
    fila = c.fetchone()

    if not fila:
        return "Tarjeta no encontrada", 404

    nombre = fila[0]
    c.execute("SELECT fecha FROM cargas WHERE tarjeta = ? ORDER BY fecha DESC", (tarjeta,))
    cargas = c.fetchall()
    conn.close()

    return render_template("historial.html", nombre=nombre, tarjeta=tarjeta, cargas=cargas)

@app.route("/activas")
def activas():
    conn = sqlite3.connect("cargas.db")
    c = conn.cursor()
    c.execute("SELECT nombre, tarjeta, fecha FROM cargas WHERE en_proceso = 1")
    activas = c.fetchall()
    conn.close()
    return render_template("activas.html", activas=activas)

if __name__ == "__main__":
    app.run(debug=True)
