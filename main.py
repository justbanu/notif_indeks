import json
import os
import smtplib
import time  # <--- TAMBAHKAN BARIS INI
from email.message import EmailMessage
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# Load variable dari file .env (EMAIL_USER dan EMAIL_PASS)
load_dotenv()

FILE_DATA = "data_nilai.json"


def kirim_notifikasi_email(subjek, isi_pesan):
    EMAIL_PENGIRIM = os.getenv("EMAIL_USER")
    PASSWORD_KAMU = os.getenv("EMAIL_PASS")
    EMAIL_PENERIMA = EMAIL_PENGIRIM  # Dikirim ke diri sendiri

    msg = EmailMessage()
    msg["Subject"] = subjek
    msg["From"] = EMAIL_PENGIRIM
    msg["To"] = EMAIL_PENERIMA
    msg.set_content(isi_pesan)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_PENGIRIM, PASSWORD_KAMU)
            server.send_message(msg)
        print("Email notifikasi berhasil dikirim!")
    except Exception as e:
        print(f"Gagal mengirim email. Error: {e}")


def cek_nilai():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # Memuat sesi login yang sudah direkam sebelumnya
        context = browser.new_context(storage_state="auth.json")
        page = context.new_page()

        url_historis = "https://six.itb.ac.id/app/mahasiswa/18225109/statusmhs/transkrip/historis/2021180266"
        page.goto(url_historis)
        page.wait_for_load_state("networkidle")

        # Mengambil seluruh baris (tr) yang berada di dalam tabel indeks
        rows = page.query_selector_all(
            "table.table-striped.table-condensed tbody tr"
        )

        nilai_terbaru = {}
        for row in rows:
            cols = row.query_selector_all("th, td")

            # Mengambil data mata kuliah (kolom ke-2) dan Nilai (kolom ke-4)
            if len(cols) >= 5:
                matkul = cols[1].inner_text().strip()
                nilai = cols[3].inner_text().strip()

                if matkul:
                    nilai_terbaru[matkul] = nilai

        browser.close()
        return nilai_terbaru


# --- Logika Utama  Notifikasi ---
# --- Logika Utama Penyelaras Notifikasi (Mode Auto-Loop) ---
if __name__ == "__main__":
    # Menghitung menit ke dalam detik (15 menit = 900 detik)
    JEDA_WAKTU = 15 * 60 
    
    print(" Program pemantau indeks SIX ITB aktif!")
    print("Program akan berjalan otomatis di terminal ini setiap 15 menit.")
    print("Jangan tutup terminal ini agar pengecekan tetap berjalan.\n")
    
    while True:
        try:
            # 1. Baca database nilai dari pengecekan sebelumnya
            try:
                with open(FILE_DATA, "r") as f:
                    nilai_lama = json.load(f)
            except FileNotFoundError:
                nilai_lama = {}

            # 2. Jalankan scraping untuk mengambil data SIX saat ini
            print(f"[{time.strftime('%H:%M:%S')}] Sedang mengecek nilai ke SIX ITB...")
            nilai_sekarang = cek_nilai()

            # 3. Bandingkan nilai lama dengan nilai sekarang
            for matkul, nilai in nilai_sekarang.items():
                if nilai_lama.get(matkul) == "" and nilai != "":
                    subjek_email = f" [SIX ITB] Nilai {matkul} Keluar!"
                    pesan_email = (
                        f"Halo Banu,\n\nNilai untuk mata kuliah {matkul} "
                        f"sudah diperbarui di SIX ITB.\nIndeks kamu: {nilai}\n\n"
                        f"Silakan cek langsung."
                    )
                    kirim_notifikasi_email(subjek_email, pesan_email)
                    print(f" Notifikasi email dikirim untuk {matkul}")

            # 4. Simpan kondisi terbaru ke file JSON
            with open(FILE_DATA, "w") as f:
                json.dump(nilai_sekarang, f)

            print(f"Pengecekan selesai. Tidur selama 15 menit ke depan...\n")
            
        except Exception as e:
            print(f"Terjadi kesalahan pada sesi ini: {e}")
            print("Mencoba lagi di sesi berikutnya...\n")
            
        # Program akan diam/tidur selama 15 menit sebelum mengulang ke atas
        time.sleep(JEDA_WAKTU)