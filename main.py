import pandas as pd
import streamlit as st
from pathlib import Path
import functions
import openpyxl

import streamlit as st

st.title("Basic Data Cleaning Automation App")
file = st.file_uploader(label="Upload a csv or excel file:", type=["xlsx", "csv"])


if file is not None:

    extension = Path(file.name).suffix
    df = pd.DataFrame()
    if extension == ".xlsx":
       df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)

    with st.form("Remove Duplicates form"):
        remove_duplicates = st.radio("Do you want to remove duplicate rows?", ["yes", "no"])
        submitted_duplicates = st.form_submit_button("Submit")
        if submitted_duplicates:
            if remove_duplicates == "yes":
                df = df.drop_duplicates(keep="first")
                st.write("Current Dataframe:", df)

    column = st.selectbox('Select a column before going on to the next steps', tuple(df.columns))

    if df[column].dtype == 'object':
        with st.form("Handle missing values in the selected column"):

            # if the column selected is categorical, show options for handling
            option = st.radio("Replace missing values in selected column with:",
                                   ["missing",
                                    "mode",
                                    "delete column if more than 50% values are missing"])
            submitted_missing_cat = st.form_submit_button("Submit")
            if submitted_missing_cat:
                df = functions.handle_missing_values(df, column, option)
                st.write("Current Dataframe:", df)

        with st.form("Data Type Conversion"):

            # if the column selected is categorical, show options for handling
            option = st.radio("Convert the selected column into one of the following datatypes",
                                   ["int",
                                    "float",
                                    "datetime"])
            submitted_convert = st.form_submit_button("Submit")
            if submitted_convert:
                try:
                    df = functions.cat_datatype_conversion (df, column, option)
                    st.write(f"Datatype of {column} currently is {df[column].dtype}")
                except:
                    st.write("Please choose as an appropriate datatype")
                    st.write(f"Datatype of {column} currently is {df[column].dtype}")

        with st.form("Trimming"):

            # if the column selected is categorical, show options for handling
            option = st.radio("Do you want to trim whitespace for the current column",
                                   ["yes",
                                    "no"])
            submitted_trim = st.form_submit_button("Submit")
            if submitted_trim:
                df[column] = df[column].str.trim()
                st.write("Current Dataframe:", df)

        with st.form("Uppercase / Lowercase"):

            # if the column selected is categorical, show options for handling
            option = st.radio("Choose (if needed) an orientiation for the column:",
                                   ["Upper",
                                    "Lower"])
            submitted_orient = st.form_submit_button("Submit")
            if submitted_orient:
                if option == "Upper":
                    df[column] = df[column].str.upper()
                    st.write("Current Dataframe:", df)
                else:
                    df[column] = df[column].str.lower()
                    st.write("Current Dataframe:", df)

        with st.form("Replace"):

            # if the column selected is categorical, show options for handling
            replace_info = st.text_input("Replace a certain substring by another substring:", placeholder="old_substring(and)new_substring")
            submitted_replace = st.form_submit_button("Submit")
            if submitted_replace:
                old_string = replace_info.split('(and)')[0]
                new_string = replace_info.split('(and)')[1]
                df[column] = df[column].str.replace(old_string, new_string)
                st.write("Current Dataframe:", df)

        with st.form("Data Encoding"):

            # if the column selected is categorical, show options for handling
            option = st.radio("Encode the selected column using one hot encoding:", ["yes", "no"])
            submitted_convert = st.form_submit_button("Submit")
            if submitted_convert:
                if option == "yes":
                    df = pd.concat([pd.get_dummies(df[column], dtype="float"), df], axis=1)
                    df = df.drop(column, axis=1)
                st.write("Current Dataframe:", df)

    else:
        with st.form("Handle missing values in the selected column"):
            # if the column selected is a number, show options for handling
            option = st.radio("Replace missing values in selected column with:",
                              ["mean",
                               "mode",
                               "median",
                               "ffill",
                               "bfill",
                               "quadratic interpolation",
                               "linear interpolation",
                               "delete column if more than 50% values are missing"])
            submitted_missing_num = st.form_submit_button("Submit")
            if submitted_missing_num:
                df = functions.handle_missing_values(df, column, option)
                st.write("Current Dataframe:", df)
        with st.form("Remove outliers"):
            option = st.radio("Remove outliers in the selected column:",
                              ["yes", "no"])
            submitted_outliers = st.form_submit_button("Submit")
            if submitted_outliers:
                if "yes":
                    st.write("Current Dataframe:", functions.remove_outliers(df, column))







