import streamlit as st

# Ustawienia strony dla urządzeń mobilnych (iOS/Android)
st.set_page_config(
    page_title="MaksStandard",
    page_icon="🍔",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- STYLIZACJA I ANIMOWANE TŁO (Szybki deszcz jedzenia + własna ikona iOS) ---
st.markdown("""
<head>
    <link rel="apple-touch-icon" href="https://img.icons8.com/emoji/192/hamburger-emoji.png">
    <link rel="apple-touch-icon" sizes="152x152" href="https://img.icons8.com/emoji/152/hamburger-emoji.png">
    <link rel="apple-touch-icon" sizes="180x180" href="https://img.icons8.com/emoji/180/hamburger-emoji.png">
    <link rel="icon" type="image/png" href="https://img.icons8.com/emoji/192/hamburger-emoji.png">
</head>
<style>
    /* Tło aplikacji */
    .stApp {
        background: linear-gradient(135deg, #1e1e24 0%, #2a2a35 100%);
        color: #ffffff;
        overflow: hidden;
    }
    
    /* Animacja deszczu jedzenia */
    @keyframes foodRain {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 0; }
        10% { opacity: 0.8; }
        90% { opacity: 0.8; }
        100% { transform: translateY(105vh) rotate(360deg); opacity: 0; }
    }
    
    .food-particle {
        position: fixed;
        top: -10%;
        font-size: 24px;
        user-select: none;
        pointer-events: none;
        animation: foodRain 10s linear infinite;
        animation-fill-mode: backwards; /* Startuje od pierwszej klatki natychmiast */
        z-index: 0;
    }
    
    /* Nagłówek aplikacji */
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

<div class="food-particle" style="left: 5%; animation-delay: 0s; animation-duration: 8s;">🍔</div>
<div class="food-particle" style="left: 15%; animation-delay: 2s; animation-duration: 11s;">🍽️</div>
<div class="food-particle" style="left: 25%; animation-delay: 0.5s; animation-duration: 12s;">🍣</div>
<div class="food-particle" style="left: 35%; animation-delay: 4s; animation-duration: 9s;">🥤</div>
<div class="food-particle" style="left: 45%; animation-delay: 0s; animation-duration: 10s;">🥪</div>
<div class="food-particle" style="left: 55%; animation-delay: 3s; animation-duration: 13s;">🍴</div>
<div class="food-particle" style="left: 65%; animation-delay: 1.5s; animation-duration: 11s;">🍔</div>
<div class="food-particle" style="left: 75%; animation-delay: 5s; animation-duration: 8s;">🍽️</div>
<div class="food-particle" style="left: 85%; animation-delay: 0.2s; animation-duration: 12s;">🍣</div>
<div class="food-particle" style="left: 95%; animation-delay: 2.5s; animation-duration: 10s;">🥤</div>
""", unsafe_allow_html=True)

# --- TYTUŁ GŁÓWNY ---
st.markdown('<div class="main-title">MaksStandard</div>', unsafe_allow_html=True)

# --- STAN APLIKACJI (Session State dla nawigacji) ---
if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "Główne"

# Funkcja powrotu
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

# --- PODMENU: PRACOWNIA (Bez hasła) ---
elif st.session_state.current_menu == "Pracownia":
    st.subheader("🛠️ Pracownia – Panel Główny")
    if st.button("⬅️ Powrót", on_click=go_back): pass
    
    st.write("Wybierz sekcję w Pracowni:")
    st.button("Dodatkowe podmenu 1")
    st.button("Dodatkowe podmenu 2")

# --- PODMENU: KUCHNIA (Hasło: 0000) ---
elif st.session_state.current_menu == "Kuchnia":
    st.subheader("🍳 Kuchnia – Strefa Chroniona")
    pin = st.text_input("Podaj 4-cyfrowy PIN dostępu:", type="password", max_chars=4)
    
    if pin == "0000":
        st.success("Dostęp przyznany!")
        st.button("Dodatkowe menu Kuchni 1")
        st.button("Dodatkowe menu Kuchni 2")
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
        st.button("Zarządzanie użytkownikami")
    elif pin != "":
        st.error("Błędny kod PIN!")
        
    if st.button("⬅️ Powrót", on_click=go_back): pass
