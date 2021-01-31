import pandas as pd


def extract_codes():

    print("<< Starting fips state codes processing... >>")

    output_file = "ETL-Results/fips_state_codes.csv"

    # URL for HTML page that contains the FIPS state codes
    url = 'https://www.census.gov/library/reference/code-lists/ansi.html'

    print("reading fips state codes from source web page...")

    # Grab all the codes from the HTML and put into pandas dataframe
    tables = pd.read_html(url)

    # Table 6 is the codes we need
    table_df = tables[6]

    print("cleaning fips state codes...")

    # Convert the FIPS State Numeric Code to a String for later use in APIs.
    table_df['FIPS State Numeric Code'] = table_df['FIPS State Numeric Code'].values.astype(
        str)

    # Pad 1 character digits with a zero
    table_df['FIPS State Numeric Code'] = table_df['FIPS State Numeric Code'].str.zfill(
        2)

    print(f"writing fips state codes to {output_file}...")
    table_df.to_csv(output_file, index=False)

    print("<< Completed fips state codes processing... >>")
