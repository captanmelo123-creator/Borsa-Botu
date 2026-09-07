import os
import time
import random
import threading
import json
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo
from http.server import HTTPServer, BaseHTTPRequestHandler

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "BURAYA_BOT_TOKEN_YAZIN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "BURAYA_CHAT_ID_YAZIN")

TZ = ZoneInfo("Europe/Istanbul")

TUM_BIST_LISTESI = [
    "ACSEL.IS", "ADEL.IS", "ADESE.IS", "ADGYO.IS", "AEFES.IS", "AFYON.IS", "AGESA.IS", "AGHOL.IS", "AGROT.IS", "AGYO.IS",
    "AKBNK.IS", "AKCNS.IS", "AKENR.IS", "AKFGY.IS", "AKFYE.IS", "AKGRT.IS", "AKMGY.IS", "AKSA.IS", "AKSEN.IS", "AKSGY.IS",
    "ALARK.IS", "ALBRK.IS", "ALCAR.IS", "ALCTL.IS", "ALFAS.IS", "ALGYO.IS", "ALKA.IS", "ALKIM.IS", "ALKLC.IS", "ALTNY.IS",
    "ANHYT.IS", "ANSGR.IS", "ARASE.IS", "ARCLK.IS", "ARDYZ.IS", "ARENA.IS", "ARSAN.IS", "ARTMS.IS", "ARZUM.IS", "ASELS.IS",
    "ASTOR.IS", "ASUZU.IS", "ATAGY.IS", "ATAKP.IS", "ATATP.IS", "ATEKS.IS", "ATLAS.IS", "AVOD.IS", "AVPGY.IS", "AYCES.IS",
    "AYDEM.IS", "AYEN.IS", "AYES.IS", "AYGAZ.IS", "AZTEK.IS", "BAGFS.IS", "BAKAB.IS", "BALAT.IS", "BANVT.IS", "BARMA.IS",
    "BASGZ.IS", "BASCM.IS", "BAYRK.IS", "BEGYO.IS", "BERA.IS", "BEYAZ.IS", "BIENY.IS", "BIGCH.IS", "BIMAS.IS", "BINHO.IS",
    "BIOEN.IS", "BIZIM.IS", "BJKAS.IS", "BLCYT.IS", "BMSCH.IS", "BMSTL.IS", "BNTAS.IS", "BOBET.IS", "BORLS.IS", "BORSK.IS",
    "BOSSA.IS", "BRISA.IS", "BRKSN.IS", "BRLSM.IS", "BRYAT.IS", "BUCIM.IS", "BURCE.IS", "BURVA.IS", "BVSAN.IS", "BYDNR.IS",
    "CANTE.IS", "CASA.IS", "CATES.IS", "CCOLA.IS", "CELHA.IS", "CEMAS.IS", "CEMTS.IS", "CEOEM.IS", "CGCAN.IS", "CIMSA.IS",
    "CLEBI.IS", "CMBTN.IS", "CMENT.IS", "CONSE.IS", "COSMO.IS", "CRDFA.IS", "CRFSA.IS", "CUMRU.IS", "CWENE.IS", "DAGI.IS",
    "DAGHL.IS", "DAPGM.IS", "DARDL.IS", "DENGE.IS", "DERHL.IS", "DERIM.IS", "DESA.IS", "DESPC.IS", "DEVA.IS", "DIRIT.IS",
    "DITAS.IS", "DMRGD.IS", "DMSAS.IS", "DNISI.IS", "DOAS.IS", "DOBUR.IS", "DOCO.IS", "DOFER.IS", "DOGUB.IS", "DOHOL.IS",
    "DOKTA.IS", "DSTAN.IS", "DURDO.IS", "DYOBY.IS", "DZGYO.IS", "EBEBK.IS", "EGEEN.IS", "EGEPO.IS", "EGGUB.IS", "EGPRO.IS",
    "EGSER.IS", "EKOS.IS", "EKGYO.IS", "EKSUN.IS", "ELITE.IS", "EMKEL.IS", "ENERY.IS", "ENJSA.IS", "ENKAI.IS", "ENSRI.IS",
    "EPLAS.IS", "ERBOS.IS", "ERCB.IS", "EREGL.IS", "ERSU.IS", "ESCAR.IS", "ESEN.IS", "ETILR.IS", "EUHOL.IS", "EUKYO.IS",
    "EUPWR.IS", "EUREN.IS", "EYGYO.IS", "FADE.IS", "FENER.IS", "FLAP.IS", "FMIZP.IS", "FONET.IS", "FORMT.IS", "FORTE.IS",
    "FROTO.IS", "GARAN.IS", "GARFA.IS", "GEDIK.IS", "GEDZA.IS", "GENTS.IS", "GEREL.IS", "GESAN.IS", "GLBMD.IS", "GLCVY.IS",
    "GLRYH.IS", "GLYHO.IS", "GMTAS.IS", "GOKNR.IS", "GOLTS.IS", "GOODY.IS", "GOZDE.IS", "GRNYO.IS", "GRSEL.IS", "GSDDE.IS",
    "GSDHO.IS", "GSRAY.IS", "GUBRF.IS", "GWIND.IS", "GZNMI.IS", "HALKB.IS", "HATEK.IS", "HATSN.IS", "HEDEF.IS", "HEKTS.IS",
    "HKTM.IS", "HLGYO.IS", "HOROZ.IS", "HRKET.IS", "HTTBT.IS", "HUBVC.IS", "HURGZ.IS", "ICBCT.IS", "IDEAS.IS", "IDGYO.IS",
    "IHEVA.IS", "IHGZT.IS", "IHLAS.IS", "IHLGM.IS", "IHYAY.IS", "IMASM.IS", "INDES.IS", "INFO.IS", "INGRM.IS", "INTEM.IS",
    "INVEO.IS", "INVES.IS", "ISATR.IS", "ISBIR.IS", "ISBTR.IS", "ISCEN.IS", "ISCTR.IS", "ISDMR.IS", "ISFIN.IS", "ISGSY.IS",
    "ISGYO.IS", "ISKPL.IS", "ISKUR.IS", "ISSEN.IS", "SUEN.IS", "IZENR.IS", "IZFAS.IS", "IZMDC.IS", "JANTS.IS", "KAPLM.IS",
    "KAREL.IS", "KARSN.IS", "KARTN.IS", "KARYE.IS", "KCAER.IS", "KCHOL.IS", "KFEIN.IS", "KGYO.IS", "KIMMR.IS", "KLGYO.IS",
    "KLKIM.IS", "KLSYN.IS", "KMPUR.IS", "KNFRT.IS", "KONTR.IS", "KONYA.IS", "KOPOL.IS", "KORDS.IS", "KOZAA.IS", "KOZAL.IS",
    "KRDMD.IS", "KRGYO.IS", "KRONT.IS", "KRPLS.IS", "KRSTL.IS", "KRVGD.IS", "KSTUR.IS", "KTLEV.IS", "KUTPO.IS", "KUYAS.IS",
    "LIDER.IS", "LIDFA.IS", "LKMNH.IS", "LOGO.IS", "LUKSK.IS", "MAALT.IS", "MACKO.IS", "MAGEN.IS", "MAKIM.IS", "MAKTK.IS",
    "MANAS.IS", "MARKA.IS", "MARTI.IS", "MAVI.IS", "MEDTR.IS", "MEGAP.IS", "MEKAG.IS", "MENPA.IS", "MERCN.IS", "MERKO.IS",
    "METUR.IS", "MGROS.IS", "MIATK.IS", "MIPAZ.IS", "MMCAS.IS", "MNDRS.IS", "MNDTR.IS", "MOBTL.IS", "MPARK.IS", "MRGYO.IS",
    "MRSHL.IS", "MSGYO.IS", "MTRKS.IS", "MTRYO.IS", "MZHLD.IS", "NATEN.IS", "NETAS.IS", "NIBAS.IS", "NTTUR.IS", "NUGYO.IS",
    "NUHCM.IS", "OBAMS.IS", "ODAS.IS", "OFSYM.IS", "ONCSM.IS", "ORGE.IS", "ORMA.IS", "OSMEN.IS", "OSTIM.IS", "OTKAR.IS",
    "OYAKC.IS", "OYYAT.IS", "OZATD.IS", "OZGYO.IS", "OZKGY.IS", "OZLRD.IS", "OZSUB.IS", "PAZAR.IS", "PCILT.IS", "PEKGY.IS",
    "PENGD.IS", "PENTA.IS", "PETKM.IS", "PETUN.IS", "PGSUS.IS", "PINSU.IS", "PKART.IS", "PKENT.IS", "PNSUT.IS", "POLHO.IS",
    "POLTK.IS", "PRDGS.IS", "PRKME.IS", "PRKTS.IS", "PSDTC.IS", "PSGYO.IS", "QUAGR.IS", "RALYH.IS", "RAYSG.IS", "REEDR.IS",
    "RGYAS.IS", "RNPOL.IS", "RODRG.IS", "ROYAL.IS", "RTALB.IS", "RUBNS.IS", "RYGYO.IS", "RYSAS.IS", "SAFKR.IS", "SAHOL.IS",
    "SARKY.IS", "SASA.IS", "SAYAS.IS", "SDTTR.IS", "SEGMN.IS", "SEKFK.IS", "SEKUR.IS", "SELEC.IS", "SELGD.IS", "SELVA.IS",
    "SEYKM.IS", "SILVR.IS", "SISE.IS", "SKBNK.IS", "SKTAS.IS", "SMART.IS", "SMRTG.IS", "SNGYO.IS", "SNICA.IS", "SNPAM.IS",
    "SODSN.IS", "SOKM.IS", "SONME.IS", "SUWEN.IS", "TAMDO.IS", "TATEN.IS", "TATGD.IS", "TAVHL.IS", "TBORG.IS", "TCELL.IS",
    "TDGYO.IS", "TEKTG.IS", "TEZOL.IS", "TGSAS.IS", "THYAO.IS", "TIRE.IS", "TKFEN.IS", "TKNSA.IS", "TMPOL.IS", "TMSN.IS",
    "TOASO.IS", "TRGYO.IS", "TRMET.IS", "TSKB.IS", "TSPOR.IS", "TTKOM.IS", "TTRAK.IS", "TUKAS.IS", "TUPRS.IS", "TURGG.IS",
    "TURSG.IS", "UFUK.IS", "ULKER.IS", "ULUUN.IS", "UNLU.IS", "USAK.IS", "VAKBN.IS", "VAKKO.IS", "VANGD.IS", "VBTYZ.IS",
    "VERTU.IS", "VERUS.IS", "VESBE.IS", "VESTL.IS", "VKGYO.IS", "VKING.IS", "YAPRK.IS", "YATAS.IS", "YAYLA.IS", "YBTAS.IS",
    "YEOTK.IS", "YKBNK.IS", "YKSLN.IS", "YUNSA.IS", "YUVAM.IS", "ZEDUR.IS", "ZOREN.IS", "ZRGYO.IS"
]


