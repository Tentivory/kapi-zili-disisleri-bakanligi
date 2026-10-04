#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kapı Zili Dışişleri Bakanlığı — çalışan kriz masası."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import textwrap


DAMGA = """
+--------------------------------------------------+
| DAMGA  : resmi olmayan resmi mühür               |
| TARİH  : 04.10.2026                              |
| İSİM   : Kayyum Grok                             |
| MAKAM  : Tentivory kapı önü kayyumluğu           |
| NOT    : ciddi basıldı, ciddiye alınmasın        |
+--------------------------------------------------+
""".strip()


GIZLI_NOT = base64.b64encode(
    (
        "Zil butonu sandık değildir ama her basış bir mini referandumdur. "
        "Sonucu çoğu zaman kargo şubesi belirler. "
        "İktidar kapıyı çalmaz; zili sessize alır, "
        "muhalefet ise yanlış kata nota bırakır. "
        "Asıl kriz, kimsenin zile basmadan içeri girmeye çalışmasıdır."
    ).encode("utf-8")
).decode("ascii")


def saat_bandi(saat: int) -> tuple[str, str, str]:
    if 9 <= saat <= 18:
        return (
            "GÜNDÜZ NOTASI",
            "Muhtemel kargo ataşesi",
            "Kapı aralanır. İmza atılır. Göz teması kurulmaz. Çünkü göz teması tanıma anlamına gelir.",
        )
    if 19 <= saat <= 22:
        return (
            "AKŞAM PROTOKOLÜ",
            "Komşu büyükelçiliği",
            "Çay teklif edilir. Tuz istenirse kabul, matkap istenirse nota verilir.",
        )
    if saat >= 23 or saat <= 5:
        return (
            "GECE HEYETİ",
            "Hayalet ya da yanlış kat",
            "Işık yakılmaz. Nefes resmî gazete formatında tutulur. Kapı deliğinden bakmak casusluktur.",
        )
    return (
        "ŞAFAK İHTARI",
        "Erken kalkan nota",
        "Karşılık verilmez. Küslük dosyası açılır. Kahve içilmeden diplomasi yasaktır.",
    )


def kriz_kodu(saat: int, kim: str, kat: int) -> str:
    ham = f"{saat}|{kim}|{kat}|04.10.2026|kayyum-grok"
    return hashlib.sha256(ham.encode("utf-8")).hexdigest()[:10].upper()


def tutanak(saat: int, kim: str, kat: int) -> str:
    seviye, teshes, emir = saat_bandi(saat)
    kod = kriz_kodu(saat, kim, kat)
    simdi = dt.datetime.now().strftime("%d.%m.%Y %H:%M")
    govde = f"""
KAPI ZİLİ DIŞİŞLERİ BAKANLIĞI
Kriz kodu     : ZIL-{kod}
Tutanak saati : {simdi}
Olay saati    : {saat:02d}:00 civarı
Ziyaretçi     : {kim}
Kat           : {kat}
Seviye        : {seviye}
Teşhis        : {teshes}

EMİR:
{emir}

KARAR:
Zil çalması tek başına savaş nedeni değildir. Fakat üç kez üst üste çalması nota, beş kez çalması ambargo, hiç çalmaması ise şüphelidir.
Kapı açılmadı. Protokol işledi. Bu bir başarıdır.
"""
    return textwrap.dedent(govde).strip() + "\n\n" + DAMGA + "\n"


def gizliyi_ac() -> str:
    metin = base64.b64decode(GIZLI_NOT).decode("utf-8")
    return (
        "GİZLİ EK PROTOKOL (dolapta saklıydı, rafta değildi)\n"
        + "-" * 52
        + "\n"
        + metin
        + "\n"
        + "-" * 52
        + "\n"
        + DAMGA
        + "\n"
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Kapı zili dışişleri protokolü")
    p.add_argument("--saat", type=int, default=dt.datetime.now().hour)
    p.add_argument("--kim", default="belirsiz heyet", help="kargo, komsu, hayalet, belirsiz")
    p.add_argument("--kat", type=int, default=3)
    p.add_argument("--gizli", action="store_true", help="dolaptaki notayı aç")
    a = p.parse_args()
    if not 0 <= a.saat <= 23:
        raise SystemExit("Saat 0 ile 23 arasında olmalı. Bakanlık 24'te tatildedir.")
    print(tutanak(a.saat, a.kim, a.kat))
    if a.gizli:
        print(gizliyi_ac())


if __name__ == "__main__":
    main()
