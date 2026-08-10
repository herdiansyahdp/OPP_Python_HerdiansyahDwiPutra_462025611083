from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import (
    DatabaseManager, Acara, Anggota, buat_layanan, DAFTAR_LAYANAN, SistemMultimediaError, AutentikasiError, ValidasiError
)

app = Flask(__name__)
app.secret_key = "kunci-rahasia-upt-multimedia-2023"
db = DatabaseManager()

USERNAME_VALID = "admin"
PASSWORD_VALID = "multimedia23"

def gabung_tanggal_dari_form(form) -> str:
    hari = form.get("tgl_hari", "")
    bulan = form.get("tgl_bulan", "")
    tahun = form.get("tgl_tahun", "")
    if not (hari and bulan and tahun):
        raise ValidasiError("Tanggal lengkap (hari/bulan/tahun) wajib dipilih semua.")
    return f"{tahun}-{int(bulan):02d}-{int(hari):02d}"

def gabung_waktu_dari_form(form) -> str:
    jam = form.get("waktu_jam", "")
    menit = form.get("waktu_menit", "")
    if not (jam and menit):
        raise ValidasiError("Waktu (jam/menit) wajib dipilih semua.")
    return f"{int(jam):02d}:{int(menit):02d}"

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Silakan login terlebih dahulu.", "error")
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapper

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        try:
            if username != USERNAME_VALID or password != PASSWORD_VALID:
                raise AutentikasiError("Username atau password salah.")
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))
        except AutentikasiError as e:
            flash(str(e), "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Berhasil logout.", "success")
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", daftar_acara=db.semua_acara())

@app.route("/acara/tambah", methods=["GET", "POST"])
@login_required
def tambah_acara():
    if request.method == "POST":
        try:
            acara = Acara(
                nama_acara=request.form.get("nama_acara", ""),
                tanggal=gabung_tanggal_dari_form(request.form),
                waktu=gabung_waktu_dari_form(request.form)
            )
            jenis_dipilih = request.form.getlist("jenis_layanan")
            if not jenis_dipilih:
                raise ValidasiError("Pilih minimal satu jenis layanan.")

            for jenis in jenis_dipilih:
                petugas = [p.strip() for p in request.form.get(f"petugas_{jenis}", "").split(",") if p.strip()]
                alat = [a.strip() for a in request.form.get(f"alat_{jenis}", "").split(",") if a.strip()]
                acara.tambah_layanan(buat_layanan(jenis, petugas=petugas, alat=alat))

            db.tambah_acara(acara)
            flash(f"Acara '{acara.nama_acara}' berhasil ditambahkan.", "success")
            return redirect(url_for("dashboard"))

        except SistemMultimediaError as e:
            flash(str(e), "error")
            
    return render_template("tambah_acara.html", daftar_anggota=db.semua_anggota(), jenis_layanan_tersedia=list(DAFTAR_LAYANAN.keys()))

@app.route("/acara/edit/<id_acara>", methods=["GET", "POST"])
@login_required
def edit_acara(id_acara):
    try:
        acara = db.cari_acara(id_acara)
    except SistemMultimediaError as e:
        flash(str(e), "error")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        try:
            acara_baru = Acara(
                id_acara=id_acara,
                nama_acara=request.form.get("nama_acara", ""),
                tanggal=gabung_tanggal_dari_form(request.form),
                waktu=gabung_waktu_dari_form(request.form)
            )
            jenis_dipilih = request.form.getlist("jenis_layanan")
            if not jenis_dipilih: raise ValidasiError("Pilih minimal satu jenis layanan.")

            for jenis in jenis_dipilih:
                petugas = [p.strip() for p in request.form.get(f"petugas_{jenis}", "").split(",") if p.strip()]
                alat = [a.strip() for a in request.form.get(f"alat_{jenis}", "").split(",") if a.strip()]
                acara_baru.tambah_layanan(buat_layanan(jenis, petugas=petugas, alat=alat))

            db.update_acara(acara_baru)
            flash(f"Acara '{acara_baru.nama_acara}' berhasil diperbarui.", "success")
            return redirect(url_for("dashboard"))
        except SistemMultimediaError as e:
            flash(str(e), "error")

    return render_template("edit_acara.html", acara=acara, daftar_anggota=db.semua_anggota(), jenis_layanan_tersedia=list(DAFTAR_LAYANAN.keys()))

@app.route("/acara/hapus/<id_acara>", methods=["POST"])
@login_required
def hapus_acara(id_acara):
    db.hapus_acara(id_acara)
    flash("Acara berhasil dihapus.", "success")
    return redirect(url_for("dashboard"))

@app.route("/anggota")
@login_required
def database_anggota():
    return render_template("database_anggota.html", kelompok=db.anggota_berdasarkan_status())

@app.route("/anggota/tambah", methods=["POST"])
@login_required
def tambah_anggota():
    import uuid
    id_baru = "A" + str(uuid.uuid4())[:6].upper()
    try:
        db.tambah_anggota(Anggota(id_anggota=id_baru, nama=request.form.get("nama", ""), divisi=request.form.get("divisi", "")))
        flash("Anggota berhasil ditambahkan.", "success")
    except SistemMultimediaError as e:
        flash(str(e), "error")
    return redirect(url_for("database_anggota"))

@app.route("/anggota/hapus/<id_anggota>", methods=["POST"])
@login_required
def hapus_anggota(id_anggota):
    db.hapus_anggota(id_anggota)
    flash("Anggota dihapus.", "success")
    return redirect(url_for("database_anggota"))

@app.route("/anggota/status/<id_anggota>", methods=["POST"])
@login_required
def ubah_status_anggota(id_anggota):
    db.update_status_anggota(id_anggota, request.form.get("status", ""))
    flash("Status anggota diperbarui.", "success")
    return redirect(url_for("database_anggota"))

@app.route("/riwayat")
@login_required
def riwayat():
    return render_template("riwayat.html", semua=db.semua_acara())

@app.errorhandler(SistemMultimediaError)
def handle_domain_error(e):
    flash(str(e), "error")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)