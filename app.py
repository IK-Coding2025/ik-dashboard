import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def create_dashboard_plot(dashboard_name, selected_indicators, filtered_df):
    if selected_indicators:
        fig = go.Figure()
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

        # Trennen der Indikatoren in normale und Index-Indikatoren
        selected_normal = [ind for ind in selected_indicators if 'Index_' not in ind]
        selected_index = [ind for ind in selected_indicators if 'Index_' in ind]

        # Normale Indikatoren auf der linken Y-Achse (nur für Konjunktur/Arbeitsmarkt)
        if dashboard_name == "Rohstoffe":
            # Nur die Index-Indikatoren für das Rohstoffe-Dashboard anzeigen
            for i, indicator in enumerate(selected_index):
                fig.add_trace(go.Scatter(
                    x=filtered_df['Zeitachse'],
                    y=filtered_df[indicator],
                    name=indicator,
                    yaxis='y1',  # Alle Indikatoren auf der linken Y-Achse
                    mode='lines+markers',
                    line=dict(color=colors[i])
                ))

            # Layout für Rohstoffe (nur eine Y-Achse auf der linken Seite)
            fig.update_layout(
                title=f"Entwicklung ({dashboard_name})",
                xaxis=dict(
                    title="Zeitraum",
                    titlefont=dict(color="#000000"),
                    tickfont=dict(color="#000000"),
                    tickangle=45
                ),
                yaxis=dict(
                    title="Index-Werte",  # Beschriftung der linken Y-Achse
                    titlefont=dict(color="#000000"),
                    tickfont=dict(color="#000000"),
                    tickformat=',',
                    separatethousands=True,
                    rangemode='tozero'
                ),
                height=400,
                template="plotly_white",
                showlegend=True,
                margin=dict(l=40, r=40, t=40, b=80)
            )

        # Für das Dashboard "Index": Nur die Index-Indikatoren auf der rechten Y-Achse
        elif dashboard_name == "Index":
            for i, indicator in enumerate(selected_index):
                fig.add_trace(go.Scatter(
                    x=filtered_df['Zeitachse'],
                    y=filtered_df[indicator],
                    name=indicator,
                    yaxis='y2',  # Index-Indikatoren auf der rechten Y-Achse
                    mode='lines+markers',
                    line=dict(color=colors[i])
                ))

            # Layout für Index-Dashboard (mit rechter Y-Achse)
            fig.update_layout(
                title=f"Entwicklung ({dashboard_name})",
                xaxis=dict(
                    title="Zeitraum",
                    titlefont=dict(color="#000000"),
                    tickfont=dict(color="#000000"),
                    tickangle=45
                ),
                yaxis=dict(
                    title=None,  # Keine Beschriftung auf der linken Achse für Index-Dashboard
                    titlefont=dict(color="#000000"),
                    tickfont=dict(color="#000000"),
                    tickformat=',',
                    separatethousands=True,
                    rangemode='tozero'
                ),
                yaxis2=dict(
                    title="Index-Wert",  # Index-Wert für die rechte Y-Achse
                    titlefont=dict(color="#000000"),
                    tickfont=dict(color="#000000"),
                    overlaying="y",
                    side="right",
                    type='linear',
                    tickformat=',',
                    separatethousands=True,
                    rangemode='tozero'
                ),
                height=400,
                template="plotly_white",
                showlegend=True,
                margin=dict(l=40, r=40, t=40, b=80)
            )

        # Für andere Dashboards (z.B. Konjunktur, Arbeitsmarkt)
        else:
            # Normale Indikatoren auf der linken Y-Achse
            for i, indicator in enumerate(selected_normal):
                fig.add_trace(go.Scatter(
                    x=filtered_df['Zeitachse'],
                    y=filtered_df[indicator],
                    name=indicator,
                    yaxis='y1',
                    mode='lines+markers',
                    line=dict(color=colors[i])
                ))

            # Index-Indikatoren auf der rechten Y-Achse (nur für Dashboards mit Index-Indikatoren)
            for i, indicator in enumerate(selected_index):
                fig.add_trace(go.Scatter(
                    x=filtered_df['Zeitachse'],
                    y=filtered_df[indicator],
                    name=indicator,
                    yaxis='y2',
                    mode='lines+markers',
                    line=dict(color=colors[i + len(selected_normal)])
                ))

            # Layout anpassen für alle anderen Dashboards
            fig.update_layout(
                title=f"Entwicklung ({dashboard_name})",
                xaxis=dict(
                    title="Zeitraum",
                    titlefont=dict(color="#000000"),
                    tickfont=dict(color="#000000"),
                    tickangle=45
                ),
                yaxis=dict(
                    title="Absolute Werte (Nicht-Index Indikatoren)" if selected_normal else None,
                    titlefont=dict(color="#000000"),
                    tickfont=dict(color="#000000"),
                    tickformat=',',
                    separatethousands=True,
                    rangemode='tozero'
                ),
                yaxis2=dict(
                    title="Index-Wert" if selected_index else None,
                    titlefont=dict(color="#000000"),
                    tickfont=dict(color="#000000"),
                    overlaying="y",
                    side="right",
                    type='linear',
                    tickformat=',',
                    separatethousands=True,
                    rangemode='tozero'
                ) if selected_index else None,
                height=400,
                template="plotly_white",
                showlegend=True,
                margin=dict(l=40, r=40, t=40, b=80)
            )

        # Plot anzeigen
        st.plotly_chart(fig, use_container_width=True)

        # Lesebeispiel einfügen
        if dashboard_name == "Konjunktur":
            st.markdown("""
            ### Lesebeispiel:

            Die linke Y-Achse zeigt die Umsatzwerte in Euro, während die rechte Y-Achse die Indexwerte anzeigt. Nicht alle Indikatoren können historisch über den kompletten Zeitverlauf abgebildet werden.

            **Was ist ein Indexwert?**
            Ein Indexwert zeigt Veränderungen im Vergleich zu einem Basiszeitraum an. Bei den HWWI-Indizes (Energierohstoffe, Rohöl, Kohle, Erdgas) zeigt ein höherer Wert steigende Preise an. Bei den IK-Indizes zeigt ein positiver Wert eine Verbesserung, ein negativer Wert eine Verschlechterung der Situation im Vergleich zum Vorquartal an. Die IK-Indizes basieren auf den Einschätzungen der befragten Unternehmen und können Werte zwischen -100 und +100 annehmen. Je höher der absolute Wert, desto stärker ist der Konsens unter den Befragten. Beispielsweise würde ein IK-Index von +50 bedeuten, dass deutlich mehr Unternehmen eine Verbesserung als eine Verschlechterung erwarten, während ein Wert von -50 auf eine überwiegend negative Einschätzung hindeuten würde.

            **Interpretation der aktuellen Werte:**
            Im vierten Quartal 2023 lag der Gesamtumsatz bei 5,8 Mio. Euro, wovon 2,7 Mio. Euro auf den Auslandsumsatz entfielen. Der Index für Exporte erreichte einen Wert von -43 Punkten, was auf eine deutlich pessimistischere Einschätzung der Exportentwicklung durch die befragten Unternehmen im Vergleich zum Vorquartal hindeutet. Diese negative Einschätzung hat sich in den Daten bestätigt: Die Exportzahlen zeigen einen Rückgang vom zweiten zum dritten Quartal 2023.
            """)
        elif dashboard_name == "Arbeitsmarkt":
            st.markdown("""
            ### Lesebeispiel:

            Die linke Y-Achse zeigt die absoluten Werte der Beschäftigten und Betriebe, während die rechte Y-Achse die Indexwerte anzeigt. Nicht alle Indikatoren können historisch über den kompletten Zeitverlauf abgebildet werden.

            **Was ist ein Indexwert?**
            Ein Indexwert zeigt Veränderungen im Vergleich zu einem Basiszeitraum an. Bei den HWWI-Indizes (Energierohstoffe, Rohöl, Kohle, Erdgas) zeigt ein höherer Wert steigende Preise an. Bei den IK-Indizes zeigt ein positiver Wert eine Verbesserung, ein negativer Wert eine Verschlechterung der Situation im Vergleich zum Vorquartal an. Die IK-Indizes basieren auf den Einschätzungen der befragten Unternehmen und können Werte zwischen -100 und +100 annehmen. Je höher der absolute Wert, desto stärker ist der Konsens unter den Befragten. Beispielsweise würde ein IK-Index von +50 bedeuten, dass deutlich mehr Unternehmen eine Verbesserung als eine Verschlechterung erwarten, während ein Wert von -50 auf eine überwiegend negative Einschätzung hindeuten würde.

            **Interpretation der aktuellen Werte:**
            Im vierten Quartal 2023 lag die Anzahl der Beschäftigten bei 91.700 Personen. Der Index für die Beschäftigtenzahl liegt bei -32,6 Punkten, während der Index für die Wirtschaftslage bei -62,9 Punkten liegt. Dies deutet auf eine deutlich pessimistische Einschätzung sowohl der Beschäftigungsentwicklung als auch der allgemeinen Wirtschaftslage hin.
            """)
        elif dashboard_name == "Rohstoffe":
            st.markdown("""
            ### Lesebeispiel:

            Die Y-Achse zeigt die verschiedenen Indexwerte an. Da es sich ausschließlich um Indizes handelt, wird nur eine Y-Achse benötigt. Nicht alle Indikatoren können historisch über den kompletten Zeitverlauf abgebildet werden.

            **Was ist ein Indexwert?**
            Ein Indexwert zeigt Veränderungen im Vergleich zu einem Basiszeitraum an. Bei den HWWI-Indizes (Energierohstoffe, Rohöl, Kohle, Erdgas) zeigt ein höherer Wert steigende Preise an. Bei den IK-Indizes zeigt ein positiver Wert eine Verbesserung, ein negativer Wert eine Verschlechterung der Situation im Vergleich zum Vorquartal an. Die IK-Indizes basieren auf den Einschätzungen der befragten Unternehmen und können Werte zwischen -100 und +100 annehmen. Je höher der absolute Wert, desto stärker ist der Konsens unter den Befragten. Beispielsweise würde ein IK-Index von +50 bedeuten, dass deutlich mehr Unternehmen eine Verbesserung als eine Verschlechterung erwarten, während ein Wert von -50 auf eine überwiegend negative Einschätzung hindeuten würde.
            
            **Interpretation der aktuellen Werte:**
            Im dritten Quartal 2022 erreichte der Index zur Preisentiwcklung der Energierohstoffe mit 718 Punkten einen historischen Höchststand. Diese extreme Preisentwicklung bei den Energierohstoffen spiegelt sich deutlich in den Einschätzungen der Unternehmen wider: Der Index für die Rohstoffverfügbarkeit liegt bei -17,4 Punkten, was auf Schwierigkeiten bei der Beschaffung hinweist. Besonders gravierend wirkt sich dies auf die Ertragslage aus, die mit einem Index von -76 Punkten einen sehr niedrigen Stand erreicht. Die außergewöhnlich hohen Energiepreise belasten die Unternehmen stark, da diese Kostensteigerungen nicht vollständig an die Kunden weitergegeben werden können.
            """)

        # Statistiken als ausklappbares Element
        #with st.expander(f"Statistiken ({dashboard_name})"):
            #for indicator in selected_indicators:
                #st.write(f"Kennzahlen für {indicator}:")
                #st.write(filtered_df[indicator].describe())
    else:
        st.info(f"Bitte Indikatoren für {dashboard_name} auswählen")

