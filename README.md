# Coletor de FIIs — Funds Explorer para Google Sheets

Script Python que coleta automaticamente os dados de ranking de Fundos Imobiliários (FIIs) do [Funds Explorer](https://www.fundsexplorer.com.br/ranking) e os envia diretamente para uma planilha do **Google Sheets**.

---

## O que o script faz?

1.  Acessa o site Funds Explorer em modo "invisível".
2.  Extrai todos os dados da tabela de ranking (541+ FIIs e 30 colunas).
3.  Conecta-se à API do Google Sheets usando uma conta de serviço.
4.  Cria ou atualiza uma aba chamada **"Dados_FIIs"** na sua planilha.
5.  Limpa os dados antigos e insere os novos, formatando o cabeçalho automaticamente.

---

## Como configurar na sua máquina

### 1. Pré-requisitos
- Python 3.8 ou superior instalado.
- Google Chrome instalado.
- O arquivo de credenciais do Google Cloud (`.json`) na mesma pasta do script.

### 2. Instalação
Execute o comando abaixo para instalar as bibliotecas necessárias:
```bash
pip install selenium gspread google-auth webdriver-manager
```

### 3. Configuração do Script
No arquivo `coletar_fiis_sheets.py`, verifique se as variáveis estão corretas:
- `SPREADSHEET_URL`: O link da sua planilha do Google Sheets.
- `CREDENTIALS_FILE`: O nome do seu arquivo JSON de credenciais (ex: `credentials.json`).
- `SHEET_NAME`: O nome da aba onde os dados serão salvos.

### 4. Execução
Para rodar a automação:
```bash
python coletar_fiis_sheets.py
```

---

## Vantagens desta versão
- **Direto ao Ponto:** Não precisa baixar arquivos Excel manualmente; os dados aparecem na nuvem.
- **Formatação Inteligente:** O script congela a primeira linha e aplica cores profissionais ao cabeçalho.
- **Tipagem de Dados:** Números e percentuais são enviados de forma que o Google Sheets os reconheça como valores numéricos (permitindo somas e gráficos imediatos).

---

*Desenvolvido para automatizar o monitoramento mensal de investimentos em FIIs.*


python coletar_fiis_sheets.py
# alpha-fiis
