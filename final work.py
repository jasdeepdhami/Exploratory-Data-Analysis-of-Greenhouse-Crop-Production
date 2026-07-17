import streamlit as st
import pandas as pd
import plotly.express as plt
import datetime as dt
import numpy as np
st.set_page_config(
    page_title="Exploratory Analysis of Greenhouse Crop Production",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)
#Main Title
st.title("Demo Title")
st.title("🏡 Exploratory Analysis of Greenhouse Crop Production")
st.markdown("---")
#==============================================================================================================================================
#Executive Summary
#==============================================================================================================================================
st.header("📄 Executive Summary")
st.markdown("""
This comprehensive data science project analyzes environmental, agronomic, and yield data collected across
thousands of greenhouse growing cycles. The analysis aims to uncover valuable insights about how climate
conditions, cultivation inputs, and crop genetics interact to determine final crop yield.

**🔑 Key Objectives:**
- Understand yield performance patterns across different crop types and varieties
- Analyze how climate variables (temperature, humidity, CO2, light) relate to yield outcomes
- Examine the effect of cultivation inputs such as irrigation, fertilizer, and pest severity
- Investigate seasonal and temporal trends in planting and yield
- Identify hierarchical relationships between crop, variety, and greenhouse performance
- Identify opportunities to optimize greenhouse operations for higher productivity

**📦 Expected Deliverables:**
- Interactive visualizations showcasing the greenhouse growing landscape
- Statistical analysis of key climate and yield indicators
- Actionable insights for greenhouse operators and agronomists
- A cleaned, analysis-ready dataset with documented data quality treatment
""")

st.markdown("---")

# ============================================================
# Project Description
# ============================================================
st.header("💡 Project Description")

st.subheader("⚠️ Problem Statement")
st.markdown("""
Controlled-environment agriculture is highly dependent on precise climate management and nutrient delivery,
yet growers do not always have a clear, data-driven view of which factors most influence yield. This project
leverages a comprehensive greenhouse crop yield dataset to provide insights that can help:

- **Greenhouse Operators**: Optimize climate control, irrigation, and fertilization strategies
- **Agronomists & Researchers**: Understand which growing conditions correlate most strongly with yield
- **Farm Managers**: Plan planting schedules and crop/variety selection based on historical performance
- **Investors**: Identify high-performing crop and variety combinations worth scaling
""")

st.subheader("🗂️ Dataset Overview")
st.markdown("""
The greenhouse crop yield dataset contains comprehensive information about individual growing cycles including:

**Core Crop Information:**
- Greenhouse identifiers
- Crop type and variety
- Planting and harvest dates, days to maturity

**Climate Conditions:**
- Average, minimum, and maximum temperature (°C)
- Humidity percentage
- CO2 concentration (ppm)
- Light intensity (lux) and photoperiod (hours)

**Cultivation Inputs:**
- Irrigation amount (mm)
- Fertilizer application: Nitrogen, Phosphorus, and Potassium (kg/ha)
- Pest severity index
- Soil pH

**Outcome Metric:**
- Yield in kilograms per square meter (yield_kg_per_m2)
""")

st.markdown("---")

@st.cache_data
def load():
    try:
        DATA_PATH="dataset.csv"
        df=pd.read_csv(DATA_PATH)
        return df,DATA_PATH
    except:
        st.error("Error in loading dataset")
df,path=load()
st.header("📈 Data Set Basic Information")
memory=df.memory_usage(deep=True).sum()/(1024**2)
st.divider()
column1,column2,column3=st.columns(3)
with column1:
    st.metric("Total Records",f"{df.shape[0]:,}")
with column2:
    st.metric("Total Columns",f"{df.shape[1]:,}")
with column3:
    st.metric("Memory used",f"{memory:.2f}MB")
tab1,tab2,tab3,tab4,tab5,tab6=st.tabs(
    [
    "📋 Column Info",
    "❌ Missing Values",
    "👀 Sample Data",
    "📊 Statistics",
    "🔤 Categorical Data",
    "✅ Data Quality"
    ])
with tab1:
    st.subheader("📋 Column Information")
    df_info=pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Non-Null Values":df.count().values,
        "Null Values":df.isnull().sum().values,
        "Unique Values":df.nunique().values
    })
    st.dataframe(df_info,use_container_width=True)

    st.subheader("Data Types Summary")
    st.dataframe(
        df.dtypes.value_counts().rename_axis("Data Type").reset_index(name="Count"),
        use_container_width=True
    )
    st.subheader("Detailed Column Descriptions")
    st.markdown("""
        **Column Descriptions:**\n
        • **greenhouse_id**: Identifier for the greenhouse where the crop was grown\n
        • **crop_type**: Type of crop (Tomato, Cucumber, Pepper, Lettuce)\n
        • **variety**: Specific variety of the crop\n
        • **planting_date**: Date the crop was planted\n
        • **harvest_date**: Date the crop was harvested\n
        • **days_to_maturity**: Number of days from planting to harvest\n
        • **avg_temperature_C / min_temperature_C / max_temperature_C**: Temperature readings during growth (°C)\n
        • **humidity_percent**: Average relative humidity (%)\n
        • **co2_ppm**: CO2 concentration (parts per million)\n
        • **light_intensity_lux**: Average light intensity (lux)\n
        • **photoperiod_hours**: Hours of light exposure per day\n
        • **irrigation_mm**: Total irrigation applied (mm)\n
        • **fertilizer_N_kg_ha / fertilizer_P_kg_ha / fertilizer_K_kg_ha**: Fertilizer application rates (kg/ha)\n
        • **pest_severity**: Index representing severity of pest presence\n
        • **soil_pH**: Soil pH level\n
        • **yield_kg_per_m2**: Final crop yield (kg per square meter)\n
        """)
