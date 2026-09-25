import sys
sys.path.append(".")
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.utils.db_connection import get_engine

st.set_page_config(
    page_title="CivicLens India",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.main { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    border-right: 1px solid rgba(255,255,255,0.1);
}
section[data-testid="stSidebar"] * { color: white !important; }
.hero-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 20px 60px rgba(102,126,234,0.4);
}
.hero-title {
    font-size: 3rem;
    font-weight: 700;
    color: white;
    text-shadow: 0 0 30px rgba(255,255,255,0.5);
    margin: 0;
}
.hero-subtitle {
    font-size: 1rem;
    color: rgba(255,255,255,0.85);
    margin-top: 10px;
}
.metric-card {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    border-radius: 16px;
    padding: 25px 20px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 15px;
}
.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #00d2ff;
    text-shadow: 0 0 20px rgba(0,210,255,0.5);
}
.metric-label {
    font-size: 0.8rem;
    color: rgba(255,255,255,0.7);
    margin-top: 5px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.metric-icon { font-size: 1.8rem; margin-bottom: 8px; }
.section-header {
    font-size: 1.3rem;
    font-weight: 700;
    color: #667eea !important;
    margin: 20px 0 15px 0;
    padding-left: 10px;
    border-left: 4px solid #667eea;
}
.insight-card {
    background: rgba(102,126,234,0.15);
    border-radius: 12px;
    padding: 12px 18px;
    border: 1px solid rgba(102,126,234,0.3);
    margin-bottom: 8px;
    color: white;
}
.footer {
    text-align: center;
    padding: 20px;
    color: rgba(255,255,255,0.4);
    font-size: 0.8rem;
    border-top: 1px solid rgba(255,255,255,0.1);
    margin-top: 40px;
}
h1, h2, h3, p, label { color: white !important; }
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 5px;
}
.stTabs [data-baseweb="tab"] { color: rgba(255,255,255,0.6) !important; border-radius: 8px; }
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    engine = get_engine()
    query = """
        SELECT
            s.state_name,
            y.year,
            f.total_crimes,
            f.population_lakhs_2022,
            f.crime_rate_per_lakh_2022,
            f.chargesheeting_rate_2022,
            f.literacy_rate,
            f.literacy_year
        FROM fact_crime f
        JOIN dim_state s ON f.state_id = s.state_id
        JOIN dim_year y ON f.year_id = y.year_id
        ORDER BY s.state_name, y.year
    """
    return pd.read_sql(query, engine)


df = load_data()

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Filters")
    st.markdown("---")
    selected_year = st.selectbox(
        "📅 Year",
        sorted(df['year'].unique(), reverse=True)
    )
    all_states = sorted(df['state_name'].unique().tolist())
    selected_states = st.multiselect(
        "🗺️ States",
        all_states,
        default=all_states
    )
    st.markdown("---")
    st.markdown("### 📊 Top N States")
    top_n = st.slider("Show top N states", 5, 36, 10)
    st.markdown("---")
    st.markdown("""
    <div style='color:rgba(255,255,255,0.5); font-size:0.75rem;'>
    📦 Data Sources<br>
    • NCRB Crime Data 2020–2022<br>
    • Census Literacy 2011<br>
    • Mid-Year Population 2022
    </div>
    """, unsafe_allow_html=True)

filtered = df[
    (df['year'] == selected_year) &
    (df['state_name'].isin(selected_states))
]

# ── HERO ─────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-container'>
    <div class='hero-title'>🇮🇳 CivicLens India</div>
    <div class='hero-subtitle'>Automated Crime & Literacy Analytics Platform</div>
