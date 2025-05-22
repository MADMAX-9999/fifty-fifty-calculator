import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Ustaw konfigurację strony
st.set_page_config(page_title="Kalkulator Strategii Fifty/Fifty", 
                   layout="wide",
                   initial_sidebar_state="expanded")

# Niestandardowa funkcja formatowania EUR bez użycia locale
def format_eur(value):
    if isinstance(value, (int, float)):
        return f"{int(value):,} €".replace(",", " ")
    return f"0 €"

# Definicja strategii
strategies = [
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
        "step": 250
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
        "step": 500
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
        "step": 5000
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
    "BALANCE": [
        {
            "name": "GTS + GR S-3",
            "minValue": 10000,
            "maxValue": 29999,
            "agio": "3,5% dla SSW + 300 EUR (stała kwota) dla Auvesta",
            "metals": "GTS: 40% złoto, 20% srebro, 20% platyna, 20% pallad | GR: 50% złoto, 50% srebro",
            "storage": "SSW: 1,5% netto + VAT rocznie | Auvesta: 0,08% netto + VAT miesięcznie",
            "advantages": ["Równowaga między dostawcami", "Dywersyfikacja metali", "AGIO w GR zwracane w 100% jako bonus metali", "Zakupy dodatkowe bez AGIO"],
            "details": "Podział 50/50 między SSW (GTS) i Auvesta (GR). Zakupy dodatkowe: 250-2.500 EUR/tydzień bez AGIO."
        },
        {
            "name": "GTS + GR M-6",
            "minValue": 30000,
            "maxValue": 49999,
            "agio": "3,5% dla SSW + 600 EUR (stała kwota) dla Auvesta",
            "metals": "GTS: 40% złoto, 20% srebro, 20% platyna, 20% pallad | GR: 50% złoto, 50% srebro",
            "storage": "SSW: 1,5% netto + VAT rocznie | Auvesta: 0,07% netto + VAT miesięcznie",
            "advantages": ["Równowaga między dostawcami", "Dywersyfikacja metali", "AGIO w GR zwracane w 100% jako bonus metali", "Ceny zakupu metali: 1% taniej od taryfy S-3"],
            "details": "Podział 50/50 między SSW (GTS) i Auvesta (GR). Zakupy dodatkowe: 250-2.500 EUR/tydzień bez AGIO."
        },
        {
            "name": "GTS + GR L-12",
            "minValue": 50000,
            "maxValue": 99999,
            "agio": "3,5% dla SSW + 1.200 EUR (stała kwota) dla Auvesta",
            "metals": "GTS: 40% złoto, 20% srebro, 20% platyna, 20% pallad | GR: 50% złoto, 50% srebro",
            "storage": "SSW: 1,5% netto + VAT rocznie | Auvesta: 0,06% netto + VAT miesięcznie",
            "advantages": ["Równowaga między dostawcami", "Dywersyfikacja metali", "AGIO w GR zwracane w 100% jako bonus metali", "Ceny zakupu metali: 3% taniej od taryfy S-3"],
            "details": "Podział 50/50 między SSW (GTS) i Auvesta (GR). Zakupy dodatkowe: 250-2.500 EUR/tydzień bez AGIO."
        }
    ],
    "FOUNDATION": [
        {
            "name": "GT + GR XL-24",
            "minValue": 100000,
            "maxValue": 299999,
            "agio": "3,5% dla SSW + 2.400 EUR (stała kwota) dla Auvesta",
            "metals": "GT: 20% złoto, 10% srebro, 10% platyna, 10% pallad, 50% metale strategiczne | GR: 50% złoto, 50% srebro",
            "storage": "SSW: 1,5% netto + VAT rocznie | Auvesta: 0,05% netto + VAT miesięcznie",
            "advantages": ["Dostęp do metali strategicznych", "Optymalne koszty magazynowania", "AGIO w GR zwracane w 100% jako bonus metali", "Ceny zakupu metali: 6% taniej od taryfy S-3"],
            "details": "Podział 50/50 między SSW (GT) i Auvesta (GR). Zakupy dodatkowe: 500-5.000 EUR/tydzień bez AGIO."
        },
        {
            "name": "GT + GR VIP",
            "minValue": 300000,
            "maxValue": 699999,
            "agio": "3,5% dla SSW + 2.400 EUR (stała kwota) dla Auvesta",
            "metals": "GT: 20% złoto, 10% srebro, 10% platyna, 10% pallad, 50% metale strategiczne | GR: 50% złoto, 50% srebro",
            "storage": "SSW: 1,5% netto + VAT rocznie | Auvesta: 0,04% netto + VAT miesięcznie",
            "advantages": ["Dostęp do metali strategicznych", "Optymalne koszty magazynowania", "AGIO w GR zwracane w 100% jako bonus metali", "Ceny zakupu metali: 7% taniej od taryfy S-3"],
            "details": "Podział 50/50 między SSW (GT) i Auvesta (GR). Zakupy dodatkowe: 500-5.000 EUR/tydzień bez AGIO."
        }
    ],
    "OPTIMAL": [
        {
            "name": "GT + GR VIP",
            "minValue": 700000,
            "maxValue": 2099999,
            "agio": "3,5% dla SSW + 2.400 EUR za każde 150.000 EUR dla Auvesta",
            "metals": "GT: 20% złoto, 10% srebro, 10% platyna, 10% pallad, 50% metale strategiczne | GR: 50% złoto, 50% srebro",
            "storage": "SSW: 1,5% netto + VAT rocznie | Auvesta: 0,04% netto + VAT miesięcznie",
            "advantages": ["Maksymalna efektywność kosztowa", "Idealna dywersyfikacja", "Dostęp do taryf VIP", "Ceny zakupu metali: 7% taniej od taryfy S-3"],
            "details": "Podział 50/50 między SSW (GT) i Auvesta (GR). Dla kwot powyżej 900.000 EUR zalecany podział na maksymalnie 6 depozytów VIP. Zakupy dodatkowe: 1.000-20.000 EUR/tydzień bez AGIO."
        }
    ],
    "PRESTIGE": [
        {
            "name": "GTS + GT + GR VIP + SMH",
            "minValue": 2100000,
            "maxValue": 5000000,
            "agio": "3,5% dla SSW (GTS, GT) + 2.400 EUR za każde 150.000 EUR dla Auvesta + 0% dla SMH",
            "metals": "Złożony portfel w proporcjach: 10% GTS, 20% GT, 30% GR, 40% SMH",
            "storage": "SSW: 1,5% netto + VAT rocznie | Auvesta: 0,04% netto + VAT miesięcznie",
            "advantages": ["Maksymalna dywersyfikacja", "Dominujący udział metali strategicznych (SMH)", "Najniższe koszty utrzymania", "Dedykowany komponent dla metali strategicznych"],
            "details": "Podział: 10% GTS, 20% GT, 30% GR, 40% SMH. Zakupy dodatkowe: 2.500-50.000 EUR/tydzień bez AGIO."
        }
    ]
}

