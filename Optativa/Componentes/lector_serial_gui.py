import tkinter as tk
from tkinter import messagebox
import serial
import threading
import requests

# Puerto COM que recibe datos desde SimulIDE (ajustado según com0com)
PUERTO_COM = "COM14"  # Asegúrate de que COM20 esté en SimulIDE

class LectorSerialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lector Serial para Motorinas")
        self.root.geometry("400x250")

        self.label_estado = tk.Label(root, text="Esperando datos...", font=("Arial", 12))
        self.label_estado.pack(pady=10)

        self.label_voltaje = tk.Label(root, text="", font=("Arial", 10))
        self.label_voltaje.pack(pady=5)

        self.boton_salir = tk.Button(root, text="Cerrar", command=root.quit, bg="red", fg="white")
        self.boton_salir.pack(pady=20)

        try:
            self.puerto = serial.Serial(PUERTO_COM, 9600, timeout=1)
            self.label_estado.config(text=f"Escuchando en {PUERTO_COM}", fg="green")
            threading.Thread(target=self.leer_serial, daemon=True).start()
        except serial.SerialException:
            self.label_estado.config(text=f"No se pudo abrir {PUERTO_COM}", fg="red")

    def leer_serial(self):
        while True:
            try:
                if self.puerto.in_waiting:
                    linea = self.puerto.readline().decode("utf-8").strip()
                    print("📥 Recibido desde COM:", linea)  # Verifica la entrada
                    self.root.after(0, self.procesar_dato, linea)
            except Exception as e:
                print("Error leyendo puerto:", e)

    def procesar_dato(self, linea):
        if linea.startswith("CARD:"):
            tarjeta = linea.replace("CARD:", "").strip()
            self.label_estado.config(text=f"🎴 Tarjeta: {tarjeta}")
            try:
                requests.post("http://127.0.0.1:5000/registro-auto", data={"tarjeta": tarjeta})
            except Exception as e:
                print("Error al registrar tarjeta:", e)

        elif linea.startswith("CARGA:"):
            valor = linea.replace("CARGA:", "").strip()
            self.label_estado.config(text=f"🔋 Carga: {valor}%")
            try:
                requests.post("http://127.0.0.1:5000/actualizar-carga", data={"valor": valor})
            except Exception as e:
                print("Error al enviar carga:", e)

        elif linea.startswith("VOLT:"):
            volt = linea.replace("VOLT:", "").strip()
            self.label_voltaje.config(text=f"🔌 Voltaje: {volt} V")
            try:
                requests.post("http://127.0.0.1:5000/actualizar-voltaje", data={"volt": volt})
            except Exception as e:
                print("Error al enviar voltaje:", e)

# Ejecutar app
if __name__ == "__main__":
    root = tk.Tk()
    app = LectorSerialApp(root)
    root.mainloop()
