# scripts/03_analysis.py
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from datetime import datetime, timedelta
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AnalyseNorthwind:
    def __init__(self):
        self.data_path = Path('../data/processed')
        self.figures_path = Path('../figures')
        self.donnees = {}
        self.kpis = {}
        self.rapport_analyse = []
        
    def charger_donnees_propres(self):
        """Charge les données nettoyées depuis le dossier processed"""
        logging.info("📥 CHARGEMENT DES DONNÉES NETTOYÉES")
        
        fichiers = {
            'sales_facts': 'sales_facts_clean.csv',
            'products': 'products_clean.csv', 
            'customers': 'customers_clean.csv',
            'employees': 'employees_clean.csv',
            'orders': 'orders_clean.csv',
            'order_details': 'order_details_clean.csv',
            'inventory': 'inventory_clean.csv'
        }
        
        for nom, fichier in fichiers.items():
            try:
                chemin = self.data_path / fichier
                if chemin.exists():
                    # Chargement avec parsing des dates pour sales_facts
                    if nom == 'sales_facts':
                        self.donnees[nom] = pd.read_csv(chemin, parse_dates=['order_date'])
                    else:
                        self.donnees[nom] = pd.read_csv(chemin)
                    
                    logging.info(f"✅ {fichier} chargé ({len(self.donnees[nom])} lignes)")
                else:
                    logging.warning(f"⚠️ Fichier non trouvé: {fichier}")
            except Exception as e:
                logging.error(f"❌ Erreur avec {fichier}: {e}")
                
        return self.donnees
    
    def calculer_kpi_fondamentaux(self):
        """Calcule les KPI business fondamentaux"""
        logging.info("💰 CALCUL DES KPI FONDAMENTAUX")
        
        if 'sales_facts' not in self.donnees:
            logging.error("❌ Table 'sales_facts' manquante pour l'analyse")
            return
        
        df = self.donnees['sales_facts']
        
        # KPI VENTES
        self.kpis['chiffre_affaires_total'] = df['line_total'].sum()
        self.kpis['profit_total'] = df['profit'].sum()
        self.kpis['marge_moyenne'] = (self.kpis['profit_total'] / self.kpis['chiffre_affaires_total'] * 100) if self.kpis['chiffre_affaires_total'] > 0 else 0
        
        # KPI VOLUMES
        self.kpis['nombre_commandes'] = df['order_id'].nunique()
        self.kpis['nombre_clients'] = df['customer_company'].nunique()
        self.kpis['nombre_produits_vendus'] = df['product_name'].nunique()
        self.kpis['quantite_totale_vendue'] = df['quantity'].sum()
        
        # KPI MOYENS
        self.kpis['panier_moyen'] = self.kpis['chiffre_affaires_total'] / self.kpis['nombre_commandes']
        self.kpis['profit_par_commande'] = self.kpis['profit_total'] / self.kpis['nombre_commandes']
        self.kpis['quantite_moyenne_par_commande'] = self.kpis['quantite_totale_vendue'] / self.kpis['nombre_commandes']
        
        # Ajout au rapport
        self.rapport_analyse.extend([
            "💰 KPI FONDAMENTAUX",
            "-" * 40,
            f"Chiffre d'affaires total: {self.kpis['chiffre_affaires_total']:,.2f} $",
            f"Profit total: {self.kpis['profit_total']:,.2f} $",
            f"Marge moyenne: {self.kpis['marge_moyenne']:.1f} %",
            f"Nombre de commandes: {self.kpis['nombre_commandes']}",
            f"Nombre de clients: {self.kpis['nombre_clients']}",
            f"Panier moyen: {self.kpis['panier_moyen']:.2f} $",
            ""
        ])
        
        logging.info(f"✅ KPI fondamentaux calculés")
    
    def analyser_tendances_temporelles(self):
        """Analyse l'évolution dans le temps"""
        logging.info("📅 ANALYSE DES TENDANCES TEMPORELLES")
        
        if 'sales_facts' not in self.donnees:
            return
        
        df = self.donnees['sales_facts']
        
        # Ventes par mois
        df['mois_annee'] = df['order_date'].dt.to_period('M')
        ventes_par_mois = df.groupby('mois_annee').agg({
            'line_total': 'sum',
            'profit': 'sum',
            'order_id': 'nunique',
            'quantity': 'sum'
        }).reset_index()
        
        ventes_par_mois['mois_annee'] = ventes_par_mois['mois_annee'].astype(str)
        self.kpis['ventes_par_mois'] = ventes_par_mois
        
        # Croissance mois par mois
        if len(ventes_par_mois) > 1:
            ventes_par_mois['croissance_ca'] = ventes_par_mois['line_total'].pct_change() * 100
            self.kpis['croissance_mensuelle'] = ventes_par_mois[['mois_annee', 'croissance_ca']].dropna()
        
        # Ventes par jour de la semaine
        df['jour_semaine'] = df['order_date'].dt.day_name()
        ventes_par_jour = df.groupby('jour_semaine').agg({
            'line_total': 'sum',
            'order_id': 'nunique'
        }).reset_index()
        
        # Réordonner les jours
        jours_ordre = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        ventes_par_jour['jour_semaine'] = pd.Categorical(ventes_par_jour['jour_semaine'], categories=jours_ordre, ordered=True)
        ventes_par_jour = ventes_par_jour.sort_values('jour_semaine')
        
        self.kpis['ventes_par_jour'] = ventes_par_jour
        
        logging.info(f"✅ Tendances temporelles analysées")
    
    def analyser_performance_produits(self):
        """Analyse détaillée des performances produits"""
        logging.info("📦 ANALYSE PERFORMANCE PRODUITS")
        
        if 'sales_facts' not in self.donnees:
            return
        
        df = self.donnees['sales_facts']
        
        # Top 10 produits par chiffre d'affaires
        top_produits_ca = df.groupby('product_name').agg({
            'line_total': 'sum',
            'quantity': 'sum',
            'profit': 'sum',
            'order_id': 'nunique'
        }).round(2)
        
        top_produits_ca = top_produits_ca.sort_values('line_total', ascending=False)
        top_produits_ca['marge'] = (top_produits_ca['profit'] / top_produits_ca['line_total'] * 100).round(1)
        self.kpis['top_produits_ca'] = top_produits_ca.head(15)
        
        # Top 10 produits par quantité
        top_produits_qte = df.groupby('product_name')['quantity'].sum().sort_values(ascending=False)
        self.kpis['top_produits_quantite'] = top_produits_qte.head(15)
        
        # Top 10 produits par profit
        top_produits_profit = df.groupby('product_name')['profit'].sum().sort_values(ascending=False)
        self.kpis['top_produits_profit'] = top_produits_profit.head(15)
        
        # Performance par catégorie
        if 'category' in df.columns:
            performance_categories = df.groupby('category').agg({
                'line_total': 'sum',
                'profit': 'sum',
                'quantity': 'sum',
                'order_id': 'nunique'
            }).round(2)
            
            performance_categories['marge'] = (performance_categories['profit'] / performance_categories['line_total'] * 100).round(1)
            performance_categories = performance_categories.sort_values('line_total', ascending=False)
            self.kpis['performance_categories'] = performance_categories
        
        # Ajout au rapport
        self.rapport_analyse.extend([
            "📦 PERFORMANCE PRODUITS",
            "-" * 40,
            f"Produits les plus rentables:",
        ])
        
        for i, (produit, row) in enumerate(self.kpis['top_produits_profit'].head(5).items()):
            self.rapport_analyse.append(f"  {i+1}. {produit}: {row:,.2f} $")
        
        self.rapport_analyse.append("")
        logging.info(f"✅ Performance produits analysée")
    
    def analyser_comportement_clients(self):
        """Analyse du comportement et de la valeur client"""
        logging.info("👥 ANALYSE COMPORTEMENT CLIENTS")
        
        if 'sales_facts' not in self.donnees:
            return
        
        df = self.donnees['sales_facts']
        
        # Top clients par chiffre d'affaires
        top_clients = df.groupby('customer_company').agg({
            'line_total': 'sum',
            'profit': 'sum',
            'order_id': 'nunique',
            'order_date': ['min', 'max']
        }).round(2)
        
        # Aplatir les colonnes multi-niveaux
        top_clients.columns = ['ca_total', 'profit_total', 'nb_commandes', 'premiere_commande', 'derniere_commande']
        top_clients = top_clients.sort_values('ca_total', ascending=False)
        
        # Calculer la valeur client lifetime
        top_clients['valeur_moyenne_commande'] = top_clients['ca_total'] / top_clients['nb_commandes']
        top_clients['marge_client'] = (top_clients['profit_total'] / top_clients['ca_total'] * 100).round(1)
        
        self.kpis['top_clients'] = top_clients.head(20)
        
        # Segmentation clients par valeur
        segments = {
            'VIP': top_clients[top_clients['ca_total'] > top_clients['ca_total'].quantile(0.8)],
            'Fidèles': top_clients[(top_clients['ca_total'] > top_clients['ca_total'].quantile(0.5)) & 
                                 (top_clients['ca_total'] <= top_clients['ca_total'].quantile(0.8))],
            'Occasionnels': top_clients[top_clients['ca_total'] <= top_clients['ca_total'].quantile(0.5)]
        }
        
        self.kpis['segmentation_clients'] = segments
        
        # Performance géographique
        if 'country' in df.columns:
            performance_pays = df.groupby('country').agg({
                'line_total': 'sum',
                'profit': 'sum',
                'customer_company': 'nunique'
            }).round(2).sort_values('line_total', ascending=False)
            
            self.kpis['performance_geographique'] = performance_pays
        
        logging.info(f"✅ Comportement clients analysé")
    
    def analyser_performance_commerciale(self):
        """Analyse de la performance des commerciaux"""
        logging.info("👨‍💼 ANALYSE PERFORMANCE COMMERCIALE")
        
        if 'sales_facts' not in self.donnees:
            return
        
        df = self.donnees['sales_facts']
        
        # Performance par employé
        performance_employes = df.groupby('employee_name').agg({
            'line_total': 'sum',
            'profit': 'sum',
            'order_id': 'nunique',
            'customer_company': 'nunique'
        }).round(2)
        
        performance_employes = performance_employes.rename(columns={
            'order_id': 'nb_commandes',
            'customer_company': 'nb_clients'
        })
        
        performance_employes = performance_employes.sort_values('line_total', ascending=False)
        performance_employes['ca_moyen_par_commande'] = performance_employes['line_total'] / performance_employes['nb_commandes']
        performance_employes['marge'] = (performance_employes['profit'] / performance_employes['line_total'] * 100).round(1)
        
        self.kpis['performance_employes'] = performance_employes
        
        # Ajout au rapport
        self.rapport_analyse.extend([
            "👨‍💼 PERFORMANCE COMMERCIALE",
            "-" * 40,
            f"Top commerciaux par CA:",
        ])
        
        for i, (employe, row) in enumerate(self.kpis['performance_employes'].head(3).iterrows()):
            self.rapport_analyse.append(f"  {i+1}. {employe}: {row['line_total']:,.2f} $ ({row['nb_commandes']} commandes)")
        
        self.rapport_analyse.append("")
        logging.info(f"✅ Performance commerciale analysée")
    
    def analyser_efficacite_operationnelle(self):
        """Analyse de l'efficacité opérationnelle"""
        logging.info("⚙️ ANALYSE EFFICACITÉ OPÉRATIONNELLE")
        
        if 'orders' not in self.donnees:
            return
        
        df = self.donnees['orders']
        
        # Délais de livraison
        if 'delivery_days' in df.columns:
            delais = df[df['delivery_days'].notna()]
            self.kpis['delai_livraison_moyen'] = delais['delivery_days'].mean()
            self.kpis['delai_livraison_median'] = delais['delivery_days'].median()
            
            # Taux de livraison rapide (moins de 7 jours)
            livraisons_rapides = delais[delais['delivery_days'] <= 7]
            self.kpis['taux_livraison_rapide'] = len(livraisons_rapides) / len(delais) * 100
        
        # Performance des transporteurs
        if 'shipping_company' in df.columns:
            performance_transporteurs = df.groupby('shipping_company').agg({
                'delivery_days': 'mean',
                'order_id': 'nunique',
                'shipping_fee': 'mean'
            }).round(2)
            
            performance_transporteurs = performance_transporteurs.rename(columns={
                'order_id': 'nb_commandes',
                'delivery_days': 'delai_moyen'
            })
            
            self.kpis['performance_transporteurs'] = performance_transporteurs
        
        # Méthodes de paiement
        if 'payment_type' in df.columns:
            methodes_paiement = df['payment_type'].value_counts()
            self.kpis['methodes_paiement'] = methodes_paiement
        
        logging.info(f"✅ Efficacité opérationnelle analysée")
    
    def analyser_gestion_stock(self):
        """Analyse de la gestion des stocks et inventaire"""
        logging.info("📊 ANALYSE GESTION STOCK")
        
        if 'inventory' in self.donnees and 'products' in self.donnees:
            inventory_df = self.donnees['inventory']
            products_df = self.donnees['products']
            
            # Mouvements de stock par produit
            mouvements_stock = inventory_df.groupby('product_name').agg({
                'quantity': 'sum',
                'transaction_type': 'count'
            }).rename(columns={'transaction_type': 'nb_mouvements'})
            
            # Jointure avec les informations produits
            stock_analyse = mouvements_stock.merge(
                products_df[['product_name', 'category', 'reorder_level', 'target_level']],
                on='product_name', how='left'
            )
            
            # Identifier les problèmes de stock
            stock_analyse['niveau_stock_actuel'] = stock_analyse['quantity']  # Simplification
            stock_analyse['besoin_reappro'] = stock_analyse['reorder_level'] - stock_analyse['niveau_stock_actuel']
            stock_analyse['statut_stock'] = np.where(
                stock_analyse['niveau_stock_actuel'] <= stock_analyse['reorder_level'],
                'Stock Bas',
                np.where(stock_analyse['niveau_stock_actuel'] >= stock_analyse['target_level'],
                        'Stock Élevé', 'Stock Normal')
            )
            
            self.kpis['analyse_stock'] = stock_analyse
            
            logging.info(f"✅ Gestion stock analysée")
    
    def calculer_metrics_avancees(self):
        """Calcule des métriques avancées et ratios"""
        logging.info("🎯 CALCUL MÉTRIQUES AVANCÉES")
        
        # Taux de croissance (simplifié)
        if 'ventes_par_mois' in self.kpis:
            ventes_mois = self.kpis['ventes_par_mois']
            if len(ventes_mois) > 1:
                dernier_mois = ventes_mois.iloc[-1]['line_total']
                mois_precedent = ventes_mois.iloc[-2]['line_total']
                self.kpis['taux_croissance_mensuel'] = ((dernier_mois - mois_precedent) / mois_precedent * 100) if mois_precedent > 0 else 0
        
        # Customer Lifetime Value approximatif
        if 'top_clients' in self.kpis:
            clv_moyen = self.kpis['top_clients']['ca_total'].mean()
            self.kpis['clv_moyen'] = clv_moyen
        
        # Taux de rétention (simplifié)
        if 'sales_facts' in self.donnees:
            df = self.donnees['sales_facts']
            clients_par_mois = df.groupby([df['order_date'].dt.to_period('M'), 'customer_company']).size().reset_index()
            clients_uniques_par_mois = clients_par_mois.groupby('order_date')['customer_company'].nunique()
            if len(clients_uniques_par_mois) > 1:
                self.kpis['taux_retention_approx'] = (clients_uniques_par_mois.iloc[-1] / clients_uniques_par_mois.iloc[-2] * 100) if clients_uniques_par_mois.iloc[-2] > 0 else 100
        
        logging.info(f"✅ Métriques avancées calculées")
    
    def generer_rapport_analyse_complet(self):
        """Génère un rapport d'analyse détaillé"""
        logging.info("📄 GÉNÉRATION RAPPORT D'ANALYSE")
        
        rapport_content = [
            "RAPPORT D'ANALYSE COMPLET - NORTHWIND TRADERS",
            "=" * 60,
            f"Date de génération: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Période analysée: Données complètes",
            ""
        ]
        
        # Ajouter toutes les sections d'analyse
        rapport_content.extend(self.rapport_analyse)
        
        # Ajouter les insights clés
        rapport_content.extend([
            "\n💡 INSIGHTS CLÉS",
            "=" * 40,
            f"• Chiffre d'affaires total: {self.kpis.get('chiffre_affaires_total', 0):,.2f} $",
            f"• Marge moyenne: {self.kpis.get('marge_moyenne', 0):.1f}%",
            f"• {self.kpis.get('nombre_clients', 0)} clients actifs",
            f"• Panier moyen: {self.kpis.get('panier_moyen', 0):.2f} $",
            f"• Délai livraison moyen: {self.kpis.get('delai_livraison_moyen', 0):.1f} jours",
        ])
        
        # Recommandations
        rapport_content.extend([
            "\n🎯 RECOMMANDATIONS STRATÉGIQUES",
            "=" * 40,
            "1. Focus sur les produits à haute marge",
            "2. Développer la fidélisation des top clients", 
            "3. Optimiser les délais de livraison",
            "4. Améliorer la performance des commerciaux moins performants",
            "5. Surveiller les niveaux de stock critiques"
        ])
        
        # Sauvegarde du rapport
        rapport_path = Path('../reports/rapport_analyse_complet.txt')
        with open(rapport_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(rapport_content))
        
        # Sauvegarde en JSON pour le dashboard
        kpis_json = {
            'kpis_fondamentaux': {
                'chiffre_affaires_total': self.kpis.get('chiffre_affaires_total', 0),
                'profit_total': self.kpis.get('profit_total', 0),
                'marge_moyenne': self.kpis.get('marge_moyenne', 0),
                'nombre_commandes': self.kpis.get('nombre_commandes', 0),
                'nombre_clients': self.kpis.get('nombre_clients', 0),
                'panier_moyen': self.kpis.get('panier_moyen', 0)
            },
            'metrics_operationnelles': {
                'delai_livraison_moyen': self.kpis.get('delai_livraison_moyen', 0),
                'taux_livraison_rapide': self.kpis.get('taux_livraison_rapide', 0)
            }
        }
        
        with open('../data/analysis/kpis_principaux.json', 'w') as f:
            json.dump(kpis_json, f, indent=2)
        
        logging.info(f"✅ Rapport d'analyse sauvegardé: {rapport_path}")
    
    def sauvegarder_donnees_analyse(self):
        """Sauvegarde toutes les données d'analyse pour la visualisation"""
        logging.info("💾 SAUVEGARDE DONNÉES POUR VISUALISATION")
        
        analysis_path = Path('../data/analysis')
        analysis_path.mkdir(exist_ok=True)
        
        # Sauvegarder les KPI principaux
        for nom, data in self.kpis.items():
            if isinstance(data, pd.DataFrame):
                # Sauvegarder les DataFrames
                data.to_csv(analysis_path / f'{nom}.csv', index=True)
            elif isinstance(data, dict):
                # Sauvegarder les dictionnaires de DataFrames (segmentation clients)
                for segment_name, segment_data in data.items():
                    if isinstance(segment_data, pd.DataFrame):
                        segment_data.to_csv(analysis_path / f'{nom}_{segment_name}.csv', index=True)
        
        # Sauvegarder un résumé des KPI numériques
        kpis_numeriques = {}
        for nom, valeur in self.kpis.items():
            if isinstance(valeur, (int, float, np.number)):
                kpis_numeriques[nom] = valeur
        
        pd.Series(kpis_numeriques).to_csv(analysis_path / 'kpis_numeriques.csv')
        
        logging.info("✅ Données d'analyse sauvegardées")
    
    def executer_analyse_complete(self):
        """Exécute l'analyse complète"""
        logging.info("🚀 DÉMARRAGE ANALYSE COMPLÈTE")
        logging.info("=" * 60)
        
        try:
            # 1. Chargement
            self.charger_donnees_propres()
            
            # 2. Analyses
            self.calculer_kpi_fondamentaux()
            self.analyser_tendances_temporelles()
            self.analyser_performance_produits()
            self.analyser_comportement_clients()
            self.analyser_performance_commerciale()
            self.analyser_efficacite_operationnelle()
            self.analyser_gestion_stock()
            self.calculer_metrics_avancees()
            
            # 3. Rapports et sauvegarde
            self.generer_rapport_analyse_complet()
            self.sauvegarder_donnees_analyse()
            
            logging.info("🎉 ANALYSE TERMINÉE AVEC SUCCÈS!")
            return self.kpis
            
        except Exception as e:
            logging.error(f"💥 ÉCHEC ANALYSE: {e}")
            return None

if __name__ == "__main__":
    analyse = AnalyseNorthwind()
    kpis = analyse.executer_analyse_complete()