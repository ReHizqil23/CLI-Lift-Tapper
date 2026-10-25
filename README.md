# CLI-Lift-Tapper

# Smart Elevator Allocation - The Landmark Center

Sebuah simulasi berbasis Command Line Interface (CLI) untuk sistem alokasi lift pintar (Smart Elevator) pada gedung perkantoran 32 lantai. Program ini mengalokasikan penumpang ke 5 lift yang tersedia secara optimal berdasarkan jarak terdekat, arah perjalanan, dan batas kapasitas beban maksimal, serta dilengkapi dengan validasi hak akses (Role-Based Access Control).

## Tim Pengembang (Kelompok 10)
*   Anugrah Yusuf Rekimsa (26110300001)
*   Muhammad Hizqil Zakaria (26110300009)
*   Muhammad Ihdan Dinurachman (26110300029)

*Mata Kuliah: Programming Fundamental (Python)*

---

## Fitur Andalan
1. **Smart Dispatching System**: Memilih lift terbaik menggunakan rumus jarak mutlak (`abs()`), memprioritaskan lift yang searah, dan memastikan beban tidak melebihi 1200 kg.
2. **Deteksi Lantai Otomatis**: Sistem mengingat lantai terakhir penumpang turun berdasarkan riwayat.
3. **Mode Evakuasi Darurat**: Jika penumpang berada di lantai yang bukan hak aksesnya (misal: tersesat atau naik tangga), sistem menolak perjalanan normal namun memberikan opsi evakuasi langsung ke Lobi (Lantai 1).
4. **Mode Simulasi Otomatis (Menu 99)**: Fitur rahasia untuk men-generate penumpang acak dan menjalankan lift secara otomatis hingga semua penumpang tiba di tujuan, lalu menampilkan ringkasan perjalanan.
5. **Closed Menu UI**: Tampilan antarmuka terminal yang bersih dengan navigasi masuk-keluar menu (tombol `[0]` untuk kembali).

---

## Struktur Modul
Project ini dibangun dengan prinsip modularitas (dipisah per fungsi):
*   `main.py` : Main sequence. Mengatur alur menu utama menggunakan **Nested Loop**.
*   `database.py` : Menyimpan semua data statis (Data lift, kartu, riwayat) dan fungsi randomizer posisi lift.
*   `prioritas_lift.py` : Berisi rumus algoritma untuk menentukan lift mana yang paling efisien dipilih.
*   `validasi.py` : Mengurus semua validasi input, pencarian kartu, dan pengecekan hak akses lantai.
*   `fitur.py` : Berisi logic dari setiap menu (Tap Kartu, Jalankan Lift, Riwayat, Simulasi Otomatis).

---

## Penerapan Materi Programming Fundamental
1. **Percabangan (If-Else)**: Digunakan pada `validasi.py` untuk mengecek kecocokan kartu dan di `prioritas_lift.py` untuk menentukan prioritas lift.
2. **Looping (For)**: Digunakan untuk mengiterasi data list `database.riwayat` (mencari data) dan dictionary `database.lifts`.
3. **While Loop**: Digunakan untuk memaksa validasi input (di `validasi.py`) dan untuk pergerakan lift pada simulasi (di `fitur.py`).
4. **Nested Loop**: Diimplementasikan pada `main.py` (Loop luar untuk menu utama, Loop dalam untuk menu 1-5) agar program terus berjalan sampai user memilih keluar.

---

## Cara Menjalankan Program
Pastikan sudah menginstal **Python 3.x** di komputermu.

1. Buka terminal atau Command Prompt.
2. Masuk ke dalam direktori folder project.
3. Jalankan perintah berikut:

```bash
python main.py
