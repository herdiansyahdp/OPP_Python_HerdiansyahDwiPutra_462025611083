class E_Wallet:
    def __init__(self, nama, id_pengguna, pin, saldo):
        self.__nama = nama
        self.__id_pengguna = id_pengguna
        self.__pin = pin
        self.__saldo = saldo

    def get_nama(self):
        return self.__nama
    def get_id_pengguna(self):
        return self.__id_pengguna
    
    def cek_saldo(self, pin):
        if pin == self.__pin:
            return (f"Saldo Kamu: Rp.{self.__saldo}")
        else:
            return ("PIN YANG KAMU MASUKKAN SALAH!!! PERMINTAAN DITOLAK")
            
    def tarik_uang(self, pin, jumlah):
        if pin == self.__pin:
            if jumlah <= self.__saldo:
                self.__saldo -= jumlah
                return(f"Penarikan berhasil. Sisa saldo kamu: Rp.{self.__saldo}")
            else:
                return ("HEYY SALDO KAMU TIDAK CUKUP!!!")
        else:
            return ("PIN YANG KAMU MASUKKAN SALAH!!! PERMINTAAN DITOLAK")
            
user1 = E_Wallet("Junkyu", "TRZ004", "090900", 17000000)
user2 = E_Wallet("Asahi", "TRZ006", "200803", 10000000)

print("Nama: ", user1.get_nama())
print("ID Pengguna: ", user1.get_id_pengguna())

print("=====CEK SALDO=====")
print(user1.cek_saldo("090900"))

print("=====TARIK UANG=====")
print(user1.tarik_uang("090900", 1000000))

print("\ncNama: ", user2.get_nama())
print("ID Pengguna: ", user2.get_id_pengguna())

print("=====CEK SALDO=====")
print(user2.cek_saldo("200803"))
print(user2.cek_saldo("123456"))

print("=====TARIK UANG=====")
print(user2.tarik_uang("200803", 1000000))
print(user2.tarik_uang("123456", 1000000))