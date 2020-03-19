try: 
    import pandas as pd
except:
    !pip3 install pandas
    import pandas as pd
    
def clean_data(file_path):
    # Prepare the pandas dataframe
    file1 = pd.read_csv(file_path, sep="\t").T
    file1 = file1.reset_index()
    file1 = file1.rename(columns={"index":"Posts"})

    # Drop Rows with this info 
    file = file1[~file1.Posts.str.contains("Unnamed:")]
    file = file[~file.Posts.str.contains("thank you for following me")]
    
    # Remove items from the strings
    file['Posts'] = file['Posts'].str.encode('ascii', 'ignore').str.decode('ascii') # Remove Non ascii characters
    file['Posts'] = file['Posts'].str.replace('https?:\/\/.*[\r\n]*', '', regex=True) # Remove URL
    file['Posts'] = file['Posts'].str.replace('&gt;', '', regex=True) # Remove HTML >
    file['Posts'] = file['Posts'].str.replace('#[a-zA-Z1-9]+', '', regex=True) # Remove Hashtags
    file['Posts'] = file['Posts'].str.replace('@[a-zA-Z1-9]+', '', regex=True) # Remove mentions
    file['Posts'] = file['Posts'].str.replace('\[removed\]', '', regex=True) # Remove removed messages
    file['Posts'] = file['Posts'].str.replace('\[deleted\]', '', regex=True)# Remove deleted messages
    
    # Replace symbols and acronyms 
    file = file.replace({'Posts':{'\n':'','\(':'','\)':'','\[':'','\]':'','\?':'','\.':' ',';':'',':':'','!':'','\|':'','~':'','&amp':''}}, regex=True)
    file = file[file['Posts'].str.contains("[a-z]")] # Remove anything without lower case letters in it
    
    # Overwrite file
    file.to_csv(file_path,index=False,header=True,sep='\t')
