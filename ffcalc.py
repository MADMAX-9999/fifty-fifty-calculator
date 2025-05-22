import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Konfiguracja strony z lepszymi ustawieniami
st.set_page_config(
    page_title="Kalkulator Strategii Fifty/Fifty", 
    layout="wide",
    base="dark",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://bit.ly/m/wozniak',
        'Report a bug': None,
        'About': "Kalkulator Strategii Fifty/Fifty v2.0"
    }
)





# CSS dla lepszego stylu
st.markdown("""
<style>
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .strategy-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #2F80ED;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #FFF3CD;
        border: 1px solid #FFE69C;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #D1E7DD;
        border: 1px solid #BADBCC;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #2F80ED, #56CCF2);
    }
</style>
""", unsafe_allow_html=True)

# Caching dla lepszej wydajności
@st.cache_data
def load_strategies():
    """Ładowanie strategii z cache"""
    return [
        {
            "name": "START",
            "minValue": 5000,
            "maxValue": 10000,
            "description": "Fundamentalny pierwszy krok w budowaniu trwałego, materialnego majątku zabezpieczonego przed inflacją",
            "minPurchase": 100,
            "maxPurchase": 1000,
            "minYears": 7,
            "maxYears": 30,
            "yearsDescription": "Horyzont czasowy 7-30+ lat stanowi perspektywę dla budowy solidnych podstaw majątkowych",
            "step": 250,
            "risk_level": "Niskie",
            "complexity": "Proste"
        },
        {
            "name": "BALANCE",
            "minValue": 10000,
            "maxValue": 100000,
            "description": "Zaawansowana dywersyfikacja majątku poprzez zrównoważoną alokację kapitału między różne klasy metali",
            "minPurchase": 250,
            "maxPurchase": 2500,
            "minYears": 7,
            "maxYears": 30,
            "yearsDescription": "Perspektywa 7-30+ lat to początek drogi ku stworzeniu trwałego majątku rodzinnego",
            "step": 500,
            "risk_level": "Umiarkowane",
            "complexity": "Średnie"
        },
        {
            "name": "FOUNDATION",
            "minValue": 100000,
            "maxValue": 700000,
            "description": "Kompleksowe rozwiązanie dla budowania solidnego fundamentu majątkowego opartego na materialnych aktywach",
            "minPurchase": 500,
            "maxPurchase": 5000,
            "minYears": 15,
            "maxYears": 30,
            "yearsDescription": "Horyzont 15-30+ lat to optymalny okres dla ukazania pełnego potencjału strategii",
            "step": 5000,
            "risk_level": "Umiarkowane",
            "complexity": "Zaawansowane"
        },
        {
            "name": "OPTIMAL",
            "minValue": 700000,
            "maxValue": 2100000,
            "description": "Zaawansowane rozwiązanie dla tworzenia znaczącego majątku materialnego o najwyższym stopniu odporności",
            "minPurchase": 1000,
            "maxPurchase": 20000,
            "minYears": 15,
            "maxYears": 30,
            "yearsDescription": "Perspektywa 15-30+ lat stanowi ramę czasową dla strategicznego rozwoju portfela",
            "step": 10000,
            "risk_level": "Umiarkowane",
            "complexity": "Ekspert"
        },
        {
            "name": "PRESTIGE",
            "minValue": 2100000,
            "maxValue": 5000000,
            "description": "Kwintesencja budowania dynastycznego majątku materialnego z dominującym udziałem metali strategicznych",
            "minPurchase": 2500,
            "maxPurchase": 50000,
            "minYears": 20,
            "maxYears": 30,
            "yearsDescription": "Perspektywa 20-30+ lat odzwierciedla horyzont planowania ponadpokoleniowego majątku",
            "step": 25000,
            "risk_level": "Wysokie",
            "complexity": "Ekspert"
        }
    ]

@st.cache_data
def calculate_projection(initial_amount, weekly_purchase, years, annual_growth_rate=0.05):
    """Obliczanie projekcji wzrostu z uwzględnieniem stopy zwrotu"""
    months = years * 12
    monthly_purchase = weekly_purchase * 52 / 12
    
    total_value = initial_amount
    monthly_values = [total_value]
    
    for month in range(months):
        # Dodaj miesięczny zakup
        total_value += monthly_purchase
        # Zastosuj miesięczny wzrost
        total_value *= (1 + annual_growth_rate / 12)
        monthly_values.append(total_value)
    
    return monthly_values

def format_eur(value):
    """Ulepszony formatter EUR"""
    if isinstance(value, (int, float)):
        if value >= 1000000:
            return f"{value/1000000:.1f}M €"
        elif value >= 1000:
            return f"{int(value):,} €".replace(",", " ")
        else:
            return f"{int(value)} €"
    return "0 €"

def create_risk_indicator(risk_level):
    """Tworzenie wskaźnika ryzyka"""
    risk_colors = {
        "Niskie": "#27AE60",
        "Umiarkowane": "#F39C12", 
        "Wysokie": "#E74C3C"
    }
    
    return f"""
    <div style="display: inline-block; background: {risk_colors.get(risk_level, '#95A5A6')}; 
                color: white; padding: 4px 12px; border-radius: 20px; 
                font-size: 12px; font-weight: bold;">
        {risk_level}
    </div>
    """