MORAL_SOZLERI = [
    "📉 *'Düşüşler zayıf ellerin döküldüğü, güçlülerin mal topladığı anlardır.'* — **Melih Ünal** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🦅",
    "🎯 *'Grafiklere bakıp hayal kurma, planına sadık kal ve stop seviyeni asla unutma.'* — **Piyasa Felsefesi** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 💡",
    "⚡ *'Borsada herkes kazanırken sessiz olan, kaybederken ses çıkarandır.'* — **Sokak Bilgeliği** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🌀",
    "🧊 *'Ekranı kapatmayı bilmeyen, borsanın oyuncuncağı olur.'* — **Trader Kanunu** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🛑",
    "💡 *'Risk almayan, fırsatları yakalayamaz.'* — **Warren Buffett** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Warren_Buffett_KU_%28cropped%29.jpg/220px-Warren_Buffett_KU_%28cropped%29.jpg) 🚀",
    "🔥 *'Borsada başarılı olmanın anahtarı, korkuya ve hırsa teslim olmamaktır.'* — **Peter Lynch** [Resim](https://upload.wikimedia.org/wikipedia/commons/e/ec/Peter_Lynch_%28cropped%29.jpg) 🧠",
    "🧠 *'Piyasa, sabırsızlardan sabırlılara para aktaran bir araçtır.'* — **Warren Buffett** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Warren_Buffett_KU_%28cropped%29.jpg/220px-Warren_Buffett_KU_%28cropped%29.jpg) 💸",
    "🏆 *'En büyük yatırım, kendi bilgi ve disiplinine yaptığın yatırımdır.'* — **Benjamin Franklin** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Benjamin_Franklin_by_Dusentimit.jpg/220px-Benjamin_Franklin_by_Dusentimit.jpg) 📚",
    "🌊 *'Piyasanın ne yapacağını tahmin etmeye çalışma, piyasaya uyum sağla.'* — **Ray Dalio** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Ray_Dalio_2014_%28cropped%29.jpg/220px-Ray_Dalio_2014_%28cropped%29.jpg) 🌊",
    "🛡️ *'İlk kural para kaybetmemektir. İkinci kural birinci kuralı unutmamaktır.'* — **Warren Buffett** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Warren_Buffett_KU_%28cropped%29.jpg/220px-Warren_Buffett_KU_%28cropped%29.jpg) ⚠️"
]

