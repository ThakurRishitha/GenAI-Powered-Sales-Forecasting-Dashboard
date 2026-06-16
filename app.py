import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="GenAI Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    return df

df = load_data()
st.write("Rows:", len(df))
st.write("Missing Dates:", df["Order Date"].isnull().sum())
st.write(df[["Order Date", "Sales"]].head())

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🚀 Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "🏠 Dashboard",
        "📈 Sales Analytics",
        "🌍 Regional Analytics",
        "👥 Customer Analytics",
        "📦 Product Analytics",
        "🔮 Forecasting",
        "🤖 AI Insights",
        "💬 AI Assistant",
        "📄 Reports"
    ]
)

# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if page == "🏠 Dashboard":

    st.title("🚀 GenAI-Powered Sales Forecasting Dashboard")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "💰 Sales",
        f"₹{df['Sales'].sum():,.0f}"
    )

    col2.metric(
        "📈 Profit",
        f"₹{df['Profit'].sum():,.0f}"
    )

    col3.metric(
        "📦 Orders",
        df["Order ID"].nunique()
    )

    col4.metric(
        "👥 Customers",
        df["Customer ID"].nunique()
    )

    col5.metric(
        "🛒 Avg Order",
        f"₹{df['Sales'].mean():,.0f}"
    )

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

# --------------------------------------------------
# SALES ANALYTICS
# --------------------------------------------------

elif page == "📈 Sales Analytics":

    st.header("📈 Sales Analytics")

    monthly_sales = (
        df.groupby(
            df["Order Date"].dt.to_period("M")
        )["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Order Date"] = (
        monthly_sales["Order Date"].astype(str)
    )

    fig = px.line(
        monthly_sales,
        x="Order Date",
        y="Sales",
        title="Monthly Sales Trend",
        markers=True
    )

    st.plotly_chart(fig)

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        title="Sales by Category"
    )

    st.plotly_chart(fig2)

# --------------------------------------------------
# REGIONAL ANALYTICS
# --------------------------------------------------

elif page == "🌍 Regional Analytics":

    st.header("🌍 Regional Analytics")

    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        title="Region-wise Sales"
    )

    st.plotly_chart(fig)

    state_sales = (
        df.groupby("State")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        state_sales,
        x="State",
        y="Sales",
        title="Top States by Sales"
    )

    st.plotly_chart(fig2)

# --------------------------------------------------
# CUSTOMER ANALYTICS
# --------------------------------------------------

