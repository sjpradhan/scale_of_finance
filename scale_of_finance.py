import pandas as pd
import streamlit as st


def main():


    profile_icon = "https://raw.githubusercontent.com/sjpradhan/scale_of_finance/master/salary.png"

    st.set_page_config(page_title="SOF-Upload",page_icon = profile_icon)

    st.header(":rainbow[Upload Scale Of Finance Excel File] 💾")

    col1, col2 = st.columns(2)

    with col1:
        # File uploader
        uploaded_file = st.file_uploader(":orange[Choose an Excel file] 📁", type=["xlsx", "xls"])

    try:
        if uploaded_file is not None:

            def read_from_uploaded_file ():
                df = pd.read_excel(uploaded_file)
                df['SOF Amount'].fillna(0, inplace=True)
                df['Numeric Value of Area Unit'] = 1
                return df
            df = read_from_uploaded_file ()
    except Exception as e:
        st.error("Wrong file, please upload appropriate file with correct header.")
    else:
        st.write("Please upload file to get insight ⚡")

    try:
        unique_state_name = pd.DataFrame(df['State Name'].unique(),columns= ['State Name'])
        st.write(":orange[Raw Data Preview Of:]",unique_state_name,df.head(5))
    except:
        pass

    try:
        try:
            df = df[
                ['District Name', 'District LGD Code', 'Agroclimatic Zone (Select from dropdown)',
                 'Crop Season (Select from dropdown)', 'Land Type (Select from dropdown)',
                 'Area Unit (Select form dropdown)', 'Numeric Value of Area Unit',
                 'Crop Type (Select from dropdown)', 'Crop Name in English', 'Crop Name in Local Language',
                 'SOF Amount']] \
                .rename(columns={'District Name': 'District',
                                 'District LGD Code': 'District Code',
                                 'Agroclimatic Zone (Select from dropdown)': 'Agroclimatic Zone',
                                 'Crop Season (Select from dropdown)': 'Cropping Season',
                                 'Land Type (Select from dropdown)': 'Land Type',
                                 'Area Unit (Select form dropdown)': 'Area Unit Type',
                                 'Numeric Value of Area Unit': 'Area of Unit',
                                 'Crop Type (Select from dropdown)': 'Crop Type',
                                 'Crop Name in English': 'Crop Name',
                                 'Crop Name in Local Language': 'Crop Name Local Language',
                                 'SOF Amount': 'Scale of Finance In Rs'
                                 })
        except Exception as e:
            print(f"error while resetting columns", {e})

        st.write("Total Number Of Records", df.shape)

        zero_rs = df[df['Scale of Finance In Rs'] == 0]
        st.write('Scale of Finance In Rs(Column) Contain 0', zero_rs.shape)

        df = df[df['Scale of Finance In Rs'] != 0]
        st.write("Scale of Finance In Rs(Column) does not Contain 0", df.shape)

        st.markdown(":blue[__Desired Output:__]")
        st.dataframe(df)

        st.divider()

        st.markdown("__:blue[Blank Values in Dataset:]__")
        st.write(df.isnull().sum().to_frame(name='Blank Values').transpose())

        blank_value_position = df[df[['District', 'District Code', 'Agroclimatic Zone', 'Cropping Season',
                                             'Land Type', 'Area Unit Type', 'Area of Unit', 'Crop Type', 'Crop Name',
                                             'Crop Name Local Language', 'Scale of Finance In Rs']].isnull().any(axis=1)]
        st.dataframe(blank_value_position)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("__:blue[District Name & District Code:]__")
            unique_distrcts = df.groupby(['District', 'District Code']).count().reset_index()
            unique_distrcts = unique_distrcts[['District', 'District Code']]
            st.table(unique_distrcts)
            st.write(":orange[Total Number Of Unique Districts]", unique_distrcts.shape)


        with col2:
            @st.cache_data
            def load_district_data():
                district_url = "https://media.githubusercontent.com/media/sjpradhan/lgd_hierarchy/main/Data/District%20Details.csv"
                district_df = pd.read_csv(district_url)

                district_df = district_df[
                    ["District LGD Code", "District Name (In English)", "District Name (In Local language)",
                     "Hierarchy", "Short Name of District", "Census2011 Code", "Pesa Status"]]

                return district_df

            district_df = load_district_data()

            search_term = st.text_input(":blue[Search by :green[District]/:orange[Code:]]🔎", "")

            # Filter based on District Name & it's LGD code
            if search_term:
                filtered_records = district_df[
                    district_df['District Name (In English)'].str.contains(search_term, case=False) |
                    district_df['District LGD Code'].astype(str).str.contains(search_term) |
                    district_df['Hierarchy'].str.contains(search_term, case=False)
                    ]

                # If there is invalid search it will show no matching found
                if not filtered_records.empty:
                    st.write(":blue[Filtered results:]", filtered_records.shape)
                    st.write(filtered_records)
                else:
                    st.write(":red[Opps! No matching results found.]🤦‍♂️")


        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            data = ["North Eastern Transition Zone (ACZ-1)",
                    "North Eastern Dry Zone (ACZ-2)",
                    "North Eastern Zone (ACZ-3)",
                    "Central Dry Zone (ACZ-4)",
                    "Eastern Dry Zone (ACZ-5)",
                    "Southern Dry Zone (ACZ-6)",
                    "Southern Transition Zone (ACZ-7)",
                    "North Transition Zone (ACZ-8)",
                    "Hilly Zone (ACZ-9)",
                    "Coastal Zone (ACZ-10)",
                    "Any",
                    "North Eastern zone",
                    "North Western zone",
                    "Western zone",
                    "Cauvery delta zone",
                    "Southern zone",
                    "High rainfall zone",
                    "Hill and high altitude zone",
                    ]
            actuale_agroclimate_zone = pd.DataFrame(data, columns=["Actual Agroclimatic Zone"])
            st.table(actuale_agroclimate_zone)

        with col2:
            unique_agroclimatic_zone = pd.DataFrame(df['Agroclimatic Zone'].unique(),columns=  ['Agroclimatic Zone'])
            st.table(unique_agroclimatic_zone)

        col1, col2 = st.columns(2)
        with col1:
            data = ["Rabi Crop (Nov-February)","Kharif Crop (July-Oct)","Summer Crop (March-June)",
                    "Perennial Crop (Annual Crop)","Any Season Crop","Any",
                    ]
            actuale_cropping_season = pd.DataFrame(data,columns = ['Actual Cropping Season'])
            st.table(actuale_cropping_season)

        with col2:
            unique_crop_season = pd.DataFrame(df['Cropping Season'].unique(),columns= ['Cropping Season'])
            st.table(unique_crop_season)

        col1, col2,col3,col4 = st.columns(4)

        with col1:
            data = ["Irrigated Land","Un-Irrigated Land","Any",
                    ]
            actuale_land_type = pd.DataFrame(data,columns = ['Actual Land Type'])
            st.table(actuale_land_type)

        with col2:
            unique_land_type = pd.DataFrame(df['Land Type'].unique(),columns= ['Land Type'])
            st.table(unique_land_type)

        with col3:
            data = ["Square Feet","Square Meter","Square Yard","Hectare","Bhigha","Acre","Guntha","Ground","Biswa",
                "Kanal","Are","Cent",
                    ]
            actuale_area_unit_type = pd.DataFrame(data,columns = ["Actual Area Unit Type"])
            st.table(actuale_area_unit_type)

        with col4:
            unique_area_unit_type = pd.DataFrame(df['Area Unit Type'].unique(),columns=["Area Unit Type"])
            st.table(unique_area_unit_type)

        col1,col2 = st.columns(2)

        with col1 :
            data = ["Cereals","Seed","Pulses","Fruits","Vegetable","Spices","Feed & Forage",
                    "Oil Seed","Ornamental","Industrial/Commercial/Cash English","Sericulture",
                    "Medicinal/Herbs","Mix Crop","Inter Crop","Any","Floriculture","Millet"
                    ]
            actual_crop_type = pd.DataFrame(data, columns = ['Actual Crop Type'])
            st.table(actual_crop_type)

        with col2 :
            unique_crop_type = pd.DataFrame(df['Crop Type'].unique(), columns= ['Crop Type'])
            st.table(unique_crop_type)
    except:
        pass

if __name__ == "__main__":
    main()
