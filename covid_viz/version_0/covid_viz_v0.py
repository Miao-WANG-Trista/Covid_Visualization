#!/usr/bin/env python
# coding: utf-8

# %% Import libraries

import pandas as pd
import plotly.express as px
import plotly

# %% Import and clean data

'''Geodata '''

df_geo = pd.read_csv("departements_france_long_lat.csv")
df_geo = df_geo.rename(columns={"code_departement": "dep",
                                "nom_departement": "name_dep", 
                                    "nom_region" : "name_region" })


'''total confirmed cases data ''' 

conf = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/d3a98a30-893f-47f7-96c5-2f4bcaaa0d71") 
conf = conf.rename(columns={"total_cas_confirmes": "Total confirmed cases"})  
conf = conf.iloc[:,0:2]  # extract total confirmed cases



''' daily positive tests  data'''

dailycase = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/001aca18-df6a-45c8-89e6-f82d689e6c01", 
                        sep=";", header = 0)
dailycase = dailycase.rename(columns={"reg":"code_region","jour": "Date", 
                                      "P_f": "Female","P_h": "Male","P": "Daily Total"})

# keep only daily postive tests(delete colunms for number of tests conducted)
dailycase = dailycase.drop(columns = ["T_f","T_h","T"])  

# select total daily postive tests for all-age group (code 0)
dailycase = dailycase[(dailycase["cl_age90"] == 0)] 

# merge daily positive tests with geo data (assign region names)
df_geo2 = df_geo.iloc[:,2:4].drop_duplicates('name_region')
dailycase_region = pd.merge(dailycase, df_geo2, on ="code_region", how ="left") 
dailycase_region["name_region"].fillna("Overseas",inplace = True)

# calculate daily positive tests in France
dailycase_total = dailycase_region.groupby(by=["Date"]).sum().reset_index()
dailycase_total["name_region"] = "France"

# combine the regions and total together
dailycase_cleaned = pd.concat([dailycase_total,dailycase_region])

# keep only metropolitan France(drop DROM(1, 2, 3, 4, 6 ))
dailycase_cleaned = dailycase_cleaned.drop(dailycase_cleaned[dailycase_cleaned.code_region < 10].index)


'''hospital data'''

df = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7", 
                 sep = ";", header = 0)
df = df.rename(columns={"jour": "date", "sexe": "sex"})
#df.head()

# keep only metropolitan France(drop outre-mer DROM("971", "972", "973", "974", "976"))
hosp_cleaned = df.drop(df[df.dep > "970"].index)

# keep only colunms of number people currently hosipitalized(delete colunms for intesive care, 
# returned home and deaths at hosiptal)
hosp_cleaned = hosp_cleaned.loc[:,["dep","sex","date","hosp"]]

# merge hospital data and geodata, group by regions
hosp_temp = pd.merge(df_geo, hosp_cleaned)
hosp_region = hosp_temp.groupby(["code_region","name_region", "date","long", "lat", "sex"], 
                                as_index=False)["hosp"].sum()


# %% Fliter variables           # will be replaced with input command in later stages

# for total confirmed cases 
date_query_start = "2020-03-02" 
date_query_end = dailycase_cleaned.iloc[-1,0] #latest update

# for daily new positive tests
selected_region= "France"
selected_yvalue="Daily Total"
dailycase_cleaned2 = dailycase_cleaned.loc[dailycase_cleaned["name_region"] == selected_region]

# for hospital data 
date_query = hosp_cleaned.iloc[-1,2]  #latest update
sex_query = 0
sex_query_label = {0:"All genders", 1:"Male", 2:"Female" }
hosp_cleaned = hosp_region[(hosp_region["sex"] == sex_query) & (hosp_region["date"] == date_query)]

# %%Visualization  

# Bar chart: total confirmed cases in France
fig_bar = px.bar(conf, x="date", y="Total confirmed cases", 
             labels={"Total confirmed cases":"Total confirmed cases in France", "date": "Date"},
              color_continuous_scale="peach", color="Total confirmed cases", height=500,
             title="Total COVID-19 confirmed cases in France, from " + date_query_start + " to " + date_query_end,
             range_x=[date_query_start,date_query_end])

# change the format of the charts
fig_bar.update_layout(
    font_family="Arial",
    title_font_family="Arial",
)



# Line chart: daily new positive tests in France
fig_line = px.line(dailycase_cleaned2, x="Date", y= selected_yvalue,
             labels={"Daily Total":"Daily new potisive tests"},
             color="name_region",
             title="Daily new COVID-19 positive tests in France, from " + date_query_start + " to " + date_query_end,
             range_x=[date_query_start,date_query_end])

# change the format of the charts
fig_line.update_layout(
    font_family="Arial",
    title_font_family="Arial",
    autosize=False,width=1100,height=800,
    )



# Bubble map: the number of people currently hospitalized by region
fig_bubblemap = px.scatter_mapbox(hosp_cleaned, lat="lat", lon="long", 
                        hover_name="name_region", hover_data=["hosp"],
                        size="hosp",size_max=80, 
                        color="hosp",color_continuous_scale= px.colors.sequential.YlOrRd, 
                        opacity = 0.85,
                        zoom=5, height=800,
                         title="Number of people currently hospitalized due to COVID-19 infection, "
                         + sex_query_label[sex_query] + ", as of "+ date_query)

fig_bubblemap.update_layout(mapbox_style="open-street-map")
fig_bubblemap.update_layout(margin={"r":50,"t":50,"l":50,"b":50})

# %% Export output as html files 

print('''By running this file, 3 visulizations of the CVOID-19 pandemic in France will be generated:
          1. Total COVID19 confirmed cases in France;
          2. Daily new COVID-19 positive tests in France;
          3. Number of people currently hospitalized due to COVID-19 infection in each region.
         
         Data range: Metropolitian France only, as of latest update
         Data source: Santé publique France''')
                
plotly.offline.plot(fig_bar, filename="latest_total_confirmed_cases.html")
plotly.offline.plot(fig_line, filename="latest_daily_postive_tests.html")
plotly.offline.plot(fig_bubblemap, filename="latest_bubble_map.html")
