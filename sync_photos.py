import os
import re
import shutil
from PIL import Image, ImageOps
import piexif

SOURCE_DIR = "/Users/romaincharretteur/pCloud Drive/Portfolio_Images"
CONTENT_DIR = "./content/gallery"
ASSETS_DIR = "./static/gallery" 

# --- PARAMÈTRES D'OPTIMISATION ---
QUALITY = 80          # Qualité WebP
MAX_WIDTH = 2000      # Largeur max

DESCRIPTIONS = {
    "indonesie": "&nbsp;&nbsp;&nbsp;&nbsp;Between ancestral temples, secret Balinese beaches, volcanic mists, and lush jungles, dive into a visual exploration of Indonesian contrasts—where wild nature meets sacred serenity.",
    "guatemala": "&nbsp;&nbsp;&nbsp;&nbsp;From the cobblestone streets of Antigua and ancient Mayan pyramids to the fiery peaks of Fuego and Acatenango, embark on a visual journey through Guatemala's timeless soul—where colonial history meets the raw power of the earth.",
    "cape_cod": "&nbsp;&nbsp;&nbsp;&nbsp;From iconic lighthouses guarding the vast Atlantic to the serene dance of whales on the horizon, discover the soulful charm of Cape Cod. A captivating journey through New England's coastal landscapes, where peaceful shores meet maritime history.",
    "vermont": "&nbsp;&nbsp;&nbsp;&nbsp;Immerse yourself in the tranquil beauty of the Green Mountain State. From the serene shores of Lake Willoughby to the lush, rolling hills that define the landscape, witness a peaceful harmony where nature takes center stage.",
    "new_hampshire": "&nbsp;&nbsp;&nbsp;&nbsp;Experience the fleeting magic of the Indian Summer. From the fiery foliage of the White Mountains to the golden-hued winding roads of the Kancamagus Highway, lose yourself in a landscape painted in nature’s most vibrant autumn tones.",
    "washington": "&nbsp;&nbsp;&nbsp;&nbsp;Walk through the heart of American history. From the neoclassical grandeur of the White House and the Capitol at night to the red towers of the Smithsonian, witness a city where every corner tells a story of power and heritage.",
    "suede": "&nbsp;&nbsp;&nbsp;&nbsp;Step into a Nordic winter wonderland. From the glowing reindeer displays and festive city lights to the serene, frozen harbors, experience the enchanting magic of a Swedish winter where the darkness of the season is met with a warm, golden glow.",
    "toronto": "&nbsp;&nbsp;&nbsp;&nbsp;Rising above the shores of Lake Ontario, experience the vibrant pulse of Canada's largest metropolis. From the dizzying heights of the CN Tower to the bustling streets of downtown, witness a city where soaring glass towers meet a rich, multicultural heart.",
    "rome": "&nbsp;&nbsp;&nbsp;&nbsp;Step back through two thousand years of history. From the colossal heights of the Colosseum to the moonlit elegance of the Trevi Fountain and the Pantheon, witness a city where the ancient world and modern life breathe as one.",
    "naples": "&nbsp;&nbsp;&nbsp;&nbsp;In the shadow of Mount Vesuvius, experience the raw and captivating soul of Southern Italy. Journey through a city where ancient history and vibrant street life collide under a Mediterranean sun that turns every crumbling facade into a golden masterpiece.",
    "paris": "&nbsp;&nbsp;&nbsp;&nbsp;Experience the timeless allure of the City of Light. From the sparkling iron lattice of the Eiffel Tower at night to the bohemian glow of Montmartre and the red velvet charm of the Moulin Rouge, witness a city that never loses its romantic spark.",
    "lyon": "&nbsp;&nbsp;&nbsp;&nbsp;Traverse the layers of time in France’s gastronomic capital. From the shimmering mosaics of the Fourvière Basilica to the secret Renaissance courtyards of the Old Town, uncover a city where architectural grandeur and hidden history gracefully intertwine.",
    "bordeaux": "&nbsp;&nbsp;&nbsp;&nbsp;Contemplate a city where history and modernity find a perfect balance. From the golden stone of the Grosse Cloche to the futuristic curves of the Cité du Vin, embark on an odyssey through Bordeaux’s grand boulevards and its hidden, vibrant street-art sanctuaries.",
    "finistere": "&nbsp;&nbsp;&nbsp;&nbsp;Contemplate the raw majesty of the 'Land's End'. From the legendary lighthouses of Saint-Mathieu guarding the rugged cliffs to the turquoise waters of hidden coves, embark on a visual journey through Brittany’s untamed coastline where the Atlantic meets the soul of the earth.",
    "boston": "&nbsp;&nbsp;&nbsp;&nbsp;Trace the footsteps of history along the cobblestone paths of Beacon Hill. From the grandeur of Quincy Market to the historic docks of the harbor, encounter a city where the spirit of American independence lives on through every brick and monument.",
    "new_york": "&nbsp;&nbsp;&nbsp;&nbsp;Experience the restless pulse of the world’s most iconic metropolis. From the shimmering neon of Times Square and the industrial majesty of the Brooklyn Bridge to the quiet, sun-drenched paths of Central Park, witness a city of infinite scales and electric ambitions.",
    "montreal": "&nbsp;&nbsp;&nbsp;&nbsp;Feel the dual soul of North America’s most eclectic island. From the adrenaline of the Formula 1 tracks and towering street murals to the glowing neon of the Quartier des Spectacles, capture the vibrant pulse of a city that lives for the moment.",
    "montenegro": "&nbsp;&nbsp;&nbsp;&nbsp;Behold the dramatic meeting of jagged limestone peaks and crystalline waters. Navigate through the winding Bay of Kotor, where ancient stone villages cling to the shoreline beneath the watchful gaze of mountain fortresses—a true hidden gem of the Adriatic.",
    "maine": "&nbsp;&nbsp;&nbsp;&nbsp;Surrender to the rugged charm of the Pine Tree State. From the historic beacons of Portland Head Light to the bustling docks of fishing harbors, discover a coastline where the deep blue Atlantic carves its story into granite shores and salty traditions.",
    "canada": "&nbsp;&nbsp;&nbsp;&nbsp;Venture into the raw, untamed heart of the Great White North. From close encounters with majestic wildlife in the frozen wilderness to emerald-green shorelines hidden deep within the forest, discover the spontaneous beauty of a land that knows no bounds.",
    "corse": "&nbsp;&nbsp;&nbsp;&nbsp;Behold the breathtaking cliffs of the 'Isle of Beauty.' From the dizzying heights of Bonifacio perched above the turquoise Mediterranean to the secret emerald pools of inland rivers, discover a land of granite and grit that remains wonderfully untamed.",
    "niagara_falls": "&nbsp;&nbsp;&nbsp;&nbsp;Stand at the edge of the world where thunderous waters meet a neon-lit skyline. Witness the overwhelming force of the falls in all their misty glory, before wandering into the vibrant, cinematic energy of Niagara City’s bustling streets and retro motels.",
    "ottawa": "&nbsp;&nbsp;&nbsp;&nbsp;Witness a capital in full bloom. From the vibrant endless fields of the Canadian Tulip Festival to the scenic pathways along the Rideau Canal, explore a city where nature's bright palette perfectly complements the historic stone of Parliament Hill.",
    "quebec": "&nbsp;&nbsp;&nbsp;&nbsp;Step into a living fairy tale where cobblestone streets meet the majestic silhouette of the Château Frontenac. From the frost-covered ramparts to the warm glow of Petit Champlain at night, witness the romantic soul of North America’s oldest fortified city.",
    "philadelphie": "&nbsp;&nbsp;&nbsp;&nbsp;Immerse yourself in a vibrant urban mosaic where history meets bold creativity. From the intricate glass masterpieces of the Magic Gardens to the towering blue spans of the Ben Franklin Bridge, discover the colorful soul and resilient spirit of the City of Brotherly Love."
}

