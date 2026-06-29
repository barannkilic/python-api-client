"""requests'i içeri al.
Sınıfın bir adı olsun (ne istersen — UserClient, DataClient, sana kalmış).
Sınıfın içinde sabit bir adres bulunsun: https://jsonplaceholder.typicode.com. Bu sabit, her nesnede aynı olacak (yani __init__ dışında, sınıfın tepesinde duracak).
Nesne ilk oluşturulduğunda çalışan kurulum bölümü olsun. Bu bölüm:

Dışarıdan bir api_key alıp nesneye kaydetsin.
Bir session kursun ve nesneye kaydetsin (yukarıda anlattığım gibi).


get_user adında bir metod olsun. Bu metod dışarıdan bir user_id alsın ve:

O kullanıcıyı session üzerinden çeksin. Adres şu yapıda olacak: adres/users/user_id.
Eğer durum kodu 200 ise gelen veriyi (json) döndürsün.
Değilse None döndürsün.


Sınıfın dışında: bir nesne üret (bir api_key ver, herhangi bir şey olabilir mesela "test123"), sonra get_user ile 1 numaralı kullanıcıyı çekip ekrana yazdır."""




"""
try / except → "riskli kodu dene, çökmek yerine hatayı yakala." İnternet koptuğunda program çökmesin, hatayı yakalayıp devam etsin.
retry → "bir denemede olmazsa, birkaç kez daha dene." Çoğu hata geçicidir (sunucu o an yoğun olabilir), tekrar deneyince düzelir. 
"""




"""
for i in range(retries):        # 3 kez dene
    try:
        işi yap
        return sonuç            # BAŞARI → çık (döngü biter, kalan denemeleri yapma)
    except:
        bekle (time.sleep)      # HATA → bekle, return YOK, döngü devam etsin
return None                     # 3 deneme de bitti → artık pes et

1. denemede başarılı → try içindeki return çalışır, çıkar. Hiç beklemez.
1. deneme hata, 2. başarılı → 1'de except'e düşer bekler, 2'de try başarılı olur çıkar.
3 deneme de hata → her seferinde except'e düşer bekler, döngü biter, en alttaki return None çalışır.
"""

import requests
import json   # cıktıyı temız almak ıcın 
import time   # retry için bekleme süresi


class UserClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, api_key):
        self.api_key = api_key
        self.session = requests.Session()

    def get_user(self, user_id, retries=3, wait_time=2):

        for i in range(retries):
            try:
                url = f"{self.BASE_URL}/users/{user_id}"

                response = self.session.get(url)

                if response.status_code == 200:
                    return response.json()

            except Exception as e:    # requests.RequestException: sadece requests ile ilgili hataları yakalar, Exception ise tüm hataları yakalar
                print(f"Deneme {i+1}/{retries} Hata oluştu: {e}")
                time.sleep(wait_time)  # Hata olursa bekle ve tekrar dene
        return None  # Tüm denemeler başarısız olursa None döndür
        

    def create_user(self, name, email, retries=3, wait_time=2):
        payload = {
                "name": name,
                "email": email
            }
        for i in range(retries):
            try:
                url = f"{self.BASE_URL}/users"

                response = self.session.post(url, json=payload)

                if response.status_code == 201:
                    return response.json()
                
            except Exception as e:
                print(f"Deneme {i+1}/{retries} Hata oluştu: {e}")
                time.sleep(wait_time)  # Hata olursa bekle ve tekrar dene
        return None

        

# Sınıfın dışında bir nesne üretelim ve get_user metodunu kullanalım
client = UserClient(api_key="test123")

user = client.get_user(1)
print(json.dumps(user, indent=4))  # Cıktıyı temız almak ıcın json.dumps kullandık
# veride türkçe karakter olursa  "ensure_ascii=False" parametresini de ekleyebilirsin

if user: # veri geldiyse ekrana yazdır, gelmediyse kullanıcı bulunamadı yazdır
    # ornek cıktılar
    print("-------------------")
    print(user['name'])  # Kullanıcının adını yazdır
    print(user['email'])  # Kullanıcının emailini yazdır
    print(user["phone"]) # Kullanıcının telefonunu yazdır


    print("-------------------")
    print(f"User Name: {user["name"]}")
    print(f"User Email: {user["email"]}")
    print(f"User Phone: {user["phone"]}")
else: 
    print("Kullanıcı bulunamadı.")



print("-------------------")
create_response = client.create_user(name="John Doe", email="john.doe@example.com")
if create_response:  # veri geldiyse ekrana yazdır, gelmediyse kullanıcı oluşturulamadı yazdır
    print("Kullanıcı başarıyla oluşturuldu:")
    print(json.dumps(create_response, indent=4))
else:
    print("Kullanıcı oluşturulamadı.")
