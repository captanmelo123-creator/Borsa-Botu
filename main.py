# ============================================================
# BORSA TAHMİN BOTU V3
# BIST + TEFAS FON TARAMA SİSTEMİ
# Pydroid 3 uyumlu
# ============================================================

import datetime
import logging
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import requests
import schedule
import telebot
import yfinance as yf


# ============================================================
# 1 - TELEGRAM AYARLARI
# ============================================================

TOKEN = "BURAYA_YENI_BOT_TOKENINI_YAZ"

ADMIN_ID = 123456789

bot = telebot.TeleBot(TOKEN)


# ============================================================
# 2 - LOG
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.getLogger("yfinance").setLevel(logging.CRITICAL)


# ============================================================
# 3 - GENEL AYARLAR
# ============================================================

BIST_MIN_DATA = 150

FON_MIN_DATA = 30

FON_GECMIS_GUN = 120

TOP_N = 10

CACHE_SURESI = 240

TEFAS_DELAY = 1.0


# ============================================================
# 4 - ÖZLÜ SÖZLER
# ============================================================

MORAL_SOZLERI = [

    "📉🦅🔥 *Düşüşler zayıf ellerin döküldüğü, güçlülerin mal topladığı anlardır.* — **Melih Ünal**",

    "🎯💡⚡ *Grafiklere bakıp hayal kurma, planına sadık kal ve stop seviyeni unutma.* — **Piyasa Felsefesi**",

    "⚡🌀💥 *Borsada herkes kazanırken sessiz olan, kaybederken ses çıkarandır.* — **Sokak Bilgeliği**",

    "🧊🛑🛡️ *Ekranı kapatmayı bilmeyen, borsanın oyuncağı olur.* — **Trader Kanunu**",

    "🧠💸⏳ *Piyasa, sabırsızlardan sabırlılara para aktaran bir araçtır.* — **Warren Buffett**",

    "🎯📊💎 *Fiyat ödediğin şeydir, değer ise sahip olduğun şey.* — **Warren Buffett**",

    "🛡️⚠️🔒 *İlk kural para kaybetmemektir. İkinci kural birinci kuralı unutmamaktır.* — **Warren Buffett**",

    "📈🔄🚀 *Trend senin dostundur, onunla savaşma.* — **Martin Zweig**",

    "⚡🛑🧠 *Acele ile yapılan yatırım, hırsın tuzağıdır.* — **Piyasa Felsefesi**",

    "🏆📚🧠 *En büyük yatırım, kendi bilgi ve disiplinine yaptığın yatırımdır.* — **Piyasa Felsefesi**",

    "🧘🧊🧠 *Duygusal karar kaybettirir, mantıklı plan güçlendirir.* — **Piyasa Felsefesi**",

    "🛡️🌐⚖️ *Hisseni değil, riskini çeşitlendir.* — **Harry Markowitz**",

    "📈🐂🐻 *Boğalar kazanır, ayılar kazanır, açgözlüler kaybeder.* — **Wall Street Atasözü**",

    "🏆🎯⚡ *En iyi trader, hata yaptığında inat etmeyendir.* — **Trader Kanunu**",

    "🔥📚🚀 *Başarı ateşi, sürekli öğrenmeyle güçlenir.* — **Melih Ünal**",

    "🎯🏃‍♂️📈 *Yatırım bir sprint değil, uzun bir maratondur.* — **Howard Marks**",

    "🧊🛡️🧠 *Soğukkanlılığını koruyabilen yatırımcı avantaj elde eder.* — **Piyasa Felsefesi**",

    "🧠📚📈 *Öğrenmeyi bıraktığın gün gelişimin de durur.* — **Piyasa Felsefesi**",

    "🏆🎯⚡ *Çok işlem yapmak çok kazandırmaz, doğru işlem kazandırır.* — **Trader Kanunu**",

    "✨📐🚀 *Risklerini matematiğe dökmeden işlem yapma.* — **Melih Ünal**",

    "💎⏳📈 *Sabır, yatırımcının en güçlü araçlarından biridir.* — **Melih Ünal**"
]


# ============================================================
# 5 - BIST LİSTESİ
# ============================================================

