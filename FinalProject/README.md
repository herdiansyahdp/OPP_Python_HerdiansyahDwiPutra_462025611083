# Sistem Pengadaan Dokumentasi Multimedia

Final Project mata kuliah **Object-Oriented Programming (OOP)**.

Aplikasi web berbasis Python (Flask) untuk UPT Multimedia and Public Relations. Aplikasi ini digunakan untuk mendata pengajuan pengadaan dokumentasi (Fotografi, Videografi, Broadcast, Drone, LED) di setiap acara kampus, menggantikan pencatatan manual dari surat masuk.

---

## 1. Fitur Utama

| Menu | Deskripsi |
|---|---|
| **Login Admin** | Halaman autentikasi untuk membatasi akses sistem hanya untuk admin UPT. |
| **Menu Utama (Dashboard)** | Menampilkan daftar seluruh acara yang sudah terdata beserta *badge* layanan yang digunakan. Terdapat fitur untuk Edit dan Hapus acara. |
| **Tambah & Edit Acara** | Form pengadaan dengan sinkronisasi pilihan layanan. Admin dapat memasukkan nama acara, memilih tanggal & waktu dari *dropdown*, serta mendata detail petugas dan alat untuk setiap layanan yang dipilih. |
| **Database Anggota** | Memantau status anggota UPT (*Kosong*, *Bertugas*, *Akan Bertugas*). Dilengkapi fitur untuk menambah anggota baru, mengubah status anggota (otomatis berpindah kolom), dan menghapus anggota. |
| **Riwayat & Statistik** | Rekapitulasi seluruh acara dalam bentuk tabel yang dapat di-klik (*expandable row*) untuk melihat detail petugas dan alat tanpa membuat halaman terlihat penuh. |

---

## 2. Struktur Folder

``s`text
Final_Project/
├── app.py                  #Controller Flask (routing, penerima input UI, pemanggil model)
├── models.py               #Seluruh logika OOP murni Python (Layanan, Acara, Anggota, Database)
├── requirements.txt        #Daftar dependensi library (Flask & Werkzeug)
├── README.md               #Dokumentasi proyek
├── data/                   #Folder penyimpanan data (dibuat otomatis saat pertama di-run)
│   ├── acara.json
│   └── anggota.json
├── templates/              #Tampilan HTML (Jinja2)
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── tambah_acara.html
│   ├── edit_acara.html
│   ├── database_anggota.html
│   └── riwayat.html
└── static/                 #Aset statis pendukung UI
    ├── css/style.css       #Styling warna UPT (Navy, Brown, Gold, Cream)
    ├── js/main.js          #Interaksi frontend (sinkronisasi form & flash message)
    └── img/logo.png        #Logo UPT Multimedia