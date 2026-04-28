#!/usr/bin/env python3
"""
Script: coletar_fiis_sheets.py
Descrição: Coleta dados do Funds Explorer e envia diretamente para o Google Sheets do usuário.
"""

import json
import os
import time
from datetime import datetime

import gspread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÕES
# ─────────────────────────────────────────────────────────────────────────────

URL_RANKING = "https://www.fundsexplorer.com.br/ranking"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1rERvWHCStW6LW-Ii07oZ_U1dfWjlPdqsv0EeErk9n9o/edit"
CREDENTIALS_FILE = "credentials.json"
SHEET_NAME = "Dados_FIIs"

def criar_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    return driver

def coletar_dados(driver):
    print(f"[INFO] Acessando {URL_RANKING}...")
    driver.get(URL_RANKING)
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))
    time.sleep(5)

    print("[INFO] Extraindo dados da tabela...")
    js_script = """
    const table = document.querySelector('table');
    const rows = table.querySelectorAll('tr');
    const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent.trim());
    const allData = [];
    for (let i = 1; i < rows.length; i++) {
        const cells = rows[i].querySelectorAll('td');
        if (cells.length === 0) continue;
        allData.push(Array.from(cells).map(cell => cell.textContent.trim()));
    }
    return JSON.stringify({headers: headers, data: allData});
    """
    
    resultado = json.loads(driver.execute_script(js_script))
    return resultado["headers"], resultado["data"]

def atualizar_google_sheets(headers, data):
    print("[INFO] Conectando ao Google Sheets...")
    client = gspread.service_account(filename=CREDENTIALS_FILE)

    print(f"[INFO] Abrindo a planilha...")
    sh = client.open_by_url(SPREADSHEET_URL)
    
    try:
        worksheet = sh.worksheet(SHEET_NAME)
        print(f"[INFO] Aba '{SHEET_NAME}' encontrada. Limpando dados antigos...")
        worksheet.clear()
    except gspread.exceptions.WorksheetNotFound:
        print(f"[INFO] Aba '{SHEET_NAME}' não encontrada. Criando nova aba...")
        worksheet = sh.add_worksheet(title=SHEET_NAME, rows="1000", cols="40")

    content = [headers] + data
    print(f"[INFO] Enviando {len(data)} linhas para o Google Sheets...")
    # Usando a sintaxe correta do gspread 6.0+
    worksheet.update(values=content, range_name='A1', value_input_option='USER_ENTERED')
    
    print("[INFO] Formatando a planilha...")
    worksheet.freeze(rows=1)
    # Correção no formato da cor: o campo correto para cor de texto é 'foregroundColor' ou omitir 'color' dentro de textFormat dependendo da versão
    # Vamos usar um formato mais seguro
    worksheet.format("A1:AD1", {
        "backgroundColor": {"red": 0.1, "green": 0.3, "blue": 0.5},
        "textFormat": {
            "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0},
            "bold": True,
            "fontSize": 10
        },
        "horizontalAlignment": "CENTER"
    })
    
    # Ajustar largura das colunas
    try:
        worksheet.columns_auto_resize(0, len(headers))
    except:
        pass # Ignorar se falhar o redimensionamento
    
    print(f"[OK] Planilha atualizada com sucesso em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

def main():
    driver = None
    try:
        driver = criar_driver()
        headers, data = coletar_dados(driver)
        atualizar_google_sheets(headers, data)
        print("\n✅ Automação concluída com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
