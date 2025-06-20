import streamlit as st
import time 
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.agents.company_finder import get_leads

st.set_page_config(page_title="B2B Lead Finder", layout="wide")

industry = st.selectbox("Select Industry", ["Manufacturing", "IT", "Healthcare", "Education", "Finance", "Retail", "Real Estate", "Hospitality", "Construction", "Logistics", "Telecommunications", "Pharmaceuticals", "Food & Beverage", "Media & Entertainment", "Non-Profit", "Others"])
if industry == "Others":
    industry = st.text_input("Please specify the industry")
    
location = st.text_input("Enter Location (e.g., Hyderabad)")
num_companies = st.slider("Number of Companies", 1, 100, 10)

if st.button("Find Leads"):
    with st.spinner("Fetching leads..."):
        try:
            results = get_leads(industry, location, num_companies)
            st.success("Leads fetched successfully!")

            for company, url in results.items():
                st.markdown(f"**{company}** → [LinkedIn]({url})")

        except Exception as e:
            st.error(f"Error: {e}")