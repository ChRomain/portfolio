import os
import re
import shutil
from PIL import Image, ImageOps

SOURCE_DIR = "/Users/romaincharretteur/pCloud Drive/Portfolio_Images"
CONTENT_DIR = "./content/gallery"
ASSETS_DIR = "./assets/gallery"

# --- PARAMÈTRES D'OPTIMISATION ---
QUALITY = 80          # Qualité WebP
MAX_WIDTH = 2000      # Largeur max

def clean_name(name):
    name = name.lower().replace(" ", "_")
    name = re.sub(r'[^a-z0-9_]+', '-', name)
    return name.strip('-')

def sync_portfolio():
    if os.path.exists(CONTENT_DIR): shutil.rmtree(CONTENT_DIR)
    if os.path.exists(ASSETS_DIR): shutil.rmtree(ASSETS_DIR)
    os.makedirs(CONTENT_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)

    for folder in os.listdir(SOURCE_DIR):
        source_folder_path = os.path.join(SOURCE_DIR, folder)
        if not os.path.isdir(source_folder_path): continue
        
        folder_clean = clean_name(folder)
        hugo_content_path = os.path.join(CONTENT_DIR, folder_clean)
        hugo_assets_path = os.path.join(ASSETS_DIR, folder_clean)
        os.makedirs(hugo_content_path, exist_ok=True)
        os.makedirs(hugo_assets_path, exist_ok=True)

        img_list_markdown = ""
        images = [f for f in os.listdir(source_folder_path) if f.lower().endswith(('jpg', 'jpeg', 'png', 'webp'))]
        
        for i, img_name in enumerate(sorted(images)):
            img_clean = f"{folder_clean}_{i+1:03d}.webp"
            target_path = os.path.join(hugo_assets_path, img_clean)
            
            try:
                img = Image.open(os.path.join(source_folder_path, img_name))
                img = ImageOps.exif_transpose(img)
                
                # Récupération des dimensions d'origine
                width, height = img.size
                
                # --- REDIMENSIONNEMENT ---
                if img.width > MAX_WIDTH:
                    ratio = MAX_WIDTH / float(img.width)
                    new_height = int(float(img.height) * float(ratio))
                    img = img.resize((MAX_WIDTH, new_height), Image.Resampling.LANCZOS)
                    width, height = MAX_WIDTH, new_height 

                # ON ÉCRIT LA BALISE ICI (UNE SEULE FOIS)
                # On ajoute les dimensions pour que le navigateur réserve l'espace
                img_list_markdown += f'  <img src="gallery/{folder_clean}/{img_clean}" width="{width}" height="{height}" />\n'

                img.save(target_path, "WEBP", quality=QUALITY, method=6)
            except Exception as e:
                print(f"❌ Erreur {img_name}: {e}")

        if images:
            first_img = os.path.join(hugo_assets_path, f"{folder_clean}_001.webp")
            shutil.copy(first_img, os.path.join(hugo_content_path, "feature.webp"))

        display_title = folder.replace('_', ' ').title()
        with open(os.path.join(hugo_content_path, "index.md"), "w") as f:
            f.write(f'---\ntitle: "{display_title}"\nlayout: "gallery"\n---\n\n')
            f.write(f'{{{{< gallery >}}}}\n{img_list_markdown}{{{{< /gallery >}}}}')
        print(f"✅ Galerie optimisée : {folder_clean}")

if __name__ == "__main__":
    sync_portfolio()