</div>
""", unsafe_allow_html=True)

# ── KPI CARDS ────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-icon'>🏛️</div>
        <div class='metric-value'>{filtered['state_name'].nunique()}</div>
        <div class='metric-label'>States</div>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-icon'>🚨</div>
        <div class='metric-value'>{int(filtered['total_crimes'].sum()):,}</div>
        <div class='metric-label'>Total Crimes</div>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-icon'>📊</div>
        <div class='metric-value'>{filtered['crime_rate_per_lakh_2022'].mean():.1f}</div>
        <div class='metric-label'>Avg Crime Rate</div>
    </div>""", unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-icon'>📚</div>
        <div class='metric-value'>{filtered['literacy_rate'].mean():.1f}%</div>
        <div class='metric-label'>Avg Literacy</div>
    </div>""", unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-icon'>⚖️</div>
        <div class='metric-value'>{filtered['chargesheeting_rate_2022'].mean():.1f}%</div>
        <div class='metric-label'>Chargesheeting</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── TABS ─────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🚨 Crime Analysis",
    "📚 Literacy",
    "🔗 Correlation",
    "📈 Trends",
    "📋 Data Table"
])

bg = "rgba(0,0,0,0)"
fc = "white"
gc = "rgba(255,255,255,0.1)"

# ── TAB 1 ────────────────────────────────────────────────────────
with tab1:
    st.markdown("<div class='section-header'>Crime Rate by State</div>", unsafe_allow_html=True)

    top_crime = filtered.nlargest(top_n, 'crime_rate_per_lakh_2022')

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=top_crime['state_name'],
        y=top_crime['crime_rate_per_lakh_2022'],
        marker=dict(
            color=top_crime['crime_rate_per_lakh_2022'],
            colorscale='Reds',
            showscale=True,
            colorbar=dict(
                tickfont=dict(color='white'),
                title=dict(text="Rate", font=dict(color='white'))
            )
        ),
        text=top_crime['crime_rate_per_lakh_2022'].round(1),
        textposition='outside',
        textfont=dict(color='white'),
        hovertemplate="<b>%{x}</b><br>Crime Rate: %{y:.1f}<extra></extra>"
    ))
    fig1.update_layout(
        plot_bgcolor=bg, paper_bgcolor=bg,
        font=dict(color=fc),
        xaxis=dict(tickangle=-45, gridcolor=gc, tickfont=dict(color='white')),
        yaxis=dict(gridcolor=gc, tickfont=dict(color='white')),
        height=450, margin=dict(t=20, b=100)
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("<div class='section-header'>Total Crimes by State</div>", unsafe_allow_html=True)

    top_total = filtered.nlargest(top_n, 'total_crimes')
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=top_total['state_name'],
        y=top_total['total_crimes'],
        marker=dict(
            color=top_total['total_crimes'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                tickfont=dict(color='white'),
                title=dict(text="Crimes", font=dict(color='white'))
            )
        ),
        text=top_total['total_crimes'].apply(lambda x: f"{int(x):,}"),
        textposition='outside',
        textfont=dict(color='white'),
        hovertemplate="<b>%{x}</b><br>Total Crimes: %{text}<extra></extra>"
    ))
    fig2.update_layout(
        plot_bgcolor=bg, paper_bgcolor=bg,
        font=dict(color=fc),
        xaxis=dict(tickangle=-45, gridcolor=gc, tickfont=dict(color='white')),
        yaxis=dict(gridcolor=gc, tickfont=dict(color='white')),
        height=400, margin=dict(t=20, b=100)
    )
    st.plotly_chart(fig2, use_container_width=True)

# ── TAB 2 ────────────────────────────────────────────────────────
with tab2:
    st.markdown("<div class='section-header'>Literacy Rate by State (Census 2011)</div>", unsafe_allow_html=True)

    lit_df = filtered.dropna(subset=['literacy_rate']).sort_values('literacy_rate', ascending=True)

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        y=lit_df['state_name'],
        x=lit_df['literacy_rate'],
        orientation='h',
        marker=dict(
            color=lit_df['literacy_rate'],
            colorscale='Greens',
            showscale=True,
            colorbar=dict(
                tickfont=dict(color='white'),
                title=dict(text="%", font=dict(color='white'))
            )
        ),
        text=lit_df['literacy_rate'].round(1).astype(str) + "%",
        textposition='outside',
        textfont=dict(color='white'),
        hovertemplate="<b>%{y}</b><br>Literacy: %{x:.1f}%<extra></extra>"
    ))
    fig3.update_layout(
        plot_bgcolor=bg, paper_bgcolor=bg,
        font=dict(color=fc),
        xaxis=dict(gridcolor=gc, tickfont=dict(color='white'), range=[0, 110]),
        yaxis=dict(gridcolor=gc, tickfont=dict(color='white')),
        height=600, margin=dict(t=20, r=80)
    )
    st.plotly_chart(fig3, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        top5 = filtered.nlargest(5, 'literacy_rate')[['state_name', 'literacy_rate']].dropna()
        st.markdown("<div class='section-header'>Top 5 Literate</div>", unsafe_allow_html=True)
        for _, row in top5.iterrows():
            st.markdown(f"""
            <div class='insight-card'>
                🏆 <b>{row['state_name']}</b> — {row['literacy_rate']:.1f}%
            </div>""", unsafe_allow_html=True)

    with col2:
        bot5 = filtered.nsmallest(5, 'literacy_rate')[['state_name', 'literacy_rate']].dropna()
        st.markdown("<div class='section-header'>Bottom 5 States</div>", unsafe_allow_html=True)
        for _, row in bot5.iterrows():
            st.markdown(f"""
            <div class='insight-card'>
                ⚠️ <b>{row['state_name']}</b> — {row['literacy_rate']:.1f}%
            </div>""", unsafe_allow_html=True)

# ── TAB 3 ────────────────────────────────────────────────────────
with tab3:
    st.markdown("<div class='section-header'>Literacy vs Crime Rate</div>", unsafe_allow_html=True)

    scatter_df = filtered.dropna(subset=['literacy_rate', 'crime_rate_per_lakh_2022'])

    fig4 = px.scatter(
        scatter_df,
        x='literacy_rate',
        y='crime_rate_per_lakh_2022',
        size='population_lakhs_2022',
        color='crime_rate_per_lakh_2022',
        color_continuous_scale='RdYlGn_r',
        text='state_name',
        labels={
            'literacy_rate': 'Literacy Rate (%)',
            'crime_rate_per_lakh_2022': 'Crime Rate per Lakh',
            'population_lakhs_2022': 'Population (Lakhs)'
        },
        height=500
    )
    fig4.update_traces(
        textposition='top center',
        textfont=dict(size=10, color='white'),
        marker=dict(line=dict(width=1, color='white'))
    )
    fig4.update_layout(
        plot_bgcolor=bg, paper_bgcolor=bg,
        font=dict(color=fc),
        xaxis=dict(gridcolor=gc, tickfont=dict(color='white')),
        yaxis=dict(gridcolor=gc, tickfont=dict(color='white')),
        coloraxis_colorbar=dict(
            tickfont=dict(color='white'),
            title=dict(text="Rate", font=dict(color='white'))
        ),
        margin=dict(t=20)
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<div class='section-header'>Crime vs Chargesheeting Rate</div>", unsafe_allow_html=True)

    fig5 = px.scatter(
        filtered.dropna(),
        x='chargesheeting_rate_2022',
        y='crime_rate_per_lakh_2022',
        size='population_lakhs_2022',
        color='literacy_rate',
        color_continuous_scale='Blues',
        text='state_name',
        labels={
            'chargesheeting_rate_2022': 'Chargesheeting Rate (%)',
            'crime_rate_per_lakh_2022': 'Crime Rate per Lakh',
            'literacy_rate': 'Literacy Rate'
        },
        height=500
    )
    fig5.update_traces(
        textposition='top center',
        textfont=dict(size=9, color='white'),
        marker=dict(line=dict(width=1, color='rgba(255,255,255,0.3)'))
    )
    fig5.update_layout(
        plot_bgcolor=bg, paper_bgcolor=bg,
        font=dict(color=fc),
        xaxis=dict(gridcolor=gc, tickfont=dict(color='white')),
        yaxis=dict(gridcolor=gc, tickfont=dict(color='white')),
        coloraxis_colorbar=dict(
            tickfont=dict(color='white'),
            title=dict(text="Literacy", font=dict(color='white'))
        ),
        margin=dict(t=20)
    )
    st.plotly_chart(fig5, use_container_width=True)

# ── TAB 4 ────────────────────────────────────────────────────────
with tab4:
    st.markdown("<div class='section-header'>Crime Trend 2020 → 2022</div>", unsafe_allow_html=True)

    trend_states = st.multiselect(
        "Select States",
        all_states,
        default=all_states[:6]
    )

    trend_df = df[df['state_name'].isin(trend_states)]
    colors = px.colors.qualitative.Set1

    fig6 = go.Figure()
    for i, state in enumerate(trend_states):
        sdf = trend_df[trend_df['state_name'] == state]
        fig6.add_trace(go.Scatter(
            x=sdf['year'],
            y=sdf['total_crimes'],
            mode='lines+markers',
            name=state,
            line=dict(color=colors[i % len(colors)], width=2.5),
            marker=dict(size=8, line=dict(width=2, color='white')),
            hovertemplate=f"<b>{state}</b><br>Year: %{{x}}<br>Crimes: %{{y:,}}<extra></extra>"
        ))
    fig6.update_layout(
        plot_bgcolor=bg, paper_bgcolor=bg,
        font=dict(color=fc),
        xaxis=dict(gridcolor=gc, tickfont=dict(color='white'), tickmode='linear', dtick=1),
        yaxis=dict(gridcolor=gc, tickfont=dict(color='white')),
        legend=dict(
            bgcolor='rgba(255,255,255,0.05)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1,
            font=dict(color='white')
        ),
        height=450,
        hovermode='x unified'
    )
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("<div class='section-header'>Crime Rate Trend</div>", unsafe_allow_html=True)

    fig7 = go.Figure()
    for i, state in enumerate(trend_states):
        sdf = trend_df[trend_df['state_name'] == state]
        fig7.add_trace(go.Scatter(
            x=sdf['year'],
            y=sdf['crime_rate_per_lakh_2022'],
            mode='lines+markers',
            name=state,
            line=dict(color=colors[i % len(colors)], width=2.5, dash='dot'),
            marker=dict(size=8, line=dict(width=2, color='white')),
            hovertemplate=f"<b>{state}</b><br>Year: %{{x}}<br>Rate: %{{y:.1f}}<extra></extra>"
        ))
    fig7.update_layout(
        plot_bgcolor=bg, paper_bgcolor=bg,
        font=dict(color=fc),
        xaxis=dict(gridcolor=gc, tickfont=dict(color='white'), tickmode='linear', dtick=1),
        yaxis=dict(gridcolor=gc, tickfont=dict(color='white')),
        legend=dict(
            bgcolor='rgba(255,255,255,0.05)',
            bordercolor='rgba(255,255,255,0.2)',
            borderwidth=1,
            font=dict(color='white')
        ),
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig7, use_container_width=True)

# ── TAB 5 ────────────────────────────────────────────────────────
with tab5:
    st.markdown("<div class='section-header'>Complete Data Table</div>", unsafe_allow_html=True)

    search = st.text_input("🔍 Search State", "")
    if search:
        table_df = filtered[filtered['state_name'].str.contains(search, case=False)]
    else:
        table_df = filtered

    st.dataframe(
        table_df[[
            'state_name', 'year', 'total_crimes',
            'crime_rate_per_lakh_2022', 'literacy_rate',
            'chargesheeting_rate_2022', 'population_lakhs_2022'
        ]].rename(columns={
            'state_name': 'State',
            'year': 'Year',
            'total_crimes': 'Total Crimes',
            'crime_rate_per_lakh_2022': 'Crime Rate/Lakh',
            'literacy_rate': 'Literacy %',
            'chargesheeting_rate_2022': 'Chargesheeting %',
            'population_lakhs_2022': 'Population (Lakhs)'
        }).reset_index(drop=True),
        use_container_width=True,
        height=500
    )

    csv = table_df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name=f"civicLens_{selected_year}.csv",
        mime='text/csv'
    )

# ── FOOTER ───────────────────────────────────────────────────────
st.markdown("""
<div class='footer'>
    🇮🇳 CivicLens India &nbsp;|&nbsp;
    Data: NCRB Crime 2020–2022 &nbsp;|&nbsp;
    Census Literacy 2011 &nbsp;|&nbsp;
    Built with Python · Streamlit · Plotly · MySQL
</div>
""", unsafe_allow_html=True)