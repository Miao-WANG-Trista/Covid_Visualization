"""the main module to realize all basic interactivity by input() function, corresponding data cleaning & graph plotting"""

import datacleaning
import charts
from raise_error import DateError_total,out_of_range_error
import raise_error


regionfr = {0:'France',11:"Île-de-France", 24: "Centre-Val de Loire",
           27:"Bourgogne-Franche-Comté", 28:"Normandie",
           32:"Hauts-de-France", 44:"Grand Est",
           52:"Pays de la Loire", 53:"Bretagne",
           75:"Nouvelle-Aquitaine", 76:"Occitanie",
           84:" Auvergne-Rhône-Alpes",93:"Provence-Alpes-Côte d'Azur",
           94:"Corse" }
alert='Please use the format YYYY-MM-DD'
geo=datacleaning.geodata()


def main():
    #first step is to choose indicator, different choices lead to different following steps
    i=input('Which indicator would you like to know? 1. Total cases 2.Daily cases 3.Hospitalization')
    if i not in ['1','2','3']:
        raise out_of_range_error(i)

    if i=='1':
        #to look at total cases
        start_date = input('Which date do you want to look at as the start?'+alert)
        raise_error.invalid_input(start_date)
        if start_date< '2020-03-20':
           raise DateError_total(start_date)
        end_date = input('Which date do you want to look at as the end? if you enter ''no'',the default choice is the latest '+alert)
        if end_date !='no':
            raise_error.invalid_input(end_date)
        totalcases = datacleaning.total_case()
        return charts.bar_chart(totalcases, start_date, end_date)

    elif i=='3':
        #to look at hospitalization
        sex=input('Which gender do you particulary want to look at? 1 is male, 2 is female, 0 is total')
        if sex not in ['1','2','0']:
            raise ValueError ('you must choose 1/2/0')
        print('Which region are you more interested in?')
        for key, value in regionfr.items():
            print(str(key) + " =>" + value)
        region=input('What"s your choice for region?')
        if region not in['11','24','27','28','32','44','52','53','75','76','84','93','94']:
            raise out_of_range_error(region)
        start_date = input('Which date do you want to look at as the start?'+alert)
        raise_error.invalid_input(start_date)
        if start_date < '2020-03-18':
            raise DateError_total(start_date)
        date_query=input('Which date do you want to look at as the end? if you enter ''no'',the default choice is the latest'+alert)
        hospdata=datacleaning.hosp_data(geo)
        hosp_age_cleaned=datacleaning.hosp_age()
        return charts.Bubble_map(hospdata, sex, start_date, date_query), charts.Histogram(hosp_age_cleaned, start_date, date_query, region, regionfr)

    else :
        #to look at daily cases
        sex = input('Which gender do you particulary want to look at? 1 is male, 2 is female, 0 is total')
        print('Which region do you want to look at? if you enter "0", you will request the sum')
        for key, value in regionfr.items():
            print(str(key) + " =>" + value)
        region = input("What's your choice for region?")
        if region not in ['0','11', '24', '27', '28', '32', '44', '52', '53', '75', '76', '84', '93', '94']:
            raise out_of_range_error(region)
        region_chosen=regionfr[int(region)]
        start_date = input('Which date do you want to look at as the start?'+alert)
        if start_date < '2020-03-10':
            raise DateError_total(start_date)
        end_date = input('Which date do you want to look at as the end? if you enter ''no'',the default choice is the latest'+alert)
        dailydata=datacleaning.daily_case(geo)
        return charts.line_chart(dailydata, sex, region_chosen, start_date, end_date)

if __name__ == '__main__':
    main()
