# scripts/debug_simple.py
print("🔧 DIAGNOSTIC DU PROJET")
print("=" * 30)

# Test 1: Python
print("1. Version Python...")
import sys
print(f"   Python {sys.version}")

# Test 2: Bibliothèques
print("2. Bibliothèques...")
try:
    import pandas as pd
    print("   ✅ pandas")
except: print("   ❌ pandas")

try:
    import dash
    print("   ✅ dash") 
except: print("   ❌ dash")

try:
    import plotly
    print("   ✅ plotly")
except: print("   ❌ plotly")

# Test 3: Données
print("3. Données...")
from pathlib import Path
data_file = Path('../data/processed/sales_facts_clean.csv')
if data_file.exists():
    df = pd.read_csv(data_file)
    print(f"   ✅ Données: {len(df)} lignes")
    print(f"   Colonnes: {list(df.columns)}")
else:
    print("   ❌ Fichier données manquant")

print("\n🎯 RECOMMANDATIONS:")
if not data_file.exists():
    print("👉 Exécutez l'ETL: python main.py -> option 1")
else:
    print("👉 Dashboard prêt! Lancez: python test_dashboard_final.py")

input("\nAppuyez sur Entrée pour fermer...")