TUM_BIST_LISTESI = [

    "ACSEL.IS",
    "ADEL.IS",
    "ADESE.IS",
    "ADGYO.IS",
    "AEFES.IS",
    "AFYON.IS",
    "AGESA.IS",
    "AGHOL.IS",
    "AGROT.IS",
    "AKBNK.IS",
    "AKCNS.IS",
    "AKENR.IS",
    "AKFGY.IS",
    "AKFYE.IS",
    "AKGRT.IS",
    "AKSA.IS",
    "AKSEN.IS",
    "ALARK.IS",
    "ALBRK.IS",
    "ALCAR.IS",
    "ALCTL.IS",
    "ALFAS.IS",
    "ALGYO.IS",
    "ALKA.IS",
    "ALKIM.IS",
    "ALTNY.IS",
    "ANHYT.IS",
    "ANSGR.IS",
    "ARCLK.IS",
    "ARDYZ.IS",
    "ARENA.IS",
    "ARSAN.IS",
    "ASELS.IS",
    "ASTOR.IS",
    "ASUZU.IS",
    "ATAKP.IS",
    "ATATP.IS",
    "AYDEM.IS",
    "AYEN.IS",
    "AYGAZ.IS",
    "AZTEK.IS",
    "BAGFS.IS",
    "BAKAB.IS",
    "BALAT.IS",
    "BANVT.IS",
    "BARMA.IS",
    "BASGZ.IS",
    "BAYRK.IS",
    "BERA.IS",
    "BEYAZ.IS",
    "BIENY.IS",
    "BIGCH.IS",
    "BIMAS.IS",
    "BINHO.IS",
    "BIOEN.IS",
    "BIZIM.IS",
    "BJKAS.IS",
    "BLCYT.IS",
    "BMSCH.IS",
    "BMSTL.IS",
    "BNTAS.IS",
    "BOBET.IS",
    "BORLS.IS",
    "BORSK.IS",
    "BOSSA.IS",
    "BRISA.IS",
    "BRKSN.IS",
    "BRLSM.IS",
    "BRYAT.IS",
    "BUCIM.IS",
    "BURCE.IS",
    "BURVA.IS",
    "BVSAN.IS",

    "CANTE.IS",
    "CATES.IS",
    "CCOLA.IS",
    "CEMAS.IS",
    "CEMTS.IS",
    "CIMSA.IS",
    "CLEBI.IS",
    "CONSE.IS",
    "COSMO.IS",
    "CRDFA.IS",
    "CRFSA.IS",
    "CWENE.IS",

    "DAGI.IS",
    "DAPGM.IS",
    "DARDL.IS",
    "DENGE.IS",
    "DERIM.IS",
    "DESA.IS",
    "DESPC.IS",
    "DEVA.IS",
    "DITAS.IS",
    "DOAS.IS",
    "DOHOL.IS",
    "DOKTA.IS",
    "DURDO.IS",
    "DYOBY.IS",
    "DZGYO.IS",

    "EBEBK.IS",
    "EGEEN.IS",
    "EGEPO.IS",
    "EGGUB.IS",
    "EGPRO.IS",
    "EGSER.IS",
    "EKGYO.IS",
    "EKSUN.IS",
    "ELITE.IS",
    "ENERY.IS",
    "ENJSA.IS",
    "ENKAI.IS",
    "EREGL.IS",
    "EUPWR.IS",
    "EUREN.IS",

    "FENER.IS",
    "FROTO.IS",

    "GARAN.IS",
    "GARFA.IS",
    "GEDIK.IS",
    "GEDZA.IS",
    "GENTS.IS",
    "GEREL.IS",
    "GESAN.IS",
    "GLYHO.IS",
    "GMTAS.IS",
    "GOKNR.IS",
    "GOLTS.IS",
    "GOODY.IS",
    "GOZDE.IS",
    "GRSEL.IS",
    "GSDHO.IS",
    "GSRAY.IS",
    "GUBRF.IS",
    "GWIND.IS",

    "HALKB.IS",
    "HATSN.IS",
    "HEDEF.IS",
    "HEKTS.IS",
    "HKTM.IS",
    "HLGYO.IS",
    "HOROZ.IS",
    "HRKET.IS",
    "HTTBT.IS",

    "ICBCT.IS",
    "IDEAS.IS",
    "IDGYO.IS",
    "IHEVA.IS",
    "IHLAS.IS",
    "IHLGM.IS",
    "IMASM.IS",
    "INDES.IS",
    "INFO.IS",
    "INGRM.IS",
    "INVEO.IS",
    "INVES.IS",
    "ISCTR.IS",
    "ISDMR.IS",
    "ISFIN.IS",
    "ISGYO.IS",

    "IZENR.IS",
    "IZFAS.IS",
    "IZMDC.IS",

    "JANTS.IS",

    "KAREL.IS",
    "KARSN.IS",
    "KARTN.IS",
    "KARYE.IS",
    "KCAER.IS",
    "KCHOL.IS",
    "KFEIN.IS",
    "KGYO.IS",
    "KIMMR.IS",
    "KLGYO.IS",
    "KLKIM.IS",
    "KLSYN.IS",
    "KMPUR.IS",
    "KNFRT.IS",
    "KONTR.IS",
    "KONYA.IS",
    "KOPOL.IS",
    "KORDS.IS",
    "KOZAA.IS",
    "KOZAL.IS",
    "KRDMD.IS",
    "KRONT.IS",
    "KRPLS.IS",
    "KRVGD.IS",
    "KTLEV.IS",
    "KUTPO.IS",
    "KUYAS.IS",

    "LIDER.IS",
    "LIDFA.IS",
    "LKMNH.IS",
    "LOGO.IS",
    "LUKSK.IS",

    "MAALT.IS",
    "MACKO.IS",
    "MAGEN.IS",
    "MAKIM.IS",
    "MANAS.IS",
    "MAVI.IS",
    "MEDTR.IS",
    "MEGAP.IS",
    "MEKAG.IS",
    "MERCN.IS",
    "MERKO.IS",
    "METUR.IS",
    "MGROS.IS",
    "MIATK.IS",
    "MNDTR.IS",
    "MOBTL.IS",
    "MPARK.IS",
    "MRGYO.IS",
    "MRSHL.IS",
    "MTRKS.IS",

    "NATEN.IS",
    "NETAS.IS",
    "NUGYO.IS",
    "NUHCM.IS",

    "OBAMS.IS",
    "ODAS.IS",
    "OFSYM.IS",
    "ONCSM.IS",
    "ORGE.IS",
    "OSMEN.IS",
    "OSTIM.IS",
    "OTKAR.IS",
    "OYAKC.IS",
    "OZATD.IS",
    "OZKGY.IS",
    "OZLRD.IS",
    "OZSUB.IS",

    "PCILT.IS",
    "PEKGY.IS",
    "PENGD.IS",
    "PENTA.IS",
    "PETKM.IS",
    "PETUN.IS",
    "PGSUS.IS",
    "PKART.IS",
    "PKENT.IS",
    "PNSUT.IS",
    "POLHO.IS",
    "PRDGS.IS",
    "PRKME.IS",
    "PSDTC.IS",
    "PSGYO.IS",

    "RALYH.IS",
    "RAYSG.IS",
    "REEDR.IS",
    "RGYAS.IS",
    "RUBNS.IS",
    "RYGYO.IS",
    "RYSAS.IS",

    "SAHOL.IS",
    "SARKY.IS",
    "SASA.IS",
    "SAYAS.IS",
    "SDTTR.IS",
    "SELEC.IS",
    "SILVR.IS",
    "SISE.IS",
    "SKBNK.IS",
    "SMART.IS",
    "SMRTG.IS",
    "SOKM.IS",
    "SUWEN.IS",

    "TATEN.IS",
    "TAVHL.IS",
    "TCELL.IS",
    "TEKTG.IS",
    "TEZOL.IS",
    "THYAO.IS",
    "TKFEN.IS",
    "TKNSA.IS",
    "TMSN.IS",
    "TOASO.IS",
    "TRGYO.IS",
    "TSKB.IS",
    "TTKOM.IS",
    "TTRAK.IS",
    "TUKAS.IS",
    "TUPRS.IS",
    "TURSG.IS",

    "ULKER.IS",
    "UNLU.IS",
    "USAK.IS",

    "VAKBN.IS",
    "VAKKO.IS",
    "VESTL.IS",
    "VKGYO.IS",

    "YKBNK.IS",
    "YKSLN.IS",
    "YEOTK.IS",
    "YUNSA.IS",

    "ZOREN.IS",
    "ZRGYO.IS"
]


