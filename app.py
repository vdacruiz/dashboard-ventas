"""
Dashboard Venta Nacional — Viña de Aguirre
Deploy: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="Dashboard Venta Nacional",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

GOOGLE_SHEET_ID = "1mtythtz8KLzrP-MoSFbCJvCQApEbRbzA1LAF2Synz1A"
GOOGLE_SHEET_URL = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=xlsx"

AZUL_OSCURO = '#1B2A4A'
AZUL = '#2E5090'
AZUL_CLARO = '#4472C4'
VERDE = '#27AE60'
ROJO = '#E74C3C'
NARANJA = '#F39C12'
GRIS = '#95A5A6'

MESES = {1:'Ene',2:'Feb',3:'Mar',4:'Abr',5:'May',6:'Jun',
          7:'Jul',8:'Ago',9:'Sep',10:'Oct',11:'Nov',12:'Dic'}

# ============================================================
# ESTILOS CORPORATIVOS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .main .block-container { padding-top: 0.5rem; max-width: 1500px; }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* Sidebar ejecutivo */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0D1B2A 0%, #1B2A4A 40%, #2E5090 100%);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label {
        color: #87CEEB !important; font-weight: 600; font-size: 12px;
        text-transform: uppercase; letter-spacing: 0.5px;
    }

    /* Header corporativo */
    .corp-header {
        background: linear-gradient(135deg, #0D1B2A, #1B2A4A, #2E5090);
        color: white; padding: 20px 30px; border-radius: 12px;
        margin-bottom: 20px; position: relative; overflow: hidden;
    }
    .corp-header::after {
        content: ''; position: absolute; top: 0; right: 0;
        width: 200px; height: 100%; opacity: 0.1;
        background: linear-gradient(135deg, transparent, rgba(255,255,255,0.3));
    }
    .corp-header h1 { font-size: 28px; font-weight: 800; margin: 0; letter-spacing: -0.5px; }
    .corp-header .subtitle { font-size: 13px; color: #87CEEB; margin-top: 4px; font-weight: 400; }
    .corp-header .badge {
        display: inline-block; background: rgba(255,255,255,0.15);
        padding: 4px 12px; border-radius: 20px; font-size: 11px;
        color: #C9960C; font-weight: 600; margin-top: 8px; letter-spacing: 0.5px;
    }

    /* KPI Cards premium */
    .kpi-card {
        background: white; border-radius: 16px; padding: 22px 18px;
        text-align: center; position: relative; overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06); border: 1px solid #e8ecf1;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kpi-card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.1); }
    .kpi-card::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0;
        height: 4px; background: linear-gradient(90deg, #2E5090, #4472C4);
    }
    .kpi-card-green::before { background: linear-gradient(90deg, #27AE60, #2ECC71); }
    .kpi-card-red::before { background: linear-gradient(90deg, #E74C3C, #C0392B); }
    .kpi-card-gold::before { background: linear-gradient(90deg, #C9960C, #F39C12); }

    .kpi-value {
        font-size: 28px; font-weight: 800; color: #0D1B2A;
        margin: 8px 0 4px 0; letter-spacing: -0.5px;
    }
    .kpi-label {
        font-size: 10px; color: #6B7B8D; text-transform: uppercase;
        letter-spacing: 1.5px; font-weight: 600;
    }
    .kpi-delta-pos {
        color: #27AE60; font-size: 13px; font-weight: 700;
        background: #E8F8F0; padding: 2px 8px; border-radius: 12px; display: inline-block;
    }
    .kpi-delta-neg {
        color: #E74C3C; font-size: 13px; font-weight: 700;
        background: #FDEDEC; padding: 2px 8px; border-radius: 12px; display: inline-block;
    }

    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #0D1B2A, #1B2A4A);
        color: white; padding: 10px 20px; border-radius: 8px;
        margin: 24px 0 12px 0; font-size: 14px; font-weight: 700;
        letter-spacing: 0.5px; text-transform: uppercase;
        box-shadow: 0 2px 8px rgba(13,27,42,0.2);
    }

    /* Insight boxes */
    .insight-box {
        background: linear-gradient(135deg, #FFF8E1, #FFFDE7);
        border-left: 4px solid #C9960C; padding: 14px 18px;
        border-radius: 0 10px 10px 0; margin: 8px 0;
        font-size: 13px; color: #333; font-weight: 500;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .insight-alert {
        background: linear-gradient(135deg, #FDEDEC, #FFF5F5);
        border-left: 4px solid #E74C3C;
    }
    .insight-success {
        background: linear-gradient(135deg, #E8F8F0, #F0FFF4);
        border-left: 4px solid #27AE60;
    }

    /* Tabs premium */
    .stTabs [data-baseweb="tab-list"] {
        background: #f8f9fa; border-radius: 10px; padding: 4px;
        gap: 4px; border: 1px solid #e8ecf1;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px; font-weight: 600; font-size: 13px;
        padding: 8px 20px; letter-spacing: 0.3px;
    }
    .stTabs [aria-selected="true"] {
        background: #1B2A4A !important; color: white !important;
        border-radius: 8px; box-shadow: 0 2px 8px rgba(27,42,74,0.3);
    }

    /* DataFrames */
    .stDataFrame { border-radius: 10px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
    div[data-testid="stMetric"] {
        background: white; border-radius: 12px; padding: 16px;
        border-left: 4px solid #2E5090; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    /* Footer */
    .corp-footer {
        text-align: center; padding: 20px; margin-top: 40px;
        border-top: 2px solid #e8ecf1; color: #6B7B8D; font-size: 11px;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# CARGA DE DATOS
# ============================================================
@st.cache_data(ttl=300)
def cargar_datos():
    df = pd.read_excel(GOOGLE_SHEET_URL)

    for col in df.columns:
        if df[col].dtype == object:
            sample = df[col].dropna().head(50).astype(str)
            if sample.str.contains(r'[\$]|USD|EUR', regex=True).any():
                df[col] = df[col].apply(limpiar_numero)

    num_cols = [
        'Cantidad_Final', 'Cajas_Final', 'Neto_Final', 'Costo PRD',
        'Costo Rappel', 'Rappel x3', 'Bonificacion Casal', 'Costo Total',
        'Utilidad', 'Mg_Pct', 'Util_Unitaria', 'Unid_x_Caja',
        'Año', 'Mes'
    ]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df['Año'] = df['Año'].fillna(df['Fecha'].dt.year).astype(int)
    df['Mes'] = df['Mes'].fillna(df['Fecha'].dt.month).astype(int)
    df['Mes_Nombre'] = df['Mes'].map(MESES)

    if 'Ejecutivo' in df.columns:
        df['Ejecutivo'] = df['Ejecutivo'].astype(str).str.strip()

    return df


def limpiar_numero(val):
    if pd.isna(val):
        return np.nan
    s = str(val).strip()
    if s in ('', '-', 'nan', 'None'):
        return np.nan
    s = s.replace('$', '').replace('USD', '').replace('EUR', '').strip()
    if s in ('', '-'):
        return np.nan
    if ',' in s and '.' in s:
        s = s.replace('.', '').replace(',', '.')
    elif ',' in s:
        s = s.replace(',', '.')
    elif '.' in s:
        parts = s.split('.')
        if len(parts) == 2 and len(parts[1]) == 3:
            s = s.replace('.', '')
        elif len(parts) > 2:
            s = s.replace('.', '')
    try:
        return float(s)
    except ValueError:
        return np.nan


# ============================================================
# HELPERS
# ============================================================
def fmt_m(val):
    if pd.isna(val) or val == 0:
        return "$0"
    if abs(val) >= 1e9:
        return f"${val/1e9:,.1f}B"
    if abs(val) >= 1e6:
        return f"${val/1e6:,.1f}MM"
    return f"${val:,.0f}"

def fmt_n(val):
    if pd.isna(val):
        return "0"
    return f"{val:,.0f}"

def fmt_pct(val):
    if pd.isna(val):
        return "0%"
    return f"{val:.1%}"

def var_pct(actual, anterior):
    if anterior == 0 or pd.isna(anterior):
        return None
    return (actual - anterior) / abs(anterior)

def kpi_card(label, value, delta=None, prefix="", suffix="", card_class=""):
    delta_html = ""
    if delta is not None and not pd.isna(delta):
        cls = "kpi-delta-pos" if delta >= 0 else "kpi-delta-neg"
        arrow = "▲" if delta >= 0 else "▼"
        delta_html = f'<div style="margin-top:6px"><span class="{cls}">{arrow} {abs(delta):.0%}</span> <span style="font-size:10px;color:#999">vs año ant.</span></div>'
    extra = f" {card_class}" if card_class else ""
    st.markdown(f"""
    <div class="kpi-card{extra}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{prefix}{value}{suffix}</div>
        {delta_html}
    </div>""", unsafe_allow_html=True)

def section(text):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)

def tabla_comparativa(df_act, df_ant, group_col, metrics_config):
    """Genera tabla comparativa año actual vs anterior con variaciones."""
    agg_dict = {m['col']: 'sum' for m in metrics_config if m.get('agg', 'sum') == 'sum'}

    g_act = df_act.groupby(group_col, dropna=False).agg(**{
        m['col']: (m['col'], m.get('agg', 'sum')) for m in metrics_config
        if m.get('agg', 'sum') == 'sum'
    }).reset_index() if len(df_act) > 0 else pd.DataFrame()

    g_ant = df_ant.groupby(group_col, dropna=False).agg(**{
        m['col']: (m['col'], m.get('agg', 'sum')) for m in metrics_config
        if m.get('agg', 'sum') == 'sum'
    }).reset_index() if len(df_ant) > 0 else pd.DataFrame()

    return g_act, g_ant


def build_comparison_df(df_act, df_ant, group_col, año_act, año_ant):
    """Construye DataFrame comparativo completo para mostrar."""
    sum_cols = ['Cajas_Final', 'Neto_Final', 'Costo Total', 'Utilidad']

    g_act = df_act.groupby(group_col).agg(
        Cajas=('Cajas_Final', 'sum'),
        Neto=('Neto_Final', 'sum'),
        Costo=('Costo Total', 'sum'),
        Utilidad=('Utilidad', 'sum'),
    ).reset_index() if len(df_act) > 0 else pd.DataFrame(columns=[group_col, 'Cajas', 'Neto', 'Costo', 'Utilidad'])

    g_ant = df_ant.groupby(group_col).agg(
        Cajas=('Cajas_Final', 'sum'),
        Neto=('Neto_Final', 'sum'),
        Costo=('Costo Total', 'sum'),
        Utilidad=('Utilidad', 'sum'),
    ).reset_index() if len(df_ant) > 0 else pd.DataFrame(columns=[group_col, 'Cajas', 'Neto', 'Costo', 'Utilidad'])

    if len(g_act) > 0:
        g_act['Util_Unit'] = np.where(g_act['Cajas'] > 0, g_act['Utilidad'] / g_act['Cajas'], 0)
        g_act['Mg'] = np.where(g_act['Neto'] > 0, g_act['Utilidad'] / g_act['Neto'], 0)
    if len(g_ant) > 0:
        g_ant['Util_Unit'] = np.where(g_ant['Cajas'] > 0, g_ant['Utilidad'] / g_ant['Cajas'], 0)
        g_ant['Mg'] = np.where(g_ant['Neto'] > 0, g_ant['Utilidad'] / g_ant['Neto'], 0)

    all_keys = set()
    if len(g_act) > 0:
        all_keys.update(g_act[group_col].tolist())
    if len(g_ant) > 0:
        all_keys.update(g_ant[group_col].tolist())

    rows = []
    for key in sorted(all_keys, key=str):
        row = {group_col: key}
        a = g_act[g_act[group_col] == key].iloc[0] if len(g_act) > 0 and key in g_act[group_col].values else None
        b = g_ant[g_ant[group_col] == key].iloc[0] if len(g_ant) > 0 and key in g_ant[group_col].values else None

        for metric in ['Cajas', 'Neto', 'Costo', 'Utilidad', 'Util_Unit', 'Mg']:
            va = a[metric] if a is not None else 0
            vb = b[metric] if b is not None else 0
            row[f'{metric}_{año_act}'] = va
            row[f'{metric}_{año_ant}'] = vb
            if metric in ('Cajas', 'Neto', 'Utilidad'):
                row[f'Var_{metric}'] = va - vb
                row[f'Var%_{metric}'] = var_pct(va, vb)

        rows.append(row)

    return pd.DataFrame(rows)


def render_comparison_table(comp_df, group_col, año_act, año_ant, sort_by=None):
    """Renderiza tabla comparativa formateada."""
    if len(comp_df) == 0:
        st.info("Sin datos para este período")
        return

    if sort_by and sort_by in comp_df.columns:
        comp_df = comp_df.sort_values(sort_by, ascending=False)

    display = pd.DataFrame()
    display[group_col] = comp_df[group_col]
    display[f'Cajas {año_act}'] = comp_df[f'Cajas_{año_act}'].apply(fmt_n)
    display[f'Vta Neta {año_act}'] = comp_df[f'Neto_{año_act}'].apply(fmt_m)
    display[f'Costo {año_act}'] = comp_df[f'Costo_{año_act}'].apply(fmt_m)
    display[f'Utilidad {año_act}'] = comp_df[f'Utilidad_{año_act}'].apply(fmt_m)
    display[f'Mg% {año_act}'] = comp_df[f'Mg_{año_act}'].apply(fmt_pct)
    display[f'Cajas {año_ant}'] = comp_df[f'Cajas_{año_ant}'].apply(fmt_n)
    display[f'Vta Neta {año_ant}'] = comp_df[f'Neto_{año_ant}'].apply(fmt_m)
    display[f'Utilidad {año_ant}'] = comp_df[f'Utilidad_{año_ant}'].apply(fmt_m)
    display[f'Mg% {año_ant}'] = comp_df[f'Mg_{año_ant}'].apply(fmt_pct)
    display['Var% Cajas'] = comp_df['Var%_Cajas'].apply(lambda x: f"{x:+.1%}" if pd.notna(x) else "-")
    display['Var% Neto'] = comp_df['Var%_Neto'].apply(lambda x: f"{x:+.1%}" if pd.notna(x) else "-")
    display['Var% Util'] = comp_df['Var%_Utilidad'].apply(lambda x: f"{x:+.1%}" if pd.notna(x) else "-")

    st.dataframe(display, use_container_width=True, hide_index=True)


def build_super_detail(df_act, df_ant, group_col, año_act, año_ant):
    """Tabla especial Supermercado con desglose Costo PRD, Rappel, etc."""
    agg = {
        'Cantidad_Final': 'sum', 'Cajas_Final': 'sum', 'Neto_Final': 'sum',
        'Costo PRD': 'sum', 'Costo Rappel': 'sum', 'Rappel x3': 'sum',
        'Bonificacion Casal': 'sum',
    }

    g_act = df_act.groupby(group_col).agg(**{k: (k, v) for k, v in agg.items()}).reset_index() if len(df_act) > 0 else pd.DataFrame()
    g_ant = df_ant.groupby(group_col).agg(**{k: (k, v) for k, v in agg.items()}).reset_index() if len(df_ant) > 0 else pd.DataFrame()

    if len(g_act) > 0:
        g_act['Mg'] = np.where(g_act['Neto_Final'] != 0,
            (g_act['Neto_Final'] + g_act['Costo PRD'] + g_act['Costo Rappel'] + g_act['Rappel x3'] + g_act['Bonificacion Casal']) / g_act['Neto_Final'], 0)
    if len(g_ant) > 0:
        g_ant['Mg'] = np.where(g_ant['Neto_Final'] != 0,
            (g_ant['Neto_Final'] + g_ant['Costo PRD'] + g_ant['Costo Rappel'] + g_ant['Rappel x3'] + g_ant['Bonificacion Casal']) / g_ant['Neto_Final'], 0)

    display = pd.DataFrame()
    if len(g_act) > 0:
        display[group_col] = g_act[group_col]
        display['Unidades'] = g_act['Cantidad_Final'].apply(fmt_n)
        display['Cajas'] = g_act['Cajas_Final'].apply(fmt_n)
        display['Neto'] = g_act['Neto_Final'].apply(fmt_m)
        display['Costo PRD'] = g_act['Costo PRD'].apply(fmt_m)
        display['Rappel'] = g_act['Costo Rappel'].apply(fmt_m)
        display['Rappel x3'] = g_act['Rappel x3'].apply(fmt_m)
        display['Bonif.'] = g_act['Bonificacion Casal'].apply(fmt_m)
        display['% Mg'] = g_act['Mg'].apply(fmt_pct)

    st.dataframe(display, use_container_width=True, hide_index=True)


# ============================================================
# SIDEBAR FILTERS
# ============================================================
def sidebar_filters(df):
    st.sidebar.markdown("## 🎛️ Filtros")

    años = sorted(df['Año'].unique(), reverse=True)
    año_act = st.sidebar.selectbox("Año", años, index=0)
    año_ant = año_act - 1

    meses_disponibles = sorted(df[df['Año'] == año_act]['Mes'].unique())
    mes_hasta = st.sidebar.selectbox("Acumulado hasta", meses_disponibles,
                                      index=len(meses_disponibles)-1,
                                      format_func=lambda x: MESES.get(x, str(x)))
    meses_sel = list(range(1, mes_hasta + 1))

    canales = ['Todos'] + sorted(df['Canal de ventas'].dropna().unique().tolist())
    canal = st.sidebar.selectbox("Canal", canales)

    categorias = ['Todas'] + sorted(df['Categoria'].dropna().unique().tolist())
    categoria = st.sidebar.selectbox("Categoría", categorias)

    marcas = ['Todas'] + sorted(df['Marca'].dropna().unique().tolist())
    marca = st.sidebar.selectbox("Marca", marcas)

    ejecutivos = ['Todos'] + sorted(df['Ejecutivo'].dropna().unique().tolist())
    ejecutivo = st.sidebar.selectbox("Ejecutivo", ejecutivos)

    clientes = ['Todos'] + sorted(df['Razon Social'].dropna().unique().tolist())
    cliente = st.sidebar.selectbox("Cliente", clientes)

    mask = (df['Mes'].isin(meses_sel))
    df_act = df[(df['Año'] == año_act) & mask].copy()
    df_ant = df[(df['Año'] == año_ant) & mask].copy()

    if canal != 'Todos':
        df_act = df_act[df_act['Canal de ventas'] == canal]
        df_ant = df_ant[df_ant['Canal de ventas'] == canal]
    if categoria != 'Todas':
        df_act = df_act[df_act['Categoria'] == categoria]
        df_ant = df_ant[df_ant['Categoria'] == categoria]
    if marca != 'Todas':
        df_act = df_act[df_act['Marca'] == marca]
        df_ant = df_ant[df_ant['Marca'] == marca]
    if ejecutivo != 'Todos':
        df_act = df_act[df_act['Ejecutivo'] == ejecutivo]
        df_ant = df_ant[df_ant['Ejecutivo'] == ejecutivo]
    if cliente != 'Todos':
        df_act = df_act[df_act['Razon Social'] == cliente]
        df_ant = df_ant[df_ant['Razon Social'] == cliente]

    return df_act, df_ant, año_act, año_ant, meses_sel


# ============================================================
# KPI ROW
# ============================================================
def render_kpis(df_act, df_ant):
    cajas_a = df_act['Cajas_Final'].sum()
    cajas_b = df_ant['Cajas_Final'].sum()
    neto_a = df_act['Neto_Final'].sum()
    neto_b = df_ant['Neto_Final'].sum()
    costo_a = df_act['Costo Total'].sum()
    costo_b = df_ant['Costo Total'].sum()
    util_a = df_act['Utilidad'].sum()
    util_b = df_ant['Utilidad'].sum()
    mg_a = util_a / neto_a if neto_a else 0
    mg_b = util_b / neto_b if neto_b else 0
    uu_a = util_a / cajas_a if cajas_a else 0
    uu_b = util_b / cajas_b if cajas_b else 0

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        kpi_card("Cajas 9L", fmt_n(cajas_a), var_pct(cajas_a, cajas_b))
    with c2:
        kpi_card("Venta Neta", fmt_m(neto_a), var_pct(neto_a, neto_b), card_class="kpi-card-gold")
    with c3:
        kpi_card("Costo", fmt_m(costo_a), var_pct(abs(costo_a), abs(costo_b)), card_class="kpi-card-red")
    with c4:
        kpi_card("Utilidad", fmt_m(util_a), var_pct(util_a, util_b), card_class="kpi-card-green")
    with c5:
        kpi_card("% Margen", fmt_pct(mg_a), mg_a - mg_b, suffix="")
    with c6:
        kpi_card("Util. Unitaria", fmt_n(uu_a), var_pct(uu_a, uu_b), prefix="$")


# ============================================================
# TAB 1: RESUMEN EJECUTIVO
# ============================================================
def tab_resumen(df, df_act, df_ant, año_act, año_ant, meses_sel):
    render_kpis(df_act, df_ant)
    st.markdown("")

    # --- Charts ---
    col_ch1, col_ch2 = st.columns(2)

    CHART_LAYOUT = dict(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#1B2A4A'),
        legend=dict(orientation='h', y=1.12, font=dict(size=11)),
        margin=dict(t=30, b=40, l=50, r=20),
    )

    with col_ch1:
        section("VENTA NETA POR CANAL (MM$)")
        canal_act = df_act.groupby('Canal de ventas')['Neto_Final'].sum().reset_index()
        canal_ant = df_ant.groupby('Canal de ventas')['Neto_Final'].sum().reset_index()
        if len(canal_act) > 0 or len(canal_ant) > 0:
            fig = go.Figure()
            if len(canal_ant) > 0:
                fig.add_trace(go.Bar(name=str(año_ant), x=canal_ant['Canal de ventas'],
                    y=canal_ant['Neto_Final'], marker_color='#BDC3C7',
                    text=canal_ant['Neto_Final'].apply(lambda x: fmt_m(x)),
                    textposition='outside', textfont=dict(size=10)))
            if len(canal_act) > 0:
                fig.add_trace(go.Bar(name=str(año_act), x=canal_act['Canal de ventas'],
                    y=canal_act['Neto_Final'],
                    marker=dict(color=AZUL, line=dict(width=0)),
                    text=canal_act['Neto_Final'].apply(lambda x: fmt_m(x)),
                    textposition='outside', textfont=dict(size=11, color=AZUL_OSCURO)))
            fig.update_layout(**CHART_LAYOUT, barmode='group', height=370)
            fig.update_yaxes(tickformat=',.0f', gridcolor='#f0f0f0', gridwidth=1)
            fig.update_xaxes(tickfont=dict(size=11, color='#333'))
            st.plotly_chart(fig, use_container_width=True)

    with col_ch2:
        section("TENDENCIA MENSUAL VENTA NETA (MM$)")
        mes_act = df_act.groupby('Mes')['Neto_Final'].sum().reset_index()
        mes_ant = df_ant.groupby('Mes')['Neto_Final'].sum().reset_index()
        fig2 = go.Figure()
        if len(mes_ant) > 0:
            mes_ant_s = mes_ant.sort_values('Mes')
            fig2.add_trace(go.Scatter(name=str(año_ant), x=mes_ant_s['Mes'].map(MESES),
                y=mes_ant_s['Neto_Final'], mode='lines+markers',
                line=dict(color='#BDC3C7', width=2, dash='dot'),
                marker=dict(size=6, color='#BDC3C7')))
        if len(mes_act) > 0:
            mes_act_s = mes_act.sort_values('Mes')
            fig2.add_trace(go.Scatter(name=str(año_act), x=mes_act_s['Mes'].map(MESES),
                y=mes_act_s['Neto_Final'], mode='lines+markers+text',
                line=dict(color=AZUL, width=3),
                marker=dict(size=8, color=AZUL, line=dict(width=2, color='white')),
                text=mes_act_s['Neto_Final'].apply(lambda x: fmt_m(x)),
                textposition='top center', textfont=dict(size=9, color=AZUL_OSCURO)))
            fig2.add_trace(go.Scatter(name='', x=mes_act_s['Mes'].map(MESES),
                y=mes_act_s['Neto_Final'], fill='tozeroy', showlegend=False,
                line=dict(width=0), fillcolor='rgba(46,80,144,0.08)'))
        fig2.update_layout(**CHART_LAYOUT, height=370)
        fig2.update_yaxes(tickformat=',.0f', gridcolor='#f0f0f0', gridwidth=1)
        st.plotly_chart(fig2, use_container_width=True)

    # --- Ventas por Canal ---
    section(f"VENTAS POR CANAL — {año_act} vs {año_ant}")
    comp_canal = build_comparison_df(df_act, df_ant, 'Canal de ventas', año_act, año_ant)
    render_comparison_table(comp_canal, 'Canal de ventas', año_act, año_ant, f'Neto_{año_act}')

    # --- Ventas por Mes ---
    section(f"VENTAS POR MES — {año_act} vs {año_ant}")
    df_act_m = df_act.copy()
    df_ant_m = df_ant.copy()
    df_act_m['Mes_Sort'] = df_act_m['Mes']
    df_ant_m['Mes_Sort'] = df_ant_m['Mes']
    df_act_m['Mes_Label'] = df_act_m['Mes'].map(MESES)
    df_ant_m['Mes_Label'] = df_ant_m['Mes'].map(MESES)
    comp_mes = build_comparison_df(df_act_m, df_ant_m, 'Mes', año_act, año_ant)
    comp_mes = comp_mes.sort_values('Mes')
    comp_mes['Mes'] = comp_mes['Mes'].map(MESES)
    render_comparison_table(comp_mes, 'Mes', año_act, año_ant)

    # --- Ranking por Marca ---
    section(f"RANKING DE RENTABILIDAD POR MARCA — {año_act} vs {año_ant}")
    comp_marca = build_comparison_df(df_act, df_ant, 'Marca', año_act, año_ant)
    render_comparison_table(comp_marca, 'Marca', año_act, año_ant, f'Utilidad_{año_act}')

    # --- Insights ---
    if len(df_act) > 0:
        st.markdown("")
        section("ALERTAS E INSIGHTS")
        total_neto_a = df_act['Neto_Final'].sum()
        total_neto_b = df_ant['Neto_Final'].sum()
        var_neto = var_pct(total_neto_a, total_neto_b)
        if var_neto is not None:
            if var_neto < -0.05:
                insight(f"⚠️ Venta neta cae {abs(var_neto):.1%} vs {año_ant}. Revisar canales con mayor retroceso.")
            elif var_neto > 0.05:
                insight(f"✅ Venta neta crece {var_neto:.1%} vs {año_ant}.")

        if len(comp_marca) > 0:
            top = comp_marca.sort_values(f'Mg_{año_act}', ascending=False).head(3)
            nombres = ", ".join(top['Marca'].tolist())
            insight(f"🏆 Marcas con mejor margen: {nombres}")

            bot = comp_marca[comp_marca[f'Neto_{año_act}'] > 0].sort_values(f'Mg_{año_act}').head(3)
            if len(bot) > 0:
                nombres_b = ", ".join(bot['Marca'].tolist())
                insight(f"📉 Marcas con menor margen: {nombres_b}")


# ============================================================
# TAB 2: SUPERMERCADO
# ============================================================
def tab_supermercado(df, df_act, df_ant, año_act, año_ant):
    df_s_act = df_act[df_act['Canal de ventas'] == 'Supermercado'].copy()
    df_s_ant = df_ant[df_ant['Canal de ventas'] == 'Supermercado'].copy()

    render_kpis(df_s_act, df_s_ant)
    st.markdown("")

    section(f"VENTAS POR SUPERMERCADO — {año_act}")
    build_super_detail(df_s_act, df_s_ant, 'Razon Social', año_act, año_ant)

    section(f"VENTAS POR MES — {año_act} vs {año_ant}")
    df_s_act_m = df_s_act.copy()
    df_s_ant_m = df_s_ant.copy()
    comp_mes = build_comparison_df(df_s_act_m, df_s_ant_m, 'Mes', año_act, año_ant)
    comp_mes = comp_mes.sort_values('Mes')
    comp_mes['Mes'] = comp_mes['Mes'].map(MESES)
    render_comparison_table(comp_mes, 'Mes', año_act, año_ant)

    section(f"VENTAS POR CATEGORÍA — {año_act}")
    build_super_detail(df_s_act, df_s_ant, 'Categoria', año_act, año_ant)

    section(f"VENTAS POR MARCA — {año_act}")
    build_super_detail(df_s_act, df_s_ant, 'Marca', año_act, año_ant)

    section("PARTICIPACION VENTA NETA POR CLIENTE")
    if len(df_s_act) > 0:
        cli = df_s_act.groupby('Razon Social')['Neto_Final'].sum().reset_index().sort_values('Neto_Final', ascending=False)
        colors = ['#1B2A4A', '#2E5090', '#4472C4', '#6B9BD2', '#A8C8E8']
        fig = go.Figure(go.Pie(labels=cli['Razon Social'], values=cli['Neto_Final'],
            hole=0.45, marker=dict(colors=colors[:len(cli)], line=dict(color='white', width=2)),
            textinfo='percent+label', textfont=dict(size=11),
            insidetextorientation='radial'))
        fig.update_layout(height=420, margin=dict(t=20, b=20, l=20, r=20),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Inter'), showlegend=False,
            annotations=[dict(text='Venta<br>Neta', x=0.5, y=0.5, font_size=14,
                             font_color='#1B2A4A', showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# TAB 3: MAYORISTA
# ============================================================
def tab_mayorista(df, df_act, df_ant, año_act, año_ant):
    df_m_act = df_act[df_act['Canal de ventas'] == 'Mayorista'].copy()
    df_m_ant = df_ant[df_ant['Canal de ventas'] == 'Mayorista'].copy()

    render_kpis(df_m_act, df_m_ant)
    st.markdown("")

    # Ventas por Ejecutivo
    section(f"VENTAS POR EJECUTIVO — {año_act} vs {año_ant}")
    comp_ej = build_comparison_df(df_m_act, df_m_ant, 'Ejecutivo', año_act, año_ant)
    render_comparison_table(comp_ej, 'Ejecutivo', año_act, año_ant, f'Neto_{año_act}')

    # Ventas por Mes
    section(f"VENTAS POR MES — {año_act} vs {año_ant}")
    comp_mes = build_comparison_df(df_m_act, df_m_ant, 'Mes', año_act, año_ant)
    comp_mes = comp_mes.sort_values('Mes')
    comp_mes['Mes'] = comp_mes['Mes'].map(MESES)
    render_comparison_table(comp_mes, 'Mes', año_act, año_ant)

    # Ranking por Marca
    section(f"RANKING POR MARCA — {año_act} vs {año_ant}")
    comp_marca = build_comparison_df(df_m_act, df_m_ant, 'Marca', año_act, año_ant)
    render_comparison_table(comp_marca, 'Marca', año_act, año_ant, f'Utilidad_{año_act}')

    CHART_LAYOUT_M = dict(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color='#1B2A4A'), margin=dict(t=10, b=20, l=10, r=10),
    )

    col1, col2 = st.columns(2)
    with col1:
        section("VENTA POR EJECUTIVO")
        if len(df_m_act) > 0:
            ej = df_m_act.groupby('Ejecutivo')['Neto_Final'].sum().reset_index().sort_values('Neto_Final', ascending=True)
            fig = go.Figure(go.Bar(y=ej['Ejecutivo'], x=ej['Neto_Final'], orientation='h',
                marker=dict(color=AZUL, line=dict(width=0)),
                text=ej['Neto_Final'].apply(fmt_m), textposition='outside', textfont=dict(size=10)))
            fig.update_layout(**CHART_LAYOUT_M, height=320)
            fig.update_xaxes(tickformat=',.0f', gridcolor='#f0f0f0')
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        section("TOP 10 CLIENTES")
        if len(df_m_act) > 0:
            cli = df_m_act.groupby('Razon Social')['Neto_Final'].sum().reset_index().sort_values('Neto_Final', ascending=False).head(10)
            cli = cli.sort_values('Neto_Final', ascending=True)
            fig = go.Figure(go.Bar(y=cli['Razon Social'], x=cli['Neto_Final'], orientation='h',
                marker=dict(color=VERDE, line=dict(width=0)),
                text=cli['Neto_Final'].apply(fmt_m), textposition='outside', textfont=dict(size=10)))
            fig.update_layout(**CHART_LAYOUT_M, height=320)
            fig.update_xaxes(tickformat=',.0f', gridcolor='#f0f0f0')
            st.plotly_chart(fig, use_container_width=True)


# ============================================================
# TAB 4: RESUMEN VINOS
# ============================================================
def tab_vinos(df, df_act, df_ant, año_act, año_ant):
    cats_vino = ['Vino', 'Vino Saldos', 'Vino Coctel', 'Saldos']
    df_v_act = df_act[df_act['Categoria'].isin(cats_vino)].copy()
    df_v_ant = df_ant[df_ant['Categoria'].isin(cats_vino)].copy()

    render_kpis(df_v_act, df_v_ant)
    st.markdown("")

    col1, col2 = st.columns(2)

    with col1:
        section(f"VENTAS POR CATEGORÍA — {año_act} vs {año_ant}")
        comp_cat = build_comparison_df(df_v_act, df_v_ant, 'Categoria', año_act, año_ant)
        render_comparison_table(comp_cat, 'Categoria', año_act, año_ant, f'Neto_{año_act}')

    with col2:
        section(f"VENTAS POR MES — {año_act} vs {año_ant}")
        comp_mes = build_comparison_df(df_v_act, df_v_ant, 'Mes', año_act, año_ant)
        comp_mes = comp_mes.sort_values('Mes')
        comp_mes['Mes'] = comp_mes['Mes'].map(MESES)
        render_comparison_table(comp_mes, 'Mes', año_act, año_ant)

    # Ventas por Marca de Vino
    section(f"RANKING POR MARCA — VINOS {año_act} vs {año_ant}")
    comp_marca = build_comparison_df(df_v_act, df_v_ant, 'Marca', año_act, año_ant)
    render_comparison_table(comp_marca, 'Marca', año_act, año_ant, f'Neto_{año_act}')

    # Cepa analysis if available
    if 'Cepa' in df_v_act.columns:
        cepas_act = df_v_act[df_v_act['Cepa'].astype(str) != '0']
        if len(cepas_act) > 0:
            section(f"VENTAS POR CEPA — {año_act}")
            cepas_ant = df_v_ant[df_v_ant['Cepa'].astype(str) != '0']
            comp_cepa = build_comparison_df(cepas_act, cepas_ant, 'Cepa', año_act, año_ant)
            render_comparison_table(comp_cepa, 'Cepa', año_act, año_ant, f'Neto_{año_act}')

    # Linea Vino if available
    if 'Linea Vino' in df_v_act.columns:
        lineas_act = df_v_act[df_v_act['Linea Vino'].astype(str) != '0']
        if len(lineas_act) > 0:
            section(f"VENTAS POR LÍNEA DE VINO — {año_act}")
            lineas_ant = df_v_ant[df_v_ant['Linea Vino'].astype(str) != '0']
            comp_linea = build_comparison_df(lineas_act, lineas_ant, 'Linea Vino', año_act, año_ant)
            render_comparison_table(comp_linea, 'Linea Vino', año_act, año_ant, f'Neto_{año_act}')

    section("TENDENCIA MENSUAL VINOS (MM$)")
    mes_v_act = df_v_act.groupby('Mes')['Neto_Final'].sum().reset_index().sort_values('Mes')
    mes_v_ant = df_v_ant.groupby('Mes')['Neto_Final'].sum().reset_index().sort_values('Mes')
    fig = go.Figure()
    if len(mes_v_ant) > 0:
        fig.add_trace(go.Scatter(name=str(año_ant), x=mes_v_ant['Mes'].map(MESES),
            y=mes_v_ant['Neto_Final'], mode='lines+markers',
            line=dict(color='#BDC3C7', width=2, dash='dot'), marker=dict(size=6)))
    if len(mes_v_act) > 0:
        fig.add_trace(go.Scatter(name=str(año_act), x=mes_v_act['Mes'].map(MESES),
            y=mes_v_act['Neto_Final'], mode='lines+markers',
            line=dict(color='#8B0000', width=3), marker=dict(size=8, line=dict(width=2, color='white'))))
        fig.add_trace(go.Scatter(name='', x=mes_v_act['Mes'].map(MESES),
            y=mes_v_act['Neto_Final'], fill='tozeroy', showlegend=False,
            line=dict(width=0), fillcolor='rgba(139,0,0,0.06)'))
    fig.update_layout(height=370, margin=dict(t=30, b=40, l=50, r=20),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter'), legend=dict(orientation='h', y=1.12))
    fig.update_yaxes(tickformat=',.0f', gridcolor='#f0f0f0')
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# MAIN
# ============================================================
try:
    df = cargar_datos()
except Exception as e:
    st.error(f"Error cargando datos: {e}")
    st.info("Verifica que el Google Sheet esté compartido como 'Cualquier persona con el enlace'")
    st.stop()

df_act, df_ant, año_act, año_ant, meses_sel = sidebar_filters(df)

meses_txt = f"{MESES[meses_sel[0]]} a {MESES[meses_sel[-1]]}" if len(meses_sel) > 1 else MESES[meses_sel[0]]
n_reg = len(df_act)
n_cli = df_act['Razon Social'].nunique()
total_cajas = df_act['Cajas_Final'].sum()

st.markdown(f"""
<div class="corp-header">
    <h1>Dashboard Rentabilidad — Mercado Nacional</h1>
    <div class="subtitle">Vina de Aguirre · Mercado Nacional · {meses_txt} {año_act}</div>
    <div class="badge">{n_reg:,} registros &nbsp;|&nbsp; {n_cli} clientes &nbsp;|&nbsp; {total_cajas:,.0f} cajas 9L</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Resumen Ejecutivo",
    "🏪 Supermercado",
    "📦 Mayorista",
    "🍷 Resumen Vinos"
])

with tab1:
    tab_resumen(df, df_act, df_ant, año_act, año_ant, meses_sel)
with tab2:
    tab_supermercado(df, df_act, df_ant, año_act, año_ant)
with tab3:
    tab_mayorista(df, df_act, df_ant, año_act, año_ant)
with tab4:
    tab_vinos(df, df_act, df_ant, año_act, año_ant)

st.markdown("""
<div class="corp-footer">
    <strong>Vina de Aguirre</strong> · Dashboard Rentabilidad Mercado Nacional<br>
    Datos actualizados desde Google Sheets · Cache 5 minutos
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="text-align:center; padding:10px;">
    <div style="font-size:18px; font-weight:800; color:#C9960C;">VA</div>
    <div style="font-size:10px; color:#87CEEB; margin-top:4px;">VINA DE AGUIRRE</div>
    <div style="font-size:9px; color:#6B7B8D; margin-top:8px;">Dashboard CFO</div>
</div>
""", unsafe_allow_html=True)
