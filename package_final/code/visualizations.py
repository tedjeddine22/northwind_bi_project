# scripts/visualizations.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration du style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class VisualisationsNorthwind:
    def __init__(self):
        self.data_path = Path('../data/processed')
        self.figures_path = Path('../figures')
        self.donnees = {}
        
    def charger_donnees(self):
        """Charge les données pour la visualisation"""
        print("📥 CHARGEMENT DES DONNÉES POUR VISUALISATION")
        
        try:
            # Charger la table de faits
            chemin_faits = self.data_path / 'sales_facts_clean.csv'
            if chemin_faits.exists():
                self.donnees['sales_facts'] = pd.read_csv(chemin_faits, parse_dates=['order_date'])
                print(f"✅ Données de vente chargées: {len(self.donnees['sales_facts'])} lignes")
            else:
                print("❌ Fichier sales_facts_clean.csv non trouvé")
                return False
                
            # Charger les produits
            chemin_produits = self.data_path / 'products_clean.csv'
            if chemin_produits.exists():
                self.donnees['products'] = pd.read_csv(chemin_produits)
                print(f"✅ Données produits chargées: {len(self.donnees['products'])} produits")
                
            return True
            
        except Exception as e:
            print(f"❌ Erreur chargement: {e}")
            return False
    
    def creer_dossier_figures(self):
        """Crée la structure des dossiers pour les figures"""
        dossiers = ['ventes', 'produits', 'clients', 'employes', 'interactifs']
        
        for dossier in dossiers:
            chemin = self.figures_path / dossier
            chemin.mkdir(parents=True, exist_ok=True)
        
        print("✅ Dossiers de figures créés")
    
    def visualiser_kpi_principaux(self):
        """Crée les visualisations pour les KPI principaux"""
        print("📊 CRÉATION VISUALISATIONS KPI PRINCIPAUX")
        
        if 'sales_facts' not in self.donnees:
            return False
            
        df = self.donnees['sales_facts']
        
        # 1. Évolution du chiffre d'affaires dans le temps
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('DASHBOARD NORTHWIND - KPI PRINCIPAUX', fontsize=16, fontweight='bold')
        
        # Graphique 1: Évolution mensuelle du CA
        df['mois'] = df['order_date'].dt.to_period('M').astype(str)
        ca_mensuel = df.groupby('mois')['Line Total'].sum()
        
        axes[0, 0].plot(ca_mensuel.index, ca_mensuel.values, marker='o', linewidth=2, color='#2E86AB')
        axes[0, 0].set_title('Évolution du Chiffre d\'Affaires Mensuel', fontweight='bold')
        axes[0, 0].set_ylabel('Chiffre d\'Affaires ($)')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # Graphique 2: Répartition par catégorie de produits
        if 'Category' in df.columns:
            ca_par_categorie = df.groupby('Category')['Line Total'].sum().sort_values(ascending=False)
            axes[0, 1].bar(ca_par_categorie.index, ca_par_categorie.values, color='#A23B72')
            axes[0, 1].set_title('Chiffre d\'Affaires par Catégorie', fontweight='bold')
            axes[0, 1].set_ylabel('Chiffre d\'Affaires ($)')
            axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Graphique 3: Top 10 produits
        top_produits = df.groupby('product_name')['Line Total'].sum().sort_values(ascending=False).head(10)
        axes[1, 0].barh(range(len(top_produits)), top_produits.values, color='#F18F01')
        axes[1, 0].set_yticks(range(len(top_produits)))
        axes[1, 0].set_yticklabels(top_produits.index, fontsize=9)
        axes[1, 0].set_title('Top 10 Produits par Chiffre d\'Affaires', fontweight='bold')
        axes[1, 0].set_xlabel('Chiffre d\'Affaires ($)')
        
        # Graphique 4: Performance des employés
        perf_employes = df.groupby('employee_name')['Line Total'].sum().sort_values(ascending=False)
        axes[1, 1].bar(perf_employes.index, perf_employes.values, color='#C73E1D')
        axes[1, 1].set_title('Performance des Employés', fontweight='bold')
        axes[1, 1].set_ylabel('Chiffre d\'Affaires ($)')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(self.figures_path / 'ventes/kpi_principaux.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Graphiques KPI principaux sauvegardés")
        return True
    
    def visualiser_analyse_produits(self):
        """Visualisations détaillées pour l'analyse produits"""
        print("📦 CRÉATION VISUALISATIONS PRODUITS")
        
        if 'sales_facts' not in self.donnees:
            return False
            
        df = self.donnees['sales_facts']
        
        # 1. Analyse de la marge par produit
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Graphique marges
        if 'Standard Cost' in df.columns and 'Unit Price' in df.columns:
            df_produits = df.groupby('product_name').agg({
                'Line Total': 'sum',
                'Quantity': 'sum',
                'Unit Price': 'mean',
                'Standard Cost': 'mean'
            }).round(2)
            
            df_produits['Marge'] = df_produits['Unit Price'] - df_produits['Standard Cost']
            df_produits['Marge %'] = (df_produits['Marge'] / df_produits['Unit Price'] * 100).round(1)
            
            # Top produits par marge
            top_marges = df_produits.nlargest(10, 'Marge %')
            
            axes[0].barh(range(len(top_marges)), top_marges['Marge %'], color='#2A9D8F')
            axes[0].set_yticks(range(len(top_marges)))
            axes[0].set_yticklabels(top_marges.index, fontsize=9)
            axes[0].set_title('Top 10 Produits par Marge (%)', fontweight='bold')
            axes[0].set_xlabel('Marge (%)')
        
        # 2. Quantités vendues par catégorie
        if 'Category' in df.columns:
            qte_par_categorie = df.groupby('Category')['Quantity'].sum().sort_values(ascending=False)
            axes[1].pie(qte_par_categorie.values, labels=qte_par_categorie.index, autopct='%1.1f%%')
            axes[1].set_title('Répartition des Ventes par Catégorie', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.figures_path / 'produits/analyse_produits.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Graphiques produits sauvegardés")
        return True
    
    def visualiser_analyse_clients(self):
        """Visualisations pour l'analyse clients"""
        print("👥 CRÉATION VISUALISATIONS CLIENTS")
        
        if 'sales_facts' not in self.donnees:
            return False
            
        df = self.donnees['sales_facts']
        
        # Analyse des clients
        analyse_clients = df.groupby('customer_company').agg({
            'Line Total': 'sum',
            'order_id': 'nunique',
            'Quantity': 'sum'
        }).round(2)
        
        analyse_clients = analyse_clients.rename(columns={
            'order_id': 'nb_commandes',
            'Line Total': 'ca_total'
        })
        
        analyse_clients = analyse_clients.sort_values('ca_total', ascending=False)
        
        # Graphique clients
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Top 10 clients par CA
        top_clients = analyse_clients.head(10)
        axes[0].barh(range(len(top_clients)), top_clients['ca_total'], color='#E9C46A')
        axes[0].set_yticks(range(len(top_clients)))
        axes[0].set_yticklabels(top_clients.index, fontsize=9)
        axes[0].set_title('Top 10 Clients par Chiffre d\'Affaires', fontweight='bold')
        axes[0].set_xlabel('Chiffre d\'Affaires ($)')
        
        # Distribution de la valeur client
        axes[1].hist(analyse_clients['ca_total'], bins=20, color='#F4A261', edgecolor='black')
        axes[1].set_title('Distribution de la Valeur Client', fontweight='bold')
        axes[1].set_xlabel('Chiffre d\'Affaires par Client ($)')
        axes[1].set_ylabel('Nombre de Clients')
        
        plt.tight_layout()
        plt.savefig(self.figures_path / 'clients/analyse_clients.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Graphiques clients sauvegardés")
        return True
    
    def visualiser_tendances_temporelles(self):
        """Visualisations des tendances temporelles"""
        print("📅 CRÉATION VISUALISATIONS TENDANCES")
        
        if 'sales_facts' not in self.donnees:
            return False
            
        df = self.donnees['sales_facts']
        
        # Préparation des données temporelles
        df['mois_annee'] = df['order_date'].dt.to_period('M').astype(str)
        df['semaine'] = df['order_date'].dt.isocalendar().week
        df['jour_semaine'] = df['order_date'].dt.day_name()
        
        # Agrégations temporelles
        tendances_mensuelles = df.groupby('mois_annee').agg({
            'Line Total': 'sum',
            'order_id': 'nunique',
            'Quantity': 'sum'
        }).reset_index()
        
        # Graphique tendances
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Tendance CA mensuel
        axes[0, 0].plot(tendances_mensuelles['mois_annee'], tendances_mensuelles['Line Total'], 
                       marker='o', linewidth=2, color='#264653')
        axes[0, 0].set_title('Tendance du Chiffre d\'Affaires Mensuel', fontweight='bold')
        axes[0, 0].set_ylabel('CA ($)')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # Tendance nombre de commandes
        axes[0, 1].plot(tendances_mensuelles['mois_annee'], tendances_mensuelles['order_id'], 
                       marker='s', linewidth=2, color='#2A9D8F')
        axes[0, 1].set_title('Tendance du Nombre de Commandes', fontweight='bold')
        axes[0, 1].set_ylabel('Nombre de Commandes')
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(True, alpha=0.3)
        
        # Ventes par jour de la semaine
        ventes_par_jour = df.groupby('jour_semaine')['Line Total'].sum()
        jours_ordre = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        ventes_par_jour = ventes_par_jour.reindex(jours_ordre)
        
        axes[1, 0].bar(ventes_par_jour.index, ventes_par_jour.values, color='#E9C46A')
        axes[1, 0].set_title('Ventes par Jour de la Semaine', fontweight='bold')
        axes[1, 0].set_ylabel('CA ($)')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Heatmap des ventes (exemple simplifié)
        if 'Category' in df.columns:
            ventes_categorie_mois = df.pivot_table(
                values='Line Total', 
                index='Category', 
                columns='mois_annee', 
                aggfunc='sum'
            ).fillna(0)
            
            sns.heatmap(ventes_categorie_mois, ax=axes[1, 1], cmap='YlOrRd', cbar_kws={'label': 'CA ($)'})
            axes[1, 1].set_title('Heatmap: CA par Catégorie et Mois', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(self.figures_path / 'ventes/tendances_temporelles.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Graphiques tendances sauvegardés")
        return True
    
    def creer_visualisations_interactives(self):
        """Crée des visualisations interactives avec Plotly"""
        print("🎨 CRÉATION VISUALISATIONS INTERACTIVES")
        
        if 'sales_facts' not in self.donnees:
            return False
            
        df = self.donnees['sales_facts']
        
        # 1. Graphique interactif: Évolution du CA
        df['mois'] = df['order_date'].dt.to_period('M').astype(str)
        ca_mensuel = df.groupby('mois')['Line Total'].sum().reset_index()
        
        fig1 = px.line(ca_mensuel, x='mois', y='Line Total', 
                      title='Évolution du Chiffre d\'Affaires Mensuel',
                      labels={'Line Total': 'Chiffre d\'Affaires ($)', 'mois': 'Mois'})
        fig1.update_traces(line=dict(width=3), marker=dict(size=8))
        fig1.write_html(str(self.figures_path / 'interactifs/evolution_ca.html'))
        
        # 2. Graphique interactif: Top produits
        top_produits = df.groupby('product_name')['Line Total'].sum().sort_values(ascending=False).head(15).reset_index()
        
        fig2 = px.bar(top_produits, x='Line Total', y='product_name', orientation='h',
                     title='Top 15 Produits par Chiffre d\'Affaires',
                     labels={'Line Total': 'Chiffre d\'Affaires ($)', 'product_name': 'Produit'})
        fig2.update_layout(yaxis={'categoryorder': 'total ascending'})
        fig2.write_html(str(self.figures_path / 'interactifs/top_produits.html'))
        
        # 3. Graphique interactif: Répartition par catégorie
        if 'Category' in df.columns:
            ca_categories = df.groupby('Category')['Line Total'].sum().reset_index()
            
            fig3 = px.pie(ca_categories, values='Line Total', names='Category',
                         title='Répartition du CA par Catégorie')
            fig3.write_html(str(self.figures_path / 'interactifs/repartition_categories.html'))
        
        # 4. Dashboard interactif combiné
        fig4 = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Évolution CA Mensuel', 'Top Produits', 'Répartition Catégories', 'Performance Employés'),
            specs=[[{"type": "scatter"}, {"type": "bar"}],
                   [{"type": "pie"}, {"type": "bar"}]]
        )
        
        # Graphique 1: Évolution CA
        fig4.add_trace(go.Scatter(x=ca_mensuel['mois'], y=ca_mensuel['Line Total'],
                                 mode='lines+markers', name='CA Mensuel'),
                      row=1, col=1)
        
        # Graphique 2: Top produits
        fig4.add_trace(go.Bar(x=top_produits['Line Total'], y=top_produits['product_name'],
                             orientation='h', name='Top Produits'),
                      row=1, col=2)
        
        # Graphique 3: Répartition catégories
        if 'Category' in df.columns:
            fig4.add_trace(go.Pie(labels=ca_categories['Category'], values=ca_categories['Line Total'],
                                 name='Catégories'),
                          row=2, col=1)
        
        # Graphique 4: Performance employés
        perf_employes = df.groupby('employee_name')['Line Total'].sum().sort_values(ascending=False).head(10).reset_index()
        fig4.add_trace(go.Bar(x=perf_employes['employee_name'], y=perf_employes['Line Total'],
                             name='Performance Employés'),
                      row=2, col=2)
        
        fig4.update_layout(height=800, title_text="DASHBOARD NORTHWIND INTERACTIF", showlegend=False)
        fig4.write_html(str(self.figures_path / 'interactifs/dashboard_complet.html'))
        
        print("✅ Visualisations interactives sauvegardées")
        return True
    
    def generer_rapport_visualisation(self):
        """Génère un rapport des visualisations créées"""
        print("📄 GÉNÉRATION RAPPORT VISUALISATIONS")
        
        rapport = [
            "RAPPORT DES VISUALISATIONS NORTHWIND TRADERS",
            "=" * 50,
            f"Date de génération: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "📊 VISUALISATIONS CRÉÉES:",
            "",
            "📈 Graphiques Statiques (PNG):",
            "- figures/ventes/kpi_principaux.png",
            "- figures/produits/analyse_produits.png", 
            "- figures/clients/analyse_clients.png",
            "- figures/ventes/tendances_temporelles.png",
            "",
            "🎨 Graphiques Interactifs (HTML):",
            "- figures/interactifs/evolution_ca.html",
            "- figures/interactifs/top_produits.html",
            "- figures/interactifs/repartition_categories.html",
            "- figures/interactifs/dashboard_complet.html",
            "",
            "💡 INSTRUCTIONS:",
            "- Les fichiers PNG peuvent être ouverts avec n'importe quel visionneuse d'images",
            "- Les fichiers HTML peuvent être ouverts dans un navigateur web",
            "- Le dashboard_complet.html contient tous les graphiques principaux"
        ]
        
        with open('../reports/rapport_visualisations.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(rapport))
        
        print("✅ Rapport des visualisations généré")
    
    def executer_visualisations_completes(self):
        """Exécute toutes les visualisations"""
        print("🚀 DÉMARRAGE CRÉATION DES VISUALISATIONS")
        print("=" * 50)
        
        try:
            # 1. Préparation
            if not self.charger_donnees():
                return False
                
            self.creer_dossier_figures()
            
            # 2. Création des visualisations
            self.visualiser_kpi_principaux()
            self.visualiser_analyse_produits()
            self.visualiser_analyse_clients()
            self.visualiser_tendances_temporelles()
            self.creer_visualisations_interactives()
            
            # 3. Rapport final
            self.generer_rapport_visualisation()
            
            print("🎉 VISUALISATIONS TERMINÉES AVEC SUCCÈS!")
            print(f"📁 Tous les graphiques sont dans le dossier: figures/")
            return True
            
        except Exception as e:
            print(f"💥 ERREUR VISUALISATIONS: {e}")
            return False

# Fonction pour exécuter directement
def executer_visualisations():
    viz = VisualisationsNorthwind()
    return viz.executer_visualisations_completes()

if __name__ == "__main__":
    executer_visualisations()