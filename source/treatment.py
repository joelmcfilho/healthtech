
import os
import pandas as pd
from unidecode import unidecode
import re
import zipfile


def collect_processed_files(base_dir="data/processed"):
    file_list = []

    if not os.path.exists(base_dir):
        return file_list

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith((".csv", ".txt", ".xlsx")):
                file_list.append(os.path.join(root, file))

    return file_list


def normalize_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .map(unidecode)
    )
    return df
#----------------------------------------------------------------

def find_value_column(df):
    for col in df.columns:
        if "vl_saldo_final" in col or "valor" in col:
            return col
    return None
#----------------------------------------------------------------

def extract_period(filepath):
    match = re.search(r'(\d)T(\d{4})', filepath)
    if match:
        return match.group(2), match.group(1)  # ano, trimestre
    return None, None
#---------------------------------------------------------------

def read_file(filepath):
    if not os.path.exists(filepath):
        print("Caminho para arquivo não existe.")
        return None
    else:
        try:
            if filepath.endswith(".csv"):
                return  pd.read_csv(filepath,sep=";",dtype=str,low_memory=False)
            elif filepath.endswith(".txt"):
                return pd.read_csv(filepath,sep=";",dtype=str,low_memory=False)
            elif filepath.endswith(".xlsx"):
                return pd.read_excel(filepath,dtype=str)
            else:
                print("Formato não suportado!")
                return None
        except Exception as e:
            print(f"Erro ao ler {filepath}: {e}")
            return None
#----------------------------------------------------------------

def find_description_column(dataframe):
    for col in dataframe.columns:
        normalized = col.lower()
        if "descri" in normalized or "evento" in normalized:
            return col
    return None
#----------------------------------------------------------------
    
def filter_expense_rows(dataframe,df_col):
    keys = ["despesa","evento","sinistro"]

    mask = dataframe[df_col].astype(str).str.lower().apply(lambda x: any(k in x for k in keys))

    return dataframe[mask]
#----------------------------------------------------------------

def normalize_structure(df,year,trim):

    df = normalize_columns(df)

    desc_col = "descricao"
    valor_col = find_value_column(df)
    reg_ans_col = "reg_ans"

    if not all([desc_col in df.columns, valor_col, reg_ans_col in df.columns]):
        print("Colunas disponíveis:", df.columns.tolist())
        return None

    df = df[[reg_ans_col, desc_col, valor_col]].copy()

    df.columns = ["RegistroANS", "Descricao", "ValorDespesas"]

    df["Ano"] = year
    df["Trimestre"] = trim

    return df
#----------------------------------------------------------------

def process_expense_files():
    file_list = collect_processed_files()

    if not file_list:
        print("Nenhum arquivo encontrado em data/processed.")
        return None

    consolidated = []

    for filepath in file_list:
        print(f"\nAbrindo {filepath}")

        year, trim = extract_period(filepath)

        df = read_file(filepath)
        if df is None or df.empty:
            continue

        df = normalize_columns(df)

        desc_col = find_description_column(df)
        if not desc_col:
            continue

        df_filtered = filter_expense_rows(df, desc_col)
        if df_filtered.empty:
            continue

        df_norm = normalize_structure(df_filtered, year, trim)
        if df_norm is None:
            continue

        consolidated.append(df_norm)

    if not consolidated:
        return None

    return pd.concat(consolidated, ignore_index=True)        
#----------------------------------------------------------------
def run_treatment_pipeline():
    df_final = process_expense_files()

    if df_final is None or df_final.empty:
        print("Nenhum dado consolidado.")
        return None

    df_final["CNPJ"] = df_final["RegistroANS"]

    df_final["RazaoSocial"] = "NAO_INFORMADO"

    df_final = df_final[
        ["CNPJ", "RazaoSocial", "Trimestre", "Ano", "ValorDespesas"]
    ]

    df_final["ValorDespesas"] = (
        df_final["ValorDespesas"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    output_csv = "data/finalized/consolidado_despesas.csv"
    output_zip = "data/finalized/consolidado_despesas.zip"

    os.makedirs("data/finalized", exist_ok=True)
    df_final.to_csv(output_csv, index=False, sep=";", encoding="utf-8-sig")

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(output_csv)

    return df_final


if __name__ == "__main__":
    run_treatment_pipeline()