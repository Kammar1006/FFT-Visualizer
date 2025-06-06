import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import get_window
import tkinter as tk
from tkinter import ttk, messagebox

class Signal:
    def __init__(self, type_="sin", amplitude=1.0, frequency=50.0, phase=0.0,
                 duration=1.0, decay=5.0, start_time=0.0, visible=True):
        self.type = type_
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
        self.duration = duration
        self.decay = decay
        self.start_time = start_time
        self.visible = visible

    def __str__(self):
        status = "✓" if self.visible else "✗"
        return f"{status} {self.type}, {self.frequency} Hz, {self.start_time}–{self.start_time + self.duration:.2f}s"

class SignalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Symulacja Sygnałów")
        self.root.geometry("1000x600")

        self.signals = []
        self.selected_index = None

        self.fs = tk.IntVar(value=1000)
        self.window_type = tk.StringVar(value="Brak")

        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Lewy panel: lista sygnałów + dodaj
        self.left_frame = ttk.Frame(main_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.signal_buttons_frame = ttk.Frame(self.left_frame)
        self.signal_buttons_frame.pack(fill=tk.Y)

        ttk.Button(self.left_frame, text="Dodaj sygnał (+)", command=self.add_signal).pack(pady=5)

        # Prawy panel: edytor + globalne + wykres
        self.right_frame = ttk.Frame(main_frame)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.editor_frame = ttk.LabelFrame(self.right_frame, text="Parametry sygnału")
        self.editor_frame.pack(fill=tk.X, pady=5)

        self.signal_type = tk.StringVar()
        self.amplitude = tk.DoubleVar()
        self.frequency = tk.DoubleVar()
        self.phase = tk.DoubleVar()
        self.duration = tk.DoubleVar()
        self.decay = tk.DoubleVar()
        self.start_time = tk.DoubleVar()

        self.param_vars = [self.signal_type, self.amplitude, self.frequency, self.phase,
                           self.duration, self.decay, self.start_time]

        self.param_widgets = []

        def add_param(label, var, widget_class, **kwargs):
            row = ttk.Frame(self.editor_frame)
            row.pack(fill=tk.X, pady=2)
            ttk.Label(row, text=label, width=20).pack(side=tk.LEFT)
            widget = widget_class(row, textvariable=var, **kwargs)
            widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.param_widgets.append(widget)

        add_param("Typ:", self.signal_type, ttk.Combobox, values=["sin", "gasnacy"])
        add_param("Amplituda:", self.amplitude, ttk.Entry)
        add_param("Częstotliwość (Hz):", self.frequency, ttk.Entry)
        add_param("Faza (rad):", self.phase, ttk.Entry)
        add_param("Czas trwania (s):", self.duration, ttk.Entry)
        add_param("Zanikanie (n):", self.decay, ttk.Entry)
        add_param("Start (s):", self.start_time, ttk.Entry)

        ttk.Button(self.editor_frame, text="Ukryj / Pokaż sygnał", command=self.toggle_visibility).pack(pady=2)
        ttk.Button(self.editor_frame, text="Usuń sygnał", command=self.remove_signal).pack(pady=2)
        ttk.Button(self.editor_frame, text="Zapisz sygnał", command=self.save_signal).pack(pady=2)

        # Ustawienia globalne
        global_frame = ttk.LabelFrame(self.right_frame, text="Ustawienia globalne")
        global_frame.pack(fill=tk.X, pady=5)

        self.create_labeled_entry(global_frame, "Fs (Hz):", ttk.Entry, self.fs)
        self.create_labeled_entry(global_frame, "Okno FFT:", ttk.Combobox, self.window_type, {"values": ["Brak", "Hamming", "Hann"]})

        ttk.Button(self.right_frame, text="Generuj Wykres", command=self.generate_plot).pack(pady=10)

        self.editor_frame.pack_forget()  # startowo ukryty

    def create_labeled_entry(self, parent, label, widget_class, variable, widget_options=None):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        ttk.Label(frame, text=label, width=20).pack(side=tk.LEFT)
        options = widget_options if widget_options else {}
        widget = widget_class(frame, textvariable=variable, **options)
        widget.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def add_signal(self):
        sig = Signal()
        self.signals.append(sig)
        self.refresh_signal_buttons()
        self.select_signal(len(self.signals) - 1)

    def refresh_signal_buttons(self):
        for widget in self.signal_buttons_frame.winfo_children():
            widget.destroy()
        for i, sig in enumerate(self.signals):
            btn = ttk.Button(self.signal_buttons_frame, text=str(sig),
                             command=lambda idx=i: self.select_signal(idx))
            btn.pack(fill=tk.X, pady=1)

    def select_signal(self, index):
        self.selected_index = index
        self.load_signal_into_form(index)
        self.editor_frame.pack(fill=tk.X, pady=5)

    def load_signal_into_form(self, index):
        sig = self.signals[index]
        self.signal_type.set(sig.type)
        self.amplitude.set(sig.amplitude)
        self.frequency.set(sig.frequency)
        self.phase.set(sig.phase)
        self.duration.set(sig.duration)
        self.decay.set(sig.decay)
        self.start_time.set(sig.start_time)

    def save_signal(self):
        if self.selected_index is None:
            return
        try:
            sig = self.signals[self.selected_index]
            sig.type = self.signal_type.get()
            sig.amplitude = self.amplitude.get()
            sig.frequency = self.frequency.get()
            sig.phase = self.phase.get()
            sig.duration = self.duration.get()
            sig.decay = self.decay.get()
            sig.start_time = self.start_time.get()
            self.refresh_signal_buttons()
        except tk.TclError:
            messagebox.showerror("Błąd", "Nieprawidłowe dane.")

    def remove_signal(self):
        if self.selected_index is not None:
            del self.signals[self.selected_index]
            self.selected_index = None
            self.refresh_signal_buttons()
            self.editor_frame.pack_forget()

    def toggle_visibility(self):
        if self.selected_index is not None:
            self.signals[self.selected_index].visible ^= True
            self.refresh_signal_buttons()

    def generate_plot(self):
        fs = self.fs.get()
        signals = [s for s in self.signals if s.visible]
        if not signals:
            messagebox.showwarning("Brak danych", "Brak aktywnych sygnałów do pokazania.")
            return

        max_time = max(s.start_time + s.duration for s in signals)
        t = np.linspace(0, max_time, int(fs * max_time), endpoint=False)
        y_total = np.zeros_like(t)

        for s in signals:
            t_local = np.linspace(0, s.duration, int(fs * s.duration), endpoint=False)
            y = s.amplitude * np.sin(2 * np.pi * s.frequency * t_local + s.phase)
            if s.type == "gasnacy":
                y *= np.exp(-s.decay * t_local)

            start_idx = int(s.start_time * fs)
            end_idx = start_idx + len(y)
            if end_idx > len(y_total):
                continue  # zbyt długi sygnał – pomijamy
            y_total[start_idx:end_idx] += y

        # Okno
        win_type = self.window_type.get().lower()
        win = get_window(win_type, len(y_total)) if win_type != "brak" else np.ones(len(y_total))
        Y = fft(y_total * win)
        freqs = fftfreq(len(t), 1 / fs)
        mask = freqs >= 0

        # Wykres
        self.editor_frame.pack_forget()
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        ax1.plot(t, y_total)
        ax1.set_title("Sygnał w dziedzinie czasu")
        ax2.plot(freqs[mask], np.abs(Y[mask]))
        ax2.set_title("Widmo sygnału")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = SignalApp(root)
    root.mainloop()
