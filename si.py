import mplfinance as mpf
import matplotlib.pyplot as plt

# Crear un objeto que almacene la figura y los ejes
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

# Datos de ejemplo
data = mpf.sample_data.get_sample_data()

# Crear gráficos mplfinance y asignarlos a ejes específicos
mpf.plot(data[:50], type='candle', ax=axes[0, 0], title="Gráfico 1")
mpf.plot(data[50:100], type='candle', ax=axes[0, 1], title="Gráfico 2")
mpf.plot(data[100:150], type='candle', ax=axes[1, 0], title="Gráfico 3")
mpf.plot(data[150:200], type='candle', ax=axes[1, 1], title="Gráfico 4")

# Ajustar el espacio entre los gráficos
plt.tight_layout()

# Mostrar la figura
plt.show()



