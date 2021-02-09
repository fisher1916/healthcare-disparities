# Healthcare Disparities

- Healthcare Disparities tackles the question: Is there a correlation between demographics of race and rural/urban, and specific treatable healthcare conditions in hospitals across the United States? Data is collected from U.S. Census Bureau 2019 (include link), and CMS data from hospitals across the country (include link).

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

Health conditions: COPD - Heart failure - Pneumonia - Heart attack <br>

-
