"""
MODUL FITUR
Berisi fungsi-fungsi untuk setiap menu CLI (menu 1 sampai 5).
Setiap fitur memanggil modul database, prioritas_lift, dan validasi.
"""

import database
import prioritas_lift
import validasi
import random


def garis():
    print("=" * 60)


def tap_kartu():
    """Menu 1: penumpang men-tap kartu dan memilih lantai tujuan."""
    garis()
    print("TAP KARTU")
    id_kartu = input("Masukkan ID kartu (contoh 001): ").strip()

    # Validasi kartu & perjalanan
    data = validasi.cek_kartu(id_kartu)
    if data is None:
        print("  [DITOLAK] Kartu tidak terdaftar.")
        return
    elif validasi.cek_sedang_perjalanan(id_kartu):
        print("  [DITOLAK] Kartu ini masih dalam perjalanan. Tunggu sampai tiba.")
        return

    print(f"  Halo, {data['nama']}! (berat {data['berat']} kg)")
    print(f"  Lantai yang diizinkan: {data['izin']}")

    # --- 1. SISTEM DETEKSI OTOMATIS ---
    lantai_asal = 1  # Default: Lobi
    for p in reversed(database.riwayat):
        if p["kartu"] == id_kartu and p["status"] == "sudah tiba":
            lantai_asal = p["tujuan"]
            break

    print(f"  [SISTEM] Berdasarkan riwayat lift, Anda terakhir berada di lantai {lantai_asal}.")
    
    # --- 2. KASUS NAIK TANGGA (USER BISA KOREKSI) ---
    print(f"  (Jika Anda naik tangga, ketik lantai Anda sekarang. Atau tekan Enter jika sudah benar)")
    input_asal = input(f"  Anda sekarang di lantai: ").strip()
    
    if input_asal != "":
        if not input_asal.isdigit():
            print("  [!] Input tidak valid.")
            return
        
        lantai_baru = int(input_asal)
        
        # --- FITUR ZONA TERLARANG ---
        if lantai_baru not in data["izin"]:
            print(f"  [!] KARTU ANDA TIDAK PUNYA AKSES KE LANTAI {lantai_baru}.")
            # Beri opsi evakuasi darurat
            evakuasi = input(f"  [DARURAT] Apakah Anda ingin dievakuasi turun ke Lobi (Lantai 1)? (y/n): ").strip().lower()
            if evakuasi == "y":
                lantai_asal = lantai_baru
                lantai_tujuan = 1  # Paksa tujuannya ke lobi
                print("  [SISTEM] Mode evakuasi aktif. Lift akan menjemput Anda dan membawa ke Lantai 1.")
                proses_alokasi(id_kartu, lantai_asal, lantai_tujuan)
                return
            else:
                print("  [BATAL] Silakan hubungi keamanan gedung.")
                return
        else:
            lantai_asal = lantai_baru # Lantai diizinkan
    
    print(f"  -> Dikonfirmasi Anda berada di lantai {lantai_asal}.")

    # --- 3. INPUT LANTAI TUJUAN ---
    lantai_tujuan = validasi.input_lantai("Mau ke lantai berapa? ")
    
    boleh, pesan = validasi.cek_tujuan(data, lantai_asal, lantai_tujuan)
    if not boleh:
        print(f"  {pesan}")
        return

    print()
    proses_alokasi(id_kartu, lantai_asal, lantai_tujuan)


