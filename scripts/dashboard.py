# scripts/dashboard.py
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
import os
warnings.filterwarnings('ignore')

class DashboardNorthwind:
    def __init__(self):
        # Chemin relatif corrigé
        current_dir = Path(__file__).parent
        self.data_path = current_dir / 'data' / 'processed'
        
        # Créer le dossier si nécessaire
        self.data_path.mkdir(parents=True, exist_ok=True)
        self.donnees = {}
        
    def charger_donnees(self):
        """Charge les données pour le dashboard"""
        print("📥 CHARGEMENT DES DONNÉES POUR LE DASHBOARD")
        print(f"📁 Recherche dans: {self.data_path}")
        
        try:
            # Vérifier si le dossier existe
            if not self.data_path.exists():
                print(f"❌ Dossier non trouvé: {self.data_path}")
                return False
                
            # Liste les fichiers disponibles
            fichiers = list(self.data_path.glob('*.csv'))
            print(f"📋 Fichiers trouvés: {[f.name for f in fichiers]}")
            
            # Charger la table de faits
            chemin_faits = self.data_path / 'sales_facts_clean.csv'
            if chemin_faits.exists():
                self.donnees['sales_facts'] = pd.read_csv(chemin_faits)
                print(f"✅ Données de vente chargées: {len(self.donnees['sales_facts'])} lignes")
                
                # Convertir les dates si la colonne existe
                if 'order_date' in self.donnees['sales_facts'].columns:
                    self.donnees['sales_facts']['order_date'] = pd.to_datetime(self.donnees['sales_facts']['order_date'])
            else:
                print("❌ Fichier sales_facts_clean.csv non trouvé")
                print("💡 Essayez de générer d'abord les données avec analysis_main.py")
                return False
                
            # Charger les produits (optionnel)
            chemin_produits = self.data_path / 'products_clean.csv'
            if chemin_produits.exists():
                self.donnees['products'] = pd.read_csv(chemin_produits)
                print(f"✅ Données produits chargées: {len(self.donnees['products'])} produits")
                
            return True
            
        except Exception as e:
            print(f"❌ Erreur chargement: {e}")
            import traceback
            traceback.print_exc()
            return False

    def creer_donnees_exemple(self):
        """Crée des données d'exemple si les fichiers sont manquants"""
        print("🔄 Création de données d'exemple...")
        
        # Données d'exemple pour tester
        dates = pd.date_range('2023-01-01', '2024-01-01', freq='D')
        n_records = 1000
        
        donnees_exemple = {
            'order_id': [f'ORD_{i:04d}' for i in range(n_records)],
            'order_date': np.random.choice(dates, n_records),
            'customer_company': np.random.choice(['Client A', 'Client B', 'Client C', 'Client D'], n_records),
            'employee_name': np.random.choice(['Alice', 'Bob', 'Charlie', 'Diana'], n_records),
            'product_name': np.random.choice(['Produit 1', 'Produit 2', 'Produit 3', 'Produit 4'], n_records),
            'Category': np.random.choice(['Catégorie A', 'Catégorie B', 'Catégorie C'], n_records),
            'Quantity': np.random.randint(1, 50, n_records),
            'UnitPrice': np.random.uniform(10, 100, n_records),
            'Line Total': np.random.uniform(100, 5000, n_records),
            'Profit': np.random.uniform(10, 500, n_records)
        }
        
        self.donnees['sales_facts'] = pd.DataFrame(donnees_exemple)
        print("✅ Données d'exemple créées")
        return True

    def calculer_kpi(self, df):
        """Calcule les KPI pour le dashboard"""
        try:
            kpis = {
                'ca_total': df['Line Total'].sum(),
                'profit_total': df['Profit'].sum() if 'Profit' in df.columns else df['Line Total'].sum() * 0.2,
                'nb_commandes': df['order_id'].nunique(),
                'nb_clients': df['customer_company'].nunique(),
                'nb_produits': df['product_name'].nunique(),
                'quantite_totale': df['Quantity'].sum() if 'Quantity' in df.columns else 0
            }
            
            kpis['marge_moyenne'] = (kpis['profit_total'] / kpis['ca_total'] * 100) if kpis['ca_total'] > 0 else 0
            kpis['panier_moyen'] = kpis['ca_total'] / kpis['nb_commandes'] if kpis['nb_commandes'] > 0 else 0
            
            return kpis
        except Exception as e:
            print(f"❌ Erreur calcul KPI: {e}")
            # Retourner des KPI par défaut
            return {
                'ca_total': 0, 'profit_total': 0, 'nb_commandes': 0, 
                'nb_clients': 0, 'nb_produits': 0, 'quantite_totale': 0,
                'marge_moyenne': 0, 'panier_moyen': 0
            }

    def creer_dashboard(self):
        """Crée l'application Dash"""
        print("🚀 CRÉATION DU DASHBOARD INTERACTIF")
        
        # Charger les données ou créer des exemples
        if not self.charger_donnees():
            print("⚠️  Utilisation de données d'exemple")
            if not self.creer_donnees_exemple():
                return None
            
        df = self.donnees['sales_facts']
        
        # Initialiser l'app Dash
        app = dash.Dash(__name__)
        
        # Calculer les KPI globaux
        kpis = self.calculer_kpi(df)
        
        # Préparer les données pour les graphiques
        if 'order_date' in df.columns:
            df['order_date'] = pd.to_datetime(df['order_date'])
            df['mois'] = df['order_date'].dt.to_period('M').astype(str)
            df['annee'] = df['order_date'].dt.year
        else:
            # Créer des dates fictives si non disponibles
            df['mois'] = '2023-01'
            df['annee'] = 2023
        
        # Layout du dashboard (identique à votre code original)
        app.layout = html.Div([
            # Votre layout existant ici...
            html.Div([
                html.H1("📊 DASHBOARD NORTHWIND TRADERS", 
                       style={'textAlign': 'center', 'color': '#2E86AB', 'marginBottom': 0}),
                html.P("Business Intelligence - Analyse des performances commerciales",
                      style={'textAlign': 'center', 'color': '#666', 'marginTop': 0}),
            ], style={'backgroundColor': '#f8f9fa', 'padding': '20px', 'marginBottom': '20px'}),
            
            # Les autres composants...
            html.Div([
                html.Div([
                    html.H4("💰 CA Total", style={'color': '#2E86AB', 'marginBottom': '5px'}),
                    html.H2(f"{kpis['ca_total']:,.0f} $", style={'color': '#2E86AB', 'margin': '0'})
                ], style={'textAlign': 'center', 'padding': '15px', 'backgroundColor': 'white', 'borderRadius': '5px', 'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'})
            ], style={'textAlign': 'center', 'margin': '20px'}),
            
            html.Div([
                dcc.Graph(
                    figure=px.bar(df.head(20), x='product_name', y='Line Total', 
                                 title='Exemple de graphique - Top 20 ventes')
                )
            ])
        ])
        
        return app
    
    def lancer_dashboard(self, port=8050):  # Changement de port
        """Lance le dashboard"""
        app = self.creer_dashboard()
        if app is not None:
            print(f"🌐 Dashboard lancé sur http://localhost:{port}")
            print("💡 Arrêtez le dashboard avec Ctrl+C")
            try:
                app.run(debug=True, port=port, host='127.0.0.1')
            except OSError as e:
                if "Address already in use" in str(e):
                    print(f"❌ Le port {port} est déjà utilisé. Essayez un autre port.")
                    print("💡 Utilisez: netstat -ano | findstr :8050 pour vérifier")
                else:
                    print(f"❌ Erreur: {e}")
        else:
            print("❌ Impossible de créer le dashboard")

# Fonction pour exécuter directement
def executer_dashboard(port=8050):
    dashboard = DashboardNorthwind()
    dashboard.lancer_dashboard(port)

if __name__ == "__main__":
    executer_dashboard()