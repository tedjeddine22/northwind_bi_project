# scripts/01_exploration.py
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

class ExplorationDonnees:
    def __init__(self):
        self.data_path = Path('../data/raw')
        self.donnees = {}
        self.rapport = []
        
    def charger_toutes_donnees(self):
        """Charge tous les fichiers Excel"""
        print("📥 CHARGEMENT DES DONNÉES")
        print("=" * 50)
        
        fichiers = {
            'orders': 'Orders.xlsx',
            'order_details': 'Order Details.xlsx',
            'products': 'Products.xlsx', 
            'customers': 'Customers.xlsx',
            'employees': 'Employees.xlsx',
            'inventory': 'Inventory Transactions.xlsx',
            'inventory_types': 'Inventory Transaction Types.xlsx',
            'orders_status': 'Orders Status.xlsx',
            'order_details_status': 'Order Details Status.xlsx'
        }
        
        for nom, fichier in fichiers.items():
            try:
                chemin = self.data_path / fichier
                self.donnees[nom] = pd.read_excel(chemin)
                self.rapport.append(f"✅ {fichier}: {len(self.donnees[nom])} lignes, {len(self.donnees[nom].columns)} colonnes")
                print(f"✅ {fichier} chargé")
            except Exception as e:
                erreur = f"❌ {fichier}: {e}"
                self.rapport.append(erreur)
                print(erreur)
                
        return self.donnees
    
    def analyser_structure(self):
        """Analyse détaillée de la structure"""
        print("\n🔍 ANALYSE DE STRUCTURE")
        print("=" * 50)
        
        for nom, df in self.donnees.items():
            print(f"\n📊 {nom.upper()}")
            print(f"   Shape: {df.shape}")
            print(f"   Colonnes: {list(df.columns)}")
            print(f"   Types:\n{df.dtypes}")
            print(f"   Valeurs manquantes:\n{df.isnull().sum()}")
            
            # Ajout au rapport
            self.rapport.append(f"\n📊 {nom.upper()}")
            self.rapport.append(f"Shape: {df.shape}")
            self.rapport.append(f"Colonnes: {list(df.columns)}")
    
    def analyser_relations(self):
        """Identifie les relations entre les tables"""
        print("\n🔗 ANALYSE DES RELATIONS")
        print("=" * 50)
        
        relations = """
        📋 RELATIONS IDENTIFIÉES :
        
        Customers (1) ←→ (Many) Orders (1) ←→ (Many) Order Details (Many) ←→ (1) Products
            ↓                                                            ↓
        Employees (vendeurs)                                      Inventory Transactions
            ↓                                                            ↓
        Employee Privileges ←→ Privileges                      Inventory Transaction Types
        
        Orders Status → Orders
        Order Details Status → Order Details  
        Orders Tax Status → Orders
        """
        
        print(relations)
        self.rapport.append(relations)
    
    def generer_rapport(self):
        """Génère un rapport d'exploration"""
        print("\n📄 GÉNÉRATION DU RAPPORT")
        print("=" * 50)
        
        with open('../reports/exploration_rapport.txt', 'w', encoding='utf-8') as f:
            f.write("RAPPORT D'EXPLORATION - NORTHWIND TRADERS\n")
            f.write("=" * 50 + "\n\n")
            for ligne in self.rapport:
                f.write(ligne + "\n")
        
        print("✅ Rapport sauvegardé: reports/exploration_rapport.txt")
    
    def executer_exploration_complete(self):
        """Exécute l'exploration complète"""
        print("🚀 DÉMARRAGE EXPLORATION COMPLÈTE")
        self.charger_toutes_donnees()
        self.analyser_structure() 
        self.analyser_relations()
        self.generer_rapport()
        print("\n🎉 EXPLORATION TERMINÉE!")
        return self.donnees

if __name__ == "__main__":
    explore = ExplorationDonnees()
    explore.executer_exploration_complete()