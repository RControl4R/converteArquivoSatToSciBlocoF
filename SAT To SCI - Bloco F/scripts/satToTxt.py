# ================================
# Importações
# ================================
import pandas as pd
import os
import csv

# ================================
# Pastas
# ================================
INPUT_FOLDER = "../input/"
OUTPUT_FOLDER = "../output/"

# ================================
# Campo 01 - Condicional
# Origem: segunda linha 00, coluna 8
# ================================
def calc_campo_01(ctx_00_2):
    if ctx_00_2 is None:
        return ""

    valor = str(ctx_00_2[7]).strip()  # coluna 8 (índice 7)

    if valor == "1":
        return "5"
    if valor == "2":
        return "6"
    if valor == "3":
        return "7"
    return ""

# ================================
# Processamento do arquivo TXT
# ================================
def processar_arquivo():

    # Localiza arquivo TXT
    arquivo_txt = None
    for file in os.listdir(INPUT_FOLDER):
        if file.lower().endswith(".txt"):
            arquivo_txt = os.path.join(INPUT_FOLDER, file)
            break

    if not arquivo_txt:
        print("Nenhum arquivo TXT encontrado na pasta input/")
        return

    # Leitura do TXT
    df = pd.read_csv(
        arquivo_txt,
        sep=";",
        dtype=str,
        header=None,
        keep_default_na=False,
        engine="python",
        names=list(range(0, 60))  # número seguro de colunas
    )

    registros_saida = []

    ctx_00_1 = None
    ctx_00_2 = None

    # ================================
    # Loop sequencial por estado
    # ================================
    for _, row in df.iterrows():
        tipo = str(row[0]).strip()

        # Primeira linha 00
        if tipo == "00" and ctx_00_1 is None:
            ctx_00_1 = row
            continue

        # Segunda linha 00
        if tipo == "00" and ctx_00_1 is not None and ctx_00_2 is None:
            ctx_00_2 = row
            continue

        # Linha principal 06
        if tipo == "06":
            if ctx_00_1 is None or ctx_00_2 is None:
                continue

            # ================================
            # Campo 01 (implementado)
            # ================================
            campo_01 = calc_campo_01(ctx_00_2)

            # Campo 02 - valor fixo
            campo_02 = "0"

            # Campo 03 - coluna 14 da primeira linha 00
            campo_03 = str(ctx_00_1[14]).strip()

            # Campo 05 - coluna 14 da primeira linha 00
            campo_05 = str(ctx_00_1[3]).strip()


            # ================================
            # Demais campos (ainda não mapeados)
            # ================================
            registro = {
                1: campo_01,
                2: campo_02,
                3: campo_03,
                4: "",
                5: campo_05,
                6: "",
                7: "",
                8: "",
                9: "",
                10: "",
                11: "",
                12: "",
                13: "",
                14: "",
                15: "",
                16: "",
                17: "",
                18: "",
                19: "",
                20: "",
                21: "",
                **{i: "" for i in range(22, 55)}
            }

            registros_saida.append(registro)

            # Limpa contexto
            ctx_00_1 = None
            ctx_00_2 = None

    # ================================
    # DataFrame final
    # ================================
    df_final = pd.DataFrame(registros_saida)

    # Colunas com aspas (mantido padrão)
    colunas_com_aspas = [2,3,4,5,6,7,8,9,10,11,15,19,21]

    def colocar_aspas(x):
        if x is None or x == "":
            return "\"\""
        return f"\"{x}\""

    for col in colunas_com_aspas:
        if col in df_final.columns:
            df_final[col] = df_final[col].apply(colocar_aspas)

    # ================================
    # Escrita do arquivo final
    # ================================
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    nome_base = os.path.splitext(os.path.basename(arquivo_txt))[0]
    output_path = f"{OUTPUT_FOLDER}/{nome_base}_formatado.txt"

    df_final.to_csv(
        output_path,
        sep=",",
        index=False,
        header=False,
        quoting=csv.QUOTE_NONE,
        escapechar='\\'
    )

    print(f"Arquivo gerado com sucesso: {output_path}")

# ================================
# Main
# ================================
if __name__ == "__main__":
    processar_arquivo()
