# python-api-client

Python ile sıfırdan yazılmış, `requests` tabanlı bir API istemcisi: class yapısı, GET/POST, hata yönetimi (try/except) ve retry mantığı.

## Hakkında

Bu repo, bir API'ye nasıl bağlanılacağını, veri çekip gönderileceğini ve gerçek dünyaya dayanıklı bir istemcinin (client) nasıl yazılacağını adım adım gösteren bir öğrenme projesidir. Test API'si olarak [JSONPlaceholder](https://jsonplaceholder.typicode.com) kullanılmıştır.

İlgili Medium yazısı: *(https://medium.com/@ibrahimbarankilicc/1b5bd48e8a7b)*

## Neler Var?

- **Class yapısı** — API ile ilgili her şeyi (`BASE_URL`, ayarlar, metotlar) tek kutuda toplayan `UserClient` sınıfı
- **`__init__` ve session** — nesne kurulumu ve `requests.Session()` ile verimli bağlantı yönetimi
- **GET** — `get_user`, `get_all_users` metotlarıyla veri çekme
- **POST** — `create_user` metoduyla payload göndererek veri oluşturma
- **try/except** — internet kopması, sunucu hatası gibi durumlarda çökmeyen kod
- **retry** — geçici hatalarda belirli sayıda tekrar deneme
- **pandas** — çekilen veriyi `json_normalize` ile düzleştirip analiz etme

## Kurulum

```bash
pip install requests pandas
```

## Kullanım

```python
client = UserClient(api_key="test123")

# Tek bir kullanıcıyı çek
user = client.get_user(1)

# Tüm kullanıcıları çek
users = client.get_all_users()

# Yeni kullanıcı oluştur
new_user = client.create_user("Ali Veli", "ali@example.com")
```

## Gereksinimler

- Python 3.8+
- requests
- pandas
