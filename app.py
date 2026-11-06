import base64
import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as gg
from plotly.subplots import make_subplots
import streamlit as st

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & THEME STATE
# ---------------------------------------------------------
st.set_page_config(
    page_title="FleetCare Analytics | Diagnostic & Maintenance Prédictive",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded",
)

if 'theme' not in st.session_state:
  st.session_state['theme'] = 'dark'

if 'authenticated' not in st.session_state:
  st.session_state['authenticated'] = False

if 'user_role' not in st.session_state:
  st.session_state['user_role'] = None

# Chargement automatique de l'image d'arrière-plan si présente, sinon fallback
bg_image_path = "Automobile_1.jpg"
if os.path.exists(bg_image_path):
  with open(bg_image_path, "rb") as img_file:
    BACKGROUND_IMAGE_B64 = base64.b64encode(img_file.read()).decode("utf-8")
else:
  BACKGROUND_IMAGE_B64 = ""

# ---------------------------------------------------------
# 2. DICTIONNAIRE DE TRADUCTION
# ---------------------------------------------------------
translations = {
    "Français": {
        "page_title": (
            "FleetCare Analytics | Diagnostic & Maintenance Prédictive"
        ),
        "login_portal": "Connexion Plateforme",
        "login_sub": (
            "Accédez au portail d'analyse et de gestion de votre flotte"
            " automobile 🚘"
        ),
        "user_label": "👤 Identifiant",
        "pass_label": "🔑 Mot de passe",
        "role_label": "🎯 Rôle",
        "roles": [
            "Responsable Flotte",
            "Ingénieur Maintenance",
            "Analyste Data Science",
        ],
        "login_btn": "🚀 Se Connecter",
        "login_success": "Connexion réussie ! Redirection...",
        "login_error": (
            "Identifiants incorrects (Indice: admin / fleetcare2026)"
        ),
        "sidebar_filters": "🔍 Filtres & Paramètres",
        "period_label": "Période d'analyse 📅",
        "model_label": "Modèle de véhicule 🚚",
        "all_models": "Tous",
        "health_filter": "Filtre état santé 🔧",
        "health_options": ["Tous", "Pannes détectées", "Sans Panne"],
        "nav_title": "📌 Navigation",
        "menu_items": [
            "📊 Tableau de Bord Global",
            "🔧 Maintenance Prédictive & IA",
            "🚘 Analyse par Véhicule",
            "🧹 Nettoyage & Data Quality",
        ],
        "user_connected": "Utilisateur:",
        "logout_btn": "🚪 Déconnexion",
        "dash_title": "📊 FleetCare Analytics — Dashboard Exécutif",
        "dash_sub": (
            "Aperçu télématique globale de la flotte et indicateurs clés de"
            " performance."
        ),
        "kpi_active": "Véhicules Actifs 🚘",
        "kpi_active_sub": "Flotte sous contrôle",
        "kpi_health": "Santé Globale Moyenne 🤖",
        "kpi_health_sub": "Indice de Fiabilité",
        "kpi_pannes": "Pannes Enregistrées 🔧",
        "kpi_km": "Kilométrage Parcouru 🛣️",
        "predict_title": "🤖 Maintenance Prédictive & Algorithmes IA",
        "predict_sub": (
            "Détection anticipée du risque de panne sous 30 jours"
            " (panne_dans_30j)."
        ),
        "vehicle_title": "🚘 Diagnostic Individuel de Véhicule",
        "vehicle_sub": (
            "Sélectionnez un véhicule pour examiner l'historique chronologique"
            " complet de ses capteurs."
        ),
        "data_title": "🧹 Qualité des Données & Contrôle Pandas",
        "data_sub": (
            "Inspection du jeu de données brut `akhdaich_marwa.csv` et"
            " vérification des règles métier."
        ),
    },
    "English": {
        "page_title": (
            "FleetCare Analytics | Diagnostic & Predictive Maintenance"
        ),
        "login_portal": "Platform Login",
        "login_sub": "Access your fleet analysis and management portal 🚘",
        "user_label": "👤 Username",
        "pass_label": "🔑 Password",
        "role_label": "🎯 Role",
        "roles": [
            "Fleet Manager",
            "Maintenance Engineer",
            "Data Science Analyst",
        ],
        "login_btn": "🚀 Login",
        "login_success": "Login successful! Redirecting...",
        "login_error": (
            "Incorrect credentials (Hint: admin / fleetcare2026)"
        ),
        "sidebar_filters": "🔍 Filters & Settings",
        "period_label": "Analysis Period 📅",
        "model_label": "Vehicle Model 🚚",
        "all_models": "All",
        "health_filter": "Health Filter 🔧",
        "health_options": ["All", "Failures Detected", "No Failure"],
        "nav_title": "📌 Navigation",
        "menu_items": [
            "📊 Global Dashboard",
            "🔧 Predictive Maintenance & AI",
            "🚘 Vehicle Analysis",
            "🧹 Data Quality & Cleaning",
        ],
        "user_connected": "User:",
        "logout_btn": "🚪 Logout",
        "dash_title": "📊 FleetCare Analytics — Executive Dashboard",
        "dash_sub": (
            "Global fleet telemetry overview and key performance indicators."
        ),
        "kpi_active": "Active Vehicles 🚘",
        "kpi_active_sub": "Fleet under control",
        "kpi_health": "Average Overall Health 🤖",
        "kpi_health_sub": "Reliability Index",
        "kpi_pannes": "Recorded Failures 🔧",
        "kpi_km": "Distance Traveled 🛣️",
        "predict_title": "🤖 Predictive Maintenance & AI Algorithms",
        "predict_sub": (
            "Early detection of failure risk within 30 days (panne_dans_30j)."
        ),
        "vehicle_title": "🚘 Individual Vehicle Diagnosis",
        "vehicle_sub": (
            "Select a vehicle to inspect its complete sensor historical data."
        ),
        "data_title": "🧹 Data Quality & Pandas Control",
        "data_sub": (
            "Inspection of raw dataset `akhdaich_marwa.csv` and business rule"
            " verification."
        ),
    },
    "Español": {
        "page_title": (
            "FleetCare Analytics | Diagnóstico y Mantenimiento Predictivo"
        ),
        "login_portal": "Conexión a la Plataforma",
        "login_sub": (
            "Acceda al portal de análisis y gestión de su flota de vehículos 🚘"
        ),
        "user_label": "👤 Usuario",
        "pass_label": "🔑 Contraseña",
        "role_label": "🎯 Rol",
        "roles": [
            "Responsable de Flota",
            "Ingeniero de Mantenimiento",
            "Analista de Ciencia de Datos",
        ],
        "login_btn": "🚀 Iniciar Sesión",
        "login_success": "¡Conexión exitosa! Redirigiendo...",
        "login_error": (
            "Credenciales incorrectas (Pista: admin / fleetcare2026)"
        ),
        "sidebar_filters": "🔍 Filtros y Parámetros",
        "period_label": "Período de análisis 📅",
        "model_label": "Modelo de vehículo 🚚",
        "all_models": "Todos",
        "health_filter": "Filtro de estado 🔧",
        "health_options": ["Todos", "Averías detectadas", "Sin Avería"],
        "nav_title": "📌 Navegación",
        "menu_items": [
            "📊 Tablero de Control Global",
            "🔧 Mantenimiento Predictivo e IA",
            "🚘 Análisis por Vehículo",
            "🧹 Calidad de Datos y Limpieza",
        ],
        "user_connected": "Usuario:",
        "logout_btn": "🚪 Cerrar Sesión",
        "dash_title": "📊 FleetCare Analytics — Tablero Ejecutivo",
        "dash_sub": (
            "Resumen telemático global de la flota e indicadores clave de"
            " rendimiento."
        ),
        "kpi_active": "Vehículos Activos 🚘",
        "kpi_active_sub": "Flota bajo control",
        "kpi_health": "Salud Global Promedio 🤖",
        "kpi_health_sub": "Índice de Fiabilidad",
        "kpi_pannes": "Averías Registradas 🔧",
        "kpi_km": "Kilometraje Recorrido 🛣️",
        "predict_title": "🤖 Mantenimiento Predictivo y Algoritmos IA",
        "predict_sub": (
            "Detección temprana del riesgo de avería en 30 días"
            " (panne_dans_30j)."
        ),
        "vehicle_title": "🚘 Diagnóstico Individual de Vehículo",
        "vehicle_sub": (
            "Seleccione un vehículo para examinar el historial cronológico"
            " completo de sus sensores."
        ),
        "data_title": "🧹 Calidad de Datos y Control Pandas",
        "data_sub": (
            "Inspección del conjunto de datos bruto `akhdaich_marwa.csv` y"
            " verificación de reglas de negocio."
        ),
    },
}

