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
        return "22"
    if valor == "2":
        return "23"
    if valor == "3":
        return "24"
    return ""

# ================================
# Converte valor inteiro em string monetária (divide por 100)
# Ex: "000000000052455" -> "524.55"
# ================================
def int_to_monetario(valor):
    if valor is None:
        return "0.00"

    texto = str(valor).strip()
    if texto == "":
        return "0.00"

    try:
        return f"{int(texto) / 100:.2f}"
    except:
        return "0.00"

# ================================
# Campo 14 - cálculo padrão
# (campo12 * campo13) / 100
# ================================
def calc_campo_14(campo_12, campo_13):
    try:
        v1 = float(str(campo_12).replace(",", "."))
        v2 = float(str(campo_13))
        return f"{(v1 * v2) / 100:.2f}"
    except:
        return "0.00"

# ================================
# Campo 18 - cálculo padrão
# (campo16 * campo17) / 100
# ================================
def calc_campo_18(campo_16, campo_17):
    try:
        v1 = float(str(campo_16).replace(",", "."))
        v2 = float(str(campo_17))
        return f"{(v1 * v2) / 100:.2f}"
    except:
        return "0.00"

# ================================
# Formata datas para AAAAMMDD
# ================================
def formatar_data(valor):
    if valor is None:
        return ""

    texto = str(valor).strip()

    if texto == "":
        return ""

    # Caso já venha como DDMMAAAA (8 dígitos)
    if texto.isdigit() and len(texto) == 8:
        dia = texto[0:2]
        mes = texto[2:4]
        ano = texto[4:8]
        return f"{ano}{mes}{dia}"

    # Formato dd/mm/yyyy
    if "/" in texto:
        try:
            dia, mes, ano = texto.split("/")
            return f"{ano}{mes}{dia}"
        except:
            pass

    # Formato yyyy-mm-dd
    if "-" in texto and len(texto.split("-")[0]) == 4:
        try:
            ano, mes, dia = texto.split(" ")[0].split("-")
            return f"{ano}{mes}{dia}"
        except:
            pass

    return texto


# ================================
# Processamento do arquivo TXT
# ================================
def processar_arquivo(caminho_arquivo_txt=None):

    # -----------------------------
    # MODO 1: arquivo passado (GUI)
    # -----------------------------
    if caminho_arquivo_txt:
        arquivo_txt = caminho_arquivo_txt
    else:
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
    encoding="latin-1",
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

            # Campo 05 - coluna 4 da primeira linha 00
            campo_05 = formatar_data(ctx_00_1[3])

            # Campo 06 - coluna 05 da primeira linha 00 (após a "/")
            valor_col_05 = str(ctx_00_1[4]).strip()

            if "/" in valor_col_05:
                campo_06 = valor_col_05.split("/", 1)[1]
            else:
                campo_06 = ""
            
            # Campo 07 - Valor fixo "V"
            campo_07 = "V"

            # Campo 08 
            campo_08 = int_to_monetario(row[8])

            # Campo 09
            campo_09 = ""

            # Campo 10
            campo_10 = ""

            # Campo 11 - condicional baseado no Campo 01
            if campo_01 in ("22", "23"):
                campo_11 = "53"
            elif campo_01 == "24":
                campo_11 = "63"
            else:
                campo_11 = ""

            # Campo 12 - mesmo valor do Campo 08 (sem aspas)
            campo_12 = campo_08

            # Campo 13 - condicional baseado no Campo 01
            if campo_01 == "22":
                campo_13 = "1.65"
            else:
                campo_13 = "1.2375"

            # Campo 14
            campo_14 = calc_campo_14(campo_12, campo_13)

            # Campo 15 
            campo_15 = campo_11

            # Campo 16
            campo_16 = campo_12

            # campo_17 
            if campo_01 == "22":
                campo_17 = "7.6"
            else:
                campo_17 = "5.7"

            # Campo 18
            campo_18 = calc_campo_18(campo_16, campo_17)

            # Campo 19
            campo_19 = "14"

            # Campo 20
            campo_20 = "0"

            # Campo 21 
            campo_21 = "CREDITO SOBRE SUBCONTRATACAO DE FRETE"


            # ================================
            # Demais campos (ainda não mapeados)
            # ================================
            registro = {
                1: campo_01,
                2: campo_02,
                3: campo_03,
                4: "",
                5: campo_05,
                6: campo_06,
                7: campo_07,
                8: campo_08,
                9: "",
                10: "",
                11: campo_11,
                12: campo_12,
                13: campo_13,
                14: campo_14,
                15: campo_15,
                16: campo_16,
                17: campo_17,
                18: campo_18,
                19: campo_19,
                20: campo_20,
                21: campo_21,
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
    pasta_origem = os.path.dirname(arquivo_txt)
    nome_base = os.path.splitext(os.path.basename(arquivo_txt))[0]

    output_path = os.path.join(
        pasta_origem,
        f"{nome_base}_SCI.txt"
    )


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
