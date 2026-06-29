import requests
import json
import time
import pandas as pd
import matplotlib.pyplot as plt


class UserClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self,api_key):
        self.api_key = api_key
        self.session = requests.Session()


    def get_user(self, user_id, retries=3 , wait_time=2):

        for i in range(retries):
            try:
                url = f"{self.BASE_URL}/users/{user_id}"

                response = self.session.get(url)

                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"Deneme {i+1}/{retries} Hata oluştu: {e}")
                time.sleep(wait_time)  # Hata olursa bekle ve tekrar dene
        return None
    
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
    

    def get_all_users(self, retries=3, wait_time=2):

        for i in range(retries):
            try:
                url = f"{self.BASE_URL}/users"
                response = self.session.get(url)

                if response.status_code == 200:
                    return response.json()
                
            except Exception as e:
                print(f"Deneme {i+1}/{retries} Hata oluştu: {e}")
                time.sleep(wait_time)  # Hata olursa bekle ve tekrar dene
        return None
    


client = UserClient(api_key="test123")
users = client.get_all_users()

print(type(users)) # <class'list'> döner, çünkü tüm kullanıcılar bir liste olarak gelir
print(f"Toplam kullanıcı sayısı: {len(users)}")
print(json.dumps(users, indent=4))  # Cıktıyı temız almak ıcın json.dumps kullandık


# Pandas DataFrame'e çevirip, kullanıcıların isimlerini ve email adreslerini yazdıralım
# if users:  # veri geldiyse ekrana yazdır, gelmediyse kullanıcılar alınamadı yazdır
if users:
    df = pd.DataFrame(users)
    print(df.head())  # ilk 5 satırı yazdır
    print(df[['name', 'email']])  # sadece isim ve email sütunlarını yazdır
else:
    print("Kullanıcılar alınamadı.")


## sutunlarda içiçe sozlukler var onlarıda ayrı sutunlara ayırmak için 
# json_normalize kullanabiliriz

if users:
    df_normalized = pd.json_normalize(users)
    print(df_normalized.head())  # ilk 5 satırı yazdır
    print(df_normalized[['name', 'email', 'address.street', 'address.city']])  # sadece isim, email ve adres bilgilerini yazdır

else:
    print("Kullanıcılar alınamadı.")



# GOREVLER
print("----------GOREVLER---------")

# Gorev 1:address.city sütununa bak ve her şehirde kaç kullanıcı olduğunu say. 
print("----------GOREV 1---------")
df_city_count = df_normalized["address.city"].value_counts()
print(df_city_count)

# Gorev 2: Kullanıcıları name'e göre alfabetik sırala. Sadece name ve email sütunlarını göster.
print("----------GOREV 2---------")

df_sorted_name = df_normalized.sort_values("name")[["name", "email"]]
print(df_sorted_name)


# Gorev 3: id'si 5'ten küçük olan kullanıcıları filtrele ve sadece name ve email sütunlarını göster.
print("----------GOREV 3---------")

df_filtred_id = df_normalized[df_normalized["id"] > 5][["name", "email"]]
print(df_filtred_id)


# Gorev 4: Sehir bazli grafik ciz. Her sehirde kac kullanici var onu goster. (matplotlib veya seaborn kullanabilirsin)

plt.figure(figsize=(10, 6))
df_city_count.plot(kind="bar")

plt.title("Şehir Bazlı Kullanıcı Sayısı")
plt.xlabel("Şehir")
plt.ylabel("Kullanıcı Sayısı")
plt.tight_layout()        # uzun şehir isimleri taşmasın
plt.show()