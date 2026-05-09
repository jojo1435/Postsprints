from flask import current_app

def inject_asset_version():
    def asset_url(filename):
        asset_map = current_app.config.get("ASSET_MAP", {})
        hashed_name = asset_map.get(filename)
        if not hashed_name:
            return f"/{filename}"
        return f"/hashed/{hashed_name}"

    return dict(asset_url=asset_url)