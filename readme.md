
# 📊 SuperstoreViz an Interactive Dashboard

An interactive web application built using **Streamlit** and **Plotly** to visualize and analyze sales data from a Superstore dataset. This dashboard allows users to upload their own Excel or CSV files, filter data in real-time, and explore dynamic insights through a variety of visualizations.

## 🚀 Features

- 📁 **File Upload:** Supports `.csv`, `.xlsx`, `.xls`, `.txt` formats for custom data input.
- 📅 **Date Range Selector:** Interactive start and end date filters based on available order dates.
- 🌐 **Hierarchical Filtering:** Region, State, and City-based filtering from the sidebar.
- 📊 **Visualizations:**
  - Category-wise Sales (Bar Chart)
  - Region-wise Sales (Donut Chart)
  - Time Series Analysis (Line Chart)
  - Treemap (Region > Category > Sub-category)
  - Segment & Category Sales (Pie Charts)
  - Sales vs Profit (Scatter Plot)
  - Ship Mode Sales Distribution (Box Plot)
  - Category-wise Correlation of Sales vs Profit (Bar Chart)
  - Monthly Sales Heatmap (Year x Month)
- 💾 **Download Options:** Export filtered data and summary tables as CSV files.
- 📋 **Summary Table:** Month-wise sub-category sales in pivot format.

## 🛠 Tech Stack

- **Frontend & App Interface:** Streamlit
- **Data Handling:** Pandas
- **Visualizations:** Plotly Express, Plotly Figure Factory
- **File Support:** Excel, CSV

## 📂 Folder Structure

```
📁 Project Root
│
├── main.py           # Main Streamlit app script
└── Superstore.xls    # (Optional) Default dataset used when no file is uploaded
```

## 💡 How to Run the Project

1. Clone the repository or download the project folder.
2. Make sure you have Python 3 installed.
3. Install dependencies:
   ```bash
   pip install streamlit plotly pandas openpyxl
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```

## 📌 Notes

- The app defaults to `Superstore.xls` if no file is uploaded.
- Filter and analyze data interactively from the sidebar and main view.
- Fully responsive layout using Streamlit’s column structure.

## 🔗 Author & Acknowledgements

Created with ❤️ by Vanshaj P Mohan with a passion for Data Science and Interactive Dashboards.
