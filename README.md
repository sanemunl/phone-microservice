# 📱 Phone Microservice (Flask + MySQL + Docker + Nginx)

Bu proje; telefon numarası doğrulama, kullanıcı kaydı oluşturma, kayıt listeleme ve çeşitli kurallara göre telefon sayılarını hesaplama amaçlı geliştirilmiş bir mikroservis mimarisi örneğidir.

Projede:

- **Flask API (Python)**
- **MySQL veritabanı**
- **Nginx frontend**
- **Docker Compose ile container orkestrasyonu**

kullanılmıştır.

---

## 🚀 Özellikler

### ✔ Telefon Doğrulama
- 6 haneli telefon numarası
- Format kontrolü (sadece rakam)
- Matematiksel kurallar:
  - En az 1 tane sıfır olmayan rakam olmalı
  - İlk 3 hanenin toplamı = Son 3 hanenin toplamı
  - Tek indeks toplamı = Çift indeks toplamı

### ✔ Kullanıcı Kaydı
- İsim, e-posta, telefon
- Telefon doğrulanmadan kayıt yapılamaz
- Aynı telefon ile ikinci kez kayıt engellenir

### ✔ API + Frontend + Veritabanı tamamen Docker ile çalışır

---

## 🗂 Proje Yapısı

phone-microservice/
│
├── api/
│ ├── app.py
│ ├── db.py
│ ├── validators.py
│ ├── requirements.txt
│
├── db/
│ └── init.sql
│
├── frontend/
│ ├── index.html
│ └── script.js
│
├── docker-compose.yml
└── README.md

yaml
Kodu kopyala

---

## 🧰 Kullanılan Teknolojiler

| Teknoloji | Açıklama |
|----------|----------|
| Python 3.10 | API geliştirme |
| Flask | Web framework |
| Flask-CORS | CORS yönetimi |
| MySQL 8 | Veritabanı |
| Docker Compose | Servis yönetimi |
| Nginx | Frontend sunucusu |
| JavaScript | Frontend istekleri |

---

## ▶ Projeyi Çalıştırma

## Depoyu klonla
git clone https://github.com/KULLANICIADIN/phone-microservice.git
cd phone-microservice
2) Docker Compose ile projeyi başlat
docker compose up --build

## Uygulama adresleri
Servis	URL
Frontend	http://localhost:8080
API	http://localhost:3000
MySQL	localhost:3306


## 📌 API Uç Noktaları
🔸 Telefon Doğrulama
POST /api/phone/validate

{
  "number": "123321"
}

🔸 Kayıt Oluşturma
POST /api/registration
{
  "name": "Ali",
  "email": "ali@example.com",
  "phone": "123321"
}

Yanıt:
{
  "status": "accepted",
  "message": "Kayıt oluşturuldu.",
  "data": {
    "name": "Ali",
    "email": "ali@example.com",
    "phone": "123321"
  }
  
}
🔸 Kayıt Listeleme
GET /api/registrations

🔸 Geçerli Telefon Sayısı
GET /api/phone/count

## 💾 Veritabanı Yapısı
db/init.sql:

sql
Kodu kopyala
CREATE TABLE registrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(6) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
### 🐳 Docker Servisleri
yml
Kodu kopyala
services:
  api:
    build: ./api
    ports:
      - "3000:3000"

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
    ports:
      - "3306:3306"

  frontend:
    image: nginx:alpine
    volumes:
      - ./frontend:/usr/share/nginx/html
    ports:
      - "8080:80"

      
###  Yaygın Hatalar ve Çözümleri
❌ Failed to fetch
Çözüm: API çalışmıyordur → yeniden build et
docker compose down
docker compose up --build

❌ ModuleNotFoundError: flask_cors
Çözüm: requirements.txt eksik → API imajını yeniden oluştur

❌ MySQL bağlantı hatası
Çözüm: db servisi geç başlıyor olabilir → tekrar başlat
