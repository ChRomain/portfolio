import piexif
import json
import os
import shutil
import re
import numpy as np
from PIL import Image, ImageOps

SOURCE_DIR = "/Users/romaincharretteur/pCloud Drive/Portfolio_Images"
CONTENT_DIR = "./content/gallery"
ASSETS_DIR = "./static/gallery" 

# --- PARAMÈTRES D'OPTIMISATION ---
QUALITY = 55          # Qualité WebP
MAX_WIDTH = 1600      # Largeur max

# --- BASE DE DONNÉES VIDÉOS ---
VIDEOS = {
    "new_york": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-12-06%2023-47-51.mp4",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-12-08%2012-20-58.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-06-23%2013-16-26.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-12-06%2000-27-10.mov"
    ],
    "finistere": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-05-21%2017-30-11.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-12-19%2014-54-12.mp4",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-12-19%2014-53-02.mp4"
    ],
    "new_hampshire": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-10-06%2011-54-14.mov"
    ],
    "montreal": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-07-07%2000-04-23.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-07-09%2021-46-58.mov"
    ],
    "niagara_falls": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-08-24%2010-38-55.mp4",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-08-24%2013-22-45.mp4"
    ],
    "quebec": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-10-14%2000-31-25.mov"
    ],
    "canada": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-07-08%2023-38-40.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-02-11%2014-29-22.mov"
    ],
    "guatemala": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-09-10%2014-31-25.mp4",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-01-23%2010-52-09.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-09-03%2008-48-03.mp4",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2025-09-11%2019-05-15.mov"
    ],
    "keys": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-07%2019-10-13.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-07%2023-15-36.mov"
    ],
    "miami": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-07-17.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-08-17.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-06-15.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-05%2020-26-44.mov"
    ],
    "everglades": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-09-58.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-12-38.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-13-27.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-14-12.mov",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-04-09%2000-14-59.mov"
    ],
    "machu_picchu": [
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-07-16%2022-42-17.mp4",
        "https://pub-4f55cfaeea7f4e58ae5f19966ae63baf.r2.dev/2026-07-16%2022-43-50.mp4"
    ]
}

# --- CATÉGORIES VIDÉO (filtres de la page /videos/) ---
# Alignées sur les groupes de layouts/index.html et sur les clés i18n cat_*.
VIDEO_CATEGORIES = {
    "new_york": "urban", "miami": "urban",
    "finistere": "wild", "new_hampshire": "wild", "niagara_falls": "wild",
    "keys": "wild", "everglades": "wild",
    "montreal": "canada", "quebec": "canada", "canada": "canada",
    "guatemala": "latam", "machu_picchu": "latam",
}

# --- DESCRIPTIONS DES DESTINATIONS (texte intro par langue) ---
# Contenu éditorial externalisé dans data/destination_descriptions.json
# pour ne pas mélanger texte et logique, et garder des diffs Git lisibles.
with open("data/destination_descriptions.json", "r", encoding="utf-8") as _f:
    DESCRIPTIONS = json.load(_f)

# --- TAGS DE MOOD PAR PHOTO (analyse visuelle réelle, pas une heuristique) ---
# Produit par un passage d'analyse d'image par photo (voir data/photo_tags.json).
# Clé = slug (nom de fichier sans extension), valeur = liste de tags parmi la
# taxonomie fixe. Une photo absente de ce fichier (nouvel ajout pas encore
# analysé) reçoit simplement une liste vide, jamais un tag deviné.
PHOTO_TAGS_PATH = "data/photo_tags.json"
if os.path.exists(PHOTO_TAGS_PATH):
    with open(PHOTO_TAGS_PATH, "r", encoding="utf-8") as _f:
        PHOTO_TAGS = json.load(_f)
else:
    PHOTO_TAGS = {}

# --- MAPPING DOSSIER -> PAYS (pour stats carte) ---
FOLDER_TO_COUNTRY = {
    "paris": "France", "lyon": "France", "bordeaux": "France", "corse": "France", "finistere": "France",
    "rome": "Italie", "naples": "Italie",
    "suede": "Suède",
    "montenegro": "Monténégro",
    "new_york": "USA", "washington": "USA", "boston": "USA", "philadelphie": "USA", "cape_cod": "USA", "maine": "USA", "vermont": "USA", "new_hampshire": "USA", "miami": "USA", "keys": "USA", "everglades": "USA", "chicago": "USA",
    "montreal": "Canada", "quebec": "Canada", "ottawa": "Canada", "toronto": "Canada", "niagara_falls": "Canada", "canada": "Canada",
    "guatemala": "Guatemala",
    "indonesie": "Indonésie",
    "peru": "Pérou"
}

# --- MAPPING PAYS -> CODE ISO 3166-1 alpha-2 ---
# Consommé par layouts/partials/flag-badge.html, qui lit .Params.country_code.
# Ce champ n'était écrit nulle part : le badge drapeau ne s'affichait donc jamais.
COUNTRY_TO_CODE = {
    "France": "fr",
    "Italie": "it",
    "Suède": "se",
    "Monténégro": "me",
    "USA": "us",
    "Canada": "ca",
    "Guatemala": "gt",
    "Indonésie": "id",
    "Pérou": "pe",
    "Guadeloupe": "gp",
}