# ============================================================
# 6 - BIST CACHE
# ============================================================

BIST_CACHE = {}


# ============================================================
# 7 - BIST VERİ ÇEK
# ============================================================

def bist_veri_getir(sembol):

    try:

        simdi = time.time()

        if sembol in BIST_CACHE:

            zaman, veri = BIST_CACHE[sembol]

            if simdi - zaman < CACHE_SURESI:

                return veri.copy()

        ticker = yf.Ticker(sembol)

        df = ticker.history(
            period="1y",
            interval="1d",
            auto_adjust=False
        )

        if df is None or df.empty:
            return None

        df = df.dropna(
            subset=[
                "Open",
                "High",
                "Low",
                "Close",
                "Volume"
            ]
        )

        if len(df) < BIST_MIN_DATA:
            return None

        BIST_CACHE[sembol] = (
            simdi,
            df.copy()
        )

        return df

    except Exception as e:

        logging.error(
            f"BIST VERİ HATASI {sembol}: {e}"
        )

        return None


# ============================================================
# 8 - RSI
# ============================================================

def rsi_hesapla(close, period=14):

    delta = close.diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()

    avg_loss = loss.ewm(
        alpha=1 / period,
        adjust=False
    ).mean()

    rs = avg_gain / avg_loss.replace(
        0,
        1e-9
    )

    return 100 - (
        100 / (1 + rs)
    )


# ============================================================
# 9 - BIST ANALİZ
# ============================================================

