import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score

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
    
from sklearn.ensemble import RandomForestRegressor
x=df[['Discount', 'Quantity', 'Profit']]
y=df['Sales']

x_train, x_test, y_train, y_test=train_test_split(x, y, test_size=0.2, random_state=42)
rf=RandomForestRegressor(n_estimators=200, random_state=42)
rf.fit(x_train, y_train)
y_pred=rf.predict(x_test)

#check model performance
rmse=np.sqrt(mean_squared_error(y_test, y_pred))
r2=r2_score(y_test, y_pred)
st.subheader("Model Performance (used Random Forest Regressor)")
st.write(f"**RMSE:** {rmse:.2f}")
st.write(f"**R² Score:** {r2:.2f}")

#visualize results
results = pd.DataFrame({"Actual Sales": y_test, "Predicted Sales": y_pred})
chart = px.scatter(results, x="Actual Sales", y="Predicted Sales", opacity=0.6,
                  title="Actual vs Predicted Sales using Random Forest")
chart.add_shape(type="line", x0=y_test.min(), y0=y_test.min(),
               x1=y_test.max(), y1=y_test.max(),
               line=dict(color="red", dash="dash"))
st.plotly_chart(chart, use_container_width=True)