with tab2:
    st.subheader("❌ Missing Values Analysis")
    check=df.isnull().sum().sort_values(ascending=False)
    if check.empty:
        st.success("No null values encountered in Dataset")
    else:
        missing = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values,
        "Missing %": ((df.isnull().sum()/len(df))*100).round(2)
        })
        st.dataframe(missing, use_container_width=True)

        st.bar_chart(missing.set_index("Column")["Missing %"])
with tab3:
    st.subheader("👀 Sample Data")

    option = st.radio(
        "Select Sample",
        ["First 10 Rows","Last 10 Rows","Random 10 Rows"],
        horizontal=True
    )

    if option=="First 10 Rows":
        st.dataframe(df.head(10),use_container_width=True)

    elif option=="Last 10 Rows":
        st.dataframe(df.tail(10),use_container_width=True)

    else:
        st.dataframe(df.sample(10),use_container_width=True)
with tab4:

    st.subheader("📊 Statistical Summary")

    st.write("### Numerical Statistics")

    st.dataframe(
        df.select_dtypes(include=np.number).describe(),
        use_container_width=True
    )

    st.write("### Categorical Statistics")

    categorical=df.select_dtypes(include=["object"])

    if not categorical.empty:
        st.dataframe(
            categorical.describe(),
            use_container_width=True
        )

with tab5:

    st.subheader("🌸 Species Analysis")

    if "variety" in df.columns:

        variety=df[["crop_type","variety"]].value_counts().reset_index()

        variety.columns=["Crop Type","Variety","Count"]

        st.dataframe(variety,use_container_width=True)

        col1,col2=st.columns(2)

        with col1:

            fig=plt.bar(
                variety,
                x="Crop Type",
                y="Count",
                color="Variety",
                title="Variety Distribution"
            )

            st.plotly_chart(fig,use_container_width=True)

        with col2:

            fig=plt.pie(
                variety,
                names="Variety",
                values="Count",
                hole=0.4,
                title="Variety Percentage"
            )

            st.plotly_chart(fig,use_container_width=True)

        st.subheader("Variety-wise Statistics")
        new_df=df.groupby("variety").mean(numeric_only=True)
        new_df.drop(columns=["greenhouse_id"],inplace=True)
        st.dataframe(
            new_df,
            use_container_width=True
        )
with tab6:

    st.subheader("✅ Data Quality Report")

    duplicate=df.duplicated().sum()
    missing=df.isnull().sum().sum()

    completeness=((df.size-missing)/df.size)*100

    col1,col2,col3=st.columns(3)

    col1.metric("Duplicate Rows",duplicate)
    col2.metric("Missing Values",missing)
    col3.metric("Data Completeness",f"{completeness:.2f}%")

    st.markdown("---")

    quality=pd.DataFrame({
        "Column":df.columns,
        "Missing Values":df.isnull().sum().values,
        "Completeness %":((df.notnull().sum()/len(df))*100).round(2)
    })

    st.dataframe(quality,use_container_width=True)

    st.bar_chart(quality.set_index("Column")["Completeness %"])
st.divider()
st.header("Data Cleaning & Preprocessing")
st.divider()
@st.cache_data
def load_cleandataset():
    try:
        cleaned_df=df.copy()
        cleaned_df.head(1)
        cleaned_df.info()
        cleaned_df["crop_type"].unique()
        cleaned_df["variety"].unique()
        list(cleaned_df["planting_date"].unique())
        cleaned_df.isnull().sum()
        cleaned_df.describe()
        cleaned_df.fillna({"avg_temperature_C":cleaned_df["avg_temperature_C"].mean()},inplace=True)
        cleaned_df.fillna({"min_temperature_C":cleaned_df["min_temperature_C"].mean()},inplace=True)
        cleaned_df.fillna({"max_temperature_C":cleaned_df["max_temperature_C"].median()},inplace=True)
        cleaned_df.fillna({"humidity_percent":cleaned_df["humidity_percent"].mean()},inplace=True)
        cleaned_df.fillna({"co2_ppm":cleaned_df["co2_ppm"].mean()},inplace=True)
        cleaned_df.fillna({"light_intensity_lux":cleaned_df["light_intensity_lux"].mean()},inplace=True)
        cleaned_df.fillna({"fertilizer_N_kg_ha":cleaned_df["fertilizer_N_kg_ha"].median()},inplace=True)
        cleaned_df.fillna({"fertilizer_P_kg_ha":cleaned_df["fertilizer_P_kg_ha"].mean()},inplace=True)
        cleaned_df.fillna({"fertilizer_K_kg_ha":cleaned_df["fertilizer_K_kg_ha"].median()},inplace=True)
        cleaned_df.fillna({"pest_severity":cleaned_df["pest_severity"].mean()},inplace=True)
        cleaned_df.fillna({"soil_pH":cleaned_df["soil_pH"].median()},inplace=True)
        return cleaned_df
    except:
        st.error("Error in cleaning Dataset")
