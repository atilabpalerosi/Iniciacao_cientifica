#region INFORMAÇÕES DO PROJETO
# ==========================================================
# PROJETO: Scraping de Cursos Online (Hotmart/Udemy)
# AUTOR: Átila Baeza Palerosi
# DATA: 2026-04-07
# VERSÃO: 1.0
# ==========================================================

# DESCRIÇÃO:
# Script para coleta de dados de cursos online (título, descrição,
# categoria, preço, métricas e URL), com exportação para arquivo CSV.

# FUNCIONALIDADES:
# - Coleta dados de múltiplas URLs informadas manualmente
# - Trata ausência de dados (alunos, avaliações, nota)
# - Converte valores para formato numérico
# - Salva os dados em CSV (UTF-8 compatível com Excel)

# HISTÓRICO DE VERSÕES:
# v2.0 (2026-04-07)
# → Implementação inicial do scraping funcional
# → Inclusão de loop para múltiplas URLs
# → Tratamento de exceções (NoSuchElementException)
# → Correção de encoding para Excel (utf-8-sig)
# endregion

# 1. Importar o Selenium
# Importa o Selenium → permite controlar o navegador.
from selenium import webdriver

# Permite escolher como localizar elementos (CSS, XPath, etc.). 
# Vamos colocar um import time para dar tempo da página carregar    
from selenium.webdriver.common.by import By
import time

# Import de exceção para tratar cursos que não tem algum elemento na página
from selenium.common.exceptions import NoSuchElementException

# Importando a codificação em UTF-8
import sys
sys.stdout.reconfigure(encoding="utf-8")

# Para trabalhar com caminhos de arquivos no sistema
import os

# Importando editor de CSV
import csv

# ---------> CRIANDO ARQUIVO CSV

# Cabeçalho do arquivo CSV
cabecalho = ["titulo", "descricao", "categoria", "preco", "numero_alunos", 
             "numero_aulas", "duracao_horas", "numero_avaliacoes", "nota", "url"]

# Depois de testes, vimos que o python salva o arquivo CSV em um diretório de trabalho. 
# Vamos forçá-lo a salvar no mesmo diretório do aqruivo .py

pasta_script = os.path.dirname(os.path.abspath(__file__))   # caminho do arquivo .py
caminho_csv = os.path.join(pasta_script, "cursos.csv")

# ---------> COMEÇANDO O WITH QUE FARÁ O CÓDIGO FUNCIONAR
# Criando arquivo "cursos.csv" em modo escrita e garantindo que não pulará linhas
with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo:

# Chamando ferramenta "writer" no modo CSV. Para evitar problemas com Excel em pt-br, 
# coloquei o limitador de colunas como ;
    writer = csv.writer(arquivo, delimiter=";")

# writer = csv.writer(arquivo) → caso prefira o original

# Escrevendo o cabeçalho
    writer.writerow(cabecalho)
    
