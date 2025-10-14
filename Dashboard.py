# dashboard_crypto.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import random
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Top 40 Cryptomonnaies - Marché des Crypto-actifs",
    page_icon="₿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(45deg, #F7931A, #FF6B00, #FF9500, #FFB800);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        padding: 1rem;
    }
    .crypto-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .crypto-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .crypto-change {
        font-size: 1.2rem;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        display: inline-block;
        margin-top: 0.5rem;
    }
    .positive { background-color: rgba(40, 167, 69, 0.2); color: #28a745; border: 2px solid #28a745; }
    .negative { background-color: rgba(220, 53, 69, 0.2); color: #dc3545; border: 2px solid #dc3545; }
    .neutral { background-color: rgba(108, 117, 125, 0.2); color: #6c757d; border: 2px solid #6c757d; }
    .section-header {
        color: #F7931A;
        border-bottom: 3px solid #4A4A4A;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        font-size: 1.8rem;
    }
    .crypto-icon {
        font-size: 2rem;
        margin-right: 1rem;
    }
    .metric-highlight {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .volatility-indicator {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-weight: bold;
    }
    .low-vol { background-color: #d4edda; color: #155724; }
    .medium-vol { background-color: #fff3cd; color: #856404; }
    .high-vol { background-color: #f8d7da; color: #721c24; }
    .category-major { background: linear-gradient(135deg, #F7931A, #FF9500); }
    .category-defi { background: linear-gradient(135deg, #7B3FF2, #A855F7); }
    .category-meme { background: linear-gradient(135deg, #FF6B00, #FF9500); }
    .category-metaverse { background: linear-gradient(135deg, #00ACC1, #00BCD4); }
    .category-gaming { background: linear-gradient(135deg, #4CAF50, #8BC34A); }
    .category-privacy { background: linear-gradient(135deg, #424242, #616161); }
    .category-layer1 { background: linear-gradient(135deg, #2196F3, #03A9F4); }
    .category-layer2 { background: linear-gradient(135deg, #9C27B0, #BA68C8); }
    .category-exchange { background: linear-gradient(135deg, #FF5722, #FF7043); }
    .category-stablecoin { background: linear-gradient(135deg, #607D8B, #90A4AE); }
</style>
""", unsafe_allow_html=True)

class CryptoDashboard:
    def __init__(self):
        self.cryptos = self.define_cryptos()
        self.historical_data = self.initialize_historical_data()
        self.current_data = self.initialize_current_data()
        self.market_data = self.initialize_market_data()
        
    def define_cryptos(self):
        """Définit les 40 principales cryptomonnaies avec leurs caractéristiques"""
        return {
            # Cryptomonnaies Majeures
            'BTC/USD': {
                'nom': 'Bitcoin / Dollar Américain',
                'symbole': 'BTC/USD',
                'icone': '₿',
                'categorie': 'Majeures',
                'unite': 'prix',
                'prix_base': 65250.0,
                'volatilite': 4.5,
                'volume_journalier': 30.0,  # milliards USD
                'blockchain': 'Bitcoin',
                'date_creation': '2009',
                'total_supply': 21000000,
                'description': 'La première et plus grande cryptomonnaie'
            },
            'ETH/USD': {
                'nom': 'Ethereum / Dollar Américain',
                'symbole': 'ETH/USD',
                'icone': 'Ξ',
                'categorie': 'Majeures',
                'unite': 'prix',
                'prix_base': 3250.0,
                'volatilite': 5.0,
                'volume_journalier': 20.0,
                'blockchain': 'Ethereum',
                'date_creation': '2015',
                'total_supply': None,  # Pas de limite fixe
                'description': 'Plateforme de contrats intelligents'
            },
            'BNB/USD': {
                'nom': 'Binance Coin / Dollar Américain',
                'symbole': 'BNB/USD',
                'icone': '🔶',
                'categorie': 'Majeures',
                'unite': 'prix',
                'prix_base': 580.0,
                'volatilite': 4.2,
                'volume_journalier': 2.5,
                'blockchain': 'Binance Smart Chain',
                'date_creation': '2017',
                'total_supply': 200000000,
                'description': 'Jeton de l\'écosystème Binance'
            },
            'XRP/USD': {
                'nom': 'Ripple / Dollar Américain',
                'symbole': 'XRP/USD',
                'icone': '✕',
                'categorie': 'Majeures',
                'unite': 'prix',
                'prix_base': 0.52,
                'volatilite': 5.5,
                'volume_journalier': 2.0,
                'blockchain': 'Ripple',
                'date_creation': '2012',
                'total_supply': 100000000000,
                'description': 'Système de paiement et de règlement'
            },
            'ADA/USD': {
                'nom': 'Cardano / Dollar Américain',
                'symbole': 'ADA/USD',
                'icone': '₳',
                'categorie': 'Majeures',
                'unite': 'prix',
                'prix_base': 0.45,
                'volatilite': 5.8,
                'volume_journalier': 0.8,
                'blockchain': 'Cardano',
                'date_creation': '2017',
                'total_supply': 45000000000,
                'description': 'Plateforme blockchain à preuve de participation'
            },
            'SOL/USD': {
                'nom': 'Solana / Dollar Américain',
                'symbole': 'SOL/USD',
                'icone': '◎',
                'categorie': 'Majeures',
                'unite': 'prix',
                'prix_base': 145.0,
                'volatilite': 7.2,
                'volume_journalier': 2.8,
                'blockchain': 'Solana',
                'date_creation': '2020',
                'total_supply': None,
                'description': 'Blockchain haute performance'
            },
            'DOGE/USD': {
                'nom': 'Dogecoin / Dollar Américain',
                'symbole': 'DOGE/USD',
                'icone': '🐕',
                'categorie': 'Meme',
                'unite': 'prix',
                'prix_base': 0.16,
                'volatilite': 8.5,
                'volume_journalier': 0.9,
                'blockchain': 'Dogecoin',
                'date_creation': '2013',
                'total_supply': None,
                'description': 'Cryptomonnaie meme populaire'
            },
            'DOT/USD': {
                'nom': 'Polkadot / Dollar Américain',
                'symbole': 'DOT/USD',
                'icone': '●',
                'categorie': 'Majeures',
                'unite': 'prix',
                'prix_base': 7.5,
                'volatilite': 6.8,
                'volume_journalier': 0.7,
                'blockchain': 'Polkadot',
                'date_creation': '2020',
                'total_supply': None,
                'description': 'Plateforme d\'interopérabilité multi-chaînes'
            },
            
            # DeFi
            'UNI/USD': {
                'nom': 'Uniswap / Dollar Américain',
                'symbole': 'UNI/USD',
                'icone': '🦄',
                'categorie': 'DeFi',
                'unite': 'prix',
                'prix_base': 10.5,
                'volatilite': 7.5,
                'volume_journalier': 0.4,
                'blockchain': 'Ethereum',
                'date_creation': '2020',
                'total_supply': 1000000000,
                'description': 'Protocole d\'échange décentralisé'
            },
            'AAVE/USD': {
                'nom': 'Aave / Dollar Américain',
                'symbole': 'AAVE/USD',
                'icone': '👻',
                'categorie': 'DeFi',
                'unite': 'prix',
                'prix_base': 95.0,
                'volatilite': 7.8,
                'volume_journalier': 0.3,
                'blockchain': 'Ethereum',
                'date_creation': '2017',
                'total_supply': 16000000,
                'description': 'Protocole de prêt décentralisé'
            },
            'LINK/USD': {
                'nom': 'Chainlink / Dollar Américain',
                'symbole': 'LINK/USD',
                'icone': '🔗',
                'categorie': 'DeFi',
                'unite': 'prix',
                'prix_base': 14.5,
                'volatilite': 6.5,
                'volume_journalier': 0.6,
                'blockchain': 'Ethereum',
                'date_creation': '2017',
                'total_supply': 1000000000,
                'description': 'Réseau d\'oracles décentralisé'
            },
            'MKR/USD': {
                'nom': 'Maker / Dollar Américain',
                'symbole': 'MKR/USD',
                'icone': '🎩',
                'categorie': 'DeFi',
                'unite': 'prix',
                'prix_base': 2100.0,
                'volatilite': 7.2,
                'volume_journalier': 0.2,
                'blockchain': 'Ethereum',
                'date_creation': '2017',
                'total_supply': 1000000,
                'description': 'Gouvernance du protocole DAI'
            },
            'COMP/USD': {
                'nom': 'Compound / Dollar Américain',
                'symbole': 'COMP/USD',
                'icone': '💰',
                'categorie': 'DeFi',
                'unite': 'prix',
                'prix_base': 55.0,
                'volatilite': 7.0,
                'volume_journalier': 0.15,
                'blockchain': 'Ethereum',
                'date_creation': '2017',
                'total_supply': 10000000,
                'description': 'Protocole de prêt décentralisé'
            },
            'YFI/USD': {
                'nom': 'yearn.finance / Dollar Américain',
                'symbole': 'YFI/USD',
                'icone': '💎',
                'categorie': 'DeFi',
                'unite': 'prix',
                'prix_base': 7200.0,
                'volatilite': 8.5,
                'volume_journalier': 0.12,
                'blockchain': 'Ethereum',
                'date_creation': '2020',
                'total_supply': 36666,
                'description': 'Agrégateur de rendement DeFi'
            },
            'SNX/USD': {
                'nom': 'Synthetix / Dollar Américain',
                'symbole': 'SNX/USD',
                'icone': '🔮',
                'categorie': 'DeFi',
                'unite': 'prix',
                'prix_base': 3.2,
                'volatilite': 8.0,
                'volume_journalier': 0.18,
                'blockchain': 'Ethereum',
                'date_creation': '2017',
                'total_supply': 300000000,
                'description': 'Plateforme d\'actifs synthétiques'
            },
            'CRV/USD': {
                'nom': 'Curve DAO / Dollar Américain',
                'symbole': 'CRV/USD',
                'icone': '〰️',
                'categorie': 'DeFi',
                'unite': 'prix',
                'prix_base': 0.85,
                'volatilite': 7.8,
                'volume_journalier': 0.2,
                'blockchain': 'Ethereum',
                'date_creation': '2020',
                'total_supply': 3300000000,
                'description': 'Plateforme d\'échange stablecoin'
            },
            
            # Layer 1
            'AVAX/USD': {
                'nom': 'Avalanche / Dollar Américain',
                'symbole': 'AVAX/USD',
                'icone': '🔺',
                'categorie': 'Layer 1',
                'unite': 'prix',
                'prix_base': 38.0,
                'volatilite': 7.5,
                'volume_journalier': 0.6,
                'blockchain': 'Avalanche',
                'date_creation': '2020',
                'total_supply': 720000000,
                'description': 'Plateforme blockchain rapide et évolutive'
            },
            'MATIC/USD': {
                'nom': 'Polygon / Dollar Américain',
                'symbole': 'MATIC/USD',
                'icone': '🟣',
                'categorie': 'Layer 2',
                'unite': 'prix',
                'prix_base': 0.92,
                'volatilite': 7.2,
                'volume_journalier': 0.4,
                'blockchain': 'Polygon',
                'date_creation': '2017',
                'total_supply': 10000000000,
                'description': 'Solution de scalabilité pour Ethereum'
            },
            'FTM/USD': {
                'nom': 'Fantom / Dollar Américain',
                'symbole': 'FTM/USD',
                'icone': '👻',
                'categorie': 'Layer 1',
                'unite': 'prix',
                'prix_base': 0.85,
                'volatilite': 8.2,
                'volume_journalier': 0.25,
                'blockchain': 'Fantom',
                'date_creation': '2019',
                'total_supply': 3175000000,
                'description': 'Blockchain DAG haute performance'
            },
            'ATOM/USD': {
                'nom': 'Cosmos / Dollar Américain',
                'symbole': 'ATOM/USD',
                'icone': '⚛️',
                'categorie': 'Layer 1',
                'unite': 'prix',
                'prix_base': 10.5,
                'volatilite': 7.0,
                'volume_journalier': 0.3,
                'blockchain': 'Cosmos',
                'date_creation': '2019',
                'total_supply': None,
                'description': 'Écosystème de blockchains interconnectées'
            },
            'ALGO/USD': {
                'nom': 'Algorand / Dollar Américain',
                'symbole': 'ALGO/USD',
                'icone': '🔷',
                'categorie': 'Layer 1',
                'unite': 'prix',
                'prix_base': 0.18,
                'volatilite': 6.8,
                'volume_journalier': 0.2,
                'blockchain': 'Algorand',
                'date_creation': '2019',
                'total_supply': 10000000000,
                'description': 'Blockchain à preuve de participation pure'
            },
            'NEAR/USD': {
                'nom': 'NEAR Protocol / Dollar Américain',
                'symbole': 'NEAR/USD',
                'icone': '🔵',
                'categorie': 'Layer 1',
                'unite': 'prix',
                'prix_base': 7.8,
                'volatilite': 7.5,
                'volume_journalier': 0.25,
                'blockchain': 'NEAR',
                'date_creation': '2020',
                'total_supply': 1000000000,
                'description': 'Plateforme blockchain conviviale pour les développeurs'
            },
            'ICP/USD': {
                'nom': 'Internet Computer / Dollar Américain',
                'symbole': 'ICP/USD',
                'icone': '🌐',
                'categorie': 'Layer 1',
                'unite': 'prix',
                'prix_base': 13.5,
                'volatilite': 8.0,
                'volume_journalier': 0.3,
                'blockchain': 'Internet Computer',
                'date_creation': '2021',
                'total_supply': 469000000,
                'description': 'Blockchain décentralisée pour le web'
            },
            'HBAR/USD': {
                'nom': 'Hedera / Dollar Américain',
                'symbole': 'HBAR/USD',
                'icone': '🌿',
                'categorie': 'Layer 1',
                'unite': 'prix',
                'prix_base': 0.085,
                'volatilite': 7.2,
                'volume_journalier': 0.15,
                'blockchain': 'Hedera',
                'date_creation': '2019',
                'total_supply': 50000000000,
                'description': 'Réseau DLT entreprise'
            },
            
            # Gaming & Metaverse
            'MANA/USD': {
                'nom': 'Decentraland / Dollar Américain',
                'symbole': 'MANA/USD',
                'icone': '🌍',
                'categorie': 'Metaverse',
                'unite': 'prix',
                'prix_base': 0.45,
                'volatilite': 8.5,
                'volume_journalier': 0.12,
                'blockchain': 'Ethereum',
                'date_creation': '2017',
                'total_supply': 2200000000,
                'description': 'Monde virtuel décentralisé'
            },
            'SAND/USD': {
                'nom': 'The Sandbox / Dollar Américain',
                'symbole': 'SAND/USD',
                'icone': '🏖️',
                'categorie': 'Metaverse',
                'unite': 'prix',
                'prix_base': 0.58,
                'volatilite': 8.2,
                'volume_journalier': 0.15,
                'blockchain': 'Ethereum',
                'date_creation': '2011',
                'total_supply': 3000000000,
                'description': 'Plateforme de gaming métaverse'
            },
            'AXS/USD': {
                'nom': 'Axie Infinity / Dollar Américain',
                'symbole': 'AXS/USD',
                'icone': '🎮',
                'categorie': 'Gaming',
                'unite': 'prix',
                'prix_base': 7.5,
                'volatilite': 8.8,
                'volume_journalier': 0.18,
                'blockchain': 'Ethereum',
                'date_creation': '2020',
                'total_supply': 270000000,
                'description': 'Jeu blockchain play-to-earn'
            },
            'GALA/USD': {
                'nom': 'Gala Games / Dollar Américain',
                'symbole': 'GALA/USD',
                'icone': '🎉',
                'categorie': 'Gaming',
                'unite': 'prix',
                'prix_base': 0.045,
                'volatilite': 9.0,
                'volume_journalier': 0.12,
                'blockchain': 'Ethereum',
                'date_creation': '2019',
                'total_supply': 35000000000,
                'description': 'Plateforme de gaming blockchain'
            },
            'ENJ/USD': {
                'nom': 'Enjin Coin / Dollar Américain',
                'symbole': 'ENJ/USD',
                'icone': '💎',
                'categorie': 'Gaming',
                'unite': 'prix',
                'prix_base': 0.35,
                'volatilite': 8.0,
                'volume_journalier': 0.1,
                'blockchain': 'Ethereum',
                'date_creation': '2017',
                'total_supply': 1000000000,
                'description': 'Écosystème gaming NFT'
            },
            'CHZ/USD': {
                'nom': 'Chiliz / Dollar Américain',
                'symbole': 'CHZ/USD',
                'icone': '🌶️',
                'categorie': 'Gaming',
                'unite': 'prix',
                'prix_base': 0.12,
                'volatilite': 8.5,
                'volume_journalier': 0.08,
                'blockchain': 'Chiliz',
                'date_creation': '2018',
                'total_supply': 8888888888,
                'description': 'Tokenisation du sport et du divertissement'
            },
            
            # Privacy
            'XMR/USD': {
                'nom': 'Monero / Dollar Américain',
                'symbole': 'XMR/USD',
                'icone': '🕵️',
                'categorie': 'Privacy',
                'unite': 'prix',
                'prix_base': 165.0,
                'volatilite': 6.5,
                'volume_journalier': 0.08,
                'blockchain': 'Monero',
                'date_creation': '2014',
                'total_supply': None,
                'description': 'Cryptomonnaie axée sur la confidentialité'
            },
            'ZEC/USD': {
                'nom': 'Zcash / Dollar Américain',
                'symbole': 'ZEC/USD',
                'icone': '🛡️',
                'categorie': 'Privacy',
                'unite': 'prix',
                'prix_base': 28.5,
                'volatilite': 7.0,
                'volume_journalier': 0.05,
                'blockchain': 'Zcash',
                'date_creation': '2016',
                'total_supply': 21000000,
                'description': 'Transactions privées avec zk-SNARKs'
            },
            'DASH/USD': {
                'nom': 'Dash / Dollar Américain',
                'symbole': 'DASH/USD',
                'icone': '💨',
                'categorie': 'Privacy',
                'unite': 'prix',
                'prix_base': 32.5,
                'volatilite': 6.8,
                'volume_journalier': 0.04,
                'blockchain': 'Dash',
                'date_creation': '2014',
                'total_supply': 18900000,
                'description': 'Transactions instantanées et privées'
            },
            
            # Exchange Tokens
            'CRO/USD': {
                'nom': 'Cronos / Dollar Américain',
                'symbole': 'CRO/USD',
                'icone': '🔵',
                'categorie': 'Exchange',
                'unite': 'prix',
                'prix_base': 0.095,
                'volatilite': 7.5,
                'volume_journalier': 0.08,
                'blockchain': 'Cronos',
                'date_creation': '2018',
                'total_supply': 30000000000,
                'description': 'Jeton de l\'écosystème Crypto.com'
            },
            'HT/USD': {
                'nom': 'Huobi Token / Dollar Américain',
                'symbole': 'HT/USD',
                'icone': '🔥',
                'categorie': 'Exchange',
                'unite': 'prix',
                'prix_base': 2.8,
                'volatilite': 7.0,
                'volume_journalier': 0.06,
                'blockchain': 'Ethereum',
                'date_creation': '2018',
                'total_supply': 500000000,
                'description': 'Jeton de l\'échange Huobi'
            },
            'KCS/USD': {
                'nom': 'KuCoin Token / Dollar Américain',
                'symbole': 'KCS/USD',
                'icone': '🪙',
                'categorie': 'Exchange',
                'unite': 'prix',
                'prix_base': 8.5,
                'volatilite': 7.2,
                'volume_journalier': 0.05,
                'blockchain': 'KuCoin',
                'date_creation': '2017',
                'total_supply': 170000000,
                'description': 'Jeton de l\'échange KuCoin'
            },
            
            # Stablecoins
            'USDT/USD': {
                'nom': 'Tether / Dollar Américain',
                'symbole': 'USDT/USD',
                'icone': '💵',
                'categorie': 'Stablecoin',
                'unite': 'prix',
                'prix_base': 1.0,
                'volatilite': 0.1,
                'volume_journalier': 45.0,
                'blockchain': 'Multiple',
                'date_creation': '2014',
                'total_supply': None,
                'description': 'Stablecoin adossée au dollar'
            },
            'USDC/USD': {
                'nom': 'USD Coin / Dollar Américain',
                'symbole': 'USDC/USD',
                'icone': '🪙',
                'categorie': 'Stablecoin',
                'unite': 'prix',
                'prix_base': 1.0,
                'volatilite': 0.1,
                'volume_journalier': 25.0,
                'blockchain': 'Multiple',
                'date_creation': '2018',
                'total_supply': None,
                'description': 'Stablecoin régulée par Circle'
            },
            'BUSD/USD': {
                'nom': 'Binance USD / Dollar Américain',
                'symbole': 'BUSD/USD',
                'icone': '💰',
                'categorie': 'Stablecoin',
                'unite': 'prix',
                'prix_base': 1.0,
                'volatilite': 0.1,
                'volume_journalier': 15.0,
                'blockchain': 'Binance',
                'date_creation': '2019',
                'total_supply': None,
                'description': 'Stablecoin régulée par Binance'
            },
            'DAI/USD': {
                'nom': 'Dai / Dollar Américain',
                'symbole': 'DAI/USD',
                'icone': '🔷',
                'categorie': 'Stablecoin',
                'unite': 'prix',
                'prix_base': 1.0,
                'volatilite': 0.2,
                'volume_journalier': 5.0,
                'blockchain': 'Ethereum',
                'date_creation': '2017',
                'total_supply': None,
                'description': 'Stablecoin algorithmique décentralisée'
            }
        }
    
    def initialize_historical_data(self):
        """Initialise les données historiques des cryptomonnaies"""
        dates = pd.date_range('2020-01-01', datetime.now(), freq='D')
        data = []
        
        for date in dates:
            for symbole, info in self.cryptos.items():
                # Prix de base
                base_price = info['prix_base']
                
                # Impact des événements majeurs du marché crypto
                market_impact = 1.0
                
                # Bull run 2020-2021
                if date.year == 2020 and date.month >= 10:
                    market_impact *= random.uniform(1.02, 1.15)
                elif date.year == 2021 and date.month <= 5:
                    market_impact *= random.uniform(1.05, 1.25)
                # Crash de mai 2021
                elif date.year == 2021 and date.month == 5 and date.day >= 19:
                    market_impact *= random.uniform(0.7, 0.9)
                # Reprise mi-2021
                elif date.year == 2021 and date.month >= 7 and date.month <= 10:
                    market_impact *= random.uniform(1.05, 1.15)
                # Crash de novembre 2021
                elif date.year == 2021 and date.month >= 11:
                    market_impact *= random.uniform(0.8, 0.95)
                # Bear market 2022
                elif date.year == 2022:
                    market_impact *= random.uniform(0.85, 1.05)
                # Reprise 2023
                elif date.year == 2023:
                    if date.month >= 10:
                        market_impact *= random.uniform(1.05, 1.2)
                    else:
                        market_impact *= random.uniform(0.95, 1.1)
                # Bull market 2024
                elif date.year == 2024:
                    market_impact *= random.uniform(1.02, 1.15)
                
                # Volatilité quotidienne basée sur le profil de volatilité
                daily_volatility = random.normalvariate(1, info['volatilite']/100)
                
                # Tendance saisonnière (effet "Uptober", etc.)
                seasonal = 1.0
                if date.month == 10:  # "Uptober"
                    seasonal *= random.uniform(1.01, 1.05)
                elif date.month == 12:  # Rallye de fin d'année
                    seasonal *= random.uniform(1.01, 1.03)
                elif date.month in [1, 2]:  # "Januarry"
                    seasonal *= random.uniform(0.98, 1.02)
                
                # Effet Bitcoin halving (mai 2020, mai 2024)
                if (date.year == 2020 and date.month == 5) or (date.year == 2024 and date.month == 5):
                    market_impact *= random.uniform(1.1, 1.3)
                
                prix_actuel = base_price * market_impact * daily_volatility * seasonal
                
                data.append({
                    'date': date,
                    'symbole': symbole,
                    'nom': info['nom'],
                    'categorie': info['categorie'],
                    'prix': prix_actuel,
                    'volume': random.uniform(100000, 5000000),
                    'volatilite_jour': abs(daily_volatility - 1) * 100
                })
        
        return pd.DataFrame(data)
    
    def initialize_current_data(self):
        """Initialise les données courantes"""
        current_data = []
        for symbole, info in self.cryptos.items():
            # Dernières données historiques
            last_data = self.historical_data[self.historical_data['symbole'] == symbole].iloc[-1]
            
            # Variations simulées
            change_pct = random.uniform(-5.0, 5.0)
            
            current_data.append({
                'symbole': symbole,
                'nom': info['nom'],
                'icone': info['icone'],
                'categorie': info['categorie'],
                'unite': info['unite'],
                'prix': last_data['prix'] * (1 + change_pct/100),
                'change_pct': change_pct,
                'volatilite': info['volatilite'],
                'volume_journalier': info['volume_journalier'],
                'blockchain': info['blockchain'],
                'date_creation': info['date_creation'],
                'total_supply': info['total_supply'],
                'market_cap': last_data['prix'] * (info['total_supply'] if info['total_supply'] else 1000000000) / 1000000000,  # En milliards
                'spread': random.uniform(0.01, 0.5)
            })
        
        return pd.DataFrame(current_data)
    
    def initialize_market_data(self):
        """Initialise les données des marchés crypto"""
        indices = {
            'Crypto Fear & Greed Index': {'valeur': 65, 'change': 0, 'secteur': 'Sentiment'},
            'Bitcoin Dominance': {'valeur': 48.5, 'change': 0, 'secteur': 'BTC'},
            'Ethereum Dominance': {'valeur': 18.2, 'change': 0, 'secteur': 'ETH'},
            'DeFi TVL': {'valeur': 85.3, 'change': 0, 'secteur': 'DeFi'},
            'NFT Volume': {'valeur': 2.8, 'change': 0, 'secteur': 'NFT'},
            'Stablecoin Supply': {'valeur': 125.5, 'change': 0, 'secteur': 'Stablecoins'}
        }
        
        return {'indices': indices}
    
    def update_live_data(self):
        """Met à jour les données en temps réel"""
        for idx in self.current_data.index:
            symbole = self.current_data.loc[idx, 'symbole']
            
            # Mise à jour des prix
            if random.random() < 0.7:  # 70% de chance de changement
                variation = random.uniform(-2.0, 2.0)
                
                self.current_data.loc[idx, 'prix'] *= (1 + variation/100)
                self.current_data.loc[idx, 'change_pct'] = variation
                
                # Mise à jour du volume
                self.current_data.loc[idx, 'volume_journalier'] *= random.uniform(0.8, 1.2)
                
                # Mise à jour de la capitalisation boursière
                if self.current_data.loc[idx, 'total_supply']:
                    self.current_data.loc[idx, 'market_cap'] = (
                        self.current_data.loc[idx, 'prix'] * 
                        self.current_data.loc[idx, 'total_supply'] / 1000000000
                    )
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown(
            '<h1 class="main-header">₿ DASHBOARD TOP 40 CRYPTOMONNAIES - MARCHÉ DES CRYPTO-ACTIFS</h1>', 
            unsafe_allow_html=True
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                '<div style="text-align: center; background: linear-gradient(45deg, #F7931A, #FF6B00); '
                'color: white; padding: 1rem; border-radius: 10px; margin-bottom: 2rem;">'
                '<h3>🔴 SURVEILLANCE EN TEMPS RÉEL DES 40 PRINCIPALES CRYPTOMONNAIES</h3>'
                '</div>', 
                unsafe_allow_html=True
            )
        
        current_time = datetime.now().strftime('%H:%M:%S')
        st.sidebar.markdown(f"**🕐 Dernière mise à jour: {current_time}**")
    
    def display_crypto_cards(self):
        """Affiche les cartes de cryptomonnaies principales"""
        st.markdown('<h3 class="section-header">💰 PRIX DES CRYPTOMONNAIES EN TEMPS RÉEL</h3>', 
                   unsafe_allow_html=True)
        
        # Grouper par catégorie
        categories = self.current_data['categorie'].unique()
        
        for categorie in categories:
            st.markdown(f'<h4 style="color: #F7931A; margin-top: 1rem;">{categorie}</h4>', 
                       unsafe_allow_html=True)
            
            cat_data = self.current_data[self.current_data['categorie'] == categorie]
            
            # Afficher 4 cryptomonnaies par ligne
            for i in range(0, len(cat_data), 4):
                cols = st.columns(min(4, len(cat_data) - i))
                
                for j, (_, crypto) in enumerate(cat_data.iloc[i:i+4].iterrows()):
                    with cols[j]:
                        change_class = "positive" if crypto['change_pct'] > 0 else "negative" if crypto['change_pct'] < 0 else "neutral"
                        card_class = f"crypto-card category-{categorie.lower().replace(' ', '').replace('/', '').replace('-', '')}"
                        
                        st.markdown(f"""
                        <div class="{card_class}">
                            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                                <span class="crypto-icon">{crypto['icone']}</span>
                                <div>
                                    <h3 style="margin: 0; font-size: 1.2rem;">{crypto['symbole']}</h3>
                                    <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">{crypto['nom']}</p>
                                </div>
                            </div>
                            <div class="crypto-value">${crypto['prix']:.4f}</div>
                            <div style="font-size: 0.9rem; opacity: 0.8;">{crypto['unite']}</div>
                            <div class="crypto-change {change_class}">
                                {crypto['change_pct']:+.2f}%
                            </div>
                            <div style="margin-top: 1rem; font-size: 0.8rem;">
                                📊 Vol: ${crypto['volume_journalier']:.1f}B<br>
                                📈 Volatilité: {crypto['volatilite']:.1f}%<br>
                                💰 Cap: ${crypto['market_cap']:.1f}B
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    def display_key_metrics(self):
        """Affiche les métriques clés"""
        st.markdown('<h3 class="section-header">📊 INDICATEURS MARCHÉ</h3>', 
                   unsafe_allow_html=True)
        
        # Calcul des métriques globales
        avg_change = self.current_data['change_pct'].mean()
        total_volume = self.current_data['volume_journalier'].sum()
        total_market_cap = self.current_data['market_cap'].sum()
        strongest_crypto = self.current_data.loc[self.current_data['change_pct'].idxmax()]
        weakest_crypto = self.current_data.loc[self.current_data['change_pct'].idxmin()]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Performance Moyenne",
                f"{avg_change:+.2f}%",
                "Journalier",
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                "Volume Total Journalier",
                f"${total_volume:,.1f}B",
                f"{random.randint(-15, 25)}% vs hier"
            )
        
        with col3:
            st.metric(
                "Capitalisation Totale",
                f"${total_market_cap:,.0f}B",
                f"{random.randint(-5, 10)}% vs hier"
            )
        
        with col4:
            st.metric(
                "Plus Forte Hausse",
                f"{strongest_crypto['symbole']}",
                f"{strongest_crypto['change_pct']:+.2f}%"
            )
    
    def create_price_overview(self):
        """Crée la vue d'ensemble des prix"""
        st.markdown('<h3 class="section-header">📈 ANALYSE DES PRIX HISTORIQUES</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "Évolution Historique", 
            "Analyse par Catégorie", 
            "Volatilité", 
            "Performances Relatives"
        ])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Sélection des cryptomonnaies à afficher
                selected_cryptos = st.multiselect(
                    "Sélectionnez les cryptomonnaies:",
                    list(self.cryptos.keys()),
                    default=['BTC/USD', 'ETH/USD', 'BNB/USD', 'XRP/USD', 'SOL/USD']
                )
            
            with col2:
                # Période d'analyse
                period = st.selectbox(
                    "Période d'analyse:",
                    ['1 mois', '3 mois', '6 mois', '1 an', '2 ans', 'Toute la période'],
                    index=3
                )
            
            # Filtrage des données
            filtered_data = self.historical_data[
                self.historical_data['symbole'].isin(selected_cryptos)
            ]
            
            if period != 'Toute la période':
                if 'mois' in period:
                    months = int(period.split()[0])
                    cutoff_date = datetime.now() - timedelta(days=30 * months)
                else:
                    years = int(period.split()[0])
                    cutoff_date = datetime.now() - timedelta(days=365 * years)
                filtered_data = filtered_data[filtered_data['date'] >= cutoff_date]
            
            fig = px.line(filtered_data, 
                         x='date', 
                         y='prix',
                         color='symbole',
                         title=f'Évolution des Prix des Cryptomonnaies ({period})',
                         color_discrete_sequence=px.colors.qualitative.Bold)
            fig.update_layout(yaxis_title="Prix (USD)")
            st.plotly_chart(fig, width='stretch')
        
        with tab2:
            # Analyse par catégorie
            fig = px.box(self.historical_data, 
                        x='categorie', 
                        y='prix',
                        title='Distribution des Prix par Catégorie',
                        color='categorie')
            st.plotly_chart(fig, width='stretch')
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Volatilité historique
                volatilite_data = self.historical_data.groupby('symbole')['volatilite_jour'].mean().reset_index()
                fig = px.bar(volatilite_data, 
                            x='symbole', 
                            y='volatilite_jour',
                            title='Volatilité Historique Moyenne (%)',
                            color='symbole',
                            color_discrete_sequence=px.colors.qualitative.Bold)
                st.plotly_chart(fig, width='stretch')
            
            with col2:
                # Volatilité récente (30 derniers jours)
                recent_data = self.historical_data[
                    self.historical_data['date'] > (datetime.now() - timedelta(days=30))
                ]
                recent_vol = recent_data.groupby('symbole')['volatilite_jour'].std().reset_index()
                
                fig = px.scatter(recent_vol, 
                               x='symbole', 
                               y='volatilite_jour',
                               size='volatilite_jour',
                               title='Volatilité Récente (30 jours)',
                               color='symbole',
                               size_max=40)
                st.plotly_chart(fig, width='stretch')
        
        with tab4:
            # Performance relative
            performance_data = []
            for symbole in self.cryptos.keys():
                crypto_data = self.historical_data[self.historical_data['symbole'] == symbole]
                if len(crypto_data) > 0:
                    start_price = crypto_data.iloc[0]['prix']
                    end_price = crypto_data.iloc[-1]['prix']
                    performance = ((end_price - start_price) / start_price) * 100
                    performance_data.append({
                        'symbole': symbole,
                        'performance': performance,
                        'categorie': self.cryptos[symbole]['categorie']
                    })
            
            performance_df = pd.DataFrame(performance_data)
            fig = px.bar(performance_df, 
                        x='symbole', 
                        y='performance',
                        color='categorie',
                        title='Performance Totale depuis 2020 (%)',
                        color_discrete_sequence=px.colors.qualitative.Bold)
            st.plotly_chart(fig, width='stretch')
    
    def create_blockchain_analysis(self):
        """Analyse des blockchains"""
        st.markdown('<h3 class="section-header">⛓️ ANALYSE DES BLOCKCHAINS</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Écosystèmes", "Métriques On-Chain", "Développement"])
        
        with tab1:
            st.subheader("Principaux Écosystèmes Blockchain")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🟠 Bitcoin
                
                **Position:** Leader du marché
                **Capitalisation:** $1.3T
                **Hash Rate:** 450 EH/s
                **Difficulté:** 72.01T
                
                **Facteurs d'influence:**
                - Halving tous les 4 ans
                - Adoption institutionnelle
                - ETFs Bitcoin
                
                ### 🔵 Ethereum
                
                **Position:** Leader des contrats intelligents
                **Capitalisation:** $400B
                **TVL:** $85B
                **Gas Fee:** 15 Gwei
                
                **Facteurs d'influence:**
                - Mise à jour Dencun
                - EIP-4844 (Proto-Danksharding)
                - ETFs Ethereum
                """)
            
            with col2:
                st.markdown("""
                ### 🟣 Solana
                
                **Position:** Blockchain haute performance
                **Capitalisation:** $65B
                **TPS:** 65,000
                **Temps de bloc:** 400ms
                
                **Facteurs d'influence:**
                - Écosystème DeFi en croissance
                - Projets NFT
                - Performance technique
                
                ### 🔶 Binance Smart Chain
                
                **Position:** Alternative à Ethereum
                **Capitalisation:** $85B
                **TVL:** $5.8B
                **Transactions/jour:** 4.2M
                
                **Facteurs d'influence:**
                - Écosystème Binance
                - Faibles coûts de transaction
                - Projets GameFi
                """)
        
        with tab2:
            st.subheader("Métriques On-Chain Clés")
            
            # Données des métriques on-chain
            on_chain_metrics = {
                'Bitcoin': {
                    'Active Addresses': 950000,
                    'Transactions/Day': 280000,
                    'Average Fee': 2.5,
                    'Hash Rate': 450,
                    'Difficulty': 72.01
                },
                'Ethereum': {
                    'Active Addresses': 520000,
                    'Transactions/Day': 1150000,
                    'Average Fee': 1.8,
                    'Gas Used': 95.2,
                    'TVL': 85.3
                },
                'BNB Chain': {
                    'Active Addresses': 1800000,
                    'Transactions/Day': 4200000,
                    'Average Fee': 0.15,
                    'TVL': 5.8,
                    'Validators': 41
                },
                'Solana': {
                    'Active Addresses': 350000,
                    'Transactions/Day': 25000000,
                    'Average Fee': 0.00025,
                    'TPS': 65000,
                    'Validators': 3200
                },
                'Cardano': {
                    'Active Addresses': 180000,
                    'Transactions/Day': 85000,
                    'Average Fee': 0.17,
                    'Stake Pools': 3200,
                    'Staked ADA': 23.5
                }
            }
            
            # Création du graphique
            metrics_df = pd.DataFrame([
                {'Blockchain': k, 'Active Addresses': v['Active Addresses']/1000} 
                for k, v in on_chain_metrics.items()
            ])
            
            fig = px.bar(metrics_df, 
                        x='Blockchain', 
                        y='Active Addresses',
                        title='Adresses Actives (en milliers)',
                        color='Blockchain',
                        color_discrete_sequence=px.colors.qualitative.Bold)
            st.plotly_chart(fig, width='stretch')
            
            # Tableau des métriques
            st.subheader("Tableau Comparatif des Métriques")
            metrics_table = pd.DataFrame(on_chain_metrics).T
            st.dataframe(metrics_table, use_container_width=True)
        
        with tab3:
            st.subheader("Activité de Développement")
            
            st.markdown("""
            ### 📊 Mises à Jour Récentes et Roadmaps
            
            **🟠 Bitcoin:**
            - Taproot activé (novembre 2021)
            - Lightning Network en croissance
            - Prochaines mises à jour: OP_CHECKTEMPLATEVERIFY, CTV
            
            **🔵 Ethereum:**
            - Dencun Upgrade (mars 2024)
            - Proto-Danksharding (EIP-4844)
            - Roadmap: The Surge, The Scourge, The Verge, The Purge, The Splurge
            
            **🟣 Solana:**
            - Mise à niveau v1.17 (février 2024)
            - Améliorations de la fiabilité
            - Roadmap: Solana Mobile, Firedancer
            
            **🔶 BNB Chain:**
            - BNB Chain opBNB Mainnet (septembre 2023)
            - zkBNB en développement
            - Roadmap: BNB Greenfield, BNB Chain 2.0
            
            **🟪 Polygon:**
            - Polygon 2.0 (2023-2024)
            - zkEVM Mainnet (mars 2023)
            - Roadmap: AggLayer, Polygon Miden
            """)
    
    def create_technical_analysis(self):
        """Analyse technique avancée"""
        st.markdown('<h3 class="section-header">🔬 ANALYSE TECHNIQUE AVANCÉE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Indicateurs Techniques", "Patterns de Trading", "Signaux"])
        
        with tab1:
            crypto_selectionnee = st.selectbox("Sélectionnez une cryptomonnaie:", 
                                             list(self.cryptos.keys()))
            
            if crypto_selectionnee:
                crypto_data = self.historical_data[
                    self.historical_data['symbole'] == crypto_selectionnee
                ].copy()
                
                # Calcul des indicateurs techniques
                crypto_data['MA20'] = crypto_data['prix'].rolling(window=20).mean()
                crypto_data['MA50'] = crypto_data['prix'].rolling(window=50).mean()
                crypto_data['RSI'] = self.calculate_rsi(crypto_data['prix'])
                crypto_data['Bollinger_High'], crypto_data['Bollinger_Low'] = self.calculate_bollinger_bands(crypto_data['prix'])
                
                fig = make_subplots(rows=3, cols=1, 
                                  shared_xaxes=True, 
                                  vertical_spacing=0.05,
                                  subplot_titles=('Prix et Moyennes Mobiles', 'Bandes de Bollinger', 'RSI'),
                                  row_heights=[0.5, 0.25, 0.25])
                
                # Prix et moyennes mobiles
                fig.add_trace(go.Scatter(x=crypto_data['date'], y=crypto_data['prix'],
                                       name='Prix', line=dict(color='#F7931A')), row=1, col=1)
                fig.add_trace(go.Scatter(x=crypto_data['date'], y=crypto_data['MA20'],
                                       name='MM20', line=dict(color='orange')), row=1, col=1)
                fig.add_trace(go.Scatter(x=crypto_data['date'], y=crypto_data['MA50'],
                                       name='MM50', line=dict(color='red')), row=1, col=1)
                
                # Bandes de Bollinger
                fig.add_trace(go.Scatter(x=crypto_data['date'], y=crypto_data['Bollinger_High'],
                                       name='Bollinger High', line=dict(color='gray', dash='dash')), row=2, col=1)
                fig.add_trace(go.Scatter(x=crypto_data['date'], y=crypto_data['prix'],
                                       name='Prix', line=dict(color='#F7931A'), showlegend=False), row=2, col=1)
                fig.add_trace(go.Scatter(x=crypto_data['date'], y=crypto_data['Bollinger_Low'],
                                       name='Bollinger Low', line=dict(color='gray', dash='dash'), 
                                       fill='tonexty'), row=2, col=1)
                
                # RSI
                fig.add_trace(go.Scatter(x=crypto_data['date'], y=crypto_data['RSI'],
                                       name='RSI', line=dict(color='purple')), row=3, col=1)
                fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
                fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)
                
                fig.update_layout(height=800, title_text=f"Analyse Technique - {crypto_selectionnee}")
                st.plotly_chart(fig, width='stretch')
        
        with tab2:
            st.subheader("Patterns de Trading Identifiés")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 📈 Patterns Haussiers
                
                **🔺 Double Bottom (BTC/USD):**
                - Support solide à $60,000
                - Rebond technique confirmé
                - Objectif: $72,000
                
                **🔼 Triangle Ascendant (ETH/USD):**
                - Consolidation haussière
                - Rupture imminente
                - Volume croissant
                
                **🚀 Breakout (SOL/USD):**
                - Résistance franchie à $150
                - Momentum positif
                - Retest réussi
                """)
            
            with col2:
                st.markdown("""
                ### 📉 Patterns Baissiers
                
                **🔻 Double Top (XRP/USD):**
                - Résistance à $0.65
                - Échec de rupture
                - Objectif: $0.45
                
                **🔽 Tête et Épaules (ADA/USD):**
                - Pattern de retournement
                - Volume de distribution
                - Ligne de cou à $0.40
                
                **⬇️ Baisse en Biseau (DOT/USD):**
                - Structure baissière
                - Volume décroissant
                - Support à $6.50
                """)
        
        with tab3:
            st.subheader("Signaux de Trading")
            
            # Tableau des signaux
            signals_data = []
            for symbole in list(self.cryptos.keys())[:10]:  # Limiter à 10 pour l'exemple
                signal_type = random.choice(['Achat', 'Vente', 'Neutre'])
                strength = random.randint(1, 10)
                timeframe = random.choice(['1H', '4H', '1D', '1W'])
                
                signals_data.append({
                    'Cryptomonnaie': symbole,
                    'Signal': signal_type,
                    'Force': strength,
                    'Timeframe': timeframe,
                    'Prix Cible': f"${random.uniform(0.1, 100000):.2f}"
                })
            
            signals_df = pd.DataFrame(signals_data)
            
            # Coloration des signaux
            def color_signal(val):
                color = 'green' if val == 'Achat' else 'red' if val == 'Vente' else 'gray'
                return f'color: {color}'
            
            styled_df = signals_df.style.applymap(color_signal, subset=['Signal'])
            st.dataframe(styled_df, use_container_width=True)
    
    def calculate_rsi(self, prices, window=14):
        """Calcule le RSI (Relative Strength Index)"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def calculate_bollinger_bands(self, prices, window=20, num_std=2):
        """Calcule les bandes de Bollinger"""
        rolling_mean = prices.rolling(window=window).mean()
        rolling_std = prices.rolling(window=window).std()
        upper_band = rolling_mean + (rolling_std * num_std)
        lower_band = rolling_mean - (rolling_std * num_std)
        return upper_band, lower_band
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Catégories à afficher
        st.sidebar.markdown("### 🏷️ Catégories à surveiller")
        categories = list(self.current_data['categorie'].unique())
        categories_selectionnees = st.sidebar.multiselect(
            "Sélectionnez les catégories:",
            categories,
            default=categories
        )
        
        # Période d'analyse
        st.sidebar.markdown("### 📅 Période d'analyse")
        date_debut = st.sidebar.date_input("Date de début", 
                                         value=datetime.now() - timedelta(days=365))
        date_fin = st.sidebar.date_input("Date de fin", 
                                       value=datetime.now())
        
        # Options d'analyse
        st.sidebar.markdown("### ⚙️ Options d'analyse")
        auto_refresh = st.sidebar.checkbox("Rafraîchissement automatique", value=True)
        show_advanced = st.sidebar.checkbox("Indicateurs avancés", value=True)
        alert_threshold = st.sidebar.slider("Seuil d'alerte (%)", 1.0, 10.0, 3.0)
        
        # Bouton de rafraîchissement
        if st.sidebar.button("🔄 Rafraîchir les données"):
            self.update_live_data()
            st.rerun()
        
        # Alertes en temps réel
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🔔 ALERTES EN TEMPS RÉEL")
        
        for _, crypto in self.current_data.iterrows():
            if abs(crypto['change_pct']) > alert_threshold:
                alert_type = "warning" if crypto['change_pct'] > 0 else "error"
                if alert_type == "warning":
                    st.sidebar.warning(
                        f"{crypto['icone']} {crypto['symbole']}: "
                        f"{crypto['change_pct']:+.2f}%"
                    )
                else:
                    st.sidebar.error(
                        f"{crypto['icone']} {crypto['symbole']}: "
                        f"{crypto['change_pct']:+.2f}%"
                    )
        
        return {
            'categories_selectionnees': categories_selectionnees,
            'date_debut': date_debut,
            'date_fin': date_fin,
            'auto_refresh': auto_refresh,
            'show_advanced': show_advanced,
            'alert_threshold': alert_threshold
        }
    
    def create_market_analysis(self):
        """Analyse des marchés crypto"""
        st.markdown('<h3 class="section-header">🌍 ANALYSE DES MARCHÉS CRYPTO</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Indices Crypto", "Analyse Macro"])
        
        with tab1:
            st.subheader("Indices du Marché Crypto")
            
            cols = st.columns(3)
            indices_list = list(self.market_data['indices'].items())
            
            for i, (indice, data) in enumerate(indices_list):
                with cols[i % 3]:
                    data['change'] = random.uniform(-5, 5)  # Mise à jour simulée
                    st.metric(
                        indice,
                        f"{data['valeur']:.1f}",
                        f"{data['change']:+.2f}%",
                        delta_color="normal"
                    )
        
        with tab2:
            st.subheader("Facteurs Macroéconomiques")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 📈 Facteurs Haussiers
                
                **🏦 Adoption Institutionnelle:**
                - ETFs Bitcoin approuvés
                - Entreprises Fortune 500
                - Gestionnaires d'actifs traditionnels
                
                **🌐 Régulation Favorable:**
                - Cadres légaux clairs
                - Protection des investisseurs
                - Stabilité juridique
                
                **💰 Innovation Technologique:**
                - Scalabilité améliorée
                - Solutions Layer 2
                - Interopérabilité
                """)
            
            with col2:
                st.markdown("""
                ### 📉 Facteurs Baissiers
                
                **⚖️ Régulation Stricte:**
                - Interdictions partielles
                - Taxes élevées
                - Restrictions bancaires
                
                **🔒 Cybersécurité:**
                - Hacks et vols
                - Vulnérabilités smart contracts
                - Perte de confiance
                
                **📉 Volatilité Extrême:**
                - Manipulation de marché
                - Liquidations massives
                - Paniques collectives
                """)
    
    def create_risk_analysis(self):
        """Analyse des risques"""
        st.markdown('<h3 class="section-header">⚠️ ANALYSE DES RISQUES</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Risques par Crypto", "Stress Tests", "Stratégies"])
        
        with tab1:
            st.subheader("Évaluation des Risques par Cryptomonnaie")
            
            risk_data = []
            for symbole, info in self.cryptos.items():
                risk_score = random.randint(20, 90)
                risk_level = "FAIBLE" if risk_score < 40 else "MOYEN" if risk_score < 70 else "ÉLEVÉ"
                
                risk_data.append({
                    'Cryptomonnaie': info['nom'],
                    'Symbole': symbole,
                    'Score Risque': risk_score,
                    'Niveau': risk_level,
                    'Risque Réglementaire': random.randint(10, 80),
                    'Risque Technologique': random.randint(15, 75),
                    'Risque de Marché': random.randint(20, 85)
                })
            
            risk_df = pd.DataFrame(risk_data)
            st.dataframe(risk_df, width='stretch')
        
        with tab2:
            st.subheader("Scénarios de Stress Test")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 📉 Scénario Bear Market
                
                **Hypothèses:**
                - Bitcoin -70%
                - Altcoins -85%
                - Volume -60%
                - Fuite des capitaux
                
                **Impacts:**
                - Liquidations massives
                - Faillite d'exchanges
                - Perte de confiance
                - Régulation renforcée
                
                **Probabilité:** 30%
                """)
            
            with col2:
                st.markdown("""
                ### 📈 Scénario Bull Run
                
                **Hypothèses:**
                - Bitcoin +300%
                - Altcoins +500%
                - Volume +400%
                - Adoption massive
                
                **Impacts:**
                - Nouveaux records
                - Institutionnalisation
                - Innovation accélérée
                - Médias positifs
                
                **Probabilité:** 25%
                """)
        
        with tab3:
            st.subheader("Stratégies de Gestion des Risques")
            
            st.markdown("""
            ### 🛡️ Approches de Sécurité
            
            **🔐 Diversification:**
            - Allocation multi-actifs
            - Différentes catégories
            - Répartition géographique
            
            **⏱️ Dollar Cost Averaging:**
            - Investissements réguliers
            - Lissage de la volatilité
            - Discipline d'investissement
            
            **🔒 Stockage Sécurisé:**
            - Cold storage
            - Hardware wallets
            - Multi-signatures
            
            **📊 Analyse Technique:**
            - Points d'entrée/sortie
                - Stop-loss
                - Take-profit
                - Gestion de position
            """)
    
    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Mise à jour des données
        self.update_live_data()
        
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Cartes de cryptomonnaies
        self.display_crypto_cards()
        
        # Métriques clés
        self.display_key_metrics()
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 Vue d'Ensemble", 
            "⛓️ Blockchains", 
            "🔬 Technique", 
            "🌍 Marchés", 
            "⚠️ Risques", 
            "💡 Insights"
        ])
        
        with tab1:
            self.create_price_overview()
        
        with tab2:
            self.create_blockchain_analysis()
        
        with tab3:
            self.create_technical_analysis()
        
        with tab4:
            self.create_market_analysis()
        
        with tab5:
            self.create_risk_analysis()
        
        with tab6:
            st.markdown("## 💡 INSIGHTS STRATÉGIQUES")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🎯 Tendances du Marché
                
                **📊 Adoption Croissante:**
                - ETFs gagnent en popularité
                - Entreprises traditionnelles s'intéressent
                - Gouvernements explorent la CBDC
                
                **🔗 DeFi 2.0:**
                - Solutions de scalabilité
                - Interopérabilité entre chaînes
                - Yield farming optimisé
                
                **🎮 Gaming & Metaverse:**
                - Play-to-earn évolue
                - Actifs numériques vérifiables
                - Économies virtuelles
                """)
            
            with col2:
                st.markdown("""
                ### 🚀 Opportunités d'Investissement
                
                **🌐 Layer 1 Émergents:**
                - Blockchains spécialisées
                - Consensus innovants
                - Écosystèmes en croissance
                
                **🔐 Solutions de Confidentialité:**
                - ZK-proofs
                - Transactions privées
                - Protection des données
                
                **⚡ Infrastructure Web3:**
                - Stockage décentralisé
                - Oracles fiables
                - Interopérabilité
                """)
            
            st.markdown("---")
            
            st.subheader("📈 Prévisions et Perspectives")
            
            st.markdown("""
            ### 🎯 Scénario Base (Probabilité: 45%)
            
            **2024-2025:**
            - Bitcoin atteint $100,000
            - Ethereum dépasse $5,000
            - Capitalisation totale > $5T
            - Adoption institutionnelle continue
            
            **Facteurs clés:**
            - ETFs bien reçus
            - Régulation équilibrée
            - Innovation technologique
            - Stabilité macroéconomique
            
            ### ⚠️ Points de Vigilance
            
            **🔴 Risques Réglementaires:**
            - Surveillance accrue
            - Taxation des plus-values
            - Restrictions géographiques
            
            **🟡 Risques Technologiques:**
            - Failles de sécurité
                - Problèmes de scalabilité
                - Bugs dans les smart contracts
                
            **🟢 Opportunités:**
            - Nouveaux cas d'usage
            - Partenariats stratégiques
            - Innovation continue
            """)

# Exécution du dashboard
if __name__ == "__main__":
    dashboard = CryptoDashboard()
    dashboard.run_dashboard()