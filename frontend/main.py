import streamlit as st
import time 

st.set_page_config(page_title="B2B Lead Finder", layout="wide")

industry = st.selectbox("Select Industry", ["Manufacturing", "IT", "Healthcare", "Education", "Finance", "Retail", "Real Estate", "Hospitality", "Construction", "Logistics", "Telecommunications", "Pharmaceuticals", "Food & Beverage", "Media & Entertainment", "Non-Profit", "Others"])
if industry == "Others":
    industry = st.text_input("Please specify the industry")
    
location = st.text_input("Enter Location (e.g., Hyderabad)")
num_companies = st.slider("Number of Companies", 1, 100, 10)

if st.button("Find Leads"):
    params = {
        "industry": industry,
        "location": location,
        "num_companies": num_companies
    }
    
    #Placeholder for response
    st.spinner("Fetching leads...")
    time.sleep(1)  
    st.markdown("### Found Leads")
    st.write(f"Industry: {industry}")
    st.write(f"Location: {location}")
    st.write(f"Number of Companies: {num_companies}")