def bist_analiz(sembol):

    try:

        df = bist_veri_getir(sembol)

        if df is None:
            return None

        close = df["Close"]

        high = df["High"]

        low = df["Low"]

        volume = df["Volume"]

        fiyat = float(close.iloc[-1])

        onceki = float(close.iloc[-2])

        gunluk = (
            (fiyat / onceki) - 1
        ) * 100

        ema20 = close.ewm(
            span=20,
            adjust=False
        ).mean()

        ema50 = close.ewm(
            span=50,
            adjust=False
        ).mean()

        sma200 = close.rolling(200).mean()

        rsi_serisi = rsi_hesapla(close)

        rsi = float(
            rsi_serisi.iloc[-1]
        )

        ema12 = close.ewm(
            span=12,
            adjust=False
        ).mean()

        ema26 = close.ewm(
            span=26,
            adjust=False
        ).mean()

        macd = ema12 - ema26

        signal = macd.ewm(
            span=9,
            adjust=False
        ).mean()

        macd_val = float(
            macd.iloc[-1]
        )

        signal_val = float(
            signal.iloc[-1]
        )

        hacim_ortalama = float(
            volume.rolling(20).mean().iloc[-1]
        )

        hacim_orani = (
            float(volume.iloc[-1]) /
            (hacim_ortalama + 1e-9)
        )

        momentum_5 = (
            fiyat /
            float(close.iloc[-6]) - 1
        ) * 100

        momentum_20 = (
            fiyat /
            float(close.iloc[-21]) - 1
        ) * 100

        tr = pd.concat(
            [
                high - low,

                (high - close.shift()).abs(),

                (low - close.shift()).abs()
            ],
            axis=1
        ).max(axis=1)

        atr = float(
            tr.rolling(14).mean().iloc[-1]
        )

        skor = 50

        if fiyat > float(ema20.iloc[-1]):
            skor += 7

        else:
            skor -= 7

        if float(ema20.iloc[-1]) > float(ema50.iloc[-1]):
            skor += 7

        else:
            skor -= 7

        if fiyat > float(sma200.iloc[-1]):
            skor += 8

        else:
            skor -= 8

        if 50 <= rsi <= 65:
            skor += 8

        elif rsi < 30:
            skor += 5

        elif rsi > 70:
            skor -= 10

        if macd_val > signal_val:
            skor += 8

        else:
            skor -= 8

        if hacim_orani > 1.5:
            skor += 6

        elif hacim_orani < 0.7:
            skor -= 3

        if momentum_5 > 3:
            skor += 5

        elif momentum_5 < -3:
            skor -= 5

        if momentum_20 > 5:
            skor += 5

        elif momentum_20 < -5:
            skor -= 5

        skor = max(
            0,
            min(100, skor)
        )

        if skor >= 80:
            sinyal = "🟢 GÜÇLÜ AL"

        elif skor >= 70:
            sinyal = "🟢 POZİTİF"

        elif skor >= 55:
            sinyal = "🟡 İZLE"

        elif skor >= 40:
            sinyal = "🟠 ZAYIF"

        else:
            sinyal = "🔴 NEGATİF"

        stop = fiyat - (
            atr * 1.5
        )

        hedef = fiyat + (
            atr * 3
        )

        if stop <= 0:
            stop = fiyat * 0.95

        return {
            "kod": sembol.replace(".IS", ""),
            "fiyat": fiyat,
            "skor": skor,
            "sinyal": sinyal,
            "rsi": rsi,
            "macd": macd_val,
            "hacim": hacim_orani,
            "momentum5": momentum_5,
            "momentum20": momentum_20,
            "stop": stop,
            "hedef": hedef
        }

    except Exception as e:

        logging.error(
            f"BIST ANALİZ HATASI {sembol}: {e}"
        )

        return None


# ============================================================
# 10 - BIST TOPLU TARAMA
# ============================================================

def bist_taramasi():

    sonuclar = []

    logging.info(
        f"BIST taraması başladı: "
        f"{len(TUM_BIST_LISTESI)} hisse"
    )

    with ThreadPoolExecutor(
        max_workers=4
    ) as executor:

        futures = {

            executor.submit(
                bist_analiz,
                hisse
            ): hisse

            for hisse in TUM_BIST_LISTESI
        }

        for future in as_completed(
            futures
        ):

            try:

                sonuc = future.result()

                if sonuc:
                    sonuclar.append(sonuc)

            except Exception as e:

                logging.error(
                    f"THREAD HATASI: {e}"
                )

    sonuclar.sort(
        key=lambda x: x["skor"],
        reverse=True
    )

    return sonuclar


# ============================================================
# TEFAS SİSTEMİ
# ============================================================

TEFAS_URL = (
    "https://www.tefas.gov.tr/api/DB/BindHistoryInfo"
)


TEFAS_SESSION = requests.Session()


TEFAS_HEADERS = {

    "User-Agent":
        "Mozilla/5.0 (Linux; Android 10) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/131.0 Mobile Safari/537.36",

    "Accept":
        "application/json, text/javascript, */*; q=0.01",

    "Origin":
        "https://www.tefas.gov.tr",

    "Referer":
        "https://www.tefas.gov.tr/TarihselVeriler.aspx",

    "X-Requested-With":
        "XMLHttpRequest",

    "Content-Type":
        "application/x-www-form-urlencoded; charset=UTF-8"
}


TEFAS_CACHE = None

TEFAS_CACHE_TIME = 0


# ============================================================
# 11 - TEFAS SESSION
# ============================================================

def tefas_session_baslat():

    try:

        response = TEFAS_SESSION.get(
            "https://www.tefas.gov.tr/",
            headers={
                "User-Agent":
                    TEFAS_HEADERS["User-Agent"]
            },
            timeout=20
        )

        response.raise_for_status()

        logging.info(
            "TEFAS session başlatıldı."
        )

        return True

    except Exception as e:

        logging.error(
            f"TEFAS SESSION HATASI: {e}"
        )

        return False