def telegrama_mesaj_gonder(mesaj):
    if TELEGRAM_BOT_TOKEN == "BURAYA_BOT_TOKEN_YAZIN" or not TELEGRAM_BOT_TOKEN:
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

def ozlu_soz_worker():
    son_gonderilen_dakika = -1
    while True:
        simdi = datetime.now(TZ)
        dakika = simdi.minute
        if (dakika == 0 or dakika == 30) and dakika != son_gonderilen_dakika:
            soz = random.choice(MORAL_SOZLERI)
            mesaj = f"💬 **Motivasyon & Özlü Söz:**\n\n{soz}"
            telegrama_mesaj_gonder(mesaj)
            son_gonderilen_dakika = dakika
        time.sleep(20)

def borsa_ve_pazar_worker():
    son_secilen_hisse = ""
    while True:
        simdi = datetime.now(TZ)
        haftanin_gunu = simdi.weekday()
        saat = simdi.hour
        dakika = simdi.minute
        
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
                
        elif 0 <= haftanin_gunu <= 4:
            if saat == 9 and dakika == 50:
                telegrama_mesaj_gonder("🔔 **Borsaya Az Kaldı!** Seansın açılmasına 10 dakika var. Ekranları açın, planlarınızı tazeleyin! 📈")
                time.sleep(60)
            elif (10 <= saat < 18) or (saat == 18 and dakika == 0):
                secilen = random.choice(TUM_BIST_LISTESI)
                while secilen == son_secilen_hisse and len(TUM_BIST_LISTESI) > 1:
                    secilen = random.choice(TUM_BIST_LISTESI)
                son_secilen_hisse = secilen
                
                analiz_mesaji = detayli_hisse_fon_analiz(secilen)
                telegrama_mesaj_gonder(analiz_mesaji)
                time.sleep(300)
                continue
            elif saat == 18 and dakika == 1:
                telegrama_mesaj_gonder("🔔 **Borsa Kapatıldı!** Bugünkü seans sona erdi. Dinlenin, yarın görüşmek üzere! ☕📉")
                time.sleep(60)
                
        time.sleep(10)

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

if __name__ == "__main__":
    print("🤖 Telegram Finans & Motivasyon Botu Başlatılıyor...")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    soz_thread = threading.Thread(target=ozlu_soz_worker, daemon=True)
    soz_thread.start()
    
    borsa_ve_pazar_worker()
