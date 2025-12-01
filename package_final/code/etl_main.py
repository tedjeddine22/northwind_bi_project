# scripts/etl_main.py
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class ETLNorthwind:
    def __init__(self):
        self.data_path = Path('../data')
        self.raw_path = self.data_path / 'raw'
        self.processed_path = self.data_path / 'processed'
        self.donnees_brutes = {}
        self.donnees_propres = {}
        
    def charger_donnees_brutes(self):
        """Charge les données brutes"""
        print("📥 CHARGEMENT DES DONNÉES BRUTES")
        
        try:
            # Liste des fichiers à charger
            fichiers = {
                'orders': 'Orders.xlsx',
                'order_details': 'Order Details.xlsx',
                'products': 'Products.xlsx',
                'customers': 'Customers.xlsx',
                'employees': 'Employees.xlsx'
            }
            
            for nom, fichier in fichiers.items():
                chemin = self.raw_path / fichier
                if chemin.exists():
                    self.donnees_brutes[nom] = pd.read_excel(chemin)
                    print(f"✅ {fichier} chargé ({len(self.donnees_brutes[nom])} lignes)")
                else:
                    print(f"❌ Fichier manquant: {fichier}")
            
            return self.donnees_brutes
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement: {e}")
            return None
    
    def nettoyer_orders(self):
        """Nettoie la table Orders"""
        print("🧹 NETTOYAGE TABLE ORDERS")
        
        if 'orders' not in self.donnees_brutes:
            print("❌ Table 'orders' non chargée")
            return None
            
        df = self.donnees_brutes['orders'].copy()
        
        # Conversion des dates
        df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
        df['Shipped Date'] = pd.to_datetime(df['Shipped Date'], errors='coerce')
        
        # Nettoyage des valeurs numériques
        df['Shipping Fee'] = pd.to_numeric(df['Shipping Fee'], errors='coerce').fillna(0)
        df['Taxes'] = pd.to_numeric(df['Taxes'], errors='coerce').fillna(0)
        
        # Calcul du délai de livraison
        df['Delivery Days'] = (df['Shipped Date'] - df['Order Date']).dt.days
        
        self.donnees_propres['orders'] = df
        print(f"✅ Orders nettoyée: {len(df)} lignes")
        return df
    
    def nettoyer_order_details(self):
        """Nettoie la table Order Details"""
        print("🧹 NETTOYAGE TABLE ORDER DETAILS")
        
        if 'order_details' not in self.donnees_brutes:
            print("❌ Table 'order_details' non chargée")
            return None
            
        df = self.donnees_brutes['order_details'].copy()
        
        # Nettoyage numérique
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        df['Unit Price'] = pd.to_numeric(df['Unit Price'], errors='coerce')
        df['Discount'] = pd.to_numeric(df['Discount'], errors='coerce').fillna(0)
        
        # Calcul du total par ligne
        df['Line Total'] = df['Quantity'] * df['Unit Price'] * (1 - df['Discount'])
        
        self.donnees_propres['order_details'] = df
        print(f"✅ Order Details nettoyée: {len(df)} lignes")
        return df
    
    def nettoyer_products(self):
        """Nettoie la table Products"""
        print("🧹 NETTOYAGE TABLE PRODUCTS")
        
        if 'products' not in self.donnees_brutes:
            print("❌ Table 'products' non chargée")
            return None
            
        df = self.donnees_brutes['products'].copy()
        
        # Nettoyage des prix
        df['Standard Cost'] = pd.to_numeric(df['Standard Cost'], errors='coerce')
        df['List Price'] = pd.to_numeric(df['List Price'], errors='coerce')
        
        # Calcul de la marge
        df['Profit Margin'] = df['List Price'] - df['Standard Cost']
        
        self.donnees_propres['products'] = df
        print(f"✅ Products nettoyée: {len(df)} produits")
        return df
    
    def creer_table_faits(self):
        """Crée la table de faits principale"""
        print("🔗 CRÉATION TABLE DE FAITS")
        
        try:
            # Jointure Orders + Order Details
            faits = self.donnees_propres['order_details'].merge(
                self.donnees_propres['orders'][['Order ID', 'Order Date', 'Customer', 'Employee', 'Shipping Fee']],
                on='Order ID',
                how='left'
            )
            
            # Jointure avec Products
            faits = faits.merge(
                self.donnees_propres['products'][['Product Name', 'Category', 'Standard Cost']],
                left_on='Product',
                right_on='Product Name',
                how='left'
            )
            
            # Calcul du profit
            faits['Profit'] = (faits['Unit Price'] - faits['Standard Cost']) * faits['Quantity']
            
            # Renommage des colonnes
            faits = faits.rename(columns={
                'Order ID': 'order_id',
                'Order Date': 'order_date',
                'Customer': 'customer_company',
                'Employee': 'employee_name',
                'Product': 'product_name'
            })
            
            self.donnees_propres['sales_facts'] = faits
            print(f"✅ Table de faits créée: {len(faits)} lignes")
            return faits
            
        except Exception as e:
            print(f"❌ Erreur création table de faits: {e}")
            return None
    
    def sauvegarder_donnees(self):
        """Sauvegarde les données nettoyées"""
        print("💾 SAUVEGARDE DES DONNÉES NETTOYÉES")
        
        # Créer le dossier s'il n'existe pas
        self.processed_path.mkdir(exist_ok=True)
        
        for nom, df in self.donnees_propres.items():
            try:
                chemin = self.processed_path / f"{nom}_clean.csv"
                df.to_csv(chemin, index=False)
                print(f"✅ {nom}_clean.csv sauvegardé ({len(df)} lignes)")
            except Exception as e:
                print(f"❌ Erreur sauvegarde {nom}: {e}")
    
    def executer_etl_complet(self):
        """Exécute l'ETL complet"""
        print("🚀 DÉMARRAGE ETL COMPLET")
        print("=" * 50)
        
        try:
            # 1. Chargement
            if not self.charger_donnees_brutes():
                return None
            
            # 2. Nettoyage
            self.nettoyer_orders()
            self.nettoyer_order_details()
            self.nettoyer_products()
            
            # 3. Table de faits
            self.creer_table_faits()
            
            # 4. Sauvegarde
            self.sauvegarder_donnees()
            
            print("🎉 ETL TERMINÉ AVEC SUCCÈS!")
            return self.donnees_propres
            
        except Exception as e:
            print(f"💥 ERREUR ETL: {e}")
            return None

# Fonction pour exécuter directement
def executer_etl():
    etl = ETLNorthwind()
    return etl.executer_etl_complet()

if __name__ == "__main__":
    resultat = executer_etl()