# Tytuł i opis aplikacji
st.title("Kalkulator Strategii Fifty/Fifty")
st.markdown("Optymalizacja alokacji aktywów w metale szlachetne i strategiczne")

# Sidebar z konfiguracją strategii
with st.sidebar:
    st.header("Konfiguracja Strategii")
    
    # Wybór strategii
    strategy_names = [s["name"] for s in strategies]
    strategy_index = st.select_slider(
        "Wybierz strategię:",
        options=list(range(len(strategies))),
        format_func=lambda i: strategy_names[i],
        value=2  # Domyślnie FOUNDATION
    )
    
    current_strategy = strategies[strategy_index]
    st.markdown(f"**{current_strategy['name']}**")
    st.markdown(f"*{current_strategy['description']}*")
    
    # Kwota alokacji z podziałem na suwak i wyświetlenie wartości
    st.subheader("Kwota alokacji")

    amount = st.slider(
        "Wybierz kwotę:",
        min_value=current_strategy["minValue"],
        max_value=current_strategy["maxValue"],
        value=int((current_strategy["minValue"] + current_strategy["maxValue"]) / 2),
        step=current_strategy["step"]
    )
    st.metric("Kwota", value=format_eur(amount))
  
    
    # Efekt Kursu Średniego
    st.subheader("Efekt Kursu Średniego")
    col1, col2 = st.columns([3, 1])
    with col1:
        purchase = st.slider(
            "Wybierz kwotę tygodniową:",
            min_value=current_strategy["minPurchase"],
            max_value=current_strategy["maxPurchase"],
            value=int((current_strategy["minPurchase"] + current_strategy["maxPurchase"]) / 2),
            step=int(current_strategy["minPurchase"] / 2)
        )
    with col2:
        st.metric("Tygodniowo", value=format_eur(purchase))
    
    st.caption("Regularne dokupienia metali dla optymalizacji średniej ceny zakupu")
    
    # Perspektywa czasowa
    st.subheader("Perspektywa czasowa")
    col1, col2 = st.columns([3, 1])
    with col1:
        years_value = st.slider(
            "Wybierz horyzont czasowy:",
            min_value=current_strategy["minYears"],
            max_value=current_strategy["maxYears"],
            value=20
        )
    with col2:
        years_display = "30+" if years_value >= 30 else str(years_value)
        st.metric("Lat", value=years_display)
    
    st.caption(current_strategy["yearsDescription"])

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
            {"name": "Złoto", "value": 20, "amount": amount * 0.20, "color": "#FFD700"},
            {"name": "Srebro", "value": 16, "amount": amount * 0.16, "color": "#C0C0C0"},
            {"name": "Platyna", "value": 7, "amount": amount * 0.07, "color": "#E5E4E2"},
            {"name": "Pallad", "value": 7, "amount": amount * 0.07, "color": "#B9F2FF"},
            
            {"name": "Hafn", "value": 2, "amount": amount * 0.02, "color": "#A9A9A9"},
            {"name": "Gal", "value": 2, "amount": amount * 0.02, "color": "#6495ED"},
            {"name": "Ind", "value": 2, "amount": amount * 0.02, "color": "#9370DB"},
            {"name": "German", "value": 2, "amount": amount * 0.02, "color": "#808080"},
            {"name": "Tantal", "value": 2, "amount": amount * 0.02, "color": "#708090"},
            {"name": "Metale Strategiczne", "value": 40, "amount": amount * 0.4, "color": "#4169E1"}
        ]