elif page == "👥 Customer Analytics":

    st.header("👥 Customer Analytics")

    top_customers = (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.subheader("🏆 Top Customers")

    st.bar_chart(top_customers)

    st.dataframe(top_customers)

    segment_sales = (
        df.groupby("Segment")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        segment_sales,
        names="Segment",
        values="Sales",
        title="Customer Segment Distribution"
    )

    st.plotly_chart(fig)

# --------------------------------------------------
# PRODUCT ANALYTICS
# --------------------------------------------------

elif page == "📦 Product Analytics":

    st.header("📦 Product Analytics")

    top_products = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.subheader("🏆 Top Products")

    st.bar_chart(top_products)

    st.dataframe(top_products)

    profitable = (
        df.groupby("Product Name")["Profit"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.subheader("💰 Most Profitable Products")

    st.bar_chart(profitable)

# --------------------------------------------------
# FORECASTING
# --------------------------------------------------

elif page == "🔮 Forecasting":

    st.header("🔮 Sales Forecast")

    if os.path.exists("forecast_output.csv"):

        forecast = pd.read_csv(
            "forecast_output.csv"
        )

        st.dataframe(
            forecast.tail(10)
        )

        if "ds" in forecast.columns and "yhat" in forecast.columns:

            fig = px.line(
                forecast,
                x="ds",
                y="yhat",
                title="Future Sales Forecast"
            )

            st.plotly_chart(fig)

    else:

        st.error(
            "forecast_output.csv not found"
        )

# --------------------------------------------------
# AI INSIGHTS
# --------------------------------------------------

elif page == "🤖 AI Insights":

    st.header("🤖 AI Business Insights")

    best_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .idxmax()
    )

    best_category = (
        df.groupby("Category")["Profit"]
        .sum()
        .idxmax()
    )

    best_customer = (
        df.groupby("Customer Name")["Sales"]
        .sum()
        .idxmax()
    )

    st.success(f"""
📈 Business Summary

🌍 Best Region: {best_region}

📦 Most Profitable Category: {best_category}

👑 Top Customer: {best_customer}

🎯 Recommendations:

• Increase inventory in {best_region}

• Focus on {best_category}

• Retain high-value customers

• Expand marketing campaigns
""")

# --------------------------------------------------
# AI ASSISTANT
# --------------------------------------------------

elif page == "💬 AI Assistant":

    st.header("🤖 Smart Business AI Assistant")

    question = st.text_input(
        "Ask anything about your sales data"
    )

    if question:

        q = question.lower()

        total_sales = df["Sales"].sum()
        total_profit = df["Profit"].sum()

        best_region = (
            df.groupby("Region")["Sales"]
            .sum()
            .idxmax()
        )

        best_customer = (
            df.groupby("Customer Name")["Sales"]
            .sum()
            .idxmax()
        )

        best_product = (
            df.groupby("Product Name")["Sales"]
            .sum()
            .idxmax()
        )

        best_category = (
            df.groupby("Category")["Sales"]
            .sum()
            .idxmax()
        )

        if "sales" in q:

            st.success(
                f"💰 Total Sales = ₹{total_sales:,.0f}"
            )

        elif "profit" in q:

            st.success(
                f"📈 Total Profit = ₹{total_profit:,.0f}"
            )

        elif "region" in q:

            st.success(
                f"🌍 Best Region = {best_region}"
            )

        elif "customer" in q:

            st.success(
                f"👑 Top Customer = {best_customer}"
            )

        elif "product" in q:

            st.success(
                f"🏆 Best Product = {best_product}"
            )

        elif "category" in q:

            st.success(
                f"📦 Best Category = {best_category}"
            )

        elif "orders" in q:

            st.success(
                f"📦 Total Orders = {df['Order ID'].nunique()}"
            )

        elif "quantity" in q:

            st.success(
                f"🛒 Total Quantity Sold = {df['Quantity'].sum():,.0f}"
            )

        elif "state" in q:

            top_state = (
                df.groupby("State")["Sales"]
                .sum()
                .idxmax()
            )

            st.success(
                f"🏙️ Highest Sales State = {top_state}"
            )

        elif "segment" in q:

            seg = (
                df.groupby("Segment")["Sales"]
                .sum()
                .idxmax()
            )

            st.success(
                f"👥 Best Segment = {seg}"
            )

        elif "payment" in q:

            pay = (
                df.groupby("Payment Mode")["Sales"]
                .sum()
                .idxmax()
            )

            st.success(
                f"💳 Most Used Payment Mode = {pay}"
            )

        elif "return" in q:

            returns = df["Returns"].sum()

            st.success(
                f"📦 Total Returns = {returns}"
            )

        elif "summary" in q:

            st.success(f"""
📊 BUSINESS SUMMARY

💰 Total Sales: ₹{total_sales:,.0f}

📈 Total Profit: ₹{total_profit:,.0f}

🌍 Best Region: {best_region}

👑 Top Customer: {best_customer}

🏆 Top Product: {best_product}

📦 Best Category: {best_category}
""")

        else:

            st.info("""
Try asking:

• What are total sales?

• What is total profit?

• Who is the top customer?

• Which region performs best?

• What is the best product?

• What is the best category?

• Give me a summary

• Which state has highest sales?

• What is the best segment?

• What is the most used payment mode?
""")

# --------------------------------------------------
# REPORTS
# --------------------------------------------------

elif page == "📄 Reports":

    st.header("📄 Reports")

    csv = df.to_csv(index=False)

    st.download_button(
        "⬇ Download Clean Dataset",
        csv,
        "clean_sales_data.csv",
        "text/csv"
    )

    if os.path.exists(
        "forecast_output.csv"
    ):

        with open(
            "forecast_output.csv",
            "rb"
        ) as f:

            st.download_button(
                "⬇ Download Forecast",
                f,
                "forecast_output.csv"
            )