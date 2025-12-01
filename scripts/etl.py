# scripts/02_etl.py
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../reports/etl_log.txt'),
        logging.StreamHandler()
    ]
)

warnings.filterwarnings('ignore')

class ETLNorthwind:
    def __init__(self):
        self.data_path = Path('../data')
        self.raw_path = self.data_path / 'raw'
        self.processed_path = self.data_path / 'processed'
        self.donnees_brutes = {}
        self.donnees_propres = {}
        self.stats_etl = {}
        
    def charger_donnees_brutes(self):
        """Charge toutes les données brutes avec gestion d'erreurs"""
        logging.info("📥 CHARGEMENT DES DONNÉES BRUTES")
        
        fichiers = {
            'orders': 'Orders.xlsx',
            'order_details': 'Order Details.xlsx', 
            'products': 'Products.xlsx',
            'customers': 'Customers.xlsx',
            'employees': 'Employees.xlsx',
            'inventory': 'Inventory Transactions.xlsx',
            'inventory_types': 'Inventory Transaction Types.xlsx',
            'orders_status': 'Orders Status.xlsx',
            'order_details_status': 'Order Details Status.xlsx',
            'orders_tax_status': 'Orders Tax Status.xlsx',
            'privileges': 'Privileges.xlsx',
            'employee_privileges': 'Employee Privileges.xlsx'
        }
        
        for nom, fichier in fichiers.items():
            try:
                chemin = self.raw_path / fichier
                if chemin.exists():
                    self.donnees_brutes[nom] = pd.read_excel(chemin)
                    logging.info(f"✅ {fichier} chargé ({len(self.donnees_brutes[nom])} lignes)")
                else:
                    logging.warning(f"⚠️ Fichier non trouvé: {fichier}")
            except Exception as e:
                logging.error(f"❌ Erreur avec {fichier}: {e}")
                
        return self.donnees_brutes
    
    def nettoyer_orders(self):
        """Nettoie la table Orders de manière robuste"""
        logging.info("🧹 NETTOYAGE TABLE ORDERS")
        
        if 'orders' not in self.donnees_brutes:
            logging.error("❌ Table 'orders' non chargée")
            return None
            
        df = self.donnees_brutes['orders'].copy()
        
        # 1. Renommage des colonnes
        rename_map = {
            'Order ID': 'order_id',
            'Employee': 'employee_name', 
            'Customer': 'customer_company',
            'Order Date': 'order_date',
            'Shipped Date': 'shipped_date',
            'Ship Via': 'shipping_company',
            'Ship Name': 'ship_name',
            'Ship Address': 'ship_address',
            'Ship City': 'ship_city',
            'Ship State/Province': 'ship_state',
            'Ship ZIP/Postal Code': 'ship_zip',
            'Ship Country/Region': 'ship_country',
            'Shipping Fee': 'shipping_fee',
            'Taxes': 'taxes',
            'Payment Type': 'payment_type',
            'Paid Date': 'paid_date',
            'Notes': 'notes',
            'Tax Rate': 'tax_rate',
            'Tax Status': 'tax_status',
            'Status ID': 'status_id'
        }
        
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
        
        # 2. Conversion des dates avec gestion d'erreurs
        date_columns = ['order_date', 'shipped_date', 'paid_date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # 3. Nettoyage des valeurs numériques
        numeric_columns = ['shipping_fee', 'taxes', 'tax_rate']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # 4. Nettoyage des textes
        text_columns = ['employee_name', 'customer_company', 'payment_type']
        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
        
        # 5. Colonnes calculées
        df['delivery_days'] = (df['shipped_date'] - df['order_date']).dt.days
        df['order_year'] = df['order_date'].dt.year
        df['order_month'] = df['order_date'].dt.month
        df['order_quarter'] = df['order_date'].dt.quarter
        df['order_day_name'] = df['order_date'].dt.day_name()
        
        # 6. Gestion des statuts
        if 'status_id' in df.columns:
            status_map = {'New': 0, 'Invoiced': 1, 'Shipped': 2, 'Closed': 3}
            df['status_id'] = df['status_id'].map(status_map).fillna(0)
        
        self.donnees_propres['orders'] = df
        self.stats_etl['orders'] = {
            'lignes_originales': len(self.donnees_brutes['orders']),
            'lignes_nettoyees': len(df),
            'dates_manquantes': df['order_date'].isna().sum()
        }
        
        logging.info(f"✅ Orders nettoyée: {len(df)} lignes")
        return df
    
    def nettoyer_order_details(self):
        """Nettoie la table Order Details"""
        logging.info("🧹 NETTOYAGE TABLE ORDER DETAILS")
        
        if 'order_details' not in self.donnees_brutes:
            logging.error("❌ Table 'order_details' non chargée")
            return None
            
        df = self.donnees_brutes['order_details'].copy()
        
        # Renommage
        rename_map = {
            'ID': 'order_detail_id',
            'Order ID': 'order_id', 
            'Product': 'product_name',
            'Quantity': 'quantity',
            'Unit Price': 'unit_price',
            'Discount': 'discount',
            'Status ID': 'status_id',
            'Date Allocated': 'date_allocated',
            'Purchase Order ID': 'purchase_order_id',
            'Inventory ID': 'inventory_id'
        }
        
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
        
        # Nettoyage numérique
        numeric_cols = ['quantity', 'unit_price', 'discount']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Valeurs par défaut
        df['quantity'] = df['quantity'].fillna(0)
        df['unit_price'] = df['unit_price'].fillna(0)
        df['discount'] = df['discount'].fillna(0)
        
        # Calculs
        df['line_total'] = df['quantity'] * df['unit_price'] * (1 - df['discount'])
        df['line_total'] = df['line_total'].round(2)
        
        self.donnees_propres['order_details'] = df
        logging.info(f"✅ Order Details nettoyée: {len(df)} lignes")
        return df
    
    def nettoyer_products(self):
        """Nettoie la table Products"""
        logging.info("🧹 NETTOYAGE TABLE PRODUCTS")
        
        if 'products' not in self.donnees_brutes:
            logging.error("❌ Table 'products' non chargée")
            return None
            
        df = self.donnees_brutes['products'].copy()
        
        rename_map = {
            'ID': 'product_id',
            'Product Code': 'product_code',
            'Product Name': 'product_name', 
            'Description': 'description',
            'Standard Cost': 'standard_cost',
            'List Price': 'list_price',
            'Reorder Level': 'reorder_level',
            'Target Level': 'target_level',
            'Quantity Per Unit': 'quantity_per_unit',
            'Discontinued': 'discontinued',
            'Minimum Reorder Quantity': 'min_reorder_quantity',
            'Category': 'category'
        }
        
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
        
        # Nettoyage des prix
        price_cols = ['standard_cost', 'list_price']
        for col in price_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Colonnes calculées
        df['profit_margin'] = df['list_price'] - df['standard_cost']
        df['margin_percentage'] = (df['profit_margin'] / df['list_price'] * 100).round(2)
        
        # Gestion booléenne
        if 'discontinued' in df.columns:
            df['discontinued'] = df['discontinued'].astype(bool)
        
        self.donnees_propres['products'] = df
        logging.info(f"✅ Products nettoyée: {len(df)} produits")
        return df
    
    def nettoyer_customers(self):
        """Nettoie la table Customers"""
        logging.info("🧹 NETTOYAGE TABLE CUSTOMERS")
        
        if 'customers' not in self.donnees_brutes:
            logging.error("❌ Table 'customers' non chargée")
            return None
            
        df = self.donnees_brutes['customers'].copy()
        
        rename_map = {
            'ID': 'customer_id',
            'Company': 'company_name',
            'Last Name': 'last_name',
            'First Name': 'first_name',
            'E-mail Address': 'email',
            'Job Title': 'job_title', 
            'Business Phone': 'business_phone',
            'Address': 'address',
            'City': 'city',
            'State/Province': 'state',
            'ZIP/Postal Code': 'zip_code',
            'Country/Region': 'country'
        }
        
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
        
        # Création colonnes dérivées
        df['customer_name'] = df['first_name'] + ' ' + df['last_name']
        df['region'] = df['state'] + ', ' + df['country']
        
        self.donnees_propres['customers'] = df
        logging.info(f"✅ Customers nettoyée: {len(df)} clients")
        return df
    
    def nettoyer_employees(self):
        """Nettoie la table Employees"""
        logging.info("🧹 NETTOYAGE TABLE EMPLOYEES")
        
        if 'employees' not in self.donnees_brutes:
            logging.error("❌ Table 'employees' non chargée")
            return None
            
        df = self.donnees_brutes['employees'].copy()
        
        rename_map = {
            'ID': 'employee_id',
            'Last Name': 'last_name',
            'First Name': 'first_name',
            'E-mail Address': 'email',
            'Job Title': 'job_title',
            'Business Phone': 'business_phone',
            'Address': 'address', 
            'City': 'city',
            'State/Province': 'state',
            'ZIP/Postal Code': 'zip_code',
            'Country/Region': 'country',
            'Notes': 'notes'
        }
        
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
        
        # Colonnes dérivées
        df['employee_name'] = df['first_name'] + ' ' + df['last_name']
        df['full_address'] = df['address'] + ', ' + df['city'] + ', ' + df['state']
        
        # Extraction langues des notes
        if 'notes' in df.columns:
            df['languages'] = df['notes'].str.extract(r'(Fluent in [A-Za-z, ]+)')[0]
        
        self.donnees_propres['employees'] = df
        logging.info(f"✅ Employees nettoyée: {len(df)} employés")
        return df
    
    def creer_table_faits(self):
        """Crée la table de faits principale avec jointures"""
        logging.info("🔗 CRÉATION TABLE DE FAITS")
        
        try:
            # Jointure Orders + Order Details
            faits = self.donnees_propres['order_details'].merge(
                self.donnees_propres['orders'], on='order_id', how='left'
            )
            
            # Jointure Products
            faits = faits.merge(
                self.donnees_propres['products'][['product_name', 'category', 'standard_cost', 'profit_margin']],
                on='product_name', how='left'
            )
            
            # Jointure Customers
            faits = faits.merge(
                self.donnees_propres['customers'][['company_name', 'customer_name', 'city', 'state', 'country']],
                left_on='customer_company', 
                right_on='company_name', 
                how='left'
            )
            
            # Calculs finaux
            faits['profit'] = (faits['unit_price'] - faits['standard_cost']) * faits['quantity']
            faits['profit'] = faits['profit'].round(2)
            
            # Sélection colonnes finales
            colonnes_finales = [
                'order_id', 'order_date', 'order_year', 'order_month', 'order_quarter',
                'customer_company', 'customer_name', 'city', 'state', 'country',
                'employee_name', 'product_name', 'category',
                'quantity', 'unit_price', 'line_total', 'standard_cost', 'profit',
                'shipping_fee', 'payment_type', 'delivery_days', 'status_id'
            ]
            
            faits = faits[colonnes_finales]
            
            self.donnees_propres['sales_facts'] = faits
            logging.info(f"✅ Table de faits créée: {len(faits)} lignes")
            return faits
            
        except Exception as e:
            logging.error(f"❌ Erreur création table de faits: {e}")
            return None
    
    def analyser_qualite_donnees(self):
        """Analyse la qualité des données après nettoyage"""
        logging.info("🔍 ANALYSE QUALITÉ DONNÉES")
        
        rapport_qualite = []
        
        for nom, df in self.donnees_propres.items():
            stats = {
                'table': nom,
                'lignes': len(df),
                'colonnes': len(df.columns),
                'valeurs_manquantes': df.isnull().sum().sum(),
                'doublons': df.duplicated().sum()
            }
            
            # Analyse spécifique par table
            if 'order_date' in df.columns:
                stats['periode'] = f"{df['order_date'].min()} to {df['order_date'].max()}"
            
            rapport_qualite.append(stats)
            logging.info(f"📊 {nom}: {len(df)} lignes, {df.isnull().sum().sum()} valeurs manquantes")
        
        return rapport_qualite
    
    def sauvegarder_donnees_propres(self):
        """Sauvegarde toutes les données nettoyées"""
        logging.info("💾 SAUVEGARDE DONNÉES NETTOYÉES")
        
        self.processed_path.mkdir(parents=True, exist_ok=True)
        
        for nom, df in self.donnees_propres.items():
            try:
                # Sauvegarde en CSV
                chemin_csv = self.processed_path / f"{nom}_clean.csv"
                df.to_csv(chemin_csv, index=False, encoding='utf-8')
                
                # Sauvegarde en Excel pour analyse manuelle
                chemin_excel = self.processed_path / f"{nom}_clean.xlsx"
                df.to_excel(chemin_excel, index=False)
                
                logging.info(f"✅ {nom} sauvegardé ({len(df)} lignes)")
            except Exception as e:
                logging.error(f"❌ Erreur sauvegarde {nom}: {e}")
    
    def generer_rapport_etl(self):
        """Génère un rapport détaillé de l'ETL"""
        logging.info("📄 GÉNÉRATION RAPPORT ETL")
        
        rapport_content = [
            "RAPPORT ETL - NORTHWIND TRADERS",
            "=" * 50,
            f"Date de génération: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ]
        
        # Statistiques par table
        rapport_content.append("📊 STATISTIQUES PAR TABLE:")
        rapport_content.append("-" * 30)
        
        for nom, df in self.donnees_propres.items():
            rapport_content.append(f"\n{nom.upper()}:")
            rapport_content.append(f"  Lignes: {len(df)}")
            rapport_content.append(f"  Colonnes: {len(df.columns)}")
            rapport_content.append(f"  Valeurs manquantes: {df.isnull().sum().sum()}")
            rapport_content.append(f"  Doublons: {df.duplicated().sum()}")
        
        # Métriques business
        if 'sales_facts' in self.donnees_propres:
            faits = self.donnees_propres['sales_facts']
            ca_total = faits['line_total'].sum()
            profit_total = faits['profit'].sum()
            
            rapport_content.extend([
                "\n💰 MÉTRIQUES BUSINESS:",
                "-" * 30,
                f"Chiffre d'affaires total: {ca_total:,.2f} $",
                f"Profit total: {profit_total:,.2f} $", 
                f"Marge moyenne: {(profit_total/ca_total*100):.1f}%",
                f"Commandes totales: {faits['order_id'].nunique()}",
                f"Clients uniques: {faits['customer_company'].nunique()}",
                f"Produits uniques: {faits['product_name'].nunique()}"
            ])
        
        # Sauvegarde du rapport
        rapport_path = Path('../reports/rapport_etl_complet.txt')
        with open(rapport_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(rapport_content))
        
        logging.info(f"✅ Rapport ETL sauvegardé: {rapport_path}")
    
    def executer_etl_complet(self):
        """Exécute le processus ETL complet"""
        logging.info("🚀 DÉMARRAGE ETL COMPLET")
        logging.info("=" * 60)
        
        try:
            # 1. Chargement
            self.charger_donnees_brutes()
            
            # 2. Nettoyage
            self.nettoyer_orders()
            self.nettoyer_order_details() 
            self.nettoyer_products()
            self.nettoyer_customers()
            self.nettoyer_employees()
            
            # 3. Table de faits
            self.creer_table_faits()
            
            # 4. Analyse qualité
            self.analyser_qualite_donnees()
            
            # 5. Sauvegarde
            self.sauvegarder_donnees_propres()
            
            # 6. Rapport
            self.generer_rapport_etl()
            
            logging.info("🎉 ETL TERMINÉ AVEC SUCCÈS!")
            return self.donnees_propres
            
        except Exception as e:
            logging.error(f"💥 ECHEC ETL: {e}")
            return None

if __name__ == "__main__":
    etl = ETLNorthwind()
    donnees_propres = etl.executer_etl_complet()