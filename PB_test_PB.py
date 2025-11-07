from numpy import *
from matplotlib.pyplot import *
from pylab import *


# définition fonction de tranfert
wt=12e3 # fréquence ou pulsation de travail
H0=1 # gain statique
wc=5500# fréquence ou pulsation de coupure
we=1e6 # fréquence ou pulstion échantillonnage

# définition paramètres numériques
fcn=wc/we
fcnt=wt/we
wcn=2*pi*fcn
wcnt=2*pi*fcnt
kcn=1+wcn


# Définition de la fonction de filtrage
def Hn(wn, H0, wcn, kcn):
    return H0 * wcn / (kcn - np.cos(wn) - 1j * np.sin(wn))


# Générer un signal sinusoïdal
fs = 500  # Fréquence d'échantillonnage
t = np.linspace(0, 1, fs, endpoint=False)  # Vecteur temps
freq = 5  # Fréquence du signal sinusoïdal
x = np.sin(2 * np.pi * freq * t)  # Signal sinusoïdal

# Calculer la transformée de Fourier du signal
X = np.fft.fft(x)
frequencies = np.fft.fftfreq(len(x), 1/fs)

# Appliquer le filtre dans le domaine fréquentiel
H = Hn(frequencies, H0, wcn, kcn)
Y = X * H

# Revenir dans le domaine temporel en utilisant la transformée de Fourier inverse
y = np.fft.ifft(Y).real

# Affichage des signaux
plt.plot(t, x, label='Signal original')
plt.plot(t, y, label='Signal filtré', linestyle='--')
plt.xlabel('Temps [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.title('Signal Sinusoïdal avec Filtrage Passe-Bas')
plt.grid()
plt.show()
