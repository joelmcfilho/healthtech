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

Basta rodar o script ```main.py```, localizado em "~/source".

Observação: É necessário ter as dependências do Python 3.11 ou superior instaladas no ambiente de testes.

## Como funciona o programa?
### **1- Fluxo Básico**

Ao iniciar o programa, este irá preparar o Download das três últimas demonstrações contabéis disponíveis em https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis e irá executá-los logo em seguida na máquina do usuário. Com o download bem sucedido, o programa irá continuar automaticamente para a descompactação dos arquivos baixados, e em seguida, irá abrir demonstração por demonstração para tratar seus dados. 

Após selecionar as linhas com os termos chave "despesas", "eventos", e "sinistros", o programa seleciona campos relevantes relacionados a essas linhas, como CNPJ , RazaoSocial , Trimestre , Ano e Valor das Despesas, e os agrupa em um único arquivo .CSV. 

### **2- Componentes do Programa**
#### **2.1- main.py**

É o script central do programa, que inicializa o Pipeline e roda todas as instruções nos Scripts, executando todos os procedimentos necessários.

#### **2.2- downloader.py**

Este script, como o nome sugere, é responsável pela etapa inicial do Pipeline: o download dos arquivos desejados pelas regras de negócio propostas. 

O fluxo de execução do script é dividido em três etapas principais:

1- Leitura e varredura da estrutura do site

2- Construção dinâmica das URLs dos arquivos ZIP

3- Download sequencial dos arquivos selecionados

Cada uma dessas etapas é encapsulada em funções específicas, garantindo organização, legibilidade e reaproveitamento de código.

Ao final da execução deste Script, o programa deverá realizar o Download das três demonstrações contábeis mais recentes disponíveis no endereço, em condições para ser processado por outros componentes do Pipeline.

##### Função ```get_links_by_years()```

Essa função é responsável por navegar pela API, identificar os anos disponíveis e construir a lista final de URLs dos arquivos ZIP a serem baixados.

- É feita uma requisição GET para a URL base: https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis, e é processada com a biblioteca BeautifulSoup

- O script extrai todos os links "href" da página e filtra apenas aqueles cujo nome começa com quatro dígitos (YYYY) e Termina com /, indicando um diretório. (Cada diretório representa um ano de publicação.)

- Para cada ano identificado uma nova requisição HTTP é realizada. Os links internos são analisados novamente e são selecionados apenas arquivos que terminam com ".zip".

- Cada arquivo ZIP encontrado tem sua URL completa construída dinamicamente. Todas as URLs são adicionadas a uma lista acumuladora.

- Ao final do processo, a função retorna apenas os três últimos arquivos ZIP encontrados, assumindo que estão ordenados cronologicamente no diretório.

##### Função ```download_file(url)```

Realizar o download físico de um arquivo ZIP a partir de uma URL fornecida e o salva localmente.

- Primeiramente, ele garante a existência do diretório ("data/downloaded"). Caso não exista, ele é criado automaticamente.

- A requisição é feita com "stream=True", permitindo o download em blocos. Isso evita o carregamento completo do arquivo na memória.

- O arquivo é salvo com o mesmo nome presente na URL. A escrita é feita em chunks de 1024 bytes.

- Durante o processo é utilizado uma estrutura "try-except" para tratamento de erros.

##### Função ```download_execution()```

Sua responsabilidade é orquestrar todo o fluxo do Script.

- Inicialmente chama a função ```get_links_by_years()``` para obter a lista de URLs.

- Itera sobre cada URL retornada, e para cada uma, executa a função download_file(url), realizando o download sequencial dos arquivos.

**OBS:** Essa função atua como o ponto de entrada lógico do processo de download.

#### Considerações Técnicas:

A abordagem baseada em scraping permite uma atualização automática dos anos disponíveis a cada execução do Script.

#### **2.3- decompresser.py**

Este script é responsável por descompactar automaticamente todos os arquivos ZIP baixados na etapa inicial, organizando seu conteúdo em uma estrutura de diretórios bem definida.

##### Função ```decompresser(download_dir="data/downloaded",extracted_dir="data/processed")```

Executar a extração completa dos arquivos ZIP presentes no diretório de download, salvando seus conteúdos no diretório de processamento.

**Parâmetros:** 

- ```download_dir``` (str): Diretório onde estão localizados os arquivos ZIP baixados.
Valor padrão: "data/downloaded"

- ```extracted_dir``` (str): Diretório onde os arquivos extraídos serão armazenados.
Valor padrão: "data/processed"

**Funcionamento:**

- O script garante que o diretório "data/processed" exista. Caso não exista, ele é criado automaticamente.

- Utiliza os.listdir(download_dir) para listar todos os arquivos presentes no diretório de download. Cada item retornado é tratado como um arquivo ZIP a ser processado.

- Para cada arquivo ZIP, o caminho completo do arquivo é montado (zip_path) e um diretório exclusivo de saída é criado com o nome do próprio arquivo ZIP

- Por fim, a biblioteca padrão zipfile é utilizada para abrir e extrair os arquivos com o método extractall(), que descompacta todo o conteúdo no diretório correspondente.

- Durante o processo é utilizado uma estrutura "try-except" para tratamento de erros.

#### **2.4- treatment.py**

O script realiza a leitura de arquivos heterogêneos (CSV, TXT, XLSX), identifica colunas de interesse por proximidade semântica, filtra registros específicos, e consolida os dados em um arquivo CSV único.

##### Função ```normalize_columns(df)```

- Remove espaços em branco, converte para minúsculas e remove acentuação (ex: "Razão Social" vira "razao_social").

##### Função ```find_value_column(df)``` e ```find_description_column(df)```

