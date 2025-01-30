
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("retail_store_clean_data.csv")  # Replace with your dataset file
    return df

df = load_data()

# --- Streamlit App Title ---
st.title("📊 Data Analysis Dashboard")

# --- Sidebar ---
st.sidebar.header("Navigation")
analysis_type = st.sidebar.radio("Select Analysis Type", ["Univariate Analysis", "BI/Multi-variate Analysis", "Conclusion"])

# --- Filters ---
st.sidebar.subheader("Filters")
selected_category = st.sidebar.multiselect("Filter by Category", df["Category"].unique(), default=df["Category"].unique())
selected_payment = st.sidebar.multiselect("Filter by Payment Method", df["Payment Method"].unique(), default=df["Payment Method"].unique())
selected_months = st.sidebar.slider("Select Month Range", min_value=1, max_value=12, value=(1, 12))

# Apply Filters
df_filtered = df[(df["Category"].isin(selected_category)) & 
                 (df["Payment Method"].isin(selected_payment)) & 
                 (df["Month"].between(selected_months[0], selected_months[1]))]

# --- Univariate Analysis ---
if analysis_type == "Univariate Analysis":
    st.header("📌 Univariate Analysis")

    st.subheader("Price Per Unit Distribution")
    price_fig = px.histogram(df_filtered, x="Price Per Unit", nbins=30, title="Price Per Unit Distribution", color_discrete_sequence=["purple"])
    st.plotly_chart(price_fig)

    st.subheader("Most Purchased Product Categories")
    category_freq_fig = px.bar(df_filtered["Category"].value_counts().reset_index(), x="Category", y="count", title="Product Category Distribution", height=600)
    st.plotly_chart(category_freq_fig)

    st.subheader("Distribution of Total Spent")
    total_spent_fig = px.histogram(df_filtered, x="Total Spent", nbins=20, title="Distribution of Total Spent", color_discrete_sequence=["green"])
    st.plotly_chart(total_spent_fig)

    st.subheader("Payment Method Distribution")
    pay_method_fig = px.pie(df_filtered, names="Payment Method", title="Distribution of Payment Methods")
    st.plotly_chart(pay_method_fig)

    st.subheader("Transaction Frequency by Month")
    month_fig = px.bar(df_filtered["Month"].value_counts().reset_index(), x="Month", y="count", title="Transaction Frequency by Month")
    st.plotly_chart(month_fig)

# --- BI/Multi-variate Analysis ---
elif analysis_type == "BI/Multi-variate Analysis":
    st.header("📌 BI/Multi-variate Analysis")

    st.subheader("Correlation Heatmap")
    pqt_corr = df_filtered[["Price Per Unit", "Quantity", "Total Spent"]].corr()
    heatmap_fig = px.imshow(pqt_corr, text_auto=True, color_continuous_scale="Sunsetdark")
    st.plotly_chart(heatmap_fig)

    st.subheader("Spending Trends by Month")
    month_trend_fig = px.line(df_filtered.groupby("Month")["Total Spent"].sum().reset_index(), x="Month", y="Total Spent", title="Total Spending by Month")
    st.plotly_chart(month_trend_fig)

    st.subheader("Customer CLV vs Transaction Count")
    clv_fig = px.scatter(df_filtered, x="Transaction Count", y="CLV", title="Customer CLV vs Transaction Count", trendline="ols")
    st.plotly_chart(clv_fig)

    st.subheader("Top 15 Best-Selling Products")
    df_top_products = (df[~df["Item"].str.startswith("Item_0")]
                       .groupby("Item")["Quantity"].sum()
                       .reset_index()
                       .sort_values(by="Quantity", ascending=False)
                       .head(15))
    top_selling_fig = px.bar(df_top_products, x="Quantity", y="Item", title="Top 15 Best-Selling Products", orientation="h", height=500, color="Quantity")
    st.plotly_chart(top_selling_fig)

    st.subheader("Price Per Unit vs Quantity Density")
    density_fig = px.density_heatmap(df_filtered, x="Price Per Unit", y="Quantity", title="Price Per Unit vs Quantity Density", color_continuous_scale="Blues")
    st.plotly_chart(density_fig)

    st.subheader("Total Spending by Location")
    location_fig = px.bar(df_filtered.groupby("Location", as_index=False)["Total Spent"].sum(), x="Total Spent", y="Location", title="Total Spent by Shopping Location", color="Location", orientation="h")
    st.plotly_chart(location_fig)

    st.subheader("Spending by Category & Payment Method")
    df_grouped = df_filtered.groupby(["Category", "Payment Method"])["Total Spent"].mean().reset_index()
    category_payment_fig = px.bar(df_grouped, x="Category", y="Total Spent", color="Payment Method", barmode="group", text_auto=True, title="Average Spending by Category and Payment Method")
    st.plotly_chart(category_payment_fig)

# --- Conclusion Section ---
elif analysis_type == "Conclusion":
    st.header("📌 Conclusion & Insights")

    conclusion_text = """
     1. Based the distribution of Total spent and Price per unit more transactions occur at lower price points, indicating a price-sensitive customer base.
     **Discounts and promotions can encourage moderate spenders to buy more**
     
     2. Certain categories, like Furniture, Food, and Electronic house-hold essentials have more orders.
     
     3. Cash payments are slightly more common, but overall there's a fair distribution.
     
     4. Peak sales occur in specific months, (Jan and July are the highest likely influenced by holidays).
     **Plan marketing campaigns and discounts around high-sales months**
     
     5. Top-selling products:
     **Ensure stock availability for best-selling products to prevent shortages (i.e. Milk Products are among the most common to apply this for)**
     
     6. Customers purchase products with the price range 15-30 with higher quantities.
     **For high-priced items, consider offering installment plans or financing.**
     **For low-priced, high-volume items, implement bulk discounts to encourage larger purchases.**
     
     7. Online transactions generally have higher total spend.
     **Encourage in-store customers to make higher purchases through in-store promotions.**
     
     8. Beverages & Butchers:
     
         Credit Card users tend to spend slightly more than other categories.
     
         Electronics (Computers & Accessories, Household Essentials):
     
         Spending is slightly higher for Digital Wallet users.
     
     9. Price Per Unit vs Total Spent:
     
         Moderately positive correlation:
     
         Higher price per unit generally leads to higher total spending.
     
         Quantity vs Total Spent:
     
         Strong positive correlation: Higher quantity strongly impacts total spending.
     
         Price Per Unit vs Quantity:
     
         No significant correlation: Price per unit does not strongly influence the number of items purchased.
     
     10. Customer CLV vs Transaction Count:
     
         Trend:
     
         Positive Linear Relationship: Customers with more transactions tend to have higher CLV. (Normal)
     
         Anomaly:
     
         Some customers have high CLV despite fewer transactions, suggesting high-value purchases.
     """


    st.markdown(conclusion_text)

# --- Footer ---
st.markdown("**Developed by: Amr Shawky**")