clean_df=load_cleandataset()
clean_df["harvest_date"]=pd.to_datetime(clean_df["harvest_date"])
clean_df=clean_df.drop_duplicates()
clean_tab1, clean_tab2 = st.tabs([
        "🔧 Missing Values Treatment",
        "🔍 Outlier Detection & Treatment"
    ])
with clean_tab1:
    st.subheader("Missing Values Treatment")

    st.write("**Data Cleaning Applied:**")
    st.markdown("""
        The following cleaning operations have been applied:\n
        • **Date Parsing**: `planting_date` and `harvest_date` converted from `DD-MM-YY` text to proper dates\n
        • **Climate Columns**: Humidity,min temperature and avg temperature, CO2, and light intensity values filled with the **mean within the same column** and missing temperature with max temperature values are filled with the **median within the same column**.\n
        • **Fertilizer Columns**: Missing Nitrogen and Potassium application values filled with
          crop-type medians and  Phosphorus with mean value\n
        • **Pest Severity & Soil pH**: Missing values filled with crop-type mean\n
        • **Remaining Numeric Columns**: Any values still missing after group-wise imputation filled with the
          overall column mean
        """)
    st.subheader("Before vs After Cleaning Comparison")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Original Dataset:**")
        original_nulls = df.isnull().sum().sum()
        st.metric("Total Missing Values", f"{original_nulls:,}")

    with col2:
        st.write("**Cleaned Dataset:**")
        cleaned_nulls = clean_df.isnull().sum().sum()
        st.metric("Total Missing Values", f"{cleaned_nulls:,}")
        reduction_pct = ((original_nulls - cleaned_nulls) / original_nulls * 100) if original_nulls > 0 else 0
        st.metric("Reduction", f"{reduction_pct:.1f}%")

    st.subheader("Data Cleaning Results")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Original Records", f"{df.shape[0]:,}")
    with col2:
        st.metric("Cleaned Records", f"{clean_df.shape[0]:,}")
    with col3:
        rows_removed = df.shape[0] - clean_df.shape[0]
        st.metric("Rows Removed", rows_removed)
