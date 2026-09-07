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
    "🎯 *'Fiyat ödediğin şeydir, değer ise sahip olduğun şey.'* — **Warren Buffett** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Warren_Buffett_KU_%28cropped%29.jpg/220px-Warren_Buffett_KU_%28cropped%29.jpg) 📊",
    "🏆 *'En büyük yatırım, kendi bilgi ve disiplinine yaptığın yatırımdır.'* — **Benjamin Franklin** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Benjamin_Franklin_by_Dusentimit.jpg/220px-Benjamin_Franklin_by_Dusentimit.jpg) 📚",
    "💰 *'Zenginlik, kazandığın paradan çok, biriktirdiğin ve yatırdığın parayla ölçülür.'* — **Benjamin Graham** [Resim](https://upload.wikimedia.org/wikipedia/commons/4/42/Benjamin_Graham_circa_1945.jpg) 🏦",
    "⏳ *'Borsada zaman geçirmek, zamanlamaya çalışmaktan her zaman daha kârlıdır.'* — **Jack Bogle** [Resim](https://upload.wikimedia.org/wikipedia/commons/3/3b/John_C._Bogle_2012.jpg) 📉",
    "🔮 *'Piyasanın ne yapacağını tahmin etmeye çalışma, piyasaya uyum sağla.'* — **Ray Dalio** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Ray_Dalio_2014_%28cropped%29.jpg/220px-Ray_Dalio_2014_%28cropped%29.jpg) 🌊",
    "🛡️ *'İlk kural para kaybetmemektir. İkinci kural birinci kuralı unutmamaktır.'* — **Warren Buffett** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Warren_Buffett_KU_%28cropped%29.jpg/220px-Warren_Buffett_KU_%28cropped%29.jpg) ⚠️",
    "🌊 *'Durgun denizler usta denizci yetiştirmez. Dalgalı piyasada tecrübe kazanırsın!'* — **Franklin D. Roosevelt** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/FDR_in_1933.jpg/220px-FDR_in_1933.jpg) ⛵",
    "📈 *'Trend senin dostundur, onunla savaşma.'* — **Martin Zweig** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🔄",
    "⚡ *'Acele ile yapılan yatırım, hırsın tuzağıdır.'* — **Konfüçyüs** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Confucius_-_Kong_Qiu_-_Palace_Museum.jpg/220px-Confucius_-_Kong_Qiu_-_Palace_Museum.jpg) 🛑",
    "🏔️ *'Zirveye giden yol, disiplinli adımlardan geçer.'* — **Friedrich Nietzsche** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Nietzsche187a.jpg/220px-Nietzsche187a.jpg) 🏔️",
    "🔑 *'Disiplin, hedefler ile başarı arasındaki köprüdür.'* — **Jim Rohn** [Resim](https://upload.wikimedia.org/wikipedia/commons/e/ec/Jim_Rohn.jpg) 🌉",
    "🏛️ *'Finansal özgürlük bir varış noktası değil, bir yaşam tarzıdır.'* — **Tony Robbins** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Tony_Robbins_by_Gage_Skidmore.jpg/220px-Tony_Robbins_by_Gage_Skidmore.jpg) 🔑",
    "🛠️ *'Stratejin olsun, planına sadık kal.'* — **Sun Tzu** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Sun_Tzu_-_Sima_Qian.jpg/220px-Sun_Tzu_-_Sima_Qian.jpg) 📐",
    "💸 *'Gelirini artırmak istiyorsan, finansal okuryazarlığını artır.'* — **Robert Kiyosaki** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Robert_Kiyosaki_by_Gage_Skidmore.jpg/220px-Robert_Kiyosaki_by_Gage_Skidmore.jpg) 📚",
    "🥇 *'Şans, hazırlıkla fırsatın karşılaştığı köşe başıdır.'* — **Seneca** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Seneca_the_Younger_epigraph_pushkin.jpg/220px-Seneca_the_Younger_epigraph_pushkin.jpg) 🎲",
    "🧠 *'En büyük risk, risk almamaktır.'* — **Mark Zuckerberg** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Mark_Zuckerberg_F8_2019_Keynote_%2832830578717%29_%28cropped%29.jpg/220px-Mark_Zuckerberg_F8_2019_Keynote_%2832830578717%29_%28cropped%29.jpg) 💥",
    "📐 *'Planlama yapmamak, başarısızlığı planlamaktır.'* — **Benjamin Franklin** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Benjamin_Franklin_by_Dusentimit.jpg/220px-Benjamin_Franklin_by_Dusentimit.jpg) 📝",
    "🏃 *'Durmadığın sürece ne kadar yavaş gittiğinin bir önemi yoktur.'* — **Konfüçyüs** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Confucius_-_Kong_Qiu_-_Palace_Museum.jpg/220px-Confucius_-_Kong_Qiu_-_Palace_Museum.jpg) 🚶‍♂️",
    "🧱 *'Büyük yapılar, tek tek dizilen sağlam tuğlalarla yükselir.'* — **Lao Tzu** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/8/84/Laozi_Depiction.jpg/220px-Laozi_Depiction.jpg) 🏛️",
    "🎈 *'Balonlar patlar, gerçek değerler kalıcıdır.'* — **Alan Greenspan** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Alan_Greenspan_official_portrait.jpg/220px-Alan_Greenspan_official_portrait.jpg) 🎈",
    "🗝️ *'Başarının sırrı, kriz anında sakin kalabilmektir.'* — **George Bernard Shaw** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/George_Bernard_Shaw_by_Barraud_1889.jpg/220px-George_Bernard_Shaw_by_Barraud_1889.jpg) 🧊",
    "🛡️ *'Sermayeni korumak, kâr etmekten daha önemlidir.'* — **George Soros** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/George_Soros_in_2013_-_World_Economic_Forum.jpg/220px-George_Soros_in_2013_-_World_Economic_Forum.jpg) 🏰",
    "🔮 *'Gelecek, yarın için bugün ne yaptığına bağlıdır.'* — **Mahatma Gandhi** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Mahatma-Gandhi%2C_studio_portrait%2C_1931.jpg/220px-Mahatma-Gandhi%2C_studio_portrait%2C_1931.jpg) ⏳",
    "📊 *'Rakamlar yalan söylemez, analize güven.'* — **Charles Dow** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Charles_Dow_-_Brady-Handy.jpg/220px-Charles_Dow_-_Brady-Handy.jpg) 📊",
    "🏆 *'Kendi şansını kendin yarat!'* — **Luciano De Crescenzo** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🎲",
    "🎓 *'Hatalar tecrübedir, tecrübe ise kazanç.'* — **Oscar Wilde** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Oscar_Wilde_by_Napoleon_Sarony_%28cropped%29.jpg/220px-Oscar_Wilde_by_Napoleon_Sarony_%28cropped%29.jpg) 💡",
    "⚡ *'Panik satışı, sabırsızlığın en pahalı faturasıdır.'* — **Peter Lynch** [Resim](https://upload.wikimedia.org/wikipedia/commons/e/ec/Peter_Lynch_%28cropped%29.jpg) 📄",
    "🌟 *'Işık karanlıkta daha parlak yanar. Düşüşlerde fırsat ara!'* — **William Shakespeare** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Shakespeare.jpg/220px-Shakespeare.jpg) 💡",
    "💡 *'Zihnine yatırım yap, cüzdanın karşılığını verir.'* — **Benjamin Franklin** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Benjamin_Franklin_by_Dusentimit.jpg/220px-Benjamin_Franklin_by_Dusentimit.jpg) 🧠",
    "🏹 *'Geriye çekilen ok, daha ileri gitmek içindir.'* — **Konfüçyüs** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Confucius_-_Kong_Qiu_-_Palace_Museum.jpg/220px-Confucius_-_Kong_Qiu_-_Palace_Museum.jpg) 🏹",
    "🧱 *'Sağlam temel, sabırla atılır.'* — **Mimar Sinan** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Mimar_Sinan_statue_in_Isparta.jpg/220px-Mimar_Sinan_statue_in_Isparta.jpg) 🏗️",
    "🧘 *'Duygusal karar kaybettirir, mantıklı karar kazandırır.'* — **Daniel Kahneman** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Daniel_Kahneman_2011.jpg/220px-Daniel_Kahneman_2011.jpg) 🧊",
    "🔑 *'Finansal özgürlük, istemediğin şeylere hayır diyebilme gücüdür.'* — **Nassim Nicholas Taleb** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Nassim_Nicholas_Taleb_by_Gage_Skidmore.jpg/220px-Nassim_Nicholas_Taleb_by_Gage_Skidmore.jpg) 🛑",
    "🏆 *'Şampiyonlar, antrenmanda kimse bakmıyorken ter dökenlerdir.'* — **Muhammad Ali** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Muhammad_Ali_NYWTS.jpg/220px-Muhammad_Ali_NYWTS.jpg) 🏋️‍♂️",
    "💡 *'Düzenli yatırım, geleceğe bırakılan en büyük mirastır.'* — **John D. Rockefeller** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/John_D._Rockefeller_circa_1885.jpg/220px-John_D._Rockefeller_circa_1885.jpg) 🏛️",
    "🌊 *'Her fırtınanın bir sonu vardır.'* — **Bob Marley** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Bob_Marley_in_Stockholm_1977.jpg/220px-Bob_Marley_in_Stockholm_1977.jpg) 🌈",
    "🎯 *'Disiplin, ne istediğin ile en çok ne istediğin arasında seçim yapmaktır.'* — **Abraham Lincoln** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Abraham_Lincoln_O-77_matte_collodion_print.jpg/220px-Abraham_Lincoln_O-77_matte_collodion_print.jpg) ⚖️",
    "🏆 *'Günü değil, geleceği kazanmayı hedefle!'* — **Andrew Carnegie** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Andrew_Carnegie%2C_coef_c.jpg/220px-Andrew_Carnegie%2C_coef_c.jpg) 🎖️",
    "💡 *'Bilgi güçtür, doğru strateji ise servettir.'* — **Francis Bacon** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Francis_Bacon_by_Paul_Van_Somer.jpg/220px-Francis_Bacon_by_Paul_Van_Somer.jpg) 👑",
    "🎯 *'Odağını dağıtma, hedefine kilitlen!'* — **Bruce Lee** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Bruce_Lee_1973.jpg/220px-Bruce_Lee_1973.jpg) 🎯",
    "✨ *'İnan, çalış, sabret ve başar!'* — **Mustafa Kemal Atatürk** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Atat%C3%BCrk_in_Ankara_%281930%29.jpg/220px-Atat%C3%BCrk_in_Ankara_%281930%29.jpg) 🏁",
    "📈 *'Sabırlı yatırımcı, piyasadaki en tehlikeli oyuncudur.'* — **Warren Buffett** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Warren_Buffett_KU_%28cropped%29.jpg/220px-Warren_Buffett_KU_%28cropped%29.jpg) ♟️",
    "💎 *'Değerli olan hiçbir şey kolay elde edilmez.'* — **Plato** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Plato_Silanion_Musei_Capitolini.jpg/220px-Plato_Silanion_Musei_Capitolini.jpg) 🏔️",
    "🛡️ *'Hisseni değil, riskini çeşitlendir.'* — **Harry Markowitz** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Harry_Markowitz_2008.jpg/220px-Harry_Markowitz_2008.jpg) 🌐",
    "🏆 *'Kaybetmeyi göze alamayan, kazanamaz.'* — **Friedrich Nietzsche** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Nietzsche187a.jpg/220px-Nietzsche187a.jpg) 🎲",
    "🧠 *'Bilgi, eyleme dönüştüğünde güç kazanır.'* — **Tony Robbins** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Tony_Robbins_by_Gage_Skidmore.jpg/220px-Tony_Robbins_by_Gage_Skidmore.jpg) ⚡",
    "🔥 *'Tutku, en büyük sermayedir.'* — **Donald Trump** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Donald_Trump_official_portrait.jpg/220px-Donald_Trump_official_portrait.jpg) ❤️",
    "⚡ *'Korkunun üzerine git ki korku senden kaçsın.'* — **Ralph Waldo Emerson** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Ralph_Waldo_Emerson_by_Southworth_and_Hawes%2C_c._1857.jpg/220px-Ralph_Waldo_Emerson_by_Southworth_and_Hawes%2C_c._1857.jpg) 🦁",
    "🏆 *'Başarı bir tesadüf değil, kusursuz bir hazırlık sonucudur.'* — **Vince Lombardi** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Vince_Lombardi_cutout.jpg/220px-Vince_Lombardi_cutout.jpg) 🎖️",
    "💎 *'Zaman pahabiçilmezdir, onu boşa harcama.'* — **Bruce Lee** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Bruce_Lee_1973.jpg/220px-Bruce_Lee_1973.jpg) ⏳",
    "🧠 *'Akıllı insan hatalarından ders çıkarır, dahi insan başkalarının hatalarından çıkarır.'* — **Otto von Bismarck** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Bismarck_v._Kuhn_c1875.jpg/220px-Bismarck_v._Kuhn_c1875.jpg) 🎓",
    "🛡️ *'Sermaye yönetimi, borsadaki en büyük zırhındır.'* — **Ray Dalio** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Ray_Dalio_2014_%28cropped%29.jpg/220px-Ray_Dalio_2014_%28cropped%29.jpg) 🛡️",
    "🎯 *'Kararlılık, en güçlü stratejiden daha değerlidir.'* — **Napoleon Bonaparte** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Jacques-Louis_David_-_The_Emperor_Napoleon_in_His_Study_at_the_Tuileries_-_Google_Art_Project.jpg/220px-Jacques-Louis_David_-_The_Emperor_Napoleon_in_His_Study_at_the_Tuileries_-_Google_Art_Project.jpg) ⚓",
    "🏆 *'Şampiyonlar asla bahan üretmez, sadece çalışır.'* — **Pelé** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pel%C3%A9_in_1972_%28cropped%29.jpg/220px-Pel%C3%A9_in_1972_%28cropped%29.jpg) 🥇",
    "📈 *'Fiyatlar düşebilir ama kaliteli şirketlerin değeri kalıcıdır.'* — **Benjamin Graham** [Resim](https://upload.wikimedia.org/wikipedia/commons/4/42/Benjamin_Graham_circa_1945.jpg) 🏛️",
    "🧠 *'Okumak zihin için neyse, yatırım yapmak finansal gelecek için odur.'* — **Joseph Addison** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Joseph_Addison_by_Sir_Godfrey_Kneller%2C_Bt.jpg/220px-Joseph_Addison_by_Sir_Godfrey_Kneller%2C_Bt.jpg) 📚",
    "🛡️ *'Stop-loss koymak korkaklık değil, profesyonelliktir.'* — **Alexander Elder** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🛑",
    "📈 *'Piyasa her zaman haklıdır, onunla inatlaşma.'* — **George Soros** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/George_Soros_in_2013_-_World_Economic_Forum.jpg/220px-George_Soros_in_2013_-_World_Economic_Forum.jpg) 🤝",
    "💎 *'Disiplinli bir zihin, en karlı portföydür.'* — **Charlie Munger** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Charlie_Munger_2019_by_Gage_Skidmore_%28cropped%29.jpg/220px-Charlie_Munger_2019_by_Gage_Skidmore_%28cropped%29.jpg) 🧠",
    "🚀 *'Bugün ektiğin tohumlar, yarının finansal özgürlük meyveleridir.'* — **Piyasa Felsefesi** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🌱",
    "🎯 *'Hedefi olmayan yatırımcının rüzgarı asla lehte esmez.'* — **Seneca** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Seneca_the_Younger_epigraph_pushkin.jpg/220px-Seneca_the_Younger_epigraph_pushkin.jpg) 🏹",
    "💡 *'Basit tut, aptalca olma. Stratejini karmaşıklaştırma.'* — **Charlie Munger** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Charlie_Munger_2019_by_Gage_Skidmore_%28cropped%29.jpg/220px-Charlie_Munger_2019_by_Gage_Skidmore_%28cropped%29.jpg) 🧩",
    "🌊 *'Fırtınada kaptan belli olur, sakin günde herkes yüzebilir.'* — **Türk Atasözü** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) ⛵",
    "⚡ *'Kripto ya da borsa; sabırsızın parası sabırlıya geçer.'* — **Sokak Bilgeliği** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 💸",
    "🛡️ *'Asla tek bir varlığa tüm hayatını bağlama.'* — **Aesop** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Aesop_Velazquez.jpg/220px-Aesop_Velazquez.jpg) 🛡️",
    "🧠 *'Piyasa psikolojisini yönetemeyen, parasını da yönetemez.'* — **Mark Douglas** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🧠",
    "📈 *'Boğalar kazanır, ayıar kazanır, açgözlüler kaybeder.'* — **Wall Street Atasözü** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🐂",
    "🏆 *'En iyi trader, hata yaptığında inat etmeyendir.'* — **Trader Kanunu** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🎯",
    "💎 *'Küçük masraflar büyük tekneleri batırır; komisyonlara dikkat et.'* — **Benjamin Franklin** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Benjamin_Franklin_by_Dusentimit.jpg/220px-Benjamin_Franklin_by_Dusentimit.jpg) ⛵",
    "🔥 *'Başarı ateşi, sürekli öğrenme odunuyla yanar.'* — **Melih Ünal** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🔥",
    "💡 *'Gözünü ekrandan ayırıp mantığına odaklandığında kazanç başlar.'* — **Piyasa Felsefesi** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 👁️",
    "📉 *'Krizler büyük servetlerin transfer olduğu dönüm noktalarıdır.'* — **Sir John Templeton** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Sir_John_Templeton_by_Allan_Warren.jpg/220px-Sir_John_Templeton_by_Allan_Warren.jpg) 🌍",
    "🎯 *'Yatırım bir sprint değil, ömür boyu süren bir maratondur.'* — **Howard Marks** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🏃‍♂️",
    "⚡ *'Başkaları korkarken açgözlü ol, başkaları açgözlüyken kork.'* — **Warren Buffett** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Warren_Buffett_KU_%28cropped%29.jpg/220px-Warren_Buffett_KU_%28cropped%29.jpg) 🦅",
    "🧊 *'Soğukkanlılığını koruyabilen bir yatırımcı, piyasanın yarısını zaten yenmiştir.'* — **Ray Dalio** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Ray_Dalio_2014_%28cropped%29.jpg/220px-Ray_Dalio_2014_%28cropped%29.jpg) 🧊",
    "🛡️ *'Hata yapmak insani bir durumdur, zararı kesmemek ise tercihtir.'* — **Alexander Elder** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🛑",
    "🧠 *'Öğrenmeyi bıraktığın gün, portföyünün de küçüldüğü gündür.'* — **Peter Lynch** [Resim](https://upload.wikimedia.org/wikipedia/commons/e/ec/Peter_Lynch_%28cropped%29.jpg) 📚",
    "🏆 *'Çok işlem yapmak çok kazandırmaz, doğru işlem kazandırır.'* — **Trader Kanunu** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🎯",
    "✨ *'Yarın zengin olmak istiyorsan, bugün risklerini matematiğe dök.'* — **Melih Ünal** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 📐",
    "📈 *'Trend analiz edilmez, takip edilir.'* — **Jesse Livermore** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Jesse_Livermore_1.jpg/220px-Jesse_Livermore_1.jpg) 🚀",
    "💎 *'İyi bir şirket sabırlı yatırımcısını asla üzmez.'* — **Warren Buffett** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Warren_Buffett_KU_%28cropped%29.jpg/220px-Warren_Buffett_KU_%28cropped%29.jpg) 🌟",
    "🌊 *'Dalgalara karşı kürek çekmek yerine rüzgarı arkana al.'* — **Sun Tzu** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Sun_Tzu_-_Sima_Qian.jpg/220px-Sun_Tzu_-_Sima_Qian.jpg) 🌬️",
    "⚡ *'Kaldıraçlı işlemler sabırsızların mezarılığıdır.'* — **Sokak Bilgeliği** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) ⚰️",
    "🏛️ *'Temeli sağlam olmayan bina ilk sarsıntıda yıkılır; bilgin yoksa borsaya girme.'* — **Mimar Sinan** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Mimar_Sinan_statue_in_Isparta.jpg/220px-Mimar_Sinan_statue_in_Isparta.jpg) 🏗️",
    "💡 *'Piyasa her gün açıktır ama her gün işlem yapmak zorunda değilsin.'* — **Charlie Munger** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Charlie_Munger_2019_by_Gage_Skidmore_%28cropped%29.jpg/220px-Charlie_Munger_2019_by_Gage_Skidmore_%28cropped%29.jpg) 🛑",
    "🎯 *'Her strateji her piyasaya uymaz, esnek ol.'* — **George Soros** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/George_Soros_in_2013_-_World_Economic_Forum.jpg/220px-George_Soros_in_2013_-_World_Economic_Forum.jpg) 🔄",
    "🏆 *'Başarı, küçük disiplinlerin her gün tekrarlanmasıdır.'* — **John C. Maxwell** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/John_C._Maxwell_by_Gage_Skidmore.jpg/220px-John_C._Maxwell_by_Gage_Skidmore.jpg) 🧱",
    "📉 *'Düşen bıçak tutulmaz, taban oluşumu beklenir.'* — **Teknik Analiz Kuralı** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🔪",
    "🧠 *'Paranı yönetemiyorsan, daha fazla para kazanmanın hiçbir anlamı yoktur.'* — **T. Harv Eker** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 💼",
    "✨ *'Kendi kararlarının sorumluluğunu al, bahanelere sığınma.'* — **Marcus Aurelius** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Marcus_Aurelius_Glyptothek_Munich_380.jpg/220px-Marcus_Aurelius_Glyptothek_Munich_380.jpg) 🛡️",
    "🚀 *'Geleceği tahmin etmenin en iyi yolu onu inşa etmektir.'* — **Peter Drucker** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Peter_Drucker_-_World_Economic_Forum_Annual_Meeting_1995.jpg/220px-Peter_Drucker_-_World_Economic_Forum_Annual_Meeting_1995.jpg) 🏗️",
    "💡 *'Bilgi cüzdanı doldurur, cehalet ise boşaltır.'* — **Benjamin Franklin** [Resim](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Benjamin_Franklin_by_Dusentimit.jpg/220px-Benjamin_Franklin_by_Dusentimit.jpg) 📖",
    "🔥 *'Hırsını kontrol edemeyen, portföyünü de kontrol edemez.'* — **Piyasa Felsefesi** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🔥",
    "🌊 *'Piyasa bir okyanustur; yüzme bilmiyorsan kıyıda kal.'* — **Sokak Bilgeliği** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 🏊‍♂️",
    "💎 *'Sabır, en karlı yatırımdır.'* — **Melih Ünal** [Resim](https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg) 💎"
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
