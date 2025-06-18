# # 📊 Smart CSV Analyzer Dashboard

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import seaborn as sns
# import matplotlib.pyplot as plt

# # 🛠️ Page Config
# st.set_page_config(page_title="📊 Executive Dashboard", layout="wide", page_icon="📈")

# # 💄 Custom Styles
# st.markdown("""
#     <style>
#     .big-font { font-size:30px !important; font-weight:700; }
#     .section-header { font-size:22px; margin-top:30px; font-weight:bold; color:#3A5AFF; }
#     .st-emotion-cache-1v0mbdj p { font-size: 16px; }
#     </style>
# """, unsafe_allow_html=True)

# # 🧠 Main Title
# st.markdown('<p class="big-font">📊 Data Insight Dashboard - Smart CSV Analyzer</p>', unsafe_allow_html=True)

# # 📤 Sidebar - Upload CSV
# with st.sidebar:
#     st.header("📤 Upload Data")
#     uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

# # ✅ Main Logic
# if uploaded_file:
#     df = pd.read_csv(uploaded_file)
#     st.sidebar.success("✅ File uploaded!")

#     row_limit = st.sidebar.selectbox("🔢 Rows to display", [5, 10, 20, 50, 100, 500, "All"])
#     display_df = df if row_limit == "All" else df.head(int(row_limit))

#     st.subheader("📌 Key Metrics")
#     total_rows = df.shape[0]
#     total_columns = df.shape[1]
#     missing_percent = round((df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100, 2)
#     duplicate_rows = df.duplicated().sum()
#     num_cols = df.select_dtypes(include='number').shape[1]
#     cat_cols = df.select_dtypes(exclude='number').shape[1]

#     col1, col2, col3 = st.columns(3)
#     col1.metric("📄 Total Records", f"{total_rows:,}")
#     col2.metric("🧩 Total Features", total_columns)
#     col3.metric("⚠️ Missing Data (%)", f"{missing_percent}%")

#     col4, col5, col6 = st.columns(3)
#     col4.metric("🔢 Numeric Features", num_cols)
#     col5.metric("🔤 Categorical Features", cat_cols)
#     col6.metric("♻️ Duplicate Rows", duplicate_rows)

#     st.markdown('<div class="section-header">🔍 Filter Data</div>', unsafe_allow_html=True)
#     filter_col = st.selectbox("Select a column to filter", df.columns)
#     unique_values = df[filter_col].dropna().unique()
#     selected_values = st.multiselect("Select values to include", unique_values)
#     if selected_values:
#         df = df[df[filter_col].isin(selected_values)]
#         st.success(f"Showing {len(df)} filtered rows.")

#     st.markdown('<div class="section-header">📊 Custom Chart Generator</div>', unsafe_allow_html=True)
#     if not df.empty:
#         x_axis = st.selectbox("Select X-axis", df.columns)
#         y_axis = st.selectbox("Select Y-axis", df.select_dtypes(include='number').columns)
#         color_dim = st.selectbox("Select Color (Optional)", [None] + df.columns.tolist())
#         chart_type = st.selectbox("Select Chart Type", ["Scatter", "Line", "Bar", "Area"])

#         if st.button("Generate Chart"):
#             if chart_type == "Scatter":
#                 fig = px.scatter(df, x=x_axis, y=y_axis, color=color_dim)
#             elif chart_type == "Line":
#                 fig = px.line(df, x=x_axis, y=y_axis, color=color_dim)
#             elif chart_type == "Bar":
#                 fig = px.bar(df, x=x_axis, y=y_axis, color=color_dim)
#             elif chart_type == "Area":
#                 fig = px.area(df, x=x_axis, y=y_axis, color=color_dim)
#             st.plotly_chart(fig, use_container_width=True)

#     # 📋 Data Table (Simple)
#     st.markdown('<div class="section-header">📋 Data Table</div>', unsafe_allow_html=True)
#     st.dataframe(display_df, use_container_width=True)