with clean_tab2:
    st.subheader("Outlier Detection & Treatment")

    @st.cache_data
    def detect_and_treat_outliers(df_input):
        """Detect and treat outliers using the IQR method"""
        df_outliers_treated = df_input.copy()
        outlier_summary = {}
        numerical_cols = df_outliers_treated.select_dtypes(include="number").columns.tolist()
        if "greenhouse_id" in numerical_cols:
            numerical_cols.remove("greenhouse_id")
        # numerical_cols = ['yield_kg_per_m2', 'avg_temperature_C', 'irrigation_mm']
        # numerical_cols = [col for col in numerical_cols if col in df_outliers_treated.columns]

        for col in numerical_cols:
            col_data = df_outliers_treated[col].dropna()

            if len(col_data) > 0:
                Q1 = col_data.quantile(0.25)
                Q3 = col_data.quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers_mask = (col_data < lower_bound) | (col_data > upper_bound)
                outliers_count = outliers_mask.sum()
                outliers_percentage = (outliers_count / len(col_data)) * 100

                outlier_summary[col] = {
                        'count': outliers_count,
                        'percentage': outliers_percentage,
                        'lower_bound': lower_bound,
                        'upper_bound': upper_bound,
                        'Q1': Q1,
                        'Q3': Q3,
                        'IQR': IQR
                }

                # Detect outliers in all numerical columns.
                # Cap only irrigation_mm; keep other columns unchanged for analysis.
                if col == 'irrigation_mm' and outliers_count > 0:
                    df_outliers_treated[col] = df_outliers_treated[col].clip(
                            lower=lower_bound, upper=upper_bound
                    )
                    outlier_summary[col]['treatment'] = 'Capped to IQR bounds'
                else:
                    outlier_summary[col]['treatment'] = 'No treatment applied (kept for analysis)'

        return df_outliers_treated, outlier_summary

    df_with_outliers_treated, outlier_info = detect_and_treat_outliers(clean_df)

    st.write("**Outlier Detection Results:**")

    if outlier_info:
        outlier_summary_df = pd.DataFrame({
                'Column': list(outlier_info.keys()),
                'Outliers Count': [info['count'] for info in outlier_info.values()],
                'Outliers %': [f"{info['percentage']:.2f}%" for info in outlier_info.values()],
                'Lower Bound': [f"{info['lower_bound']:.2f}" for info in outlier_info.values()],
                'Upper Bound': [f"{info['upper_bound']:.2f}" for info in outlier_info.values()],
                'Treatment Applied': [info['treatment'] for info in outlier_info.values()]
        })
        st.dataframe(outlier_summary_df,use_container_width=True)

        st.subheader("Outlier Visualizations")

        for col in outlier_info.keys():
            st.write(f"**{col.replace('_', ' ').title()}:**")

            col_data = df_with_outliers_treated[col].dropna()
            info = outlier_info[col]

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Box Plot Statistics:**")
                box_stats = pd.DataFrame({
                        'Statistic': ['Min', 'Q1', 'Median', 'Q3', 'Max'],
                        'Value': [
                            col_data.min(),
                            info['Q1'],
                            col_data.median(),
                            info['Q3'],
                            col_data.max()
                        ]
                })
                st.dataframe(box_stats,use_container_width=True)

                st.write("**Outlier Bounds:**")
                st.write(f"Lower: {info['lower_bound']:.2f}")
                st.write(f"Upper: {info['upper_bound']:.2f}")

            with col2:
                st.write("**Distribution:**")
                bins = pd.cut(col_data, bins=20)
                bin_counts = bins.value_counts().sort_index()
                bin_labels = [f"{interval.left:.2f}-{interval.right:.2f}" for interval in bin_counts.index]

                chart_data = pd.DataFrame({
                        'Bin Range': bin_labels,
                        'Count': bin_counts.values
                }).set_index('Bin Range')

                st.bar_chart(chart_data)

                st.write("**Distribution Stats:**")
                dist_stats = pd.DataFrame({
                        'Metric': ['Mean', 'Std Dev', 'Skewness'],
                        'Value': [
                            f"{col_data.mean():.2f}",
                            f"{col_data.std():.2f}",
                            f"{col_data.skew():.2f}"
                        ]
                })
                st.dataframe(dist_stats,use_container_width=True)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Outliers", int(info['count']))
            with col2:
                st.metric("Outlier %", f"{info['percentage']:.2f}%")
            with col3:
                st.metric("IQR", f"{info['IQR']:.2f}")
            with col4:
                st.metric("Median", f"{col_data.median():.2f}")

            st.markdown("---")
    else:
        st.info("No numerical columns available for outlier detection")

st.subheader("Final Processed Dataset Summary")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Final Records", f"{clean_df.shape[0]:,}")
with col2:
    st.metric("Final Columns", clean_df.shape[1])
with col3:
    remaining_nulls = clean_df.isnull().sum().sum()
    st.metric("Remaining Nulls", int(remaining_nulls))

st.subheader("Column Summary")
col_summary = pd.DataFrame({
        'Column': clean_df.columns,
        'Data Type': clean_df.dtypes.astype(str),
        'Non-Null Count': clean_df.count(),
        'Null Count': clean_df.isnull().sum(),
        'Unique Values': clean_df.nunique()
})
st.dataframe(col_summary,use_container_width=True)
st.divider()
# ============================================================
# Data Visualization & Insights
# ============================================================
if "selected_crop" not in st.session_state:
    st.session_state.selected_crop=sorted(clean_df["crop_type"].unique())
if "selected_variety" not in st.session_state:
    st.session_state.selected_variety=sorted(clean_df["variety"].unique())
if "selected_yield" not in st.session_state:
    st.session_state.selected_yield=(float(clean_df["yield_kg_per_m2"].min()),float(clean_df["yield_kg_per_m2"].max()))
if "selected_maturity" not in st.session_state:
    st.session_state.selected_maturity=(int(clean_df["days_to_maturity"].min()),int(clean_df["days_to_maturity"].max()))
st.sidebar.header("Data Filters")
st.sidebar.markdown("Use these filters to explore specific segments of the data:")
st.sidebar.markdown("Tip: Set your desired filters and click 'Apply Filters' to update visualizations.")
st.sidebar.markdown("---")
with st.sidebar.form("Filter's Form"):
    st.write("🌽 Crop Filter")
    crop=st.multiselect(
        "Select the type of crop",
        options=sorted(clean_df["crop_type"].unique()),
        default=st.session_state.selected_crop
        )
    st.divider()
    st.write("🌱 Variety Filter ")
    variety=st.multiselect(
        "Select the type of crop",
        options=sorted(clean_df["variety"].unique()),
        default=st.session_state.selected_variety
        )
    st.divider()
    st.write("🌾 Yield Filter")
    Yield=st.slider(
        "Select the yield range ",
        clean_df["yield_kg_per_m2"].min(),
        clean_df["yield_kg_per_m2"].max(),
        st.session_state.selected_yield
    )
    st.divider()
    st.write("⏳ Days to Maturity Filter")
    maturity=st.slider(
        "Select the Days to Maturity Range",
        clean_df["days_to_maturity"].min(),
        clean_df["days_to_maturity"].max(),
        st.session_state.selected_maturity
    )
    st.divider()
    col1,col2=st.columns(2)
    with col1:
        apply=st.form_submit_button("✅ Apply Filters", type="primary", use_container_width=True)
    with col2:
        reset= st.form_submit_button("🔄 Reset Filters", use_container_width=True)
