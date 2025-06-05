import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import windows
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class SignalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Symulacja Sygnałów")

        # Parametry domyślne
        self.signal_type = tk.StringVar(value="sin")
        self.amplitude = tk.DoubleVar(value=1.0)
        self.frequency = tk.DoubleVar(value=50.0)
        self.phase = tk.DoubleVar(value=0.0)
        self.duration = tk.DoubleVar(value=1.0)
        self.fs = tk.IntVar(value=1000)
        self.decay = tk.DoubleVar(value=5.0)  # tylko dla gasnącego

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        ttk.Label(frame, text="Typ sygnału:").grid(row=0, column=0)
        ttk.Combobox(frame, textvariable=self.signal_type, values=["sin", "gasnacy"]).grid(row=0, column=1)

        ttk.Label(frame, text="Amplituda:").grid(row=1, column=0)
        ttk.Entry(frame, textvariable=self.amplitude).grid(row=1, column=1)

        ttk.Label(frame, text="Częstotliwość (Hz):").grid(row=2, column=0)
        ttk.Entry(frame, textvariable=self.frequency).grid(row=2, column=1)

        ttk.Label(frame, text="Faza (φ, rad):").grid(row=3, column=0)
        ttk.Entry(frame, textvariable=self.phase).grid(row=3, column=1)

        ttk.Label(frame, text="Czas trwania (s):").grid(row=4, column=0)
        ttk.Entry(frame, textvariable=self.duration).grid(row=4, column=1)

        ttk.Label(frame, text="Fs (Hz):").grid(row=5, column=0)
        ttk.Entry(frame, textvariable=self.fs).grid(row=5, column=1)

        ttk.Label(frame, text="Wsp. zaniku (n):").grid(row=6, column=0)
        ttk.Entry(frame, textvariable=self.decay).grid(row=6, column=1)

        ttk.Button(frame, text="Generuj i pokaż", command=self.plot_signal).grid(row=7, columnspan=2, pady=10)

    def plot_signal(self):
        A = self.amplitude.get()
        f = self.frequency.get()
        phi = self.phase.get()
        T = self.duration.get()
        fs = self.fs.get()
        n = self.decay.get()

        t = np.linspace(0, T, int(fs*T), endpoint=False)

        if self.signal_type.get() == "sin":
            y = A * np.sin(2 * np.pi * f * t + phi)
        elif self.signal_type.get() == "gasnacy":
            y = A * np.sin(2 * np.pi * f * t + phi) * np.exp(-n * t)
        else:
            messagebox.showerror("Błąd", "Nieznany typ sygnału")
            return

        # Widmo
        Y = fft(y)
        freqs = fftfreq(len(t), 1/fs)
        mask = freqs >= 0

        # Wykresy
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        ax1.plot(t, y)
        ax1.set_title("Sygnał w dziedzinie czasu")
        ax1.set_xlabel("Czas [s]")
        ax1.set_ylabel("Amplituda")

        ax2.plot(freqs[mask], np.abs(Y[mask]))
        ax2.set_title("Widmo sygnału (FFT)")
        ax2.set_xlabel("Częstotliwość [Hz]")
        ax2.set_ylabel("|Y(f)|")

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalApp(root)
    root.mainloop()
