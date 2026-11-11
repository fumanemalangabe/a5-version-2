import streamlit as st, pandas as pd
st.set_page_config(page_title="Sales Dashboard", layout="wide", initial_sidebar_state="expanded")
st.sidebar.title("Regional Sales Dashboard")
@st.cache_data
def load_data():
  return pd.read_csv("sales.csv", parse_dates=["date"])
df = load_data()
all_regions = sorted(df["region"].unique())
regions = st.sidebar.multiselect("Regions", all_regions, default=all_regions)
start, end = st.sidebar.date_input("Dates", (df["date"].min(), df["date"].max()))
mask = df["region"].isin(regions) & df["date"].between(pd.Timestamp(start), pd.Timestamp(end))
data = df[mask]
if data.empty: st.warning("No sales for this selection."); st.stop()
c1, c2, c3 = st.columns(3)
c1.metric("Revenue", f"R{data['revenue'].sum():,.0f}")
c2.metric("Orders", data["order_id"].nunique())
c3.metric("Average order", f"R{data['revenue'].sum() / data['order_id'].nunique():,.2f}")
monthly = data.set_index("date")["revenue"].resample("MS").sum()
st.line_chart(monthly)
st.bar_chart(data.groupby("region")["revenue"].sum())
