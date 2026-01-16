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

        with open(os.path.join(hugo_content_path, "index.md"), "w") as f:
            f.write(f'---\ntitle: "{display_title}"\ndescription: "{meta_desc}"\nlayout: "gallery"\n---\n\n')
            f.write(f'{{{{< gallery >}}}}\n{img_list_markdown}{{{{< /gallery >}}}}')
        
        print(f"✅ Dossier traité : {folder} -> {folder_clean}")

if __name__ == "__main__":
    sync_portfolio()