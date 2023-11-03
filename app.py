# import libraries
import streamlit as st
from streamlit_extras.colored_header import colored_header 
import os
import processfile as pf
import documentai as docai



def header():
  colored_header(
    label="Product Demo - OCR Application",
    description="This Application processes documents in your choosen directory. It will return a dataframe after it processed all of the documents",
    color_name="light-blue-70",
    )

def file_list(Folder_name):
    files = [f for f in os.listdir(Folder_name)]
    return files

def main():
    Folder_name = st.text_input('Enter Directory Path:')
    if st.button('List Files',type="secondary"):
        if Folder_name and os.path.isdir(Folder_name):
            files = file_list(Folder_name)
            with st.expander("Files to be processed"):
                st.write(files)
            st.write(f'Selected Directory: {Folder_name}')
        else:
            st.error('Please enter a valid directory path.')

    form = st.radio('Document:', ('medcert_land', 'mer_annexd','medcert_sea','mer_annexc','hiv','psych'))
  
    if st.button('Submit',type="primary"):
        files = file_list(Folder_name)
        kv = pf.prompt_kv(form)
      

        if Folder_name and os.path.isdir(Folder_name):
            # call the processes
            with st.spinner(text="In progress..."):
              docai.DocAI_API(Folder_name,files)
              files = [f for f in os.listdir(Folder_name)]
              result = [f for f in os.listdir("results")]
              pf.call_openai(result,form,kv)
              st.success('Files processed successfully!')

        else:
            st.error('Please select a valid directory before submitting.')
    try:
        with open(f"{form}.zip", "rb") as file:
            btn = st.download_button(
                    label="Download zip file",
                    data=file,
                    file_name=f"{form}.zip",
                    mime="application/zip",
                    type="secondary"
                )
    except:
        btn = st.button('Download zip file',disabled=True,type="secondary")

if __name__ == '__main__':
    header()
    main()
    

