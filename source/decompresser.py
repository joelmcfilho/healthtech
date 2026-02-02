import os
import zipfile

# Este método garante que o diretório de saída (Para os arquivos descompactados) exista, 
# itera em uma lista de diretórios geradas pelo método "listdir()" e prepara/executa a descompactação
# de item por item dessa lista através da biblioteca Zipfile.
def extract_all(download_dir="data/downloaded",extracted_dir="data/processed"):
    os.makedirs("data/processed",exist_ok=True)

    for zip_file in os.listdir(download_dir):
        zip_path = os.path.join(download_dir,zip_file)

        output_path = os.path.join(extracted_dir,zip_file)
        print(f"Descompactando {zip_file}...")
        try:            
            with zipfile.ZipFile(zip_path,"r") as zip:
                zip.extractall(output_path)
            
            print(f"Arquivo {zip_file} descompactado com sucesso!")
            print("-----------------------------------------------------")
        except Exception as e:
            print(f"O arquivo {zip_file} falhou ao descompactar: {e}")
            print("-----------------------------------------------------")

#-----------------------------------------------------------------------------------
        

if __name__ == "__main__":
    print(extract_all())