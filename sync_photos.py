import os
import re
import shutil
from PIL import Image, ImageOps

SOURCE_DIR = "/Users/romaincharretteur/pCloud Drive/Portfolio_Images"
CONTENT_DIR = "./content/gallery"
ASSETS_DIR = "./assets/gallery"

def clean_name(name):
    name = name.lower().replace(" ", "_")
    name = re.sub(r'[^a-z0-9_]+', '-', name)
    return name.strip('-')

def sync_portfolio():
    # Nettoyage des dossiers de destination pour éviter les conflits
    for p in [CONTENT_DIR, ASSETS_DIR]:
        if os.path.exists(p): shutil.rmtree(p)
        os.makedirs(p, exist_ok=True)

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
            
            # CRUCIAL : Le chemin pour le shortcode doit être relatif à 'assets/'
            # Ton thème utilise resources.GetMatch, donc 'gallery/dossier/image.webp'
            img_list_markdown += f'  <img src="gallery/{folder_clean}/{img_clean}" />\n'
            
            try:
                img = Image.open(os.path.join(source_folder_path, img_name))
                img = ImageOps.exif_transpose(img)
                img.save(target_path, "WEBP", quality=100)
            except Exception as e:
                print(f"❌ Erreur {img_name}: {e}")

        # Ecriture du fichier index.md avec le format attendu par ton layout
        display_title = folder.replace('_', ' ').title()
        with open(os.path.join(hugo_content_path, "index.md"), "w") as f:
            f.write(f'---\ntitle: "{display_title}"\nlayout: "gallery"\n---\n\n')
            f.write(f'{{{{< gallery >}}}}\n{img_list_markdown}{{{{< /gallery >}}}}')
        print(f"✅ Galerie générée : {folder_clean}")

if __name__ == "__main__":
    sync_portfolio()