#     # 📊 Category Distribution
#     st.markdown('<div class="section-header">📊 Category Distribution</div>', unsafe_allow_html=True)
#     cat_columns = df.select_dtypes(include=['object', 'category']).columns
#     if len(cat_columns):
#         col1, col2 = st.columns(2)
#         with col1:
#             cat_col = st.selectbox("Choose categorical column", cat_columns)
#         with col2:
#             chart_type = st.selectbox("Choose chart type", ["Bar Chart", "Pie Chart", "Histogram"])
#         value_counts_df = df[cat_col].value_counts().reset_index()
#         value_counts_df.columns = [cat_col, 'count']

#         if chart_type == "Bar Chart":
#             st.plotly_chart(px.bar(value_counts_df, x=cat_col, y='count', color='count'), use_container_width=True)
#         elif chart_type == "Pie Chart":
#             st.plotly_chart(px.pie(value_counts_df, names=cat_col, values='count'), use_container_width=True)
#         elif chart_type == "Histogram":
#             st.plotly_chart(px.histogram(df, x=cat_col), use_container_width=True)

#     # 🔁 Pivot Table
#     st.markdown('<div class="section-header">🔁 Pivot Table</div>', unsafe_allow_html=True)
#     group_cols = st.multiselect("Group By", df.columns.tolist())
#     agg_cols = st.multiselect("Aggregate Columns", df.select_dtypes(include='number').columns.tolist())
#     agg_funcs = st.multiselect("Aggregation Functions", ["sum", "mean", "count", "min", "max", "nunique"], default=["sum"])

#     if st.button("Generate Pivot Table"):
#         if group_cols and agg_cols:
#             pivot = df.groupby(group_cols)[agg_cols].agg(agg_funcs)
#             if isinstance(pivot.columns, pd.MultiIndex):
#                 pivot.columns = ['_'.join(map(str, col)).strip() for col in pivot.columns]
#             st.dataframe(pivot.reset_index(), use_container_width=True)
#         else:
#             st.warning("Select at least one group and one aggregation column.")

#     # ➕ Add Calculated Column
#     st.markdown('<div class="section-header">➕ Add Calculated Column</div>', unsafe_allow_html=True)
#     formula = st.text_input("Enter formula (e.g., col1 * 2 + col2)")
#     new_col_name = st.text_input("New column name")
#     if st.button("Add Column") and formula and new_col_name:
#         try:
#             df[new_col_name] = df.eval(formula)
#             st.success(f"Added new column: {new_col_name}")
#             st.dataframe(df.head(), use_container_width=True)
#         except Exception as e:
#             st.error(f"Error: {e}")

#     # 📈 Correlation Heatmap
#     st.markdown('<div class="section-header">📈 Correlation Heatmap</div>', unsafe_allow_html=True)
#     numeric_df = df.select_dtypes(include='number')
#     if not numeric_df.empty:
#         fig, ax = plt.subplots(figsize=(10, 6))
#         sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
#         st.pyplot(fig)






# 📊 Smart CSV Analyzer Dashboard

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# 🛠️ Page Config
st.set_page_config(page_title="📊 Executive Dashboard", layout="wide", page_icon="📈")