# --- DICTIONNAIRES SEO POUR L'IA SÉMANTIQUE ---
SEO_VOCAB = {
    "fr": {
        "neige": ["hivernale", "enneigée", "glaciale", "pure"],
        "ocean": ["maritime", "aquatique", "côtière", "azur"],
        "sunset": ["crépusculaire", "dorée", "chaleureuse", "poétique"],
        "nature": ["sauvage", "verdoyante", "naturelle", "organique"],
        "urban": ["urbaine", "architecturale", "citadine", "moderne"],
        "vintage": ["nostalgique", "historique", "intemporelle", "rétro"],
        "warm": "aux tons chauds",
        "cold": "aux reflets froids",
        "lush": "luxuriante",
        "bright": "lumineuse",
        "dark": "sombre et mystérieuse",
        "templates": [
            "Une vue {mood} de {location}. {spec}",
            "Cliché {mood} immortalisé à {location} par Romain Charretteur.",
            "Atmosphère {mood} à {location}, une photographie {spec}.",
            "Exploration visuelle de {location}, révélant une esthétique {mood}."
        ]
    },
    "en": {
        "neige": ["wintry", "snowy", "frozen", "pure"],
        "ocean": ["maritime", "aquatic", "coastal", "azure"],
        "sunset": ["cinematic", "golden", "warm", "poetic"],
        "nature": ["wild", "green", "natural", "organic"],
        "urban": ["urban", "architectural", "modern", "vibrant"],
        "vintage": ["nostalgic", "historic", "timeless", "retro"],
        "warm": "with warm tones",
        "cold": "with cold reflections",
        "lush": "lush and vibrant",
        "bright": "bright and clear",
        "dark": "dark and mysterious",
        "templates": [
            "A {mood} view of {location}. {spec}",
            "Capturing the {mood} essence of {location}. Photo by Romain Charretteur.",
            "The {mood} atmosphere of {location}, a {spec} shot.",
            "Visual exploration of {location}, featuring a {mood} aesthetic."
        ]
    },
    "es": {
        "neige": ["invernal", "nevada", "glacial", "pura"],
        "ocean": ["marítima", "acuática", "costera", "azul"],
        "sunset": ["cinematográfica", "dorada", "cálida", "poética"],
        "nature": ["salvaje", "verde", "natural", "orgánica"],
        "urban": ["urbana", "arquitectónica", "moderna", "vibrante"],
        "vintage": ["nostálgica", "histórica", "atemporal", "retro"],
        "warm": "con tonos cálidos",
        "cold": "con reflejos fríos",
        "lush": "exuberante",
        "bright": "luminosa",
        "dark": "oscura y misteriosa",
        "templates": [
            "Una vista {mood} de {location}. {spec}",
            "Capturando la esencia {mood} de {location}. Foto de Romain Charretteur.",
            "La atmósfera {mood} de {location}, una toma {spec}.",
            "Exploración visual de {location}, con una estética {mood}."
        ]
    }
}

import random

def build_meta_description(gallery_desc, fallback, max_len=155):
    """Dérive une meta description unique à partir du texte d'intro réel de la
    destination (au lieu du gabarit générique dupliqué sur toutes les pages)."""
    text = re.sub(r'&nbsp;|<[^>]+>', ' ', gallery_desc or "").strip()
    text = re.sub(r'\s+', ' ', text)
    if not text:
        return fallback
    if len(text) <= max_len:
        return text
    truncated = text[:max_len].rsplit(' ', 1)[0]
    return truncated + "…"

def generate_smart_alt(lang, location, tags, color_mood):
    vocab = SEO_VOCAB.get(lang, SEO_VOCAB["en"])
    
    # Choisir un mood au hasard parmi les tags ou défaut
    default_mood = {"fr": "unique", "en": "unique", "es": "única"}.get(lang, "unique")
    mood_word = default_mood
    if tags:
        primary_tag = tags[0]
        words = vocab.get(primary_tag, [default_mood])
        mood_word = random.choice(words) if isinstance(words, list) else words
        
    default_spec = {"fr": "artistique", "en": "artistic", "es": "artística"}.get(lang, "artistic")
    spec_word = vocab.get(color_mood, default_spec)
    template = random.choice(vocab["templates"])
    
    return template.format(mood=mood_word, location=location, spec=spec_word)

# --- COORDONNÉES PAR DÉFAUT (Fallback si pas de GPS dans les photos) ---
DEFAULT_GPS = {
    "paris": [48.8566, 2.3522], "lyon": [45.7640, 4.8357], "bordeaux": [44.8378, -0.5792], "corse": [42.0396, 9.0129], "finistere": [48.3147, -4.1441],
    "rome": [41.9028, 12.4964], "naples": [40.8518, 14.2681],
    "suede": [59.3293, 18.0686],
    "montenegro": [42.7087, 19.3744],
    "new_york": [40.7128, -74.0060], "washington": [38.9072, -77.0369], "boston": [42.3601, -71.0589], "philadelphie": [39.9526, -75.1652], "cape_cod": [41.6688, -70.2962], "maine": [45.2538, -69.4455], "vermont": [44.5588, -72.5778], "new_hampshire": [43.1939, -71.5724], "miami": [25.7617, -80.1918], "keys": [24.5551, -81.7800], "everglades": [25.2866, -80.8987], "chicago": [41.8781, -87.6298],
    "montreal": [45.5017, -73.5673], "quebec": [46.8139, -71.2080], "ottawa": [45.4215, -75.6972], "toronto": [43.6532, -79.3832], "niagara_falls": [43.0896, -79.0849], "canada": [45.5017, -73.5673],
    "guatemala": [15.7835, -90.2308],
    "indonesie": [-8.4095, 115.1889],
    "peru": [-12.04637, -77.04279]
}