def proses_alokasi(id_kartu, lantai_asal, lantai_tujuan):
    """Memilih lift, menjadwalkannya, lalu mencatat ke riwayat (menu 1)."""
    berat = database.kartu[id_kartu]["berat"]

    # Pilih lift terbaik yang masih muat (modul prioritas_lift)
    nama_lift, alasan = prioritas_lift.pilih_lift(lantai_asal, lantai_tujuan, berat)
    if nama_lift is None:
        print(f"  [PENUH] Kartu {id_kartu}: {alasan}. Jalankan lift dulu, lalu tap ulang.")
        return

    lift = database.lifts[nama_lift]
    prioritas_lift.jadwalkan(lift, lantai_asal, lantai_tujuan)

    # Penumpang baru bisa masuk kalau lift sudah ada di lantai asal
    if lift["posisi"] == lantai_asal:
        status = "di dalam lift"
    else:
        status = "menunggu lift"

    # Simpan ke riwayat (modul database)
    database.riwayat.append({
        "kartu": id_kartu,
        "asal": lantai_asal,
        "tujuan": lantai_tujuan,
        "lift": nama_lift,
        "status": status,
    })

    beban = prioritas_lift.beban_lift(nama_lift)
    print(f"  >>> Kartu {id_kartu} -> Lantai {lantai_tujuan} -> Silakan menuju LIFT {nama_lift}")
    print(f"      (alasan: {alasan}; beban Lift {nama_lift}: {beban}/{database.KAPASITAS_MAKS_KG} kg)")
    if status == "menunggu lift":
        print(f"      Lift {nama_lift} sedang menuju lantai {lantai_asal}, mohon tunggu.")


def tampilkan_status():
    """Menu 2: menampilkan posisi, arah, dan tujuan setiap lift."""
    garis()
    print("STATUS LIFT")
    print(f"{'Lift':<6}{'Posisi':<9}{'Arah':<8}{'Isi':<6}{'Beban (kg)':<13}Tujuan")
    for nama, lift in database.lifts.items():
        if len(lift["tujuan"]) == 0:
            tujuan = "-"
        else:
            tujuan = ", ".join(str(x) for x in lift["tujuan"])
        # Hitung penumpang yang sedang berada di dalam lift ini
        isi = 0
        for p in database.riwayat:
            if p["lift"] == nama and p["status"] == "di dalam lift":
                isi = isi + 1
        beban = f"{prioritas_lift.beban_lift(nama)}/{database.KAPASITAS_MAKS_KG}"
        print(f"{nama:<6}{lift['posisi']:<9}{prioritas_lift.arah_lift(lift):<8}{isi:<6}{beban:<13}{tujuan}")


def jalankan_lift():
    """Menu 3: setiap lift bergerak ke lantai tujuan berikutnya."""
    garis()
    print("MENJALANKAN LIFT (1 langkah)")
    ada_gerak = False
    for nama, lift in database.lifts.items():
        if len(lift["tujuan"]) > 0:
            dari = lift["posisi"]
            ke = lift["tujuan"].pop(0)   # ambil tujuan pertama
            lift["posisi"] = ke
            print(f"  Lift {nama}: lantai {dari} -> {ke} (pintu terbuka)")
            ada_gerak = True

            # Penumpang yang tujuannya lantai ini turun dulu
            for p in database.riwayat:
                if p["lift"] == nama and p["status"] == "di dalam lift" and p["tujuan"] == ke:
                    p["status"] = "sudah tiba"
                    print(f"      Kartu {p['kartu']} turun di lantai {ke}")
            # Lalu penumpang yang menunggu di lantai ini naik
            for p in database.riwayat:
                if p["lift"] == nama and p["status"] == "menunggu lift" and p["asal"] == ke:
                    p["status"] = "di dalam lift"
                    print(f"      Kartu {p['kartu']} naik, menuju lantai {p['tujuan']}")
    if not ada_gerak:
        print("  Semua lift sedang diam, tidak ada panggilan.")


def tampilkan_kartu():
    """Menu 4: daftar kartu yang bisa dipakai untuk mencoba program."""
    garis()
    print("DAFTAR KARTU TERDAFTAR")
    for id_kartu, data in database.kartu.items():
        if id_kartu == "999":
            izin = "semua lantai"
        else:
            izin = str(data["izin"])
        print(f"  {id_kartu}  {data['nama']:<25} {data['berat']:>3} kg  izin: {izin}")


def tampilkan_riwayat():
    """Menu 5: menampilkan riwayat alokasi lift."""
    garis()
    print("RIWAYAT ALOKASI")
    if len(database.riwayat) == 0:
        print("  Belum ada riwayat.")
    for i, p in enumerate(database.riwayat, start=1):
        posisi_lift = database.lifts[p["lift"]]["posisi"]
        print(f"  {i}. Kartu {p['kartu']}: lantai {p['asal']} -> {p['tujuan']}, "
              f"Lift {p['lift']} (sekarang di lantai {posisi_lift}) [{p['status']}]")