# VARIÁVEIS

    url = ""
    opcao = ""
    
    # Abrir navegador, controlado pelo Python
    driver = webdriver.Chrome()
    
    
    # Esse while é importante porque controla a possibilidade do usuário colocar mais URLs
    
    while opcao != "N" and opcao != "n":
        url = input("Cole a url do curso: ")
        
        # abre nova aba
        driver.execute_script("window.open('');")
    
        # muda para a nova aba
        driver.switch_to.window(driver.window_handles[-1])
    
        # abre a URL nela
        driver.get(url)
        time.sleep(5)
        driver.minimize_window()
        
        # ---------> ELEMENTO: TÍTULO
    
        # 1. Pegar o título a partir do <h1> da página (geralmente é único)
        titulo = driver.find_element(By.TAG_NAME, "h1").text
        
        # 2. Exibir o título
        print(titulo)
        
        # ---------> ELEMENTO: DESCRIÇÃO
        
        # 1. Pegar todos os parágrafos da descrição
        # A ideia é pegar todos os <p> dentro desse bloco
        
        paragrafos = driver.find_elements(By.XPATH, "//div[contains(@class, '_w-full')]//p")
        
        # 2. Juntar todos os parágrafos em uma única string
        descricao = " ".join([p.get_attribute("innerText") for p in paragrafos])
        
        # 3. Mostrar
        print(descricao)
        
        # ---------> ELEMENTO: CATEGORIA
    
        # 1. Pegar a categoria
        # Procura o <span> pela classe específica e pega o texto visível
        
        categoria = driver.find_element(By.XPATH, "//span[contains(@class, 'breadcrumbs__category-label')]").text
        
        # 2. Mostrar
        print(categoria)
        
        # ---------> ELEMENTO: PREÇO DO CURSO
    
        # 1. Encontrar onde o preço está na tela
        # Procura um elemento <span> que contenha “R$”
        # .text pega o texto visível → "R$ 197,00"
        
        preco = driver.find_element(By.XPATH, "//span[contains(text(), 'R$')]").text
        
        # 2. Mostrar o preço bruto
        print(preco)
        
        # 3. Remover símbolos e espaços
        # Remove "R$"
        # .strip() remove espaços extras
        
        preco_limpo = preco.replace("R$", "").strip()
        
        # 7. Ajustar formato numérico
        # Remove separador de milhar (.)
        # Troca vírgula por ponto (padrão Python)
        
        preco_limpo = preco_limpo.replace(".", "").replace(",", ".")
        
        # 8. Converter para número
        # Converte de string para número decimal (float)
        
        preco_num = float(preco_limpo)
        
        # 9. Mostrar resultado final
        print(preco_num)
        
        # ---------> ELEMENTO: NÚMERO DE AULAS/DURAÇÃO DO CURSO
    
        # As duas informações estão no mesmo elemento, o que torna a extração bem mais fácil
        # Porém, nem todas as páginas têm "aulas e horas" — algumas têm só "horas"
        
        # 1. Pegar o texto pelo aria-label (mais confiável)
        info = driver.find_element(
            By.XPATH,
            "//div[contains(@aria-label, 'aulas') or contains(@aria-label, 'horas')]"
        ).get_attribute("aria-label")
        
        # 2. Separar as partes (quando houver "e")
        partes = info.split(" e ")
        
        # 3. Extrair corretamente, tratando os dois casos possíveis
        
        # Caso 1: tem aulas E horas
        if len(partes) == 2:
            numero_aulas = int(partes[0].split()[0])   # ex: "60 aulas"
            duracao = int(partes[1].split()[0])        # ex: "30 horas"
        
        # Caso 2: tem apenas horas
        else:
            numero_aulas = None                        # não há informação de aulas
            duracao = int(partes[0].split()[0])        # ex: "160 horas"
        
        # 4. Imprimir (para teste)
        print(numero_aulas)
        print(duracao)
        
        # ---------> ELEMENTO: NÚMERO DE ALUNOS
    
        # 1. Pegar o texto
        # Procura um <div> que contenha “estudantes” → Resultado esperado: "+4200 estudantes"
        
        # .text nem sempre funciona, pois às vezes o dado está em um atributo
        # Aqui usamos aria-label (comum em scraping)
        
        # Nem todo curso mostra quantidade de estudantes.
        # Então, primeiro tentamos pegar o dado; se ele não existir, deixamos vazio.
        
        try:
            # 1. Pegar o texto
            alunos = driver.find_element(By.XPATH, "//div[contains(@aria-label, 'estudantes')]").get_attribute("aria-label")
        
            # 2. Remover texto desnecessário
            alunos_limpo = alunos.replace("estudantes", "").replace("+", "").strip()
        
            # 3. Converter para número
            numero_alunos = int(alunos_limpo)
        
        except NoSuchElementException:
            numero_alunos = None
        
        # 4. Mostrar resultado final
        print(numero_alunos)
        
        # ---------> ELEMENTO: NÚMERO DE AVALIAÇÕES
        
        # Nem todo curso mostra quantidade de avaliações.
        # Então, primeiro tentamos pegar o dado; se ele não existir, deixamos vazio.
        
        try:
            # 1. Pegar o texto
            avaliacoes = driver.find_element(By.XPATH, "//span[contains(@class, 'total-reviews')]").text
        
            # 2. Extrair os parênteses
            avaliacoes_limpo = avaliacoes.replace("(", "").replace(")", "")
        
            # 3. Converter para número
            numero_avaliacoes = int(avaliacoes_limpo)
        
        except NoSuchElementException:
            numero_avaliacoes = None
        
        # 4. Imprimir
        print(numero_avaliacoes)
        
        # ---------> ELEMENTO: NOTA DO CURSO
    
        try:
            # 1. Pegar a nota
            nota = driver.find_element(By.XPATH, "//span[contains(@class, 'rating-total')]").text
        
            # 2. Converter para número
            nota = float(nota)
        
        except NoSuchElementException:
            nota = None
        
        # 3. Testar
        print(nota)
        
        # ---------> ELEMENTO: ENDEREÇO DA PÁGINA
        
        # 1. Pegar a URL atual
        url = driver.current_url
        
        # 2. Exibir
        print(url)
        
        # ---------> ESCREVENDO A LINHA
        
        linha = [titulo, descricao, categoria, preco_num, numero_alunos, numero_aulas, 
            duracao, numero_avaliacoes, nota, url]
            
        writer.writerow(linha)
        
        opcao = input("Deseja incluir mais algum curso (S/N)?: ")

# ENCERRANDO O PROGRAMA
print("\nArquivo criado com sucesso.")
input("Pressione ENTER para encerrar...")
driver.quit()