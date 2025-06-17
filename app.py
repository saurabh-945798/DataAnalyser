# 📊 Smart CSV Analyzer Dashboard

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from pyod.models.iforest import IForest
from ydata_profiling import ProfileReport
import sweetviz as sv
from streamlit_extras.metric_cards import style_metric_cards
from st_aggrid import AgGrid, GridOptionsBuilder
import os

# 🛠️ Page Config
st.set_page_config(page_title="📊 Executive Dashboard", layout="wide", page_icon="📈")

# 💄 Custom Styles
st.markdown("""
    <style>
    .big-font { font-size:30px !important; font-weight:700; }
    .section-header { font-size:22px; margin-top:30px; font-weight:bold; color:#3A5AFF; }
    .st-emotion-cache-1v0mbdj p { font-size: 16px; }
    .metric-card { padding: 1rem; border-radius: 12px; background-color: #f0f2f6; }
    </style>
""", unsafe_allow_html=True)

# 🧠 Main Title
st.markdown('<p class="big-font">📊 Data Insight Dashboard - Smart CSV Analyzer</p>', unsafe_allow_html=True)

# 📤 Sidebar - Upload CSV
with st.sidebar:
    st.header("📤 Upload Data")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

# ✅ Main Logic
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ File uploaded!")

    # 📏 Row Display Limit
    row_limit = st.sidebar.selectbox("🔢 Rows to display", [10,20, 50, 100, 500, "All"])
    display_df = df if row_limit == "All" else df.head(int(row_limit))

    # 🔢 Key Metrics
    st.subheader("📌 Key Metrics")
    total_rows = df.shape[0]
    total_columns = df.shape[1]
    missing_percent = round((df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100, 2)
    duplicate_rows = df.duplicated().sum()
    num_cols = df.select_dtypes(include='number').shape[1]
    cat_cols = df.select_dtypes(exclude='number').shape[1]

    col1, col2, col3 = st.columns(3)
    col1.metric("📄 Total Records", f"{total_rows:,}")
    col2.metric("🧩 Total Features", total_columns)
    col3.metric("⚠️ Missing Data (%)", f"{missing_percent}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("🔢 Numeric Features", num_cols)
    col5.metric("🔤 Categorical Features", cat_cols)
    col6.metric("♻️ Duplicate Rows", duplicate_rows)

    try:
        style_metric_cards()
    except:
        pass

    # 🔍 Data Filter
    st.markdown('<div class="section-header">🔍 Filter Data</div>', unsafe_allow_html=True)
    filter_col = st.selectbox("Select a column to filter", df.columns)
    unique_values = df[filter_col].dropna().unique()
    selected_values = st.multiselect("Select values to include", unique_values)
    if selected_values:
        df = df[df[filter_col].isin(selected_values)]
        st.success(f"Showing {len(df)} filtered rows.")

    # 📊 Custom Chart Generator
    st.markdown('<div class="section-header">📊 Custom Chart Generator</div>', unsafe_allow_html=True)
    if not df.empty:
        x_axis = st.selectbox("Select X-axis", df.columns)
        y_axis = st.selectbox("Select Y-axis", df.select_dtypes(include='number').columns)
        color_dim = st.selectbox("Select Color (Optional)", [None] + df.columns.tolist())
        chart_type = st.selectbox("Select Chart Type", ["Scatter", "Line", "Bar", "Area"])

        if st.button("Generate Chart"):
            if chart_type == "Scatter":
                fig = px.scatter(df, x=x_axis, y=y_axis, color=color_dim)
            elif chart_type == "Line":
                fig = px.line(df, x=x_axis, y=y_axis, color=color_dim)
            elif chart_type == "Bar":
                fig = px.bar(df, x=x_axis, y=y_axis, color=color_dim)
            elif chart_type == "Area":
                fig = px.area(df, x=x_axis, y=y_axis, color=color_dim)
            st.plotly_chart(fig, use_container_width=True)

    # 📋 Data Table
    st.markdown('<div class="section-header">📋 Data Table</div>', unsafe_allow_html=True)
    gb = GridOptionsBuilder.from_dataframe(display_df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_default_column(filterable=True, sortable=True, resizable=True, editable=True)
    grid_options = gb.build()
    AgGrid(display_df, gridOptions=grid_options, height=400, fit_columns_on_grid_load=True)

    # 📊 Category Distribution
    st.markdown('<div class="section-header">📊 Category Distribution</div>', unsafe_allow_html=True)
    cat_columns = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_columns):
        col1, col2 = st.columns(2)
        with col1:
            cat_col = st.selectbox("Choose categorical column", cat_columns)
        with col2:
            chart_type = st.selectbox("Choose chart type", [
                "Bar Chart", "Pie Chart", "Histogram",
                "Donut Chart", "Treemap", "Funnel Chart",
                "Sunburst Chart", "Strip Plot"
            ])
        value_counts_df = df[cat_col].value_counts().reset_index()
        value_counts_df.columns = [cat_col, 'count']

        if chart_type == "Bar Chart":
            st.plotly_chart(px.bar(value_counts_df, x=cat_col, y='count', color='count'), use_container_width=True)
        elif chart_type == "Pie Chart":
            st.plotly_chart(px.pie(value_counts_df, names=cat_col, values='count'), use_container_width=True)
        elif chart_type == "Histogram":
            st.plotly_chart(px.histogram(df, x=cat_col), use_container_width=True)
        elif chart_type == "Donut Chart":
            fig = px.pie(value_counts_df, names=cat_col, values='count', hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Treemap":
            fig = px.treemap(value_counts_df, path=[cat_col], values='count')
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Funnel Chart":
            fig = px.funnel(value_counts_df, x='count', y=cat_col)
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Sunburst Chart":
            fig = px.sunburst(value_counts_df, path=[cat_col], values='count')
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Strip Plot":
            fig = px.strip(df, x=cat_col)
            st.plotly_chart(fig, use_container_width=True)

    # 🔁 Pivot Table
    st.markdown('<div class="section-header">🔁 Advanced Pivot Table Builder</div>', unsafe_allow_html=True)
    group_cols = st.multiselect("🔹 Select Grouping Columns (1 to 3)", df.columns.tolist(), default=[df.columns[0]])
    agg_cols = st.multiselect("🔸 Select Columns to Aggregate", df.select_dtypes(include=['number']).columns.tolist())
    agg_funcs = st.multiselect("📐 Select Aggregation Functions", ["sum", "mean", "count", "min", "max", "nunique"], default=["sum"])

    if st.button("🔍 Generate Pivot Table"):
        if not group_cols:
            st.warning("⚠️ Please select at least one grouping column.")
        elif not agg_cols:
            st.warning("⚠️ Please select at least one column to aggregate.")
        elif len(group_cols) > 3:
            st.error("❌ Please select a maximum of 3 grouping columns.")
        else:
            try:
                pivot = df.groupby(group_cols)[agg_cols].agg(agg_funcs)
                if isinstance(pivot.columns, pd.MultiIndex):
                    pivot.columns = ['_'.join(map(str, col)).strip() for col in pivot.columns]
                pivot = pivot.reset_index()
                st.success("✅ Pivot Table Created Successfully")
                st.dataframe(pivot, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error while creating pivot table: {e}")

    # ➕ Add Calculated Column
    st.markdown('<div class="section-header">➕ Add Calculated Column</div>', unsafe_allow_html=True)
    formula = st.text_input("Enter formula (e.g., col1 * 1.1 + col2)")
    new_col_name = st.text_input("New column name")
    if st.button("Add Column") and formula and new_col_name:
        try:
            df[new_col_name] = df.eval(formula)
            st.success(f"✅ Column '{new_col_name}' added.")
            st.dataframe(df.head(), use_container_width=True)
        except Exception as e:
            st.error(f"❌ Error in formula: {e}")

    # 📈 Correlation Heatmap
    st.markdown('<div class="section-header">📈 Correlation Heatmap</div>', unsafe_allow_html=True)
    numeric_df = df.select_dtypes(include='number')
    if not numeric_df.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    # 🚨 Outlier Detection
    st.markdown('<div class="section-header">🚨 Outlier Detection</div>', unsafe_allow_html=True)
    if st.button("Detect Outliers"):
        if not numeric_df.empty:
            clf = IForest()
            clf.fit(numeric_df)
            df['Outlier'] = clf.labels_
            st.success("✅ Outliers detected using Isolation Forest.")
            st.dataframe(df[df["Outlier"] == 1], use_container_width=True)
        else:
            st.warning("⚠️ No numeric columns available for outlier detection.")

    # 🧠 ydata-profiling Report
    st.markdown('<div class="section-header">🧠 ydata-profiling Report</div>', unsafe_allow_html=True)
    if st.button("Generate Profile Report"):
        profile = ProfileReport(df, explorative=True)
        profile.to_file("profile_report.html")
        with open("profile_report.html", "r", encoding="utf-8") as f:
            html = f.read()
            st.components.v1.html(html, height=800, scrolling=True)

    # 📈 Sweetviz Report
    st.markdown('<div class="section-header">📈 Sweetviz Auto Report</div>', unsafe_allow_html=True)
    if st.button("Generate Sweetviz Report"):
        report = sv.analyze(df)
        report_path = "sweetviz_report.html"
        report.show_html(report_path, open_browser=False)
        with open(report_path, 'r', encoding="utf-8") as f:
            html = f.read()
            st.components.v1.html(html, height=800, scrolling=True)
