from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # headless=False wajib supaya browsermu muncul di layar
    browser = p.chromium.launch(headless=False) 
    context = browser.new_context()
    page = context.new_page()
    
    print("Membuka SIX ITB...")
    page.goto("https://six.itb.ac.id/login")
    
    # Mengklik tombol login SSO ITB
    page.click("text=Login dengan ITB Account")
    
    # Program terjeda di sini memberi kamu waktu untuk login akun Google ITB
    print("\n SILAKAN LOGIN DI BROWSER YANG MUNCUL!")
    print(" Jika sudah masuk sampai ke dashboard SIX, kembali ke sini dan tekan ENTER...")
    input()
    
    # Menyimpan file session auth.json
    context.storage_state(path="auth.json")
    browser.close()
    print("Sesi login berhasil disimpan ke file 'auth.json'!")