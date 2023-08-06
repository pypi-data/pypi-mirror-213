import requests
from bs4 import BeautifulSoup as bs

# def get_entrezID(ensid):

def ncbi_summary(geneid):
    
    # Send HTTP GET request to the web page
    url = "https://www.ncbi.nlm.nih.gov/gene/"
    gene = geneid

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://www.genecards.org/',
    }

    response = requests.get(url + gene, headers=headers)

    soup = bs(response.content, 'html.parser')

    summary_tag = soup.find('dt', string="Summary")
    next_dt_tags = summary_tag.find_next('dd')

    return(next_dt_tags.get_text())

if __name__== "__main__":
    geneid = "56979"
    print(ncbi_summary(geneid))
