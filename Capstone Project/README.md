# Udacity Data Engineering

## Capstone Project

### Instructions
- Scope the Project and Gather Data
- Explore and Assess the Data
- Define the Data Model
- Run ETL to Model the Data
- Complete Project Write Up

### Datasets 
- I94 Immigration Data: This data comes from the US National Tourism and Trade Office. A data dictionary is included in the workspace. [This](https://travel.trade.gov/research/reports/i94/historical/2016.html) is where the data comes from. There's a sample file so you can take a look at the data in csv format before reading it all in. You do not have to use the entire dataset, just use what you need to accomplish the goal you set at the beginning of the project.
- World Temperature Data: This dataset came from Kaggle. You can read more about it [here](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data).
- U.S. City Demographic Data: This data comes from OpenSoft. You can read more about it [here](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/).
- Airport Code Table: This is a simple table of airport codes and corresponding cities. It comes from [here](https://datahub.io/core/airport-codes#data).

### Data Model

- DIMENSIONS:
    - DIM AIRPORTS - iata_code, name, type, local_code, iso_country, municipality, coordinates, port_city
    - DIM DEMOGRAPHICS - City,State,Median Age,Male Population,Female Population,Total Population,Number of Veterans,Foreign-born,Average Household Size,StateCode,Race,Count
    - DIM TEMPERATURE - dt,AverageTemperature,AverageTemperatureUncertainty,City,Country,Latitude,Longitude
- FACTS:
    - FACT IMMIGRATIONS - cicid,i94yr,i94mon,i94cit,i94res,i94port,arrdate,i94mode,i94addr,depdate,i94bir,i94visa,count,dtadfile,visapost,occup,entdepa,entdepd,entdepu,matflag,biryear,dtaddto,gender,insnum,airline,admnum,fltno,visatype

![Model](modelcapstone.png)
