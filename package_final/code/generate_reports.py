# scripts/generate_reports.py
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import json
import shutil

class RapportFinal:
    def __init__(self):
        self.project_path = Path('..')
        self.reports_path = self.project_path / 'reports'
        self.data_path = self.project_path / 'data'
        self.scripts_path = self.project_path / 'scripts'
        
    def generer_rapport_technique(self):
        """Génère le rapport technique détaillé"""
        print("📄 CRÉATION DU RAPPORT TECHNIQUE")
        
        rapport = [
            "RAPPORT TECHNIQUE - PROJET NORTHWIND BI",
            "=" * 60,
            f"Date de génération: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "Auteur: [Votre Nom]",
            "Projet: Business Intelligence - Northwind Traders",
            "",
            "## 📋 TABLE DES MATIÈRES",
            "1. Introduction",
            "2. Architecture du Projet", 
            "3. Processus ETL",
            "4. Analyse des Données",
            "5. Visualisations",
            "6. Dashboard Interactif",
            "7. Choix Techniques",
            "8. Résultats et Insights",
            "9. Conclusion",
            "",
            "## 1. INTRODUCTION",
            "### Objectif du Projet",
            "Concevoir une solution BI complète basée sur la base de données Northwind pour analyser les performances commerciales.",
            "",
            "### Périmètre",
            "- ETL (Extract, Transform, Load) en Python",
            "- Analyse des KPI business",
            "- Création de visualisations",
            "- Dashboard interactif",
            "- Rapport détaillé",
            "",
            "## 2. ARCHITECTURE DU PROJET",
            "### Structure des Dossiers",
            "```",
            "northwind_bi_project/",
            "├── data/                   # Données",
            "│   ├── raw/               # Sources originales",
            "│   └── processed/         # Données nettoyées",
            "├── scripts/               # Code source",
            "├── figures/               # Graphiques",
            "├── reports/               # Rapports",
            "├── video/                 # Matériel vidéo",
            "└── README.md              # Documentation",
            "```",
            "",
            "### Flux de Données",
            "1. **Chargement** → Fichiers Excel bruts",
            "2. **Nettoyage** → Script ETL Python", 
            "3. **Analyse** → Calcul des KPI",
            "4. **Visualisation** → Graphiques et dashboard",
            "5. **Rapport** → Documentation et insights",
            "",
            "## 3. PROCESSUS ETL",
            "### Extraction",
            "- Format: Fichiers Excel (.xlsx)",
            "- Outil: pandas.read_excel()",
            "- Tables: Orders, Order Details, Products, Customers, Employees",
            "",
            "### Transformation",
            "- Nettoyage des valeurs manquantes",
            "- Conversion des types de données",
            "- Standardisation des formats",
            "- Calcul de colonnes dérivées",
            "",
            "### Chargement",
            "- Format: CSV standardisé",
            "- Encodage: UTF-8",
            "- Structure: Tables normalisées",
            "",
            "## 4. ANALYSE DES DONNÉES",
            "### KPI Calculés",
            "- 📊 Chiffre d'affaires total",
            "- 💰 Profit et marges", 
            "- 📦 Volumes de vente",
            "- 👥 Performance clients",
            "- 👨‍💼 Performance employés",
            "- ⚙️ Efficacité opérationnelle",
            "",
            "### Méthodologie d'Analyse",
            "- Agrégation par périodes",
            "- Segmentation clients/produits",
            "- Analyse temporelle",
            "- Comparaisons relatives",
            "",
            "## 5. VISUALISATIONS",
            "### Graphiques Statiques (Matplotlib/Seaborn)",
            "- Évolution temporelle",
            "- Répartition par catégorie",
            "- Top N analyses", 
            "- Heatmaps et corrélations",
            "",
            "### Graphiques Interactifs (Plotly)",
            "- Dashboard temps réel",
            "- Filtres dynamiques",
            "- Tooltips informatifs",
            "- Responsive design",
            "",
            "## 6. DASHBOARD INTERACTIF",
            "### Technologies",
            "- Framework: Dash (Plotly)",
            "- Backend: Flask",
            "- Frontend: HTML/CSS/JavaScript",
            "- Port: 8050/8060",
            "",
            "### Fonctionnalités",
            "- Filtres multi-critères",
            "- KPI en temps réel",
            "- Graphiques interactifs",
            "- Design responsive",
            "",
            "## 7. CHOIX TECHNIQUES",
            "### Bibliothèques Python",
            "```python",
            "# Data Manipulation",
            "pandas >= 1.5.0    # Manipulation données tabulaires",
            "numpy >= 1.21.0    # Calculs numériques",
            "openpyxl >= 3.0.0  # Lecture fichiers Excel",
            "",
            "# Visualisation",
            "matplotlib >= 3.5.0 # Graphiques statiques",
            "seaborn >= 0.11.0   # Visualisation statistique", 
            "plotly >= 5.10.0    # Graphiques interactifs",
            "",
            "# Dashboard",
            "dash >= 2.7.0       # Framework web interactif",
            "```",
            "",
            "### Justification des Choix",
            "- **pandas**: Standard pour la manipulation de données en Python",
            "- **plotly/dash**: Meilleure solution pour dashboards interactifs",
            "- **matplotlib**: Bibliothèque de référence pour visualisation",
            "- **openpyxl**: Support natif des fichiers Excel",
            "",
            "## 8. RÉSULTATS ET INSIGHTS",
            "### Insights Business",
            "1. **Produits Performants**: Identification des top produits par CA",
            "2. **Clients Stratégiques**: Segmentation par valeur client", 
            "3. **Performance Commerciale**: Analyse par employé",
            "4. **Tendances Temporelles**: Évolution des ventes",
            "5. **Efficacité Opérationnelle**: Délais et processus",
            "",
            "### Recommandations Stratégiques",
            "- Focus sur les produits à haute marge",
            "- Fidélisation des clients VIP",
            "- Optimisation des stocks critiques",
            "- Formation ciblée des commerciaux",
            "",
            "## 9. CONCLUSION",
            "### Bilan du Projet",
            "Le projet a permis de créer une solution BI complète permettant de:",
            "- Automatiser le traitement des données Northwind",
            "- Calculer des indicateurs business pertinents", 
            "- Visualiser les données de manière interactive",
            "- Fournir des insights actionnables",
            "",
            "### Perspectives d'Évolution",
            "- Connexion base de données temps réel",
            "- Alertes automatiques sur KPI",
            "- Intégration machine learning",
            "- Reporting automatisé par email",
            "",
            "---",
            "FIN DU RAPPORT TECHNIQUE",
            "Northwind BI Project - © 2024"
        ]
        
        # Sauvegarde du rapport
        rapport_path = self.reports_path / 'rapport_technique.md'
        with open(rapport_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(rapport))
        
        print(f"✅ Rapport technique généré: {rapport_path}")
        return rapport_path
    
    def generer_rapport_business(self):
        """Génère le rapport business avec les insights"""
        print("📊 CRÉATION DU RAPPORT BUSINESS")
        
        try:
            # Charger les données pour les stats
            df = pd.read_csv(self.data_path / 'processed/sales_facts_clean.csv')
            
            # Calculer les métriques business
            ca_total = df['Line Total'].sum()
            nb_commandes = df['order_id'].nunique()
            nb_clients = df['customer_company'].nunique()
            nb_produits = df['product_name'].nunique()
            
            # Top produits
            top_produits = df.groupby('product_name')['Line Total'].sum().sort_values(ascending=False).head(5)
            
            # Top clients
            top_clients = df.groupby('customer_company')['Line Total'].sum().sort_values(ascending=False).head(5)
            
            rapport = [
                "RAPPORT BUSINESS - NORTHWIND TRADERS",
                "=" * 50,
                f"Période d'analyse: Données complètes",
                f"Date de génération: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                "",
                "## 📈 SYNTHÈSE EXÉCUTIVE",
                f"**Chiffre d'Affaires Total**: {ca_total:,.0f} $",
                f"**Nombre de Commandes**: {nb_commandes}",
                f"**Clients Actifs**: {nb_clients}",
                f"**Produits Vendus**: {nb_produits}",
                "",
                "## 🎯 PERFORMANCE COMMERCIALE",
                "### Top 5 Produits par CA",
            ]
            
            # Ajouter top produits
            for i, (produit, ca) in enumerate(top_produits.items(), 1):
                rapport.append(f"{i}. **{produit}**: {ca:,.0f} $")
            
            rapport.extend([
                "",
                "### Top 5 Clients par CA",
            ])
            
            # Ajouter top clients
            for i, (client, ca) in enumerate(top_clients.items(), 1):
                rapport.append(f"{i}. **{client}**: {ca:,.0f} $")
            
            rapport.extend([
                "",
                "## 💡 INSIGHTS CLÉS",
                "### Forces",
                "- Large base de clients diversifiée",
                "- Gamme de produits étendue",
                "- Performance commerciale stable",
                "",
                "### Opportunités d'Amélioration", 
                "- Optimisation des produits à faible marge",
                "- Développement de la fidélisation client",
                "- Amélioration de l'efficacité opérationnelle",
                "",
                "## 🎯 RECOMMANDATIONS STRATÉGIQUES",
                "1. **Focus Produits**: Concentrer les efforts sur les top 5 produits",
                "2. **Relation Client**: Programme de fidélisation pour les top clients",
                "3. **Optimisation Stocks**: Révision des niveaux de réapprovisionnement",
                "4. **Formation Commerciale**: Partage des best practices",
                "",
                "---",
                "Ce rapport a été généré automatiquement par le système BI Northwind."
            ])
            
            # Sauvegarde
            rapport_path = self.reports_path / 'rapport_business.md'
            with open(rapport_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(rapport))
            
            print(f"✅ Rapport business généré: {rapport_path}")
            return rapport_path
            
        except Exception as e:
            print(f"❌ Erreur génération rapport business: {e}")
            return None
    
    def generer_readme(self):
        """Génère le fichier README.md principal"""
        print("📖 CRÉATION DU README.md")
        
        readme_content = [
            "# 🚀 Northwind Business Intelligence Project",
            "",
            "## 📊 Description du Projet",
            "Solution complète de Business Intelligence pour analyser les données de Northwind Traders.",
            "Ce projet implémente un pipeline ETL, des analyses KPI, des visualisations et un dashboard interactif.",
            "",
            "## 🎯 Objectifs",
            "- ✅ Nettoyage et préparation des données (ETL)",
            "- ✅ Calcul d'indicateurs de performance (KPI)", 
            "- ✅ Création de visualisations et graphiques",
            "- ✅ Développement d'un dashboard interactif",
            "- ✅ Génération de rapports détaillés",
            "",
            "## 📁 Structure du Projet",
            "```",
            "northwind_bi_project/",
            "├── data/                   # Données",
            "│   ├── raw/               # Fichiers Excel originaux",
            "│   └── processed/         # Données nettoyées (CSV)",
            "├── scripts/               # Code source Python",
            "│   ├── main.py            # Script principal avec menu",
            "│   ├── etl_main.py        # Processus ETL",
            "│   ├── analysis_main.py   # Analyse des KPI",
            "│   ├── visualizations.py  # Création graphiques",
            "│   ├── dashboard.py       # Dashboard interactif",
            "│   └── generate_reports.py # Génération rapports",
            "├── figures/               # Graphiques exportés",
            "│   ├── ventes/",
            "│   ├── produits/",
            "│   ├── clients/",
            "│   └── interactifs/       # Graphiques HTML",
            "├── reports/               # Rapports générés",
            "├── video/                 # Matériel pour vidéo",
            "└── README.md              # Ce fichier",
            "```",
            "",
            "## 🛠️ Installation",
            "### Prérequis",
            "- Python 3.8 ou supérieur",
            "- pip (gestionnaire de packages Python)",
            "",
            "### Installation des Dépendances",
            "```bash",
            "pip install -r requirements.txt",
            "```",
            "",
            "## 🚀 Utilisation",
            "### Méthode Recommandée (Menu Interactif)",
            "```bash",
            "cd scripts",
            "python main.py",
            "```",
            "",
            "### Méthodes Directes",
            "```bash",
            "# ETL seulement",
            "python etl_main.py",
            "",
            "# Analyse seulement", 
            "python analysis_main.py",
            "",
            "# Visualisations seulement",
            "python visualizations.py",
            "",
            "# Dashboard seulement",
            "python dashboard.py",
            "```",
            "",
            "## 📊 Fonctionnalités",
            "### Processus ETL",
            "- Chargement des fichiers Excel",
            "- Nettoyage et validation des données",
            "- Création de tables de faits",
            "- Export en CSV standardisé",
            "",
            "### Analyse des KPI",
            "- Chiffre d'affaires et profit",
            "- Performance produits et clients",
            "- Analyse temporelle",
            "- Segmentation et tendances",
            "",
            "### Visualisations",
            "- Graphiques statiques (PNG)",
            "- Graphiques interactifs (HTML)",
            "- Dashboard combiné",
            "",
            "### Dashboard Interactif",
            "- Interface web moderne",
            "- Filtres temps réel",
            "- KPI dynamiques",
            "- Graphiques interactifs",
            "- Accessible sur http://localhost:8050",
            "",
            "## 📈 Résultats et Insights",
            "Le projet permet de découvrir:",
            "- Les produits les plus rentables",
            "- Les clients les plus fidèles",
            "- La performance des commerciaux", 
            "- Les tendances de vente",
            "- Les opportunités d'optimisation",
            "",
            "## 🔧 Technologies Utilisées",
            "### Bibliothèques Python",
            "- **pandas** : Manipulation de données",
            "- **numpy** : Calculs numériques",
            "- **matplotlib/seaborn** : Visualisations statiques",
            "- **plotly** : Visualisations interactives",
            "- **dash** : Framework dashboard web",
            "- **openpyxl** : Lecture fichiers Excel",
            "",
            "### Justification des Choix",
            "- **pandas** : Standard pour données tabulaires",
            "- **plotly/dash** : Meilleure solution dashboards interactifs",
            "- **matplotlib** : Référence visualisation Python",
            "",
            "## 📄 Livrables",
            "- ✅ Scripts Python complets",
            "- ✅ Rapport technique détaillé", 
            "- ✅ Rapport business synthétique",
            "- ✅ Dashboard interactif",
            "- ✅ Graphiques et visualisations",
            "- ✅ Documentation complète",
            "",
            "## 👨‍💼 Auteur",
            "[Votre Nom] - Projet Business Intelligence",
            "",
            "## 📝 Licence",
            "Projet éducatif - Northwind Traders",
            "",
            "---",
            "*Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d')}*"
        ]
        
        readme_path = self.project_path / 'README.md'
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(readme_content))
        
        print(f"✅ README.md généré: {readme_path}")
        return readme_path
    
    def generer_requirements(self):
        """Génère le fichier requirements.txt"""
        print("📋 CRÉATION DU FICHIER REQUIREMENTS")
        
        requirements = [
            "# Dépendances Python - Projet Northwind BI",
            "# Généré automatiquement",
            "",
            "# Data manipulation",
            "pandas>=1.5.0",
            "numpy>=1.21.0",
            "openpyxl>=3.0.0",
            "",
            "# Visualization",
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0", 
            "plotly>=5.10.0",
            "",
            "# Dashboard",
            "dash>=2.7.0",
            "",
            "# Utilities",
            "jupyter>=1.0.0",
            "ipython>=8.0.0"
        ]
        
        requirements_path = self.project_path / 'requirements.txt'
        with open(requirements_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(requirements))
        
        print(f"✅ requirements.txt généré: {requirements_path}")
        return requirements_path
    
    def generer_script_video(self):
        """Génère le script pour la vidéo de présentation"""
        print("🎥 CRÉATION DU SCRIPT VIDÉO")
        
        video_path = self.project_path / 'video'
        video_path.mkdir(exist_ok=True)
        
        script = [
            "SCRIPT VIDÉO - PRÉSENTATION PROJET NORTHWIND BI",
            "=" * 60,
            "Durée estimée: 5-7 minutes",
            "Format: Capture d'écran + voix off",
            "",
            "SCÈNE 1: INTRODUCTION (30 secondes)",
            "VISUEL: Page d'accueil du dashboard",
            "VOIX:",
            "\"Bonjour et bienvenue dans cette présentation du projet Northwind Business Intelligence.",
            "Je vais vous montrer comment nous avons transformé des données brutes en insights actionnables",
            "grâce à une solution BI complète développée en Python.\"",
            "",
            "SCÈNE 2: PRÉSENTATION DU PROJET (1 minute)",
            "VISUEL: Structure des dossiers + énoncé du projet",
            "VOIX:",
            "\"L'objectif était de créer une solution BI complète basée sur la base Northwind.",
            "Les livrables incluent un processus ETL, des analyses KPI, des visualisations,",
            "un dashboard interactif, et bien sûr ce rapport de présentation.\"",
            "",
            "SCÈNE 3: PROCESSUS ETL (1 minute)", 
            "VISUEL: Exécution du script ETL + données avant/après",
            "VOIX:",
            "\"Commençons par le processus ETL - Extract, Transform, Load.",
            "Nous chargeons les fichiers Excel bruts, nettoyons les données, gérons les valeurs manquantes,",
            "et créons une structure standardisée pour l'analyse.\"",
            "",
            "SCÈNE 4: ANALYSE ET KPI (1 minute)",
            "VISUEL: Exécution analyse + résultats KPI",
            "VOIX:",
            "\"L'analyse nous permet de calculer des indicateurs clés comme le chiffre d'affaires,",
            "les marges, la performance des produits et clients, et les tendances temporelles.\"",
            "",
            "SCÈNE 5: VISUALISATIONS (1 minute)",
            "VISUEL: Graphiques générés + démonstration interactifs",
            "VOIX:",
            "\"Nous créons ensuite des visualisations à la fois statiques pour les rapports",
            "et interactives pour l'exploration des données. Voici quelques exemples...\"",
            "",
            "SCÈNE 6: DASHBOARD INTERACTIF (2 minutes)",
            "VISUEL: Navigation complète dans le dashboard",
            "VOIX:",
            "\"Le dashboard interactif rassemble tous ces éléments dans une interface web moderne.",
            "Vous pouvez filtrer par période, catégorie, employé... et voir les mises à jour en temps réel.",
            "Voici comment identifier les produits les plus rentables...\"",
            "*Démonstration des fonctionnalités*",
            "",
            "SCÈNE 7: INSIGHTS ET CONCLUSION (1 minute)",
            "VISUEL: Slide récapitulatif des insights",
            "VOIX:",
            "\"Ce projet nous a permis d'identifier plusieurs insights business importants:",
            "- Les top 5 produits représentent X% du chiffre d'affaires",
            "- Les clients VIP génèrent Y% du revenue",
            "- Nous observons une tendance de croissance sur Z période",
            "Ces insights permettent des décisions business éclairées.\"",
            "",
            "SCÈNE 8: CONCLUSION (30 secondes)",
            "VISUEL: Dashboard final + contact",
            "VOIX:",
            "\"En conclusion, ce projet démontre la puissance d'une approche BI complète",
            "pour transformer des données en décisions stratégiques.",
            "Merci de votre attention.\"",
            "",
            "PLAN DE TOURNAGE:",
            "- Captures d'écran de chaque étape",
            "- Démonstration en direct du dashboard", 
            "- Graphiques et visualisations",
            "- Code source et architecture",
            "- Slides de synthèse"
        ]
        
        script_path = video_path / 'script_video.md'
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(script))
        
        print(f"✅ Script vidéo généré: {script_path}")
        return script_path
    
    def generer_arborescence(self):
        """Génère un fichier d'arborescence du projet"""
        print("📁 GÉNÉRATION DE L'ARBORESCENCE")
        
        def list_files(startpath):
            lines = []
            for root, dirs, files in os.walk(startpath):
                level = root.replace(startpath, '').count(os.sep)
                indent = ' ' * 2 * level
                lines.append(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    if not file.startswith('.') and not file.startswith('__'):
                        lines.append(f"{subindent}{file}")
            return lines
        
        try:
            import os
            arborescence = list_files(str(self.project_path))
            
            arbo_path = self.reports_path / 'arborescence_projet.txt'
            with open(arbo_path, 'w', encoding='utf-8') as f:
                f.write("ARBORESCENCE DU PROJET NORTHWIND BI\n")
                f.write("=" * 50 + "\n\n")
                f.write('\n'.join(arborescence))
            
            print(f"✅ Arborescence générée: {arbo_path}")
            return arbo_path
            
        except Exception as e:
            print(f"❌ Erreur génération arborescence: {e}")
            return None
    
    def executer_generation_complete(self):
        """Exécute la génération complète des livrables"""
        print("🚀 DÉMARRAGE GÉNÉRATION DES LIVRABLES")
        print("=" * 60)
        
        try:
            # Création de tous les rapports
            self.generer_rapport_technique()
            self.generer_rapport_business()
            self.generer_readme()
            self.generer_requirements()
            self.generer_script_video()
            self.generer_arborescence()
            
            print("\n🎉 GÉNÉRATION TERMINÉE AVEC SUCCÈS!")
            print("=" * 50)
            print("📁 LIVRABLES CRÉÉS:")
            print("├── reports/rapport_technique.md")
            print("├── reports/rapport_business.md") 
            print("├── README.md")
            print("├── requirements.txt")
            print("├── video/script_video.md")
            print("└── reports/arborescence_projet.txt")
            print("\n🎯 VOTRE PROJET EST MAINTENANT COMPLET!")
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération: {e}")

def generer_livrables_complets():
    """Fonction pour exécuter la génération des livrables"""
    rapporteur = RapportFinal()
    rapporteur.executer_generation_complete()

if __name__ == "__main__":
    generer_livrables_complets()