import pandas as pd
from api_key import key
import requests
import us
import os


#
# Scrub county column as it has too much in the string
# Split to County, State
#


def county_split(x):
    if " Census Area, " in x:
        return x.split(" Census Area, ")
    elif " Parish, " in x:
        return x.split(" Parish, ")
    elif " County, " in x:
        return x.split(" County, ")
    else:
        return x.split(", ")

#
# Based on state name get two letter abbreviation for state
#


def state_abbr(x):
    return us.states.lookup(x).abbr


#
# Process the census data
#


def census_data_api_extract():

    print("<< Starting census api processing... >>")

    fips_state_codes = "ETL-Results/fips_state_codes.csv"
    output_file = "ETL-Results/census_data.csv"

    # Check to see if file exists double check they want to run?
    if (os.path.exists(output_file)):

        # Ask if they want to continue processing
        print(f"\nWARNING: {output_file} file already exists")
        run = input("File already exists, do you want to run the API? (Y/N): ")
        print("\n")

        # If not return immediately
        if run != 'Y':
            print("<< Completed census api processing... >>")
            return

    # Start processing
    # print("fetching fips state codes")

    # Read codes into a pandas dataframe
    # states = pd.read_csv(fips_state_codes, dtype=str)

    # Prepare the target output dataframe
    columns = {
        "County",
        "Household Median Income",
        "Family's Median Income",
        "Total Population",
        "Percent Poverty",
        "Percent Veteran",
        "Percent Married",
        "Percent Bachelor",
        "State Code",
        "County Code",
    }
    census_df = pd.DataFrame(columns=columns)

    # Value Mappings
    # refer to: https://api.census.gov/data/2019/acs/acs5/subject/variables.html
    # NAME = County Name
    # S1903_C03_001E = Household Median Income
    # S1903_C03_015E = Family Median Income
    # S0101_C01_001E = Total Population
    # S1701_C03_001E = Percent Poverty
    # S2101_C04_001E = Percent Veteran
    # S1201_C02_001E = Percent Married
    # S1501_C02_015E = Percent Bachelor
    fetchColumns = \
        "NAME," + \
        "S1903_C03_001E," + \
        "S1903_C03_015E," + \
        "S0101_C01_001E," + \
        "S1701_C03_001E," + \
        "S2101_C04_001E," + \
        "S1201_C02_001E," + \
        "S1501_C02_015E"

    print("start calling census API")

    # Loop through each state extracting the state info
    # for state in states["FIPS State Numeric Code"].tolist():

    # Build the URL for the API call
    url = f"https://api.census.gov/data/2019/acs/acs5/subject?get={fetchColumns}&for=county&in=state:*&in=county:*&key={key}"

    #print(f"fetching census data for state: {state}")

    # Get the response back from the API
    response = requests.get(url).json()

    print("got a response from the census API, begin processing")

    # Loop through the response appended to the end of the dataframe
    # Skip the first results as it is an info record
    for i in range(1, len(response)):
        new_row = {
            "County": response[i][0],
            "Household Median Income": response[i][1],
            "Family's Median Income": response[i][2],
            "Total Population": response[i][3],
            "Percent Poverty": response[i][4],
            "Percent Veteran": response[i][5],
            "Percent Married": response[i][6],
            "Percent Bachelor": response[i][7],
            "State Code": response[i][8],
            "County Code": response[i][9],
        }
        census_df = census_df.append(new_row, ignore_index=True)

    print("completed calling census API")

    print("scrubbing census data for county and state")

    # Split and return the list of County and State
    census_df["County_State"] = census_df.loc[:, "County"].apply(county_split)

    # Take the list from County_State column and make then separate columns in
    # the dataframe
    census_df[["County Name", "State"]] = pd.DataFrame(
        census_df["County_State"].tolist(), index=census_df.index)

    # Rearrange columns for output file
    census_df = census_df[["County Name", "State", "Household Median Income",
                           "Family's Median Income", "Total Population",
                           "Percent Poverty", "Percent Veteran",
                           "Percent Married", "Percent Bachelor",
                           "State Code", "County Code"]]

    # Get the two letter state abbreviations
    census_df["State Abbr"] = census_df["State"].apply(state_abbr)
    census_df['County Name'] = census_df['County Name'].str.upper()

    # Dump Puerto Rico
    census_df = census_df[census_df["State Abbr"] != "PR"]

    print(f"writing the census data to {output_file}")

    # Write census data to file
    census_df.to_csv(output_file, index=False, header=True)

    # Value Mappings
    # refer to: https://api.census.gov/data/2019/acs/acs5/profile/groups/DP05.html
    # NAME = County Name
    # DP05_0037E = White
    # DP05_0038E = Family Median Income
    # DP05_0039E = Total Population
    # DP05_0044E = Percent Poverty
    # DP05_0052E = Percent Veteran
    # DP05_0057E = Percent Married
    fetchColumns = \
        "NAME," + \
        "DP05_0037E," + \
        "DP05_0038E," + \
        "DP05_0039E," + \
        "DP05_0044E," + \
        "DP05_0052E," + \
        "DP05_0057E"

    url = "https://api.census.gov/data/2019/acs/acs5/profile?get={fetchColumns}&for=county:*&in=state:*&key={key}"

    print("<< Completed census api processing... >>")
