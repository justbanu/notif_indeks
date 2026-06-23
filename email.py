import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def kirim_notifikasi_email(subjek, isi_pesan):
    # Sekarang kita panggil dari environment system, bukan hardcode teks lagi
    EMAIL_PENGIRIM = os.getenv("EMAIL_USER")
    PASSWORD_KAMU = os.getenv("EMAIL_PASS")
    EMAIL_PENERIMA = EMAIL_PENGIRIM  # Dikirim ke diri sendiri
    
    msg = EmailMessage()
    msg['Subject'] = subjek
    msg['From'] = EMAIL_PENGIRIM
    msg['To'] = EMAIL_PENERIMA
    msg.set_content(isi_pesan)
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_PENGIRIM, PASSWORD_KAMU)
            server.send_message(msg)
        print("✅ Email notifikasi berhasil dikirim!")
    except Exception as e:
        print(f"Gagal mengirim email. Error: {e}")


print("Memulai tes pengiriman email...")
kirim_notifikasi_email("Tes Projek Indeks", "Halo Banu, ini test email dari Mac M5!")