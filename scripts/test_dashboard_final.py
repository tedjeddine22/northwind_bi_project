# scripts/test_dashboard_final.py
print("🚀 TEST DU DASHBOARD NORTHWIND")
print("=" * 40)

try:
    # Test des imports
    import dash
    from dash import dcc, html
    import pandas as pd
    import plotly.express as px
    print("✅ Toutes les bibliothèques importées avec succès")
    
    # Test du chargement des données
    from pathlib import Path
    data_path = Path('../data/processed/sales_facts_clean.csv')
    
    if data_path.exists():
        df = pd.read_csv(data_path)
        print(f"✅ Données chargées: {len(df)} lignes")
        
        # Création d'un dashboard minimal
        app = dash.Dash(__name__)
        
        # Calcul des KPI
        ca_total = df['Line Total'].sum()
        nb_commandes = df['order_id'].nunique()
        nb_clients = df['customer_company'].nunique()
        
        app.layout = html.Div([
            html.H1("🎉 DASHBOARD NORTHWIND - TEST RÉUSSI", 
                   style={'textAlign': 'center', 'color': 'green', 'padding': '20px'}),
            
            html.Div([
                html.Div([
                    html.H3("💰 CA Total"),
                    html.H2(f"{ca_total:,.0f} $")
                ], style={'textAlign': 'center', 'padding': '20px', 'margin': '10px', 
                         'backgroundColor': '#e8f5e8', 'borderRadius': '10px'}),
                
                html.Div([
                    html.H3("📦 Commandes"),
                    html.H2(f"{nb_commandes}")
                ], style={'textAlign': 'center', 'padding': '20px', 'margin': '10px',
                         'backgroundColor': '#e8f5e8', 'borderRadius': '10px'}),
                
                html.Div([
                    html.H3("👥 Clients"),
                    html.H2(f"{nb_clients}")
                ], style={'textAlign': 'center', 'padding': '20px', 'margin': '10px',
                         'backgroundColor': '#e8f5e8', 'borderRadius': '10px'})
            ], style={'display': 'flex', 'justifyContent': 'center', 'flexWrap': 'wrap'}),
            
            html.P("✅ Votre dashboard fonctionne parfaitement!",
                  style={'textAlign': 'center', 'color': 'green', 'fontSize': '20px', 'marginTop': '30px'})
        ])
        
        print("✅ Dashboard créé avec succès!")
        print("🌐 Lancement sur http://localhost:8070")
        print("💡 Arrêtez avec Ctrl+C")
        
        app.run(debug=True, port=8070)
        
    else:
        print("❌ Fichier de données non trouvé!")
        print("💡 Exécutez d'abord l'ETL (python main.py -> option 1)")
        
except Exception as e:
    print(f"❌ ERREUR: {e}")
    print("\n🔧 SOLUTIONS:")
    print("1. Exécutez d'abord l'ETL: python main.py -> option 1")
    print("2. Installez les dépendances: pip install dash plotly pandas")
    input("\nAppuyez sur Entrée pour continuer...")