# Ładowanie strategii
strategies = load_strategies()

# Główny interfejs
st.title("🏆 Kalkulator Strategii Fifty/Fifty")
st.markdown("**Zaawansowana optymalizacja alokacji aktywów w metale szlachetne i strategiczne**")

# Dodanie przełącznika motywu (placeholder)
col1, col2, col3 = st.columns([6, 1, 1])
with col2:
    theme_toggle = st.toggle("🌙 Ciemny motyw", disabled=True, help="Wkrótce dostępne")
with col3:
    if st.button("💾 Zapisz", help="Zapisz aktualną konfigurację"):
        st.info("Funkcja zapisu zostanie wkrótce dodana")

# Sidebar z ulepszoną konfiguracją
with st.sidebar:
    st.header("⚙️ Konfiguracja STRATEGII")
    
    # Wybór strategii z lepszą wizualizacją
    strategy_names = [s["name"] for s in strategies]
    strategy_index = st.selectbox(
        "Wybierz strategię:",
        options=list(range(len(strategies))),
        format_func=lambda i: f"{strategy_names[i]} ({strategies[i]['risk_level']})",
        index=2
    )
    
    current_strategy = strategies[strategy_index]
    
    # Karta strategii z ryzykiem
    st.markdown(f"""
    <div class="strategy-card">
        <h2>{current_strategy['name']} {create_risk_indicator(current_strategy['risk_level'])}</h2>
        <p style="color: #666; font-style: italic;">{current_strategy['description']}</p>
        <p><strong>Złożoność:</strong> {current_strategy['complexity']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Kwota z validation
    st.subheader("💰 Kwota alokacji")
    
    # Dodanie predefiniowanych kwot
    quick_amounts = {
        "5K": 5000,
        "10K": 10000, 
        "25K": 25000,
        "50K": 50000,
        "100K": 100000,
        "Custom": None
    }
    
    amount_choice = st.radio(
        "Szybki wybór:",
        options=list(quick_amounts.keys()),
        horizontal=True,
        index=len(quick_amounts)-1  # Default to Custom
    )
    
    if amount_choice != "Custom" and quick_amounts[amount_choice]:
        if current_strategy["minValue"] <= quick_amounts[amount_choice] <= current_strategy["maxValue"]:
            amount = quick_amounts[amount_choice]
        else:
            st.warning(f"Kwota {amount_choice} nie mieści się w zakresie strategii {current_strategy['name']}")
            amount = int((current_strategy["minValue"] + current_strategy["maxValue"]) / 2)
    else:
        amount = st.slider(
            "Lub ustaw dokładną kwotę:",
            min_value=current_strategy["minValue"],
            max_value=current_strategy["maxValue"],
            value=int((current_strategy["minValue"] + current_strategy["maxValue"]) / 2),
            step=current_strategy["step"],
            help=f"Zakres dla strategii {current_strategy['name']}: {format_eur(current_strategy['minValue'])} - {format_eur(current_strategy['maxValue'])}"
        )
    
    # Metryka z lepszym stylem
    st.markdown(f"""
    <div class="metric-container">
        <h3 style="margin: 0;">Kwota inwestycji</h3>
        <h2 style="margin: 0;">{format_eur(amount)}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Reszta konfiguracji...
    st.subheader("📈 Efekt Kursu Średniego")
    
    purchase = st.slider(
        "Kwota tygodniowa:",
        min_value=current_strategy["minPurchase"],
        max_value=current_strategy["maxPurchase"],
        value=int((current_strategy["minPurchase"] + current_strategy["maxPurchase"]) / 2),
        step=int(current_strategy["minPurchase"] / 2)
    )
    
    st.markdown(f"""
    <div class="metric-container">
        <h4 style="margin: 0;">Tygodniowo: {format_eur(purchase)}</h4>
        <p style="margin: 0;">Rocznie: {format_eur(purchase * 52)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Perspektywa czasowa z projekcją
    st.subheader("⏱️ Perspektywa czasowa")
    years_value = st.slider(
        "Horyzont inwestycyjny:",
        min_value=current_strategy["minYears"],
        max_value=current_strategy["maxYears"],
        value=20
    )
    
    # Dodanie wskaźnika rocznej stopy zwrotu
    expected_return = st.slider(
        "Oczekiwana stopa zwrotu (rocznie):",
        min_value=0.0,
        max_value=15.0,
        value=5.0,
        step=0.5,
        format="%.1f%%",
        help="Historyczne średnie zwroty z metali szlachetnych"
    )

# Główna zawartość z nowymi funkcjami
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Alokacja metali", 
    "🏗️ Struktura komponentów", 
    "📋 Taryfy depozytowe",
    "📈 Projekcja wzrostu",
    "⚖️ Porównanie strategii"
])

# Zakładka projekcji wzrostu (nowa)
with tab4:
    st.header("📈 Projekcja wzrostu inwestycji")
    
    # Obliczenia projekcji
    projection_values = calculate_projection(amount, purchase, years_value, expected_return/100)
    months = list(range(len(projection_values)))
    dates = [datetime.now() + timedelta(days=30*i) for i in months]
    
    # Wykres projekcji
    fig = go.Figure()
    
    # Dodaj linię projekcji
    fig.add_trace(go.Scatter(
        x=dates,
        y=projection_values,
        mode='lines',
        name='Projekcja wartości',
        line=dict(color='#2F80ED', width=3),
        fill='tonexty'
    ))
    
    # Dodaj punkty kluczowe
    key_points = [0, len(projection_values)//4, len(projection_values)//2, len(projection_values)-1]
    fig.add_trace(go.Scatter(
        x=[dates[i] for i in key_points],
        y=[projection_values[i] for i in key_points],
        mode='markers+text',
        name='Punkty kontrolne',
        text=[format_eur(projection_values[i]) for i in key_points],
        textposition="top center",
        marker=dict(size=10, color='#E74C3C')
    ))
    
    fig.update_layout(
        title=f"Projekcja wzrostu przy {expected_return}% rocznej stopie zwrotu",
        xaxis_title="Data",
        yaxis_title="Wartość portfela (EUR)",
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Podsumowanie projekcji
    final_value = projection_values[-1]
    total_invested = amount + (purchase * 52 * years_value)
    profit = final_value - total_invested
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Wartość końcowa", format_eur(final_value))
    with col2:
        st.metric("Łączne inwestycje", format_eur(total_invested))
    with col3:
        st.metric("Zysk", format_eur(profit), delta=f"{(profit/total_invested)*100:.1f}%")
    with col4:
        st.metric("ROI", f"{(profit/total_invested)*100:.1f}%")

# Porównanie strategii (nowa zakładka)
with tab5:
    st.header("⚖️ Porównanie strategii")
    
    # Wybór strategii do porównania
    compare_strategies = st.multiselect(
        "Wybierz strategie do porównania:",
        options=strategy_names,
        default=[current_strategy["name"]],
        max_selections=3
    )
    
    if len(compare_strategies) > 1:
        # Tabela porównawcza
        comparison_data = []
        for strategy_name in compare_strategies:
            strategy = next(s for s in strategies if s["name"] == strategy_name)
            
            # Oblicz dla środkowej wartości zakresu
            mid_amount = (strategy["minValue"] + strategy["maxValue"]) / 2
            mid_purchase = (strategy["minPurchase"] + strategy["maxPurchase"]) / 2
            
            projection = calculate_projection(mid_amount, mid_purchase, 20, expected_return/100)
            final_value = projection[-1]
            total_invested = mid_amount + (mid_purchase * 52 * 20)
            roi = ((final_value - total_invested) / total_invested) * 100
            
            comparison_data.append({
                "Strategia": strategy_name,
                "Zakres inwestycji": f"{format_eur(strategy['minValue'])} - {format_eur(strategy['maxValue'])}",
                "Ryzyko": strategy["risk_level"],
                "Min. horyzont": f"{strategy['minYears']} lat",
                "Proj. ROI (20 lat)": f"{roi:.1f}%",
                "Złożoność": strategy["complexity"]
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
        # Wykres porównawczy ROI
        fig = px.bar(
            comparison_df,
            x="Strategia",
            y="Proj. ROI (20 lat)",
            color="Ryzyko",
            title="Porównanie prognozowanego ROI"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Wybierz co najmniej 2 strategie do porównania")

# Dodanie alertów i powiadomień
if amount < current_strategy["minValue"] * 1.1:
    st.warning("⚠️ Rozważ zwiększenie kwoty inwestycji dla lepszej dywersyfikacji")

if purchase * 52 > amount * 0.5:
    st.warning("⚠️ Regularne dokupienia stanowią ponad 50% początkowej inwestycji - rozważ zwiększenie kwoty startowej")

# Ulepszona stopka z dodatkowymi informacjami
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; background: #F8F9FA; border-radius: 10px;">
    <h4>📊 Kalkulator Strategii Fifty/Fifty v2.0</h4>
    <p style="color: #666; margin: 10px 0;">
        ⚠️ <strong>ZASTRZEŻENIE:</strong> Ten kalkulator służy wyłącznie celom edukacyjnym i prezentuje przykładowe strategie inwestycyjne. 
        Nie stanowi porady finansowej. Wszystkie prognozy są orientacyjne i oparte na założeniach historycznych.
    </p>
    <div style="margin-top: 15px;">
        <a href="https://bit.ly/m/wozniak" target="_blank" style="background: #2F80ED; color: white; padding: 8px 16px; border-radius: 5px; text-decoration: none;">
            📞 Kontakt z doradcą
        </a>
    </div>
    <p style="color: #999; font-size: 12px; margin-top: 10px;">
        Ostatnia aktualizacja: {datetime.now().strftime("%d.%m.%Y")} | 
        Made with ❤️ using Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
