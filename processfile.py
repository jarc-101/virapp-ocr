import os
import pandas as pd
import openai
import re
import pyminizip 


def prompt_kv(form):
  if form == 'medcert_land':
    kv = "name,age,date of birth (mm/dd/yyyy),country destination,gender,result,physician,director,date of examination"

  if form == 'mer_annexd':
    kv = "name,age,date of birth (mm/dd/yyyy),place of birth,gender,result,height (cm),weight (kg),blood type,restrictions,physician,date of examination"

  if form == 'medcert_sea':
    kv = "name,age,date of birth (mm/dd/yyy),place of birth,nationality,religion,gender,result,company, physician,director,date of examination"

  if form == 'mer_annexc':
    kv = "name,age,date of birth (mm/dd/yyy),country destination,gender,result,height (cm),weight (kg),blood type,restrictions,physician,name of clinic,date of examination"

  if form == 'hiv':
    kv = "name,age,date of examination,examining physician,gender,result,med tech,pathologist"

  if form == 'psych':
    kv = "name,position applied,referred by,date of examination,intellect level,remarks,psychologist,"
  return kv


def parent_dict(dict_key,key_val,parent):
    if parent.get(dict_key) is None:
      parent[str(dict_key)] = key_val
      int(dict_key)
      dict_key+=1
    else:
      parent[str(dict_key)] = key_val
    return parent,dict_key


def call_openai(result,form,kv):
  # use API key
  openai.api_key = os.getenv("OPENAI_API_KEY")
  
  # set variables
  parent = {}
  dict_key = 1


  for file in result:
    with open(f"results/{file}","r") as f:
      read = f.read()
      text = read.replace("\n"," ")

    # Making the ai prompt specific for segmentation
    sys_msg = "You are a text segmentation expert, skilled in making key-value pairs out of a text file."
    
    # Prompt that will be send to openai API
    user_prompt = f"I need help to extract the following key-value pair{kv} in this text: {text} use this format key:value"

    # OpenAI API calling
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": sys_msg},
        {"role": "user", "content": user_prompt}
      ]
    )

    result = response.choices[0].message["content"]

    # Sentence segmentation coming from the response of the API
    sentences = result.split("\n")

    # Start Segmenting the words with 'name'
    search_word = "name"
    pattern = r'\b' + re.escape(search_word) + r'\b'
    index = None
    for i, word in enumerate(sentences):
        if re.search(pattern, word,re.IGNORECASE):
            index = i
            break
    sentences = sentences[index:]

    # Token segmentation and key-value pair creation
    key_val = {}
    for sentence in sentences:
      key_val[sentence.split(":")[0].lower().replace(' ', '_')] = sentence.split(": ")[1]

    # Save the values to create a dataframe
    parent,dict_key = parent_dict(dict_key,key_val,parent)

  # creation of dataframe to be created as csv file
  df = pd.DataFrame(parent)
  df = df.transpose()
  if os.path.isfile(f"{form}.csv"):
    df.to_csv(f"{form}.csv",mode='a',header=False,index=False)
  else:
    os.system(f"touch {form}.csv")
    df.to_csv(f"{form}.csv",mode='w',index_label='id',index=False)


  # input file path 
  inpt = f"./{form}.csv"
    
  # prefix path 
  pre = None
  
  # output zip file path 
  oupt = f"./{form}.zip"
    
  # set password value 
  password = "P@ssw0rd"
  
  # compress level 
  com_lvl = 4
    
  # compressing file 
  pyminizip.compress(
    inpt,
    None,
    oupt, 
    password,
    com_lvl)
  os.system("rm -r results")





    
