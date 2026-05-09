import os
import hashlib
import shutil

ASSET_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico", ".js", ".css"}

def hash_static_assets(app):
    static_folder = app.static_folder
    hashed_folder = os.path.join(static_folder, "hashed")
    os.makedirs(hashed_folder, exist_ok=True)

    if os.path.exists(hashed_folder):
        shutil.rmtree(hashed_folder)
    os.makedirs(hashed_folder)

    asset_map = {}

    for root, dirs, files in os.walk(static_folder):
        dirs[:] = [d for d in dirs if d != "hashed"]

        for filename in files:
            filepath = os.path.join(root, filename)
            ext = os.path.splitext(filename)[1].lower()

            if ext not in ASSET_EXTENSIONS:
                continue

            relative = os.path.relpath(filepath, static_folder).replace("\\", "/")

            with open(filepath, "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()[:8]

            hashed_name = f"{file_hash}{ext}"
            hashed_path = os.path.join(hashed_folder, hashed_name)

            if not os.path.exists(hashed_path):
                shutil.copy2(filepath, hashed_path)

            asset_map[relative] = hashed_name

    app.config["ASSET_MAP"] = asset_map
    print(app.config["ASSET_MAP"])