# Healthcare Disparities

- Healthcare Disparities tackles the question: Is there a correlation between demographics of race and rural/urban, and specific treatable healthcare conditions in hospitals across the United States? Data is collected from U.S. Census Bureau 2019 (https://www.census.gov/data/developers/data-sets.html), and CMS data from hospitals across the country (https://data.cms.gov/provider-data/search?theme=Hospitals).

Health conditions Considered: 
  - COPD mortality
  - Heart failure mortality
  - Pneumonia mortality
  - Heart attack mortality

## Files

[`app.py`](app.py) - contains database queries and API end points for the visualization

[`index.html`](template/index.html) - the html file containing the visualizations

[`logic.js`](static/js/logic.js) - The main logic file that contains the bar charts, histograms and interactivity

[`maps.js`](static/js/maps.js) - The logic that initializes the map and handles the map controls

[`style.css`](static/css/style.css) - The styles beyond bootstrap required for various positioning and text manipulations

[`cms.db`](static/data) - The sqlite database for the project

[`Race_vs_Health_Conditions.ipynb`](Analysis/Race_vs_Health_Conditions.ipynb) - This shows analysis of white vs black/african american demographics

[`Rural_urban_df.ipynb`](Analysis/Rural_urban_df.ipynb) - This shows analysis of Urban vs Rural american demographics

[`General_Demo_Analysis.ipynb`](Analysis/General_Demo_Analysis.ipynb) - This shows analysis on other demographic data

[`Untitled.ipynb`](Analysis/Unititled.ipynb) - FIPS county and state code latitude and longitude experimental discovery

[ETL](ETL/) - Directory where database prep code is carried over from last project, does csv cleansing and screen scraping (pandas)

[`load_data.ipynb`](ETL/load_data.ipynb) - Final scrub, database table creation and insertion into a sqlite database [`cms.db`](static/data)

[ETL/ETL-Results](ETL/ETL-Results) - Directory where final versions of csv files are for ETL process, sources csv's for the [`load_data.ipynb`](ETL/load_data.ipynb)

## Results
(screenshots of graphs here)

## Execution

1. The assumption is that you have a working Python 3.6 environment and:

   - Jupyter Notebook 6.1.4 (If you want to explore any of the notebooks)
   - Flask 1.1.2
   - SQLAlchemy 1.3.17

1. Clone the [git repository](https://github.com/fisher1916/healthcare-disparities) for this project
1. Change into the repository directory
1. Execute the `app.py` file by typing `python app.py`
1. Open up a browser and go to http://localhost:5000/

## Conclusion
There are some indications that point to some correlation in some disease categories. Due to the fact that the data is only looking at Medicare patients over the age of 65, and that some of the urban rural data may need further refinement, more analysis is recommended.

## Sources
1. Census - Race Data:

 - https://api.census.gov/data/2019/acs/acs5/profile?get={fetchColumns}&for=county:*&in=state:*&key={key}
 - https://api.census.gov/data/2019/acs/acs5/profile/groups/DP05.html
 
2. Census - Population/Income Data:

 - https://api.census.gov/data/2019/acs/acs5/subject?get={fetchColumns}&for=county&in=state:*&in=county:*&key={key}
 - https://api.census.gov/data/2019/acs/acs5/subject/variables.html
 
3. https://data.cms.gov/provider-data/search?theme=Hospitals

4. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5918944/

5. https://www.healthcare.gov/glossary/affordable-care-act/

## Authors

Made by Erica, Jenny, Josh(https://www.linkedin.com/in/josh-gonzalez-williams-7aa9a31b0/), [Jay](https://www.linkedin.com/in/jay-hastings-techy/) with :heart: in 2021.
