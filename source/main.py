from downloader import download_execution
from decompresser import decompresser
from treatment import run_treatment_pipeline

def main():
    print("=== INICIANDO PIPELINE ===")

    print("\n[1/3] Baixando arquivos...")
    download_execution()

    print("\n[2/3] Descompactando arquivos...")
    decompresser(download_dir="data/downloaded",extracted_dir="data/processed")

    print("\n[3/3] Processando e consolidando dados...")
    run_treatment_pipeline()

    print("\n=== PIPELINE FINALIZADO COM SUCESSO ===")

if __name__ == "__main__":
    main()