# ---------------------------------------------------------
# 3. SÉLECTION DE LA LANGUE DANS LA SIDEBAR
# ---------------------------------------------------------
selected_lang = st.sidebar.selectbox(
    "🌐 Langue / Language / Idioma", ["Français", "English", "Español"]
)
t = translations[selected_lang]


# ---------------------------------------------------------
# 4. CUSTOM CSS & STYLING (AVEC ARRIÈRE-PLAN AUTOMOBILE ET LABELS EN BLANC)
# ---------------------------------------------------------
def apply_custom_css():
  is_dark = st.session_state['theme'] == 'dark'

  bg_color = "#0B1424" if is_dark else "#F3F6FA"
  card_bg = "rgba(17, 31, 51, 0.90)" if is_dark else "rgba(255, 255, 255, 0.92)"
  text_color = "#FFFFFF" if is_dark else "#102B4E"
  subtext_color = "#A0AEC0" if is_dark else "#DFE7F4"
  border_color = "#CFDEEE" if is_dark else "#EAF1F8"

  bg_style = (
      f"""
        background: linear-gradient(rgba(11, 20, 36, 0.75), rgba(11, 20, 36, 0.88)),
                    url("data:image/jpeg;base64,{BACKGROUND_IMAGE_B64}") no-repeat center top fixed;
        background-size: 100% 100%;
    """
      if BACKGROUND_IMAGE_B64
      else f"background-color: {bg_color};"
  )

  st.markdown(
      f"""
        <style>
        .stApp {{
            {bg_style}
            color: {text_color};
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        [data-testid="stSidebar"] {{
            background-color: {"#102B4E" if is_dark else "#1D4772"};
            border-right: 1px solid #1D4772;
        }}
        /* Cible tous les labels, titres et textes des widgets de la sidebar pour forcer le blanc pur */
        [data-testid="stSidebar"] label, 
        [data-testid="stSidebar"] label p, 
        [data-testid="stSidebar"] label span, 
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] span, 
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] div[data-baseweb="select"] span {{
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }}
        /* Suppression de la marge blanche tout en haut de la page Streamlit */
        .block-container {{
            padding-top: 2rem !important;
        }}
        .stRadio label p {{
            color: white !important;
            font-weight: 500;
        }}
        .login-card {{
            background-color: {card_bg};
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid {border_color};
            border-radius: 16px;
            padding: 35px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            max-width: 460px;
            margin: 0 auto;
        }}
        .kpi-card {{
            background-color: {card_bg};
            border: 1px solid {border_color};
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
            margin-bottom: 15px;
        }}
        .kpi-title {{
            font-size: 0.9rem;
            font-weight: 600;
            color: {subtext_color};
            text-transform: uppercase;
        }}
        .kpi-value {{
            font-size: 1.8rem;
            font-weight: 800;
            color: {text_color};
            margin: 8px 0;
        }}
        .badge-success {{ color: #16A36A; font-weight: 700; }}
        .badge-danger {{ color: #DC3545; font-weight: 700; }}
        .badge-warning {{ color: #F59E0B; font-weight: 700; }}
        .stButton>button {{
            background-color: #1D4772;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            padding: 0.6rem 1.2rem;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background-color: #16A36A;
            box-shadow: 0 4px 12px rgba(22, 163, 106, 0.4);
        }}
        </style>
    """,
      unsafe_allow_html=True,
  )


