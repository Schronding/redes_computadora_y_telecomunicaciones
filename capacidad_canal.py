from numpy import *
from matplotlib.pyplot import *

# 1. Generación de la señal
t = linspace(0, 1, 100)
x = sin(2*pi*4*t)

# Simulación de ruido
r = (random.rand(100)-0.5)*2*0.1

# Cálculos de potencia
px = sum(x**2)/100
pr = sum(r**2)/100

# Cálculos de SNR
sn = 10*log(px/pr)
snl = px/pr

# Capacidad teórica (ejemplo base)
c = 10e6 * log2(1+snl)

# Configurar la figura
figure(figsize=(10, 6)) 
plot(t, x, label='Señal Senoidal')
title('Simulación de Señal para Análisis de Capacidad')
xlabel('Tiempo (s)')
ylabel('Amplitud (V)')
grid(True) 
legend()

savefig("grafica_senial_senoidal.png") 
print("Gráfica guardada como 'grafica_senial_senoidal.png'")

show() 

#%% Ethernet capacidad de un canal de comunicación

snr1 = (10**(25))/10
snr2 = (10**(35))/10

cat3 = 16e6 * log2(1+snr1)
cat5 = 100e6 * log2(1+snr1)
cat5e6 = 250e6 * log2(1+snr1)
cat6a = 500e6 * log2(1+snr2)
cat8 = 1e9 * log2(1+snr2)

print(f"Capacidad Cat6a: {cat6a/1e6:.2f} Mbps") # Print para verificar que corre

#%% Wifi capacidad de un canal de comunicación

snr = (10**20)/10

wifin = 40e6 * log2(1+snr)
wifiac = 160e6 * log2(1+snr)