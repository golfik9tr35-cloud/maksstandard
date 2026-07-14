import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Próba importu fpdf do generowania PDF. Jeśli nie ma w chmurze, streamlit sam doinstaluje,
# ale dla pewności użyjemy standardowego mechanizmu pobierania pliku tekstowego/PDF.
try:
    from fpdf import FPDF
except ImportError:
    import os
    os.system('pip install fpdf2')
    from fpdf import FPDF

# Ustawienia strony dla urządzeń mobilnych
st.set_page_config(
    page_title="MaksStandard",
    page_icon="🍔",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- STYLIZACJA I ANIMOWANE TŁO (Tylko na stronie głównej!) ---
# Stan nawigacji
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "Główne"

# Kod HTML/CSS dla tła i animacji (deszcz jedzenia aktywuje się tylko na głównej)
bg_style = """
<style>
    .stApp {
        background: linear-gradient(135deg, #1e1e24 0%, #2a2a35 100%);
        color: #ffffff;
        overflow: hidden;
    }
    @keyframes foodRain {
        0% { transform: translateY(-20vh) rotate(0deg); opacity: 0; }
        5% { opacity: 0.8; }
        95% { opacity: 0.8; }
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
        z-index: 0;
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
</style>
"""

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

# Funkcja powrotu
def go_back():
    st.session_state.current_menu = "Główne"
    st.rerun()

# Funkcja do przeliczania gramatury i miar w tekście składnika
def scale_ingredient(text, multiplier):
    if multiplier == 1:
        return text
    
    # Szukamy liczb (całkowitych lub ułamkowych np. 0.5, 1, 50, 150) stojących obok jednostek (g, dkg, kg, szt, plaster, łyżka itp.)
    def multiply_match(match):
        val = float(match.group(1))
        unit = match.group(2)
        scaled_val = val * multiplier
        # Formatowanie: usuwamy .0 jeśli liczba jest całkowita
        if scaled_val.is_integer():
            return f"{int(scaled_val)}{unit}"
        else:
            return f"{round(scaled_val, 2)}{unit}"
            
    # Wyrażenie regularne dopasowujące liczby i następujące po nich jednostki
    pattern = r"(\d+(?:\.\d+)?)\s*(g|dag|dkg|kg|szt|ml|l|plaster|plastry|lyzka|łyżka|lyzki|łyżeczka)"
    result = re.sub(pattern, multiply_match, text, flags=re.IGNORECASE)
    return result

# Funkcja generująca plik PDF
def generate_pdf(danie, porcje, skladniki_skalowane):
    pdf = FPDF()
    pdf.add_page()
    
    # Czcionka podstawowa (FPDF domyślnie wspiera standardowe czcionki bez polskich znaków, 
    # użyjemy czystego zapisu lub zamienimy polskie znaki dla pewności, by plik się nie wysypał)
    pdf.set_font("Arial", "B", 20)
    pdf.cell(190, 10, "MaksStandard - Karta Produkcji", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, f"Danie: {danie}", ln=True)
    pdf.cell(190, 10, f"Ilosc porcji: {porcje}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(190, 10, "Lista przeliczonych skladnikow:", ln=True)
    pdf.ln(2)
    
    # Podmiana polskich znaków dla kompatybilności z podstawowym PDF w FPDF
    def clean_txt(t):
        replacements = {'ą':'a','ć':'c','ę':'e','ł':'l','ń':'n','ó':'o','ś':'s','ź':'z','ż':'z',
                        'Ą':'A','Ć':'C','Ę':'E','Ł':'L','Ń':'N','Ó':'O','Ś':'S','Ź':'Z','Ż':'Z'}
        for k, v in replacements.items():
            t = t.replace(k, v)
        return t

    for item in skladniki_skalowane:
        pdf.cell(190, 8, f"- {clean_txt(item)}", ln=True)
        
    pdf.ln(15)
    pdf.set_font("Arial", "I", 9)
    pdf.cell(190, 10, "Wygenerowano automatycznie z aplikacji MaksStandard.", ln=True, align="C")
    
    return pdf.output(dest='S')

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

# --- PODMENU: PRACOWNIA (Pobiera dane z Excela w czasie rzeczywistym + Kalkulator i PDF) ---
elif st.session_state.current_menu == "Pracownia":
    st.subheader("🛠️ Pracownia – Standardy Dań")
    if st.button("⬅️ Powrót", on_click=go_back): pass
    
    st.write("Wybierz danie z listy, wpisz ilość porcji i pobierz kartę do druku:")
    
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
                # Pole wyboru ilości sztuk/porcji dla każdego dania osobno
                ilosc = st.number_input(
                    f"Wpisz ilość porcji dla: {danie_nazwa}", 
                    min_value=1, 
                    value=1, 
                    step=1, 
                    key=f"input_{index}"
                )
                
                st.markdown(f"**Składniki dla {ilosc} szt.:**")
                
                # Rozdzielenie składników
                if ";" in str(skladniki_tekst):
                    skladniki_list = str(skladniki_tekst).split(";")
                else:
                    skladniki_list = str(skladniki_tekst).split(",")
                
                # Skalowanie i wyświetlanie składników
                skladniki_skalowane = []
                for item in skladniki_list:
                    if item.strip():
                        scaled_item = scale_ingredient(item.strip(), ilosc)
                        skladniki_skalowane.append(scaled_item)
                        st.write(f"- {scaled_item}")
                
                # Przycisk generowania i pobierania pliku PDF
                try:
                    pdf_data = generate_pdf(danie_nazwa, ilosc, skladniki_skalowane)
                    st.download_button(
                        label="🖨️ Pobierz PDF do druku",
                        data=pdf_data,
                        file_name=f"Standard_{danie_nazwa.replace(' ', '_')}_{ilosc}_porcji.pdf",
                        mime="application/pdf",
                        key=f"pdf_{index}"
                    )
                except Exception as pdf_err:
                    st.warning("Nie udało się przygotować pliku PDF. Możesz skopiować tekst ręcznie.")
                    
    except Exception as e:
        st.error("Nie udało się pobrać danych z Arkusza Google.")
        st.info(f"Szczegóły błędu: {e}")

# --- PODMENU: KUCHNIA (Hasło: 0000) ---
elif st.session_state.current_menu == "Kuchnia":
    st.subheader("🍳 Kuchnia – Strefa Chroniona")
    pin = st.text_input("Podaj 4-cyfrowy PIN dostępu:", type="password", max_chars=4)
    if pin == "0000":
        st.success("Dostęp przyznany!")
        st.button("Dodatkowe menu Kuchni 1")
    elif pin != "":
        st.error("Błędny kod PIN!")
    if st.button("⬅️ Powrót", on_click=go_back): pass

# --- PODMENU: MAGAZYN (Hasło: 1111) ---
elif st.session_state.current_menu == "Magazyn":
    st.subheader("📦 Magazyn – Strefa Chroniona")
    pin = st.text_input("Podaj 4-cyfrowy PIN dostępu:", type="password", max_chars=4)
    if pin == "1111":
        st.success("Dostęp przyznany!")
        st.button("Dodatkowe menu Magazynu 1")
    elif pin != "":
        st.error("Błędny kod PIN!")
    if st.button("⬅️ Powrót", on_click=go_back): pass

# --- PODMENU: ZARZĄD (Hasło: 2222) ---
elif st.session_state.current_menu == "Zarząd":
    st.subheader("👔 Zarząd – Strefa Ściśle Chroniona")
    pin = st.text_input("Podaj 4-cyfrowy PIN dostępu:", type="password", max_chars=4)
    if pin == "2222":
        st.success("Dostęp przyznany!")
        st.button("Statystyki finansowe")
    elif pin != "":
        st.error("Błędny kod PIN!")
    if st.button("⬅️ Powrót", on_click=go_back): pass
