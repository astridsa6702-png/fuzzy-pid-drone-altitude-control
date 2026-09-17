# Simulasi Sistem Kendali Adaptif Fuzzy-PID pada Ketinggian Quadcopter

Projek ini dikembangkan sebagai bagian dari penelitian skripsi.

---

## Ringkasan Fitur & Skenario Simulasi
Sistem fuzzy merancang penyesuaian parameter PID ($K_p$, $K_i$, $K_d$) secara otomatis menggunakan variabel input *Rise Time*, *Overshoot*, dan *Settling Time*. Simulasi dilakukan dalam ruang 2D melalui 3 skenario pengujian:

1. **Variasi Periode Update Parameter:** Menguji rentang periode pembaharuan PID (100–3000).
2. **Variasi Parameter Awal PID:** Kombinasi parameter awal $K_p$, $T_i$, $T_d$ (nilai 1 dan 10).
3. **Variasi Gangguan Massa Drone:** Pengujian ketahanan/adaptivitas sistem terhadap perubahan massa drone ($0.8\text{ kg}$, $0.5\text{ kg}$, dan $1.2\text{ kg}$ dari massa awal $1.0\text{ kg}$).

---

## Fitur & Teknologi Utama
* **Bahasa:** Python
* **Software:** Visual Studio Code
* **Metode Utama:** Fuzzy Logic Control (Mamdani) + PID Auto-Tuning
* **Fokus Pengujian:** 2D Altitude Flight Dynamics & Robustness Test

---

## 🚀 Cara Menjalankan Simulasi
1. Buka file `Kendali Adaptif dengan Fuzzy_PID.py`.
2. *Copy* kodenya, lalu *paste* ke editor Python (VS Code / PyCharm / Jupyter).
3. Pastikan sudah install library `numpy`, `matplotlib`, dan `scikit-fuzzy`.
4. Jalankan (Run) filenya.
