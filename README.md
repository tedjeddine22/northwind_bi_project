# 🚀 Northwind Business Intelligence Project

## 📊 Description du Projet
Solution complète de Business Intelligence pour analyser les données de Northwind Traders.
Ce projet implémente un pipeline ETL, des analyses KPI, des visualisations et un dashboard interactif.

## 🎯 Objectifs
- ✅ Nettoyage et préparation des données (ETL)
- ✅ Calcul d'indicateurs de performance (KPI)
- ✅ Création de visualisations et graphiques
- ✅ Développement d'un dashboard interactif
- ✅ Génération de rapports détaillés

## 📁 Structure du Projet
```
northwind_bi_project/
├── data/                   # Données
│   ├── raw/               # Fichiers Excel originaux
│   └── processed/         # Données nettoyées (CSV)
├── scripts/               # Code source Python
│   ├── main.py            # Script principal avec menu
│   ├── etl_main.py        # Processus ETL
│   ├── analysis_main.py   # Analyse des KPI
│   ├── visualizations.py  # Création graphiques
│   ├── dashboard.py       # Dashboard interactif
│   └── generate_reports.py # Génération rapports
├── figures/               # Graphiques exportés
│   ├── ventes/
│   ├── produits/
│   ├── clients/
│   └── interactifs/       # Graphiques HTML
├── reports/               # Rapports générés
├── video/                 # Matériel pour vidéo
└── README.md              # Ce fichier
```

## 🛠️ Installation
### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Installation des Dépendances
```bash
pip install -r requirements.txt
```

## 🚀 Utilisation
### Méthode Recommandée (Menu Interactif)
```bash
cd scripts
python main.py
```

### Méthodes Directes
```bash
# ETL seulement
python etl_main.py

# Analyse seulement
python analysis_main.py

# Visualisations seulement
python visualizations.py

# Dashboard seulement
python dashboard.py
```

## 📊 Fonctionnalités
### Processus ETL
- Chargement des fichiers Excel
- Nettoyage et validation des données
- Création de tables de faits
- Export en CSV standardisé

### Analyse des KPI
- Chiffre d'affaires et profit
- Performance produits et clients
- Analyse temporelle
- Segmentation et tendances

### Visualisations
- Graphiques statiques (PNG)
- Graphiques interactifs (HTML)
- Dashboard combiné

### Dashboard Interactif
- Interface web moderne
- Filtres temps réel
- KPI dynamiques
- Graphiques interactifs
- Accessible sur http://localhost:8050

## 📈 Résultats et Insights
Le projet permet de découvrir:
- Les produits les plus rentables
- Les clients les plus fidèles
- La performance des commerciaux
- Les tendances de vente
- Les opportunités d'optimisation

## 🔧 Technologies Utilisées
### Bibliothèques Python
- **pandas** : Manipulation de données
- **numpy** : Calculs numériques
- **matplotlib/seaborn** : Visualisations statiques
- **plotly** : Visualisations interactives
- **dash** : Framework dashboard web
- **openpyxl** : Lecture fichiers Excel

### Justification des Choix
- **pandas** : Standard pour données tabulaires
- **plotly/dash** : Meilleure solution dashboards interactifs
- **matplotlib** : Référence visualisation Python

## 📄 Livrables
- ✅ Scripts Python complets
- ✅ Rapport technique détaillé
- ✅ Rapport business synthétique
- ✅ Dashboard interactif
- ✅ Graphiques et visualisations
- ✅ Documentation complète

## 👨‍💼 Auteur
[Votre Nom] - Projet Business Intelligence

## 📝 Licence
Projet éducatif - Northwind Traders

---
*Dernière mise à jour: {datetime.now().strftime('%Y-%m-%d')}*