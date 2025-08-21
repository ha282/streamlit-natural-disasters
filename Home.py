import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(
    page_title="Natural Disasters",
)

st.title(":green[Natural] :red[Disasters] 🔥")
#st.sidebar.success("Select a page above. ")

# Importing dataset
df = pd.read_csv("cleaned_dataset9.csv")

# # Show the data
# #st.dataframe(df)

# Select a year option
years = sorted(df['start_year'].unique())
years_options_including_all_years = []
years_options_including_all_years.append("All Years")

for year in years:
    year_str = str(year) 
    years_options_including_all_years.append(year_str)

#st.sidebar.subheader("Select a Filtering Option:")    
selected_year = st.sidebar.selectbox("Select Year", years_options_including_all_years)
month_names = ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December']

if selected_year == "All Years":
    # Add Metrics
    total_recorded_disasters = df["disno"].nunique()
    total_number_countries_affected = df["country"].nunique()
    most_frequent_disaster_type = df["disaster_type"].value_counts().idxmax()
    worst_year_df = df.groupby(['start_year']).size().reset_index(name='occurrences')
    worst_year_df = worst_year_df.sort_values(by='occurrences', ascending=False).head(1)
    worst_year = worst_year_df['start_year']
    #st.write(worst_year_df)
else:
    df_filtered_by_year = df[df['start_year'] == int(selected_year)]
    total_recorded_disasters = df_filtered_by_year["disno"].nunique()
    total_number_countries_affected = df_filtered_by_year["country"].nunique()
    most_frequent_disaster_type = df_filtered_by_year["disaster_type"].value_counts().idxmax()
    
col1, col2= st.columns(2)

col1.metric(":red[Total Disasters]", total_recorded_disasters, border=True, help="Total Number of Recorded Disasters")
col2.metric(":red[Countries Affected]", total_number_countries_affected, border=True, help="Total Number of Countries with recorded Disasters")
col1.metric(":red[Most Frequent Disaster Type]", most_frequent_disaster_type, border=True, help="Most Frequent Disaster Type")

if selected_year == "All Years":
    col2.metric(":red[Worst Year]", worst_year, border=True, help="Year with most recorded disasters")
else:
    #worst month instead
    worst_month_df = df_filtered_by_year.groupby(['start_month']).size().reset_index(name='occurrences')
    worst_month_df = worst_month_df.sort_values(by='occurrences', ascending=False).head(1)
    worst_month = int(worst_month_df['start_month'].iloc[0])
    worst_month_str = month_names[worst_month - 1]
    col2.metric(":red[Month Year]", worst_month_str, border=True, help="Month with most recorded disasters")
    

# Choropleth Map
st.subheader(":green[Natural Disaster Occurrences by Country]")
if selected_year == "All Years":
    df_country_count = df.groupby(['iso', 'country']).size().reset_index(name='Occurrences')

    fig_choropleth_map = px.choropleth(
        df_country_count,
        locations='iso',
        color='Occurrences',
        hover_name='country',
        color_continuous_scale=px.colors.sequential.Aggrnyl,
    )

    fig_choropleth_map.update_layout(
        geo=dict(
            bgcolor='black'
        ),
    )
    st.plotly_chart(fig_choropleth_map, key="unique_chart_1")
else:
    df_country_count = df_filtered_by_year.groupby(['iso', 'country']).size().reset_index(name='Occurrences')

    fig_choropleth_map = px.choropleth(
        df_country_count,
        locations='iso',
        color='Occurrences',
        hover_name='country',
        color_continuous_scale=px.colors.sequential.Aggrnyl,
    )

    fig_choropleth_map.update_layout(
        geo=dict(
            bgcolor='black'
        ),
    )
    st.plotly_chart(fig_choropleth_map, key="unique_chart_1")


#scatter
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


if selected_year == "All Years":
    df['start_month_name'] = df['start_month'].apply(lambda x: month_names[int(x) - 1])
    #st.write(df['start_month_name'])
    monthly_counts = df['start_month_name'].value_counts().reindex(month_names, fill_value=0)
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=(monthly_counts.tolist() + [monthly_counts.tolist()[0]]),
        theta=(month_names + [month_names[0]]),
        fill='toself',
        name='Disaster Frequency',
        line_color='red'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max(monthly_counts.tolist() + [monthly_counts.tolist()[0]]) + 100]), bgcolor='skyblue'),
        showlegend=False,
        #title="Natural Disasters by Month",
    )
    st.subheader(":green[Natural Disaster by Month]")
    st.plotly_chart(fig)
else:
    df_filtered_by_year['start_month_name'] = df_filtered_by_year['start_month'].apply(lambda x: month_names[int(x) - 1])
    #st.write(df['start_month_name'])
    monthly_counts = df_filtered_by_year['start_month_name'].value_counts().reindex(month_names, fill_value=0)
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=(monthly_counts.tolist() + [monthly_counts.tolist()[0]]),
        theta=(month_names + [month_names[0]]),
        fill='toself',
        name='Disaster Frequency',
        line_color='red'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max(monthly_counts.tolist() + [monthly_counts.tolist()[0]]) + 30]), bgcolor='skyblue'),
        showlegend=False,
        #title="Natural Disasters by Month",
    )
    st.subheader(":green[Natural Disaster by Month]")
    st.plotly_chart(fig)

# About Section
with st.expander("About"):
    st.write('''
        *Data was obtained from EM-DAT: https://www.emdat.be/
        
        
         **What is a natural disaster?**  
            A natural disaster is a sudden, extreme event caused by environmental factors that leads to significant damage or loss of life. 
            Examples include earthquakes, floods, hurricanes, droughts, and wildfires.
    ''')
    st.image("globe.jpg")
