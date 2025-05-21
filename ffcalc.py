import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import locale
from decimal import Decimal

# Niestandardowa funkcja formatowania walut (nie wymaga locale)
def format_eur(value):
    if isinstance(value, (int, float, Decimal)):
        # Formatowanie liczby z separatorem tysięcy i symbolem waluty
        return f"{int(value):,} €".replace(",", " ")
    return f"0 €"

# Konfiguracja strony
st.set_page_config(page_title="Kalkulator Strategii Fifty/Fifty", layout="wide")

# Usuń próbę ustawienia locale
# locale.setlocale(locale.LC_ALL, 'pl_PL') <- USUŃ TĘ LINIĘ

# Tytuł i opis
st.title("Kalkulator Strategii Fifty/Fifty")
st.markdown("Optymalizacja alokacji aktywów w metale szlachetne i strategiczne")

# Reszta kodu pozostaje bez zmian...

# Definicja strategii
strategies = [
    {
        "name": "START",
        "minValue": 5000,
        "maxValue": 9999,
        "description": "Fundamentalny pierwszy krok w budowaniu trwałego, materialnego majątku zabezpieczonego przed inflacją",
        "minPurchase": 100,
        "maxPurchase": 1000,
        "minYears": 7,
        "maxYears": 30,
        "yearsDescription": "Horyzont czasowy 7-30+ lat stanowi perspektywę dla budowy solidnych podstaw majątkowych",
        "step": 250
    },
    {
        "name": "BALANCE",
        "minValue": 10000,
        "maxValue": 99999,
        "description": "Zaawansowana dywersyfikacja majątku poprzez zrównoważoną alokację kapitału między różne klasy metali",
        "minPurchase": 250,
        "maxPurchase": 2500,
        "minYears": 7,
        "maxYears": 30,
        "yearsDescription": "Perspektywa 7-30+ lat to początek drogi ku stworzeniu trwałego majątku rodzinnego",
        "step": 500
    },
    {
        "name": "FOUNDATION",
        "minValue": 100000,
        "maxValue": 699999,
        "description": "Kompleksowe rozwiązanie dla budowania solidnego fundamentu majątkowego opartego na materialnych aktywach",
        "minPurchase": 500,
        "maxPurchase": 5000,
        "minYears": 15,
        "maxYears": 30,
        "yearsDescription": "Horyzont 15-30+ lat to optymalny okres dla ukazania pełnego potencjału strategii",
        "step": 5000
    },
    {
        "name": "OPTIMAL",
        "minValue": 700000,
        "maxValue": 2099999,
        "description": "Zaawansowane rozwiązanie dla tworzenia znaczącego majątku materialnego o najwyższym stopniu odporności",
        "minPurchase": 1000,
        "maxPurchase": 20000,
        "minYears": 15,
        "maxYears": 30,
        "yearsDescription": "Perspektywa 15-30+ lat stanowi ramę czasową dla strategicznego rozwoju portfela",
        "step": 10000
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
        "step": 25000
    }
]

# Informacje o taryfach depozytowych
deposit_tariffs = {
    "START": [
        {
            "name": "GTS",
            "minValue": 5000,
            "maxValue": 9999,
            "agio": "3,5% kwoty aktywacji",
            "metals": "40% złoto, 20% srebro, 20% platyna, 20% pallad",
            "storage": "1,5% netto + VAT rocznie",
            "advantages": ["Niski próg wejścia", "Prostota zarządzania", "Ekspozycja na podstawowe metale szlachetne", "Zakupy dodatkowe bez AGIO"],
            "details": "Zakupy dodatkowe: 100-1.000 EUR/tydzień bez AGIO"
        }
    ],
    # Reszta definicji taryf...
    # (Dodaj pozostałe taryfy z oryginalnego kodu)
}

