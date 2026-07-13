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
st.title("🏡 Exploratory Analysis of Greenhouse Crop Production")
st.write("#")
st.header("📄 Executive Summary")
st.markdown("""This report analyzes 10,400 greenhouse harvest records across four crops — tomato, cucumber, pepper, and lettuce — examining how environmental conditions and fertilization affect yield. The data was clean, with no missing values across 20 variables.\n
The clearest finding is that fertilizer, particularly nitrogen and potassium, is the strongest driver of yield, far outweighing environmental factors like CO₂, soil pH, or irrigation, which showed almost no correlation. Temperature had a moderate positive effect, and longer maturity periods generally produced higher yields.
Among crops, tomatoes performed best (avg. 16.7 kg/m²), followed by cucumbers, peppers, and lettuce. Growing conditions across greenhouses were fairly consistent, making fertilizer strategy and crop choice the main factors behind yield differences.\n
Overall, the results suggest fertilizer optimization offers the greatest potential for improving greenhouse productivity, though causal claims would need further experimental validation.""")
st.subheader("🔑 Key Points")
st.write("""• Dataset: 10,400 records, 4 crops, 5 greenhouses, no missing values\n
• Top yield driver: Nitrogen fertilizer (strongest correlation), followed by potassium and phosphorus\n
• Weak/no impact: CO₂, soil pH, irrigation, pest severity\n
• Temperature: Moderate positive effect on yield\n
• Best performing crop: Tomato (16.7 kg/m² avg.), also had the longest maturity period\n
• Crop yield ranking: Tomato > Cucumber > Pepper > Lettuce\n
• Growing conditions: Fairly uniform across greenhouses, isolating fertilizer/crop choice as key variables\n
• Limitation: Findings are correlational, not causal — needs experimental validation\n
""")
st.subheader("📦 Expected Deliverables")
st.markdown("""• A cleaned and well-organized greenhouse crop production dataset ready for analysis.\n
• An exploratory data analysis with meaningful visualizations to identify trends and patterns.\n
• An interactive Streamlit dashboard for easy exploration and presentation of the data.\n
• Key insights and recommendations to support improved greenhouse crop production and decision-making.""")
st.divider()
st.header("⚠️ Problem Description")
st.subheader("🧩 Problem Statement")
st.markdown("""Greenhouse crop production generates large amounts of data on environmental conditions, irrigation, fertilizer use, and crop yield. However, raw data alone is difficult to interpret and does not provide meaningful insights. This project applies Exploratory Data Analysis (EDA) to clean, analyze, and visualize the data, helping identify trends, relationships, and factors that influence crop productivity and support better decision-making.\n
• Raw greenhouse data is difficult to interpret without analysis.\n
• Multiple factors affect crop growth and yield.\n
• Exploratory Data Analysis helps identify hidden trends and patterns.\n
• Data visualizations simplify complex information for better understanding.\n
• Insights from the analysis support improved greenhouse crop management.""")
st.subheader("🗂️ Dataset Overview")
st.markdown("""The greenhouse crop production dataset provides comprehensive information on crop cultivation, environmental conditions, agricultural inputs, and production outcomes within a controlled greenhouse environment.\n
***Dataset Description***\n
• The dataset contains information related to greenhouse crop production and cultivation conditions.\n
• It includes environmental, agricultural, and production-related variables collected for analysis.\n
• The data is used to explore relationships between greenhouse conditions and crop yield.\n    
***Dataset Size***\n
• Number of Records: 5,000\n
• Number of Features (Columns): 19\n
***Data Types***\n
• Categorical Data: Crop Type, Variety\n
• Date Data: Planting Date, Harvest Date\n
• Numerical Data: Environmental parameters, fertilizer usage, irrigation, soil pH, pest severity, and crop yield.\n
***Purpose of the Dataset***\n
• To analyze greenhouse crop production using exploratory data analysis techniques.\n
• To identify trends, patterns, and correlations among production variables.\n
• To evaluate the impact of environmental and agricultural factors on crop yield.\n
• To support data-driven decision-making for improving greenhouse farming practices.  """)

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
clean_df=clean_df.drop_duplicates()
tab1,tab2,tab3,tab4,tab5,tab6,tab7=st.tabs(
    [
    "📋 Column Info",
    "❌ Missing Values",
    "👀 Sample Data",
    "📊 Statistics",
    "🔤 Categorical Data",
    "✅ Data Quality",
    "✨ Final Data"
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
with tab2:
    st.subheader("❌ Missing Values Analysis")

    missing = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values,
        "Missing %": ((df.isnull().sum()/len(df))*100).round(2)
    })

    st.dataframe(missing, use_container_width=True)

    fig = plt.bar(
        missing,
        x="Column",
        y="Missing Values",
        color="Missing Values",
        title="Missing Values by Column"
    )

    st.plotly_chart(fig, use_container_width=True)
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

        variety=df["variety"].value_counts().reset_index()

        variety.columns=["Variety","Count"]

        st.dataframe(variety,use_container_width=True)

        col1,col2=st.columns(2)

        with col1:

            fig=plt.bar(
                variety,
                x="Variety",
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

    fig=plt.bar(
        quality,
        x="Column",
        y="Completeness %",
        color="Completeness %",
        title="Column Completeness"
    )

    st.plotly_chart(fig,use_container_width=True)

with tab7:
    st.subheader("📈 Cleaned Dataset Basic Information")
    memory1=clean_df.memory_usage(deep=True).sum()/(1024**2)
    column1,column2,column3=st.columns(3)
    with column1:
        st.metric("Total Records",f"{clean_df.shape[0]:,}")
    with column2:
        st.metric("Total Columns",f"{clean_df.shape[1]:,}")
    with column3:
        st.metric("Memory used",f"{memory1:.2f}MB")
st.divider()
clean_df=clean_df.drop_duplicates()
if "selected_crop" not in st.session_state:
    st.session_state.selected_crop=sorted(clean_df["crop_type"].unique())
if "selected_variety" not in st.session_state:
    st.session_state.selected_variety=sorted(clean_df["variety"].unique())
if "selected_yield" not in st.session_state:
    st.session_state.selected_yield=(float(clean_df["yield_kg_per_m2"].min()),float(clean_df["yield_kg_per_m2"].max()))
if "selected_maturity" not in st.session_state:
    st.session_state.selected_maturity=(int(clean_df["days_to_maturity"].min()),int(clean_df["days_to_maturity"].max()))
with st.sidebar:
    st.write("🌽 Crop Filter")
    crop=st.multiselect(
        "Select the type of crop",
        options=sorted(clean_df["crop_type"].unique()),
        default=st.session_state.selected_crop
        )
    st.write("🌱 Variety Filter ")
    variety=st.multiselect(
        "Select the type of crop",
        options=sorted(clean_df["variety"].unique()),
        default=st.session_state.selected_variety
        )
    st.write("🌾 Yield Filter")
    Yield=st.slider(
        "Select the yield range ",
        clean_df["yield_kg_per_m2"].min(),
        clean_df["yield_kg_per_m2"].max(),
        st.session_state.selected_yield
    )
    st.write("⏳ Days to Maturity Filter")
    maturity=st.slider(
        "Select the Days to Maturity Range",
        clean_df["days_to_maturity"].min(),
        clean_df["days_to_maturity"].max(),
        st.session_state.selected_maturity
    )
    col1,col2=st.columns(2)
    with col1:
        apply=st.button("✅ Apply",type="primary")
    with col2:
        reset=st.button("❌ Reset")
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
st.header("Visualization")
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
st.subheader("4. Days to Maturity Vs Yield")
filter_df["harvest_date"]=pd.to_datetime(filter_df["harvest_date"])
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
st.header("Conclusion")
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