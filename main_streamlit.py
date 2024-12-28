import streamlit as st
import os
import time
import shutil

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

st.title("File Upload and Download App")

uploaded_file = st.file_uploader("Choose a file to upload", type=None)

if uploaded_file is not None:
    file_name = uploaded_file.name

    overwrite = st.checkbox("Overwrite existing file", value=False)

    if overwrite:
        destination_filename = file_name
    else:
        milliseconds_since_epoch = int(time.time() * 1000)
        file_base, file_ext = os.path.splitext(file_name)
        destination_filename = f"{file_base}_{milliseconds_since_epoch}{file_ext}"

    destination_path = os.path.join(UPLOAD_FOLDER, destination_filename)
    with open(destination_path, "wb") as dest_file:
        dest_file.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully!")
    st.write(f"Download link: [Click here to download](http://localhost:8501/download/{destination_filename})")

st.header("Download Files")
files_in_upload_folder = os.listdir(UPLOAD_FOLDER)
if files_in_upload_folder:
    selected_file = st.selectbox("Select a file to download", files_in_upload_folder)
    if st.button("Download Selected File"):
        file_path = os.path.join(UPLOAD_FOLDER, selected_file)
        with open(file_path, "rb") as file:
            st.download_button(
                label="Click to download",
                data=file,
                file_name=selected_file,
                mime="application/octet-stream",
            )
else:
    st.write("No files available for download.")