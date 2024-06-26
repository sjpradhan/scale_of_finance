import pandas as pd
import streamlit as st


def main():


    profile_icon = "https://raw.githubusercontent.com/sjpradhan/scale_of_finance/master/salary.png"

    st.set_page_config(page_title="SOF-Upload",page_icon = profile_icon)

    st.header("Upload Scale Of Finance Excel File 💾")

    col1, col2 = st.columns(2)

    with col1:
        # File uploader
        uploaded_file = st.file_uploader("Choose an Excel file 📁", type=["xlsx", "xls"])

    if uploaded_file is not None:
        def read_from_uploaded_file ():
            df = pd.read_excel(uploaded_file)
            df['SOF Amount'].fillna(0, inplace=True)
            return df
        df = read_from_uploaded_file ()
    else:
        st.write("Please upload file to get insight ⚡")

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

        st.write("File Content:")
        st.dataframe(df)

        st.divider()

        st.write("Blank Values in Dataset:")
        st.write(df.isnull().sum().to_frame(name='Blank Values').transpose())

        blank_value_position = df[df[['District', 'District Code', 'Agroclimatic Zone', 'Cropping Season',
                                             'Land Type', 'Area Unit Type', 'Area of Unit', 'Crop Type', 'Crop Name',
                                             'Crop Name Local Language', 'Scale of Finance In Rs']].isnull().any(axis=1)]
        st.dataframe(blank_value_position)

        col1, col2 = st.columns(2)

        with col1:
            st.write("District Name & District Code")
            unique_distrcts = df.groupby(['District', 'District Code']).count().reset_index()
            unique_distrcts = unique_distrcts[['District', 'District Code']]
            st.table(unique_distrcts)
            st.write("Total Number Of Unique Districts", unique_distrcts.shape)


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
        col1,col2,col3 = st.columns(3)

        with col1:
            unique_agroclimatic_zone = pd.DataFrame(df['Agroclimatic Zone'].unique(),columns=  ['Agroclimatic Zone'])
            st.table(unique_agroclimatic_zone)

        with col2:
            unique_crop_season = pd.DataFrame(df['Cropping Season'].unique(),columns= ['Cropping Season'])
            st.table(unique_crop_season)

        with col3:
            unique_land_type = pd.DataFrame(df['Land Type'].unique(),columns= ['Land Type'])
            st.table(unique_land_type)

        st.divider()
        col1,col2,col3 = st.columns(3)

        with col1:
            unique_area_unit_type = pd.DataFrame(df['Area Unit Type'].unique(),columns=["Area Unit Type"])
            st.table(unique_area_unit_type)

        with col2:
            df['Area of Unit'].fillna("null",inplace = True)
            unique_area_of_unit = pd.DataFrame(df['Area of Unit'].unique(), columns=['Area of Unit'])
            st.table(unique_area_of_unit)

        with col3:
            unique_crop_type = pd.DataFrame(df['Crop Type'].unique(), columns= ['Crop Type'])
            st.table(unique_crop_type)
    except Exception as e:
        pass

if __name__ == "__main__":
    main()
