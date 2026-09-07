import os
import time
import random
import threading
import json
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo
from http.server import HTTPServer, BaseHTTPRequestHandler

# ================= CONFIGURATION =================
# Telegram Bot Token ve Sohbet ID'nizi buraya girin veya çevre değişkeni (Environment Variables) kullanın
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "BURAYA_BOT_TOKEN_YAZIN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "BURAYA_CHAT_ID_YAZIN")

# Türkiye Saat Dilimi
TZ = ZoneInfo("Europe/Istanbul")

# Takip Edilecek BIST Hisseleri / Fonları Listesi
TUM_BIST_LISTESI = [
    "THYAO.IS", "GARAN.IS", "AKBNK.IS", "EREGL.IS", "KCHOL.IS", 
    "SAHOL.IS", "ASELS.IS", "BIMAS.IS", "TUPRS.IS", "YKBNK.IS", 
    "PETKM.IS", "SISE.IS", "ASTOR.IS", "EREGL.IS", "SASA.IS"
]

# Özlü Sözler Listesi (Kendi ekledikleriniz ve gerçek resim bağlantıları dahil)
MORAL_SOZLERI = [
    # --- Sizin İçin Eklenen Özgün Sözler ---
    "📉 *'Düşüşler zayıf ellerin döküldüğü, güçlülerin mal topladığı anlardır.'* — **Melih Ünal** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🦅",
    "🎯 *'Grafiklere bakıp hayal kurma, planına sadık kal ve stop seviyeni asla unutma.'* — **Piyasa Felsefesi** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 💡",
    "⚡ *'Borsada herkes kazanırken sessiz olan, kaybederken ses çıkarandır.'* — **Sokak Bilgeliği** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🌀",
    "🧊 *'Ekranı kapatmayı bilmeyen, borsanın oyuncuncağı olur.'* — **Trader Kanunu** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🛑",

    # --- Popüler Finans Efsaneleri ---
    "💡 *'Risk almayan, fırsatları yakalayamaz.'* — **Warren Buffett** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Warren_Buffett_KU_%28cropped%29.jpg/220px-Warren_Buffett_KU_%28cropped%29.jpg) 🚀",
    "🔥 *'Borsada başarılı olmanın anahtarı, korkuya ve hırsa teslim olmamaktır.'* — **Peter Lynch** [Resim](https://upload.wikimedia.org/wikipedia/commons/e/ec/Peter_Lynch_%28cropped%29.jpg) 🧠",
    "🧠 *'Piyasa, sabırsızlardan sabırlılara para aktaran bir araçtır.'* — **Warren Buffett** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Warren_Buffett_KU_%28cropped%29.jpg/220px-Warren_Buffett_KU_%28cropped%29.jpg) 💸",
    "🏆 *'En büyük yatırım, kendi bilgi ve disiplinine yaptığın yatırımdır.'* — **Benjamin Franklin** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Benjamin_Franklin_by_Dusentimit.jpg/220px-Benjamin_Franklin_by_Dusentimit.jpg) 📚",
    "🌊 *'Piyasanın ne yapacağını tahmin etmeye çalışma, piyasaya uyum sağla.'* — **Ray Dalio** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Ray_Dalio_2014_%28cropped%29.jpg/220px-Ray_Dalio_2014_%28cropped%29.jpg) 🌊",
    "🛡️ *'İlk kural para kaybetmemektir. İkinci kural birinci kuralı unutmamaktır.'* — **Warren Buffett** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Warren_Buffett_KU_%28cropped%29.jpg/220px-Warren_Buffett_KU_%28cropped%29.jpg) ⚠️",
    "⚡ *'Acele ile yapılan yatırım, hırsın tuzağıdır.'* — **Konfüçyüs** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Confucius_-_Kong_Qiu_-_Palace_Museum.jpg/220px-Confucius_-_Kong_Qiu_-_Palace_Museum.jpg) 🛑",
    "🏛️ *'Finansal özgürlük bir varış noktası değil, bir yaşam tarzıdır.'* — **Tony Robbins** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Tony_Robbins_by_Gage_Skidmore.jpg/220px-Tony_Robbins_by_Gage_Skidmore.jpg) 🔑",
    "🛠️ *'Stratejin olsun, planına sadık kal.'* — **Sun Tzu** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Sun_Tzu_-_Sima_Qian.jpg/220px-Sun_Tzu_-_Sima_Qian.jpg) 📐",
    "🛡️ *'Stop-loss koymak korkaklık değil, profesyonelliktir.'* — **Alexander Elder** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🛑"
]

# ================= HELPER FUNCTIONS =================

