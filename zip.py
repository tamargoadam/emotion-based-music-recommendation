# importing required modules 
from zipfile import ZipFile 
import os 
import json
  
def get_all_file_paths(directory): 
  
    # initializing empty file paths list 
    file_paths = [] 
  
    # crawling through directory and subdirectories 
    for root, directories, files in os.walk(directory): 
        for filename in files: 
            # join the two strings in order to form the full filepath. 
            filepath = os.path.join(root, filename) 
            file_paths.append(filepath) 
  
    # returning all file paths 
    return file_paths         
  
def main(): 
    # path to folder which needs to be zipped 
    directory = './server/endpoints/credentials'
  
    # calling function to get all file paths in the directory 
    file_paths = get_all_file_paths(directory) 
  
    # printing the list of all files to be zipped 
    print('Following files will be zipped:') 
    for file_name in file_paths: 
        print(file_name)

    # writing files to a zipfile 
    with ZipFile('credentials.zip','w') as zip: 
        # writing each file one by one 
        for file in file_paths: 
            zip.write(file) 
    
    print('All files zipped successfully!')         
"""
    #with ZipFile(zip_file) as zf:
        #zf.extractall(pwd=bytes(password,'utf-8'))

    # getting secret key for the zip file
    with open("secret.json", "r") as file2:
        creds = json.load(file2)
        password = creds['PROJ_SECRET']
        #print(password)
        # setting password for zip file
        zip_file = 'credentials.zip'
        with ZipFile(zip_file) as zf:
            zf.setpassword(pwd=bytes(password, 'utf-8'))
            zf.close()
            print('Password set to PROJ_SECRET success!')
  """

if __name__ == "__main__": 
    main() 