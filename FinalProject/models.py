import json
import os
import uuid
from datetime import datetime
from abc import ABC, abstractmethod

#1. CUSTOM EXCEPTIONS (Robustness)
class SistemMultimediaError(Exception):
    """Base exception untuk aplikasi ini."""
    pass

class ValidasiError(SistemMultimediaError):
    pass

class AutentikasiError(SistemMultimediaError):
    pass

#2. INHERITANCE & POLYMORPHISM
class Layanan(ABC):
    nama_layanan = "Layanan"

    def __init__(self, petugas=None, alat=None):
        self.petugas = petugas if petugas else []
        self.alat = alat if alat else []

    @abstractmethod
    def ikon(self) -> str:
        raise NotImplementedError

    def ringkasan(self) -> str:
        # Polymorphism: dipanggil sama, tapi hasil beda tergantung subclass
        petugas_str = ", ".join(self.petugas) if self.petugas else "-"
        alat_str = ", ".join(self.alat) if self.alat else "-"
        return f"{self.ikon()} {self.nama_layanan} | Petugas: {petugas_str} | Alat: {alat_str}"

    def to_dict(self) -> dict:
        return {"jenis": self.nama_layanan, "petugas": self.petugas, "alat": self.alat}

class Fotografi(Layanan):
    nama_layanan = "Fotografi"
    def ikon(self) -> str: return "📸"

class Videografi(Layanan):
    nama_layanan = "Videografi"
    def ikon(self) -> str: return "🎥"

class Broadcast(Layanan):
    nama_layanan = "Broadcast"
    def ikon(self) -> str: return "📡"

class Drone(Layanan):
    nama_layanan = "Drone"
    def ikon(self) -> str: return "🚁"

class LED(Layanan):
    nama_layanan = "LED"
    def ikon(self) -> str: return "📺"

DAFTAR_LAYANAN = {
    "Fotografi": Fotografi, "Videografi": Videografi,
    "Broadcast": Broadcast, "Drone": Drone, "LED": LED,
}

def buat_layanan(jenis: str, petugas=None, alat=None) -> Layanan:
    cls = DAFTAR_LAYANAN.get(jenis)
    if not cls: raise ValidasiError(f"Jenis layanan '{jenis}' tidak dikenal.")
    return cls(petugas=petugas, alat=alat)

#3. ENCAPSULATION, MAGIC & STATIC METHODS
class Anggota:
    def __init__(self, id_anggota: str, nama: str, divisi: str, status: str = "Kosong"):
        self.id_anggota = id_anggota
        self.nama = nama
        self.divisi = divisi
        self.__status = status # Encapsulation

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, value: str):
        if value not in ["Kosong", "Bertugas", "Akan Bertugas"]:
            raise ValidasiError("Status tidak valid.")
        self.__status = value

    def to_dict(self) -> dict:
        return {"id_anggota": self.id_anggota, "nama": self.nama, "divisi": self.divisi, "status": self.status}

class Acara:
    def __init__(self, nama_acara: str, tanggal: str, waktu: str, layanan_list=None, id_acara: str = None):
        self.id_acara = id_acara or str(uuid.uuid4())[:8]
        self.nama_acara = nama_acara
        self.__tanggal = None # Encapsulation
        self.tanggal = tanggal 
        self.waktu = waktu
        self.layanan_list = layanan_list if layanan_list else []

    @property
    def tanggal(self) -> str:
        return self.__tanggal

    @tanggal.setter
    def tanggal(self, value: str):
        if self.validasi_format_tanggal(value):
            self.__tanggal = value

    @staticmethod
    def validasi_format_tanggal(tanggal_str: str) -> bool:
        try:
            datetime.strptime(tanggal_str, "%Y-%m-%d")
            return True
        except ValueError:
            raise ValidasiError("Format tanggal salah. Gunakan YYYY-MM-DD.")

    def tambah_layanan(self, layanan: Layanan):
        self.layanan_list.append(layanan)

    def __lt__(self, other) -> bool:
        # Magic Method untuk urutkan list acara
        return (self.tanggal, self.waktu) < (other.tanggal, other.waktu)

    def to_dict(self) -> dict:
        return {
            "id_acara": self.id_acara, "nama_acara": self.nama_acara,
            "tanggal": self.tanggal, "waktu": self.waktu,
            "layanan_list": [l.to_dict() for l in self.layanan_list],
        }

#4. DATABASE MANAGER (I/O File JSON)
class DatabaseManager:
    def __init__(self):
        if not os.path.exists("data"): os.makedirs("data")
        self.file_acara = "data/acara.json"
        self.file_anggota = "data/anggota.json"
        
        for file_name in [self.file_acara, self.file_anggota]:
            if not os.path.exists(file_name):
                with open(file_name, "w") as f: json.dump([], f)

    def _baca(self, path):
        with open(path, "r") as f: return json.load(f)

    def _simpan(self, path, data):
        with open(path, "w") as f: json.dump(data, f, indent=2)

    def semua_acara(self):
        data = self._baca(self.file_acara)
        acaras = []
        for d in data:
            layanan_objs = [buat_layanan(l["jenis"], l.get("petugas"), l.get("alat")) for l in d.get("layanan_list", [])]
            acaras.append(Acara(d["nama_acara"], d["tanggal"], d["waktu"], layanan_objs, d["id_acara"]))
        return sorted(acaras)

    def cari_acara(self, id_acara):
        for acara in self.semua_acara():
            if acara.id_acara == id_acara: return acara
        raise ValidasiError("Acara tidak ditemukan.")

    def tambah_acara(self, acara):
        data = self._baca(self.file_acara)
        data.append(acara.to_dict())
        self._simpan(self.file_acara, data)

    def update_acara(self, acara_baru):
        data = self._baca(self.file_acara)
        for i, d in enumerate(data):
            if d["id_acara"] == acara_baru.id_acara:
                data[i] = acara_baru.to_dict()
                break
        self._simpan(self.file_acara, data)

    def hapus_acara(self, id_acara):
        data = [d for d in self._baca(self.file_acara) if d["id_acara"] != id_acara]
        self._simpan(self.file_acara, data)

    def semua_anggota(self):
        return [Anggota(d["id_anggota"], d["nama"], d["divisi"], d.get("status", "Kosong")) for d in self._baca(self.file_anggota)]

    def tambah_anggota(self, anggota):
        data = self._baca(self.file_anggota)
        data.append(anggota.to_dict())
        self._simpan(self.file_anggota, data)

    def update_status_anggota(self, id_anggota, status_baru):
        data = self._baca(self.file_anggota)
        for d in data:
            if d["id_anggota"] == id_anggota:
                d["status"] = status_baru
                break
        self._simpan(self.file_anggota, data)

    def hapus_anggota(self, id_anggota):
        data = [d for d in self._baca(self.file_anggota) if d["id_anggota"] != id_anggota]
        self._simpan(self.file_anggota, data)

    def anggota_berdasarkan_status(self):
        hasil = {"Kosong": [], "Bertugas": [], "Akan Bertugas": []}
        for a in self.semua_anggota(): hasil[a.status].append(a)
        return hasil