# Seitenkonfiguration
st.set_page_config(
    page_title="Dashboard: IK Wirtschaftsstatistik",
    layout="wide"
)

# Logo und Styling hinzufügen
st.markdown("""
    <style>
    .header-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 2rem 0;
    }

    [data-testid=stImage] {
        display: block;
        margin-left: auto !important;
        margin-right: auto !important;
        width: 200px !important;
    }

    .main-title {
        color: #004996 !important;
        font-family: 'Arial', sans-serif;
        font-size: 2.5rem;
        text-align: center;
        margin: 1rem 0;
        padding: 0;
        width: 100%;
    }

    .subtitle {
        color: #004996 !important;
        font-family: 'Arial', sans-serif;
        font-size: 1.5rem;
        text-align: center;
        margin: 0 0 1rem 0;
        padding: 0;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-container">', unsafe_allow_html=True)
#st.image("C:/Users/l.mueller/Documents/FileCloud/Team Folders/IK_Server/Wirtschaft/statistische Daten/ik-dashboard/assets/IK Logo.jpg", width=200)
st.image("assets/IK Logo.jpg", width=200)
st.markdown('''
    <h1 class="main-title">IK Wirtschaftsstatistik</h1>
    <h2 class="subtitle">Kunststoffverpackungen und -folienindustrie</h2>
</div>
''', unsafe_allow_html=True)

# Add custom CSS for the banner
st.markdown("""
    <style>
    .banner-container {
        background-color: #00B2A9;  /* IK's turquoise color */
        padding: 20px;
        border-radius: 5px;
        color: white;
        text-align: center;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Add the banner with text
st.markdown("""
    <div class="banner-container">
    Ein Dashboard ist ein interaktives Visualisierungstool, das komplexe Daten übersichtlich darstellt und wichtige Entwicklungen der Branche auf einen Blick erfassbar macht. Die IK stellt diese Informationen transparent zur Verfügung, um Mitgliedsunternehmen, Medienvertreter und die Öffentlichkeit über die wirtschaftliche Entwicklung der Kunststoffverpackungs- und folienindustrie zu informieren. Erkunden Sie die Daten und gewinnen Sie spannende Einblicke in unsere Branche!
""", unsafe_allow_html=True)
try:
    # Daten einlesen
    df = pd.read_excel(r'data/IK_Konj+Destatis_HWWI.xlsx')

    # Dashboard-Definitionen
    dashboards = {
        "Konjunktur": ["Umsatz", "Auslandsumsatz", "Auslandsumsatz mit der Eurozone",
                       "Auslandsumsatz mit dem sonstigen Ausland", "Index_Ertrag",
                       "Index_Exporte", "Index_Umsatz", "Index_Verkaufspreise (Branchenprodukte)",
                       "Index_Wirtschaftslage"],
        "Arbeitsmarkt": ["Betriebe", "Beschäftigte", "Index_Beschäftigtenzahl",
                         "Index_Wirtschaftslage"],
        "Rohstoffe": ["Index_Rohstoffverfügbarkeit", "Index_Preisentwicklung Energierohstoffe",
                      "Index_Preisentwicklung Kohle", "Index_Preisentwicklung Rohöl", "Index_Preisentwicklung Erdgas",
                      "Index_Ertrag", "Index_Verkaufspreise (Branchenprodukte)"]
    }

    # Zeitraum-Filter als ausklappbares Element im Hauptbereich
    with st.expander("Zeitraum-Filter", expanded=False):  # Der Zeitraum-Filter ist zu Beginn eingeklappt
        st.header("Zeitraum-Filter")

        # Filteroptionen im Hauptbereich, nicht in der Sidebar
        years = sorted(df['Jahr'].unique().tolist())
        selected_years = st.multiselect(
            "Jahre auswählen:",
            options=years,
            default=years
        )

        quarters = ['Q1', 'Q2', 'Q3', 'Q4']
        selected_quarters = st.multiselect(
            "Quartale auswählen:",
            options=quarters,
            default=quarters
        )

    # Daten filtern
    filtered_df = df[
        (df['Jahr'].isin(selected_years)) &
        (df['Monat'].isin(selected_quarters))
        ]

    # Sortierung und Zeitachse
    quartal_order = {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4}
    filtered_df['Quartal_Sortierung'] = filtered_df['Monat'].map(quartal_order)
    filtered_df = filtered_df.sort_values(by=['Jahr', 'Quartal_Sortierung'])
    filtered_df['Zeitachse'] = filtered_df['Jahr'].astype(str) + '-' + filtered_df['Monat']

    # Konjunktur Dashboard
    st.header("Konjunktur")
    with st.expander("ℹ️ Über dieses Dashboard"):
        st.markdown("""
            Dieses Dashboard zeigt zwei Arten von Daten für die deutsche Kunststoffverpackungs- und Folienindustrie:

            **1. Offizielle Statistiken (Destatis):**
            - Umsatz (in Euro)
            - Auslandsumsatz gesamt (in Euro)
            - Auslandsumsatz mit der Eurozone (in Euro)
            - Auslandsumsatz mit dem sonstigen Ausland (in Euro)

            **2. IK-Konjunkturumfrage (Quartalsdaten), berichtet über die Geschäftserwartungen:**
            - Index_Umsatz
            - Index_Ertrag
            - Index_Exporte
            - Index_Verkaufspreise
            - Index_Wirtschaftslage

            ➡️ Alle Daten beziehen sich ausschließlich auf die Kunststoffverpackungs- und Folienindustrie in Deutschland.
            """)

    selected_indicators_konj = st.multiselect(
        "Indikatoren für Konjunktur:",
        options=dashboards["Konjunktur"],
        default=["Umsatz", "Auslandsumsatz", "Index_Exporte"],
        max_selections=3
    )
    create_dashboard_plot("Konjunktur", selected_indicators_konj, filtered_df)
    st.markdown("---")

    # Arbeitsmarkt Dashboard
    st.header("Arbeitsmarkt")
    with st.expander("ℹ️ Über dieses Dashboard"):
        st.markdown("""
            Dieses Dashboard zeigt zwei Arten von Daten für die deutsche Kunststoffverpackungs- und Folienindustrie:

            **1. Offizielle Statistiken (Destatis):**
            - Betriebe (Anzahl)
            - Beschäftigte (Anzahl)

            **2. IK-Konjunkturumfrage (Quartalsdaten), berichtet über die Geschäftserwartungen:**
            - Index_Beschäftigtenzahl
            - Index_Wirtschaftslage

            ➡️ Alle Daten beziehen sich ausschließlich auf die Kunststoffverpackungs- und Folienindustrie in Deutschland.
            """)
    selected_indicators_arb = st.multiselect(
        "Indikatoren für Arbeitsmarkt:",
        options=dashboards["Arbeitsmarkt"],
        default=["Beschäftigte", "Index_Beschäftigtenzahl", "Index_Wirtschaftslage"],
        max_selections=3
    )
    create_dashboard_plot("Arbeitsmarkt", selected_indicators_arb, filtered_df)
    st.markdown("---")

    # Rohstoffe Dashboard
    st.header("Rohstoffe")
    with st.expander("ℹ️ Über dieses Dashboard"):
        st.markdown("""
            Dieses Dashboard zeigt zwei Arten von Daten:

            **1. Offizielle Statistiken (HWWI):**
            - Index_Preisentwicklung Energierohstoffe
            - Index_Preisentwicklung Kohle
            - Index_Preisentwicklung Rohöl
            - Index_Preisentwicklung Erdgas

            **2. IK-Konjunkturumfrage (Quartalsdaten), berichtet über die Geschäftserwartungen:**
            - Index_Verkaufspreise
            - Index_Ertrag
            - Index_Rohstoffverfügbarkeit

            ➡️ Alle Daten des HWWI beziehen sich auf Deutschland insgesamt, Daten der IK-Konjunkturumfrage beziehen sich auf die Branche der Kunststoffverpackungs- und Folienindustrie in Deutschland.
            """)
    selected_indicators_roh = st.multiselect(
        "Indikatoren für Rohstoffe:",
        options=dashboards["Rohstoffe"],
        default=["Index_Preisentwicklung Energierohstoffe", "Index_Ertrag", "Index_Rohstoffverfügbarkeit"],
        max_selections=3
    )
    create_dashboard_plot("Rohstoffe", selected_indicators_roh, filtered_df)

    # Add after the last dashboard section but before the except statement
    st.markdown("---")

    # External sources section
    st.markdown("""
    ### Externe Quellen:
    - **Destatis**: [Genesis-Online Datenbank](https://www-genesis.destatis.de/datenbank/online/)  
      *insb. Konjunkturstatistik (Tabellencode 42111), Datenmodifikation (insb. der Wirtschaftszweige 2221 und 2222 zur Branchenabgrenzung) anhand eigener Berechnungen*
    - **HWWI**: [Rohstoffpreisindex](https://www.hwwi.org/datenangebote/rohstoffpreisindex/)  

    ### Kontakt bei Fragen:
    **Referat für Wirtschaft**  
    IK Industrieverband e.V.  
    Laura C. Müller  
    L.Mueller@Kunststoffverpackungen.de
    """)

except Exception as e:
    st.error(f"Fehler beim Laden der Daten: {str(e)}")
