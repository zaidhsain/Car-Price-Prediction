import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle
import os

# Configuration de la page
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design moderne
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        padding: 0.5rem;
        border-radius: 10px;
        border: none;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
        border: none;
    }
    .prediction-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 2rem 0;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #FF4B4B;
        margin: 1rem 0;
    }
    h1 {
        color: #1f1f1f;
        font-weight: 700;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Fonction pour charger et entraîner le modèle
@st.cache_resource
def load_model(df):
    """Entraîne le modèle avec les données"""
    # Encodage des colonnes
    df_processed = df.copy()
    df_processed.replace({'Fuel_Type':{'Petrol':0,'Diesel':1,'CNG':2}}, inplace=True)
    df_processed.replace({'Seller_Type':{'Dealer':0,'Individual':1}}, inplace=True)
    df_processed.replace({'Transmission':{'Manual':0,'Automatic':1}}, inplace=True)
    
    # Préparation des données
    X = df_processed.drop(['Car_Name','Selling_Price'], axis=1)
    Y = df_processed['Selling_Price']
    
    # Division des données
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=2)
    
    # Entraînement du modèle
    model = LinearRegression()
    model.fit(X_train, Y_train)
    
    # Score R²
    r2_score = model.score(X_test, Y_test)
    
    return model, r2_score, X.columns.tolist()

# Header
st.title("🚗 Prédiction du Prix de Voiture")
st.markdown("### Estimez le prix de vente de votre voiture en quelques clics")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/car.png", width=80)
    st.title("À propos")
    st.info("""
    Cette application utilise un modèle de **Machine Learning** 
    pour prédire le prix de vente d'une voiture basé sur ses caractéristiques.
    
    **Modèle:** Régression Linéaire
    """)
    
    st.markdown("---")
    st.markdown("### 📊 Chargez vos données")
    uploaded_file = st.file_uploader("Fichier CSV", type=['csv'])

# Chargement des données
if uploaded_file is not None:
    car_dataset = pd.read_csv(uploaded_file)
    
    # Entraînement du modèle
    with st.spinner("🔄 Entraînement du modèle en cours..."):
        model, r2_score, feature_names = load_model(car_dataset)
    
    # Affichage des statistiques du modèle
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📊 Nombre de données", len(car_dataset))
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("🎯 Score R²", f"{r2_score:.4f}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("✅ Statut", "Modèle prêt")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Formulaire de prédiction
    st.markdown("## 🔮 Faites une prédiction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        year = st.slider("📅 Année de fabrication", 
                        min_value=int(car_dataset['Year'].min()), 
                        max_value=int(car_dataset['Year'].max()), 
                        value=int(car_dataset['Year'].mean()))
        
        present_price = st.number_input("💰 Prix actuel (en Lakhs)", 
                                       min_value=0.0, 
                                       max_value=100.0, 
                                       value=5.0, 
                                       step=0.5)
        
        kms_driven = st.number_input("🛣️ Kilomètres parcourus", 
                                    min_value=0, 
                                    max_value=500000, 
                                    value=50000, 
                                    step=1000)
        
        owner = st.selectbox("👤 Nombre de propriétaires précédents", 
                           options=[0, 1, 2, 3])
    
    with col2:
        fuel_type = st.selectbox("⛽ Type de carburant", 
                                options=['Petrol', 'Diesel', 'CNG'])
        
        seller_type = st.selectbox("🏪 Type de vendeur", 
                                  options=['Dealer', 'Individual'])
        
        transmission = st.selectbox("⚙️ Transmission", 
                                   options=['Manual', 'Automatic'])
    
    st.markdown("---")
    
    # Bouton de prédiction
    if st.button("🚀 PRÉDIRE LE PRIX", use_container_width=True):
        # Encodage des inputs
        fuel_encoded = {'Petrol': 0, 'Diesel': 1, 'CNG': 2}[fuel_type]
        seller_encoded = {'Dealer': 0, 'Individual': 1}[seller_type]
        transmission_encoded = {'Manual': 0, 'Automatic': 1}[transmission]
        
        # Préparation des features
        input_data = pd.DataFrame([[year, present_price, kms_driven, fuel_encoded, 
                                   seller_encoded, transmission_encoded, owner]], 
                                 columns=feature_names)
        
        # Prédiction
        prediction = model.predict(input_data)[0]
        
        # Affichage du résultat
        st.markdown(f"""
        <div class="prediction-box">
            <h2>💎 Prix Estimé</h2>
            <h1 style="font-size: 3rem; margin: 1rem 0;">₹ {prediction:.2f} Lakhs</h1>
            <p style="font-size: 1.1rem;">Soit approximativement <b>₹ {prediction * 100000:,.0f}</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Détails de la prédiction
        st.markdown("### 📋 Résumé de votre voiture")
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.markdown(f"""
            <div class="info-box">
            ✓ <b>Année:</b> {year}<br>
            ✓ <b>Prix actuel:</b> ₹ {present_price} Lakhs<br>
            ✓ <b>Kilomètres:</b> {kms_driven:,} km<br>
            ✓ <b>Propriétaires:</b> {owner}
            </div>
            """, unsafe_allow_html=True)
        
        with summary_col2:
            st.markdown(f"""
            <div class="info-box">
            ✓ <b>Carburant:</b> {fuel_type}<br>
            ✓ <b>Vendeur:</b> {seller_type}<br>
            ✓ <b>Transmission:</b> {transmission}
            </div>
            """, unsafe_allow_html=True)

else:
    # Page d'accueil sans données
    st.markdown("""
    <div class="info-box">
        <h3>👋 Bienvenue !</h3>
        <p>Pour commencer, veuillez charger votre fichier CSV de données de voitures 
        dans la barre latérale.</p>
        <p><b>Le fichier doit contenir les colonnes suivantes :</b></p>
        <ul>
            <li>Car_Name</li>
            <li>Year</li>
            <li>Selling_Price</li>
            <li>Present_Price</li>
            <li>Kms_Driven</li>
            <li>Fuel_Type</li>
            <li>Seller_Type</li>
            <li>Transmission</li>
            <li>Owner</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Image de placeholder
    st.image("https://img.icons8.com/clouds/500/000000/car.png", width=300)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Fait avec ❤️ en utilisant Streamlit & Scikit-Learn</p>
</div>
""", unsafe_allow_html=True)