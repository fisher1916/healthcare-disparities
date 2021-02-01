-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "census" (
    "county_name" VARCHAR(40)   NOT NULL,
    "state" VARCHAR(40)   NOT NULL,
    "state_abbr" VARCHAR(40)   NOT NULL,
    "household_median_income" INT   NOT NULL,
    "family_median_income" INT   NOT NULL,
    "total_population" INT   NOT NULL,
    "percent_poverty" NUMERIC   NOT NULL,
    "percent_veteran" NUMERIC   NOT NULL,
    "percent_married" NUMERIC   NOT NULL,
    "percent_bachelor" NUMERIC   NOT NULL,
    "percent_white" NUMERIC   NOT NULL,
    "percent_black" NUMERIC   NOT NULL,
    "percent_american_indian" NUMERIC   NOT NULL,
    "percent_asian" NUMERIC   NOT NULL,
    "percent_hawaiian" NUMERIC   NOT NULL,
    "percent_some_other" NUMERIC   NOT NULL,
    "percent_two_or_more" NUMERIC   NOT NULL,
    "state_code" VARCHAR(40)   NOT NULL,
    "county_code" VARCHAR(40)   NOT NULL,
    CONSTRAINT "pk_census" PRIMARY KEY (
        "county_name","state_abbr"
     )
);

CREATE TABLE "cms" (
    "cms_id"  SERIAL  NOT NULL,
    "facility_id" VARCHAR(40)   NOT NULL,
    "facility_name" VARCHAR(120)   NOT NULL,
    "address" VARCHAR(120)   NOT NULL,
    "city" VARCHAR(40)   NOT NULL,
    "state" VARCHAR(40)   NOT NULL,
    "zip_code" VARCHAR(40)   NOT NULL,
    "county_name" VARCHAR(120)   NOT NULL,
    "measure_id" VARCHAR(80)   NOT NULL,
    "measure_name" VARCHAR(120)   NOT NULL,
    "denominator" INT   NOT NULL,
    "score" NUMERIC   NOT NULL,
    "lower_estimate" NUMERIC   NOT NULL,
    "higher_estimate" NUMERIC   NOT NULL,
    "start_date" DATE   NOT NULL,
    "end_date" DATE   NOT NULL,
    CONSTRAINT "pk_cms" PRIMARY KEY (
        "cms_id"
     )
);

ALTER TABLE "cms" ADD CONSTRAINT "fk_cms_state_county_name" FOREIGN KEY("state", "county_name")
REFERENCES "census" ("state_abbr", "county_name");

