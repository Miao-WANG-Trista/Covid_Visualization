"""to define functions drawing four kinds of graphs"""

import plotly.express as px
import plotly

def bar_chart(conf,start_date,end_date):
    """Bar chart: to describe total confirmed cases in France

    :param conf: cleaned total confirmed cases dataframe
    :param start_date: the start of date query, a string passed from outside
    :param end_date: the end of date query, a string passed from outside
    :returns: a html file containing bar_chart
    """
    date_query_start = start_date
    date_query_end = end_date #conf.iloc[:,0].max() if end_date=='no' else end_date
    fig_bar = px.bar(conf, x="date", y="Total confirmed cases",
                 labels={"Total confirmed cases":"Total confirmed cases in France", "date": "Date"},
                  color_continuous_scale="peach", color="Total confirmed cases", height=500,
                 title="Total COVID-19 confirmed cases in France, from " + str(date_query_start) + " to " + str(date_query_end),
                 range_x=[date_query_start,date_query_end])
    # change the format of the charts
    fig_bar.update_layout(font_family="Arial",title_font_family="Arial",width=1100, height=800,template="ggplot2")
    #return fig_bar
    plotly.offline.plot(fig_bar, filename="latest_total_confirmed_cases.html")



def line_chart(dailycase_cleaned,sex,region,start_date,end_date):
    """Line chart: to describe daily new positive tests and death in France
    
    :param dailycase_cleaned: cleaned dataframe of daily new positive tests and death
    :param sex: sex query choice, values in ['0','1','2']
    :param region: region query choice, values in keys of a predefined dictionary
    :param start_date: the start of date query, a string passed from outside
    :param end_date: the end of date query, a string passed from outside
    :returns: a html file containing a composite line_chart
    """
    selected_region = "France" if region == 'total' else region
    dailycase_cleaned2 = dailycase_cleaned.loc[dailycase_cleaned["name_region"] == selected_region]
    if sex=='0':
        selected_yvalue = "Daily Total"
    elif sex=='1':
        selected_yvalue = "Male"
    else:
        selected_yvalue = "Female"
    end_date = dailycase_cleaned.iloc[:, 0].max() if end_date == 'no' else end_date
    fig_line = px.line(dailycase_cleaned2, x="Date", y=[selected_yvalue, 'Daily death'],
                 labels={"Daily Total":"Daily new potisive tests and death"},
                 color="name_region", hover_name='name_region',
                 title="Daily new COVID-19 positive tests and death in "+selected_region+" of "+selected_yvalue+" from " + start_date + " to " +end_date,
                 color_discrete_sequence=px.colors.qualitative.Pastel1,
                 range_x=[start_date,end_date])

    # change the format of the charts
    fig_line.update_layout(
        font_family="Arial",
        title_font_family="Arial",
        autosize=False,width=1100,height=800,
        )
    plotly.offline.plot(fig_line, filename="latest_daily_positive_tests.html")



def Bubble_map(hosp_region,sex,date_query_start,date_query):
    """Bubble map: to describe the number of people currently hospitalized by region
    
    :param hosp_region: cleaned dataframe containing info about hospitalization
    :param sex: sex query choice, values in ['0','1','2']
    :param date_query_start: the start of date query, a string passed from outside
    :param date_query: the end of date query, a string passed from outside
    :returns: a html file containing a bubble_map to describe the density of hospitalization spread among metropolitan France
    """
    date_query_start =date_query_start
    date_query = hosp_region.iloc[-1, 2] if date_query == 'no' else date_query  # latest update
    sex_query_label = {0: "All genders", 1: "Male", 2: "Female"}
    hosp_cleaned = hosp_region[(hosp_region["sex"] == int(sex)) & (hosp_region["date"] <= date_query) & (hosp_region["date"] >= date_query_start)]
    fig_bubblemap = px.scatter_mapbox(hosp_cleaned, lat="lat", lon="long",
                            hover_name="name_region", hover_data=["hosp"],
                            animation_frame="date",
                            size="hosp",size_max=80,
                            color="hosp",color_continuous_scale= px.colors.sequential.YlOrRd,
                            opacity = 0.85,
                            zoom=5, height=750,
                            title="Number of people currently hospitalized due to COVID-19 infection, by region, of "+ sex_query_label[int(sex)]+ ", from " +date_query_start+' to '+date_query)

    fig_bubblemap.update_layout(mapbox_style="open-street-map")
    fig_bubblemap.update_layout(margin={"r":50,"t":50,"l":50,"b":50})
    plotly.offline.plot(fig_bubblemap, filename="latest_hosp_bubble_map.html")



def Histogram(hosp_age_cleaned,start_date, date_query,region,regionfr):
    """Histogram: the hospitalization distributed by age group
    
    :param hosp_age_cleaned: processed dataframe containing info about distribution of hospitalization
    :param start_date: the start of date query, passed from outside
    :param date_query: the start of date query, a string passed from outside
    :param region: the end of date query, a string passed from outside
    :param regionfr: region query choice, values in keys of a predefined dictionary
    :returns: a html file containing a histogram
    """
    date_query=hosp_age_cleaned.iloc[-1, 2] if date_query == 'no' else date_query
    hosp_age_cleaned = hosp_age_cleaned[(hosp_age_cleaned["date"] >= start_date) &
                                        (hosp_age_cleaned["date"] <= date_query)
                                        & (hosp_age_cleaned["code_region"] == int(region))]
    fig_his = px.histogram(hosp_age_cleaned, x="cl_age90", y="hosp_age", nbins=10, color="cl_age90",
                           labels={"cl_age90": "Age", "hosp_age": "Daily number of newly hospitalized persons"},
                           color_discrete_sequence=px.colors.qualitative.Prism,
                           animation_frame="date",
                           opacity=0.9,
                           height=500,
                           title="Age distribution of daily newly hospitalized persons from " + start_date + " to " + date_query + " in " +regionfr[int(region)])
    plotly.offline.plot(fig_his, filename="latest_hosp_histogram.html")