def clean_name(name):
    name = name.lower().replace(" ", "_")
    name = re.sub(r'[^a-z0-9_]+', '', name)
    return name.strip('_')

def get_exif_data(img_path):
    """Extrait les réglages techniques de l'image"""
    try:
        img = Image.open(img_path)
        exif_dict = piexif.load(img.info['exif'])
        
        # Boîtier (Model)
        model = exif_dict['0th'].get(piexif.ImageIFD.Model, b"").decode().strip()
        # Ouverture (F-Stop)
        f_stop = exif_dict['Exif'].get(piexif.ExifIFD.FNumber)
        # ISO
        iso = exif_dict['Exif'].get(piexif.ExifIFD.ISOSpeedRatings)
        # Vitesse d'obturation (Exposure Time)
        shutter = exif_dict['Exif'].get(piexif.ExifIFD.ExposureTime)

        parts = []
        if model: parts.append(model)
        if f_stop:
            parts.append(f"f/{f_stop[0]/f_stop[1]}")
        if shutter:
            val = f"{shutter[0]}/{shutter[1]}s" if shutter[1] > 1 else f"{shutter[0]}s"
            parts.append(val)
        if iso:
            parts.append(f"ISO {iso}")
        
        return " | ".join(parts)
    except Exception:
        return ""

