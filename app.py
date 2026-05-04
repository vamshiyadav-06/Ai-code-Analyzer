import streamlit as st
import os
from utils.code_analyzer import (
    analyze_code_for_explanation,
    analyze_code_for_bugs,
    analyze_code_for_improvements
)

# Page configuration
st.set_page_config(
    page_title="Grok AI Code Explainer Tool",
    page_icon="🌌",
    layout="wide"
)

# Custom CSS for unique UI
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f8f9fa !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Code Input */
    .stTextArea textarea {
        font-family: 'Fira Code', 'Courier New', monospace;
        background-color: #1e1e1e !important;
        color: #d4d4d4 !important;
        border: 1px solid #333;
        border-radius: 8px;
    }
    .stTextArea textarea:focus {
        border-color: #4a90e2;
        box-shadow: 0 0 0 1px #4a90e2;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #4a90e2;
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #357abd;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
    }
    
    /* Result Container */
    .result-container {
        background-color: #1a1d24;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #2d3139;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🌌 Grok AI Code Explainer & Analyzer")
st.markdown("### *Understand, debug, and optimize your code instantly using xAI's Grok.*")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    # API Key from Environment
    env_api_key = os.getenv("GROK_API_KEY")
    if not env_api_key:
        st.warning("⚠️ `GROK_API_KEY` not found in .env file.")
    st.divider()

    # Models
    AVAILABLE_MODELS = [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768"
    ]
    selected_model = st.selectbox("AI Model", AVAILABLE_MODELS)

    # Language
    selected_language = st.selectbox(
        "Programming Language",
        ["Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin", "Ruby", "PHP", "Other"]
    )

    # Mode
    explanation_mode = st.radio(
        "Explanation Mode",
        ["Beginner", "Advanced"]
    )

# Layout
col1, col2 = st.columns([1, 1], gap="large")

# Input
with col1:
    st.subheader("📝 Input Code")
    code_input = st.text_area(
        "Paste your code here:",
        height=450,
        placeholder="# Write or paste your code here to begin analysis...\n# Grok will help you understand, debug, or optimize it.",
        label_visibility="collapsed"
    )

    st.markdown("### 🚀 Actions")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        explain_btn = st.button("🧠 Explain")
    with btn_col2:
        debug_btn = st.button("🐛 Debug")
    with btn_col3:
        optimize_btn = st.button("⚡ Optimize")

# Output
with col2:
    st.subheader("📊 Results")
    
    if explain_btn or debug_btn or optimize_btn:
        if not code_input.strip():
            st.warning("⚠️ Please enter some code to analyze.")
        elif not env_api_key:
            st.error("🔑 GROK_API_KEY is missing. Please add it to your .env file.")
        else:
            with st.spinner("🌌 Grok is analyzing your code..."):
                try:
                    if explain_btn:
                        result = analyze_code_for_explanation(
                            code_input, selected_language, explanation_mode, selected_model, env_api_key
                        )
                        st.info(f"**Mode:** {explanation_mode} Explanation | **Language:** {selected_language}")

                    elif debug_btn:
                        result = analyze_code_for_bugs(
                            code_input, selected_language, selected_model, env_api_key
                        )
                        st.info(f"**Mode:** Bug Detection | **Language:** {selected_language}")

                    elif optimize_btn:
                        result = analyze_code_for_improvements(
                            code_input, selected_language, selected_model, env_api_key
                        )
                        st.info(f"**Mode:** Optimization & Complexity | **Language:** {selected_language}")

                    st.success("✅ Analysis Complete!")
                    
                    # Display the result
                    with st.container(border=True):
                        st.markdown(result)

                except Exception as e:
                    st.error(f"❌ Error communicating with xAI API: {str(e)}")
    else:
        st.info("👈 Enter your code and click an action button to see the results here.")