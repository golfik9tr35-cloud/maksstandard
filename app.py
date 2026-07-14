import streamlit as st
import pandas as pd
import re
from fpdf import FPDF

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

# --- POMOCNICZE FUNKCJE (Usuwanie polskich znaków dla PDF) ---
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

# --- STYLIZACJA I ANIMOWANE TŁO (Bez pustych linii!) ---
bg_style = """<style>
.stApp {
    background: linear-gradient(135deg, #1e1e24 0%, #2a2a35 100%);
    color: #ffffff;
}
@keyframes foodRain {
    0% { transform: translateY(-20vh) rotate(0deg); opacity: 0; }
    5% { opacity: 0.8; }
    90% { opacity: 0.8; }
    100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
}
.food-particle {
    position: fixed;
    top: -15%;
    font-size: 26px;
    user-select: none;
    pointer-events: none;
    animation: foodRain 9s linear infinite;
    animation-fill-mode: backwards;
    z-index: 99;
}
.main-title {
    text-align: center;
    font-family: '-apple-system', BlinkMacSystemFont, 'Segoe UI', Roboto;
    font-weight: 800;
    font-size: 32px;
    margin-bottom: 30px;
    color: #ff9f43;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
}
</style>"""

if st.session_state.current_menu == "Główne":
    bg_style += """
    <div class="food-particle" style="left: 5%; animation-delay: 0s; animation-duration: 7s;">🍔</div>
    <div class="food-particle" style="left: 15%; animation-delay: 1.2s; animation-duration: 9s;">🍽️</div>
    <div class="food-particle" style="left: 25%; animation-delay: 0.2s; animation-duration: 10s;">🍣</div>
    <div class="food-particle" style="left: 35%; animation-delay: 2.5s; animation-duration: 8s;">🥤</div>
    <div class="food-particle" style="left: 45%; animation-delay: 0s; animation-duration: 9s;">🥪</div>
    <div class="food-particle" style="left: 55%; animation-delay: 1.8s; animation-duration: 11s;">🍴</div>
    <div class="food-particle" style="left: 65%; animation-delay: 0.5s; animation-duration: 9s;">🍔</div>
    <div class="food-particle" style="left: 75%; animation-delay: 3s; animation-duration: 7s;">🍽️</div>
    <div class="food-particle" style="left: 85%; animation-delay: 0.1s; animation-duration: 10s;">🍣</div>
    <div class="food-particle" style="left: 95%; animation-delay: 1.5s; animation-duration: 8s;">🥤</div>
    """

st.markdown(bg_style, unsafe_allow_html=True)

# --- TYTUŁ GŁÓWNY ---
st.markdown('<div class="main-title">MaksStandard</div>', unsafe_allow_html=True)

# --- LINK DO ARKUSZA GOOGLE ---
LINK_CSV = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQM0vjCm1BiSiMejP38yW62cFTH7YpnIQDlXI3Tt3Ip0yJ5yF2scsH4kFpCkMSPXIqvLZogwT7uQFry/pub?gid=0&single=true&output=csv"

def go_back():
    st.session_state.current_menu = "Główne"
    st.rerun()

# --- MENU GŁÓWNE ---
if st.session_state.current_menu == "Główne":
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🛠️\n\nPracownia", use_container_width=True):
            st.session_state.current_menu = "Pracownia"
            st.rerun()
        if st.button("🍳\n\nKuchnia", use_container_width=True):
            st.session_state.current_menu = "Kuchnia"
            st.rerun()
    with col2:
        if st.button("📦\n\nMagazyn", use_container_width=True):
            st.session_state.current_menu = "Magazyn"
            st.rerun()
        if st.button("👔\n\nZarząd", use_container_width=True):
            st.session_state.current_menu = "Zarząd"
            st.rerun()

# --- PODMENU: PRACOWNIA ---
elif st.session_state.current_menu == "Pracownia":
    st.subheader("🛠️ Pracownia – Standardy Dań")
    if st.button("⬅️ Powrót", on_click=go_back): pass
    
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
                
            # Naprawione st.expander
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
                
                # Bezpieczne generowanie PDF
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
    if st.button("⬅️ Powrót", on_click=go_back): pass

# --- PODMENU: MAGAZYN ---
elif st.session_state.current_menu == "Magazyn":
    st.subheader("📦 Magazyn – Strefa Chroniona")
    pin = st.text_input("Podaj 4-cyfrowy PIN dostępu:", type="password", max_chars=4)
    if pin == "1111":
        st.success("Dostęp przyznany!")
    elif pin != "":
        st.error("Błędny kod PIN!")
    if st.button("⬅️ Powrót", on_click=go_back): pass

# --- PODMENU: ZARZĄD ---
elif st.session_state.current_menu == "Zarząd":
    st.subheader("👔 Zarząd – Strefa Ściśle Chroniona")
    pin = st.text_input("Podaj 4-cyfrowy PIN dostępu:", type="password", max_chars=4)
    if pin == "2222":
        st.success("Dostęp przyznany!")
    elif pin != "":
        st.error("Błędny kod PIN!")
    if st.button("⬅️ Powrót", on_click=go_back): pass
