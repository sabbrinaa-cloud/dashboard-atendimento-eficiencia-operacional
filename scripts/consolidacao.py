"""
=========================================================
Projeto: Dashboard de Atendimento e Performance Operacional

Autora:
Sabrina Sá

Descrição:
Pipeline de ETL desenvolvido em Python para consolidação de
arquivos CSV, XLSX e TXT, tratamento dos dados, cálculo de
indicadores operacionais e geração da base consolidada para
consumo no Power BI.

Tecnologias:
- Python
- Pandas
- OpenPyXL

=========================================================
"""

from pathlib import Path
import pandas as pd

# ==========================================================
# CONFIGURAÇÃO DAS PASTAS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

print("=" * 70)
print("PIPELINE DE CONSOLIDAÇÃO DE DADOS")
print("=" * 70)

# ==========================================================
# LOCALIZAR ARQUIVOS
# ==========================================================

csv_file = next(DATA_DIR.glob("*.csv"))
txt_file = next(DATA_DIR.glob("*.txt"))
xlsx_file = next(DATA_DIR.glob("*.xlsx"))

print("\nArquivos encontrados:")
print(f"CSV  : {csv_file.name}")
print(f"TXT  : {txt_file.name}")
print(f"XLSX : {xlsx_file.name}")

# ==========================================================
# LEITURA SEGURA
# ==========================================================

def ler_csv(caminho, separador):

    try:
        return pd.read_csv(
            caminho,
            sep=separador,
            encoding="utf-8"
        )

    except UnicodeDecodeError:

        return pd.read_csv(
            caminho,
            sep=separador,
            encoding="latin1")


print("\nCarregando arquivos...")

df_csv = ler_csv(csv_file, ";")
df_txt = ler_csv(txt_file, "\t")
df_xlsx = pd.read_excel(xlsx_file)

print("Arquivos carregados com sucesso!")

print(f"CSV  : {len(df_csv):,} registros")
print(f"TXT  : {len(df_txt):,} registros")
print(f"XLSX : {len(df_xlsx):,} registros")

# ==========================================================
# PADRONIZAÇÃO DA BASE CSV
# ==========================================================

def padronizar_csv(df):

    print("\nPadronizando CSV...")

    df = df.rename(columns={
        "Data": "data",
        "CheckInSegundos": "checkin",
        "HrIniSegundos": "inicio",
        "HrFimSegundos": "fim",
        "Status": "status",
        "NomeLoja": "loja"
    })

    df["data"] = pd.to_datetime(
        df["data"],
        dayfirst=True,
        errors="coerce"
    )

    df["checkin"] = (
        df["data"] +
        pd.to_timedelta(df["checkin"], unit="s")
    )

    df["inicio"] = (
        df["data"] +
        pd.to_timedelta(df["inicio"], unit="s")
    )

    df["fim"] = (
        df["data"] +
        pd.to_timedelta(df["fim"], unit="s")
    )

    return df[
        [
            "checkin",
            "inicio",
            "fim",
            "status",
            "loja"
        ]
    ]


# ==========================================================
# PADRONIZAÇÃO DA BASE TXT
# ==========================================================

def padronizar_txt(df):

    print("Padronizando TXT...")

    df = df.rename(columns={
        "CheckIn": "checkin",
        "HrIni": "inicio",
        "HrFim": "fim",
        "Status": "status",
        "nome_da_loja": "loja"
    })

    df["checkin"] = pd.to_datetime(
        df["checkin"],
        dayfirst=True,
        errors="coerce"
    )

    df["inicio"] = pd.to_datetime(
        df["inicio"],
        dayfirst=True,
        errors="coerce"
    )

    df["fim"] = pd.to_datetime(
        df["fim"],
        dayfirst=True,
        errors="coerce"
    )

    return df[
        [
            "checkin",
            "inicio",
            "fim",
            "status",
            "loja"
        ]
    ]


# ==========================================================
# PADRONIZAÇÃO DA BASE EXCEL
# ==========================================================

