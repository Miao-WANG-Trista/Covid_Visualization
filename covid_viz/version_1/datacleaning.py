# %% Import and clean data
import pandas as pd

def geodata():
    df_geo = pd.read_csv("departements_france_long_lat.csv")
    df_geo = df_geo.rename(columns={"code_departement": "dep",
                                    "nom_departement": "name_dep",
                                        "nom_region" : "name_region" })
    return df_geo



#total confirmed cases data
def total_case():
    conf = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/d3a98a30-893f-47f7-96c5-2f4bcaaa0d71")
    conf = conf.rename(columns={"total_cas_confirmes": "Total confirmed cases"})
    conf = conf.iloc[:,0:2]  # extract total confirmed cases
    return conf



#daily positive case data
def daily_case(df_geo):
    # combine data resources from two links so that we can unify the date range
    # data before 05/13
    dailycaseold = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/b4ea7b4b-b7d1-4885-a099-71852291ff20', sep=";",header=0)
    # data after 05/13
    dailycase = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/001aca18-df6a-45c8-89e6-f82d689e6c01", sep=";", header = 0)
    dailydeath = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/6fadff46-9efd-4c53-942a-54aca783c30c', sep=";", header=0)
    
    dailycase = dailycase.rename(columns={"reg":"code_region","jour": "Date",
                                          "P_f": "Female","P_h": "Male","P": "Daily Total"})

    dailycaseold = dailycaseold.drop(columns=["nb_test", "nb_test_h", "nb_test_f"])
    dailycaseold = dailycaseold[(dailycaseold["clage_covid"] == '0')]
    dailycaseold = dailycaseold.rename(columns={'jour': 'Date', 'clage_covid': 'cl_age90',
                                                'nb_pos': 'Daily Total', 'nb_pos_h': 'Male', 'nb_pos_f': 'Female'})

    # modify the code region from 1 to 01 so we can perform merge
    dep2 = df_geo.dep.str.len() < 2
    df_geo.dep[dep2].str.zfill(2)
    
    # merge code region with dataframe, remove useless information and group by region.
    dailycaseold = pd.merge(dailycaseold,df_geo,on='dep')
    dailycaseold = dailycaseold.iloc[:, 1:9]
    dailycaseold = dailycaseold.groupby(["Date", "code_region", 'name_region'],as_index=False)[["Daily Total", "Male", "Female"]].sum()
    dailycaseold = dailycaseold[dailycaseold.Date < '2020-05-13'] 
    
    # process daily death data
    dailydeath = dailydeath.drop(columns=["incid_hosp", "incid_rea", "incid_rad"])
    dailydeath = dailydeath.rename(columns={'jour': 'Date', 'incid_dc': 'Daily death'})
    dailydeath = pd.merge(dailydeath,df_geo, on='dep',how='left')
    dailydeath = dailydeath.groupby(["Date", "code_region"],as_index=False)["Daily death"].sum()

    # keep only daily postive cases(delete colunms for number of tests conducted)
    dailycase = dailycase.drop(columns=["T_f", "T_h", "T"])

    # select total daily case for all-age group (code 0)
    dailycase = dailycase[(dailycase["cl_age90"] == 0)]

    # merge daily positive data with geo data (assign region names)
    df_geo2 = df_geo.iloc[:, 2:4]
    df_geo2 = df_geo2.drop_duplicates('name_region')
    dailycase_region = pd.merge(dailycase, df_geo2, on="code_region", how="left")
    dailycase_region["name_region"].fillna("Overseas", inplace=True)

    # combine all dates
    dailycase_region = pd.concat([dailycase_region, dailycaseold])
    dailycase_region = pd.merge(dailycase_region,dailydeath,left_on=["code_region", "Date"], right_on=["code_region", "Date"])

    # calculate daily confirmed cases in France
    dailycase_total = dailycase_region.groupby(by=["Date"]).sum().reset_index()
    dailycase_total["name_region"] = "France"

    # combine the regions and total together
    dailycase_cleaned = pd.concat([dailycase_total, dailycase_region])
    dailycase_cleaned = dailycase_cleaned.drop(columns=['cl_age90'])

    ## keep only metropolitan France(drop DROM(1, 2, 3,4,6 ))
    dailycase_cleaned.drop(dailycase_cleaned[dailycase_cleaned.code_region < 10].index)
    dailycase_cleaned.sort_values(by="Date", inplace=True)
    return dailycase_cleaned



# hospitalization data
def hosp_data(df_geo):
    df = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/63352e38-d353-4b54-bfd1-f1b3ee1cabd7", sep = ";", header = 0)
    df = df.rename(columns={"jour": "date", "sexe": "sex"})

    # keep only metropolitan France(drop outre-mer DROM("971", "972", "973", "974", "976"))
    hosp_cleaned = df.drop(df[df.dep > "970"].index)

    # keep only colunms of number people currently hosipitalized(delete colunms for intesive care, returned home and deaths at hosiptal)
    hosp_cleaned = hosp_cleaned.loc[:,["dep","sex","date","hosp"]]

    # merge hospital data and geodata, group by regions
    hosp_temp = pd.merge(df_geo, hosp_cleaned)
    hosp_region = hosp_temp.groupby(["code_region","name_region", "date","long", "lat", "sex"],
                                    as_index=False)["hosp"].sum()
    return hosp_region



#hospitalization by age group
def hosp_age():
    df1 = pd.read_csv("https://www.data.gouv.fr/fr/datasets/r/08c18e08-6780-452d-9b8c-ae244ad529b3", sep=";", header=0)
    df1 = df1.rename(columns={"reg": "code_region", "jour": "date", "hosp": "hosp_age"})

    hosp_age_cleaned = df1.drop(df1[df1.cl_age90 == 0].index) #to delete the 'sum' column
    hosp_age_cleaned = hosp_age_cleaned.loc[:, ["code_region", "cl_age90", "date", "hosp_age"]]
    return hosp_age_cleaned
