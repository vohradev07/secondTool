import streamlit as st
import pandas as pd

# Upload input CSV file
st.title("Phone Number Match Checker")
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

# Upload master CSV file
master_file = st.file_uploader("Upload master CSV file", type=["csv"])

if uploaded_file and master_file:
    # Read the uploaded files
    input_df = pd.read_csv(uploaded_file)
    master_df = pd.read_csv(master_file)

    # Ensure phone number column exists in input file
    if 'Phone Number' in input_df.columns:
        # Check for 'Phone' column in master file, considering first or second row
        phone_column = None
        if 'Phone' in master_df.columns:
            phone_column = 'Phone'
        elif not master_df.empty and len(master_df.columns) > 1 and 'Phone' in master_df.iloc[[0, 1]].values.flatten():
            for col in master_df.columns:
                if any('Phone' in str(val) for val in master_df[col].iloc[:1].values):
                    phone_column = col
                    break

        if phone_column:
            # Strip '91' prefix from master phone numbers for comparison
            master_df[phone_column] = master_df[phone_column].astype(str).str.replace('^91', '', regex=True)

            # Find all matched phone numbers
            matched_numbers = []
            for phone in input_df['Phone Number']:
                if pd.isna(phone):
                    continue
                phone_str = str(phone).strip()
                if phone_str in master_df[phone_column].values:
                    matched_numbers.append(phone_str)

            # Display results
            if matched_numbers:
                st.write(f"Number of matches: {len(matched_numbers)}")
                st.write("Matched Phone Numbers:", matched_numbers)

                # Option to export to CSV
                if st.button("Export to CSV"):
                    export_df = pd.DataFrame(matched_numbers, columns=['Matched Phone Numbers'])
                    export_df.to_csv("matched_phone_numbers.csv", index=False)
                    st.success("File 'matched_phone_numbers.csv' has been downloaded!")
            else:
                st.write("No matches found.")
        else:
            st.error("Could not find a 'Phone' column in the master CSV file.")
    else:
        st.error("Please ensure the input CSV file has a 'Phone Number' column.")