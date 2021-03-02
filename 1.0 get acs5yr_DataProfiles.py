import requests
import pandas as pd
import os

# ALL ACS API Documentation: https://www.census.gov/data/developers/data-sets/acs-5year.html

os.chdir(r'C:\Users\kylem\Dropbox\Frye_Parker_DataCollection\data\acs5yr')

# The keys are labels for file outputs, the values are correct "for" statement for each geo in the API
geoDict = {
    'US': 'us:*',
    'AIANNH': 'american indian area/alaska native area/hawaiian home land:*',
    'COUNTY' : 'county:*'
}

def make_apiRequest(geoNM, year, dataTable):
    print('Processing: ', dataTable, 'for ', geoNM)

    url = "http://api.census.gov/data/" + str(year) + "/acs/acs5/profile"

    # Add query parameters to the base url above.. requests package will handle the formatting (i.e. &)
    query = {
        'get': 'NAME,GEOCOMP,STATE,group(' + dataTable + ')',
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



# Make List of Data Tables to loop
dataTables = []
for i in range(2, 6):
    dataTables.append('DP0' + str(i))

#Make List of Years
years = [2010, 2012, 2014, 2018]

#Loop through all we need to make API REQUESTS to ACS
for geoKey, geoValue in geoDict.items():
    for dataTable in dataTables:
        for year in years:
            make_apiRequest(geoKey, year, dataTable)