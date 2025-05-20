#Importing Libraries
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Superstore!", page_icon=":bar_chart:", layout="wide")

st.title(":bar_chart: Sample Superstore Data")
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

#File Uploading Phase 
file_upload = st.file_uploader(":file_folder: Upload a file", type=(["csv", "xlsx", "xls", "txt"]))
if file_upload is not None:
    filename = file_upload.name
    st.write(filename)
    df = pd.read_excel(filename)
else:
    os.chdir(r"E:\Python Interactive dashboard\Files")
    df = pd.read_excel("Superstore.xls")

#Main development Phase
col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

#now putting min and max date
startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df  = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

st.sidebar.header("Choose your filter: ")
#For Region
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

#For State
state = st.sidebar.multiselect("Pick your State", df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

#For City
city = st.sidebar.multiselect("Pick your City", df3["City"].unique())

# Filter data based on Region, State, City
if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df = df3[df["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df = df3[df["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df = df3[df3["City"].isnin(city)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3[df3["State"].isin(state) & df3["City"].isin(city)]]

#Now let's create a column chart for category and region
category_df = filtered_df.groupby(by = ["Category"], as_index= False)["Sales"].sum()

with col1:
    st.subheader("Category Wise Sales")
    fig = px.bar(category_df, x = "Category", y = "Sales", text = ['${:,.2f}'.format(x) for x in category_df["Sales"]], template="seaborn")
    st.plotly_chart(fig,use_container_width=True, height=200)

with col2:
    st.subheader("Region Wise Sales")
    fig = px.pie(filtered_df, values="Sales", names = "Region", hole= 0.5)
    fig.update_traces(text = filtered_df["Region"], textposition = "outside")
    st.plotly_chart(fig, use_container_width=True)

# Now If we want to see and download the data based on these charts
# First Category wise sales
cl1, cl2 = st.columns(2)
with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index = False).encode("utf-8")
        st.download_button("Download the Data", data = csv, file_name = "Category.csv", mime = "text/csv", help = "Click here to download data as a CSV file")

# Second Region wise sales
with cl2:
    with st.expander("Region_ViewData"):
        # region = filtered_df.groupby(by = ["Region"], as_index= False)["Sales"].sum()
        region = filtered_df.groupby(by = "Region", as_index= False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode("utf-8")
        st.download_button("Download the Data", data = csv, file_name = "Region.csv", mime = "text/csv", help = "Click here to download data as a CSV file")

#Now visualizing the data using time series analysis based on month year.
filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
st.subheader("Time Series Analysis")

linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2 = px.line(linechart, x = "month_year", y = "Sales", labels= {"Sales": "Amount"}, height = 550, width=1050, template="gridon")
st.plotly_chart(fig2, use_container_width=True)

#Giving a download button
with st.expander("View Data of TimeSeries"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button("Download Data", data = csv, file_name="TimeSeries.csv", mime="text/csv")

#Create a tree map based on Region, Category and Sub-Category
st.subheader("A Hierarchical view of Sales using Tree Map")
fig3 = px.treemap(filtered_df, path=["Region", "Category", "Sub-Category"], values= "Sales", hover_data= ["Sales"], color= "Sub-Category")
fig3.update_layout(width = 850, height = 700)
st.plotly_chart(fig3, use_container_width=True)

#Now Creating Segment wise and Category wise sales..
chart1, chart2 = st.columns((2)) # Creating two columns
with chart1:
    st.subheader("Segment Wise Sales")
    fig = px.pie(filtered_df, values="Sales", names = "Segment", template= "plotly_dark")
    fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
    st.plotly_chart(fig, use_container_width=True)

with chart2:
    st.subheader("Category Wise Sales")
    fig = px.pie(filtered_df, values="Sales", names = "Category", template= "gridon")
    fig.update_traces(text = filtered_df["Category"], textposition = "inside")
    st.plotly_chart(fig, use_container_width=True)

#How we can show some specific data in table format using streamlit
import plotly.figure_factory as ff #using figure_factory we will create a table
st.subheader(":point_right: Month Wise Sub-Category sales summary")
with st.expander("Summary Table"):
    df_sample = df [0:5][["Region", "State", "City", "Category", "Sales", "Profit", "Quantity"]]
    fig = ff.create_table(df_sample, colorscale = "Cividis")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Month Wise Sub-Category Table")
    filtered_df["month"] = filtered_df["Order Date"].dt.month_name()
    sub_category_year = pd.pivot_table(data = filtered_df, values = "Sales", index = ["Sub-Category"], columns = "month")
    st.write(sub_category_year.style.background_gradient(cmap="Blues"))

data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity")
data1.update_layout(title="Relationship between Sales and Profit using Scatter Plot", title_font= dict(size=20), 
                       xaxis = dict(title ="Sales", title_font = dict(size=19)), yaxis = dict(title="Profit", title_font=dict(size=19)))
st.plotly_chart(data1, use_container_width=True)

#Now if we want to download the entire dataset of specific portions
with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

#And if we wanna download the entire dataset
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download Data", data = csv, file_name= "Data.csv", mime="text/csv")

# NEW GRAPHS START FROM HERE
# Monthly Sales Heatmap
st.subheader("Monthly Sales Heatmap")
filtered_df['Month'] = filtered_df['Order Date'].dt.month_name()
filtered_df['Year'] = filtered_df['Order Date'].dt.year

heatmap_data = filtered_df.groupby(['Year', 'Month'])['Sales'].sum().unstack()
months_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December']
heatmap_data = heatmap_data[months_order]

fig_heatmap = px.imshow(heatmap_data, 
                       labels=dict(x="Month", y="Year", color="Sales"),
                       x=heatmap_data.columns,
                       y=heatmap_data.index,
                       color_continuous_scale='Viridis',
                       aspect="auto")
fig_heatmap.update_layout(height=500)
st.plotly_chart(fig_heatmap, use_container_width=True)