def get_components(strategy_name, amount):
    if strategy_name == "START":
        return [
            {"name": "GTS (SSW)", "value": 100, "amount": amount, "color": "#FFD700"}
        ]
    elif strategy_name in ["BALANCE", "FOUNDATION", "OPTIMAL"]:
        component_name = "GTS (SSW)" if strategy_name == "BALANCE" else "GT (SSW)"
        return [
            {"name": component_name, "value": 50, "amount": amount * 0.5, "color": "#FFD700"},
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
            vip_count = min(6, int(auvesta_amount / 150000) + (1 if auvesta_amount % 150000 > 0 else 0))
            auvesta_agio = vip_count * 2400  # VIP
        
        initial_agio = ssw_agio + auvesta_agio
        bonus = auvesta_agio  # 100% zwrotu
    else:  # PRESTIGE
        gts_agio = amount * 0.1 * 0.035
        gt_agio = amount * 0.2 * 0.035
        gr_amount = amount * 0.3
        gr_count = min(6, int(gr_amount / 150000) + (1 if gr_amount % 150000 > 0 else 0))
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

def get_current_tariff(strategy_name, amount):
    if strategy_name in deposit_tariffs:
        for tariff in deposit_tariffs[strategy_name]:
            if tariff["minValue"] <= amount <= tariff["maxValue"]:
                return tariff
    return None

# Główne zakładki
tab1, tab2, tab3 = st.tabs(["Alokacja metali", "Struktura komponentów", "Taryfy depozytowe"])

with tab1:
    st.header("Alokacja według metali")
    
    metals = get_metals(current_strategy["name"], amount)
    
    # Przygotowanie danych do wykresu
    metals_df = pd.DataFrame(metals)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Wykres kołowy z Plotly
        fig = px.pie(
            metals_df, 
            values='value', 
            names='name',
            color='name',
            color_discrete_map={m["name"]: m["color"] for m in metals},
            hole=0.3
        )
        fig.update_traces(textinfo='percent+label', textfont_size=12)
        fig.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Tabela z danymi
        metals_data = {
            "Metal": [m["name"] for m in metals],
            "Alokacja (%)": [f"{m['value']}%" for m in metals],
            "Kwota": [format_eur(m["amount"]) for m in metals]
        }
        
        metals_table = pd.DataFrame(metals_data)
        
        # Użyj stylu Streamlit do wyświetlenia tabeli
        st.dataframe(
            metals_table,
            column_config={
                "Metal": st.column_config.TextColumn("Metal"),
                "Alokacja (%)": st.column_config.TextColumn("Alokacja (%)"),
                "Kwota": st.column_config.TextColumn("Kwota")
            },
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
        # Wykres kołowy z Plotly
        fig = px.pie(
            components_df, 
            values='value', 
            names='name',
            color='name',
            color_discrete_map={c["name"]: c["color"] for c in components},
            hole=0.3
        )
        fig.update_traces(textinfo='percent+label', textfont_size=12)
        fig.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Tabela z danymi
        components_data = {
            "Komponent": [c["name"] for c in components],
            "Alokacja (%)": [f"{c['value']}%" for c in components],
            "Kwota": [format_eur(c["amount"]) for c in components]
        }
        
        components_table = pd.DataFrame(components_data)
        
        # Użyj stylu Streamlit do wyświetlenia tabeli
        st.dataframe(
            components_table,
            column_config={
                "Komponent": st.column_config.TextColumn("Komponent"),
                "Alokacja (%)": st.column_config.TextColumn("Alokacja (%)"),
                "Kwota": st.column_config.TextColumn("Kwota")
            },
            hide_index=True,
            use_container_width=True
        )

with tab3:
    st.header(f"Taryfy depozytowe dla strategii {current_strategy['name']}")
    
    if current_strategy["name"] in deposit_tariffs:
        for idx, tariff in enumerate(deposit_tariffs[current_strategy["name"]]):
            is_current = tariff["minValue"] <= amount <= tariff["maxValue"]
            
            # Dodaj kolorowe tło dla aktualnie wybranej taryfy
            container_style = "background-color: #E6F3FF; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #0066CC;" if is_current else "background-color: #FFFFFF; padding: 20px; border-radius: 10px; margin-bottom: 20px;"
            
            with st.container():
                st.markdown(f'<div style="{container_style}">', unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.subheader(tariff["name"])
                    st.markdown(f"Kwota: {format_eur(tariff['minValue'])} - {format_eur(tariff['maxValue'])}")
                
                with col2:
                    if is_current:
                        st.success("✓ Dostępna dla aktualnej kwoty")
                    else:
                        st.info("Poza aktualnym zakresem")
                
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
                advantages_text = "".join([f"- {advantage}<br>" for advantage in tariff["advantages"]])
                st.markdown(advantages_text, unsafe_allow_html=True)
                
                st.markdown("**Szczegóły:**")
                st.info(tariff["details"])
                
                st.markdown('</div>', unsafe_allow_html=True)

# Obliczenia
agio = get_agio(current_strategy["name"], amount)
current_tariff = get_current_tariff(current_strategy["name"], amount)

# Koszty AGIO i Rekomendacje
st.header("Podsumowanie strategii")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Koszty AGIO")
    
    # Ramka początkowego AGIO
    st.markdown(
        f'''
        <div style="background-color: #FFF9E6; padding: 15px; border-radius: 10px; border-left: 4px solid #F2C94C;">
            <h4 style="margin-top: 0;">Koszt początkowy:</h4>
            <p style="font-size: 24px; font-weight: bold;">{agio["initialPercent"]:.2f}% ({format_eur(agio["initialAgio"])})</p>
        </div>
        ''', 
        unsafe_allow_html=True
    )
    
    # Ramka efektywnego AGIO
    st.markdown(
        f'''
        <div style="background-color: #E6F9E8; padding: 15px; border-radius: 10px; border-left: 4px solid #27AE60; margin-top: 15px;">
            <h4 style="margin-top: 0;">Koszt efektywny (po bonusach):</h4>
            <p style="font-size: 24px; font-weight: bold; color: #27AE60;">{agio["effectivePercent"]:.2f}% ({format_eur(agio["effectiveAgio"])})</p>
            {f'<p style="margin-top: 10px; font-size: 14px; color: #219653;"><span style="font-weight: bold;">Bonus:</span> {format_eur(agio["bonus"])} zwracane w postaci dodatkowych metali</p>' if agio["bonus"] > 0 else ''}
        </div>
        ''', 
        unsafe_allow_html=True
    )

with col2:
    st.subheader("Projekcja i rekomendacja")
    
    # Ramka z rekomendacjami
    st.markdown(
        f'''
        <div style="background-color: #E6F0FF; padding: 15px; border-radius: 10px; border-left: 4px solid #2F80ED;">
            <ul style="list-style-type: none; padding-left: 0; margin-top: 0;">
                <li style="margin-bottom: 10px;"><span style="font-weight: bold;">Rekomendowany depozyt:</span> <span style="color: #2F80ED; font-weight: 500;">{current_tariff["name"] if current_tariff else "Brak dopasowania"}</span></li>
                <li style="margin-bottom: 10px;"><span style="font-weight: bold;">Efektywne AGIO:</span> <span style="color: #27AE60;">{agio["effectivePercent"]:.2f}%</span></li>
                <li style="margin-bottom: 10px;"><span style="font-weight: bold;">Rekomendacja Efektu Kursu Średniego:</span> <span style="font-weight: 500;">{format_eur(purchase)}/tydzień</span></li>
                <li style="margin-bottom: 10px;"><span style="font-weight: bold;">Roczna kwota dokupów:</span> <span style="font-weight: 500;">{format_eur(purchase * 52)}</span></li>
                <li style="margin-bottom: 10px;"><span style="font-weight: bold;">Perspektywa budowy:</span> <span style="font-weight: 500;">{years_display} lat</span></li>
                <li><span style="font-weight: bold;">Szacowana suma po {years_display} latach:</span> <span style="color: #2F80ED; font-weight: bold;">{format_eur(round(amount + (purchase * 52 * min(years_value, 30))))}</span></li>
            </ul>
        </div>
        ''', 
        unsafe_allow_html=True
    )

# Podsumowanie
st.markdown(
    f'''
    <div style="background-color: #2F80ED; color: white; padding: 20px; border-radius: 10px; margin-top: 30px; text-align: center;">
        <h2 style="margin-top: 0; margin-bottom: 15px; font-weight: 600;">Podsumowanie strategii {current_strategy["name"]}</h2>
        <div style="margin-bottom: 15px;">
            <span style="font-weight: 500;">Kwota aktywacji:</span>
            <span style="font-weight: 700; font-size: 18px;">{format_eur(round(amount + agio["initialAgio"]))}</span>
            <span style="font-size: 14px; margin-left: 10px;">({format_eur(amount)} + {format_eur(agio["initialAgio"])} AGIO)</span>
        </div>
        <div>
            <p>Szacowana alokacja środków po {years_display} latach: <span style="font-weight: 700; font-size: 24px;">{format_eur(round(amount + (purchase * 52 * min(years_value, 30))))}</span></p>
            <p style="font-size: 14px; margin-top: 5px;">Z początkowej alokacji {format_eur(amount)} i tygodniowych dokupień w wysokości {format_eur(purchase)}</p>
        </div>
    </div>
    ''', 
    unsafe_allow_html=True
)

# Stopka
st.markdown("---")
st.markdown(
    '''
    <div style="text-align: center; color: #666; font-size: 14px;">
        ⚠️ ZASTRZEŻENIE: Ten kalkulator służy wyłącznie celom edukacyjnym i prezentuje przykładowe strategie rozwiązań. 
        Nie stanowi porady ani doradztwa inwestycyjnego w rozumieniu prawa. 
        © 2025 Kalkulator Strategii Fifty/Fifty - Narzędzie do planowania alokacji w metale | 
        <a href="https://bit.ly/m/wozniak" target="_blank" style="color: #2F80ED;">bit.ly/m/wozniak</a>
    </div>
    ''', 
    unsafe_allow_html=True
)
