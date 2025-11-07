#Importation bibliothèques
from numpy import *
from matplotlib.pyplot import *
from pylab import *

# définition fonction de tranfert
wt=2.50e3 # fréquence ou pulsation de travail
H0=1 # gain statique
w0=5.19e3 # fréquence ou pulsation propre
Q=20 # facteur de qualité
we=1e5 # fréquence ou pulstion échantillonnage


# définition paramètres numériques
f0n=w0/we
f0nt=wt/we
w0n=2*pi*f0n
w0nt=2*pi*f0nt
k0n=w0n+Q*(w0n*w0n+1)

def H(w):
    return H0*(1j*w/w0*1/Q)/(1+(1j*w/w0*1/Q)+(1j*w/w0)**2)

def Hn(wn):
    return H0*w0n*(1-cos(wn)+1j*sin(wn))/((k0n-(2*Q+w0n)*cos(wn)+Q*cos(2*wn))+1j*((2*Q+w0n)*sin(wn)-Q*sin(2*wn)))

# coefficients du filtre numérique
a0=w0n/k0n
a1=-w0n/k0n
b1=(2*Q+w0n)/k0n
b2=-Q/k0n

#Découpage des puissances de 1  à 100000
puissance=arange(0,5,0.01)

#définition des pulsations
w=10**puissance
wn=2*pi*w/we



#définition du module en dB
module=20*log10(absolute(H(w)))
modulen=20*log10(absolute(Hn(wn)))
print("Filtre analogique:")
print()
print("fréquence centrale:")
print()
print(absolute(H(w0)))
gaincoup=20*log10(absolute(H(w0)))
print(gaincoup)
print()
print("fréquence de travail:")
print()
print(absolute(H(wt)))
gaint=20*log10(absolute(H(wt)))
print(gaint)
print()
print("Filtre numérique:")
print()
print("fréquence centrale:")
print()
print(absolute(Hn(w0n)))
gaincoup=20*log10(absolute(Hn(w0n)))
print(gaincoup)
print()
print("fréquence de travail:")
print()
print(absolute(Hn(w0nt)))
gaint=20*log10(absolute(Hn(w0nt)))
print(gaint)
print()
print("Les coefficients du filtre sont ")
print("a0=",a0)
print("a1=",a1)
print("b1=",b1)
print("b2=",b2)
print(k0n)

#tracé du diagramme de bode
subplot(211) # nb graphes : 2 colonne :1 ligne 1
semilogx(w,module)
grid(True)

subplot(211) # nb graphes : 2 colonne :1 ligne 2
semilogx(w,modulen)
grid(True)


show()