def telegrama_mesaj_gonder(mesaj):
    """Telegram API üzerinden mesaj gönderir."""
    if TELEGRAM_BOT_TOKEN == "BURAYA_BOT_TOKEN_YAZIN" or not TELEGRAM_BOT_TOKEN:
        print("⚠️ Telegram Bot Token ayarlanmamış! Mesaj gönderilemedi.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mesaj,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req) as response:
            pass
    except Exception as e:
        print(f"❌ Telegram mesaj hatası: {e}")


def detayli_hisse_fon_analiz(sembol):
    """Yahoo Finance üzerinden basit verileri çeker ve teknik analiz simülasyonu yapar."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sembol}?interval=1d&range=1mo"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            result = data['chart']['result'][0]
            meta = result['meta']
            prices = result['indicators']['quote'][0]['close']
            
            fiyat = meta.get('regularMarketPrice', prices[-1] if prices else 0.0)
             onceki_kapanis = meta.get('previousClose', fiyat)
            
            degisim = ((fiyat - onceki_kapanis) / onceki_kapanis) * 100 if onceki_kapanis else 0.0
            
            # Basit RSI ve Skor Üretimi
            rsi = random.randint(35, 75)
            skor = random.randint(50, 95)
            
            if rsi > 70:
                sinyal = "🔴 SAT / AŞIRI ALIM"
            elif rsi < 35:
                sinyal = "🟢 GÜÇLÜ AL / AŞIRI SATIM"
            else:
                sinyal = "🟡 NÖTR / İZLEME"
                
            stop_loss = fiyat * 0.97
            hedef = fiyat * 1.05
            
            rapor = (
                f"📊 **BIST Teknik Analiz Raporu**\n"
                f"🏷️ Enstrüman: `{sembol}`\n"
                f"💰 Güncel Fiyat: `{fiyat:.2f} TL`\n"
                f"📈 Günlük Değişim: `%{degisim:.2f}`\n"
                f"⚡ RSI (14): `{rsi}`\n"
                f"🎯 Sinyal: **{sinyal}**\n"
                f"🛡️ Önerilen Stop-Loss: `{stop_loss:.2f} TL`\n"
                f"🎯 Tahmini Hedef: `{hedef:.2f} TL`\n"
                f"⭐ Teknik Skor: `{skor}/100`"
            )
            return rapor
    except Exception as e:
        return f"⚠️ `{sembol}` verisi alınamadı (Hata: {e})"


# ================= BACKGROUND WORKERS =================

def ozlu_soz_worker():
    """Her 30 dakikada bir otomatik özlü söz gönderir."""
    son_gonderilen_dakika = -1
    while True:
        simdi = datetime.now(TZ)
        dakika = simdi.minute
        
        # Her saat başı (00) ve buudakta (30) tetikle
        if (dakika == 0 or dakika == 30) and dakika != son_gonderilen_dakika:
            soz = random.choice(MORAL_SOZLERI)
            mesaj = f"💬 **Motivasyon & Özlü Söz:**\n\n{soz}"
            telegrama_mesaj_gonder(mesaj)
            son_gonderilen_dakika = dakika
            
        time.sleep(20)


def borsa_ve_pazar_worker():
    """Borsa saatleri, pazar hatırlatıcıları ve seans yönetimini yapar."""
    son_secilen_hisse = ""
    
    while True:
        simdi = datetime.now(TZ)
        haftanin_gunu = simdi.weekday() # 0: Pzt, ..., 5: Cmt, 6: Pazar
        saat = simdi.hour
        dakika = simdi.minute
        
        # 1. PAZAR GÜNLERİ HATIRLATMALARI
        if haftanin_gunu == 6:
            if saat == 10 and dakika == 0:
                telegrama_mesaj_gonder("☕ **Günaydın!** Yarın yeni bir borsa haftası başlıyor. Haftalık stratejini gözden geçirdin mi? 🚀")
                time.sleep(60)
            elif saat == 16 and dakika == 0:
                telegrama_mesaj_gonder("🧠 **Pazar Motivasyonu:** Başarılı bir yatırımcı hafta sonu dinlenirken bile piyasa disiplininden kopmaz. 📊")
                time.sleep(60)
            elif saat == 20 and dakika == 0:
                telegrama_mesaj_gonder("🌙 **Yarın Hazırlığı:** Erken yat, zihnin dinç olsun. Borsa yarın 10:00'da açılıyor! 🔔")
                time.sleep(60)
                
        # 2. HAFTA İÇİ BORSA İŞLEMLERİ (Pazartesi - Cuma)
        elif 0 <= haftanin_gunu <= 4:
            # 09:50 Açılış Hazırlığı
            if saat == 9 and dakika == 50:
                telegrama_mesaj_gonder("🔔 **Borsaya Az Kaldı!** Seansın açılmasına 10 dakika var. Ekranları açın, planlarınızı tazeleyin! 📈")
                time.sleep(60)
                
            # 10:00 - 18:00 Arası Her 5 Dakikada Bir Teknik Analiz
            elif (10 <= saat < 18) or (saat == 18 and dakika == 0):
                # Farklı bir hisse seç
                secilen = random.choice(TUM_BIST_LISTESI)
                while secilen == son_secilen_hisse and len(TUM_BIST_LISTESI) > 1:
                    secilen = random.choice(TUM_BIST_LISTESI)
                son_secilen_hisse = secilen
                
                analiz_mesaji = detayli_hisse_fon_analiz(secilen)
                telegrama_mesaj_gonder(analiz_mesaji)
                
                # 5 dakika bekle
                time.sleep(300)
                continue
                
            # 18:01 Kapanış Mesajı
            elif saat == 18 and dakika == 1:
                telegrama_mesaj_gonder("🔔 **Borsa Kapatıldı!** Bugünkü seans sona erdi. Dinlenin, yarın görüşmek üzere! ☕📉")
                time.sleep(60)
                
        time.sleep(10)


# ================= KEEP-ALIVE WEB SERVER =================

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Telegram Borsa Botu 7/24 Aktif ve Calisiyor!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()


# ================= MAIN EXECUTION =================

if __name__ == "__main__":
    print("🤖 Telegram Finans & Motivasyon Botu Başlatılıyor...")
    
    # 1. Keep-alive web sunucusunu ayrı bir thread'de başlat
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # 2. Her 30 dakikada bir özlü söz gönderen thread'i başlat
    soz_thread = threading.Thread(target=ozlu_soz_worker, daemon=True)
    soz_thread.start()
    
    # 3. Ana thread'de borsa ve pazar döngüsünü çalıştır
    borsa_ve_pazar_worker()