# --- COORDONNÉES DES DESTINATIONS DU PÉROU ---
PERU_COORDS = {
    "lima": [-12.04637, -77.04279],
    "paracas": [-13.7144, -76.2505],
    "huacachina": [-14.0875, -75.7633],
    "nazca": [-14.8307, -74.9386],
    "arequipa": [-16.4090, -71.5375],
    "colca_canyon": [-15.6092, -71.8874],
    "sacred_valley": [-13.3278, -72.0734],
    "salineras_de_maras": [-13.3045, -72.1554],
    "rainbow_mountain": [-13.8633, -71.3028],
    "aguas_calientes": [-13.1551, -72.5249],
    "machu_picchu": [-13.1631, -72.5450]
}

def clean_name(name):
    name = name.lower().replace(" ", "_")
    name = re.sub(r'[^a-z0-9_]+', '', name)
    return name.strip('_')

def get_decimal_from_dms(dms, ref):
    if not dms or len(dms) != 3: return None
    try:
        degrees = dms[0][0] / dms[0][1] if dms[0][1] != 0 else 0
        minutes = dms[1][0] / dms[1][1] if dms[1][1] != 0 else 0
        seconds = dms[2][0] / dms[2][1] if dms[2][1] != 0 else 0
        val = degrees + (minutes / 60.0) + (seconds / 3600.0)
        if ref in [b'S', b'W', 'S', 'W']:
            val = -val
        return val
    except:
        return None

def get_photo_tone(img):
    """Calcule la couleur dominante et une tonalité (or/bleu/vert/rouge/neutre/sombre)
    à partir de l'image RÉELLE déjà chargée (pas une vignette LQIP 20x20, dont la
    moyenne de pixels floutée produisait des tonalités fausses).

    Ne se contente pas de prendre la couleur la plus fréquente après quantification :
    sur une photo de paysage, un rocher ou un premier plan sombre couvre souvent plus
    de pixels que le ciel/l'océan qui définit pourtant la tonalité perçue. On calcule
    donc une teinte moyenne circulaire sur les pixels "vifs" (saturés et lumineux) et
    on ne bascule en sombre/neutre que si l'image n'a pas assez de pixels vifs."""
    try:
        small = img.convert('RGB').resize((120, 120))
        arr = np.asarray(small, dtype=np.float64) / 255.0
        r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
        maxc = arr.max(axis=-1)
        minc = arr.min(axis=-1)
        delta = maxc - minc
        v = maxc
        s = np.divide(delta, maxc, out=np.zeros_like(maxc), where=maxc > 1e-9)

        safe_delta = np.where(delta > 1e-9, delta, 1.0)
        rc, gc, bc = (maxc - r) / safe_delta, (maxc - g) / safe_delta, (maxc - b) / safe_delta
        hue = np.zeros_like(maxc)
        hue = np.where((maxc == r) & (delta > 1e-9), bc - gc, hue)
        hue = np.where((maxc == g) & (delta > 1e-9), 2.0 + rc - bc, hue)
        hue = np.where((maxc == b) & (delta > 1e-9), 4.0 + gc - rc, hue)
        hue_deg = (hue / 6.0) % 1.0 * 360.0

        avg_v = float(v.mean())
        vivid = (s > 0.25) & (v > 0.25)
        vivid_frac = float(vivid.mean())

        if vivid_frac > 0.03:
            hues_rad = np.deg2rad(hue_deg[vivid])
            mean_hue = np.degrees(np.arctan2(np.sin(hues_rad).mean(), np.cos(hues_rad).mean())) % 360
            mean_rgb = arr[vivid].mean(axis=0) * 255
        else:
            mean_hue = None
            mean_rgb = arr.reshape(-1, 3).mean(axis=0) * 255

        hex_color = '#%02x%02x%02x' % tuple(int(round(c)) for c in mean_rgb)

        if avg_v < 0.22:
            tone = "sombre"
        elif mean_hue is None:
            tone = "neutre"
        elif mean_hue < 25 or mean_hue >= 345:
            tone = "rouge"
        elif mean_hue < 70:
            tone = "or"
        elif mean_hue < 170:
            tone = "vert"
        elif mean_hue < 255:
            tone = "bleu"
        else:
            tone = "rouge"

        return hex_color, tone
    except Exception:
        return "", ""

# --- MOT-CLÉ SEO PAR TONALITÉ (remplace l'ancienne classification par seuils RGB) ---
TONE_TO_COLOR_MOOD = {
    "or": "warm", "rouge": "warm", "bleu": "cold",
    "vert": "lush", "sombre": "dark", "neutre": "bright"
}

