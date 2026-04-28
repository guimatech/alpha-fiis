const { Pool } = require("pg");

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false },
});

module.exports = async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Content-Type", "application/json; charset=utf-8");

  try {
    const result = await pool.query(
      "SELECT DISTINCT setor FROM fiis WHERE setor IS NOT NULL ORDER BY setor"
    );
    res.status(200).json(result.rows.map((r) => r.setor));
  } catch (err) {
    console.error("DB error:", err);
    res.status(500).json({ error: "Erro ao consultar setores" });
  }
};
