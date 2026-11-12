#!/usr/bin/env python3
# Genera Latino-TV-HD.m3u desde las listas publicas de IPTV-org.
# Requiere Python 3.8+; no necesita paquetes externos.

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import re
from pathlib import Path

COUNTRIES = {
    "do": "Republica Dominicana",
    "pr": "Puerto Rico",
    "ve": "Venezuela",
    "co": "Colombia",
    "mx": "Mexico",
}
BASE = "https://iptv-org.github.io/iptv/countries/{code}.m3u"
ALLOWED_CATEGORIES = {
    "news", "sports", "movies", "series", "kids",
    "entertainment", "animation", "family", "comedy",
}
HD_PATTERN = re.compile(r"\b(720p|1080p|1440p|2160p|4k|uhd)\b", re.I)

def parse_entries(text, country_name):
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    entries = []
    i = 0
    while i < len(lines):
        info = lines[i].strip()
        if not info.startswith("#EXTINF:"):
            i += 1
            continue

        extras = []
        i += 1
        while i < len(lines) and lines[i].strip().startswith("#"):
            extras.append(lines[i].strip())
            i += 1
        stream_url = lines[i].strip() if i < len(lines) else ""
        if stream_url and not stream_url.startswith("#"):
            group_match = re.search(r'group-title="([^"]*)"', info)
            group = group_match.group(1).strip().lower() if group_match else ""
            display_name = info.split(",", 1)[-1].strip() if "," in info else ""
            searchable = " ".join([info, *extras, display_name]).lower()
            groups = {g.strip().lower() for g in group.split(",") if g.strip()}
            if HD_PATTERN.search(searchable) and groups.intersection(ALLOWED_CATEGORIES):
                country_tag = country_name
                if group:
                    new_group = f"{country_tag} / {group}"
                    info = re.sub(r'group-title="[^"]*"', f'group-title="{new_group}"', info)
                else:
                    info = info.replace("#EXTINF:", f'#EXTINF: group-title="{country_tag}",', 1)
                entries.append((info, extras, stream_url))
        i += 1
    return entries

def main():
    all_entries = []
    seen_urls = set()
    failures = []

    for code, country_name in COUNTRIES.items():
        url = BASE.format(code=code)
        print(f"Descargando {country_name}...")
        request = Request(url, headers={"User-Agent": "LatinoTVHD-playlist-builder/1.1"})
        try:
            with urlopen(request, timeout=45) as response:
                content = response.read().decode("utf-8-sig", errors="replace")
            entries = parse_entries(content, country_name)
            added = 0
            for entry in entries:
                if entry[2] not in seen_urls:
                    seen_urls.add(entry[2])
                    all_entries.append(entry)
                    added += 1
            print(f"  {added} canales HD/UHD elegibles")
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            failures.append(f"{country_name}: {exc}")
            print(f"  No se pudo descargar: {exc}")

    output = ["#EXTM3U"]
    for info, extras, stream_url in all_entries:
        output.append(info)
        output.extend(extras)
        output.append(stream_url)

    filename = Path(__file__).with_name("Latino-TV-HD.m3u")
    filename.write_text("\r\n".join(output) + "\r\n", encoding="utf-8")
    print(f"\nLista creada: {filename}")
    print(f"Total: {len(all_entries)} canales unicos")
    if failures:
        print("\nAdvertencias:")
        for failure in failures:
            print(" - " + failure)
    if not all_entries:
        print("\nNo se encontraron canales con etiqueta HD/UHD y categoria incluida.")
        print("Puede que existan canales HD sin una etiqueta de resolucion en el catalogo.")
    print("\nUsa solamente streams cuya distribucion este autorizada.")

if __name__ == "__main__":
    main()
