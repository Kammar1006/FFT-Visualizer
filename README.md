# Symulacja Sygnałów z FFT

Aplikacja graficzna w języku Python służąca do generowania, sumowania i analizy sygnałów w dziedzinie czasu oraz częstotliwości (FFT).

## 📌 Opis

Projekt pozwala użytkownikowi na tworzenie i modyfikowanie różnych typów sygnałów:
- Sinusoidalnych (harmonicznych)
- Wygaszających (z zanikiem wykładniczym)
- Czirpów (sygnałów z liniowo zmieniającą się częstotliwością)

Użytkownik może regulować parametry każdego sygnału, takie jak:
- Amplituda
- Częstotliwość początkowa (i końcowa dla czirpów)
- Faza
- Czas trwania
- Czas rozpoczęcia
- Współczynnik zanikania (dla wygaszających)

Dodatkowo możliwa jest analiza FFT z możliwością wyboru typu okna (Brak, Hamming, Hann) oraz ustawienia częstotliwości próbkowania.

---

## 🖥️ Wymagania

- Python 3.8+
- Biblioteki:
  - `numpy`
  - `matplotlib`
  - `scipy`
  - `tkinter` (wbudowany w standardową bibliotekę Pythona)

## Instalacja:
``` 
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install numpy matplotlib scipy
```

## Uruchomienie:
```
python main.py
```

## 📷 Funkcjonalności
- Dodawanie wielu sygnałów

- Edycja parametrów sygnału przez GUI

- Włączanie / wyłączanie widoczności sygnału

- Sumowanie sygnałów i generowanie wykresu w czasie

- Obliczanie widma amplitudowego (FFT)

- Wybór okna: Brak / Hamming / Hann
