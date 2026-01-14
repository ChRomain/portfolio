import os
from PIL import Image

# Config des chemins
SOURCE_DIR = "/Users/romaincharretteur/pCloud Drive/Portfolio_Images"
DEST_DIR = "./static/gallery" # Hugo cherchera ici

def sync_and_resize():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    for root, dirs, files in os.walk(SOURCE_DIR):
        for file in files:
            if file.lower().endswith(('jpg', 'jpeg', 'png')):
                # Garder la structure des dossiers (Sport, Street...)
                rel_path = os.path.relpath(root, SOURCE_DIR)
                target_folder = os.path.join(DEST_DIR, rel_path)
                os.makedirs(target_folder, exist_ok=True)

                # Chemin final
                filename_webp = os.path.splitext(file)[0] + ".webp"
                target_path = os.path.join(target_folder, filename_webp)

                # N'optimiser que si le fichier n'existe pas déjà
                if not os.path.exists(target_path):
                    img = Image.open(os.path.join(root, file))
                    img.thumbnail((1920, 1920)) # Redimensionne pour le web
                    img.save(target_path, "WEBP", quality=82)
                    print(f"✅ Ajouté : {filename_webp}")

if __name__ == "__main__":
    sync_and_resize()