class Idol:
    def __init__(self, nama, grup, kontrak):
        self.nama = nama
        self.grup = grup
        self.kontrak = kontrak

    def profil(self):
     return (f"Idol: {self.nama}, Grup: {self.grup}, Kontrak: {self.kontrak} Tahun")

    def status_kontrak(self):
        if self.kontrak >= 8:
            return "Telah Perpanjang Kontrak Kedua"
        elif self.kontrak >= 7:
            return "Perpanjang ke Kontrak Kedua"
        elif self.kontrak >= 4:
            return "Masa-Masa Berjuang"
        else:
            return "Masih Rookie"
    
    @staticmethod
    def kategori_kontrak(nilai):
        if nilai >= 8:
            return "Kontrak Kedua"
        elif nilai >= 7:
            return "Akhir Kontrak Pertama"
        elif nilai >= 4:
            return "Pertengahan Kontrak"
        else:
            return "Baru Debut"
    
idol1 = Idol("Jeno", "NCT", 10)
idol2 = Idol("Kimberly", "VVUP", 2)

print("Hasil")
print(idol1.profil())
print("Status: ", idol1.status_kontrak())
print("Kategori Kontrak Jeno: ",Idol.kategori_kontrak(idol1.kontrak))

print(idol2.profil())
print("Status: ", idol2.status_kontrak())
print("Kategori Kontrak Kimberly: ",Idol.kategori_kontrak(idol2.kontrak))