# Sidebar z konfiguracją strategii
with st.sidebar:
    st.header("Konfiguracja Strategii")
    
    # Wybór strategii
    strategy_names = [s["name"] for s in strategies]
    strategy_index = st.select_slider(
        "Wybierz strategię:",
        options=list(range(len(strategies))),
        format_func=lambda i: strategy_names[i]
    )
    
    current_strategy = strategies[strategy_index]
    st.markdown(f"**{current_strategy['name']}**")
    st.markdown(f"*{current_strategy['description']}*")
    
    # Kwota alokacji - bez niestandardowej funkcji formatującej
    amount = st.slider(
        "Kwota alokacji (EUR):",
        min_value=current_strategy["minValue"],
        max_value=current_strategy["maxValue"],
        value=int((current_strategy["minValue"] + current_strategy["maxValue"]) / 2),
        step=current_strategy["step"]
    )

    # Wyświetl sformatowaną wartość poniżej suwaka
    st.write(f"Wybrana kwota: {format_eur(amount)}")
    
    # Efekt Kursu Średniego
    purchase = st.slider(
        "Efekt Kursu Średniego (EUR/tydzień):",
        min_value=current_strategy["minPurchase"],
        max_value=current_strategy["maxPurchase"],
        value=int((current_strategy["minPurchase"] + current_strategy["maxPurchase"]) / 2),
        step=int(current_strategy["minPurchase"] / 2),
        format=format_eur
    )
    
    # Perspektywa czasowa
    years_value = st.slider(
        "Perspektywa budowy fundamentu (lata):",
        min_value=current_strategy["minYears"],
        max_value=current_strategy["maxYears"],
        value=20
    )
    
    years_display = "30+" if years_value >= 30 else str(years_value)
    st.markdown(f"*{current_strategy['yearsDescription']}*")

# Funkcje pomocnicze
def get_metals(strategy_name, amount):
    if strategy_name == "START":
        return [
            {"name": "Złoto", "value": 40, "amount": amount * 0.4, "color": "#FFD700"},
            {"name": "Srebro", "value": 20, "amount": amount * 0.2, "color": "#C0C0C0"},
            {"name": "Platyna", "value": 20, "amount": amount * 0.2, "color": "#E5E4E2"},
            {"name": "Pallad", "value": 20, "amount": amount * 0.2, "color": "#B9F2FF"}
        ]
    elif strategy_name == "BALANCE":
        return [
            {"name": "Złoto", "value": 45, "amount": amount * 0.45, "color": "#FFD700"},
            {"name": "Srebro", "value": 35, "amount": amount * 0.35, "color": "#C0C0C0"},
            {"name": "Platyna", "value": 10, "amount": amount * 0.1, "color": "#E5E4E2"},
            {"name": "Pallad", "value": 10, "amount": amount * 0.1, "color": "#B9F2FF"}
        ]
    elif strategy_name in ["FOUNDATION", "OPTIMAL"]:
        return [
            {"name": "Złoto", "value": 35, "amount": amount * 0.35, "color": "#FFD700"},
            {"name": "Srebro", "value": 30, "amount": amount * 0.3, "color": "#C0C0C0"},
            {"name": "Platyna", "value": 5, "amount": amount * 0.05, "color": "#E5E4E2"},
            {"name": "Pallad", "value": 5, "amount": amount * 0.05, "color": "#B9F2FF"},
            {"name": "Hafn", "value": 5, "amount": amount * 0.05, "color": "#A9A9A9"},
            {"name": "Gal", "value": 5, "amount": amount * 0.05, "color": "#6495ED"},
            {"name": "Ind", "value": 5, "amount": amount * 0.05, "color": "#9370DB"},
            {"name": "German", "value": 5, "amount": amount * 0.05, "color": "#808080"},
            {"name": "Tantal", "value": 5, "amount": amount * 0.05, "color": "#708090"}
        ]
    else:  # PRESTIGE
        return [
            {"name": "Złoto", "value": 25, "amount": amount * 0.25, "color": "#FFD700"},
            {"name": "Srebro", "value": 20, "amount": amount * 0.2, "color": "#C0C0C0"},
            {"name": "Platyna", "value": 5, "amount": amount * 0.05, "color": "#E5E4E2"},
            {"name": "Pallad", "value": 5, "amount": amount * 0.05, "color": "#B9F2FF"},
            {"name": "Metale Strategiczne", "value": 40, "amount": amount * 0.4, "color": "#4169E1"},
            {"name": "Hafn", "value": 1, "amount": amount * 0.01, "color": "#A9A9A9"},
            {"name": "Gal", "value": 1, "amount": amount * 0.01, "color": "#6495ED"},
            {"name": "Ind", "value": 1, "amount": amount * 0.01, "color": "#9370DB"},
            {"name": "German", "value": 1, "amount": amount * 0.01, "color": "#808080"},
            {"name": "Tantal", "value": 1, "amount": amount * 0.01, "color": "#708090"}
        ]

