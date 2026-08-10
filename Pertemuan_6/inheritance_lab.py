class Idol:
    def __init__(self, nama):
        self.nama = nama
        print(f"{self.nama} telah debut")

    def tampilkan_profesi(self):
        print(f"{self.nama} adalah seorang idol.")

class Singer(Idol):
    def __init__(self, nama):
        super().__init__(nama)
        print(f"{self.nama} memiliki kemampuan vokal.")

    def menyanyi(self):
        print(f"{self.nama} sedang bernyanyi")

class Dancer(Idol):
    def __init__(self, nama):
        super().__init__(nama)
        print(f"{self.nama} memiliki kemampuan dance.")

    def dance(self):
        print(f"{self.nama} sedang nge-dance")

class Performer(Singer, Dancer):
    def __init__(self, nama):
        super().__init__(nama)
        print(f"{self.nama} adalah idol yang serba bisa")

idol1 = Performer("Yuju")

print("\n---Show Performance---")
idol1.tampilkan_profesi()
idol1.menyanyi()
idol1.dance()

print("\nMethod Resolution Order (MRO)")
print(Performer.__mro__)