import urllib.request
import json
import time
import random

TELEGRAM_BOT_TOKEN = "8885666495:AAHG8OPjLPp1LdYO13xp7pW8dRpM2StTU-U"
TELEGRAM_CHAT_ID = "8766074185"

# BIST Hisseleri, BYF'ler ve Kuruşlu Hisseler (100+ Enstrüman)
TUM_BIST_LISTESI = [
    # Ana Hisseler
    "THYAO.IS", "GARAN.IS", "EREGL.IS", "ASELS.IS", "SISE.IS", "KCHOL.IS", "TUPRS.IS", "AKBNK.IS",
    "YKBNK.IS", "SAHOL.IS", "BIMAS.IS", "ISCTR.IS", "PETKM.IS", "EKGYO.IS", "HALKB.IS", "VAKBN.IS",
    "HEKTS.IS", "SASA.IS", "KONTR.IS", "SMRTG.IS", "ODAS.IS", "GUBRF.IS", "ASTOR.IS", "ALARK.IS",
    "TOASO.IS", "FROTO.IS", "TTKOM.IS", "TCELL.IS", "PGSUS.IS", "KOZAL.IS", "KOZAA.IS", "ENKAI.IS",
    "OYAKC.IS", "CIMSA.IS", "DOHOL.IS", "ARCLK.IS", "TAVHL.IS", "SOKM.IS", "MAVI.IS", "BCHIP.IS",
    "KCAER.IS", "CANTE.IS", "GESAN.IS", "EUPWR.IS", "SDTTR.IS", "MIATK.IS", "REEDR.IS", "BOBET.IS",
    # Borsa Yatırım Fonları (BYF / ETF)
    "ZGOLD.IS", "USDTR.IS", "GMSTR.IS", "GLDTR.IS", "ZREIT.IS", "Z30EA.IS", "ZUSDE.IS",
    # Kuruşlu ve Düşük Fiyatlı Hisseler
    "IEYHO.IS", "METRO.IS", "EUHOL.IS", "AVOD.IS", "NTHOL.IS", "TMSN.IS", "MERSN.IS", "DAGHL.IS",
    "GLRYH.IS", "SAMAT.IS", "TSPOR.IS", "BJKAS.IS", "GSRAY.IS", "FENER.IS", "IHGVT.IS", "IHYAY.IS",
    "USAK.IS", "KRTEK.IS", "SKBNK.IS", "TSKB.IS", "CEMAS.IS", "ICBCT.IS", "VKGYO.IS", "PEKGY.IS",
    "KLGYO.IS", "HLGYO.IS", "MNGYO.IS", "DZGYO.IS", "ISGYO.IS", "SNGYO.IS", "OZGYO.IS", "TDGYO.IS"
]

SON_GONDERILENLER = []

def telegram_mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mesaj,
        "parse_mode": "Markdown"
    }).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Telegram Gönderim Hatası: {e}")
        return None

