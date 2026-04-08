# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from datetime import date

st.set_page_config(page_title="UPR Calculator", layout="wide")

# ---------- CUSTOM CSS (African Actuarial Consultants theme) ----------
st.markdown("""
<style>
    /* Global */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
        font-family: 'Calisto MT', serif;
        font-size: 11pt;
    }
    /* Header / Navigation */
    .header {
        background-color: #000000;
        padding: 1rem 2rem;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        border-bottom: 3px solid #D4AF37;
    }
    .nav-links a {
        color: #FFFFFF;
        margin-left: 2rem;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s;
    }
    .nav-links a:hover {
        color: #D4AF37;
    }
    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #000000 0%, #333333 100%);
        color: #FFFFFF;
        padding: 2rem 2rem;
        text-align: center;
        border-bottom: 3px solid #D4AF37;
    }
    .hero h1 {
        color: #D4AF37;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .hero p {
        font-size: 1.2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    /* Main container */
    .main-container {
        max-width: 1400px;
        margin: 2rem auto;
        padding: 0 2rem;
    }
    /* Cards */
    .card {
        background-color: #F9F9F9;
        border: 1px solid #D4AF37;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    .card h3 {
        color: #D4AF37;
        margin-top: 0;
        border-bottom: 2px solid #D4AF37;
        padding-bottom: 0.5rem;
    }
    /* Footer */
    .footer {
        background-color: #000000;
        color: #FFFFFF;
        text-align: center;
        padding: 1.5rem;
        border-top: 3px solid #D4AF37;
        margin-top: 3rem;
    }
    .footer a {
        color: #D4AF37;
        text-decoration: none;
    }
    /* Streamlit element overrides */
    .stButton > button, .stDownloadButton > button {
        background-color: #D4AF37;
        color: #000000;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #B8960F;
        color: #FFFFFF;
    }
    .stFileUploader {
        border: 2px dashed #D4AF37;
        border-radius: 5px;
        padding: 1rem;
    }
    .stMultiSelect [data-baseweb="select"] {
        border: 1px solid #D4AF37;
        border-radius: 4px;
    }
    .stSelectbox [data-baseweb="select"] {
        border: 1px solid #D4AF37;
        border-radius: 4px;
    }
    .dataframe {
        border: 1px solid #D4AF37;
        border-radius: 8px;
        overflow: hidden;
    }
    .required-badge {
        background-color: #D4AF37;
        color: #000000;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 10pt;
        font-weight: bold;
        display: inline-block;
        margin-left: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="header">
    <div class="nav-links">
        <a href="#">Home</a>
        <a href="#">Services</a>
        <a href="#">Tools</a>
        <a href="#">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown("""
<div class="hero">
    <h1>Unearned Premium Reserve (UPR) Calculator</h1>
    <p>Upload your CSV or Excel file. Map your columns to the required fields below. The app calculates UPR-equivalent reserves grouped by line of business using the selected method (365th, 24th, or 8th).</p>
</div>
""", unsafe_allow_html=True)

# ---------- Main Container ----------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- User inputs ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    valuation_date = st.date_input("Valuation Date", value=date(2025, 12, 31))
with col2:
    client_name = st.text_input("Client Name (for file name)", value="Client").strip()
with col3:
    method = st.selectbox("UPR Calculation Method", ["365th (exact days)", "24th (half-month)", "8th (half-quarter)"])
with col4:
    # empty for spacing
    pass

valuation_date = pd.to_datetime(valuation_date)

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Read file based on extension
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            try:
                df = pd.read_csv(uploaded_file, encoding='utf-8')
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='cp1252')
                st.info("File read with Windows-1252 encoding.")
        else:
            df = pd.read_excel(uploaded_file)

        # Drop unnamed columns
        unnamed = [c for c in df.columns if c.startswith('Unnamed:')]
        if unnamed:
            df = df.drop(columns=unnamed)
            st.info(f"Dropped {len(unnamed)} unnamed column(s).")

        # Preview
        with st.expander("Preview of uploaded data"):
            st.dataframe(df.head())

        # --- Column Mapping Section ---
        st.markdown("### Map Your Columns to Required Fields")
        st.markdown("The calculator requires the following columns. Please select which column in your data corresponds to each required field:")

        # Display required columns in a structured way
        required_fields = {
            'Start Date': 'The date when the policy starts (origin period)',
            'End Date': 'The date when the policy ends (development period)',
            'Line of Business': 'The category/segment for grouping results (e.g., Motor, Property, Health)'
        }
        
        # Create a container for required column mapping
        with st.container():
            st.markdown("#### Required Columns")
            
            # Get all column names for selection
            all_columns = df.columns.tolist()
            
            # Create three columns for the required mappings
            req_col1, req_col2, req_col3 = st.columns(3)
            
            with req_col1:
                start_date_col = st.selectbox(
                    "**Start Date** \n*Policy start date*", 
                    options=all_columns,
                    key="start_date"
                )
            
            with req_col2:
                end_date_col = st.selectbox(
                    "**End Date** \n*Policy end date*", 
                    options=all_columns,
                    key="end_date"
                )
            
            with req_col3:
                lob_col = st.selectbox(
                    "**Line of Business** \n*Grouping category*", 
                    options=all_columns,
                    key="lob"
                )

        # Numeric columns selection
        st.markdown("####Numeric Columns for UPR Calculation")
        st.markdown("Select which numeric columns (premiums, commissions, etc.) you want to calculate UPR for:")
        
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_columns:
            st.error("No numeric columns found in your data. Please ensure your file contains numeric columns for UPR calculation.")
            st.stop()
        
        selected_value_cols = st.multiselect(
            "**Select numeric columns**\n*Choose all columns that contain amounts you want to convert to UPR*",
            options=numeric_columns,
            default=numeric_columns[:min(4, len(numeric_columns))] if numeric_columns else [],
            help="Examples: Gross Premium, Reinsurance Premium, Commission amounts, etc."
        )

        # Validate mappings
        if not start_date_col or not end_date_col or not lob_col:
            st.error("Please map all required columns (Start Date, End Date, Line of Business).")
            st.stop()
        
        if not selected_value_cols:
            st.warning("Please select at least one numeric column for UPR calculation.")
            st.stop()

        # Show mapping summary
        with st.expander("View Column Mapping Summary"):
            mapping_data = {
                'Required Field': ['Start Date', 'End Date', 'Line of Business'],
                'Your Column': [start_date_col, end_date_col, lob_col],
                'Description': [
                    'Policy start date (origin period)',
                    'Policy end date (development period)',
                    'Category for grouping results'
                ]
            }
            mapping_df = pd.DataFrame(mapping_data)
            st.dataframe(mapping_df, use_container_width=True)
            
            st.markdown("**Selected numeric columns for UPR calculation:**")
            st.write(selected_value_cols)

        # --- Rename columns for internal processing ---
        df_processed = df.rename(columns={
            start_date_col: 'Start_Date',
            end_date_col: 'End_Date',
            lob_col: 'Line_of_business'
        })

        # Keep original numeric column names
        original_value_cols = selected_value_cols

        # --- Date parsing with error reporting ---
        orig_start = df_processed['Start_Date'].copy()
        orig_end = df_processed['End_Date'].copy()

        df_processed['Start_Date'] = pd.to_datetime(df_processed['Start_Date'], errors='coerce')
        df_processed['End_Date'] = pd.to_datetime(df_processed['End_Date'], errors='coerce')

        bad_start = orig_start[df_processed['Start_Date'].isna() & orig_start.notna()]
        bad_end = orig_end[df_processed['End_Date'].isna() & orig_end.notna()]

        if not bad_start.empty or not bad_end.empty:
            st.error("Some date values could not be parsed. Please check your data.")
            if not bad_start.empty:
                st.write("**Invalid Start_Date values (first 10):**")
                st.write(bad_start.head(10).tolist())
            if not bad_end.empty:
                st.write("**Invalid End_Date values (first 10):**")
                st.write(bad_end.head(10).tolist())
            st.stop()

        # Calculate Duration in days
        df_processed["Duration"] = (df_processed["End_Date"] - df_processed["Start_Date"]).dt.days
        
        # Remove rows with invalid duration
        if (df_processed["Duration"] <= 0).any():
            st.warning("Some policies have zero or negative duration. They will be excluded.")
            df_processed = df_processed[df_processed["Duration"] > 0]

        if df_processed.empty:
            st.error("No valid policies remaining after filtering. Please check your data.")
            st.stop()

        # --- CALCULATE BUTTON ---
        if st.button("Calculate UPR", use_container_width=True):
            with st.spinner("Calculating UPR..."):
                # Define conditions
                conditions = [
                    valuation_date < df_processed["Start_Date"],
                    valuation_date > df_processed["End_Date"],
                    (valuation_date <= df_processed["End_Date"]) & (valuation_date >= df_processed["Start_Date"])
                ]

                # Calculate unearned portion based on selected method
                if method == "365th (exact days)":
                    total = df_processed["Duration"]
                    remaining = (df_processed["End_Date"] - valuation_date).dt.days
                    choices = [1, 0, remaining / total]
                    df_processed["Unearned_portion"] = np.select(conditions, choices, default=np.nan)

                elif method == "24th (half-month)":
                    interval_days = 365.25 / 24
                    total = df_processed["Duration"] / interval_days
                    remaining = (df_processed["End_Date"] - valuation_date).dt.days / interval_days
                    choices = [1, 0, remaining / total]
                    df_processed["Unearned_portion"] = np.select(conditions, choices, default=np.nan)

                elif method == "8th (half-quarter)":
                    interval_days = 365.25 / 8
                    total = df_processed["Duration"] / interval_days
                    remaining = (df_processed["End_Date"] - valuation_date).dt.days / interval_days
                    choices = [1, 0, remaining / total]
                    df_processed["Unearned_portion"] = np.select(conditions, choices, default=np.nan)

                # Calculate UPR for each selected column
                for col in original_value_cols:
                    df_processed[f"{col}_UPR"] = df_processed["Unearned_portion"] * df_processed[col]

                # Aggregate by Line of Business
                upr_columns = [f"{col}_UPR" for col in original_value_cols]
                result = df_processed.groupby('Line_of_business')[upr_columns].sum().reset_index()
                
                # Rename result columns
                result.columns = ['Line_of_business'] + [col.replace('_UPR', '') for col in upr_columns]

                # Display results
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("UPR Results by Line of Business")
                
                # Format for display
                display_result = result.copy()
                for col in display_result.columns:
                    if col != 'Line_of_business':
                        display_result[col] = display_result[col].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
                
                st.dataframe(display_result, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Prepare Excel download
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    result.to_excel(writer, index=False, sheet_name='UPR_Results')
                output.seek(0)

                # Filename with client name
                safe_client = "".join(c for c in client_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                file_name = f"{safe_client}_UPR_Results.xlsx" if safe_client else "UPR_Results.xlsx"

                st.download_button(
                    label="Download results as Excel",
                    data=output,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.write("Please check your file format and column selections.")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Footer ----------
st.markdown("""
<div class="footer">
    <p>© 2026 African Actuarial Consultants. All rights reserved. | <a href="#">Privacy</a> | <a href="#">Terms</a></p>
    <p style="margin-top: 0.5rem; font-size: 0.9rem;">Powered by Vanababa</p>
</div>
""", unsafe_allow_html=True)
