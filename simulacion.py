from numpy import *
from matplotlib.pyplot import *

# linspace(tiempo_inicial, tiempo_final, numero_muestras)
t = linspace(0, 10, 100)
x = sin(2*pi * 4 * t)

r = (random.rand(100) - 0.5)* 2 * 0.1
px = sum(x**2)/ length(x)
rx = sum(r**2) / length(x)

snl = px/rx
sn = 10 * log(px/rx)

c = 10e6 * log2(1 + snl)

plot(t,x)