# ============================================================
# 12 - TEFAS VERİSİ ÇEK
# ============================================================

def tefas_veri_getir():

    global TEFAS_CACHE
    global TEFAS_CACHE_TIME

    simdi = time.time()

    if (
        TEFAS_CACHE is not None
        and
        simdi - TEFAS_CACHE_TIME < CACHE_SURESI
    ):

        return TEFAS_CACHE.copy()

    if not tefas_session_baslat():

        return None

    bugun = datetime.date.today()

    baslangic = (
        bugun -
        datetime.timedelta(
            days=FON_GECMIS_GUN
        )
    )

    bas_str = baslangic.strftime(
        "%d.%m.%Y"
    )

    bit_str = bugun.strftime(
        "%d.%m.%Y"
    )

    payload = {

        "fontip": "YAT",

        "fonkod": "",

        "bastarih": bas_str,

        "bittarih": bit_str,

        "sfontur": "",

        "fongrup": "",

        "fonturkod": "",

        "fonunvantip": "",

        "kurucukod": ""
    }

    try:

        logging.info(
            "TEFAS toplu fon verisi çekiliyor..."
        )

        response = TEFAS_SESSION.post(
            TEFAS_URL,
            headers=TEFAS_HEADERS,
            data=payload,
            timeout=60
        )

        response.raise_for_status()

        veri = response.json()

        rows = veri.get(
            "data",
            []
        )

        if not rows:

            logging.error(
                "TEFAS veri döndürmedi."
            )

            return None

        df = pd.DataFrame(rows)

        if df.empty:

            return None

        df.columns = [
            str(x).upper()
            for x in df.columns
        ]

        gerekli = [
            "TARIH",
            "FONKODU",
            "FONUNVAN",
            "FIYAT"
        ]

        for kolon in gerekli:

            if kolon not in df.columns:

                logging.error(
                    f"TEFAS kolon eksik: {kolon}"
                )

                return None

        df["FIYAT"] = pd.to_numeric(
            df["FIYAT"],
            errors="coerce"
        )

        df = df.dropna(
            subset=[
                "FIYAT"
            ]
        )

        df = df[
            df["FIYAT"] > 0
        ]

        def tarih_cevir(x):

            try:

                return pd.to_datetime(
                    x,
                    dayfirst=True
                )

            except:

                return pd.NaT

        df["TARIH"] = df[
            "TARIH"
        ].apply(
            tarih_cevir
        )

        df = df.dropna(
            subset=[
                "TARIH"
            ]
        )

        df["FONKODU"] = (
            df["FONKODU"]
            .astype(str)
            .str.upper()
            .str.strip()
        )

        df = df.sort_values(
            [
                "FONKODU",
                "TARIH"
            ]
        )

        TEFAS_CACHE = df.copy()

        TEFAS_CACHE_TIME = simdi

        logging.info(
            f"TEFAS verisi alındı: "
            f"{len(df)} kayıt / "
            f"{df['FONKODU'].nunique()} fon"
        )

        return df

    except Exception as e:

        logging.error(
            f"TEFAS VERİ HATASI: {e}"
        )

        return None


# ============================================================
# 13 - TEFAS FON ANALİZİ
# ============================================================

