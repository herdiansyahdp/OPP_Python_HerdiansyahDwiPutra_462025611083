class NamaTidakValid(Exception):
    pass

class NIMTidakValid(Exception):
    pass

class NilaiTidakValid(Exception):
    pass

class Mahasiswa:
    def __init__(self, nama, nim):
        self.nama = nama
        self.nim = nim

    def cek_nama(self):
        if self.nama.strip() == "":
            raise NamaTidakValid("Nama mahasiswa tidak boleh kosong!")

    def cek_nim(self):
        if len(self.nim) != 12:
            raise NIMTidakValid("NIM harus terdiri dari 12 digit!")
    
    def validasi_data(self):
        self.cek_nama()
        self.cek_nim()

    def input_nilai(self, nilai):
        self.validasi_data()

        if nilai < 0 or nilai > 100:
            raise NilaiTidakValid("Nilai harus berada di antara 0 - 100!")
        
        print(f"===DATA BERHASIL DISIMPAN!===")
        print(f"Nama  : {self.nama}")
        print(f"NIM   : {self.nim}")
        print(f"Nilai : {nilai}")

while True:
    try:
        nama = input("Masukkan Nama Mahasiswa: ")
        nim = input("Masukkan NIM Mahasiswa: ")
        nilai = int(input("Masukkan Nilai: "))

        mhs = Mahasiswa(nama, nim)
        mhs.input_nilai(nilai)

    except NamaTidakValid as e:
        print("ERROR: ", e)
    except NilaiTidakValid as e:
        print("ERROR: ", e)
    except NIMTidakValid as e:
        print("ERROR: ", e)
    except ValueError:
        print("ERROR: Nilai harus berupa angka!")

    lagi = input("Input Mahasiswa Lagi? (Y/n): ")

    if lagi.lower() != "y":
        print("Program Selesai!")
        break