# 💄 Custom Styles
st.markdown("""
    <style>
    .big-font { font-size:30px !important; font-weight:700; }
    .section-header { font-size:22px; margin-top:30px; font-weight:bold; color:#3A5AFF; }
    .st-emotion-cache-1v0mbdj p { font-size: 16px; }
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

    row_limit = st.sidebar.selectbox("🔢 Rows to display", [5, 10, 20, 50, 100, 500, "All"])
    display_df = df if row_limit == "All" else df.head(int(row_limit))

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
        chart_sample = st.slider("Limit records to plot", min_value=10, max_value=len(df), value=min(100, len(df)))

        if st.button("Generate Chart"):
            chart_df = df.sample(chart_sample) if chart_sample < len(df) else df
            if chart_type == "Scatter":
                fig = px.scatter(chart_df, x=x_axis, y=y_axis, color=color_dim, template="plotly_white")
            elif chart_type == "Line":
                fig = px.line(chart_df, x=x_axis, y=y_axis, color=color_dim, template="plotly_white")
            elif chart_type == "Bar":
                fig = px.bar(chart_df, x=x_axis, y=y_axis, color=color_dim, template="plotly_white")
            elif chart_type == "Area":
                fig = px.area(chart_df, x=x_axis, y=y_axis, color=color_dim, template="plotly_white")
            fig.update_layout(hovermode="closest", title=f"{chart_type} Chart", height=500)
            st.plotly_chart(fig, use_container_width=True)

    # 📋 Data Table
    st.markdown('<div class="section-header">📋 Data Table</div>', unsafe_allow_html=True)
    st.dataframe(display_df, use_container_width=True)

    # 📊 Category Distribution
    st.markdown('<div class="section-header">📊 Category Distribution</div>', unsafe_allow_html=True)
    cat_columns = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_columns):
        col1, col2, col3 = st.columns(3)
        with col1:
            cat_col = st.selectbox("Choose categorical column", cat_columns)
        with col2:
            chart_type = st.selectbox("Choose chart type", ["Bar Chart", "Pie Chart", "Histogram"])
        with col3:
            limit = st.slider("Limit top categories", min_value=5, max_value=50, value=10)

        value_counts_df = df[cat_col].value_counts().nlargest(limit).reset_index()
        value_counts_df.columns = [cat_col, 'count']

        if chart_type == "Bar Chart":
            fig = px.bar(value_counts_df, x=cat_col, y='count', color='count', template="plotly_dark")
        elif chart_type == "Pie Chart":
            fig = px.pie(value_counts_df, names=cat_col, values='count', template="seaborn")
        elif chart_type == "Histogram":
            fig = px.histogram(df[df[cat_col].isin(value_counts_df[cat_col])], x=cat_col, template="ggplot2")

        fig.update_layout(title=f"{chart_type} for {cat_col}", height=500)
        st.plotly_chart(fig, use_container_width=True)

    # 🔁 Pivot Table
    st.markdown('<div class="section-header">🔁 Pivot Table</div>', unsafe_allow_html=True)
    group_cols = st.multiselect("Group By", df.columns.tolist())
    agg_cols = st.multiselect("Aggregate Columns", df.select_dtypes(include='number').columns.tolist())
    agg_funcs = st.multiselect("Aggregation Functions", ["sum", "mean", "count", "min", "max", "nunique"], default=["sum"])

    if st.button("Generate Pivot Table"):
        if group_cols and agg_cols:
            pivot = df.groupby(group_cols)[agg_cols].agg(agg_funcs)
            if isinstance(pivot.columns, pd.MultiIndex):
                pivot.columns = ['_'.join(map(str, col)).strip() for col in pivot.columns]
            st.dataframe(pivot.reset_index(), use_container_width=True)
        else:
            st.warning("Select at least one group and one aggregation column.")

    # ➕ Add Calculated Column
    st.markdown('<div class="section-header">➕ Add Calculated Column</div>', unsafe_allow_html=True)
    formula = st.text_input("Enter formula (e.g., col1 * 2 + col2)")
    new_col_name = st.text_input("New column name")
    if st.button("Add Column") and formula and new_col_name:
        try:
            df[new_col_name] = df.eval(formula)
            st.success(f"Added new column: {new_col_name}")
            st.dataframe(df.head(), use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")

    # 📈 Correlation Heatmap
    st.markdown('<div class="section-header">📈 Correlation Heatmap</div>', unsafe_allow_html=True)
    numeric_df = df.select_dtypes(include='number')
    if not numeric_df.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

else:
    st.warning("🚨 Please upload a CSV file to begin analysis.")