if apply:
    st.session_state.selected_crop=crop
    st.session_state.selected_variety=variety
    st.session_state.selected_yield=Yield
    st.session_state.selected_maturity=maturity
    st.rerun()
if reset:
    st.session_state.selected_crop=sorted(clean_df["crop_type"].unique())
    st.session_state.selected_variety=sorted(clean_df["variety"].unique())
    st.session_state.selected_yield=(float(clean_df["yield_kg_per_m2"].min()),float(clean_df["yield_kg_per_m2"].max()))
    st.session_state.selected_maturity=(int(clean_df["days_to_maturity"].min()),int(clean_df["days_to_maturity"].max()))
    st.rerun()
    
filter_df=clean_df[clean_df["crop_type"].isin(st.session_state.selected_crop) & clean_df["variety"].isin(st.session_state.selected_variety)  & clean_df["yield_kg_per_m2"].between(st.session_state.selected_yield[0],st.session_state.selected_yield[1]) & clean_df["days_to_maturity"].between(st.session_state.selected_maturity[0],st.session_state.selected_maturity[1])]
if filter_df.empty:
    st.warning("# No Data For Current Filter")
    st.stop()
st.header("Data Visualization")
st.markdown("""
    This section presents visualizations to uncover insights from the greenhouse crop yield dataset. Each plot
    reveals a different aspect of how climate conditions, cultivation inputs, and crop genetics interact to
    determine yield.\n

    **Tip**: Use the filters in the sidebar to explore specific segments of the data. Set your desired filters
    and click 'Apply Filters' to update visualizations!
    """)
