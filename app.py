import streamlit as st
import pandas as pd
import re
import random
from fpdf import FPDF
import time

# Ustawienia strony dla urządzeń mobilnych
st.set_page_config(
    page_title="MaksStandard",
    page_icon="🍔",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CHRONIONY STAN SEKCJI ---
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "Główne"

# --- POMOCNICZE FUNKCJE ---
def clean_txt(text):
    if not isinstance(text, str):
        return ""
    replacements = {
        'ą':'a','ć':'c','ę':'e','ł':'l','ń':'n','ó':'o','ś':'s','ź':'z','ż':'z',
        'Ą':'A','Ć':'C','Ę':'E','Ł':'L','Ń':'N','Ó':'O','Ś':'S','Ź':'Z','Ż':'Z'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def scale_ingredient(text, multiplier):
    if multiplier == 1:
        return text
    def multiply_match(match):
        val = float(match.group(1))
        unit = match.group(2)
        scaled_val = val * multiplier
        if scaled_val.is_integer():
            return f"{int(scaled_val)}{unit}"
        else:
            return f"{round(scaled_val, 2)}{unit}"
    pattern = r"(\d+(?:\.\d+)?)\s*(g|dag|dkg|kg|szt|ml|l|plaster|plastry|lyzka|łyżka|lyzki|łyżeczka)"
    return re.sub(pattern, multiply_match, text, flags=re.IGNORECASE)

def generate_pdf(danie, porcje, skladniki_skalowane):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(190, 10, txt="MaksStandard - Karta Produkcji", align="C")
    pdf.ln(15)
    
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(190, 10, txt=f"Danie: {clean_txt(danie)}")
    pdf.ln(8)
    pdf.cell(190, 10, txt=f"Ilosc porcji: {porcje}")
    pdf.ln(12)
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(190, 10, txt="Lista przeliczonych skladnikow:")
    pdf.ln(8)
    
    pdf.set_font("Helvetica", "", 12)
    for item in skladniki_skalowane:
        pdf.cell(190, 8, txt=f"- {clean_txt(item)}")
        pdf.ln(8)
        
    pdf.ln(15)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(190, 10, txt="Wygenerowano automatycznie z aplikacji MaksStandard.", align="C")
    
    return bytes(pdf.output())

# --- DESZCZ JEDZENIA (generowany losowo dla wiekszej gleboko/roznorodnosci) ---
FOOD_EMOJIS = ["🍔", "🍕", "🍣", "🥪", "🌭", "🍟", "🍩", "🍦", "🍪", "🥤", "🧁", "🍿", "🥗", "🍗", "🍫"]

def generate_food_rain(n=18):
    particles = []
    for _ in range(n):
        emoji = random.choice(FOOD_EMOJIS)
        left = random.uniform(2, 96)
        duration = random.uniform(9, 20)
        delay = -random.uniform(0, duration)
        size = random.randint(15, 30)
        opacity = round(random.uniform(0.14, 0.34), 2)
        blur = 0 if size >= 23 else 1
        particles.append(
            f'<div class="food-particle" style="left:{left:.1f}%; '
            f'animation-delay:{delay:.1f}s; animation-duration:{duration:.1f}s; '
            f'font-size:{size}px; --p-opacity:{opacity}; filter: blur({blur}px);">{emoji}</div>'
        )
    return "".join(particles)

# --- STYLIZACJA I ANIMOWANE TŁO ---
bg_style = """<style>
.stApp {
background: linear-gradient(135deg, #1e1e24 0%, #2a2a35 100%) !important;
color: #ffffff !important;
}

@keyframes foodRain {
0%   { transform: translateY(-20vh) translateX(0px) rotate(0deg) scale(0.85); opacity: 0; }
10%  { opacity: var(--p-opacity, 0.25); }
30%  { transform: translateY(20vh) translateX(14px) rotate(90deg) scale(1); }
60%  { transform: translateY(60vh) translateX(-14px) rotate(200deg) scale(1); }
90%  { opacity: var(--p-opacity, 0.25); }
100% { transform: translateY(115vh) translateX(10px) rotate(360deg) scale(0.85); opacity: 0; }
}
.food-particle {
position: fixed !important;
top: -15% !important;
user-select: none !important;
pointer-events: none !important;
animation-name: foodRain !important;
animation-timing-function: linear !important;
animation-iteration-count: infinite !important;
z-index: 1 !important;
}

.main-title {
text-align: center;
font-family: '-apple-system', BlinkMacSystemFont, 'Segoe UI', Roboto;
font-weight: 800;
font-size: 34px;
margin-bottom: 2px;
color: #ff9f43;
text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
letter-spacing: -0.5px;
position: relative;
z-index: 2;
}

.main-subtitle {
text-align: center;
font-size: 13px;
color: rgba(255,255,255,0.45);
margin-bottom: 26px;
letter-spacing: 1.5px;
text-transform: uppercase;
position: relative;
z-index: 2;
}

/* --- Nowoczesne, mniejsze kafelki menu glownego --- */
div[data-testid="stAppViewContainer"] div[data-testid="stButton"] button {
    width: 100%;
    min-height: 118px; /* Zmniejszone ze 148px na 118px */
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px; /* Nieco zgrabniejszy zaokrąglony róg */
    white-space: pre-line;
    color: #ffffff;
    box-shadow: 0 10px 24px rgba(0,0,0,0.35);
    transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    position: relative;
    z-index: 2;
}
div[data-testid="stAppViewContainer"] div[data-testid="stButton"] button:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 16px 32px rgba(0,0,0,0.45);
    border-color: rgba(255,255,255,0.32);
}
div[data-testid="stAppViewContainer"] div[data-testid="stButton"] button:active {
    transform: scale(0.97);
}
div[data-testid="stAppViewContainer"] div[data-testid="stButton"] button p {
    line-height: 1.4;
}
/* Poprawka emotek na kafelkach: mniejsze i subtelnie przezroczyste */
div[data-testid="stAppViewContainer"] div[data-testid="stButton"] button p:first-child {
    font-size: 24px; /* Zmniejszone z 32px */
    opacity: 0.7;    /* Efekt przezroczystości (70% widoczności) */
    margin: 0 0 2px 0;
}
div[data-testid="stAppViewContainer"] div[data-testid="stButton"] button p:nth-child(2) {
    font-size: 16px; /* Zmniejszone z 17px */
    font-weight: 800;
    margin: 0;
}
div[data-testid="stAppViewContainer"] div[data-testid="stButton"] button p:nth-child(3) {
    font-size: 11px; /* Zmniejszone z 11.5px */
    font-weight: 400;
    opacity: 0.75;
    margin: 3px 0 0 0;
    letter-spacing: 0.2px;
}

div[data-testid="column"]:nth-of-type(1) div[data-testid="stButton"]:nth-of-type(1) button {
    background: linear-gradient(135deg, #ff9f43 0%, #ee5253 100%);
}
div[data-testid="column"]:nth-of-type(1) div[data-testid="stButton"]:nth-of-type(2) button {
    background: linear-gradient(135deg, #10ac84 0%, #1dd1a1 100%);
}
div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"]:nth-of-type(1) button {
    background: linear-gradient(135deg, #5f27cd 0%, #341f97 100%);
}
div[data-testid="column"]:nth-of-type(2) div[data-testid="stButton"]:nth-of-type(2) button {
    background: linear-gradient(135deg, #2e86de 0%, #0652DD 100%);
}
</style>"""

# Pokazuj deszcz jedzenia tylko w menu glownym
if st.session_state.current_menu == "Główne":
    bg_style += generate_food_rain()

st.markdown(bg_style, unsafe_allow_html=True)

# --- TYTUŁ GŁÓWNY ---
st.markdown('<div class="main-title">🍔 MaksStandard</div>', unsafe_allow_html=True)

# --- LINK DO ARKUSZA GOOGLE (z zabezpieczeniem przed buforowaniem) ---
LINK_CSV = f"https://docs.google.com/spreadsheets/d/e/2PACX-1vQM0vjCm1BiSiMejP38yW62cFTH7YpnIQDlXI3Tt3Ip0yJ5yF2scsH4kFpCkMSPXIqvLZogwT7uQFry/pub?gid=0&single=true&output=csv&t={int(time.time())}"

# --- MENU GŁÓWNE ---
if st.session_state.current_menu == "Główne":
    st.markdown('<div class="main-subtitle">Wybierz sekcję, aby kontynuować</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        # Zmiana ikonki z 🛠️ na 🧑‍🍳
        if st.button("🧑‍🍳\n\nPracownia\n\nStandardy i receptury", use_container_width=True, key="btn_pracownia"):
            st.session_state.current_menu = "Pracownia"
            st.rerun()
        if st.button("🍳\n\nKuchnia\n\nStrefa chroniona", use_container_width=True, key="btn_kuchnia"):
            st.session_state.current_menu = "Kuchnia"
            st.rerun()
    with col2:
        if st.button("📦\n\nMagazyn\n\nStrefa chroniona", use_container_width=True, key="btn_magazyn"):
            st.session_state.current_menu = "Magazyn"
            st.rerun()
        if st.button("👔\n\nZarząd\n\nPanel zarządzania", use_container_width=True, key="btn_zarzad"):
            st.session_state.current_menu = "Zarząd"
            st.rerun()

# --- PODMENU: PRACOWNIA ---
elif st.session_state.current_menu == "Pracownia":
    st.subheader("🛠️ Pracownia – Standardy Dań")
    if st.button("⬅️ Powrót"):
        st.session_state.current_menu = "Główne"
        st.rerun()
    
    try:
        df = pd.read_csv(LINK_CSV, sep=None, engine='python')
        df.columns = df.columns.str.strip()
        
        col_danie = [c for c in df.columns if c.lower() in ['danie', 'nazwa']][0]
        col_skladniki = [c for c in df.columns if c.lower() in ['skladniki', 'składniki', 'receptura']][0]
        
        for index, row in df.iterrows():
            danie_nazwa = row[col_danie]
            skladniki_tekst = row[col_skladniki]
            
            if pd.isna(danie_nazwa) or pd.isna(skladniki_tekst):
                continue
                
            with st.expander(f"🍔 {danie_nazwa}"):
                ilosc = st.number_input(
                    f"Wpisz ilość porcji dla: {danie_nazwa}", 
                    min_value=1, value=1, step=1, key=f"input_{index}"
                )
                st.markdown(f"**Składniki dla {ilosc} szt.:**")
                
                if ";" in str(skladniki_tekst):
                    skladniki_list = str(skladniki_tekst).split(";")
                else:
                    skladniki_list = str(skladniki_tekst).split(",")
                
                skladniki_skalowane = []
                for item in skladniki_list:
                    if item.strip():
                        scaled_item = scale_ingredient(item.strip(), ilosc)
                        skladniki_skalowane.append(scaled_item)
                        st.write(f"- {scaled_item}")
                
                # Generowanie PDF
                try:
                    pdf_data = generate_pdf(danie_nazwa, ilosc, skladniki_skalowane)
                    st.download_button(
                        label="🖨️ Pobierz PDF do druku",
                        data=pdf_data,
                        file_name=f"Standard_{clean_txt(danie_nazwa).replace(' ', '_')}_{ilosc}_porcji.pdf",
                        mime="application/pdf",
                        key=f"pdf_{index}"
                    )
                except Exception as pdf_err:
                    st.warning("Nie udało się przygotować pliku PDF.")
                    st.info(f"Szczegóły błędu: {pdf_err}")
                    
    except Exception as e:
        st.error("Nie udało się pobrać danych z Arkusza Google.")
        st.exception(e)

# --- PODMENU: KUCHNIA ---
elif st.session_state.current_menu == "Kuchnia":
    st.subheader("🍳 Kuchnia – Strefa Chroniona")
    pin = st.text_input("Podaj 4-cyfrowy PIN dostępu:", type="password", max_chars=4)
    if pin == "0000":
        st.success("Dostęp przyznany!")
    elif pin != "":
        st.error("Błędny kod PIN!")
    if st.button("⬅️ Powrót"):
        st.session_state.current_menu = "Główne"
        st.rerun()

# --- PODMENU: MAGAZYN ---
elif st.session_state.current_menu == "Magazyn":
    st.subheader("📦 Magazyn – Strefa Chroniona")
    pin = st.text_input("Podaj 4-cyfrowy PIN dostępu:", type="password", max_chars=4)
    if pin == "1111":
        st.success("Dostęp przyznany!")
    elif pin != "":
        st.error("Błędny kod PIN!")
    if st.button("⬅️ Powrót"):
        st.session_state.current_menu = "Główne"
        st.rerun()

# --- PODMENU: ZARZĄD ---
elif st.session_state.current_menu == "Zarząd":
    st.subheader("👔 Zarząd – Strefa Ściśle Chroniona")
    pin = st.text_input("Podaj 4-cyfrowy PIN dostępu:", type="password", max_chars=4)
    if pin == "2222":
        st.success("Dostęp przyznany!")
    elif pin != "":
        st.error("Błędny kod PIN!")
    if st.button("⬅️ Powrót"):
        st.session_state.current_menu = "Główne"
        st.rerun()
