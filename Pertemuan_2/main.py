class Mahasiswa:
    def __init__(self, nama, prodi, asrama):
        self.nama = nama
        self.prodi = prodi
        self.asrama = asrama

mhs1 = Mahasiswa("Jono", "Teknik Informatika", "Umar")
mhs2 = Mahasiswa("Ajun", "Hubungan Internasional", "Usman")

print(f"Nama: {mhs1.nama}, Prodi: {mhs1.prodi}, Asrama: {mhs1.asrama}")
print(f"Nama: {mhs2.nama}, Prodi: {mhs2.prodi}, Asrama: {mhs2.asrama}")