def sync_portfolio():
    if os.path.exists(CONTENT_DIR): shutil.rmtree(CONTENT_DIR)
    if os.path.exists(ASSETS_DIR): shutil.rmtree(ASSETS_DIR)
    
    os.makedirs(CONTENT_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    for folder in os.listdir(SOURCE_DIR):
        source_folder_path = os.path.join(SOURCE_DIR, folder)
        if not os.path.isdir(source_folder_path): continue
        
        folder_clean = clean_name(folder)
        display_title = folder.replace('_', ' ').title()
        
        hugo_content_path = os.path.join(CONTENT_DIR, folder_clean)
        hugo_assets_path = os.path.join(ASSETS_DIR, folder_clean)
        os.makedirs(hugo_content_path, exist_ok=True)
        os.makedirs(hugo_assets_path, exist_ok=True)

        img_list_markdown = ""
        images = [f for f in os.listdir(source_folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png', 'webp'))]
        
        for i, img_name in enumerate(sorted(images)):
            img_num = i + 1
            img_clean = f"{folder_clean}_{img_num:03d}.webp"
            full_source_path = os.path.join(source_folder_path, img_name)
            target_path = os.path.join(hugo_assets_path, img_clean)
            
            exif_info = get_exif_data(full_source_path)
            alt_text = f"Photographie de {display_title} - {img_num}"
            
            try:
                img = Image.open(full_source_path)
                img = ImageOps.exif_transpose(img)
                width, height = img.size
                
                if img.width > MAX_WIDTH:
                    ratio = MAX_WIDTH / float(img.width)
                    new_height = int(float(img.height) * float(ratio))
                    img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                    width, height = MAX_WIDTH, new_height 

                # Version standard sans lazy loading
                img_list_markdown += f'  <img src="/gallery/{folder_clean}/{img_clean}" alt="{alt_text}" title="{exif_info}" width="{width}" height="{height}" />\n'

                img.save(target_path, "WEBP", quality=QUALITY, method=6)
                
            except Exception as e:
                print(f"❌ Erreur sur {img_name}: {e}")

        if images:
            first_img_renamed = f"{folder_clean}_001.webp"
            shutil.copy(os.path.join(hugo_assets_path, first_img_renamed), 
                        os.path.join(hugo_content_path, "feature.webp"))

        meta_desc = f"Découvrez ma galerie photo de {display_title}. Une collection de clichés capturant l'architecture et l'ambiance de {display_title}."
        gallery_desc = DESCRIPTIONS.get(folder_clean, "")

        with open(os.path.join(hugo_content_path, "index.md"), "w") as f:
            f.write(f'---\ntitle: "{display_title}"\ndescription: "{meta_desc}"\nlayout: "gallery"\n---\n\n')
            if gallery_desc:
                f.write(f'<div class="gallery-description max-w-2xl mx-auto mb-8 text-neutral-600 dark:text-neutral-400 tracking-wide">\n{gallery_desc}\n</div>\n\n')
            f.write(f'{{{{< gallery >}}}}\n{img_list_markdown}{{{{< /gallery >}}}}')
        
        print(f"✅ Dossier traité : {folder} -> {folder_clean}")

if __name__ == "__main__":
    sync_portfolio()