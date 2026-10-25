"""
MODUL PRIORITAS LIFT
Berisi rumus untuk menentukan lift terbaik.
Inti rumusnya adalah jarak = abs(posisi_lift - lantai_asal),
lalu lift dipilih berdasarkan urutan prioritas:
  1. Lift yang sudah menuju lantai tujuan yang sama (pengelompokan)
  2. Lift diam yang paling dekat
  3. Lift searah yang paling dekat
  4. Kalau semua sibuk, lift yang paling dekat
Lift yang bebannya akan melebihi 1200 kg tidak ikut dipilih.
"""

import database


def hitung_jarak(posisi_lift, lantai_asal):
    """Rumus jarak lift ke penumpang memakai nilai mutlak.
    Contoh: abs(8 - 3) = 5 lantai, abs(1 - 3) = 2 lantai."""
    return abs(posisi_lift - lantai_asal)


def arah_lift(lift):
    """Menentukan arah lift: 'naik', 'turun', atau 'diam'."""
    if len(lift["tujuan"]) == 0:
        return "diam"
    elif lift["tujuan"][0] > lift["posisi"]:
        return "naik"
    else:
        return "turun"


def akan_lewat(lift, lantai):
    """Cek apakah lift sudah dijadwalkan berhenti di lantai tertentu."""
    return lift["posisi"] == lantai or lantai in lift["tujuan"]


def jadwalkan(lift, lantai_asal, lantai_tujuan):
    """Memasukkan lantai jemput dan lantai antar ke daftar tujuan lift.
    - Lantai yang sudah ada di jadwal tidak ditambah lagi (anti ghost call).
    - Lantai antar selalu dijadwalkan SETELAH lantai jemput, supaya
      penumpang benar-benar dijemput dulu baru diantar."""
    tujuan = lift["tujuan"]

    # 1. Lantai jemput
    if lift["posisi"] == lantai_asal:
        urutan_jemput = -1                  # lift sudah di sini, langsung naik
    elif lantai_asal in tujuan:
        urutan_jemput = tujuan.index(lantai_asal)
    else:
        tujuan.append(lantai_asal)
        urutan_jemput = len(tujuan) - 1

    # 2. Lantai antar, dicari hanya di jadwal sesudah lantai jemput
    if lantai_tujuan not in tujuan[urutan_jemput + 1:]:
        tujuan.append(lantai_tujuan)


def beban_lift(nama_lift):
    """Menjumlahkan berat semua penumpang yang sudah dialokasikan ke lift ini
    dan belum tiba (masih menunggu atau sudah di dalam lift)."""
    total = 0
    for p in database.riwayat:
        if p["lift"] == nama_lift and p["status"] != "sudah tiba":
            total = total + database.kartu[p["kartu"]]["berat"]
    return total


def masih_muat(nama_lift, berat):
    """True jika lift masih sanggup menampung penumpang dengan berat ini."""
    return beban_lift(nama_lift) + berat <= database.KAPASITAS_MAKS_KG


def lift_terdekat(daftar_nama, lantai_asal):
    """Dari daftar nama lift, cari yang jaraknya paling dekat ke lantai_asal."""
    terbaik = daftar_nama[0]
    jarak_terdekat = hitung_jarak(database.lifts[terbaik]["posisi"], lantai_asal)
    for nama in daftar_nama:
        jarak = hitung_jarak(database.lifts[nama]["posisi"], lantai_asal)
        if jarak < jarak_terdekat:
            terbaik = nama
            jarak_terdekat = jarak
    return terbaik, jarak_terdekat


def pilih_lift(lantai_asal, lantai_tujuan, berat):
    """Mengembalikan (nama_lift, alasan) untuk penumpang.
    Jika semua lift penuh, nama_lift bernilai None."""

    # Syarat kapasitas: hanya lift yang masih muat yang boleh dipilih
    lifts = {}
    for nama, lift in database.lifts.items():
        if masih_muat(nama, berat):
            lifts[nama] = lift
    if len(lifts) == 0:
        return None, f"semua lift penuh (maksimal {database.KAPASITAS_MAKS_KG} kg)"

    # Arah perjalanan penumpang
    if lantai_tujuan > lantai_asal:
        arah_penumpang = "naik"
    else:
        arah_penumpang = "turun"

    # PRIORITAS 1: lift yang sudah lewat lantai asal DAN menuju lantai
    # tujuan yang sama -> penumpang dikelompokkan, tidak menambah stop.
    for nama, lift in lifts.items():
        if akan_lewat(lift, lantai_asal) and lantai_tujuan in lift["tujuan"]:
            # Pastikan urutannya benar: jemput dulu di lantai asal,
            # baru kemudian ke lantai tujuan.
            if lift["posisi"] == lantai_asal:
                return nama, "lift ini sudah menuju lantai yang sama"
            elif lift["tujuan"].index(lantai_asal) < lift["tujuan"].index(lantai_tujuan):
                return nama, "lift ini sudah menuju lantai yang sama"

    # Kelompokkan lift berdasarkan kondisinya
    lift_diam = []
    lift_searah = []
    for nama, lift in lifts.items():
        arah = arah_lift(lift)
        if arah == "diam":
            lift_diam.append(nama)
        elif arah == "naik" and arah_penumpang == "naik" and lift["posisi"] <= lantai_asal:
            lift_searah.append(nama)
        elif arah == "turun" and arah_penumpang == "turun" and lift["posisi"] >= lantai_asal:
            lift_searah.append(nama)

    # PRIORITAS 2: lift yang sedang diam dan paling dekat.
    # Lift diam didahulukan agar tujuan yang berbeda tidak menumpuk
    # di satu lift (mencegah lift "menyapu lantai").
    if len(lift_diam) > 0:
        nama, jarak = lift_terdekat(lift_diam, lantai_asal)
        return nama, f"lift diam terdekat (jarak {jarak} lantai)"

    # PRIORITAS 3: lift yang searah dan paling dekat.
    if len(lift_searah) > 0:
        nama, jarak = lift_terdekat(lift_searah, lantai_asal)
        return nama, f"lift searah terdekat (jarak {jarak} lantai)"

    # PRIORITAS 4: semua lift sibuk berlawanan arah -> ambil yang terdekat.
    nama, jarak = lift_terdekat(list(lifts.keys()), lantai_asal)
    return nama, f"semua lift sibuk, dipilih yang terdekat (jarak {jarak} lantai)"
