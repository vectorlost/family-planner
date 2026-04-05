#!/usr/bin/env python3
"""
FamilyMeal → Google Sheets writer
────────────────────────────────────────────────────────────────
Lit  : familymeal_data.json  (généré par le scheduled task Claude)
Écrit: Google Sheets FamilyPlan-DATABASE (4 onglets)

Onglets cibles :
  Menus       → Semaine, Jour, Titre recette, URL, Site source,
                Protéine, Temps (min), Portions, Statut
  Circulaires → Date, Épicerie, Produit, Catégorie,
                Prix promo, Prix régulier, Économie %
  Épicerie    → Produit, Quantité, Unité, Prix, Catégorie,
                Épicerie recommandée, Imbattable Maxi
  Statut      → Valeur (A2) = "READY - AAAA-MM-JJ"
────────────────────────────────────────────────────────────────
"""

import subprocess, sys, json, os
from datetime import datetime

# ── Auto-install des dépendances si absentes ───────────────────
def install(pkg):
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", pkg,
         "--break-system-packages", "-q"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    print("   Installation de gspread...")
    install("gspread")
    install("google-auth")
    import gspread
    from google.oauth2.service_account import Credentials

# ── Configuration ──────────────────────────────────────────────
SHEET_ID   = "1HOpW3Fj0MzQ4yNF5OohFHxJjjFVOrnwsJnSn7fTt-38"
SCOPES     = ["https://www.googleapis.com/auth/spreadsheets"]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDS_FILE = os.path.join(SCRIPT_DIR, "credentials.json")
DATA_FILE  = os.path.join(SCRIPT_DIR, "familymeal_data.json")


# ── Connexion ──────────────────────────────────────────────────
def get_client():
    if not os.path.exists(CREDS_FILE):
        raise FileNotFoundError(
            f"credentials.json introuvable dans : {SCRIPT_DIR}\n"
            "Télécharge-le depuis Google Cloud Console et place-le ici."
        )
    creds  = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    return gspread.authorize(creds)


# ── Onglet Menus ───────────────────────────────────────────────
def write_menus(sheet, menus, semaine):
    ws = sheet.worksheet("Menus")
    ws.batch_clear(["A2:Z1000"])
    rows = []
    for m in menus:
        rows.append([
            semaine,
            m.get("jour", ""),
            m.get("titre", ""),
            m.get("url", ""),
            m.get("site", ""),
            m.get("proteine", ""),
            m.get("temps", ""),
            m.get("portions", ""),
            m.get("statut", "Suggéré"),
        ])
    if rows:
        ws.update(f"A2:I{1 + len(rows)}", rows)
    print(f"   ✓ Menus : {len(rows)} ligne(s)")


# ── Onglet Circulaires ─────────────────────────────────────────
def write_circulaires(sheet, circulaires, semaine):
    ws = sheet.worksheet("Circulaires")
    ws.batch_clear(["A2:Z1000"])
    rows = []
    for c in circulaires:
        rows.append([
            semaine,
            c.get("epicerie", ""),
            c.get("produit", ""),
            c.get("categorie", ""),
            c.get("prix_promo", ""),
            c.get("prix_regulier", ""),
            c.get("economie_pct", ""),
        ])
    if rows:
        ws.update(f"A2:G{1 + len(rows)}", rows)
    print(f"   ✓ Circulaires : {len(rows)} ligne(s)")


# ── Onglet Épicerie ────────────────────────────────────────────
# Ordre des colonnes :
#   A=Produit  B=Quantité  C=Unité  D=Prix  E=Catégorie
#   F=Épicerie recommandée  G=Imbattable Maxi
def write_epicerie(sheet, epicerie):
    ws = sheet.worksheet("Épicerie")
    ws.batch_clear(["A2:Z1000"])
    rows = []
    for item in epicerie:
        imbattable = item.get("imbattable_maxi", "")
        # Normalise boolean → texte lisible
        if isinstance(imbattable, bool):
            imbattable = "OUI" if imbattable else ""
        rows.append([
            item.get("produit", ""),
            item.get("quantite", ""),
            item.get("unite", ""),
            item.get("prix", ""),
            item.get("categorie", ""),
            item.get("epicerie", ""),
            imbattable,
        ])
    if rows:
        ws.update(f"A2:G{1 + len(rows)}", rows)
    print(f"   ✓ Épicerie : {len(rows)} ligne(s)")


# ── Onglet Statut ──────────────────────────────────────────────
def write_statut(sheet, semaine):
    ws = sheet.worksheet("Statut")
    ws.update("A2", [[f"READY - {semaine}"]])
    print(f"   ✓ Statut : READY - {semaine}")


# ── Main ───────────────────────────────────────────────────────
def main():
    print("\n📊 FamilyMeal → Google Sheets")
    print("─" * 40)

    # 1. Lire le JSON généré par Claude
    if not os.path.exists(DATA_FILE):
        print(f"❌ Fichier introuvable : {DATA_FILE}")
        print("   Assure-toi que le scheduled task a bien généré familymeal_data.json")
        sys.exit(1)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    semaine = data.get("semaine", datetime.today().strftime("%Y-%m-%d"))
    print(f"   Semaine    : {semaine}")
    print(f"   Menus      : {len(data.get('menus', []))}")
    print(f"   Circulaires: {len(data.get('circulaires', []))}")
    print(f"   Épicerie   : {len(data.get('epicerie', []))}")
    print()

    # 2. Connexion Google Sheets
    print("   Connexion à Google Sheets...")
    try:
        client = get_client()
        sheet  = client.open_by_key(SHEET_ID)
    except Exception as e:
        print(f"❌ Connexion échouée : {e}")
        sys.exit(1)

    # 3. Écriture des 4 onglets
    write_menus(sheet, data.get("menus", []), semaine)
    write_circulaires(sheet, data.get("circulaires", []), semaine)
    write_epicerie(sheet, data.get("epicerie", []))
    write_statut(sheet, semaine)

    print()
    print(f"✅ Google Sheets mis à jour avec succès !")
    print(f"   https://docs.google.com/spreadsheets/d/{SHEET_ID}")


if __name__ == "__main__":
    main()