def fon_analiz_grup(grup):

    try:

        grup = grup.sort_values(
            "TARIH"
        )

        fiyatlar = grup[
            "FIYAT"
        ].astype(float)

        if len(fiyatlar) < FON_MIN_DATA:

            return None

        fiyat = float(
            fiyatlar.iloc[-1]
        )

        onceki = float(
            fiyatlar.iloc[-2]
        )

        gunluk = (
            fiyat / onceki - 1
        ) * 100

        getiri_7 = None

        getiri_30 = None

        getiri_60 = None

        if len(fiyatlar) >= 8:

            getiri_7 = (
                fiyat /
                float(fiyatlar.iloc[-8]) - 1
            ) * 100

        if len(fiyatlar) >= 31:

            getiri_30 = (
                fiyat /
                float(fiyatlar.iloc[-31]) - 1
            ) * 100

        if len(fiyatlar) >= 61:

            getiri_60 = (
                fiyat /
                float(fiyatlar.iloc[-61]) - 1
            ) * 100

        ema20 = fiyatlar.ewm(
            span=20,
            adjust=False
        ).mean()

        ema50 = fiyatlar.ewm(
            span=50,
            adjust=False
        ).mean()

        ema20_val = float(
            ema20.iloc[-1]
        )

        ema50_val = float(
            ema50.iloc[-1]
        )

        rsi_serisi = rsi_hesapla(
            fiyatlar
        )

        rsi = float(
            rsi_serisi.iloc[-1]
        )

        momentum = 0

        if getiri_30 is not None:

            if getiri_30 > 10:
                momentum += 10

            elif getiri_30 > 5:
                momentum += 6

            elif getiri_30 < -10:
                momentum -= 10

            elif getiri_30 < -5:
                momentum -= 6

        getiriler = fiyatlar.pct_change()

        volatilite = float(
            getiriler.tail(30).std()
        ) * 100

        rolling_max = (
            fiyatlar.cummax()
        )

        drawdown = (
            fiyatlar /
            rolling_max - 1
        ) * 100

        max_drawdown = float(
            drawdown.min()
        )

        skor = 50

        nedenler = []

        riskler = []

        if fiyat > ema20_val:

            skor += 8

            nedenler.append(
                "EMA20 üzeri"
            )

        else:

            skor -= 8

            riskler.append(
                "EMA20 altı"
            )

        if fiyat > ema50_val:

            skor += 8

            nedenler.append(
                "EMA50 üzeri"
            )

        else:

            skor -= 8

            riskler.append(
                "EMA50 altı"
            )

        if ema20_val > ema50_val:

            skor += 7

            nedenler.append(
                "Orta vadeli trend pozitif"
            )

        else:

            skor -= 7

            riskler.append(
                "Orta vadeli trend negatif"
            )

        if 50 <= rsi <= 65:

            skor += 10

            nedenler.append(
                "RSI sağlıklı"
            )

        elif rsi < 30:

            skor += 5

            nedenler.append(
                "RSI aşırı satım"
            )

        elif rsi > 70:

            skor -= 10

            riskler.append(
                "RSI aşırı alım"
            )

        if getiri_30 is not None:

            if getiri_30 > 10:

                skor += 8

                nedenler.append(
                    "30G güçlü momentum"
                )

            elif getiri_30 > 0:

                skor += 4

            elif getiri_30 < -10:

                skor -= 8

                riskler.append(
                    "30G negatif momentum"
                )

        if getiri_60 is not None:

            if getiri_60 > 15:

                skor += 5

            elif getiri_60 < -15:

                skor -= 5

        if volatilite < 2:

            skor += 4

            nedenler.append(
                "Volatilite düşük"
            )

        elif volatilite > 5:

            skor -= 4

            riskler.append(
                "Volatilite yüksek"
            )

        if max_drawdown > -10:

            skor += 4

        elif max_drawdown < -30:

            skor -= 5

            riskler.append(
                "Yüksek geri çekilme"
            )

        skor = max(
            0,
            min(100, skor)
        )

        if skor >= 80:

            sinyal = "🟢 GÜÇLÜ"

        elif skor >= 70:

            sinyal = "🟢 POZİTİF"

        elif skor >= 55:

            sinyal = "🟡 İZLE"

        elif skor >= 40:

            sinyal = "🟠 ZAYIF"

        else:

            sinyal = "🔴 NEGATİF"

        kod = str(
            grup["FONKODU"].iloc[-1]
        )

        ad = str(
            grup["FONUNVAN"].iloc[-1]
        )

        return {

            "kod": kod,

            "ad": ad,

            "fiyat": fiyat,

            "skor": skor,

            "sinyal": sinyal,

            "rsi": rsi,

            "gunluk": gunluk,

            "getiri7": getiri_7,

            "getiri30": getiri_30,

            "getiri60": getiri_60,

            "volatilite": volatilite,

            "drawdown": max_drawdown,

            "nedenler": nedenler,

            "riskler": riskler
        }

    except Exception as e:

        logging.error(
            f"FON ANALİZ HATASI: {e}"
        )

        return None


# ============================================================
# 14 - TÜM FONLARI TARA
# ============================================================

def fon_taramasi():

    df = tefas_veri_getir()

    if df is None:

        return []

    sonuclar = []

    gruplar = df.groupby(
        "FONKODU"
    )

    logging.info(
        f"{len(gruplar)} fon analiz edilecek."
    )

    for kod, grup in gruplar:

        sonuc = fon_analiz_grup(
            grup
        )

        if sonuc:

            sonuclar.append(
                sonuc
            )

    sonuclar.sort(
        key=lambda x: x["skor"],
        reverse=True
    )

    return sonuclar


# ============================================================
# 15 - FON TOP LİSTESİ
# ============================================================

def fon_top_mesaji(
    sonuclar,
    adet=10
):

    if not sonuclar:

        return (
            "❌ TEFAS fon verisi alınamadı."
        )

    mesaj = (
        "🏆 **TEFAS EN GÜÇLÜ FONLAR**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
    )

    for i, fon in enumerate(
        sonuclar[:adet],
        1
    ):

        getiri30 = fon["getiri30"]

        if getiri30 is None:

            getiri30_text = "N/A"

        else:

            getiri30_text = (
                f"%{getiri30:+.2f}"
            )

        mesaj += (
            f"{i}. **{fon['kod']}** "
            f"→ **{fon['skor']}/100** "
            f"{fon['sinyal']}\n"
            f"   💰 {fon['fiyat']:.4f} TL\n"
            f"   📈 30G: {getiri30_text}\n"
            f"   ⚡ RSI: {fon['rsi']:.1f}\n\n"
        )

    mesaj += (
        "⚠️ Teknik skor yatırım olasılığı değildir."
    )

    return mesaj


# ============================================================
# 16 - TEK FON MESAJI
# ============================================================

