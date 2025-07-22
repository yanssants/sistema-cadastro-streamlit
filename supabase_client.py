# supabase_client.py
import streamlit as st
from supabase import create_client, Client

# Pega as credenciais do Streamlit Secrets
supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]

# Cria uma instância única do cliente Supabase
supabase: Client = create_client(supabase_url, supabase_key)