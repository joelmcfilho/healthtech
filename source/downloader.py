import requests
from bs4 import BeautifulSoup
import os

base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis"

# Varre o base_url e gera uma lista de links na estrutura "~/ano/demonstração.zip". Ao final, retorna
# uma lista menor com as três demonstrações mais recentes
def get_links_by_years():
    soup = BeautifulSoup(requests.get(base_url).text,"html.parser")
    links_with_years = []

    parse_links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
    filter_by_year = [l for l in parse_links if l[:4].isdigit() and l.endswith('/')]
    
    
    for year in filter_by_year:
        link = f"{base_url}/{year}"
        links_with_years.append(link)

    target_url_all = []

    for link in links_with_years:
        soup_again = BeautifulSoup(requests.get(link).text,"html.parser")        

        parse_links_again = [a.get('href') for a in soup_again.find_all('a') if a.get('href')]
        zip_files = [l for l in parse_links_again if l.endswith('.zip') and l.lower()]
        
        for link in zip_files:
            target_url = f"{base_url}/{year}{link}"
            target_url_all.append(target_url)

    target_url_list = [target_url_all[-1],target_url_all[-2],target_url_all[-3]]

    return target_url_list
#-------------------------------------------------------------------------------------

# Garante que o caminho de download exista, e configura o download pelo caminho url
def download_file(url):
    os.makedirs("data/downloaded",exist_ok=True)

    response = requests.get(url, stream=True)

    filename = url.split('/')[-1]
    save_path = os.path.join("data/downloaded",filename)

    try:
        with open(save_path,"wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Download de {url} realizado com sucesso!")
    except Exception as e:
        print(f"Download de {url} falhou: {e}")
#----------------------------------------------------------------------------------------------

# Este método itera a lista de links gerado pelo método "get_links_by_years()" e utiliza o método 
# "download_file(url) para baixar os arquivos ZIP contidos nela, uma a uma. "
def download_execution():
    print("Lendo a URL e preparando os arquivos...")

    for url in get_links_by_years():
        download_file(url)

if __name__ == "__main__":
    download_execution()