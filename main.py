import streamlit as st
import time 
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.agents.company_finder import get_leads

st.set_page_config(page_title="B2B Lead Finder", layout="wide")

st.header("Lead Finder using CrewAI")

industry = st.selectbox(
    "Select Industry",
    [
        "IT & Software",
        "Healthcare & Pharma",
        "Finance & Banking",
        "Manufacturing",
        "Retail & E-commerce",
        "Education & EdTech",
        "Logistics & Supply Chain",
        "Construction & Real Estate",
        "Media & Entertainment",
        "Food & Beverage",
        "Hospitality & Travel",
        "Telecommunications",
        "Non-Profit / NGOs",
        "Other"
    ]
)
if industry == "Other":
    industry = st.text_input("Please specify the industry")
    
location = st.text_input("Enter Location (e.g., Hyderabad)")
num_companies = st.slider("Number of Companies", 1, 100, 10)

if st.button("Find Leads"):
    with st.spinner("Fetching leads..."):
        try:
            start_time = time.time()
            results = get_leads(industry, location, num_companies)
            end_time = time.time()
            duration = end_time - start_time
            st.success("Leads fetched successfully!")
            st.write(f"Time taken: {duration:.2f} seconds")

            # Display cards: 2 cards per row
            cols = st.columns(2)
            for i, (company, url) in enumerate(results.items()):
                with cols[i % 2]:
                    st.markdown(
                        f"""
                        <div style="padding:15px 20px; border:1px solid #DDD; border-radius:12px;
                                    margin-bottom:15px;">
                            <h4 style="margin-bottom:5px;">{company}</h4>
                            <a href="{url}" target="_blank" style="color:#1a73e8;">View LinkedIn Profile</a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        except Exception as e:
            st.error(f"Error: {e}")
