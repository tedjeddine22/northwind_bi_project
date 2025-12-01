# scripts/final_check.py
from pathlib import Path
import pandas as pd
import sys
import os

class ValidationFinale:
    def __init__(self):
        self.project_path = Path('..')
        self.erreurs = []
        self.avertissements = []
        
    def verifier_structure(self):
        """Vérifie la structure complète du projet"""
        print("🔍 VÉRIFICATION DE LA STRUCTURE...")
        
        dossiers_requis = [
            'data/raw',
            'data/processed', 
            'scripts',
            'figures/ventes',
            'figures/produits',
            'figures/clients',
            'figures/interactifs',
            'reports',
            'video'
        ]
        
        fichiers_requis = {
            'scripts': [
                'main.py',
                'etl_main.py', 
                'analysis_main.py',
                'visualizations.py',
                'dashboard.py',
                'generate_reports.py',
                'final_check.py'
            ],
            'data/raw': [
                'Orders.xlsx',
                'Order Details.xlsx',
                'Products.xlsx',
                'Customers.xlsx',
                'Employees.xlsx'
            ],
            'data/processed': [
                'sales_facts_clean.csv',
                'orders_clean.csv',
                'products_clean.csv'
            ],
            'reports': [
                'rapport_technique.md',
                'rapport_business.md',
                'arborescence_projet.txt'
            ],
            '.': [
                'README.md',
                'requirements.txt'
            ]
        }
        
        # Vérification des dossiers
        for dossier in dossiers_requis:
            chemin = self.project_path / dossier
            if not chemin.exists():
                self.erreurs.append(f"❌ Dossier manquant: {dossier}")
            else:
                print(f"✅ Dossier: {dossier}")
        
        # Vérification des fichiers
        for dossier, fichiers in fichiers_requis.items():
            for fichier in fichiers:
                chemin = self.project_path / dossier / fichier
                if not chemin.exists():
                    self.avertissements.append(f"⚠️ Fichier manquant: {dossier}/{fichier}")
                else:
                    # Vérifier que le fichier n'est pas vide
                    if chemin.stat().st_size == 0:
                        self.erreurs.append(f"❌ Fichier vide: {dossier}/{fichier}")
                    else:
                        print(f"✅ Fichier: {dossier}/{fichier}")
        
        return len(self.erreurs) == 0
    
    def verifier_fonctionnement(self):
        """Teste le fonctionnement des scripts principaux"""
        print("\n🔧 VÉRIFICATION DU FONCTIONNEMENT...")
        
        tests = [
            {
                'nom': 'Import des bibliothèques',
                'code': "import pandas, dash, plotly, matplotlib, seaborn",
                'critique': True
            },
            {
                'nom': 'Chargement des données',
                'code': "pd.read_csv('../data/processed/sales_facts_clean.csv')",
                'critique': True
            },
            {
                'nom': 'Création dashboard',
                'code': "dash.Dash('test')",
                'critique': False
            }
        ]
        
        for test in tests:
            try:
                exec(test['code'])
                print(f"✅ {test['nom']}")
            except Exception as e:
                message = f"❌ {test['nom']}: {e}"
                if test['critique']:
                    self.erreurs.append(message)
                else:
                    self.avertissements.append(message)
        
        return len([e for e in self.erreurs if 'critique' in e]) == 0
    
    def verifier_donnees(self):
        """Vérifie la qualité des données"""
        print("\n📊 VÉRIFICATION DES DONNÉES...")
        
        try:
            df = pd.read_csv(self.project_path / 'data/processed/sales_facts_clean.csv')
            
            # Vérifications de base
            if len(df) == 0:
                self.erreurs.append("❌ Aucune donnée dans sales_facts_clean.csv")
                return False
            
            # Colonnes requises
            colonnes_requises = ['order_id', 'order_date', 'customer_company', 'product_name', 'Line Total']
            for col in colonnes_requises:
                if col not in df.columns:
                    self.erreurs.append(f"❌ Colonne manquante: {col}")
            
            # Vérifier valeurs manquantes
            valeurs_manquantes = df[colonnes_requises].isnull().sum().sum()
            if valeurs_manquantes > 0:
                self.avertissements.append(f"⚠️ {valeurs_manquantes} valeurs manquantes dans les colonnes critiques")
            
            # Vérifier cohérence des données
            ca_total = df['Line Total'].sum()
            if ca_total <= 0:
                self.erreurs.append("❌ Chiffre d'affaires total invalide")
            
            nb_commandes = df['order_id'].nunique()
            if nb_commandes <= 0:
                self.erreurs.append("❌ Aucune commande trouvée")
            
            print(f"✅ Données: {len(df)} lignes, {nb_commandes} commandes, CA: {ca_total:,.0f} $")
            
            return True
            
        except Exception as e:
            self.erreurs.append(f"❌ Erreur vérification données: {e}")
            return False
    
    def generer_rapport_validation(self):
        """Génère un rapport de validation complet"""
        print("\n📄 GÉNÉRATION RAPPORT DE VALIDATION...")
        
        # Exécuter toutes les vérifications
        structure_ok = self.verifier_structure()
        fonctionnement_ok = self.verifier_fonctionnement()
        donnees_ok = self.verifier_donnees()
        
        # Créer le rapport
        rapport = [
            "RAPPORT DE VALIDATION - PROJET NORTHWIND BI",
            "=" * 50,
            f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## 📋 RÉSULTATS DE VALIDATION",
            f"Structure: {'✅ VALIDÉ' if structure_ok else '❌ ÉCHEC'}",
            f"Fonctionnement: {'✅ VALIDÉ' if fonctionnement_ok else '❌ ÉCHEC'}",
            f"Données: {'✅ VALIDÉ' if donnees_ok else '❌ ÉCHEC'}",
            "",
            "## ❌ ERREURS CRITIQUES" if self.erreurs else "## ✅ AUCUNE ERREUR CRITIQUE",
        ]
        
        for erreur in self.erreurs:
            rapport.append(f"- {erreur}")
        
        rapport.extend([
            "",
            "## ⚠️ AVERTISSEMENTS" if self.avertissements else "## ✅ AUCUN AVERTISSEMENT",
        ])
        
        for avertissement in self.avertissements:
            rapport.append(f"- {avertissement}")
        
        # Recommandations
        if not self.erreurs:
            rapport.extend([
                "",
                "## 🎉 PROJET PRÊT POUR LA SOUMISSION!",
                "### Prochaines étapes:",
                "1. ✅ Créer un repository Git",
                "2. ✅ Ajouter tous les fichiers au repository",
                "3. ✅ Préparer la vidéo de présentation",
                "4. ✅ Soumettre le projet",
                "",
                "### Félicitations! 🏆"
            ])
        else:
            rapport.extend([
                "",
                "## 🔧 CORRECTIONS NÉCESSAIRES",
                "### Actions recommandées:"
            ])
            for erreur in self.erreurs:
                if "Dossier manquant" in erreur:
                    rapport.append(f"- Créer le dossier manquant")
                elif "Fichier manquant" in erreur:
                    rapport.append(f"- Régénérer le fichier manquant")
                elif "Import" in erreur:
                    rapport.append(f"- Installer les dépendances manquantes: pip install [bibliothèque]")
        
        # Sauvegarder le rapport
        rapport_path = self.project_path / 'reports' / 'rapport_validation.md'
        with open(rapport_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(rapport))
        
        # Affichage console
        print("\n" + "=" * 60)
        if not self.erreurs:
            print("🎉 PROJET VALIDÉ AVEC SUCCÈS!")
            print("📁 Tous les livrables sont présents et fonctionnels")
            print("🚀 Prêt pour la soumission!")
        else:
            print("❌ PROJET INCOMPLET")
            print(f"Erreurs critiques: {len(self.erreurs)}")
            print(f"Avertissements: {len(self.avertissements)}")
        
        return len(self.erreurs) == 0

def valider_projet_complet():
    """Fonction principale de validation"""
    validateur = ValidationFinale()
    return validateur.generer_rapport_validation()

if __name__ == "__main__":
    valider_projet_complet()