#Plot 1
st.subheader(" 1. Avg. Yield by Crop Type & Variety")
new_df=filter_df.groupby(["crop_type","variety"],as_index=False)["yield_kg_per_m2"].mean()
graph1=plt.bar(new_df,x="crop_type",y="yield_kg_per_m2",color="crop_type",title="Bar Graph")
graph1.update_layout(
    xaxis_title="Crop Type",
    yaxis_title="Yield"
)
st.plotly_chart(graph1, use_container_width=True)
st.subheader("👁️ Key Insight")
st.markdown("""
• Shows which crop (and which variety within it) produces the most yield on average.\n
• Quick way to rank crops — helps decide which crop is most "worth growing" for output \n                                
• Easy way to see the "best" crop at a glance.""")
st.divider()
#Plot 2
st.subheader("2. Temperature Vs Yield")
new_df=new_df=filter_df.groupby(["crop_type","avg_temperature_C"],as_index=False)["yield_kg_per_m2"].mean()
graph2=plt.scatter(new_df,x="avg_temperature_C",y="yield_kg_per_m2",color="crop_type",title="Scatter Plot")
graph2.update_layout(
    xaxis_title="Avg. Temperature ℃",
    yaxis_title="Yield"
)
st.plotly_chart(graph2,use_container_width=True)
st.subheader("👁️ Key Insight")
st.markdown("""
• Shows if hotter or cooler temperature helps crops grow better.\n
• If dots go up, temperature helps yield. If dots are messy, temperature doesn't matter much.\n                                        
• Comparing crops on the same chart shows if different crops have different "ideal" temperature zones.""")
st.divider()
#Plot 3
st.subheader("3. CO2 Vs Yield")
new_df=filter_df.groupby("days_to_maturity",as_index=False)[["yield_kg_per_m2","co2_ppm"]].mean()
graph3=plt.scatter(new_df,x="co2_ppm",y="yield_kg_per_m2",size="days_to_maturity",title="Bubble Chart",color="co2_ppm")
graph3.update_layout(
    xaxis_title="Co2 PPM",
    yaxis_title="Yield"
)
st.plotly_chart(graph3,use_container_width=True)
st.header("👁️ Key Insight")
st.markdown("""
• Checks if more CO₂ means more yield.\n
• Bubble size shows how long the crop took to grow.\n
• If no clear pattern, CO₂ isn't very important for yield.""")
st.divider()
#Plot 4
st.subheader("4. Month of Harvest Vs Yield")
new_df=filter_df.groupby(["harvest_date"],as_index=False)["yield_kg_per_m2"].mean()
new_df["month"]=new_df["harvest_date"].dt.to_period('M')
new_df["month"]=new_df["month"].astype(str)
graph4=plt.line(new_df,x="month",y="yield_kg_per_m2",title="Line Plot")
graph4.update_layout(
    height=600,
    xaxis_title="Month",
    yaxis_title="Yield"
)
st.plotly_chart(graph4,use_container_width=True)
st.header("👁️ Key Insight")
st.markdown("""
• Shows if waiting longer to harvest gives more yield.\n
• Line going up = longer growing time = better yield.\n
• Helps decide if it's worth extending growing time for better output, or if yield plateaus after a point.\n""")
st.divider()
#Plot 5
st.subheader("5. Temperature Vs Humidity")
new_df=filter_df.groupby("days_to_maturity",as_index=False)[["avg_temperature_C","humidity_percent"]].mean()
graph5=plt.density_heatmap(new_df,x="avg_temperature_C",y="humidity_percent")
graph5.update_layout(
    xaxis_title="Avg. Temperature ℃",
    yaxis_title="Humidity %"
)
st.plotly_chart(graph5,use_container_width=True)
st.header("👁️ Key Insight")
st.markdown("""
• Shows which temperature and humidity levels happen most often.\n
• Helps check if greenhouse conditions stay steady or change a lot.\n
• Helps spot whether extreme or unusual temperature-humidity combos are rare or common, which matters for reliability of other findings.""")
st.divider()
#Plot 6
st.subheader("6. Crop → Variety → Greenhouse (Days To Maturity)")
new_df=filter_df.groupby(["crop_type","variety","greenhouse_id"],as_index=False)["days_to_maturity"].mean()
new_df["days_to_maturity"]=new_df["days_to_maturity"].astype(int)
graph6=plt.sunburst(new_df,path=["crop_type","variety","greenhouse_id"],values="days_to_maturity",title="Sunburst")
st.plotly_chart(graph6,use_container_width=True)
st.header("👁️ Key Insight")
st.markdown("""
• Shows how maturity time is spread across crops, varieties, and greenhouses.\n
• Easy to spot which group takes longest or shortest to grow.\n                                                         
• Useful for spotting if a specific greenhouse consistently produces slower- or faster-maturing batches.
""")
st.divider()
#Plot 7
st.subheader("7. Crop → Variety → Yield")
new_df=filter_df.groupby(["crop_type","variety"],as_index=False)[["yield_kg_per_m2","days_to_maturity"]].median()
new_df["days_to_maturity"]=new_df["days_to_maturity"].astype(int)
graph7=plt.treemap(new_df,path=["crop_type","variety","yield_kg_per_m2"],values="yield_kg_per_m2",hover_data=["days_to_maturity"],title="Treemap")
st.plotly_chart(graph7,use_container_width=True)
st.header("👁️ Key Insight")
st.markdown("""
• Bigger boxes mean higher yield.\n
• Quick way to see best and worst crop varieties.\n                       
• Good for identifying underperforming varieties that might need review or could be phased out.""")
st.divider()
#Plot 8
st.subheader("8. Yield Spread by Variety")
graph8=plt.violin(filter_df,x="variety",y="yield_kg_per_m2",color="variety")
graph8.update_layout(
    xaxis_title="Variety",
    yaxis_title="Yield"
)
st.plotly_chart(graph8,use_container_width=True)
st.header("👁️ Key Insight")
st.markdown("""
• Shows if yield is steady or changes a lot for each variety.\n
• Thin shape = consistent yield. Wide shape = unpredictable yield.\n
• Helps identify varieties that are both high-yielding and dependable — often more valuable than just high average.""")
st.divider()
#Plot 9
st.subheader("9. Yield by Crop and Greenhouse")
graph9=plt.box(filter_df,x="crop_type",y="yield_kg_per_m2",color="greenhouse_id")
graph9.update_layout(
    xaxis_title="Crop Type",
    yaxis_title="Yield"
)
st.plotly_chart(graph9,use_container_width=True)
st.header("👁️ Key Insight")
st.markdown("""
• Compares yield across crops and greenhouses.\n
• Shows if one greenhouse does better or worse than others.\n
• Dots outside the box are unusual results worth checking.""")
st.divider()
#Plot 10
st.subheader("10. Light Vs Maturity Vs Photoperiod")
new_df=filter_df.groupby(["crop_type","greenhouse_id","days_to_maturity"],as_index=False)[["days_to_maturity","light_intensity_lux","photoperiod_hours"]].mean()
graph10=plt.scatter_3d(new_df,x="days_to_maturity",y="light_intensity_lux",z="photoperiod_hours",color="crop_type",title="Scatter 3D Plot")
graph10.update_layout(
    height=800,
    width=800,
    xaxis_title="Days to Maturity",
    yaxis_title="Light Intensity (Lux)",
    scene=dict(
        zaxis_title="Photoperiod (Hours)"
    )
)
st.plotly_chart(graph10,use_container_width=True)
st.header("👁️ Key Insight")
st.markdown("""
• Checks if more light or longer light hours help crops mature faster.\n
• Different crop colors show different light needs.\n
• Helps evaluate whether adjusting lighting setups (intensity or day-length) could speed up or optimize growing cycles.""")
st.divider()
#Plot 11
st.header("11.Fertilizer Composition for High Yield Crops")
filter_df["Yield Category"] = pd.qcut(
    filter_df["yield_kg_per_m2"],
    q=3,
    labels=["Low", "Medium", "High"]
)
high = filter_df[filter_df["Yield Category"] == "High"]
fertilizer = pd.DataFrame({
    "Fertilizer": ["Nitrogen", "Phosphorus", "Potassium"],
    "Amount": [
        high["fertilizer_N_kg_ha"].sum(),
        high["fertilizer_P_kg_ha"].sum(),
        high["fertilizer_K_kg_ha"].sum()
    ]
})
graph11= plt.pie(
    fertilizer,
    names="Fertilizer",
    values="Amount",
    title="Pie Chart"
)
st.plotly_chart(graph11,use_container_width=True)
st.subheader("👁️ Key Insight")
st.markdown("""• Nitrogen contributes the largest share of fertilizer usage in the high-yield category, indicating its significant role in achieving higher crop productivity (if it is the largest slice in your chart.\n
• Phosphorus and Potassium are also essential, but their usage is comparatively lower, showing that balanced nutrient application supports high yields.\n
• High-yield crops are associated with a combination of N, P, and K fertilizers, highlighting the importance of balanced fertilization rather than relying on a single nutrient.""")
st.divider()
#===================================================
#Conclusion and summary
#===================================================
st.header("Conclusion and Summary")
st.markdown("""This project successfully demonstrated the use of Exploratory Data Analysis (EDA) to analyze greenhouse crop production data and identify the factors affecting crop yield. By applying data cleaning, preprocessing, visualization, and interactive dashboard development, the project transformed raw data into meaningful insights that support informed decision-making in greenhouse farming.
**Key Conclusions:**
• Successfully cleaned, processed, and analyzed the greenhouse crop production dataset using Python and Pandas.\n
• Developed an interactive Streamlit dashboard with filters and visualizations for efficient data exploration.\n
• Identified fertilizer application, particularly nitrogen and potassium, as the most influential factors affecting crop yield.\n
• Observed that temperature has a moderate positive relationship with crop productivity, while factors such as • CO₂ concentration, soil pH, irrigation, and pest severity showed relatively weak correlations.\n
• Found that tomatoes achieved the highest average yield among the crops analyzed, followed by cucumbers, peppers, and lettuce.\n
• Demonstrated how interactive visualizations help users compare crop performance, identify trends, and better understand production patterns.\n
• Showed that Exploratory Data Analysis is an effective approach for extracting valuable insights from agricultural datasets and supporting data-driven greenhouse management.\n
• Established a strong foundation for future enhancements, including predictive analytics, real-time monitoring, and advanced decision-support systems.""")
st.divider()
st.header("Future scope")
st.markdown("""
Although this project provides valuable insights into greenhouse crop production through exploratory data analysis, there are several opportunities for further enhancement:

• Develop machine learning models to predict crop yield based on environmental and agricultural parameters.\n
• Integrate real-time IoT sensor data to enable continuous monitoring and live analysis of greenhouse conditions.\n
• Expand the dataset by including additional crops, greenhouse locations, and multiple growing seasons to improve the scope of analysis.\n
• Add advanced analytical features such as trend forecasting, anomaly detection, and automated recommendation systems for fertilizer and irrigation management.\n
• Deploy the dashboard as a cloud-based web application with user authentication, report generation, and data export capabilities for farmers, researchers, and agricultural organizations.\n
• Incorporate external data sources such as weather forecasts, market prices, and energy consumption to support more comprehensive decision-making.\n
• Enhance the dashboard with customizable visualizations, interactive reports, and mobile-friendly access to improve usability and accessibility.\n
• Implement automated data collection and database integration to reduce manual data entry and ensure that analyses remain accurate and up to date.""")
st.subheader("Data Analysis Summary")
st.markdown("""
This comprehensive analysis of the greenhouse crop yield dataset has revealed significant insights into how
climate conditions, cultivation inputs, and crop genetics interact to shape productivity. Through ten diverse
visualizations and statistical analyses, we have uncovered valuable patterns that can guide greenhouse
operations and crop planning.
""")

