import requests
import pandas as pd
from bs4 import BeautifulSoup

def info_extractor(source):
    # Number of data points in the DataFrame
    rows=source.shape[0]
    # Creating a Dataframe to store the Title and Content of the Article
    df=pd.DataFrame(columns=['Title','Content'])
    for i in range(rows):
        # Url from where we need to get the data
        url=source.iloc[i,1]
        # Get the response from the server
        response=requests.get(url)
        # If the page is found then extract the information from it
        if response.status_code==200:
            # Parsing the response and getting the html document from it
            soup=BeautifulSoup(response.content,'html.parser')
            # Getting the Heading of the article
            heading=soup.find('h1',class_='entry-title').text
            # Getting the content of the article
            content_list=soup.find_all('p')
            # Initializing a string to concat all the Content to it
            content=""
            # Adding all the Content in the single variable
            for con in content_list:
                content+=con.text
            # adding the Title and Content to the Dataframe
            df=pd.concat([df,pd.DataFrame({'Title':[heading],'Content':[content]})],axis=0).reset_index(drop=True)
        # If the requested page is not found
        elif response.status_code==404:
            # add "N/A" in corresponding columns
            df=pd.concat([df,pd.DataFrame({'Title':["N/A"],'Content':["N/A"]})],axis=0).reset_index(drop=True)
    return df

def main():
    # Loading the Input file to access the links to the web pages
    source=pd.read_csv(r'Input.csv')
    # Calling Extract function that returns a Data Frame that has heading and content of Article
    df=info_extractor(source)
    # Appending the dataframe to existing data
    new_df=pd.concat([source,df],axis=1)
    # Saving the obtained data
    new_df.to_csv("Details.csv",index=False)

if __name__=='__main__':
    main()






