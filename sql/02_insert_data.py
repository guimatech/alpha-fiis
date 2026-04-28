"""
Script para importar dados do CSV de FIIs para o PostgreSQL.

Uso:
    python sql/02_insert_data.py

Variáveis de ambiente (ou edite DB_CONFIG abaixo):
    PGHOST      - Host do PostgreSQL (padrão: localhost)
    PGPORT      - Porta (padrão: 5432)
    PGDATABASE  - Nome do banco (padrão: fiis_db)
    PGUSER      - Usuário (padrão: postgres)
    PGPASSWORD  - Senha
"""

import csv
import os
import re
import sys

try:
    import psycopg2
except ImportError:
    print("Dependência necessária: psycopg2")
    print("Instale com: pip install psycopg2-binary")
    sys.exit(1)


# ── Configuração do banco ──────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Tentar carregar do .env na raiz do projeto
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()
        DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Erro: DATABASE_URL não definida. Configure no .env ou como variável de ambiente.")
    sys.exit(1)

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "dados-fiis.csv")
SQL_CREATE_PATH = os.path.join(os.path.dirname(__file__), "01_create_table.sql")


# ── Funções de parsing ─────────────────────────────────────────

def parse_decimal(value: str):
    """
    Converte string no formato brasileiro para float.
    Ex: '1.234,56' -> 1234.56, '0,75' -> 0.75
    Retorna None para 'N/A' ou valores vazios.
    """
    if not value or value.strip().upper() == "N/A":
        return None
    cleaned = value.strip().replace(".", "").replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_percent(value: str):
    """
    Converte string de porcentagem brasileira para float.
    Ex: '1,49 %' -> 1.49, '-17,49 %' -> -17.49
    Retorna None para 'N/A' ou valores vazios.
    """
    if not value or value.strip().upper() == "N/A":
        return None
    cleaned = value.strip().replace("%", "").strip().replace(".", "").replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return None


def parse_int(value: str):
    """Converte string para inteiro. Retorna None para 'N/A'."""
    if not value or value.strip().upper() == "N/A":
        return None
    cleaned = value.strip().replace(".", "").replace(",", "")
    try:
        return int(cleaned)
    except ValueError:
        return None


def parse_taxa(value: str):
    """Retorna a taxa como texto ou None para 'N/A'."""
    if not value or value.strip().upper() == "N/A":
        return None
    return value.strip()


def parse_setor(value: str):
    """Retorna o setor ou None para 'N/A'."""
    if not value or value.strip().upper() == "N/A":
        return None
    return value.strip()


# ── Mapeamento CSV → colunas da tabela ─────────────────────────

COLUMN_MAP = [
    # (nome_coluna_db, índice_csv, função_parse)
    ("ticker",                  0,  lambda v: v.strip()),
    ("setor",                   1,  parse_setor),
    ("preco_atual",             2,  parse_decimal),
    ("liquidez_diaria",         3,  parse_decimal),
    ("p_vp",                    4,  parse_decimal),
    ("ultimo_dividendo",        5,  parse_decimal),
    ("dividend_yield",          6,  parse_percent),
    ("dy_3m_acumulado",         7,  parse_percent),
    ("dy_6m_acumulado",         8,  parse_percent),
    ("dy_12m_acumulado",        9,  parse_percent),
    ("dy_3m_media",             10, parse_percent),
    ("dy_6m_media",             11, parse_percent),
    ("dy_12m_media",            12, parse_percent),
    ("dy_ano",                  13, parse_percent),
    ("variacao_preco",          14, parse_percent),
    ("rentab_periodo",          15, parse_percent),
    ("rentab_acumulada",        16, parse_percent),
    ("patrimonio_liquido",      17, parse_decimal),
    ("vpa",                     18, parse_decimal),
    ("p_vpa",                   19, parse_decimal),
    ("dy_patrimonial",          20, parse_percent),
    ("variacao_patrimonial",    21, parse_percent),
    ("rentab_patr_periodo",     22, parse_percent),
    ("rentab_patr_acumulada",   23, parse_percent),
    ("quant_ativos",            24, parse_int),
    ("volatilidade",            25, parse_decimal),
    ("num_cotistas",            26, parse_int),
    ("taxa_gestao",             27, parse_taxa),
    ("taxa_performance",        28, parse_taxa),
    ("taxa_administracao",      29, parse_taxa),
]

COLUMNS = [col for col, _, _ in COLUMN_MAP]

INSERT_SQL = f"""
    INSERT INTO fiis ({', '.join(COLUMNS)})
    VALUES ({', '.join(['%s'] * len(COLUMNS))})
    ON CONFLICT (ticker) DO UPDATE SET
        {', '.join(f'{col} = EXCLUDED.{col}' for col in COLUMNS if col != 'ticker')},
        data_importacao = CURRENT_TIMESTAMP;
"""


# ── Execução principal ─────────────────────────────────────────

def main():
    csv_path = os.path.abspath(CSV_PATH)
    sql_path = os.path.abspath(SQL_CREATE_PATH)

    if not os.path.exists(csv_path):
        print(f"Erro: CSV não encontrado em {csv_path}")
        sys.exit(1)

    # Conectar ao banco
    print(f"Conectando ao PostgreSQL (Neon)...")
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = False
        cur = conn.cursor()
    except psycopg2.OperationalError as e:
        print(f"Erro ao conectar: {e}")
        print("\nVerifique a DATABASE_URL.")
        sys.exit(1)

    # Criar tabela (se não existir)
    if os.path.exists(sql_path):
        print("Executando script de criação da tabela...")
        with open(sql_path, "r", encoding="utf-8") as f:
            cur.execute(f.read())
        conn.commit()
        print("Tabela criada/verificada com sucesso.")
    else:
        print(f"Aviso: Script SQL não encontrado em {sql_path}. Assumindo que a tabela já existe.")

    # Ler e inserir dados do CSV
    print(f"Lendo dados de {csv_path}...")
    inserted = 0
    errors = 0

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # pular cabeçalho

        for line_num, row in enumerate(reader, start=2):
            if not row or not row[0].strip():
                continue

            try:
                values = []
                for col_name, idx, parser in COLUMN_MAP:
                    raw = row[idx] if idx < len(row) else ""
                    values.append(parser(raw))

                cur.execute("SAVEPOINT sp")
                cur.execute(INSERT_SQL, values)
                cur.execute("RELEASE SAVEPOINT sp")
                inserted += 1
            except Exception as e:
                errors += 1
                cur.execute("ROLLBACK TO SAVEPOINT sp")
                ticker = row[0] if row else "?"
                print(f"  Erro na linha {line_num} ({ticker}): {e}")
                continue

    conn.commit()
    cur.close()
    conn.close()

    print(f"\nImportação concluída:")
    print(f"  Registros inseridos/atualizados: {inserted}")
    print(f"  Erros: {errors}")
    print(f"  Total de linhas processadas: {inserted + errors}")


if __name__ == "__main__":
    main()
