# import libraries
import streamlit as st
import tkinter as tk
from tkinter import filedialog
from streamlit_extras.colored_header import colored_header 


# Set up tkinter
root = tk.Tk()
root.withdraw()

# Make folder picker dialog appear on top of other windows
root.wm_attributes('-topmost', 1)

def example():
  colored_header(
    label="OCR Application",
    description="This Application processes documents in your choosen directory. It will return a dataframe after it processed all of the documents",
    color_name="light-blue-70",
    )
example()


# Folder picker button

# st.write('''
# This Application processes documents in your choosen directory. It will return a dataframe after it processed all of the documents.
#          ''')
st.write('Please select a folder:')
clicked = st.button('Folder Picker')
if clicked:
    dirname = st.text_input('Selected folder:', filedialog.askdirectory(master=root))