def tek_fon_mesaji(kod):

    kod = kod.upper().strip()

    df = tefas_veri_getir()

    if df is None:

        return (
            "❌ TEFAS verisi alınamadı."
        )

    grup = df[
        df["FONKODU"] == kod
    ]

    if grup.empty:

        return (
            f"❌ **{kod}** kodlu fon "
            f"veride bulunamadı."
        )

    sonuc = fon_analiz_grup(
        grup
    )

    if sonuc is None:

        return (
            f"⚠️ **{kod}** için yeterli "
            f"tarihsel veri bulunamadı."
        )

    getiri7 = sonuc["getiri7"]

    getiri30 = sonuc["getiri30"]

    getiri60 = sonuc["getiri60"]

    def fmt(x):

        if x is None:
            return "N/A"

        return f"%{x:+.2f}"

    mesaj = (

        "🧠 **TEFAS FON ANALİZİ**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"

        f"📌 Fon: **{sonuc['kod']}**\n"

        f"🏦 {sonuc['ad'][:100]}\n\n"

        f"💰 Fiyat: **{sonuc['fiyat']:.6f} TL**\n"

        f"🎯 Teknik Skor: **{sonuc['skor']}/100**\n"

        f"📢 Sinyal: **{sonuc['sinyal']}**\n"

        "━━━━━━━━━━━━━━━━━━━━\n"

        f"⚡ RSI: **{sonuc['rsi']:.1f}**\n"

        f"📈 7G Getiri: **{fmt(getiri7)}**\n"

        f"📈 30G Getiri: **{fmt(getiri30)}**\n"

        f"📈 60G Getiri: **{fmt(getiri60)}**\n"

        f"📊 Volatilite: **%{sonuc['volatilite']:.2f}**\n"

        f"📉 Max Drawdown: **%{sonuc['drawdown']:.2f}**\n"

        "━━━━━━━━━━━━━━━━━━━━\n"

        "🟢 Pozitif Faktörler:\n"

        + (
            ", ".join(
                sonuc["nedenler"][:5]
            )
            if sonuc["nedenler"]
            else "Yok"
        )

        + "\n\n"

        "🔴 Risk Faktörleri:\n"

        + (
            ", ".join(
                sonuc["riskler"][:5]
            )
            if sonuc["riskler"]
            else "Belirgin risk yok"
        )

        + "\n━━━━━━━━━━━━━━━━━━━━\n"

        "⚠️ Bu skor % kazanma ihtimali değildir.\n"

        "📡 Veri kaynağı: TEFAS\n"

    )

    return mesaj


# ============================================================
# 17 - OTOMATİK FON BİLDİRİMİ
# ============================================================

def otomatik_fon_bildirimi():

    try:

        sonuclar = fon_taramasi()

        if not sonuclar:

            return

        secilenler = sonuclar[:10]

        secilen = random.choice(
            secilenler
        )

        mesaj = tek_fon_mesaji(
            secilen["kod"]
        )

        bot.send_message(
            ADMIN_ID,
            mesaj,
            parse_mode="Markdown"
        )

    except Exception as e:

        logging.error(
            f"AUTOMATIK FON HATASI: {e}"
        )


# ============================================================
# 18 - OTOMATİK BIST BİLDİRİMİ
# ============================================================

def otomatik_bist_bildirimi():

    try:

        sonuclar = bist_taramasi()

        if not sonuclar:

            return

        secilenler = sonuclar[:10]

        secilen = random.choice(
            secilenler
        )

        mesaj = (

            "🧠 **BIST OTOMATİK TARAMA**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"

            f"📌 Hisse: **{secilen['kod']}**\n"

            f"💰 Fiyat: **{secilen['fiyat']:.2f} TL**\n"

            f"🎯 Teknik Skor: **{secilen['skor']}/100**\n"

            f"📢 Sinyal: **{secilen['sinyal']}**\n"

            "━━━━━━━━━━━━━━━━━━━━\n"

            f"⚡ RSI: **{secilen['rsi']:.1f}**\n"

            f"📊 Hacim: **{secilen['hacim']:.2f}x**\n"

            f"📈 5G Momentum: **%{secilen['momentum5']:+.2f}**\n"

            f"📈 20G Momentum: **%{secilen['momentum20']:+.2f}**\n"

            "━━━━━━━━━━━━━━━━━━━━\n"

            f"🛑 ATR Stop: **{secilen['stop']:.2f} TL**\n"

            f"🎯 ATR Hedef: **{secilen['hedef']:.2f} TL**\n"

            "━━━━━━━━━━━━━━━━━━━━\n"

            "⚠️ Teknik skor olasılık değildir.\n"

            "📡 Veri: Yahoo Finance"
        )

        bot.send_message(
            ADMIN_ID,
            mesaj,
            parse_mode="Markdown"
        )

    except Exception as e:

        logging.error(
            f"AUTOMATIK BIST HATASI: {e}"
        )


# ============================================================
# 19 - ÖZLÜ SÖZ
# ============================================================