def detayli_hisse_fon_analiz(kod):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{kod}?range=1mo&interval=1d"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode())
            fiyatlar = res['chart']['result'][0]['indicators']['quote'][0]['close']
            hacimler = res['chart']['result'][0]['indicators']['quote'][0]['volume']
            
            fiyatlar = [f for f in fiyatlar if f is not None]
            hacimler = [h for h in hacimler if h is not None]
            
            if not fiyatlar or len(fiyatlar) < 14:
                return None

            son_fiyat = fiyatlar[-1]
            onceki_kapanis = fiyatlar[-2]
            gunluk_degisim = ((son_fiyat - onceki_kapanis) / onceki_kapanis) * 100
            
            ort_20 = sum(fiyatlar) / len(fiyatlar)
            en_yuksek = max(fiyatlar)
            en_dusuk = min(fiyatlar)
            
            # --- 14 Günlük RSI Hesaplama ---
            farklar = [fiyatlar[i] - fiyatlar[i-1] for i in range(1, len(fiyatlar))]
            kazanclar = [f for f in farklar if f > 0]
            kayiplar = [-f for f in farklar if f < 0]
            
            ort_kazanc = sum(kazanclar) / 14 if kazanclar else 0.001
            ort_kayip = sum(kayiplar) / 14 if kayiplar else 0.001
            
            rs = ort_kazanc / ort_kayip
            rsi = 100 - (100 / (1 + rs))

            # --- Gelişmiş Skorlama ve Risk Yönetimi ---
            skor = 50
            if son_fiyat > ort_20: skor += 15
            if gunluk_degisim > 0: skor += 10
            if hacimler and hacimler[-1] > (sum(hacimler)/len(hacimler)): skor += 15
            if son_fiyat >= en_yuksek * 0.95: skor += 10

            # Stop-Loss (Kayıp Önleme) Seviyesi (%3 Zarar Kes)
            stop_loss = son_fiyat * 0.97
            hedef_fiyat = son_fiyat * 1.08 # %8 Tahmini Kâr Hedefi

            # --- Tahmini Zaman / Vade Penceresi Hesaplama ---
            if rsi < 35 ve gunluk_degisim > 1:
                tahmini_vade = "⚡ **Çok Kısa Vade (1 - 3 Gün İçinde)**"
            elif rsi >= 35 ve rsi <= 60 ve son_fiyat > ort_20:
                tahmini_vade = "📈 **Kısa/Orta Vade (3 - 10 Gün İçinde)**"
            elif rsi > 60 ve rsi <= 70:
                tahmini_vade = "⏳ **Orta Vade (1 - 3 Hafta İçinde)**"
            else:
                tahmini_vade = "⚠️ **Belirsiz / Riski Yüksek (Beklemede)**"

            # --- Risk & Düşüş Analizi ---
            if rsi > 70:
                dusse_risk_mesaji = "⚠️ **YÜKSEK DÜŞÜŞ RİSKİ!** (Aşırı Alımda, Kâr Satışı Gelebilir)"
                skor -= 20
            elif son_fiyat < ort_20 and gunluk_degisim < -2:
                dusse_risk_mesaji = "🔴 **DÜŞÜŞ TRENDİ!** (Destek Kırılabilir, Bulaşma)"
                skor -= 25
            else:
                dusse_risk_mesaji = "🟢 **Düşüş Riski Düşük** (Trend Stabil)"

            # Tür Tespiti
            if "GOLD" in kod or "TR" in kod or "Z30" in kod or "ZUS" in kod:
                tur = "Borsa Fonu (ETF)"
            elif son_fiyat < 10.0:
                tur = "Kuruşlu / Ucuz Hisse"
            else:
                tur = "Ana Hisse Senedi"

            if skor >= 70:
                durum = "🟢 **YÜKSEK POTANSİYEL (GÜÇLÜ AL)**"
            elif skor >= 50:
                durum = "🟡 **ORTA SEVİYE (NÖTR / İZLEME)**"
            else:
                durum = "🔴 **DÜŞÜK SEVİYE (SAT / BEKLE)**"

            fiyat_format = f"{son_fiyat:.4f}" if son_fiyat < 5.0 else f"{son_fiyat:.2f}"
            stop_format = f"{stop_loss:.4f}" if son_fiyat < 5.0 else f"{stop_loss:.2f}"
            hedef_format = f"{hedef_fiyat:.4f}" if son_fiyat < 5.0 else f"{hedef_fiyat:.2f}"

            return (
                f"🧠 **Gelişmiş BIST Analiz Raporu**\n"
                f"📌 **Enstrüman:** `{kod.replace('.IS', '')}` ({tur})\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"💰 **Anlık Fiyat:** {fiyat_format} TL\n"
                f"📈 **Günlük Değişim:** %{gunluk_degisim:+.2f}\n"
                f"📊 **20 Günlük Ort.:** {ort_20:.2f} TL\n"
                f"⚡ **RSI Göstergesi:** {rsi:.1f} / 100\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"🎯 **Sinyal:** {durum}\n"
                f"🎲 **Yükseliş İhtimali:** %{skor}\n"
                f"⏱ **Tahmini Hareket Vadesi:**\n{tahmini_vade}\n\n"
                f"🛡 **Risk Yönetimi (Kayıp Önleme):**\n"
                f"🛑 **Stop-Loss (Zarar Kes):** {stop_format} TL\n"
                f"🎯 **Tahmini Hedef Fiyat:** {hedef_format} TL\n"
                f"⚠️ **Düşüş İhtimali:** {dusse_risk_mesaji}\n"
                f"━━━━━━━━━━━━━━━━━━━\n"
                f"⏰ **Durum:** Canlı Veri"
            )
    except Exception as e:
        print(f"Veri Çekme Hatası ({kod}): {e}")
        return None

if __name__ == "__main__":
    BEKLEME_SURESI = 300  # 5 Dakikada bir çalışır
    
    while True:
        kullanilabilir_liste = [h for h in TUM_BIST_LISTESI if h not in SON_GONDERILENLER]
        
        if not kullanilabilir_liste:
            SON_GONDERILENLER.clear()
            kullanilabilir_liste = TUM_BIST_LISTESI
            
        secilen = random.choice(kullanilabilir_liste)
        rapor = detayli_hisse_fon_analiz(secilen)
        
        if rapor:
            telegram_mesaj_gonder(rapor)
            SON_GONDERILENLER.append(secilen)
            if len(SON_GONDERILENLER) > 30:
                SON_GONDERILENLER.pop(0)
                
        time.sleep(BEKLEME_SURESI)
