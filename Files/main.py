#Importing Libraries
import streamlit as st
import plotly.express as ex
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
# if not city:
#     df4 = df3.copy()
# else:
#     df4 = df3[df3["City"].isin(city)]

# Filter data based on Region, State, City
if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not city:
    fileterd_df = df[df["State"].isin(state)]
elif state and city:
    fileterd_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    fileterd_df = df3[df["State"].isin(region) & df3["City"].isin(city)]
elif region and state:
    fileterd_df = df3[df["State"].isin(region) & df3["City"].isin(state)]
elif city:
    fileterd_df = df3[df3["City"].isnin(city)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3[df3["State"].isin(state) & df3["City"].isin(city)]]