def get_components(strategy_name, amount):
    if strategy_name == "START":
        return [
            {"name": "GTS (SSW)", "value": 100, "amount": amount, "color": "#FFD700"}
        ]
    elif strategy_name in ["BALANCE", "FOUNDATION", "OPTIMAL"]:
        return [
            {"name": "START" == strategy_name and "GTS (SSW)" or "GT (SSW)", "value": 50, "amount": amount * 0.5, "color": "#FFD700"},
            {"name": "GR (Auvesta)", "value": 50, "amount": amount * 0.5, "color": "#C0C0C0"}
        ]
    else:  # PRESTIGE
        return [
            {"name": "GTS (SSW)", "value": 10, "amount": amount * 0.1, "color": "#FFD700"},
            {"name": "GT (SSW)", "value": 20, "amount": amount * 0.2, "color": "#E5E4E2"},
            {"name": "GR (Auvesta)", "value": 30, "amount": amount * 0.3, "color": "#C0C0C0"},
            {"name": "SMH (SSW)", "value": 40, "amount": amount * 0.4, "color": "#6495ED"}
        ]

def get_agio(strategy_name, amount):
    initial_agio = 0
    bonus = 0
    
    if strategy_name == "START":
        initial_agio = amount * 0.035  # 3.5%
    elif strategy_name in ["BALANCE", "FOUNDATION", "OPTIMAL"]:
        ssw_agio = amount * 0.5 * 0.035  # 3.5% dla SSW
        auvesta_agio = 0
        
        auvesta_amount = amount * 0.5
        if auvesta_amount < 15000:
            auvesta_agio = 300  # S-3
        elif auvesta_amount < 25000:
            auvesta_agio = 600  # M-6
        elif auvesta_amount < 50000:
            auvesta_agio = 1200  # L-12
        elif auvesta_amount < 150000:
            auvesta_agio = 2400  # XL-24
        else:
            vip_count = min(6, round(auvesta_amount / 150000))
            auvesta_agio = vip_count * 2400  # VIP
        
        initial_agio = ssw_agio + auvesta_agio
        bonus = auvesta_agio  # 100% zwrotu
    else:  # PRESTIGE
        gts_agio = amount * 0.1 * 0.035
        gt_agio = amount * 0.2 * 0.035
        gr_amount = amount * 0.3
        gr_count = min(6, round(gr_amount / 150000))
        gr_agio = gr_count * 2400
        
        initial_agio = gts_agio + gt_agio + gr_agio
        bonus = gr_agio
    
    effective_agio = initial_agio - bonus
    initial_percent = (initial_agio / amount) * 100 if amount > 0 else 0
    effective_percent = (effective_agio / amount) * 100 if amount > 0 else 0
    
    return {
        "initialAgio": initial_agio,
        "bonus": bonus,
        "effectiveAgio": effective_agio,
        "initialPercent": initial_percent,
        "effectivePercent": effective_percent
    }

# Główne zakładki
tab1, tab2, tab3 = st.tabs(["Alokacja metali", "Struktura komponentów", "Taryfy depozytowe"])

with tab1:
    st.header("Alokacja według metali")
    
    metals = get_metals(current_strategy["name"], amount)
    
    # Przygotowanie danych do wykresu
    metals_df = pd.DataFrame(metals)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            metals_df, 
            values='value', 
            names='name',
            color='name',
            color_discrete_map={m["name"]: m["color"] for m in metals},
            hole=0.3
        )
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.dataframe(
            pd.DataFrame({
                "Metal": [m["name"] for m in metals],
                "Alokacja (%)": [f"{m['value']}%" for m in metals],
                "Kwota (EUR)": [format_eur(m["amount"]) for m in metals]
            }),
            hide_index=True,
            use_container_width=True
        )

