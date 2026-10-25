"""
MODUL DATABASE
Berisi semua data program dalam bentuk dictionary dan list:
data lift, data kartu (termasuk berat badan), dan riwayat alokasi.
Modul lain membaca dan mengubah data lewat `import database`.
"""
import random

# List nama buat diacak
nama_nama_acak = [
    "Budi", "Siti", "Andi", "Rina", "Dewi", "Agus", "Bambang", "Sari", 
    "Joko", "Rizky", "Putri", "Fajar", "Anugrah", "Hizqil", "Ihdan",
    "Tono", "Nina", "Dodi", "Lestari", "Hendra", "Maya", "Eko", "Indah"
]

LANTAI_TERENDAH = 1    # lantai 1 = lobi utama
LANTAI_TERTINGGI = 32  # sesuaikan dengan jumlah lantai gedung
KAPASITAS_MAKS_KG = 1200  # beban maksimal satu lift (kg)

# Data setiap lift disimpan dalam dictionary.
lifts = {
    "A": {"posisi": 1, "tujuan": []},
    "B": {"posisi": 1, "tujuan": []},
    "C": {"posisi": 1, "tujuan": []},
    "D": {"posisi": 1, "tujuan": []},
    "E": {"posisi": 1, "tujuan": []},
}

# Data kartu: ID kartu -> nama pemilik, berat badan (kg), dan lantai yang diizinkan.
kartu = {
    "001": {"nama": "Mahasiswa - Anugrah", "berat": 70, "izin": [1, 10, 11, 12]},
    "002": {"nama": "Mahasiswa - Hizqil", "berat": 65, "izin": [1, 10, 11, 12]},
    "003": {"nama": "Mahasiswa - Ihdan", "berat": 68, "izin": [1, 10, 11, 12]},
    "004": {"nama": "Dosen", "berat": 75, "izin": [1, 10, 11, 12, 15]},
    "005": {"nama": "Karyawan Kantor PT X", "berat": 72, "izin": [1, 3, 4, 7]},
    "006": {"nama": "Karyawan Kantor PT Y", "berat": 80, "izin": [1, 20, 21, 25]},
    "007": {"nama": "Karyawan Kantor PT Z - Budi", "berat": 85, "izin": [1, 10, 11, 12]},
    "008": {"nama": "Manajer Kantor PT Y - Citra", "berat": 52, "izin": [1, 10, 11, 12]},
    "009": {"nama": "OB - Dimas", "berat": 90, "izin": [1, 10, 11, 12]},
    "010": {"nama": "Marketing PT A - Eka", "berat": 58, "izin": [1, 10, 11, 12]},
    "011": {"nama": "Mahasiswa - Fajar", "berat": 78, "izin": [1, 10, 11, 12]},
    "012": {"nama": "Mahasiswa - Gita", "berat": 55, "izin": [1, 10, 11, 12]},
    "013": {"nama": "Mahasiswa - Hendra", "berat": 95, "izin": [1, 10, 11, 12]},
    "014": {"nama": "Mahasiswa - Indah", "berat": 60, "izin": [1, 10, 11, 12]},
    "015": {"nama": "Mahasiswa - Joko", "berat": 82, "izin": [1, 10, 11, 12]},
    "016": {"nama": "Mahasiswa - Kirana", "berat": 57, "izin": [1, 10, 11, 12]},
    "017": {"nama": "Mahasiswa - Lukman", "berat": 88, "izin": [1, 10, 11, 12]},
    "018": {"nama": "Mahasiswa - Maya", "berat": 62, "izin": [1, 10, 11, 12]},
    "019": {"nama": "Mahasiswa - Nanda", "berat": 74, "izin": [1, 10, 11, 12]},
    "020": {"nama": "Mahasiswa - Oki", "berat": 92, "izin": [1, 10, 11, 12]},
    "021": {"nama": "Mahasiswa - Putri", "berat": 54, "izin": [1, 10, 11, 12]},
    "022": {"nama": "Mahasiswa - Rizky", "berat": 86, "izin": [1, 10, 11, 12]},
    "999": {"nama": "Pengelola Gedung", "berat": 78, "izin": list(range(1, 33))},
}

# Riwayat alokasi
riwayat = []

def acak_data(seed=None):
    if seed is not None:
        random.seed(seed)

    # 1. Acak posisi awal lift
    for nama in lifts:
        lifts[nama]["posisi"] = random.randint(1, 15)

    # 2. Aturan Lantai Acak per Role (min, max, jumlah_lantai)
    role_rules = {
        # --- Mahasiswa & Akademisi ---
        "Mahasiswa": {"min": 10, "max": 18, "jml": 3},
        "Dosen": {"min": 10, "max": 20, "jml": 4},
        
        # --- Karyawan Umum ---
        "OB": {"min": 2, "max": 8, "jml": 3},
        "Security": {"min": 1, "max": 5, "jml": 3},
        "Resepsionis": {"min": 1, "max": 3, "jml": 2},
        "IT Support": {"min": 8, "max": 20, "jml": 5},
        
        # --- Manajerial & Spesialis ---
        "Manajer": {"min": 20, "max": 29, "jml": 4},
        "HRD": {"min": 5, "max": 12, "jml": 3},
        "Marketing": {"min": 5, "max": 25, "jml": 4},
        "Akuntan PT X": {"min": 10, "max": 15, "jml": 3},
        "Akuntan PT Y": {"min": 16, "max": 22, "jml": 3},
        
        # --- Eksekutif ---
        "CEO": {"min": 30, "max": 32, "jml": 2},
        "Direktur": {"min": 28, "max": 32, "jml": 3},
    }
    
    # 3. Acak Berat, Role, Nama, dan Izin Lantai
    for id_kartu, data in kartu.items():
        if id_kartu == "999":
            continue
            
        # Acak berat badan (45 - 100 kg)
        data["berat"] = random.randint(45, 100)
        
        # Pilih role dan nama secara acak
        role_baru = random.choice(list(role_rules.keys()))
        nama_baru = random.choice(nama_nama_acak)
        data["nama"] = f"{role_baru} - {nama_baru}"
        
        # --- RANDOMIZER LANTAI IZIN ---
        aturan = role_rules[role_baru]
        # Ambil lantai acak sesuai aturan role
        lantai_acak = random.sample(range(aturan["min"], aturan["max"] + 1), aturan["jml"])
        
        # Wajib bisa ke Lantai 1 (Lobi)
        lantai_acak.append(1)
        
        # Hapus duplikat dan urutkan dari kecil ke besar
        lantai_acak = sorted(list(set(lantai_acak)))
        data["izin"] = lantai_acak

    # 4. Acak ID Kartu (Kecuali Admin)
    data_admin = kartu["999"]
    daftar_user = [data for id_kartu, data in kartu.items() if id_kartu != "999"]
    id_baru_angka = random.sample(range(1, 100), len(daftar_user))
    
    kartu.clear()
    kartu["999"] = data_admin
    
    for id_angka, data in zip(id_baru_angka, daftar_user):
        id_str = f"{id_angka:03d}"
        kartu[id_str] = data