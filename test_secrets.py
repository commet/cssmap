"""
Streamlit secrets 테스트 페이지
"""
import streamlit as st
import os

st.title("API Key Detection Test")

st.subheader("1. Checking st.secrets")
try:
    if "PADLET_API_KEY" in st.secrets:
        key = st.secrets["PADLET_API_KEY"]
        st.success(f"Found in st.secrets: {key[:10]}... (length: {len(key)})")
    else:
        st.warning("PADLET_API_KEY not found in st.secrets")
        st.write("Available secrets:", list(st.secrets.keys()))
except Exception as e:
    st.error(f"Error accessing st.secrets: {e}")

st.subheader("2. Checking environment variables")
env_key = os.getenv("PADLET_API_KEY")
if env_key:
    st.success(f"Found in environment: {env_key[:10]}... (length: {len(env_key)})")
else:
    st.warning("PADLET_API_KEY not found in environment")

st.subheader("3. All environment variables starting with PADLET")
padlet_vars = {k: v[:10] + "..." for k, v in os.environ.items() if k.startswith("PADLET")}
if padlet_vars:
    st.write(padlet_vars)
else:
    st.write("No PADLET* environment variables found")

st.subheader("4. Debug Info")
st.write("Running on Streamlit Cloud:", "STREAMLIT_SHARING_MODE" in os.environ)
st.write("Python version:", os.sys.version)