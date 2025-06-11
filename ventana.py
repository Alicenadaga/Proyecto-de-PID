import matplotlib.pyplot as plt

# Nombres de los bugs
bug_names = [
    "Inicio de sesión permite campos vacíos",
    "Registro de rutas duplicadas",
    "Botón 'Solicitar transporte' no responde",
    "Lista de usuarios no se actualiza"
]

# Número de veces que se evidenció cada bug (puedes ajustar según tu caso)
bug_counts = [5, 3, 4, 2]

# Crear gráfico de barras
plt.figure(figsize=(10, 6))
bars = plt.barh(bug_names, bug_counts, color='skyblue')
plt.xlabel("Cantidad de ocurrencias")
plt.title("Frecuencia de Bugs Detectados en Pruebas del Sistema")

# Mostrar los valores al lado de cada barra
for bar in bars:
    plt.text(bar.get_width() + 0.1, bar.get_y() + 0.25, str(bar.get_width()), va='center')

plt.tight_layout()
plt.gca().invert_yaxis()  # Para mostrar el bug más frecuente arriba
plt.show()
