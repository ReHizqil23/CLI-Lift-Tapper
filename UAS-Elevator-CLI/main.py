"""
=====================================================================
 SIMULASI SMART ELEVATOR ALLOCATION (ALOKASI LIFT PINTAR)
 Studi Kasus : The Landmark Center, Jakarta
 Mata Kuliah : Programming Fundamental (Python)

 Kelompok 10:
   - Anugrah Yusuf Rekimsa     (26110300001)
   - Muhammad Hizqil Zakaria   (26110300009)
   - Muhammad Ihdan Dinurachman (26110300029)

 Cara menjalankan:  python main.py
=====================================================================
"""

import os
import fitur
import database

# ---------------------------------------------------------------
# UTILITAS
# ---------------------------------------------------------------

def bersihkan():
    os.system("cls" if os.name == "nt" else "clear")


def menu_utama():
    fitur.garis()
    print("   SMART ELEVATOR - THE LANDMARK CENTER")
    fitur.garis()
    print()
    print("  1. Tap kartu (panggil lift)")
    print("  2. Lihat status lift")
    print("  3. Jalankan lift (1 langkah)")
    print("  4. Lihat daftar kartu")
    print("  5. Lihat riwayat alokasi")
    print("  0. Keluar")
    print()


# ---------------------------------------------------------------
# MAIN SEQUENCE - NESTED LOOP
# ---------------------------------------------------------------

def main():
    database.acak_data()  # <--- Dipanggil di sini (acak ID, nama, lantai, dll)
    
    while True:                                  # ← LOOP LUAR
        bersihkan()
        menu_utama()
        pilihan = input("Pilih menu: ").strip()
        bersihkan()

        # ---------- MENU 1: TAP KARTU ----------
        if pilihan == "1":
            while True:                          # ← LOOP DALAM
                fitur.tap_kartu()
                print()
                print("  [0] Kembali ke menu utama")
                if input("Pilih: ").strip() == "0":
                    break                        # keluar loop dalam

        # ---------- MENU 2: STATUS LIFT ----------
        elif pilihan == "2":
            while True:
                bersihkan()
                fitur.tampilkan_status()
                print()
                print("  [0] Kembali ke menu utama")
                if input("Pilih: ").strip() == "0":
                    break

        # ---------- MENU 3: JALANKAN LIFT ----------
        elif pilihan == "3":
            while True:
                bersihkan()
                fitur.jalankan_lift()
                print()
                print("  [1] Langkah berikutnya")
                print("  [0] Kembali ke menu utama")
                sub = input("Pilih: ").strip()
                if sub == "0":
                    bersihkan()
                    break
                elif sub != "1":
                    print("  [!] Pilihan tidak tersedia.")
                    input("  Tekan Enter...")

        # ---------- MENU 4: DAFTAR KARTU ----------
        elif pilihan == "4":
            while True:
                bersihkan()
                fitur.tampilkan_kartu()
                print()
                print("  [0] Kembali ke menu utama")
                if input("Pilih: ").strip() == "0":
                    break

        # ---------- MENU 5: RIWAYAT ----------
        elif pilihan == "5":
            while True:
                bersihkan()
                fitur.tampilkan_riwayat()
                print()
                print("  [0] Kembali ke menu utama")
                if input("Pilih: ").strip() == "0":
                    break

        # ---------- KELUAR ----------
        elif pilihan == "0":
            print("Terima kasih telah menggunakan Smart Elevator!")
            break                                # keluar LOOP LUAR -> program selesai

        elif pilihan == "99":  # Menu rahasia
            fitur.simulasi_otomatis()
            input("\n  Tekan Enter untuk kembali ke menu utama...")

        else:
            print("  [!] Pilihan tidak tersedia.")
            input("  Tekan Enter untuk lanjut...")


if __name__ == "__main__":
    main()