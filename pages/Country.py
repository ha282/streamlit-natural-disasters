import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Country")
st.title(":green[Country] 🌍")

# Importing dataset
df = pd.read_csv("cleaned_dataset9.csv")

# Select country

country = sorted(df['country'].unique())
selected_country = st.selectbox("Select a Country", country)

# Adding slider
min_year = int(df['start_year'].min())
max_year = int(df['start_year'].max())

selected_year_range = st.sidebar.slider(
    "Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year),
    step=1
)

df_filtered_by_year_range = df[
    (df['start_year'] >= selected_year_range[0]) &
    (df['start_year'] <= selected_year_range[1])
]

# df for country with filtered dataset
df_where_country_selected = df_filtered_by_year_range[df_filtered_by_year_range['country'] == selected_country]
df_year_count = df_where_country_selected.groupby(['start_year', 'disaster_type']).size().reset_index(name='occurrences')
most_frequent_disaster_type = df_year_count["disaster_type"].value_counts().idxmax()

# select sub_group
sub_group = sorted(df_filtered_by_year_range['disaster_subgroup'].unique())

disaster_types = df_year_count['disaster_type'].unique()

highlight_most_frequent_color_map = {}

for disaster_type in df_year_count['disaster_type'].unique():
    if disaster_type == most_frequent_disaster_type:
        highlight_most_frequent_color_map[disaster_type] = 'red'
    else:
        highlight_most_frequent_color_map[disaster_type] = 'skyblue'
        
st.subheader(f":green[Disasters per Year in {selected_country} - Most Frequent ]"+ " " +f":red[{most_frequent_disaster_type}]")

years_range_1 = list(range(selected_year_range[0], selected_year_range[1] + 1))
# st.write(years_range_1)

all_disaster = df_year_count['disaster_type'].unique().tolist()
# st.write(all_disaster)

df_years_range = pd.DataFrame({'start_year': years_range_1})
df_disaster = pd.DataFrame({'disaster_type': all_disaster})

data = df_years_range.merge(df_disaster, how='cross')

filled_data = data.merge(
    df_year_count,
    on=['start_year', 'disaster_type'],
    how='left'
)

fig_bar = px.bar(
    filled_data,
    x='start_year',
    y="occurrences",
    color="disaster_type",
    color_discrete_map=highlight_most_frequent_color_map,
    labels={'start_year': 'Year', 'occurrences': 'Number of Disasters', 'disaster_type': 'Disaster Type'},
)

if selected_year_range == (min_year, max_year):
    fig_bar.update_xaxes(range=[1999, 2025], dtick=1)
else:
    fig_bar.update_xaxes(range=[selected_year_range[0]-1, selected_year_range[1]+1], dtick=1)
    

st.plotly_chart(fig_bar, use_container_width=True)

#metrics section
total_recorded_disasters1 = df_year_count["occurrences"].sum()

#rest of the world
# st.write(df_filtered_by_year_range.shape[0])

#filter our select country data 
df_where_country_is_not_selected = df_filtered_by_year_range[df_filtered_by_year_range['country'] != selected_country]
disasters_each_country = df_where_country_is_not_selected.groupby('country').size().reset_index(name='occurrences')
# st.write(disasters_each_country)
mean_disaster_rest_of_the_world = round(disasters_each_country['occurrences'].mean())
# st.write(mean_disaster_rest_of_the_world)

col1, col2= st.columns(2)
#st.write(df_year_count)
#st.write(total_recorded_disasters)

if total_recorded_disasters1 > mean_disaster_rest_of_the_world:
    col1.metric(":red[Total Disasters]", total_recorded_disasters1, border=True, help="Total Number of Recorded Disasters")
    col2.metric(":green[Mean Disaster]", mean_disaster_rest_of_the_world, border=True, help="Mean Number of Disasters All Other Countries")
    #col3.metric(":red[Most Frequent Disaster Type]", most_frequent_disaster_type, border=True, help="Most Frequent Disaster Type")
else:
    col1.metric(":green[Total Disasters]", total_recorded_disasters1, border=True, help="Total Number of Recorded Disasters")
    col2.metric(":red[Mean Disaster]", mean_disaster_rest_of_the_world, border=True, help="Mean Number of Disasters All Other Countries")
 
#drop down section   
#st.write(df_year_count)
df_drop_down = df_where_country_selected.groupby(['start_year', 'disaster_type', 'disaster_subtype']).size().reset_index(name='occurrences')
#st.write(df_drop_down)


st.subheader('Type of Disaster')
# st.selectbox("Select ", years_options_including_all_years))
with st.popover("Type of Disaster"):sort_option = st.radio(
                "select:",
                ["Broad Type","Subtype"],
                index=0
            )
# selected_disaster = st.selectbox('Select a Disaster to view Subtypes', disaster_types)




if sort_option == "Broad Type":
    #col1, col2 = st.columns(2)
    df_drop_down_1 =df_year_count.groupby(['disaster_type']).size().reset_index(name='occurrences').sort_values(ascending=False, by='occurrences')
    #st.table(df_drop_down_1[['disaster_type','occurrences']])
    df_drop_down_1.columns=['Disaster Types', 'Occurrences']
    st.markdown(
        df_drop_down_1[['Disaster Types', 'Occurrences']].to_html(index=False), unsafe_allow_html=True
    )

    df_drop_down_1_new =df_year_count.groupby(['disaster_type']).size().reset_index(name='occurrences').sort_values(ascending=False, by='occurrences')
    disaster_types = df_drop_down_1_new['disaster_type'].unique().tolist()
    selected_disaster = st.selectbox('Select a Broad Disaster Type to view Subtypes', disaster_types)
    #st.write(df_drop_down)
    df_where_type_selected = df_drop_down[df_drop_down['disaster_type'] == selected_disaster]
    df_where_type_selected_show_subtype = df_where_type_selected.groupby(['disaster_subtype']).size().reset_index(name='occurrences').sort_values(ascending=False, by='occurrences')
    #st.write(df_where_type_selected_show_subtype)
    df_where_type_selected_show_subtype.columns=['Disaster Subtypes', 'Number of Occurrences']
    st.markdown(
        df_where_type_selected_show_subtype[['Disaster Subtypes', 'Number of Occurrences']].to_html(index=False), unsafe_allow_html=True
    )
            

if sort_option == "Subtype":
    #st.write(df_drop_down)
    df_drop_down_2 = df_drop_down.groupby(['disaster_subtype']).size().reset_index(name='occurrences').sort_values(ascending=False, by='occurrences')
    df_drop_down_2.columns=['Disaster Subtypes', 'Number of Occurrences']
    st.markdown(
        df_drop_down_2[['Disaster Subtypes', 'Number of Occurrences']].to_html(index=False), unsafe_allow_html=True
    )