apply_custom_css()


# ---------------------------------------------------------
# 5. DATA LOADING & CLEANING (PANDAS)
# ---------------------------------------------------------
@st.cache_data
def load_and_clean_data():
  file_path = "data/akhdaich_marwa.csv"
  if not os.path.exists(file_path):
    file_path = "akhdaich_marwa.csv"

  df = pd.read_csv(file_path)
  df['date'] = pd.to_datetime(df['date'])
  df.drop_duplicates(inplace=True)

  string_cols = [
      'vehicule_id',
      'modele',
      'code_defaut_obd',
      'composant_en_panne',
      'type_maintenance',
  ]
  for col in string_cols:
    if col in df.columns:
      df[col] = df[col].astype(str).str.strip()

  return df


try:
  df_raw = load_and_clean_data()
except Exception as e:
  st.error(f"Erreur lors du chargement des données : {e}")
  st.stop()


# ---------------------------------------------------------
# 6. LOGO DISPLAY & BRANDING
# ---------------------------------------------------------
def render_logo(width="280px"):
  logo_html = f"""
    <div style="display: flex; justify-content: center; width: 100%; padding: 10px 0;">
        <div style="background: linear-gradient(135deg, #102B4E 0%, #1D4772 100%); 
                    border: 2px solid #16A36A; border-radius: 14px; padding: 15px; 
                    box-shadow: 0 6px 18px rgba(0,0,0,0.25); width: {width}; text-align: center;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 12px;">
                <span style="font-size: 2.2rem;">🚚</span>
                <div style="text-align: left;">
                    <div style="font-size: 1.4rem; font-weight: 900; color: #FFFFFF; letter-spacing: 1px; line-height: 1.1;">FLEETCARE</div>
                    <div style="font-size: 0.85rem; font-weight: 700; color: #16A36A; letter-spacing: 3px;">ANALYTICS 🤖</div>
                </div>
            </div>
            <div style="font-size: 0.75rem; color: #EAF1F8; margin-top: 8px; font-weight: 500; border-top: 1px solid rgba(255,255,255,0.15); padding-top: 6px;">
                ⚙️ Maintenance Prédictive & IoT
            </div>
        </div>
    </div>
    """
  st.markdown(logo_html, unsafe_allow_html=True)