with tab2:
    st.header("Struktura komponentów")
    
    components = get_components(current_strategy["name"], amount)
    
    # Przygotowanie danych do wykresu
    components_df = pd.DataFrame(components)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.pie(
            components_df, 
            values='value', 
            names='name',
            color='name',
            color_discrete_map={c["name"]: c["color"] for c in components},
            hole=0.3
        )
        fig.update_traces(textinfo='percent+label')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.dataframe(
            pd.DataFrame({
                "Komponent": [c["name"] for c in components],
                "Alokacja (%)": [f"{c['value']}%" for c in components],
                "Kwota (EUR)": [format_eur(c["amount"]) for c in components]
            }),
            hide_index=True,
            use_container_width=True
        )

with tab3:
    st.header(f"Taryfy depozytowe dla strategii {current_strategy['name']}")
    
    if current_strategy["name"] in deposit_tariffs:
        for tariff in deposit_tariffs[current_strategy["name"]]:
            with st.expander(
                f"{tariff['name']} ({format_eur(tariff['minValue'])} - {format_eur(tariff['maxValue'])})",
                expanded=tariff['minValue'] <= amount <= tariff['maxValue']
            ):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**AGIO:**")
                    st.markdown(tariff["agio"])
                    
                    st.markdown("**Koszty magazynowania:**")
                    st.markdown(tariff["storage"])
                
                with col2:
                    st.markdown("**Alokacja metali:**")
                    st.markdown(tariff["metals"])
                
                st.markdown("**Zalety:**")
                for advantage in tariff["advantages"]:
                    st.markdown(f"- {advantage}")
                
                st.markdown("**Szczegóły:**")
                st.markdown(f"_{tariff['details']}_")

# Koszty AGIO i Rekomendacje
col1, col2 = st.columns(2)

with col1:
    st.header("Koszty AGIO")
    
    agio = get_agio(current_strategy["name"], amount)
    
    st.subheader("Koszt początkowy:")
    st.metric(
        label=f"{agio['initialPercent']:.2f}%",
        value=format_eur(agio["initialAgio"])
    )
    
    st.subheader("Koszt efektywny (po bonusach):")
    st.metric(
        label=f"{agio['effectivePercent']:.2f}%",
        value=format_eur(agio["effectiveAgio"]),
        delta=f"-{format_eur(agio['bonus'])}" if agio["bonus"] > 0 else None
    )
    
    if agio["bonus"] > 0:
        st.info(f"Bonus: {format_eur(agio['bonus'])} zwracane w postaci dodatkowych metali")

with col2:
    st.header("Projekcja i rekomendacja")
    
    # Znajdowanie odpowiedniej taryfy
    current_tariff = None
    if current_strategy["name"] in deposit_tariffs:
        for tariff in deposit_tariffs[current_strategy["name"]]:
            if tariff["minValue"] <= amount <= tariff["maxValue"]:
                current_tariff = tariff
                break
    
    metrics = [
        ("Rekomendowany depozyt", current_tariff["name"] if current_tariff else "Brak dopasowania"),
        ("Efektywne AGIO", f"{agio['effectivePercent']:.2f}%"),
        ("Rekomendacja Efektu Kursu Średniego", f"{format_eur(purchase)}/tydzień"),
        ("Roczna kwota dokupów", format_eur(purchase * 52)),
        ("Perspektywa budowy", f"{years_display} lat"),
        ("Szacowana suma po {years_display} latach", format_eur(round(amount + (purchase * 52 * min(years_value, 30)))))
    ]
    
    for label, value in metrics:
        st.metric(label=label, value=value)

# Podsumowanie
st.header(f"Podsumowanie strategii {current_strategy['name']}")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:
    st.metric(
        label="Kwota aktywacji",
        value=format_eur(round(amount + agio["initialAgio"])),
        delta=f"{format_eur(amount)} + {format_eur(agio['initialAgio'])} AGIO"
    )

with summary_col2:
    st.metric(
        label=f"Szacowana alokacja środków po {years_display} latach",
        value=format_eur(round(amount + (purchase * 52 * min(years_value, 30)))),
        delta=f"Z początkowej alokacji {format_eur(amount)}"
    )

# Stopka
st.markdown("---")
st.markdown("© 2025 Kalkulator Strategii Fifty/Fifty - Narzędzie do planowania alokacji w metale | [bit.ly/m/wozniak](https://bit.ly/m/wozniak)")
