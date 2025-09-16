"""
FoodieBot - Error-Free Version
"""

import streamlit as st
import requests
import json
import uuid

# Page configuration
st.set_page_config(
    page_title="🤖 FoodieBot AI",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
# Custom CSS with FIXED INPUT TEXT VISIBILITY
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        min-height: 100vh;
        padding: 0 !important;
    }
    
    .block-container {
        padding: 0.5rem 1rem 0 1rem !important;
        max-width: 1200px;
        gap: 0 !important;
    }
    
    .main-header {
        background: linear-gradient(135deg, #e94560 0%, #f27121 100%);
        padding: 1.8rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 1.2rem;
        box-shadow: 0 8px 32px rgba(233, 69, 96, 0.3);
        border: 1px solid rgba(242, 113, 33, 0.4);
    }
    
    .main-header h1 {
        color: #ffffff;
        font-size: 2.6rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        font-weight: 500;
    }
    
    .chat-container {
        background: linear-gradient(135deg, #2d4a87 0%, #3d5a99 100%);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 28px rgba(45, 74, 135, 0.25);
        border: 1px solid rgba(61, 90, 153, 0.3);
        margin-bottom: 1rem;
        min-height: auto;
        max-height: 500px;
        overflow-y: auto;
    }
    
    .user-message {
        background: linear-gradient(135deg, #e94560 0%, #f27121 100%);
        color: #ffffff;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0;
        margin-left: 25%;
        box-shadow: 0 4px 16px rgba(233, 69, 96, 0.3);
        font-weight: 500;
        border: 1px solid rgba(242, 113, 33, 0.2);
    }
    
    .bot-message {
        background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
        color: #ffffff;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px 0;
        margin-right: 25%;
        box-shadow: 0 4px 16px rgba(0, 210, 255, 0.25);
        font-weight: 500;
        border: 1px solid rgba(58, 123, 213, 0.2);
    }
    
    .welcome-message {
        background: linear-gradient(135deg, #2d4a87 0%, #3d5a99 100%);
        color: #ffffff;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 28px rgba(45, 74, 135, 0.25);
        border: 1px solid rgba(61, 90, 153, 0.3);
        margin-bottom: 1rem;
        font-weight: 500;
        font-size: 1.1rem;
    }
    
    .product-card {
        background: linear-gradient(135deg, #2d4a87 0%, #3d5a99 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.8rem 0;
        box-shadow: 0 6px 24px rgba(45, 74, 135, 0.25);
        border: 1px solid rgba(61, 90, 153, 0.3);
        transition: all 0.3s ease;
    }
    
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 36px rgba(45, 74, 135, 0.35);
        border-color: rgba(233, 69, 96, 0.4);
    }
    
    .product-name {
        font-size: 1.3rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    
    .product-price {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f27121;
        margin-bottom: 0.5rem;
    }
    
    .product-description {
        color: rgba(255, 255, 255, 0.85);
        line-height: 1.5;
        margin-bottom: 1rem;
        font-weight: 400;
    }
    
    .product-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .product-tag {
        background: rgba(233, 69, 96, 0.8);
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 500;
        border: 1px solid rgba(233, 69, 96, 0.3);
    }
    
    .spice-tag {
        background: rgba(242, 113, 33, 0.8);
        border-color: rgba(242, 113, 33, 0.3);
    }
    
    .health-tag {
        background: rgba(0, 210, 255, 0.8);
        border-color: rgba(0, 210, 255, 0.3);
    }
    
    .popularity-tag {
        background: rgba(255, 193, 7, 0.8);
        border-color: rgba(255, 193, 7, 0.3);
        color: #000000;
        font-weight: 600;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2d4a87 0%, #1a1a2e 100%);
        border-radius: 16px;
        padding: 1rem;
        border: 1px solid rgba(45, 74, 135, 0.3);
        box-shadow: 0 6px 20px rgba(26, 26, 46, 0.4);
    }
    
    /* FIXED INPUT TEXT STYLING - DARK TEXT ON LIGHT BACKGROUND */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #e94560 !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease;
        background: #ffffff !important;
        color: #1a1a2e !important;
        box-shadow: 0 2px 8px rgba(233, 69, 96, 0.2) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #f27121 !important;
        box-shadow: 0 0 0 3px rgba(242, 113, 33, 0.2) !important;
        outline: none !important;
        background: #ffffff !important;
        color: #1a1a2e !important;
    }
    
    /* PLACEHOLDER TEXT STYLING */
    .stTextInput > div > div > input::placeholder {
        color: #6c757d !important;
        opacity: 0.7 !important;
        font-weight: 500 !important;
    }
    
    /* SEARCH INPUT STYLING */
    .stTextInput input {
        background: #ffffff !important;
        color: #1a1a2e !important;
        border: 2px solid #00d2ff !important;
        border-radius: 12px !important;
        padding: 10px 16px !important;
        font-weight: 600 !important;
    }
    
    .stTextInput input:focus {
        background: #ffffff !important;
        color: #1a1a2e !important;
        border-color: #3a7bd5 !important;
        box-shadow: 0 0 0 3px rgba(58, 123, 213, 0.2) !important;
    }
    
    .stTextInput input::placeholder {
        color: #6c757d !important;
        opacity: 0.7 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #e94560 0%, #f27121 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(233, 69, 96, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(233, 69, 96, 0.4) !important;
        background: linear-gradient(135deg, #f27121 0%, #e94560 100%) !important;
    }
    
    /* SELECTBOX STYLING - DARK TEXT ON LIGHT BACKGROUND */
    .stSelectbox > div > div {
        border-radius: 12px !important;
        border: 2px solid #00d2ff !important;
        background: #ffffff !important;
        box-shadow: 0 2px 8px rgba(0, 210, 255, 0.2) !important;
    }
    
    .stSelectbox > div > div > div {
        color: #1a1a2e !important;
        font-weight: 600 !important;
    }
    
    /* SELECTBOX DROPDOWN STYLING */
    .stSelectbox > div > div > div[data-baseweb="select"] > div {
        color: #1a1a2e !important;
        background: #ffffff !important;
    }
    
    .stInfo > div {
        background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%) !important;
        border: 1px solid rgba(0, 210, 255, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 16px rgba(0, 210, 255, 0.2) !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    div[data-testid="column"] {
        padding: 0 0.4rem !important;
    }
    
    /* ENSURE ALL INPUT TEXT IS VISIBLE */
    input {
        background: #ffffff !important;
        color: #1a1a2e !important;
    }
    
    input:focus {
        background: #ffffff !important;
        color: #1a1a2e !important;
    }
    
    textarea {
        background: #ffffff !important;
        color: #1a1a2e !important;
    }
    
    /* FIX FORM INPUT VISIBILITY */
    .stForm input {
        background: #ffffff !important;
        color: #1a1a2e !important;
        font-weight: 600 !important;
    }
    
    .stForm input::placeholder {
        color: #6c757d !important;
        opacity: 0.7 !important;
    }
</style>
""", unsafe_allow_html=True)


# API Configuration
API_URL = "http://127.0.0.1:8000"

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_products' not in st.session_state:
    st.session_state.current_products = []

# Helper Functions
def send_message(message):
    try:
        response = requests.post(f"{API_URL}/api/chat", json={
            "message": message,
            "session_id": st.session_state.session_id
        }, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

def get_products(category=None, search=None):
    try:
        params = {}
        if category and category != "All Categories":
            params['category'] = category
        if search:
            params['search'] = search
        
        response = requests.get(f"{API_URL}/api/products", params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"products": [], "categories": []}
    except Exception as e:
        st.error(f"Error loading products: {e}")
        return {"products": [], "categories": []}

# Header
st.markdown("""
<div class="main-header">
    <h1>🍔 FoodieBot AI</h1>
    <p>Your Intelligent Food Discovery Assistant</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #e94560, #f27121); border-radius: 16px; color: white; margin-bottom: 1rem; border: 1px solid rgba(242, 113, 33, 0.3);">
        <h3 style="margin: 0; font-weight: 700;">🍽️ Navigation</h3>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">Choose your experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.selectbox("", ["💬 Chat with AI", "🍕 Browse Menu"], label_visibility="collapsed")
    
    if page == "💬 Chat with AI":
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 1rem; color: white;">
            <h4 style="margin-bottom: 1rem; font-weight: 600;">🎯 Quick Actions</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🆕 New Chat", use_container_width=True):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.chat_history = []
            st.session_state.current_products = []
            st.rerun()
        
        if st.button("🌶️ Spicy Food", use_container_width=True):
            message = "I want something really spicy!"
            result = send_message(message)
            if result:
                st.session_state.chat_history.append({
                    "user": message, 
                    "bot": result['response'], 
                    "products": result['recommended_products']
                })
                st.session_state.current_products = result['recommended_products']
                st.rerun()
        
        if st.button("🥗 Healthy Options", use_container_width=True):
            message = "Show me healthy food options"
            result = send_message(message)
            if result:
                st.session_state.chat_history.append({
                    "user": message, 
                    "bot": result['response'], 
                    "products": result['recommended_products']
                })
                st.session_state.current_products = result['recommended_products']
                st.rerun()
        
        if st.button("🍕 Pizza Time", use_container_width=True):
            message = "I want pizza!"
            result = send_message(message)
            if result:
                st.session_state.chat_history.append({
                    "user": message, 
                    "bot": result['response'], 
                    "products": result['recommended_products']
                })
                st.session_state.current_products = result['recommended_products']
                st.rerun()

# Main Content
if page == "💬 Chat with AI":
    col1, col2 = st.columns([2, 1], gap="small")
    
    with col1:
        if st.session_state.chat_history:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            for chat in st.session_state.chat_history:
                st.markdown(f'<div class="user-message">{chat["user"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="bot-message">{chat["bot"]}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="welcome-message">
                <h3 style="margin: 0 0 1rem 0; color: #ffffff;">👋 Welcome to FoodieBot!</h3>
                <p style="margin: 0; font-size: 1.1rem;">I'm your AI food consultant, ready to help you discover amazing dishes. Start by typing what you're craving, or use the quick actions on the left!</p>
            </div>
            """, unsafe_allow_html=True)
        
        with st.form("chat_form", clear_on_submit=True):
            col_input, col_send = st.columns([4, 1], gap="small")
            
            with col_input:
                user_input = st.text_input("", placeholder="What delicious food are you craving?", label_visibility="collapsed")
            
            with col_send:
                send_clicked = st.form_submit_button("Send 🚀", use_container_width=True)
            
            if send_clicked and user_input:
                with st.spinner("🤤 FoodieBot is cooking up recommendations..."):
                    result = send_message(user_input)
                
                if result:
                    st.session_state.chat_history.append({
                        "user": user_input,
                        "bot": result['response'],
                        "products": result['recommended_products']
                    })
                    st.session_state.current_products = result['recommended_products']
                    st.rerun()
    
    with col2:
        st.markdown("### 🍽️ Recommendations")
        
        if st.session_state.current_products:
            for product in st.session_state.current_products:
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-name">{product['name']}</div>
                    <div class="product-price">${product['price']:.2f}</div>
                    <div class="product-description">{product['description'][:70]}...</div>
                    <div class="product-tags">
                        <span class="product-tag popularity-tag">⭐ {product['popularity_score']}/100</span>
                        <span class="product-tag spice-tag">🌶️ {product.get('spice_level', 1)}/10</span>
                        <span class="product-tag health-tag">📊 {product.get('calories', 500)} cal</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("💡 Start chatting to get personalized food recommendations!")

else:  # Browse Menu
    st.markdown("### 🍕 Explore Our Delicious Menu")
    
    col1, col2, col3 = st.columns(3, gap="small")
    
    with col1:
        products_data = get_products()
        categories = ["All Categories"] + products_data.get('categories', [])
        selected_category = st.selectbox("🏷️ Category", categories)
    
    with col2:
        search_term = st.text_input("🔍 Search", placeholder="Pizza, Burger, Tacos...")
    
    with col3:
        st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
        if st.button("🔍 Search Menu", use_container_width=True):
            st.rerun()
    
    filtered_products = get_products(
        category=selected_category if selected_category != "All Categories" else None,
        search=search_term if search_term else None
    )
    
    products = filtered_products.get('products', [])
    
    if products:
        cols = st.columns(3, gap="small")
        
        for i, product in enumerate(products):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-name">{product['name']}</div>
                    <div class="product-price">${product['price']:.2f}</div>
                    <div class="product-description">{product['description']}</div>
                    <div class="product-tags">
                        <span class="product-tag">📂 {product['category']}</span>
                        <span class="product-tag popularity-tag">⭐ {product['popularity_score']}/100</span>
                        <span class="product-tag spice-tag">🌶️ {product.get('spice_level', 1)}/10</span>
                        <span class="product-tag health-tag">📊 {product.get('calories', 500)} cal</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("🍽️ No products found. Try different filters!")

# Footer
st.markdown("""
<div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #2d4a87 0%, #1a1a2e 100%); border-radius: 16px; margin-top: 1rem; border: 1px solid rgba(45, 74, 135, 0.3); box-shadow: 0 6px 20px rgba(26, 26, 46, 0.4);">
    <p style="margin: 0; color: #ffffff; font-weight: 600;">🤖 <strong>FoodieBot AI</strong> - Powered by Advanced Food Intelligence</p>
    <p style="margin: 0.5rem 0 0 0; color: rgba(255, 255, 255, 0.8); font-size: 0.9rem;">Discover your perfect meal with AI-powered recommendations 🍔✨</p>
</div>
""", unsafe_allow_html=True)