def otomatik_soz_bildirimi():

    try:

        soz = random.choice(
            MORAL_SOZLERI
        )

        mesaj = (
            "💬 **30 DAKİKALIK MORAL & MOTİVASYON** 🚀\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"{soz}"
        )

        bot.send_message(
            ADMIN_ID,
            mesaj,
            parse_mode="Markdown"
        )

    except Exception as e:

        logging.error(
            f"SÖZ HATASI: {e}"
        )


# ============================================================
# 20 - PAZAR
# ============================================================

def pazar_bildirimi():

    soz = random.choice(
        MORAL_SOZLERI
    )

    mesaj = (

        "📅 **HAFTALIK BORSA & FON HAZIRLIK RAPORU**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"

        "📈 BIST ve TEFAS verilerini kontrol et.\n"
        "🛑 Risk seviyelerini belirle.\n"
        "⚖️ Pozisyon büyüklüğünü kontrol et.\n"
        "🧠 Duygusal işlem yapma.\n\n"

        f"💬 **Haftanın Sözü:**\n{soz}"

    )

    bot.send_message(
        ADMIN_ID,
        mesaj,
        parse_mode="Markdown"
    )


# ============================================================
# 21 - AÇILIŞ
# ============================================================

def acilis_bildirimi():

    if datetime.datetime.now().weekday() >= 5:

        return

    soz = random.choice(
        MORAL_SOZLERI
    )

    mesaj = (

        "🔔 **BIST SEANS AÇILIŞ UYARISI** 📈🟢\n"
        "━━━━━━━━━━━━━━━━━━━━\n"

        "☀️ Borsa açılışına 5 dakika kaldı.\n\n"

        "📊 Risk planını kontrol et.\n"
        "🛑 Stop seviyelerini unutma.\n"
        "🧠 Duygusal karar verme.\n\n"

        f"💬 **Günün Sözü:**\n{soz}"

    )

    bot.send_message(
        ADMIN_ID,
        mesaj,
        parse_mode="Markdown"
    )


# ============================================================
# 22 - KAPANIŞ
# ============================================================

def kapanis_bildirimi():

    if datetime.datetime.now().weekday() >= 5:

        return

    soz = random.choice(
        MORAL_SOZLERI
    )

    mesaj = (

        "🔔 **BIST SEANS KAPANIŞ RAPORU** 📊\n"
        "━━━━━━━━━━━━━━━━━━━━\n"

        "🌆 Seans tamamlandı.\n"
        "🧘 Günün sonuçlarını değerlendirme zamanı.\n\n"

        f"💬 **Akşamın Sözü:**\n{soz}"

    )

    bot.send_message(
        ADMIN_ID,
        mesaj,
        parse_mode="Markdown"
    )


# ============================================================
# 31 - ZAMANLAYICI
# ============================================================

# BIST (5 Dakika)
schedule.every(5).minutes.do(
    otomatik_bist_bildirimi
)

# Fonlar (5 Dakika)
schedule.every(5).minutes.do(
    otomatik_fon_bildirimi
)

# Özlü söz (30 Dakika)
schedule.every(30).minutes.do(
    otomatik_soz_bildirimi
)


# Pazar
schedule.every().sunday.at(
    "20:00"
).do(
    pazar_bildirimi
)


# Açılış
schedule.every().monday.at(
    "09:55"
).do(
    acilis_bildirimi
)

schedule.every().tuesday.at(
    "09:55"
).do(
    acilis_bildirimi
)

schedule.every().wednesday.at(
    "09:55"
).do(
    acilis_bildirimi
)

schedule.every().thursday.at(
    "09:55"
).do(
    acilis_bildirimi
)

schedule.every().friday.at(
    "09:55"
).do(
    acilis_bildirimi
)


# Kapanış
schedule.every().monday.at(
    "18:10"
).do(
    kapanis_bildirimi
)

schedule.every().tuesday.at(
    "18:10"
).do(
    kapanis_bildirimi
)

schedule.every().wednesday.at(
    "18:10"
).do(
    kapanis_bildirimi
)

schedule.every().thursday.at(
    "18:10"
).do(
    kapanis_bildirimi
)

schedule.every().friday.at(
    "18:10"
).do(
    kapanis_bildirimi
)


# ============================================================
# 32 - SCHEDULE THREAD
# ============================================================

def schedule_runner():

    while True:

        try:

            schedule.run_pending()

        except Exception as e:

            logging.error(
                f"SCHEDULE HATASI: {e}"
            )

        time.sleep(5)


threading.Thread(
    target=schedule_runner,
    daemon=True
).start()


# ============================================================
# 33 - BAŞLAT
# ============================================================

print(
    "============================================"
)

print(
    "🤖 BORSA TAHMİN BOTU V3"
)

print(
    f"📈 BIST sembolü: {len(TUM_BIST_LISTESI)}"
)

print(
    "💰 TEFAS: Toplu fon taraması aktif"
)

print(
    "⏱️ BIST: 5 dakika"
)

print(
    "💰 Fon: 5 dakika"
)

print(
    "💬 Söz: 30 dakika"
)

print(
    "============================================"
)


bot.infinity_polling(
    timeout=60,
    long_polling_timeout=60
)
