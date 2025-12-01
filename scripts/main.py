# scripts/main.py (VERSION CORRIGÉE - SANS THREADING)
import time
import sys
import os
import webbrowser
from pathlib import Path

# Ajouter le dossier scripts au path Python
sys.path.append(os.path.dirname(__file__))

def lancer_dashboard_direct():
    """Lance le dashboard directement (sans threading)"""
    try:
        from dashboard import executer_dashboard
        print("🚀 Lancement du dashboard...")
        executer_dashboard()
    except Exception as e:
        print(f"❌ Erreur lors du lancement du dashboard: {e}")
        input("Appuyez sur Entrée pour continuer...")

def verifier_prerequis():
    """Vérifie que tout est prêt pour le dashboard"""
    print("🔍 VÉRIFICATION DES PRÉREQUIS...")
    
    # Vérifier que l'ETL a été exécuté
    data_file = Path('../data/processed/sales_facts_clean.csv')
    if not data_file.exists():
        print("❌ Les données nettoyées n'existent pas!")
        print("💡 Exécutez d'abord l'ETL (option 1)")
        return False
    
    # Vérifier les dépendances
    try:
        import dash
        import plotly
        import pandas
        print("✅ Toutes les dépendances sont installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("💡 Exécutez: pip install dash plotly pandas")
        return False

def main():
    print("🚀 PROJET NORTHWIND BI - SCRIPT PRINCIPAL")
    print("=" * 50)
    
    while True:
        print("\n📋 MENU PRINCIPAL:")
        print("1. 🔧 Exécuter l'ETL (nettoyage des données)")
        print("2. 📈 Exécuter l'analyse (calcul des KPI)")
        print("3. 📊 Exécuter les visualisations (graphiques)")
        print("4. 🌐 Lancer le dashboard interactif")
        print("5. 🚀 Lancer le dashboard (mode simple)")
        print("6. 🎯 Exécuter tout (ETL + Analyse + Visualisations)")
        print("7. ❌ Quitter")
        
        choix = input("\nChoisissez une option (1-7): ").strip()
        
        if choix == "1":
            executer_etl()
        elif choix == "2":
            executer_analyse()
        elif choix == "3":
            executer_visualisations()
        elif choix == "4":
            print("\n🌐 LANCEMENT DU DASHBOARD INTERACTIF...")
            if verifier_prerequis():
                print("Le dashboard va s'ouvrir dans votre navigateur.")
                print("Si ce n'est pas le cas, allez sur: http://localhost:8050")
                print("💡 Pour arrêter le dashboard, appuyez sur Ctrl+C")
                time.sleep(2)
                webbrowser.open("http://localhost:8050")
                lancer_dashboard_direct()
        elif choix == "5":
            print("\n🚀 LANCEMENT DU DASHBOARD SIMPLE...")
            from dashboard_simple import lancer_dashboard_simple
            lancer_dashboard_simple()
        elif choix == "6":
            print("\n🎯 EXÉCUTION COMPLÈTE ETL + ANALYSE + VISUALISATIONS")
            print("=" * 50)
            if executer_etl():
                time.sleep(1)
                if executer_analyse():
                    time.sleep(1)
                    executer_visualisations()
        elif choix == "7":
            print("👋 Au revoir!")
            break
        else:
            print("❌ Option invalide. Choisissez 1, 2, 3, 4, 5, 6 ou 7.")

# Importer les fonctions
try:
    from etl_main import executer_etl
    from analysis_main import executer_analyse
    from visualizations import executer_visualisations
    print("✅ Modules principaux chargés avec succès!")
except ImportError as e:
    print(f"⚠️ Certains modules ne sont pas chargés: {e}")

if __name__ == "__main__":
    main()