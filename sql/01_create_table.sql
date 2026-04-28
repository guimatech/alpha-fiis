-- =============================================================
-- Tabela de Fundos de Investimento Imobiliário (FIIs)
-- Criada a partir do arquivo dados-fiis.csv
-- =============================================================

CREATE TABLE IF NOT EXISTS fiis (
    id                      SERIAL PRIMARY KEY,

    -- Identificação
    ticker                  VARCHAR(10)     NOT NULL UNIQUE,
    setor                   VARCHAR(60),

    -- Preço e liquidez
    preco_atual             NUMERIC(12,2),
    liquidez_diaria         NUMERIC(16,2),

    -- Indicadores de valor
    p_vp                    NUMERIC(8,4),

    -- Dividendos
    ultimo_dividendo        NUMERIC(12,4),
    dividend_yield          NUMERIC(8,4),       -- % mensal
    dy_3m_acumulado         NUMERIC(8,4),       -- %
    dy_6m_acumulado         NUMERIC(8,4),       -- %
    dy_12m_acumulado        NUMERIC(8,4),       -- %
    dy_3m_media             NUMERIC(8,4),       -- %
    dy_6m_media             NUMERIC(8,4),       -- %
    dy_12m_media            NUMERIC(8,4),       -- %
    dy_ano                  NUMERIC(8,4),       -- %

    -- Rentabilidade e variação
    variacao_preco          NUMERIC(10,4),      -- %
    rentab_periodo          NUMERIC(10,4),      -- %
    rentab_acumulada        NUMERIC(10,4),      -- %

    -- Patrimônio
    patrimonio_liquido      NUMERIC(18,2),
    vpa                     NUMERIC(18,2),
    p_vpa                   NUMERIC(8,4),

    -- Indicadores patrimoniais
    dy_patrimonial          NUMERIC(10,4),      -- %
    variacao_patrimonial    NUMERIC(10,4),      -- %
    rentab_patr_periodo     NUMERIC(10,4),      -- %
    rentab_patr_acumulada   NUMERIC(10,4),      -- %

    -- Outros
    quant_ativos            INTEGER,
    volatilidade            NUMERIC(14,2),
    num_cotistas            INTEGER,

    -- Taxas (armazenadas como texto pois incluem "% a.a")
    taxa_gestao             VARCHAR(30),
    taxa_performance        VARCHAR(30),
    taxa_administracao      VARCHAR(30),

    -- Metadados
    data_importacao         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para consultas frequentes
CREATE INDEX IF NOT EXISTS idx_fiis_setor ON fiis (setor);
CREATE INDEX IF NOT EXISTS idx_fiis_dy_12m ON fiis (dy_12m_acumulado DESC NULLS LAST);
CREATE INDEX IF NOT EXISTS idx_fiis_liquidez ON fiis (liquidez_diaria DESC NULLS LAST);

COMMENT ON TABLE fiis IS 'Dados de Fundos de Investimento Imobiliário (FIIs) importados do portal FIIs.com.br';
COMMENT ON COLUMN fiis.ticker IS 'Código de negociação do FII na B3';
COMMENT ON COLUMN fiis.setor IS 'Segmento de atuação do fundo';
COMMENT ON COLUMN fiis.preco_atual IS 'Preço atual da cota em R$';
COMMENT ON COLUMN fiis.liquidez_diaria IS 'Volume médio diário negociado em R$';
COMMENT ON COLUMN fiis.p_vp IS 'Relação Preço / Valor Patrimonial';
COMMENT ON COLUMN fiis.ultimo_dividendo IS 'Valor do último dividendo pago por cota em R$';
COMMENT ON COLUMN fiis.dividend_yield IS 'Dividend Yield mensal (%)';
COMMENT ON COLUMN fiis.dy_3m_acumulado IS 'Dividend Yield acumulado nos últimos 3 meses (%)';
COMMENT ON COLUMN fiis.dy_6m_acumulado IS 'Dividend Yield acumulado nos últimos 6 meses (%)';
COMMENT ON COLUMN fiis.dy_12m_acumulado IS 'Dividend Yield acumulado nos últimos 12 meses (%)';
COMMENT ON COLUMN fiis.dy_3m_media IS 'Dividend Yield médio mensal dos últimos 3 meses (%)';
COMMENT ON COLUMN fiis.dy_6m_media IS 'Dividend Yield médio mensal dos últimos 6 meses (%)';
COMMENT ON COLUMN fiis.dy_12m_media IS 'Dividend Yield médio mensal dos últimos 12 meses (%)';
COMMENT ON COLUMN fiis.dy_ano IS 'Dividend Yield acumulado no ano (%)';
COMMENT ON COLUMN fiis.variacao_preco IS 'Variação do preço da cota (%)';
COMMENT ON COLUMN fiis.rentab_periodo IS 'Rentabilidade no período (%)';
COMMENT ON COLUMN fiis.rentab_acumulada IS 'Rentabilidade acumulada (%)';
COMMENT ON COLUMN fiis.patrimonio_liquido IS 'Patrimônio líquido do fundo em R$';
COMMENT ON COLUMN fiis.vpa IS 'Valor Patrimonial por Ação/Cota em R$';
COMMENT ON COLUMN fiis.p_vpa IS 'Preço sobre Valor Patrimonial por Ação';
COMMENT ON COLUMN fiis.dy_patrimonial IS 'Dividend Yield patrimonial (%)';
COMMENT ON COLUMN fiis.variacao_patrimonial IS 'Variação patrimonial (%)';
COMMENT ON COLUMN fiis.rentab_patr_periodo IS 'Rentabilidade patrimonial no período (%)';
COMMENT ON COLUMN fiis.rentab_patr_acumulada IS 'Rentabilidade patrimonial acumulada (%)';
COMMENT ON COLUMN fiis.quant_ativos IS 'Quantidade de ativos no portfólio do fundo';
COMMENT ON COLUMN fiis.volatilidade IS 'Volatilidade do fundo';
COMMENT ON COLUMN fiis.num_cotistas IS 'Número de cotistas do fundo';
COMMENT ON COLUMN fiis.taxa_gestao IS 'Taxa de gestão (ex: 1,00 % a.a)';
COMMENT ON COLUMN fiis.taxa_performance IS 'Taxa de performance (ex: 20,00 % a.a)';
COMMENT ON COLUMN fiis.taxa_administracao IS 'Taxa de administração (ex: 0,50 % a.a)';
