# Car-Price-Prediction# 🚗 Car Price Prediction - Interface Streamlit
<img width="1920" height="1080" alt="Capture d’écran (252)" src="https://github.com/user-attachments/assets/8f757972-5fed-4bd6-8c2c-4d432b14b2d9" />


Application web élégante pour prédire le prix de vente des voitures basée sur un modèle de Machine Learning.

## 📋 Prérequis

- Python 3.8 ou supérieur
- pip

## 🚀 Installation

1. **Installez les dépendances :**
```bash
pip install -r requirements.txt
```

## ▶️ Lancement de l'application

**Méthode 1 : Depuis votre ordinateur**
```bash
streamlit run app.py
```

**Méthode 2 : Sur Google Colab**
```python
# Dans une cellule Colab
!pip install streamlit pyngrok

# Créez un tunnel avec ngrok (nécessite un compte gratuit)
from pyngrok import ngrok
!streamlit run app.py &

# Exposez l'application
public_url = ngrok.connect(8501)
print(f"URL publique: {public_url}")
```

## 📊 Utilisation

1. **Chargez vos données :** 
   - Cliquez sur "Browse files" dans la barre latérale
   - Sélectionnez votre fichier CSV de données de voitures

2. **Remplissez le formulaire :**
   - Année de fabrication
   - Prix actuel
   - Kilomètres parcourus
   - Nombre de propriétaires
   - Type de carburant
   - Type de vendeur
   - Type de transmission

3. **Obtenez la prédiction :**
   - Cliquez sur "PRÉDIRE LE PRIX"
   - Le prix estimé s'affiche avec un résumé détaillé

## 📁 Format du fichier CSV

Votre fichier CSV doit contenir les colonnes suivantes :
- `Car_Name` : Nom de la voiture
- `Year` : Année de fabrication
- `Selling_Price` : Prix de vente (pour l'entraînement)
- `Present_Price` : Prix actuel
- `Kms_Driven` : Kilomètres parcourus
- `Fuel_Type` : Type de carburant (Petrol/Diesel/CNG)
- `Seller_Type` : Type de vendeur (Dealer/Individual)
- `Transmission` : Type de transmission (Manual/Automatic)
- `Owner` : Nombre de propriétaires précédents

## 🎨 Fonctionnalités

✨ Interface moderne et intuitive
📊 Visualisation des métriques du modèle
🔮 Prédictions en temps réel
📱 Design responsive
🎯 Score R² affiché
💾 Chargement dynamique des données

## 🛠️ Technologies utilisées

- **Streamlit** : Framework d'interface web
- **Scikit-Learn** : Modèle de régression linéaire
- **Pandas** : Manipulation des données
- **NumPy** : Calculs numériques

## 📝 Notes

- Le modèle est entraîné à chaque chargement de fichier
- Les prédictions sont basées sur une régression linéaire
- Le score R² indique la qualité du modèle

## 🌐 Déploiement (optionnel)

Pour déployer gratuitement sur Streamlit Cloud :

1. Créez un compte sur [streamlit.io](https://streamlit.io)
2. Connectez votre repo GitHub
3. Déployez en un clic !

---

Fait avec ❤️ pour votre projet de Data Science
