import pandas as pd

columns = [
    'id', 'diagnosis',
    'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
    'compactness_mean', 'concavity_mean', 'concave_points_mean', 'symmetry_mean', 'fractal_dimension_mean',
    'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
    'compactness_se', 'concavity_se', 'concave_points_se', 'symmetry_se', 'fractal_dimension_se',
    'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst', 'smoothness_worst',
    'compactness_worst', 'concavity_worst', 'concave_points_worst', 'symmetry_worst', 'fractal_dimension_worst'
]

df = pd.read_csv("D:/Programacion/Optativa/wdbc.data", names=columns)


print(df.head())
# Quitamos la columna 'id'
df = df.drop('id', axis=1)

# Convertimos M y B a 1 y 0
df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})

# Separamos características y etiquetas
X = df.drop('diagnosis', axis=1)
y = df['diagnosis']

print(X.shape)  # muestra dimensiones de los datos
print(y.value_counts())  # cuántos benignos y malignos hay

from sklearn.model_selection import train_test_split

# Dividir los datos (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Tamaño entrenamiento:", X_train.shape)
print("Tamaño prueba:", X_test.shape)

from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# Crear el modelo (red con 2 capas ocultas)
model = MLPClassifier(hidden_layer_sizes=(30, 20, 10), max_iter=2000, random_state=42)

# Entrenar
model.fit(X_train, y_train)

# Predecir
y_pred = model.predict(X_test)

# Evaluar
accuracy = accuracy_score(y_test, y_pred)
print("Precisión del modelo:", accuracy)
from sklearn.metrics import classification_report, confusion_matrix

# Matriz de confusión
print("Matriz de confusión:")
print(confusion_matrix(y_test, y_pred))

# Reporte de clasificación (precisión, recall, F1)
print("\nReporte de clasificación:")
print(classification_report(y_test, y_pred))

# Ver ejemplos donde el modelo falló
import numpy as np

errores = np.where(y_pred != y_test)[0]
print(f"\nErrores encontrados: {len(errores)}")

# Mostrar algunos errores
for i in errores[:5]:  # solo los primeros 5 errores
    print(f"\nÍndice: {i}")
    print("Esperado:", y_test.iloc[i])
    print("Predicho:", y_pred[i])
    print("Datos:", X_test.iloc[i].values)

import numpy as np

# 👉 Reemplaza estos valores con los de tu nuevo paciente
nuevo_dato = np.array([
    14.0, 20.0, 90.0, 600.0, 0.1, 0.2, 0.15, 0.08, 0.2, 0.06,
    0.4, 1.2, 2.5, 30.0, 0.005, 0.02, 0.03, 0.01, 0.02, 0.004,
    16.0, 25.0, 110.0, 800.0, 0.13, 0.3, 0.4, 0.15, 0.3, 0.09
]).reshape(1, -1)

# 🧠 Predecir con el modelo
prediccion = model.predict(nuevo_dato)

# 🖨️ Mostrar resultado
if prediccion[0] == 1:
    print("\n👉 Resultado: Maligno")
else:
    print("\n👉 Resultado: Benigno")
