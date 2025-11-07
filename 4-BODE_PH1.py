#Importation bibliothèques
from numpy import *
from matplotlib.pyplot import *
from pylab import *

# définition fonction de tranfert
wt=12.1e3 # fréquence ou pulsation de travail
H0=1 # gain statique
wc=5000 # fréquence ou pulsation de coupure
we=1e5 # fréquence ou pulstion échantillonnage

# définition paramètres numériques
fcn=wc/we
fcnt=wt/we
wcn=2*pi*fcn
wcnt=2*pi*fcnt
kcn=1+wcn


def H(w):
    return H0*(w/wc)/(1+1j*w/wc)

def Hn(wn):
    return H0*(1-cos(wn)+1j*sin(wn))/(kcn-cos(wn)-1j*sin(wn))

# coefficients du filtre numérique
a0=1/(1+wcn)
a1=-1/(1+wcn)
b1=1/(1+wcn)

#Découpage des puissances de 1  à 100000
puissance=arange(0,6,0.01)

#définition des pulsations
w=10**puissance
wn=2*pi*w/we



#définition du module en dB
module=20*log10(absolute(H(w)))
modulen=20*log10(absolute(Hn(wn)))
print("Filtre analogique:")
print()
print("fréquence de coupure:")
print()
print(absolute(H(wc)))
gaincoup=20*log10(absolute(H(wc)))
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
print("fréquence de coupure:")
print()
print(absolute(Hn(wcn)))
gaincoup=20*log10(absolute(Hn(wcn)))
print(gaincoup)
print()
print("fréquence de travail:")
print()
print(absolute(Hn(wcnt)))
gaint=20*log10(absolute(Hn(wcnt)))
print(gaint)
print()
print("Les coefficients du filtre sont ")
print("a0=",a0)
print("a1=",a1)
print("b1=",b1)

#tracé du diagramme de bode
subplot(211) # nb graphes : 2 colonne :1 ligne 1
semilogx(w,module)
grid(True)

subplot(211) # nb graphes : 2 colonne :1 ligne 2
semilogx(w,modulen)
grid(True)


show()







