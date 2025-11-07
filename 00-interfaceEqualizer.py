import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

# --- Fonctions de filtrage ---
def bandpass_filter(data, fs, lowcut, highcut, order=8):
    """Applique un filtre passe-bande Butterworth"""
    sos = butter(order, [lowcut / (fs/2), highcut / (fs/2)], btype='band', output='sos')
    return sosfilt(sos, data)

def lowpass_filter(data, fs, cutoff, order=8):
    sos = butter(order, cutoff / (fs/2), btype='low', output='sos')
    return sosfilt(sos, data)

def highpass_filter(data, fs, cutoff, order=8):
    sos = butter(order, cutoff / (fs/2), btype='high', output='sos')
    return sosfilt(sos, data)

# --- Fenêtre principale ---
root = tk.Tk()
root.title("Égaliseur audio 5 bandes (.wav)")
root.geometry("700x600")

fichier_wav = tk.StringVar(value="Aucun fichier sélectionné")

# --- Fonctions de callback ---
def update_value(index, value):
    value_labels[index].config(text=f"{int(float(value))}")

def ajouter_piece_jointe():
    fichier = filedialog.askopenfilename(
        title="Sélectionner un fichier audio",
        filetypes=[("Fichiers WAV", "*.wav")]
    )
    if fichier:
        fichier_wav.set(fichier)
        print(f"✅ Fichier sélectionné : {fichier}")
    else:
        messagebox.showinfo("Information", "Aucun fichier sélectionné.")

def traiter_audio():
    chemin = fichier_wav.get()
    if chemin == "Aucun fichier sélectionné":
        messagebox.showwarning("Attention", "Veuillez d'abord sélectionner un fichier .wav !")
        return

    try:
        # Lecture du fichier audio
        fs, data = wavfile.read(chemin)
        print(f"Chargé : {chemin} — {fs} Hz")

        # Normalisation si besoin
        if data.dtype != np.float32:
            data = data / np.max(np.abs(data))

        # Si stéréo → mono
        if len(data.shape) > 1:
            data = np.mean(data, axis=1)

        # Récupération des gains (de -20 à +20 dB)
        gains = [(slider.get() - 50) / 2.5 for slider in sliders]
        print("Gains (dB) par bande :", [round(g, 2) for g in gains])

        # Définition des bandes (en Hz)
        # Basses / Bas-médium / Médium (voix) / Haut-médium / Aigus
        bands = [
            ("Basses", "lowpass", (200,)),         # Bande 0 → Basses profondes
            ("Bas-Médium", "band", (200, 800)),    # Bande 1 → corps de la musique
            ("Voix", "band", (800, 4000)),         # Bande 2 → voix, clarté
            ("Haut-Médium", "band", (4000, 8000)), # Bande 3 → brillance
            ("Aigus", "highpass", (8000,))         # Bande 4 → sifflements, air
        ]

        sortie = np.zeros_like(data)

        # Application de chaque bande avec son gain
        for i, (name, ftype, freqs) in enumerate(bands):
            if ftype == "lowpass":
                filtered = lowpass_filter(data, fs, freqs[0])
            elif ftype == "highpass":
                filtered = highpass_filter(data, fs, freqs[0])
            else:
                filtered = bandpass_filter(data, fs, freqs[0], freqs[1])

            gain_factor = 10 ** (gains[i] / 20.0)
            sortie += filtered * gain_factor

            print(f"→ {name} : {gains[i]:+.1f} dB appliqué")

        # Normalisation finale
        sortie = sortie / np.max(np.abs(sortie))
        sortie = (sortie * 32767).astype(np.int16)

        # Sauvegarde
        output_path = os.path.join(os.path.dirname(chemin), "output.wav")
        wavfile.write(output_path, fs, sortie)

        messagebox.showinfo("Succès", f"✅ Fichier traité enregistré sous :\n{output_path}")
        print(f"✅ Fichier sauvegardé : {output_path}")

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")
        print(e)

# --- Interface graphique ---
sliders_frame = ttk.Frame(root)
sliders_frame.pack(pady=20)

sliders = []
value_labels = []

# Création des 5 sliders
for i in range(5):
    frame = ttk.Frame(sliders_frame)
    frame.pack(side="left", padx=10)

    label_bande = ttk.Label(frame, text=f"Bande {i}")
    label_bande.pack()

    slider = ttk.Scale(
        frame,
        from_=0,
        to=100,
        orient='vertical',
        length=300,
        command=lambda val, i=i: update_value(i, val)
    )
    slider.set(50)
    slider.pack()

    value_label = ttk.Label(frame, text="50")
    value_label.pack(pady=5)

    sliders.append(slider)
    value_labels.append(value_label)

# Boutons
btn_piece_jointe = ttk.Button(root, text="Ajouter un fichier .wav", command=ajouter_piece_jointe)
btn_piece_jointe.pack(pady=10)

btn_traiter = ttk.Button(root, text="Traiter le fichier .wav", command=traiter_audio)
btn_traiter.pack(pady=10)

label_fichier = ttk.Label(root, textvariable=fichier_wav, wraplength=550)
label_fichier.pack(pady=10)

root.mainloop()
