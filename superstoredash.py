import streamlit as st
import pandas as pd
import plotly.express as px

df=pd.read_csv('superstore.csv')
st.set_page_config(page_title="Superstore Dashboard", page_icon="🛒", layout="wide")
st.title("Superstore products Dashboard using Streamlit!🛒")

st.sidebar.title("Filter your view")

region=df['Region'].unique()
selected_region = st.sidebar.multiselect("Select region(s): ", options=region)
if not selected_region:
    st.sidebar.info("Select at least one region.")

shipmode=df['Ship Mode'].unique()
selected_mode = st.sidebar.multiselect("Select shipping method(s): ", options=shipmode)
if not selected_mode:
    st.sidebar.info("Select at least one shipping method.")

categories = df['Category'].unique()
selected_categories = st.sidebar.multiselect("Select category(s): ", options=categories)
if not selected_categories:
    st.sidebar.info("Select at least one category.")

if selected_categories and selected_mode and selected_region:
    filtered_df = df[df['Region'].isin(selected_region) & df['Ship Mode'].isin(selected_mode) & df['Category'].isin(selected_categories)]
    st.success("Successfully filtered data.")
    st.markdown("Choose your desired chart type:")
#Area chart depicting sales in states
    with st.expander("Area chart: Sales by State"):
        st.subheader("Area chart displaying sales w.r.t sub categories in different states")
        data=filtered_df.groupby('State')['Sales'].sum().reset_index()
        fig4= px.area(data, x='State',y='Sales')
        st.plotly_chart(fig4, use_container_width=True)#use_container_width makes the chart responsive.

    #Sunburst chart depicting Discount, Profit
    with st.expander("Sunburst chart: Discount and profit by sub category"):
        st.header("Sunburst chart displaying Discount and Profit for each sub category")
        fig3 = px.sunburst(filtered_df, path=['Category', 'Sub-Category'], values='Discount', color='Profit')
        st.plotly_chart(fig3,use_container_width=True)
   
    #Pie chart depicting quantity
    with st.expander("Pie chart: Quantity by sub category"):
        st.subheader("Pie chart displaying total quantity w.r.t sub categories")
        data = filtered_df.groupby('Sub-Category')['Quantity'].sum().reset_index()
        fig2 = px.pie(data, names='Sub-Category', values='Quantity')
        st.plotly_chart(fig2,use_container_width=True)

    #Bar chart depicting Profit
    with st.expander("Bar chart: Profit by sub category"):
        st.header("Bar chart displaying profit earned w.r.t sub categories")
        data = filtered_df.groupby('Sub-Category')['Profit'].sum().reset_index()
        fig1 = px.bar(data, x='Sub-Category', y='Profit', labels='Profit')
        st.plotly_chart(fig1,use_container_width=True)

else:
    st.warning("No filters selected yet. Use them to display the charts!")


