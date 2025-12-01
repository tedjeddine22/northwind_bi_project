# scripts/dashboard_simple.py
import dash
from dash import dcc, html
import pandas as pd
from pathlib import Path
import plotly.express as px

def lancer_dashboard_simple():
    """Lance une version simple et fiable du dashboard"""
    print("🚀 LANCEMENT DU DASHBOARD SIMPLIFIÉ...")
    
    try:
        # Charger les données
        data_path = Path('../data/processed/sales_facts_clean.csv')
        df = pd.read_csv(data_path)
        print(f"✅ Données chargées: {len(df)} lignes")
        
        # Application Dash simple
        app = dash.Dash(__name__)
        
        # Layout simple
        app.layout = html.Div([
            html.H1("📊 NORTHWIND TRADERS - DASHBOARD", 
                   style={'textAlign': 'center', 'color': '#2E86AB', 'padding': '20px'}),
            
            html.Div([
                html.Div([
                    html.H3("💰 CA Total"),
                    html.H2(f"{df['Line Total'].sum():,.0f} $", 
                           style={'color': '#2E86AB'})
                ], style={'textAlign': 'center', 'padding': '20px', 
                         'backgroundColor': 'white', 'margin': '10px', 
                         'borderRadius': '10px', 'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'}),
            ], style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap'}),
            
            html.Div([
                dcc.Graph(
                    figure=px.bar(
                        df.groupby('product_name')['Line Total'].sum().sort_values(ascending=False).head(10).reset_index(),
                        x='Line Total', y='product_name', orientation='h',
                        title='Top 10 Produits par Chiffre d\'Affaires'
                    )
                )
            ], style={'padding': '20px'}),
            
            html.P("🌐 Dashboard Northwind - Version Simplifiée", 
                   style={'textAlign': 'center', 'color': '#666', 'marginTop': '30px'})
        ], style={'backgroundColor': '#f8f9fa', 'minHeight': '100vh'})
        
        print("✅ Dashboard simple créé!")
        print("🌐 Accédez à: http://localhost:8060")
        print("💡 Arrêtez avec Ctrl+C")
        
        app.run(debug=True, port=8060)
        
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    lancer_dashboard_simple()