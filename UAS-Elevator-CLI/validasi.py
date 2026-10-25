"""
MODUL VALIDASI
Berisi logika pemeriksaan dengan if-elif-else:
validasi input lantai, validasi kartu, dan validasi hak akses lantai.
"""

import database


def input_lantai(pesan):
    """Meminta input nomor lantai dan mengulang sampai inputnya valid."""
    while True:
        teks = input(pesan).strip()
        if not teks.isdigit():
            print("  [!] Masukkan angka saja.")
        elif int(teks) < database.LANTAI_TERENDAH or int(teks) > database.LANTAI_TERTINGGI:
            print(f"  [!] Lantai harus antara {database.LANTAI_TERENDAH} dan {database.LANTAI_TERTINGGI}.")
        else:
            return int(teks)


def cek_kartu(id_kartu):
    """Mengembalikan data kartu jika terdaftar, atau None jika tidak."""
    if id_kartu in database.kartu:
        return database.kartu[id_kartu]
    else:
        return None


def cek_sedang_perjalanan(id_kartu):
    """True jika kartu ini masih punya perjalanan yang belum selesai.
    Satu kartu tidak boleh memanggil lift dua kali sekaligus."""
    for p in database.riwayat:
        if p["kartu"] == id_kartu and p["status"] != "sudah tiba":
            return True
    return False


def cek_tujuan(data_kartu, lantai_asal, lantai_tujuan):
    """Memeriksa apakah perjalanan boleh dilakukan.
    Mengembalikan (True, "") jika boleh, atau (False, pesan) jika ditolak."""
    if lantai_asal == lantai_tujuan:
        return False, "[!] Anda sudah berada di lantai tersebut."
    elif lantai_tujuan not in data_kartu["izin"]:
        return False, f"[DITOLAK] Kartu tidak punya akses ke lantai {lantai_tujuan}."
    else:
        return True, ""
