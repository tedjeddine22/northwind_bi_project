# scripts/analysis_main.py
import pandas as pd
import numpy as np
from pathlib import Path
import time

class AnalyseNorthwind:
    def __init__(self):
        self.data_path = Path('../data/processed')
        self.donnees = {}
        self.kpis = {}
        
    def charger_donnees_propres(self):
        """Charge les données nettoyées"""
        print("📥 CHARGEMENT DES DONNÉES NETTOYÉES")
        
        try:
            # Charger la table de faits
            chemin_faits = self.data_path / 'sales_facts_clean.csv'
            if chemin_faits.exists():
                self.donnees['sales_facts'] = pd.read_csv(chemin_faits, parse_dates=['order_date'])
                print(f"✅ sales_facts_clean.csv chargé ({len(self.donnees['sales_facts'])} lignes)")
            else:
                print("❌ Fichier sales_facts_clean.csv non trouvé")
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ Erreur chargement: {e}")
            return False
    
    def calculer_kpi_principaux(self):
        """Calcule les KPI principaux"""
        print("💰 CALCUL DES KPI PRINCIPAUX")
        
        if 'sales_facts' not in self.donnees:
            return False
            
        df = self.donnees['sales_facts']
        
        # KPI de base
        self.kpis['chiffre_affaires_total'] = df['Line Total'].sum()
        self.kpis['profit_total'] = df['Profit'].sum()
        self.kpis['nombre_commandes'] = df['order_id'].nunique()
        self.kpis['nombre_clients'] = df['customer_company'].nunique()
        self.kpis['nombre_produits'] = df['product_name'].nunique()
        self.kpis['quantite_totale'] = df['Quantity'].sum()
        
        # KPI calculés
        self.kpis['marge_moyenne'] = (self.kpis['profit_total'] / self.kpis['chiffre_affaires_total'] * 100) if self.kpis['chiffre_affaires_total'] > 0 else 0
        self.kpis['panier_moyen'] = self.kpis['chiffre_affaires_total'] / self.kpis['nombre_commandes'] if self.kpis['nombre_commandes'] > 0 else 0
        
        print("✅ KPI calculés avec succès")
        return True
    
    def analyser_performance(self):
        """Analyse de performance détaillée"""
        print("📊 ANALYSE DE PERFORMANCE DÉTAILLÉE")
        
        if 'sales_facts' not in self.donnees:
            return
            
        df = self.donnees['sales_facts']
        
        # Top 10 produits par CA
        self.kpis['top_produits_ca'] = df.groupby('product_name')['Line Total'].sum().sort_values(ascending=False).head(10)
        
        # Top 10 clients par CA
        self.kpis['top_clients_ca'] = df.groupby('customer_company')['Line Total'].sum().sort_values(ascending=False).head(10)
        
        # Performance par employé
        self.kpis['performance_employes'] = df.groupby('employee_name')['Line Total'].sum().sort_values(ascending=False)
        
        print("✅ Analyse de performance terminée")
    
    def generer_rapport(self):
        """Génère un rapport des résultats"""
        print("📄 GÉNÉRATION DU RAPPORT")
        
        rapport = [
            "RAPPORT D'ANALYSE NORTHWIND TRADERS",
            "=" * 40,
            f"Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "KPI PRINCIPAUX:",
            f"Chiffre d'affaires total: {self.kpis.get('chiffre_affaires_total', 0):,.2f} $",
            f"Profit total: {self.kpis.get('profit_total', 0):,.2f} $",
            f"Marge moyenne: {self.kpis.get('marge_moyenne', 0):.1f} %",
            f"Nombre de commandes: {self.kpis.get('nombre_commandes', 0)}",
            f"Nombre de clients: {self.kpis.get('nombre_clients', 0)}",
            f"Panier moyen: {self.kpis.get('panier_moyen', 0):.2f} $",
            "",
            "TOP 5 PRODUITS:"
        ]
        
        # Ajouter les top produits
        if 'top_produits_ca' in self.kpis:
            for i, (produit, ca) in enumerate(self.kpis['top_produits_ca'].head().items(), 1):
                rapport.append(f"{i}. {produit}: {ca:,.2f} $")
        
        # Sauvegarder le rapport
        with open('../reports/rapport_analyse.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(rapport))
        
        print("✅ Rapport généré: reports/rapport_analyse.txt")
    
    def executer_analyse_complete(self):
        """Exécute l'analyse complète"""
        print("🚀 DÉMARRAGE ANALYSE COMPLÈTE")
        print("=" * 50)
        
        try:
            # 1. Chargement
            if not self.charger_donnees_propres():
                return None
            
            # 2. Calculs KPI
            if not self.calculer_kpi_principaux():
                return None
            
            # 3. Analyses détaillées
            self.analyser_performance()
            
            # 4. Rapport
            self.generer_rapport()
            
            print("🎉 ANALYSE TERMINÉE AVEC SUCCÈS!")
            return self.kpis
            
        except Exception as e:
            print(f"💥 ERREUR ANALYSE: {e}")
            return None

# Fonction pour exécuter directement
def executer_analyse():
    analyse = AnalyseNorthwind()
    return analyse.executer_analyse_complete()

if __name__ == "__main__":
    resultat = executer_analyse()