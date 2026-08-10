#Parent Class
class AlatPembayaran:
    def proses_bayar(self):
        print("Memproses pembayaran...")

#Child Class 1
class KartuKredit(AlatPembayaran):
    def proses_bayar(self):
        print("Pembayaran menggunakan kartu kredit")

#Child Class 2
class EWallet(AlatPembayaran):
    def proses_bayar(self):
        print("Pembayaran menggunakan E-Wallet")

def jalankan_transaksi(objek):
    objek.proses_bayar()

kartu = KartuKredit()
ewallet = EWallet()

print("   TRANSAKSI   ")
jalankan_transaksi(kartu)
jalankan_transaksi(ewallet)