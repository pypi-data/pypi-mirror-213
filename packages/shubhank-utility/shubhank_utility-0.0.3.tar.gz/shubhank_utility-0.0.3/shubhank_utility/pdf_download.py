import os
import requests
import pandas as pd


def filename(language, file_name):
    file_name = str(file_name).strip().replace("/","-")
    if file_name[-1] == ".":
        file_name += "pdf"
    else:
        file_name += ".pdf"
    return "output/"+ str(language).lower().strip().capitalize() + "/" + file_name
    

def download_pdf(url, file_name, headers, language):

    try:
        response = requests.get(url, headers=headers, timeout=60)
    except Exception as e:
        with open('check.txt', 'a') as the_file:
            the_file.write(str(url) + " --|||-- " + str(file_name) + " --|||-- " + str(language) + "\n")
        return None
    
    
    print("pdf downloaded")
    
    filepath = filename(language, file_name)
    print(filepath)
    
    if response.status_code == 200:
        with open(filepath, "wb") as f:
            f.write(response.content)
        print("pdf saved")
    else:
        print(response.status_code)


def start(type, filename, company_name, language, link, parent_dir, zip=False, aws=False):

    headers = {"User-Agent": "Chrome/51.0.2704.103"}

    if type == "excel":
        df = pd.read_excel(filename, engine='openpyxl')
    elif type == "csv":
        df = pd.read_csv(filename)
    
    data = df[[company_name, language, link]].values

    # parent_dir = "/home/ubuntu/environment/pdfs download/output"
    directories = list(set(list(map(lambda x: x.lower().strip().capitalize(), list(df[language].values)))))

    for directory in directories:
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)


    for i, x in enumerate(data[4000:]):
        print(str(i+1) + "/" + str(len(data[4000:])))
        # if str(x[1]).lower().strip().capitalize() == "English":
        #     continue
        download_pdf(x[2], x[0], headers, x[1])

    if zip:
        # os.system("zip -r pdf.zip output")
        os.system(zip)
    
    if aws:
        # os.system("aws s3 cp pdfs1.zip  s3://raw-data/")
        os.system(aws)


# start(
#     type="excel",                                          # filetype: csv or excel
#     filename="pdf_download_input.xlsx",                          # filename along with its path
#     company_name="Company Name",                         # column name containing the company_name
#     language="Language",                                 # column name containing the language
#     link="Links",                                        # column name containing the link
#     parent_dir="output"                  # create a folder and pass its path here
#     ,zip="zip -r India_05_26-04-2023.zip output",                         # optional parameter: pdf.zip: output zip name; output: output folder name
#     aws="aws s3 cp India_05_26-04-2023.zip  s3://raw-data/" # optional parameter: pdf.zip: zip file to export; s3://raw-data/: s3 bucket name
# )