- Localizam dinamicamente as colunas de "valor" e "descrição da conta".

- Utilizam buscas por palavras-chave (vl_saldo_final, valor, descri, evento).

##### Função ```extract_period(filepath)```

- Extrai metadados de tempo (Ano e Trimestre) a partir do nome do arquivo.

- Utiliza Expressões Regulares (Regex) para identificar padrões como 1T2023

##### Função ```read_file(filepath)```

- Identifica e aloca cada tipo de arquivo para o seu método de tratamento correto

- Possui lógica de detecção automática de delimitadores para CSVs (sep=None) e suporte a múltiplos formatos. Trata exceções para evitar a interrupção do pipeline caso um arquivo esteja corrompido.

##### Função ```filter_expense_rows(dataframe, df_col)```

- Filtra os arquivos analisados, procurando manter apenas linhas que representam "despesas", "eventos" ou "sinistros"

##### Função ```normalize_structure(df, year, trim)```

- Transforma um DataFrame bruto em uma estrutura fixa.

- Seleciona apenas as colunas essenciais: Registro ANS, Descrição e Valor.

- Renomeia as colunas para o padrão de saída.

- Injeta as constantes de Ano e Trimestre extraídas anteriormente.

##### Função ```process_expense_files()```

- O "cérebro" do script. Itera sobre a lista de arquivos, chama as funções de leitura, filtragem e normalização, e armazena os resultados em uma lista.

- Possui como saída um único DataFrame concatenado (pd.concat) com todos os dados processados.

##### Pós-Processamento e Exportação

- Limpeza de Dados: Converte a coluna ValorDespesas (originalmente string com padrão brasileiro 1.234,56) para float numérico, removendo pontos e substituindo vírgulas.

- Geração de Output: Exporta o resultado para CSV com codificação utf-8-sig (compatível com Excel) e o compacta em um arquivo ZIP conforme exigido pelo teste.

#### Decisões Técnicas e Trade-offs

1. Uso do código "Registro ANS" como "CNPJ": Durante o processamento dos arquivos de Demonstrações Contábeis da ANS, observou-se que não há uma coluna explícita de CNPJ nos arquivos analisados. Em vez disso, os dados identificam as operadoras por meio do campo REG_ANS (Registro ANS), que é um identificador único atribuído pela Agência Nacional de Saúde Suplementar.

Diante disso, foi adotada a seguinte estratégia:

- O campo Registro ANS foi utilizado como identificador principal da operadora

- Para atender ao requisito estrutural do CSV final, esse identificador foi mapeado para a coluna CNPJ

**Justificativa:**

- O Registro ANS é único, estável e oficialmente reconhecido pela ANS

- Ele cumpre o mesmo papel funcional de identificação que o CNPJ no contexto do dataset

- A substituição foi documentada e mantida de forma consistente em todo o pipeline

- Essa decisão preserva a rastreabilidade dos dados e permite futuras integrações, caso uma tabela de correspondência Registro ANS → CNPJ seja disponibilizada.

2. Uso de valor "placeholder" quando a Razão Social for indisponível: Os arquivos processados não contêm informações de Razão Social da operadora nos dados de despesas analisados. Como a consolidação exige essa coluna, foi adotado o valor fixo:

```RazaoSocial = "NAO_INFORMADO"```

**Justificativa:**

- Evita inferências incorretas ou joins externos não confiáveis

- Mantém o schema exigido pela proposta

- Deixa explícita a ausência da informação, em vez de mascará-la ou omitir

- Essa abordagem facilita auditorias futuras e reforça a transparência do tratamento dos dados.

3. Identificação de Despesas via conteúdo da coluna “Descrição”: Os arquivos não seguem um padrão confiável de nomenclatura para identificar despesas relacionadas a Eventos/Sinistros. A identificação foi feita com base no conteúdo textual da coluna de descrição, filtrando registros que contenham os termos: "despesa", "evento", e/ou "sinistro".

**Justificativa:**

- A classificação está semanticamente embutida na descrição do lançamento contábil

- A abordagem é mais robusta do que confiar em nomes de arquivos ou layouts variáveis

- Permite processar arquivos com estruturas heterogêneas

4. Normalização de colunas e estruturas variáveis: Devido à diversidade de formatos (CSV, TXT, XLSX) e variações de nomenclatura, foi aplicado um processo de normalização que inclui: Conversão para lowercase, remoção de acentuação (unidecode) e  padronização de nomes de colunas

- Isso permitiu identificar automaticamente campos equivalentes como: Valores monetários (valor, vl_saldo_final), descrições e Registro ANS

5. Conversão de valores monetários

- Os valores de despesas estavam em formato brasileiro (ex: 1.234.567,89). Para permitir agregações e análises numéricas:Pontos foram removidos, vírgulas foram convertidas em ponto e os valores foram convertidos para float

6. Estratégia de processamento (Trade-off Técnico): **abordagem incremental**

Foi adotado processamento incremental por arquivo, em vez de carregar todos os dados simultaneamente em memória.

**Justificativa:**

- Os arquivos possuem volumes elevados

- A abordagem incremental reduz consumo de memória

- Facilita isolamento de erros por trimestre

- Escala melhor caso novos períodos sejam adicionados

7. Consolidação final e compactação

Após o processamento individual, os dados dos três trimestres foram consolidados em um único DataFrame e exportados como: "consolidado_despesas.csv" e compactado em "consolidado_despesas.zip"

Essa etapa atende ao requisito final do desafio e facilita distribuição e versionamento do resultado.

### **3 - Conclusão**

Foi atendida apenas a Etapa 1 do Teste Técnico conforme solicitado, por razões de escopo e priorização técnica. Fico a disposição para sanar quaisquer dúvidas que aparecer neste projeto!


