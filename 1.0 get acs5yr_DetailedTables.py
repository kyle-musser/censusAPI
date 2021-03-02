import requests
import pandas as pd
import os

os.chdir(r'C:\Users\kylem\Dropbox\Frye_Parker_DataCollection\data\acs5yr')

# The keys are labels for file outputs, the values are correct "for" statement for each geo in the API
geoDict = {
    'US': 'us:*',
    'AIANNH': 'american indian area/alaska native area/hawaiian home land:*',
    'COUNTY' : 'county:*'
}



def make_apiRequest(geoNM, year, dataTable):
    print('Processing: ', dataTable, 'for ', geoNM, year)

    url = "http://api.census.gov/data/" + str(year) + "/acs/acs5"

    # Add query parameters to the base url above.. requests package will handle the formatting (i.e. &s in between)
    query = {
        'get': 'NAME,GEO_ID,GEOCOMP,STATE,group(' + dataTable + ')',
        'for': geoDict[geoNM],
        'key': 'c07720f2877c95a64c5ac82a0cbaac48cf87332d'
    }

    try:
        r = requests.get(url, params=query)
        print(str(r.url))
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    #Get JSON Data from API Request into Pandas to save
    data = pd.read_json(r.content)

    saveNM = dataTable + "_" + geoNM + "_" + str(year) + ".csv"
    data.to_csv(saveNM, header=False, index=False)




# ACS Detailed Tables we want
# The List of all is here: https://api.census.gov/data/2018/acs/acs5/groups.html
dataTables = [
    'B16001',
    'B17001', 'B17001A', 'B17001B', 'B17001C', 'B17001D', 'B17001I',
    'B19013', 'B19013A', 'B19013B', 'B19013C', 'B19013D', 'B19013I',
    'B19083',
    'B19113', 'B19113A', 'B19113B', 'B19113C', 'B19113D', 'B19113I',
    'B19301', 'B19301A', 'B19301B', 'B19301C', 'B19301D', 'B19301I',
              'B22005A', 'B22005B', 'B22005C', 'B22005D', 'B22005I',
    'B25003', 'B25003A', 'B25003B', 'B25003C', 'B25003D', 'B25003I',
              'B28009A', 'B28009B', 'B28009C', 'B28009D', 'B28009I',
              'C15002A', 'C15002B', 'C15002C', 'C15002D', 'C15002I',
              'C27001A', 'C27001B', 'C27001C', 'C27001D', 'C27001I',
]


#Make List of Years
years = [2010, 2012, 2014, 2018]
years = [2010]

#Loop through all we need to make API REQUESTS to ACS
for geoKey, geoValue in geoDict.items():
    for dataTable in dataTables:
        for year in years:

            # Need some exceptions for tables that dont appear in each year
            if dataTable[0:6] == 'B28009' and year <= 2014:
                continue

            if dataTable[0:6] == 'C27001' and year == 2010:
                continue

            make_apiRequest(geoKey, year, dataTable)