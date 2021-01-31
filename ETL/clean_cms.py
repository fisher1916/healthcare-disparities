import pandas as pd


def scrub_cms_data():

    print("<< Starting cms processing... >>")

    # The path to our CSV file
    input_file = "Resources/cms_data_2.csv"
    output_file = "ETL-Results/four_mort_measures.csv"

    print(f"reading cms cms file {input_file}...")
    df = pd.read_csv(input_file)

    print("cleaning up cms data")
    # Extract 'Facility ID', 'Facility Name', 'Address City','State', 'ZIP Code', 'County Name',
    CMS_df = df.loc[:, ['Facility ID', 'Facility Name', 'Address', 'City', 'State', 'ZIP Code',
                        'County Name', 'Measure ID', 'Measure Name',
                        'Denominator', 'Score', 'Lower Estimate',
                        'Higher Estimate', 'Start Date', 'End Date']]

    # filter out hospitals with not available in score column
    cms_df_na = CMS_df[CMS_df["Score"] != "Not Available"]

    # reset index
    cms_df_reset = cms_df_na.reset_index(drop=True)

    # filter out COMP_HIP_KNEE measure
    cms_df_m = cms_df_reset[cms_df_reset["Measure ID"] != "COMP_HIP_KNEE"]

    # filter out MORT_30_CABG measure
    cms_df_n = cms_df_m[cms_df_m["Measure ID"] != "MORT_30_CABG"]

    # filter out PSI_10_POST_KIDNEY measure
    cms_df_p = cms_df_n[cms_df_n["Measure ID"] != "PSI_10_POST_KIDNEY"]

    # filter out PSI_11_POST_RESP measure
    cms_df_r = cms_df_p[cms_df_p["Measure ID"] != "PSI_11_POST_RESP"]

    # filter out PSI_12_POSTOP_PULMEMB_DVT measure
    cms_df_s = cms_df_r[cms_df_r["Measure ID"] != "PSI_12_POSTOP_PULMEMB_DVT"]

    # filter out PSI_13_POST_SEPSIS measure
    cms_df_t = cms_df_s[cms_df_s["Measure ID"] != "PSI_13_POST_SEPSIS"]

    # filter out PSI_14_POSTOP_DEHIS measure
    cms_df_v = cms_df_t[cms_df_t["Measure ID"] != "PSI_14_POSTOP_DEHIS"]

    # filter out PSI_15_ACC_LAC measure
    cms_df_w = cms_df_v[cms_df_v["Measure ID"] != "PSI_15_ACC_LAC"]

    # filter out PSI_3_ULCER measure
    cms_df_x = cms_df_w[cms_df_w["Measure ID"] != "PSI_3_ULCER"]

    # filter out PSI_4_SURG_COMP measure
    cms_df_y = cms_df_x[cms_df_x["Measure ID"] != "PSI_4_SURG_COMP"]

    # filter out PSI_6_IAT_PTX measure
    cms_df_z = cms_df_y[cms_df_y["Measure ID"] != "PSI_6_IAT_PTX"]

    # filter out PSI_8_POST_HIP measure
    cms_df_d = cms_df_z[cms_df_z["Measure ID"] != "PSI_8_POST_HIP"]

    # filter out PSI_90_SAFETY measure
    cms_df_e = cms_df_d[cms_df_d["Measure ID"] != "PSI_90_SAFETY"]

    # filter out PSI_9_POST_HEM measure
    cms_df_f = cms_df_e[cms_df_e["Measure ID"] != "PSI_9_POST_HEM"]

    # filter out mort_30_stk measure
    cms_df_g = cms_df_f[cms_df_f["Measure ID"] != "MORT_30_STK"]

    # reset index
    cms_df_mort = cms_df_g.reset_index(drop=True)

    print(f"writing cleaned cms file to {output_file}")

    # Added clean csv to resources folder
    cms_df_mort.to_csv(output_file, index=False, header=True)

    print("<< Completed cms processing... >>")