# =====================================================================
# FITUR RAHASIA: SIMULASI OTOMATIS
# =====================================================================

def simulasi_otomatis():
    """Fitur rahasia: Generate penumpang acak dan jalankan lift sampai selesai."""
    garis()
    print("MODE SIMULASI OTOMATIS")
    garis()
    
    # Minta jumlah penumpang
    try:
        jumlah = int(input("Mau simulasikan berapa penumpang? (1-10): "))
        if jumlah < 1 or jumlah > 10:
            print("  [!] Jumlah harus antara 1 sampai 10.")
            return
    except ValueError:
        print("  [!] Masukkan angka yang valid.")
        return

    # Ambil daftar ID yang ada (kecuali admin 999)
    daftar_id = [id for id in database.kartu.keys() if id != "999"]
    
    # Pastikan ID yang dipilih nggak lebih banyak dari yang tersedia
    if jumlah > len(daftar_id):
        jumlah = len(daftar_id)
        
    id_terpilih = random.sample(daftar_id, jumlah)
    
    print(f"\n  [SISTEM] Men-generate {jumlah} penumpang acak...")
    
    # --- FASE 1: TAP KARTU OTOMATIS ---
    for id_kartu in id_terpilih:
        data = database.kartu[id_kartu]
        
        # Pilih lantai asal secara acak dari list izin
        lantai_asal = random.choice(data["izin"])
        
        # Pilih lantai tujuan secara acak, pastikan beda dengan asal
        pilihan_tujuan = [l for l in data["izin"] if l != lantai_asal]
        if not pilihan_tujuan:
            continue # Skip kalau cuma punya 1 izin lantai
        lantai_tujuan = random.choice(pilihan_tujuan)
        
        print(f"  -> {data['nama']} tap dari Lantai {lantai_asal} ke Lantai {lantai_tujuan}")
        
        # Panggil fungsi alokasi (tanpa nampilin print panjang biar rapi)
        # Kita panggil fungsi proses_alokasi yang udah ada
        proses_alokasi(id_kartu, lantai_asal, lantai_tujuan)

    print("\n  [SISTEM] Semua penumpang sudah tap kartu. Lift mulai bergerak...")
    input("  Tekan Enter untuk memulai pergerakan lift...")
    print()

    # --- FASE 2: JALANKAN LIFT SAMPAI SELESAI ---
    langkah = 1
    # Loop terus selama masih ada perjalanan yang belum "sudah tiba"
    while any(p["status"] != "sudah tiba" for p in database.riwayat):
        print(f"  --- Langkah {langkah} ---")
        ada_gerak = False
        
        for nama, lift in database.lifts.items():
            if len(lift["tujuan"]) > 0:
                dari = lift["posisi"]
                ke = lift["tujuan"].pop(0)
                lift["posisi"] = ke
                print(f"    Lift {nama}: lantai {dari} -> {ke}")
                ada_gerak = True

                # Turunin penumpang
                for p in database.riwayat:
                    if p["lift"] == nama and p["status"] == "di dalam lift" and p["tujuan"] == ke:
                        p["status"] = "sudah tiba"
                        print(f"      [TURUN] {database.kartu[p['kartu']]['nama']} tiba di lantai {ke}")
                
                # Naikin penumpang
                for p in database.riwayat:
                    if p["lift"] == nama and p["status"] == "menunggu lift" and p["asal"] == ke:
                        p["status"] = "di dalam lift"
                        print(f"      [NAIK] {database.kartu[p['kartu']]['nama']} masuk, menuju lantai {p['tujuan']}")
        
        if not ada_gerak:
            # Antisipasi kalau ada bug di mana lift nggak gerak tapi status belum tiba
            print("  [WARNING] Lift berhenti tapi masih ada penumpang tertinggal.")
            break
            
        langkah += 1
        print() 

    # --- FASE 3: HASIL AKHIR ---
    garis()
    print("SIMULASI SELESAI!")
    print("Semua penumpang telah tiba di tujuan masing-masing.")
    garis()
    
    print("\nRingkasan Perjalanan:")
    for p in database.riwayat:
        nama = database.kartu[p['kartu']]['nama']
        print(f"  - {nama}: Lantai {p['asal']} -> {p['tujuan']} (Lift {p['lift']})")