st.subheader("Major Findings & Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### **Crop & Variety Performance**
    - **Yield Variation**: Average yield differs meaningfully across crop types
    - **Consistency**: Some varieties show tighter, more predictable yield distributions than others
    - **Top Performers**: The treemap and sunburst views help identify the highest-yielding crop/variety
      combinations
    - **Distribution Shape**: Yield is not uniformly distributed — certain ranges are far more common than others

    ### **Climate Relationships**
    - **Temperature Effects**: Yield shows a relationship with average growing temperature that varies by crop
    - **CO₂ & Light Interaction**: Combining CO₂ enrichment with light intensity affects yield outcomes jointly
    - **Humidity Patterns**: Common temperature-humidity combinations cluster around typical greenhouse
      operating conditions
    """)

with col2:
    st.markdown("""
    ### **Temporal Trends**
    - **Seasonality**: Average yield fluctuates across planting months, suggesting seasonal effects on growth
    - **Planning Implications**: Identifying favorable planting windows can help schedule future crop cycles

    ### **Data Quality**
    - **Missing Data**: Several climate and fertilizer columns required crop-specific median imputation
    - **Outliers**: IQR-based detection identified extreme values in yield, temperature, and irrigation
    - **Clean Baseline**: The processed dataset provides a reliable foundation for further analysis

    ### **Operational Opportunities**
    - **Climate Control**: Fine-tuning temperature, humidity, and CO₂ levels can help maximize yield
    - **Variety Selection**: Favoring consistently high-yielding varieties can reduce output variability
    """)

st.markdown("---")

st.subheader("Business Implications & Recommendations")

with st.expander("**For Greenhouse Operators**", expanded=True):
    st.markdown("""
    **Strategic Recommendations:**

    1. **Climate Management**:
       - Maintain temperature and humidity within the ranges shown to correlate with higher yields
       - Use CO₂ enrichment alongside adequate lighting to boost productivity

    2. **Crop & Variety Selection**:
       - Prioritize greenhouse space for consistently high-yielding crop/variety combinations
       - Monitor yield variability within varieties to identify the most reliable performers

    3. **Planting Schedule**:
       - Align planting dates with the months historically associated with higher average yield
       - Track pest severity and soil pH to catch conditions that may suppress yield early

    4. **Continuous Monitoring**:
       - Regularly log environmental and input data to keep the yield model current
       - Use outlier detection to flag unusual growing cycles for investigation
    """)

with st.expander("**For Agronomists & Researchers**"):
    st.markdown("""
    **Research Insights:**

    1. **Growing Condition Analysis**:
       - Temperature, humidity, CO₂, and light intensity each play measurable roles in yield outcomes
       - Interaction effects (e.g., CO₂ combined with light) may matter more than single-factor analysis

    2. **Variety Trials**:
       - Yield distribution differences across varieties suggest genetic or management factors worth studying
       - Violin plots reveal not just averages but full performance ranges, useful for trial design

    3. **Data Collection Priorities**:
       - Columns with high missingness (fertilizer inputs, CO₂) may benefit from more consistent sensor logging
       - Soil pH and pest severity trends deserve deeper longitudinal study
    """)

with st.expander("**For Farm Managers & Investors**"):
    st.markdown("""
    **Investment & Planning Opportunities:**

    1. **Resource Allocation**:
       - Direct greenhouse capacity toward crop/variety combinations with strong, consistent yield
       - Evaluate underperforming greenhouses identified in the hierarchical breakdown

    2. **Risk Assessment**:
       - Wide yield distributions for certain varieties suggest higher production risk
       - Seasonal yield trends can inform staffing and input procurement schedules

    3. **Scalability**:
       - Varieties with narrow, high-median yield distributions are strong candidates for scaling up
       - Data-driven climate control investments can pay off where yield sensitivity to temperature/humidity
         is highest
    """)

st.markdown("---")
st.subheader("Final Conclusion")

col1, col2, col3= st.columns(3)

with col1:
    st.metric("Crop Types Analyzed", clean_df["crop_type"].nunique())
with col2:
    st.metric("Varieties Analyzed", clean_df["variety"].nunique())
with col3:
    st.metric("Greenhouses Analyzed", clean_df["greenhouse_id"].nunique())
col4,col5=st.columns(2)
with col4:
    st.metric("Avg Yield", f"{clean_df['yield_kg_per_m2'].mean():.2f} kg/m²")
with col5:
    st.metric("Max Yield", f"{clean_df['yield_kg_per_m2'].max():.2f} kg/m²")

st.markdown("""
### **Project Impact**\n

This analysis provides greenhouse operators, agronomists, and investors with a data-driven view of how growing
conditions and crop choices interact to determine yield. By identifying the strongest climate and input
relationships, decision-makers can make more informed choices about crop selection, climate control, and
planting schedules to improve productivity.\n

**Key Takeaways:**\n

1. **Data-Driven Decision Making**: Greenhouses that leverage climate and yield data can optimize operations\n
2. **Climate Optimization**: Temperature, humidity, CO₂, and light intensity together shape yield outcomes\n
3. **Variety Selection Matters**: Consistent, high-yielding varieties reduce production risk\n
4. **Seasonal Planning**: Planting-date trends can guide more effective crop scheduling\n
5. **Data Quality Foundation**: Careful cleaning and outlier treatment ensure reliable, trustworthy analysis
""")