# ---------------------------------------------------------
# 7. AUTHENTICATION (LOGIN PAGE)
# ---------------------------------------------------------
if not st.session_state['authenticated']:
  st.markdown("<br><br>", unsafe_allow_html=True)
  render_logo(width="380px")
  st.markdown("<br>", unsafe_allow_html=True)

  col1, col2, col3 = st.columns([1, 2, 1])
  with col2:
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #FFFFFF; font-weight: 700; margin-bottom: 5px;">{t["login_portal"]}</h2>
            <p style="color: #A0AEC0; font-size: 0.92rem;">{t["login_sub"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
      username = st.text_input(t["user_label"], value="")
      password = st.text_input(t["pass_label"], type="password", value="")
      role = st.selectbox(t["role_label"], t["roles"])

      submit = st.form_submit_button(t["login_btn"], use_container_width=True)

      if submit:
        if username in ["admin", "demo", "marwa"] and password in [
            "fleetcare2026",
            "admin",
            "1234",
        ]:
          st.session_state['authenticated'] = True
          st.session_state['user_role'] = role
          st.success(t["login_success"])
          st.rerun()
        else:
          st.error(t["login_error"])
    st.markdown("</div>", unsafe_allow_html=True)

  st.stop()

# ---------------------------------------------------------
# 8. SIDEBAR & FILTRES
# ---------------------------------------------------------
with st.sidebar:
  render_logo(width="100%")
  st.markdown("<br>", unsafe_allow_html=True)

  col_t1, col_t2 = st.columns([3, 1])
  with col_t1:
    st.write(
        f"Mode:"
        f" **{'🌙 Dark' if st.session_state['theme']=='dark' else '☀️ Light'}**"
    )
  with col_t2:
    if st.button("🔄"):
      st.session_state['theme'] = (
          'light' if st.session_state['theme'] == 'dark' else 'dark'
      )
      st.rerun()

  st.markdown("---")
  st.markdown(f"### {t['sidebar_filters']}")

  min_date = df_raw['date'].min().date()
  max_date = df_raw['date'].max().date()
  date_range = st.date_input(
      t["period_label"],
      value=(min_date, max_date),
      min_value=min_date,
      max_value=max_date,
  )

  modeles = [t["all_models"]] + list(df_raw['modele'].unique())
  selected_modele = st.selectbox(t["model_label"], modeles)

  statut_panne = st.radio(t["health_filter"], t["health_options"])

  st.markdown("---")
  st.markdown(f"### {t['nav_title']}")
  menu = st.radio("Sélectionnez un module :", t["menu_items"])

  st.markdown("---")
  st.write(
      f"👤 **{t['user_connected']}**"
      f" {st.session_state.get('user_role', 'Admin')}"
  )
  if st.button(t["logout_btn"], use_container_width=True):
    st.session_state['authenticated'] = False
    st.rerun()

# ---------------------------------------------------------
# 9. FILTERING DATASET
# ---------------------------------------------------------
df = df_raw.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
  start_d, end_d = date_range
  df = df[(df['date'].dt.date >= start_d) & (df['date'].dt.date <= end_d)]

if selected_modele != t["all_models"]:
  df = df[df['modele'] == selected_modele]

if statut_panne in ["Pannes détectées", "Failures Detected", "Averías detectadas"]:
  df = df[df['panne'] == 1]
elif statut_panne in ["Sans Panne", "No Failure", "Sin Avería"]:
  df = df[df['panne'] == 0]

# ---------------------------------------------------------
# 10. DASHBOARD MODULES
# ---------------------------------------------------------

# Module 1 : Tableau de Bord Global
if menu == t["menu_items"][0]:
  st.title(t["dash_title"])
  st.caption(t["dash_sub"])

  kpi1, kpi2, kpi3, kpi4 = st.columns(4)
  total_vehicules = df['vehicule_id'].nunique()
  nb_pannes = df['panne'].sum()
  taux_panne = (nb_pannes / len(df) * 100) if len(df) > 0 else 0
  sante_moyenne = (
      df[[
          'sante_moteur_pct',
          'sante_batterie_pct',
          'sante_freins_pct',
          'sante_transmission_pct',
      ]]
      .mean()
      .mean()
  )

  with kpi1:
    st.markdown(
        f"""<div class="kpi-card"><div class="kpi-title">{t["kpi_active"]}</div><div class="kpi-value">{total_vehicules}</div><div class="kpi-subtext badge-success">{t["kpi_active_sub"]}</div></div>""",
        unsafe_allow_html=True,
    )
  with kpi2:
    st.markdown(
        f"""<div class="kpi-card"><div class="kpi-title">{t["kpi_health"]}</div><div class="kpi-value">{sante_moyenne:.1f}%</div><div class="kpi-subtext badge-success">{t["kpi_health_sub"]}</div></div>""",
        unsafe_allow_html=True,
    )
  with kpi3:
    st.markdown(
        f"""<div class="kpi-card"><div class="kpi-title">{t["kpi_pannes"]}</div><div class="kpi-value">{nb_pannes}</div><div class="kpi-subtext badge-danger">Taux: {taux_panne:.1f}%</div></div>""",
        unsafe_allow_html=True,
    )
  with kpi4:
    st.markdown(
        f"""<div class="kpi-card"><div class="kpi-title">{t["kpi_km"]}</div><div class="kpi-value">{df['km_jour'].sum():,.0f} km</div><div class="kpi-subtext badge-success">Distance cumulée</div></div>""",
        unsafe_allow_html=True,
    )

  st.markdown("<br>", unsafe_allow_html=True)

  col_c1, col_c2 = st.columns(2)
  with col_c1:
    st.subheader("📈 Évolution Temporelle des Pannes et Température Moteur")
    df_daily = (
        df.groupby('date')
        .agg({'panne': 'sum', 'temp_moteur_C': 'mean'})
        .reset_index()
    )
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(
        gg.Scatter(
            x=df_daily['date'],
            y=df_daily['temp_moteur_C'],
            name="Temp. Moteur (°C)",
            line=dict(color='#1D4772', width=2),
        ),
        secondary_y=False,
    )
    fig1.add_trace(
        gg.Bar(
            x=df_daily['date'],
            y=df_daily['panne'],
            name="Nombre de Pannes",
            marker_color='#DC3545',
            opacity=0.6,
        ),
        secondary_y=True,
    )
    fig1.update_layout(
        template=(
            "plotly_dark"
            if st.session_state['theme'] == 'dark'
            else "plotly_white"
        ),
        margin=dict(l=20, r=20, t=30, b=20),
    )
    st.plotly_chart(fig1, use_container_width=True)

  with col_c2:
    st.subheader("🧩 Répartition des Composants en Panne")
    df_failures = (
        df[df['composant_en_panne'] != 'Aucun']['composant_en_panne']
        .value_counts()
        .reset_index()
    )
    fig2 = px.pie(
        df_failures,
        names='composant_en_panne',
        values='count',
        hole=0.4,
        color_discrete_sequence=[
            '#DC3545',
            '#F59E0B',
            '#1D4772',
            '#16A36A',
            '#102B4E',
        ],
    )
    fig2.update_layout(
        template=(
            "plotly_dark"
            if st.session_state['theme'] == 'dark'
            else "plotly_white"
        )
    )
    st.plotly_chart(fig2, use_container_width=True)

# Module 2 : Maintenance Prédictive
elif menu == t["menu_items"][1]:
  st.title(t["predict_title"])
  st.caption(t["predict_sub"])

  col_p1, col_p2 = st.columns([1, 2])
  with col_p1:
    st.markdown("### ⚠️ Véhicules Critiques")
    high_risk = (
        df[df['panne_dans_30j'] == 1]
        .groupby(['vehicule_id', 'modele'])
        .agg({
            'sante_moteur_pct': 'last',
            'jours_avant_panne': 'min',
            'code_defaut_obd': 'last',
        })
        .reset_index()
        .sort_values(by='jours_avant_panne')
    )
    st.dataframe(high_risk, height=400, use_container_width=True)

  with col_p2:
    st.subheader("🔥 Matrice de Corrélation Capteurs vs Pannes")
    num_cols = [
        'temp_moteur_C',
        'pression_huile_bar',
        'vibration_mm_s',
        'tension_batterie_V',
        'temp_freins_C',
        'usure_plaquettes_pct',
        'panne_dans_30j',
    ]
    corr = df[num_cols].corr()
    fig_corr = px.imshow(
        corr, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r"
    )
    fig_corr.update_layout(
        template=(
            "plotly_dark"
            if st.session_state['theme'] == 'dark'
            else "plotly_white"
        )
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# Module 3 : Analyse par Véhicule
elif menu == t["menu_items"][2]:
  st.title(t["vehicle_title"])
  st.caption(t["vehicle_sub"])

  selected_vh = st.selectbox(
      "Sélectionnez un identifiant véhicule :", sorted(df['vehicule_id'].unique())
  )
  df_vh = df[df['vehicule_id'] == selected_vh].sort_values('date')

  col_v1, col_v2, col_v3 = st.columns(3)
  col_v1.metric("Modèle", df_vh['modele'].iloc[0])
  col_v2.metric("Kilométrage Actuel", f"{df_vh['kilometrage'].max():,} km")
  col_v3.metric("Nombre total de pannes", int(df_vh['panne'].sum()))

  st.markdown("---")
  fig_vh = make_subplots(
      rows=2,
      cols=1,
      shared_xaxes=True,
      vertical_spacing=0.1,
      subplot_titles=("Températures (°C)", "Usure & Batterie"),
  )
  fig_vh.add_trace(
      gg.Scatter(
          x=df_vh['date'], y=df_vh['temp_moteur_C'], name="Temp. Moteur"
      ),
      row=1,
      col=1,
  )
  fig_vh.add_trace(
      gg.Scatter(
          x=df_vh['date'], y=df_vh['temp_freins_C'], name="Temp. Freins"
      ),
      row=1,
      col=1,
  )
  fig_vh.add_trace(
      gg.Scatter(
          x=df_vh['date'],
          y=df_vh['usure_plaquettes_pct'],
          name="Usure Plaquettes (%)",
      ),
      row=2,
      col=1,
  )
  fig_vh.add_trace(
      gg.Scatter(
          x=df_vh['date'],
          y=df_vh['tension_batterie_V'],
          name="Tension Batterie (V)",
      ),
      row=2,
      col=1,
  )
  fig_vh.update_layout(
      height=600,
      template=(
          "plotly_dark"
          if st.session_state['theme'] == 'dark'
          else "plotly_white"
      ),
  )
  st.plotly_chart(fig_vh, use_container_width=True)

# Module 4 : Nettoyage et Data Quality
elif menu == t["menu_items"][3]:
  st.title(t["data_title"])
  st.caption(t["data_sub"])

  col_q1, col_q2 = st.columns(2)
  with col_q1:
    st.subheader("📋 Valeurs Manquantes")
    null_df = df_raw.isnull().sum().reset_index()
    null_df.columns = ['Colonne', 'Nombre de NaNs']
    st.dataframe(null_df, use_container_width=True)
  with col_q2:
    st.subheader("ℹ️ Infos Structurelles")
    st.write(f"- **Total lignes:** `{len(df_raw):,}`")
    st.write(f"- **Total colonnes:** `{len(df_raw.columns)}`")
    st.write(
        f"- **Taille flotte:** `{df_raw['vehicule_id'].nunique()} véhicules`"
    )