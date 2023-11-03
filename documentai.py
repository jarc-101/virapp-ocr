from google.api_core.client_options import ClientOptions
from google.cloud import documentai
import os 

def DocAI_API(Folder_name,files):
  # Create a list then add the filenames on the directory to the list

  PROJECT_ID = os.getenv("PROJECT_ID")
  PROCESSOR_ID = os.getenv("PROCESSOR_ID") # Create processor in Cloud Console
  LOCATION = "us"  # Format is 'us' or 'eu'

  # Refer to https://cloud.google.com/document-ai/docs/file-types
  # for supported file types
  MIME_TYPE = "application/pdf"

  # Instantiates a client
  docai_client = documentai.DocumentProcessorServiceClient(
      client_options=ClientOptions(api_endpoint=f"{LOCATION}-documentai.googleapis.com")
  )

  # The full resource name of the processor, e.g.:
  # projects/project-id/locations/location/processor/processor-id
  # You must create new processors in the Cloud Console first
  RESOURCE_NAME = docai_client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)

  os.system(f"mkdir results")

  for file in files:
    FILE_PATH = file # The local file in your current working directory
    # Read the file into memory
    with open(f"{Folder_name}/{file}", "rb") as image:
        image_content = image.read()

    # Load Binary Data into Document AI RawDocument Object
    raw_document = documentai.RawDocument(content=image_content, mime_type=MIME_TYPE)

    # Configure the process request
    request = documentai.ProcessRequest(name=RESOURCE_NAME, raw_document=raw_document)

    # Use the Document AI client to process the sample form
    result = docai_client.process_document(request=request)

    document_object = result.document

    # Go to the Folder Created for reults
    os.chdir("results")

    # Create a file.txt for the results
    os.system(f"touch {files.index(file)}.txt")
    print("Result file successfully created...")

    # Write the output of every API calls to the text files
    with open(f"{files.index(file)}.txt", mode='wt') as f:
      f.write(f"{document_object.text}")
    os.chdir('..')