def get_exif_data(img_path):
    """Extrait les réglages techniques, les coordonnées GPS et la date de l'image"""
    try:
        img = Image.open(img_path)
        exif_raw = img.info.get('exif')
        if not exif_raw: return "", "", ""
        
        exif_dict = piexif.load(exif_raw)
        
        # 1. Extraction EXIF Classique
        # NB : certains boîtiers (drones DJI notamment) complètent les chaînes EXIF avec
        # des octets NUL. .strip() ne les retire pas, et ils finissaient écrits tels quels
        # dans les attributs title= du markdown, ce qui rendait les fichiers binaires
        # pour grep/diff. On les enlève explicitement.
        def _clean(raw):
            return raw.decode(errors="replace").replace("\x00", "").strip()

        model = _clean(exif_dict.get('0th', {}).get(piexif.ImageIFD.Model, b""))
        f_stop = exif_dict.get('Exif', {}).get(piexif.ExifIFD.FNumber)
        iso = exif_dict.get('Exif', {}).get(piexif.ExifIFD.ISOSpeedRatings)
        shutter = exif_dict.get('Exif', {}).get(piexif.ExifIFD.ExposureTime)
        date_raw = _clean(exif_dict.get('Exif', {}).get(piexif.ExifIFD.DateTimeOriginal, b""))
        
        parts = []
        if model: parts.append(model)
        if f_stop: parts.append(f"f/{f_stop[0]/f_stop[1]}")
        if shutter:
            val = f"{shutter[0]}/{shutter[1]}s" if shutter[1] > 1 else f"{shutter[0]}s"
            parts.append(val)
        if iso: parts.append(f"ISO {iso}")
        exif_str = " | ".join(parts)
        
        # Formatage Date (YYYY:MM:DD HH:MM:SS -> YYYY-MM-DD)
        date_str = ""
        if date_raw:
            date_str = date_raw.split(" ")[0].replace(":", "-")

        # 2. Extraction GPS
        gps_str = ""
        gps_dict = exif_dict.get('GPS', {})
        if gps_dict:
            lat = gps_dict.get(2)
            lat_ref = gps_dict.get(1)
            lng = gps_dict.get(4)
            lng_ref = gps_dict.get(3)
            if lat and lat_ref and lng and lng_ref:
                lat_dec = get_decimal_from_dms(lat, lat_ref)
                lng_dec = get_decimal_from_dms(lng, lng_ref)
                if lat_dec is not None and lng_dec is not None:
                    gps_str = f"{lat_dec:.5f},{lng_dec:.5f}"
                    
        return exif_str, gps_str, date_str
    except Exception:
        return "", "", ""

