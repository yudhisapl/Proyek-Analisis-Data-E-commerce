import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#deploy seluruh dataframe untuk visualisasi

def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name")["product_id"].count().reset_index()
    sum_order_items_df.rename(columns={
        "product_id": "products",
        "product_category_name":"category"
    }, inplace=True)
    sum_order_items_df = sum_order_items_df.sort_values(by="products", ascending=False)
    return sum_order_items_df

def create_bystate_df(df):
    state_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    state_df.rename(columns={
        "customer_id_customers": "customer_count"
    }, inplace=True)
    return state_df

def create_payment_counts(df):
    payment_counts = df['payment_type'].value_counts().reset_index()
    payment_counts.columns = ['payment_type', 'count']

    return payment_counts

all_df = pd.read_csv("all_df.csv")

sum_order_items_df = create_sum_order_items_df(all_df)
bystate_df = create_bystate_df(all_df)
payment_counts = create_payment_counts(all_df)

st.title('E-commerce Public Dashboard')

st.subheader("Best-Selling and Least-Selling Product")

sum_order_items_df = all_df.groupby("product_category_name_english")["product_id"].count().reset_index()
sum_order_items_df = sum_order_items_df.rename(columns={"product_id": "products"})
sum_order_items_df = sum_order_items_df.sort_values(by="products", ascending=False)
sum_order_items_df = sum_order_items_df.head(10)
# Split the dataframe into top 5 and bottom 5
top_5_df = sum_order_items_df.head(5)
bottom_5_df = sum_order_items_df.tail(5)

# Set up the plotting area for two subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Plot the top 5 categories
sns.barplot(
    x="products",
    y="product_category_name_english",
    data=top_5_df,
    palette="Blues_r",
    ax=axes[0]
)
axes[0].set_title('Top 5 Product Categories', fontsize=14)
axes[0].set_xlabel('Number of Products', fontsize=12)
axes[0].set_ylabel('Product Category', fontsize=12)

# Plot the bottom 5 categories
sns.barplot(
    x="products",
    y="product_category_name_english",
    data=bottom_5_df,
    palette="Reds_r",
    ax=axes[1]
)
axes[1].set_title('Bottom 5 Product Categories', fontsize=14)
axes[1].set_xlabel('Number of Products', fontsize=12)
axes[1].set_ylabel('Product Category', fontsize=12)

st.pyplot(fig)

#2 Highest Revenue Product based on Category
st.subheader("Highest Revenue Product based on Category")

revenue_df = all_df.groupby("product_category_name_english")["price"].sum().reset_index()
#price -> revenue
revenue_df = revenue_df.rename(columns={"price": "revenue"})

#sorting
revenue_df = revenue_df.sort_values(by="revenue", ascending=False)
#10 tertinggi
top_revenue_categories = revenue_df.head(10)

plt.figure(figsize=(10, 6))

# Normalizing the colors based on revenue
norm = plt.Normalize(top_revenue_categories['revenue'].min(), top_revenue_categories['revenue'].max())
colors = plt.cm.Blues(norm(top_revenue_categories['revenue']))

# Membuat barplot untuk kategori dengan revenue tertinggi (vertikal)
sns.barplot(
    x="product_category_name_english",
    y="revenue",
    data=top_revenue_categories,
    palette=colors
)

# Menambahkan judul dan label sumbu
plt.title('Top 10 Product Categories by Revenue', fontsize=16)
plt.xlabel('Product Category', fontsize=12)
plt.ylabel('Revenue', fontsize=12)

# Menampilkan plot
plt.xticks(rotation=45)

st.pyplot(plt)

#3 Highest numbers of customer in City
st.subheader("Highest numbers of customer in City")

state = all_df.groupby(by="customer_state").customer_id.nunique().reset_index()
state.rename(columns={
    "customer_id": "customer_count"
}, inplace=True)
plt.figure(figsize=(10, 6))

most_common_state = state.loc[state['customer_count'].idxmax(), 'customer_state']

state = state.sort_values(by='customer_count', ascending=False)

sns.barplot(x='customer_state',
            y='customer_count',
            data=state,
            palette=["#068DA9" if state == most_common_state else "#D3D3D3" for state in bystate_df['customer_state']]
            )

plt.title("Number customers from City", fontsize=15)
plt.xlabel("City")
plt.ylabel("Number Customers")
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)

st.pyplot(plt)

st.caption('Copyright (c) Yudhistira Andika Pandu Leksono 2024')