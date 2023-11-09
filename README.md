# OCR App
OCR Application for handwritten filled-up forms. Uses API such as DocumentAI API by Google Cloud Platform for OCR and OPENAI API for extracting key-value pairs in the raw text. It is entirely built on python and uses Streamlit web-application framework.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white) ![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)

### The applicatio is built using 3 python codes
1. [documentai.py](https://github.com/jarc-101/virapp-ocr/blob/main/documentai.py) - It uses the DocumentAI API by google cloud platform via SDK(python).
2. [process.py](https://github.com/jarc-101/virapp-ocr/blob/main/processfile.py) - The code then processes the raw text output response by the DocumentAI API and get the key-value pairs using OPENAI API. The response is also cleaned using [regex_module](https://docs.python.org/3/howto/regex.html) and [pandas](https://pandas.pydata.org/).
3. [app.py](https://github.com/jarc-101/virapp-ocr/blob/main/app.py) - This is the application created using Streamlit which users can interact with.

## Main code for the app
```python
# import libraries
import streamlit as st
from streamlit_extras.colored_header import colored_header 
import os
import processfile as pf
import documentai as docai



def header():
  colored_header(
    label="Product Demo - OCR Application",
    description="This Application processes documents in your choosen directory. It will return a zip file after it processed all of the documents",
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
            st.toast('Please enter a valid directory path.', icon='🚨')

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
```

## Demo picture
![alt text](https://github.com/jarc-101/virapp-ocr/blob/main/front-end.png)