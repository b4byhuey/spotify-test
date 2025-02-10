import requests
import random
import time
import threading

# Konfigurasi otomatis
DOMAIN = "@babyhuey.my.id"
SANDI = "@B4byhuey"
CAPSOLVER_KEY = "CAP-4FB9D4AEFD7475E11DD56BB9585E85C26C41AB61A6485A8D4C4B4A39D2BE9F87"
API_SPOTIFY = "142b583129b2df829de3656f9eb484e6"
AMOUNT = 20  # Ubah jumlah akun yang ingin dibuat

class Spotify:
    def __init__(self):
        self.api = requests.Session()

    def user_data(self):
        return self.api.get("http://api.suhu.my.id/v2/faker", headers={"User-Agent": "PanelNewbie/0.2 (Linux; rdhoni;) Termux/0.2"}).json()
    
    def create(self, ua, nama, email, sandi, ttl, gender):
        return self.api.post("https://spclient.wg.spotify.com/signup/public/v2/account/create", json={
            "account_details": {
                "birthdate": ttl,
                "consent_flags": {"eula_agreed": True, "send_email": False, "third_party_email": False},
                "display_name": nama,
                "email_and_password_identifier": {"email": email, "password": sandi},
                "gender": gender
            },
            "client_info": {"api_key": API_SPOTIFY, "app_version": "v2", "capabilities": [1]},
            "tracking": {"creation_flow": "", "creation_point": "", "referrer": ""}
        }, headers={"User-Agent": ua, "Content-Type": "application/json"})

class UserThread:
    def main(self):
        spotify = Spotify()
        generate_data = spotify.user_data()
        ua = generate_data["browser"]["user_agent"]
        nama = generate_data["email"].split("@")[0]
        gender = random.randint(1, 4)
        email = f'{nama.replace(" ", "").lower()}{DOMAIN}'
        ttl = f"{random.randint(1990, 2002)}-{random.randint(10, 12)}-{random.randint(10, 28)}"
        
        signup = spotify.create(ua, nama, email, SANDI, ttl, gender)
        if "login_token" in signup.text:
            print(f"Created: {email}")
            with open("account.txt", "a") as f:
                f.write(f"Email: {email} | Sandi: {SANDI}\n")
        else:
            print("Failed to create account or captcha detected.")
    
    def createThread(self):
        threads = []
        for _ in range(AMOUNT):
            thread = threading.Thread(target=self.main)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    UserThread().createThread()
