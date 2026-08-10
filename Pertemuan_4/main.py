class Produk:
     def __init__(self, nama, harga) :
          self.nama = nama
          self.harga = harga

     def __str__(self):
          return (f"Produk: {self.nama}, Harga: Rp.{self.harga}")

     def __eq__(self, other):
          return self.harga == other.harga

     def __it__(self, other):
          return self.harga < other.harga

     def __gt__(self, other):
          return self.harga > other.harga

p1 = Produk("Laptop", 15000000)
p2 = Produk("Handphone", 15000000)
p3 = Produk("Monitor", 500000)

print(p1)
print(p2)
print(p3)

print("\n     Perbandingan     ") 

print("Apakah harga Laptop sama dengan Handphone? ", p1 == p2) 
print("Apakah harga Laptop > Monitor?", p1 > p3)
print("Apakah Handphone < Monitor?", p2 < p3)