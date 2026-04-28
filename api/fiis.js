const { Pool } = require("pg");

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Content-Type", "application/json; charset=utf-8");

  const { setor, ordem, dir, limite, busca } = req.query;

  const colunasValidas = [
    "ticker","setor","preco_atual","liquidez_diaria","p_vp",
    "ultimo_dividendo","dividend_yield","dy_12m_acumulado",
    "dy_ano","variacao_preco","rentab_periodo","rentab_acumulada",
    "patrimonio_liquido","vpa","p_vpa","num_cotistas","volatilidade",
  ];

  const ordenarPor = colunasValidas.includes(ordem) ? ordem : "liquidez_diaria";
  const direcao = dir === "asc" ? "ASC" : "DESC";
  const max = Math.min(parseInt(limite) || 100, 1000);

  const conditions = [];
  const params = [];
  let idx = 1;

  if (setor) {
    conditions.push(`setor = $${idx++}`);
    params.push(setor);
  }
  if (busca) {
    conditions.push(`ticker ILIKE $${idx++}`);
    params.push(`%${busca}%`);
  }

  const where = conditions.length ? "WHERE " + conditions.join(" AND ") : "";

  params.push(max);

  const query = `
    SELECT ticker, setor, preco_atual, liquidez_diaria, p_vp,
           ultimo_dividendo, dividend_yield, dy_12m_acumulado,
           dy_ano, variacao_preco, patrimonio_liquido, vpa, p_vpa,
           num_cotistas
    FROM fiis
    ${where}
    ORDER BY ${ordenarPor} ${direcao} NULLS LAST
    LIMIT $${idx}
  `;

  try {
    const result = await pool.query(query, params);
    res.status(200).json(result.rows);
  } catch (err) {
    console.error("DB error:", err);
    res.status(500).json({ error: "Erro ao consultar banco de dados" });
  }
};
