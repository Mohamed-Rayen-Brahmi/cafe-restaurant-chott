import json

d = json.load(open('object-sculpt-spec.json'))

base = "rgba(183, 188, 192, 1.0)"
bright = "rgba(231, 233, 234, 1.0)"
dark = "rgba(123, 129, 134, 1.0)"

recipes = {
    "body": {
        "dominantAlbedo": base, "secondaryAlbedo": dark,
        "materialClass": "metal", "materialClassConfidence": 0.85,
        "colorGradient": {"type": "linear", "stops": [
            {"position": 0.0, "color": dark}, {"position": 0.5, "color": base}, {"position": 1.0, "color": bright}
        ]},
    },
    "lid": {
        "dominantAlbedo": base, "secondaryAlbedo": bright,
        "materialClass": "metal", "materialClassConfidence": 0.8,
        "colorGradient": {"type": "linear", "stops": [
            {"position": 0.0, "color": dark}, {"position": 1.0, "color": bright}
        ]},
    },
    "finial": {
        "dominantAlbedo": bright, "secondaryAlbedo": base,
        "materialClass": "metal", "materialClassConfidence": 0.6,
    },
    "spout": {
        "dominantAlbedo": base, "secondaryAlbedo": dark,
        "materialClass": "metal", "materialClassConfidence": 0.75,
        "colorGradient": {"type": "linear", "stops": [
            {"position": 0.0, "color": bright}, {"position": 1.0, "color": dark}
        ]},
    },
    "handle": {
        "dominantAlbedo": base, "secondaryAlbedo": dark,
        "materialClass": "metal", "materialClassConfidence": 0.45,
    },
}

for c in d['componentTree']:
    c['colorMaterialRecipe'] = recipes[c['id']]

json.dump(d, open('object-sculpt-spec.json', 'w'), indent=2)
print("fix_color_recipe applied")
