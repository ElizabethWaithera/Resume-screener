import streamlit as st
import pandas as pd

st.title("HR's Requirement")

# HR Form
with st.form("HR form"):
    position = st.text_input(label="Position", placeholder="Please enter the HR's required position")
    exp = st.text_input(label="Minimum Experience (in years)", placeholder="Please enter the minimum experience required (in years)")
    submitted = st.form_submit_button("Submit")

# Path to the Excel file
excel_file = "hr_resumes.xlsx"

# Initialize Excel file with required sheets if it doesn't exist
try:
    data = pd.read_excel(excel_file, sheet_name=None)
    if 'HR' not in data or 'Resumes' not in data:
        raise FileNotFoundError
except FileNotFoundError:
    with pd.ExcelWriter(excel_file) as writer:
        pd.DataFrame(columns=['Position', 'Experience']).to_excel(writer, sheet_name='HR', index=False)
        pd.DataFrame(columns=['Name', 'Email', 'Location', 'Score', 'Resume']).to_excel(writer, sheet_name='Resumes', index=False)

if submitted:
    position = position.lower()
    exp = int(exp)

    # Load the existing HR requirements
    hr_data = pd.read_excel(excel_file, sheet_name='HR')

    # Clear previous HR requirements
    hr_data = pd.DataFrame(columns=['Position', 'Experience'])

    # Add new HR requirements
    hr_data = hr_data.append({'Position': position, 'Experience': exp}, ignore_index=True)

    # Save the updated HR requirements back to the Excel file
    with pd.ExcelWriter(excel_file, mode='a', if_sheet_exists='replace') as writer:
        hr_data.to_excel(writer, sheet_name='HR', index=False)

# Button to show resumes
show = st.button("Show Resumes")

if show:
    # Load the resumes data
    resumes_data = pd.read_excel(excel_file, sheet_name='Resumes')

    # Display resumes in a table format
    st.write(resumes_data)

    # Option to export resumes data to a new Excel file
    export = st.button("Export Resumes to Excel")
    if export:
        resumes_data.to_excel("exported_resumes.xlsx", index=False)
        st.success("Resumes data has been exported to 'exported_resumes.xlsx'")