def padronizar_excel(df):

    print("Padronizando XLSX...")

    df = df.rename(columns={
        "CheckIn_iso": "checkin",
        "HrIni_iso": "inicio",
        "HrFim_iso": "fim",
        "fl_satus": "status",
        "nome_loja": "loja"
    })

    df["checkin"] = pd.to_datetime(
        df["checkin"],
        errors="coerce"
    )

    df["inicio"] = pd.to_datetime(
        df["inicio"],
        errors="coerce"
    )

    df["fim"] = pd.to_datetime(
        df["fim"],
        errors="coerce"
    )

    # Ajuste do status
    df["status"] = df["status"].map({
        1: "concluido",
        0: "abandono"
    })

    return df[
        [
            "checkin",
            "inicio",
            "fim",
            "status",
            "loja"
        ]
    ]


# ==========================================================
# EXECUTAR PADRONIZAÇÃO
# ==========================================================

print("\n" + "=" * 70)
print("PADRONIZANDO BASES")
print("=" * 70)

df_csv = padronizar_csv(df_csv)
df_txt = padronizar_txt(df_txt)
df_xlsx = padronizar_excel(df_xlsx)

print("\nBases padronizadas com sucesso!")

print(f"CSV  : {df_csv.shape}")
print(f"TXT  : {df_txt.shape}")
print(f"XLSX : {df_xlsx.shape}")

# ==========================================================
# CONSOLIDAÇÃO DAS BASES
# ==========================================================

print("\n" + "=" * 70)
print("CONSOLIDANDO BASES")
print("=" * 70)

df = pd.concat(
    [df_csv, df_txt, df_xlsx],
    ignore_index=True
)

print(f"\nTotal de registros após consolidação: {len(df):,}")

# ==========================================================
# LIMPEZA DOS DADOS
# ==========================================================

print("\nRealizando limpeza da base...")

# Remove espaços desnecessários
df["status"] = (
    df["status"]
    .astype(str)
    .str.lower()
    .str.strip()
)

df["loja"] = (
    df["loja"]
    .astype(str)
    .str.strip()
)

# Remove registros sem datas essenciais
df = df.dropna(
    subset=[
        "checkin",
        "inicio",
        "fim"
    ]
)

print(f"Registros após limpeza: {len(df):,}")

# ==========================================================
# CÁLCULO DAS MÉTRICAS
# ==========================================================

print("\nCalculando indicadores...")

df["tempo_espera"] = (
    (
        df["inicio"] -
        df["checkin"]
    ).dt.total_seconds() / 60
)

df["tempo_atendimento"] = (
    (
        df["fim"] -
        df["inicio"]
    ).dt.total_seconds() / 60
)

# Remove tempos negativos
df = df[
    (df["tempo_espera"] >= 0) &
    (df["tempo_atendimento"] >= 0)
]

print(f"Registros válidos: {len(df):,}")

# ==========================================================
# CLASSIFICAÇÃO DOS STATUS
# ==========================================================

print("\nClassificando atendimentos...")

def classificar_status(status):

    status = str(status).lower().strip()

    if "concl" in status:
        return "atendido"

    elif "aband" in status:
        return "abandonou"

    else:
        return "outros"


df["status_final"] = df["status"].apply(classificar_status)

df["atendido"] = (
    df["status_final"] == "atendido"
).astype(int)

df["abandonou"] = (
    df["status_final"] == "abandonou"
).astype(int)

print("Classificação concluída.")

# ==========================================================
# EXPORTAÇÃO DA BASE
# ==========================================================

print("\n" + "=" * 70)
print("EXPORTANDO BASE CONSOLIDADA")
print("=" * 70)

arquivo_saida = OUTPUT_DIR / "base_consolidada.csv"

df.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)

print(f"\nBase exportada com sucesso!")

print(f"\nArquivo:")
print(arquivo_saida)

# ==========================================================
# VALIDAÇÃO FINAL
# ==========================================================

print("\n" + "=" * 70)
print("RESUMO DA BASE")
print("=" * 70)

print(f"\nTotal de registros: {len(df):,}")

print("\nDistribuição dos Status")

print(df["status_final"].value_counts())
print("\nValores encontrados na coluna STATUS:")

print(df["status"].value_counts())

print("\nDistribuição por Loja")

print(df["loja"].value_counts())

print("\nEstatísticas")

print(df[
    [
        "tempo_espera",
        "tempo_atendimento"
    ]
].describe())

print("\n" + "=" * 70)
print("PIPELINE FINALIZADO COM SUCESSO!")
print("=" * 70)