def _snapshot_content_dir(content_dir):
    """Capture le contenu existant avant régénération, pour préserver les données
    écrites à la main (ex: itinerary_days) que le générateur ne connaît pas, et pour
    ne pas perdre les destinations qui n'ont pas (encore) de dossier photo source."""
    snapshot = {}
    if not os.path.exists(content_dir):
        return snapshot
    for folder in os.listdir(content_dir):
        folder_path = os.path.join(content_dir, folder)
        if not os.path.isdir(folder_path):
            continue
        files = {}
        for fname in os.listdir(folder_path):
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(folder_path, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                files[fname] = f.read()
        snapshot[folder] = files
    return snapshot

def _extract_itinerary_days_block(text):
    match = re.search(r'^itinerary_days:\n(?:[ \t]+.*\n?)*', text, re.MULTILINE)
    return match.group(0).rstrip("\n") + "\n" if match else None

def _restore_preserved_content(content_dir, snapshot, generated_folders):
    """Après régénération : restaure intégralement les destinations sans dossier photo
    source (le générateur ne les a jamais touchées), et réinjecte itinerary_days dans
    les destinations régénérées qui l'avaient avant."""
    for folder, files in snapshot.items():
        folder_path = os.path.join(content_dir, folder)

        if folder not in generated_folders:
            os.makedirs(folder_path, exist_ok=True)
            for fname, text in files.items():
                fpath = os.path.join(folder_path, fname)
                if not os.path.exists(fpath):
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(text)
            continue

        for fname, old_text in files.items():
            block = _extract_itinerary_days_block(old_text)
            if not block:
                continue
            fpath = os.path.join(folder_path, fname)
            if not os.path.exists(fpath):
                continue
            with open(fpath, "r", encoding="utf-8") as f:
                new_text = f.read()
            if "itinerary_days:" in new_text:
                continue
            parts = new_text.split("---", 2)
            if len(parts) < 3:
                continue
            parts[1] = parts[1].rstrip("\n") + "\n" + block
            with open(fpath, "w", encoding="utf-8") as f:
                f.write("---".join(parts))

def sync_portfolio():
    content_snapshot = _snapshot_content_dir(CONTENT_DIR)
    generated_folders = set()

    if os.path.exists(CONTENT_DIR): shutil.rmtree(CONTENT_DIR)
    # On ne supprime plus ASSETS_DIR pour permettre l'incrémental

    os.makedirs(CONTENT_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    total_images_count = 0
    all_locations = []

    for folder in os.listdir(SOURCE_DIR):
        source_folder_path = os.path.join(SOURCE_DIR, folder)
        if not os.path.isdir(source_folder_path): continue

        folder_clean = clean_name(folder)
        generated_folders.add(folder_clean)
        display_title = folder.replace('_', ' ').title()
        
        # --- CAS SPÉCIAL DU PÉROU (Toutes les destinations dans une seule page) ---
        if folder_clean == "peru":
            peru_subfolders = [
                d for d in os.listdir(source_folder_path)
                if os.path.isdir(os.path.join(source_folder_path, d))
            ]
            
            peru_route_order = [
                "lima", "paracas", "huacachina", "nazca", "arequipa", "colca_canyon",
                "sacred_valley", "salineras_de_maras", "rainbow_mountain", "aguas_calientes", "machu_picchu"
            ]
            
            subfolder_map = {clean_name(sf): sf for sf in peru_subfolders}
            ordered_clean_subs = [x for x in peru_route_order if x in subfolder_map]
            for sf_clean in subfolder_map:
                if sf_clean not in ordered_clean_subs:
                    ordered_clean_subs.append(sf_clean)
                    
            peru_images_metadata = []
            peru_itinerary_data = []
            
            hugo_assets_path = os.path.join(ASSETS_DIR, "peru")
            hugo_content_path = os.path.join(CONTENT_DIR, "peru")
            os.makedirs(hugo_assets_path, exist_ok=True)
            os.makedirs(hugo_content_path, exist_ok=True)
            
            peru_dom_color = ""
            peru_mood_tags = set()
            first_image_overall = None
            
            for sf_clean in ordered_clean_subs:
                sf_original = subfolder_map[sf_clean]
                sub_source_path = os.path.join(source_folder_path, sf_original)
                
                sf_gps = PERU_COORDS.get(sf_clean)
                sf_date = None
                
                sf_images = [f for f in os.listdir(sub_source_path) if f.lower().endswith(('jpg', 'jpeg', 'png', 'webp'))]
                sf_images.sort()
                
                sf_count = 0
                sf_cover = None
                
                for idx, img_name in enumerate(sf_images):
                    img_num = idx + 1
                    img_clean = f"peru_{sf_clean}_{img_num:03d}.webp"
                    target_path = os.path.join(hugo_assets_path, img_clean)
                    full_source_path = os.path.join(sub_source_path, img_name)
                    
                    exif_info, gps_info, date_info = get_exif_data(full_source_path)
                    
                    if gps_info and not sf_gps:
                        try:
                            lat_s, lng_s = gps_info.split(',')
                            sf_gps = [float(lat_s), float(lng_s)]
                        except: pass
                    
                    if date_info and not sf_date:
                        sf_date = date_info
                        
                    gps_attr = f' data-gps="{gps_info}"' if gps_info else ""
                    img_slug = os.path.splitext(img_clean)[0]
                    img_tags = PHOTO_TAGS.get(img_slug, [])
                    peru_mood_tags.update(img_tags)

                    try:
                        if not os.path.exists(target_path):
                            img = Image.open(full_source_path)
                            img = ImageOps.exif_transpose(img)
                            width, height = img.size

                            if img.width > MAX_WIDTH:
                                ratio = MAX_WIDTH / float(img.width)
                                new_height = int(float(img.height) * float(ratio))
                                img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                                width, height = MAX_WIDTH, new_height

                            img.save(target_path, "WEBP", quality=QUALITY, method=6)
                            print(f"    ↳ [{img_num}/{len(sf_images)}] {sf_clean}/{img_clean} optimisée.")
                        else:
                            img = Image.open(target_path)
                            width, height = img.size

                        hex_color, tone = get_photo_tone(img)
                        if not peru_dom_color:
                            peru_dom_color = hex_color

                        try:
                            lqip_basename = os.path.splitext(img_clean)[0]
                            lqip_dir = os.path.join(hugo_assets_path, "lqip")
                            lqip_path = os.path.join(lqip_dir, f"{lqip_basename}.jpg")
                            lqip_url = f"/gallery/peru/lqip/{lqip_basename}.jpg"
                            if not os.path.exists(lqip_path):
                                os.makedirs(lqip_dir, exist_ok=True)
                                lqip_img = img.copy()
                                lqip_img.thumbnail((20, 20), Image.Resampling.LANCZOS)
                                lqip_img.save(lqip_path, format="JPEG", quality=30)
                            lqip_style = f'background-image: url({lqip_url}); background-size: cover;'
                        except Exception as e:
                            print(f"Error generating LQIP for {img_clean}: {e}")
                            lqip_style = ""
                            
                        color_mood = TONE_TO_COLOR_MOOD.get(tone, "unique")

                        img_src = f"/gallery/peru/{img_clean}"
                        if not first_image_overall:
                            first_image_overall = img_src
                        if not sf_cover:
                            sf_cover = img_src

                        peru_images_metadata.append({
                            "src": img_src,
                            "title": exif_info,
                            "gps": gps_attr,
                            "width": width,
                            "height": height,
                            "tags": img_tags,
                            "color": hex_color,
                            "tone": tone,
                            "color_mood": color_mood,
                            "lqip_style": lqip_style,
                            "destination": sf_clean
                        })
                        
                        total_images_count += 1
                        sf_count += 1
                    except Exception as e:
                        print(f"❌ Erreur sur {img_name} ({sf_clean}): {e}")
                
                if not sf_date:
                    date_map = {
                        "lima": "2026-06-20", "paracas": "2026-06-22", "huacachina": "2026-06-23",
                        "nazca": "2026-06-24", "arequipa": "2026-06-25", "colca_canyon": "2026-06-27",
                        "sacred_valley": "2026-06-29", "salineras_de_maras": "2026-06-29",
                        "rainbow_mountain": "2026-06-30", "aguas_calientes": "2026-07-02", "machu_picchu": "2026-07-03"
                    }
                    sf_date = date_map.get(sf_clean, "2026-07-01")
                    
                if not sf_gps:
                    sf_gps = PERU_COORDS.get(sf_clean, [-12.04637, -77.04279])
                    
                peru_itinerary_data.append({
                    "id": sf_clean,
                    "name": sf_original.replace('_', ' ').title(),
                    "coords": sf_gps,
                    "date": sf_date,
                    "cover": sf_cover or "",
                    "count": sf_count
                })
            
            if first_image_overall:
                shutil.copy(os.path.join("./static", first_image_overall.lstrip("/")), os.path.join(hugo_content_path, "feature.webp"))
            
            languages = {
                "en": {"file": "index.md", "title": "Peru", "desc_prefix": "Explore my immersive photography portfolio from Peru."},
                "fr": {"file": "index.fr.md", "title": "Pérou", "desc_prefix": "Découvrez mes plus beaux clichés et récits de voyage au Pérou."},
                "es": {"file": "index.es.md", "title": "Perú", "desc_prefix": "Explore mi portafolio fotográfico inmersivo de Perú."}
            }
            
            gallery_desc_map = DESCRIPTIONS.get("peru", {})
            
            for lang, config in languages.items():
                filename = config["file"]
                gallery_desc = gallery_desc_map.get(lang, "")
                fallback_desc = f"{config['desc_prefix']} Un carnet de voyage visuel par Romain Charretteur."
                meta_desc = build_meta_description(gallery_desc, fallback_desc)
                
                lang_gallery_html = ""
                for img_index, img_data in enumerate(peru_images_metadata):
                    alt_seo = generate_smart_alt(lang, config["title"], img_data['tags'], img_data['color_mood'])
                    loading_attrs = 'loading="eager" fetchpriority="high" decoding="async"' if img_index == 0 else 'loading="lazy" decoding="async"'
                    lang_gallery_html += f'    <img src="{img_data["src"]}" \n'
                    lang_gallery_html += f'         alt="{alt_seo}" \n'
                    lang_gallery_html += f'         title="{img_data["title"]}" \n'
                    lang_gallery_html += f'         {img_data["gps"]} \n'
                    lang_gallery_html += f'         data-destination="{img_data["destination"]}" \n'
                    lang_gallery_html += f'         data-color="{img_data["color"]}" \n'
                    lang_gallery_html += f'         data-tone="{img_data["tone"]}" \n'
                    lang_gallery_html += f'         data-tags="{",".join(img_data["tags"])}" \n'
                    lang_gallery_html += f'         width="{img_data["width"]}" height="{img_data["height"]}" \n'
                    lang_gallery_html += f'         {loading_attrs} \n'
                    lang_gallery_html += f'         data-lqip="true" \n'
                    lang_gallery_html += f'         style="{img_data["lqip_style"]}" \n'
                    lang_gallery_html += f'         onload="this.classList.add(\'loaded\')" />\n'

                with open(os.path.join(hugo_content_path, filename), "w") as f:
                    f.write('---\n')
                    f.write(f'title: "{config["title"]}"\n')
                    f.write(f'description: {json.dumps(meta_desc, ensure_ascii=False)}\n')
                    f.write(f'layout: "peru"\n')
                    f.write(f'images: ["/gallery/peru/feature.webp"]\n')
                    f.write(f'dominant_color: "{peru_dom_color}"\n')
                    f.write(f'tags: {json.dumps(list(peru_mood_tags))}\n')
                    if COUNTRY_TO_CODE.get(FOLDER_TO_COUNTRY.get(folder_clean, "")):
                        f.write(f'country_code: "{COUNTRY_TO_CODE[FOLDER_TO_COUNTRY[folder_clean]]}"\n')
                    f.write(f'itinerary: {json.dumps(peru_itinerary_data)}\n')
                    f.write(f'intro_text: {json.dumps(gallery_desc)}\n')
                    f.write('---\n\n')
                    f.write(f'{{{{< gallery >}}}}\n{lang_gallery_html}{{{{< /gallery >}}}}')
            
            peru_gps = PERU_COORDS.get("lima", [-12.04637, -77.04279])
            all_locations.append({
                "name": display_title,
                "coords": peru_gps,
                "url": "/gallery/peru/",
                "country": "Pérou",
                "date": "2026-06-20",
                "color": peru_dom_color,
                "tags": list(peru_mood_tags)
            })
            
            print(f"✅ Pérou : {len(peru_images_metadata)} photos synchronisées sur l'ensemble des destinations.")
            continue
        
        hugo_content_path = os.path.join(CONTENT_DIR, folder_clean)
        hugo_assets_path = os.path.join(ASSETS_DIR, folder_clean)
        os.makedirs(hugo_content_path, exist_ok=True)
        os.makedirs(hugo_assets_path, exist_ok=True)

        # Représentant GPS et Date pour la carte
        folder_gps = None
        folder_date = None

        # On prépare le bloc HTML qui ira dans {{< gallery >}}
        images_metadata = []

        # --- 1. AJOUT DES VIDÉOS SI ELLES EXISTENT ---
        video_html_snippets = []
        if folder_clean in VIDEOS:
            for v_url in VIDEOS[folder_clean]:
                video_html_snippets.append(f'  <video autoplay loop muted playsinline preload="metadata" class="video-element"><source src="{v_url}" type="video/mp4"></video>\n')

        images = [f for f in os.listdir(source_folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png', 'webp'))]
        dom_color = ""
        gallery_mood_tags = set()

        for i, img_name in enumerate(sorted(images)):
            img_num = i + 1
            img_clean = f"{folder_clean}_{img_num:03d}.webp"
            full_source_path = os.path.join(source_folder_path, img_name)
            target_path = os.path.join(hugo_assets_path, img_clean)
            
            exif_info, gps_info, date_info = get_exif_data(full_source_path)
            
            # Si on n'a pas encore de GPS ou Date pour ce dossier, on prend le premier valide
            if gps_info and not folder_gps:
                try:
                    lat_s, lng_s = gps_info.split(',')
                    folder_gps = [float(lat_s), float(lng_s)]
                except: pass
            
            if date_info and not folder_date:
                folder_date = date_info

            # SEO optimized alt text
            gps_attr = f' data-gps="{gps_info}"' if gps_info else ""
            
            try:
                if not os.path.exists(target_path):
                    img = Image.open(full_source_path)
                    img = ImageOps.exif_transpose(img)
                    width, height = img.size
                    
                    if img.width > MAX_WIDTH:
                        ratio = MAX_WIDTH / float(img.width)
                        new_height = int(float(img.height) * float(ratio))
                        img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                        width, height = MAX_WIDTH, new_height 

                    img.save(target_path, "WEBP", quality=QUALITY, method=6)
                    print(f"    ↳ [{img_num}/{len(images)}] {img_clean} optimisée.")
                else:
                    # On ouvre l'image existante pour extraire le LQIP et les dimensions
                    img = Image.open(target_path)
                    width, height = img.size

                img_slug = os.path.splitext(img_clean)[0]
                img_tags = PHOTO_TAGS.get(img_slug, [])
                gallery_mood_tags.update(img_tags)
                hex_color, tone = get_photo_tone(img)
                if not dom_color:
                    dom_color = hex_color

                # --- LQIP (Low-Quality Image Placeholder) ---
                # Écrit comme fichier statique séparé (mis en cache par le navigateur)
                # plutôt qu'inline en base64 dans le HTML (voir extraction historique
                # via scripts/extract_lqip.py pour le contenu déjà généré).
                try:
                    lqip_basename = os.path.splitext(img_clean)[0]
                    lqip_dir = os.path.join(hugo_assets_path, "lqip")
                    lqip_path = os.path.join(lqip_dir, f"{lqip_basename}.jpg")
                    lqip_url = f"/gallery/{folder_clean}/lqip/{lqip_basename}.jpg"
                    if not os.path.exists(lqip_path):
                        os.makedirs(lqip_dir, exist_ok=True)
                        lqip_img = img.copy()
                        lqip_img.thumbnail((20, 20), Image.Resampling.LANCZOS)
                        lqip_img.save(lqip_path, format="JPEG", quality=30)
                    lqip_style = f'background-image: url({lqip_url}); background-size: cover;'
                except Exception as e:
                    print(f"Error generating LQIP for {img_clean}: {e}")
                    lqip_style = ""

                color_mood = TONE_TO_COLOR_MOOD.get(tone, "unique")

                # Stocke les infos de l'image pour la génération multilingue
                images_metadata.append({
                    "src": f"/gallery/{folder_clean}/{img_clean}",
                    "title": exif_info,
                    "gps": gps_attr,
                    "width": width,
                    "height": height,
                    "tags": img_tags,
                    "color": hex_color,
                    "tone": tone,
                    "color_mood": color_mood,
                    "lqip_style": lqip_style
                })

                total_images_count += 1

            except Exception as e:
                print(f"❌ Erreur sur {img_name}: {e}")

        mood_tags = list(gallery_mood_tags)

        if images:
            first_img_renamed = f"{folder_clean}_001.webp"
            first_img_path = os.path.join(hugo_assets_path, first_img_renamed)
            shutil.copy(first_img_path, os.path.join(hugo_content_path, "feature.webp"))

        # Langues à générer
        languages = {
            "en": {
                "file": "index.md", 
                "title_prefix": "Travel photography gallery of", 
                "desc_prefix": "Explore my immersive photography portfolio from"
            },
            "fr": {
                "file": "index.fr.md", 
                "title_prefix": "Galerie photo de voyage à", 
                "desc_prefix": "Découvrez mes plus beaux clichés et récits de voyage à"
            },
            "es": {
                "file": "index.es.md", 
                "title_prefix": "Galería de fotos de viaje en", 
                "desc_prefix": "Explore mi portafolio fotográfico inmersivo de"
            }
        }

        gallery_desc_map = DESCRIPTIONS.get(folder_clean, {})
        if isinstance(gallery_desc_map, str):
            gallery_desc_map = {"en": gallery_desc_map, "fr": gallery_desc_map, "es": gallery_desc_map}

        for lang, config in languages.items():
            filename = config["file"]
            gallery_desc = gallery_desc_map.get(lang, "")
            fallback_desc = f"{config['desc_prefix']} {display_title}. Un carnet de voyage visuel par Romain Charretteur."
            meta_desc = build_meta_description(gallery_desc, fallback_desc)
            
            # --- GÉNÉRATION DU HTML SPÉCIFIQUE À LA LANGUE (POUR ALT SEO) ---
            lang_gallery_html = "".join(video_html_snippets)
            for img_index, img_data in enumerate(images_metadata):
                alt_seo = generate_smart_alt(lang, display_title, img_data['tags'], img_data['color_mood'])
                # La 1ère photo est visible immédiatement (pas de vidéo avant elle) : on la charge en priorité
                # plutôt qu'en lazy, sinon elle plombe le LCP (Largest Contentful Paint).
                is_lcp_candidate = img_index == 0 and not video_html_snippets
                loading_attrs = 'loading="eager" fetchpriority="high" decoding="async"' if is_lcp_candidate else 'loading="lazy" decoding="async"'
                lang_gallery_html += f'    <img src="{img_data["src"]}" \n'
                lang_gallery_html += f'         alt="{alt_seo}" \n'
                lang_gallery_html += f'         title="{img_data["title"]}" \n'
                lang_gallery_html += f'         {img_data["gps"]} \n'
                lang_gallery_html += f'         data-color="{img_data["color"]}" \n'
                lang_gallery_html += f'         data-tone="{img_data["tone"]}" \n'
                lang_gallery_html += f'         data-tags="{",".join(img_data["tags"])}" \n'
                lang_gallery_html += f'         width="{img_data["width"]}" height="{img_data["height"]}" \n'
                lang_gallery_html += f'         {loading_attrs} \n'
                lang_gallery_html += f'         data-lqip="true" \n'
                lang_gallery_html += f'         style="{img_data["lqip_style"]}" \n'
                lang_gallery_html += f'         onload="this.classList.add(\'loaded\')" />\n'

            with open(os.path.join(hugo_content_path, filename), "w") as f:
                f.write('---\n')
                f.write(f'title: "{display_title}"\n')
                f.write(f'description: {json.dumps(meta_desc, ensure_ascii=False)}\n')
                f.write(f'layout: "gallery"\n')
                if images:
                    f.write(f'images: ["/gallery/{folder_clean}/feature.webp"]\n')
                f.write(f'dominant_color: "{dom_color}"\n')
                f.write(f'tags: {json.dumps(mood_tags)}\n')
                if COUNTRY_TO_CODE.get(FOLDER_TO_COUNTRY.get(folder_clean, "")):
                    f.write(f'country_code: "{COUNTRY_TO_CODE[FOLDER_TO_COUNTRY[folder_clean]]}"\n')
                f.write('---\n\n')
                if gallery_desc:
                    f.write(f'<div class="gallery-description max-w-2xl mx-auto mb-8 text-neutral-600 dark:text-neutral-400 tracking-wide">\n{gallery_desc}\n</div>\n\n')
                
                f.write(f'{{{{< gallery >}}}}\n{lang_gallery_html}{{{{< /gallery >}}}}')
        
        
        # Ajout à la liste des points pour la carte
        # Fallback sur les coordonnées par défaut si pas de GPS trouvé
        if not folder_gps:
            folder_gps = DEFAULT_GPS.get(folder_clean)

        if folder_gps:
            all_locations.append({
                "name": display_title,
                "coords": folder_gps,
                "url": f"/gallery/{folder_clean}/",
                "country": FOLDER_TO_COUNTRY.get(folder_clean, "Inconnu"),
                "date": folder_date if folder_date else "2024-01-01",
                "color": dom_color,
                "tags": mood_tags
            })


        print(f"✅ {display_title} : {len(images)} photos synchronisées.")

    # --- 3. EXPORT DES STATISTIQUES ---
    stats = {
        "total_images": total_images_count
    }
    os.makedirs("data", exist_ok=True)
    with open("data/stats.json", "w") as f:
        json.dump(stats, f, indent=4)
        
    # --- Restauration du contenu écrit à la main (itinéraires, pages sans photos) ---
    _restore_preserved_content(CONTENT_DIR, content_snapshot, generated_folders)

    # Tri par date pour le "Cinematic Journey"
    all_locations.sort(key=lambda x: x['date'])

    # --- 4. EXPORT DES LOCATIONS (MAP) ---
    with open("data/locations.json", "w") as f:
        json.dump(all_locations, f, indent=4)

    # --- 5. EXPORT DES VIDÉOS (page /videos/ + compteur du dashboard) ---
    # Les layouts lisent .Site.Data.videos.{videos,categories} ; sans ce fichier
    # la page /videos/ est vide et le compteur du dashboard affiche 0.
    with open("data/videos.json", "w", encoding="utf-8") as f:
        json.dump({"videos": VIDEOS, "categories": VIDEO_CATEGORIES}, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\n📊 Statistiques générées : {total_images_count} photos au total.")
    print(f"📍 Carte : {len(all_locations)} points générés dynamiquement.")

if __name__ == "__main__":
    sync_portfolio()