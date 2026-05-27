# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from datetime import date
import re

st.set_page_config(page_title="UPR Calculator", layout="wide")

# ---------- CUSTOM CSS (unchanged) ----------
st.markdown("""
<style>
    /* Global */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
        font-family: 'Calisto MT', serif;
        font-size: 11pt;
    }
    
    /* Apply Calisto MT to all text elements */
    body, p, h1, h2, h3, h4, h5, h6, div, span, label, .stMarkdown, 
    .stTextInput label, .stDateInput label, .stSelectbox label, .stMultiSelect label,
    .stButton button, .stDownloadButton button, .stFileUploader label,
    .stAlert, .stInfo, .stWarning, .stError, .stSuccess, .stSpinner, 
    .stProgress, .stToast, .stSidebar, .stMetric, .stExpander {
        font-family: 'Calisto MT', serif !important;
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
        font-family: 'Calisto MT', serif;
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
        font-family: 'Calisto MT', serif;
    }
    .hero p {
        font-size: 1.2rem;
        max-width: 800px;
        margin: 0 auto;
        font-family: 'Calisto MT', serif;
    }
    
    /* Main container */
    .main-container {
        max-width: 1400px;
        margin: 2rem auto;
        padding: 0 2rem;
    }
    
    /* Required Column Containers */
    .required-container {
        background-color: #F9F9F9;
        border: 2px solid #D4AF37;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        min-height: 120px;
        height: auto;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        width: 100%;
        margin-bottom: 1rem;
    }
    .required-container h3 {
        color: #D4AF37;
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .required-container p {
        color: #666666;
        font-size: 0.85rem;
        margin-bottom: 0;
        line-height: 1.3;
    }
    
    /* Grouping Columns Container */
    .grouping-container {
        background-color: #F9F9F9;
        border: 2px solid #D4AF37;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .grouping-container h3 {
        color: #D4AF37;
        margin-top: 0;
        margin-bottom: 0.5rem;
        font-size: 1.2rem;
        font-weight: bold;
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
        font-family: 'Calisto MT', serif;
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
        font-family: 'Calisto MT', serif;
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
        font-family: 'Calisto MT', serif !important;
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
    
    .stMultiSelect [data-baseweb="select"], 
    .stSelectbox [data-baseweb="select"] {
        border: 1px solid #D4AF37;
        border-radius: 4px;
    }
    
    .dataframe {
        border: 1px solid #D4AF37;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Data Check Containers */
    .data-check-container {
        background-color: #E3F2FD;
        border: 2px solid #2196F3;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .data-check-warning {
        background-color: #FFF3E0;
        border: 2px solid #FF9800;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .data-check-error {
        background-color: #FFEBEE;
        border: 2px solid #F44336;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Fix for select box container */
    .stSelectbox div[data-baseweb="select"] {
        width: 100%;
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
    <p>Upload  CSV or Excel Data file. Map the columns to the required fields below. The app calculates UPR-equivalent reserves grouped by the selected columns (e.g., Line of Business, Currency) using the chosen method (365th, 24th, or 8th).</p>
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
    pass

valuation_date = pd.to_datetime(valuation_date)

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        original_filename = uploaded_file.name
        base_filename = re.sub(r'\.[^.]*$', '', original_filename)

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

        unnamed = [c for c in df.columns if c.startswith('Unnamed:')]
        if unnamed:
            df = df.drop(columns=unnamed)
            st.info(f"Dropped {len(unnamed)} unnamed column(s).")

        st.markdown("#### Preview of uploaded data")
        st.dataframe(df.head())
        st.markdown("---")

        # --- Column Mapping Section ---
        st.markdown("### Map Your Columns to Required Fields")
        all_columns = df.columns.tolist()
        
        # Required columns: Start_Date, End_Date, and at least one grouping column
        req_col1, req_col2 = st.columns(2)
        
        with req_col1:
            st.markdown("""
            <div class="required-container">
                <h3>Start_Date</h3>
                <p>The date when the policy starts (origin period)</p>
            </div>
            """, unsafe_allow_html=True)
            start_date_col = st.selectbox("Select your Start Date column", options=[""] + all_columns, key="start_date", label_visibility="collapsed")
            if start_date_col == "": start_date_col = None
        
        with req_col2:
            st.markdown("""
            <div class="required-container">
                <h3>End_Date</h3>
                <p>The date when the policy ends (development period)</p>
            </div>
            """, unsafe_allow_html=True)
            end_date_col = st.selectbox("Select your End Date column", options=[""] + all_columns, key="end_date", label_visibility="collapsed")
            if end_date_col == "": end_date_col = None

        st.markdown("---")
        
        # --- Grouping Columns Selection (NEW) ---
        st.markdown("""
        <div class="grouping-container">
            <h3>Grouping Columns</h3>
            <p>Select the columns you want to group by (e.g., Line_of_Business, Currency). Results will be aggregated by these columns.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Exclude the date columns from grouping options
        grouping_options = [col for col in all_columns if col not in [start_date_col, end_date_col]]
        grouping_cols = st.multiselect(
            "Choose columns to group results by (at least one required):",
            options=grouping_options,
            default=[grouping_options[0]] if grouping_options else [],
            help="Select one or more columns. The UPR results will be aggregated by these columns."
        )
        
        if not grouping_cols:
            st.error("Please select at least one grouping column (e.g., Line_of_Business).")
            st.stop()

        st.markdown("---")

        # --- Numeric columns selection ---
        st.markdown("### Select Numeric Columns for UPR Calculation")
        
        numeric_columns = []
        for col in df.columns:
            if col in [start_date_col, end_date_col] + grouping_cols:
                continue
            try:
                pd.to_numeric(df[col])
                numeric_columns.append(col)
            except (ValueError, TypeError):
                pass
        
        numeric_columns.extend([col for col in df.select_dtypes(include=[np.number]).columns.tolist() if col not in numeric_columns])
        numeric_columns = list(set(numeric_columns))
        
        if not numeric_columns:
            st.error("No numeric columns found.")
            st.stop()
        
        selected_value_cols = st.multiselect(
            "Choose the numeric columns you want to convert to UPR:",
            options=numeric_columns,
            default=numeric_columns[:min(4, len(numeric_columns))] if numeric_columns else []
        )

        if not start_date_col or not end_date_col:
            st.error("Please map all required date columns.")
            st.stop()
        
        if not selected_value_cols:
            st.warning("Please select at least one numeric column.")
            st.stop()

        # --- DATA CHECKS SECTION ---
        st.markdown("### Data Quality Checks")
        st.info("The following checks identify potential issues in your data. Please review and correct them before proceeding with the calculation.")
        
        df_check = df.copy()
        df_check = df_check.rename(columns={
            start_date_col: 'Start_Date',
            end_date_col: 'End_Date',
        })
        
        # Also rename grouping columns to keep original names (no renaming needed)
        # Keep original column names for grouping
        
        df_check['Start_Date'] = pd.to_datetime(df_check['Start_Date'], errors='coerce')
        df_check['End_Date'] = pd.to_datetime(df_check['End_Date'], errors='coerce')
        
        all_selected_cols = ['Start_Date', 'End_Date'] + grouping_cols + selected_value_cols
        
        has_critical_errors = False
        error_messages = []
        warning_messages = []
        
        # 1. Missing Values Check
        st.markdown("#### 1. Missing Values Check")
        missing_summary = {}
        for col in all_selected_cols:
            if col in df_check.columns:
                missing_count = df_check[col].isna().sum()
                missing_summary[col] = missing_count
                if missing_count > 0:
                    warning_messages.append(f"Column '{col}' has {missing_count} missing value(s).")
        
        missing_df = pd.DataFrame(list(missing_summary.items()), columns=['Column', 'Missing Values'])
        st.dataframe(missing_df, use_container_width=True)
        
        if sum(missing_summary.values()) == 0:
            st.success("✅ No missing values found.")
        else:
            st.warning(f"⚠️ Total missing values: {sum(missing_summary.values())}")
        
        # 2. Date Reasonability Check
        st.markdown("#### 2. Date Reasonability Check")
        
        valid_dates = df_check.dropna(subset=['Start_Date', 'End_Date'])
        invalid_dates = valid_dates[valid_dates['End_Date'] <= valid_dates['Start_Date']]
        
        if len(invalid_dates) > 0:
            has_critical_errors = True
            error_messages.append(f"Found {len(invalid_dates)} row(s) where End_Date is not after Start_Date.")
            st.error(f"❌ {len(invalid_dates)} row(s) have End_Date <= Start_Date.")
            with st.expander("View invalid date rows (first 10)"):
                st.dataframe(invalid_dates[['Start_Date', 'End_Date']].head(10))
        else:
            st.success("✅ All valid dates have End_Date after Start_Date.")
        
        # 3. Duplicate Entry Check
        st.markdown("#### 3. Duplicate Entry Check")
        
        duplicate_rows = df_check[df_check.duplicated()]
        if len(duplicate_rows) > 0:
            warning_messages.append(f"Found {len(duplicate_rows)} exact duplicate row(s).")
            st.warning(f"⚠️ {len(duplicate_rows)} exact duplicate row(s) found.")
            with st.expander("View duplicate rows (first 10)"):
                st.dataframe(duplicate_rows.head(10))
        else:
            st.success("✅ No exact duplicate rows found.")
        
        # --- Summary of Data Checks ---
        st.markdown("#### Data Quality Summary")
        
        if error_messages:
            st.markdown('<div class="data-check-error">', unsafe_allow_html=True)
            st.markdown("**❌ Critical Issues Found - Please fix these before continuing:**")
            for err in error_messages:
                st.write(f"• {err}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if warning_messages:
            st.markdown('<div class="data-check-warning">', unsafe_allow_html=True)
            st.markdown("**⚠️ Warnings - Recommended to review:**")
            for warn in warning_messages:
                st.write(f"• {warn}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        if not error_messages and not warning_messages:
            st.markdown('<div class="data-check-container">', unsafe_allow_html=True)
            st.markdown("**✅ All data quality checks passed!**")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        if has_critical_errors:
            st.error("❌ Calculation cannot proceed due to critical data issues. Please fix the issues above and re-upload your file.")
            st.stop()
        
        # --- Prepare data for calculation ---
        df_processed = df_check.copy()
        
        # Remove rows with invalid dates
        df_processed = df_processed.dropna(subset=['Start_Date', 'End_Date'])
        df_processed = df_processed[df_processed['End_Date'] > df_processed['Start_Date']]
        
        original_value_cols = selected_value_cols
        
        for col in original_value_cols:
            if col in df_processed.columns:
                df_processed[col] = pd.to_numeric(df_processed[col], errors='coerce')
        
        df_processed["Duration"] = (df_processed["End_Date"] - df_processed["Start_Date"]).dt.days
        df_processed = df_processed[df_processed["Duration"] > 0]

        if df_processed.empty:
            st.error("No valid policies remaining after data cleaning.")
            st.stop()

        # --- CALCULATE BUTTON ---
        if st.button("Calculate UPR", use_container_width=True):
            with st.spinner("Calculating UPR..."):
                conditions = [
                    valuation_date < df_processed["Start_Date"],
                    valuation_date > df_processed["End_Date"],
                    (valuation_date <= df_processed["End_Date"]) & (valuation_date >= df_processed["Start_Date"])
                ]

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

                for col in original_value_cols:
                    df_processed[f"{col}_UPR"] = df_processed["Unearned_portion"] * df_processed[col]

                # Group by the selected grouping columns
                upr_columns = [f"{col}_UPR" for col in original_value_cols]
                result = df_processed.groupby(grouping_cols)[upr_columns].sum().reset_index()
                
                # Rename result columns (remove _UPR suffix)
                result.columns = grouping_cols + [col.replace('_UPR', '') for col in upr_columns]

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("UPR Results by " + ", ".join(grouping_cols))
                
                display_result = result.copy()
                for col in display_result.columns:
                    if col not in grouping_cols:
                        display_result[col] = display_result[col].apply(lambda x: f"{x:,.2f}" if pd.notna(x) else "N/A")
                
                st.dataframe(display_result, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    result.to_excel(writer, index=False, sheet_name='UPR_Results')
                output.seek(0)

                safe_client = re.sub(r'[\\/*?:"<>|]', "", client_name).strip()
                safe_client = safe_client if safe_client else "Client"
                safe_original = re.sub(r'[\\/*?:"<>|]', "", base_filename).strip()
                safe_original = safe_original if safe_original else "Data"
                
                file_name = f"{safe_client}_{safe_original}_UPR_Results.xlsx"

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
