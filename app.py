import streamlit as st
import pandas as pd
import json
# 30 mins for python 
# Function to load data based on file type and user input
def load_data(file, file_type, encoding, delimiter, has_header):
    if file_type == "json":
        df = pd.read_json(file,orient="index")
    elif file_type == "csv":
        df = pd.read_csv(file, encoding=encoding, delimiter=delimiter, header=0 if has_header else None)
    else:
        df = pd.DataFrame()  # Placeholder for other file types

    return df

# Streamlit app
custom_css = """
                    <style>
                    .stApp {
                        margin-top: -50px; /* Adjust the value as needed */
                    }
                    </style>
                """
st.markdown(custom_css, unsafe_allow_html=True)
st.title("Product Data Import and Display")

# File upload and details form
uploaded_file = st.file_uploader("Upload file", type=["csv", "json"])
if uploaded_file is not None:
    # User input form
    i=0
    st.subheader("File Details")
    file_type = st.selectbox("Select file type", ["json", "csv"])
    encoding = st.text_input("Enter encoding (e.g., utf-8)", "utf-8")

    if file_type == "csv":
        delimiter = st.text_input("Enter delimiter", ",")
        has_header = st.checkbox("File has header", value=True)
    else:
        delimiter = ""
        has_header = False

    # Load data based on user input
    try:
        df = load_data(uploaded_file, file_type, encoding, delimiter, has_header)
        st.sidebar.header("Display Handling Options")
        selected_fields = st.sidebar.multiselect("Select Fields to Display", df.columns.tolist())
        add_button = st.sidebar.button(">> Add to Display", key="add_button")
        remove_button = st.sidebar.button("<< Remove from Display", key="remove_button")

        # Update selected fields based on button clicks
        if add_button:
            selected_fields = [field for field in df.columns if field not in selected_fields]
        if remove_button:
            selected_fields.extend(selected_fields)
            selected_fields = []

    # Display the table
        st.sidebar.write("Fields to Display:", selected_fields)
        st.write("### Displayed Product Data")

        st.dataframe(df[:][selected_fields],width=500)
    except:
        st.warning("Wrong type selected")

    # Display handling options
    
