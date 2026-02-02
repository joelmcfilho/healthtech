# **Healthtech de SaaS Vertical**
# Um Projeto Teste de admissão - Intuitive Care

## **Objetivo**

Construir um pipeline simples de dados integrado com API, fazendo o download de arquivos, sua descompactação e preparação, e por fim, seu tratamento de dados.

### Tecnologias Usadas

- Python 3.14.0

### Bibliotecas

(Disponível para consulta em requirements.txt ou instalação rápida com `pip install -r requirements.txt` )

- requests (para requisições HTTP)
- beautifulsoup4 (para leitura e extração de dados em páginas HTML)
- pandas (manipulação de dados de maneira geral)
- openpyxl (leitor de arquivos .xlsx)
- python-dateutil (possibilitar a leitura de datas em formatos distintos dos tradicionais) *- Por segurança -*

## Como rodar?

## Como funciona o programa?
### **1- Fluxo Básico**

Ao iniciar o programa, este irá preparar o Download das três últimas demonstrações contabéis disponíveis em https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis e irá executá-los logo em seguida na máquina do usuário. Com o download bem sucedido, o programa irá continuar automaticamente para a descompactação dos arquivos baixados, e em seguida, irá abrir demonstração por demonstração para tratar seus dados.

### **2- Componentes do Programa**
#### **2.1- main.py**
#### **2.2- downloader.py**
Este script, como o nome sugere, é responsável pela etapa inicial do Pipeline: o download dos arquivos desejados pelas regras de negócio propostas. 

Ele é composto de três métodos, sendo um deles o principal do script e os outros dois métodos auxiliares, que irão alimentar este método principal com dados da API em tempo de execução.
#### **2.3- decompresser.py**