#region INFORMAÇÕES DO PROJETO
# ==========================================================
# PROJETO: Coleta de dados para análise de engajamento
# AUTOR: Átila Baeza Palerosi
# ORIENTADOR: Arthur Schneider Figueira
# DATA: 2026-04-10
# VERSÃO: 2.3
# ==========================================================

# DESCRIÇÃO:
# Script de scraping para coleta de dados de cursos online,
# com geração de dataset estruturado em CSV.

# FUNCIONALIDADES:
# - Coleta dados de múltiplas URLs
# - Extrai métricas de engajamento (alunos, avaliações, nota)
# - Trata ausência de dados
# - Exporta resultados para CSV (utf-8-sig)

# OBSERVAÇÕES:
# Este script faz parte de um projeto de pesquisa voltado à
# análise de engajamento e evasão (churn) em cursos online.
# endregion

# region ----> IMPORTS
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
#endregion

# region ----> CRIANDO ARQUIVO CSV

# Cabeçalho do arquivo CSV
cabecalho = [
    "titulo",
    "descricao",
    "categoria",
    "subcategoria",
    "preco",
    "idioma",
    "numero_alunos",
    "numero_aulas",
    "duracao_horas",
    "quantidade_conteudos",
    "vantagens_descricao",
    "detalhes_descricao",
    "nome_instrutor",
    "tempo_plataforma",
    "numero_avaliacoes",
    "nota",
    "url"]

# Depois de testes, vimos que o python salva o arquivo CSV em um diretório de trabalho. 
# Vamos forçá-lo a salvar no mesmo diretório do aqruivo .py

pasta_script = os.path.dirname(os.path.abspath(__file__))   # caminho do arquivo .py
caminho_csv = os.path.join(pasta_script, "cursos.csv")
# endregion

# ----> WITH QUE FARÁ O CÓDIGO FUNCIONAR
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
        # driver.execute_script("window.open('');")
    
        # muda para a nova aba
        # driver.switch_to.window(driver.window_handles[-1])
    
        # abre a URL nela
        driver.get(url)
        time.sleep(5)
        driver.minimize_window()
        
        # region ----> ELEMENTO: TÍTULO
    
        # 1. Pegar o título a partir do <h1> da página (geralmente é único)
        titulo = driver.find_element(By.TAG_NAME, "h1").text
        
        # 2. Exibir o título
        print(titulo)
        #endregion
        
        # region ----> ELEMENTO: DESCRIÇÃO
        
        # 1. Pegar todos os parágrafos da descrição
        # A ideia é pegar todos os <p> dentro desse bloco
        
        blocos_descricao = driver.find_elements(By.XPATH,"//div[contains(@class, '_w-full') and contains(@class, '_line-height-lg') and contains(@class, '_text-gray-600')]")
        
        # 2. O primeiro bloco é a descrição do curso
        paragrafos = blocos_descricao[0].find_elements(By.TAG_NAME, "p")

        # 3. Juntar todos os parágrafos em uma única string
        descricao = " ".join([p.get_attribute("innerText") for p in paragrafos])

        # 4. Mostrar
        print(descricao)
        # endregion
        
        # region ----> ELEMENTO: CATEGORIA
    
        # 1. Pegar a categoria
        # Procura o <span> pela classe específica e pega o texto visível
        
        categoria = driver.find_element(By.XPATH, "//span[contains(@class, 'breadcrumbs__category-label')]").text
        
        # 2. Mostrar
        print(categoria)
        # endregion

        # region ----> ELEMENTO: SUBCATEGORIA

        # 1. Pegar todos os elementos que têm a classe da categoria/subcategoria
        categorias = driver.find_elements(By.XPATH, "//span[contains(@class, 'breadcrumbs__category-label')]")

        # 2. A subcategoria é o segundo elemento da lista
        subcategoria = categorias[1].text.strip()

        # 3. Mostrar (teste)
        print(subcategoria)
        # endregion
        
        # region ----> ELEMENTO: PREÇO DO CURSO
    
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
        # endregion

        # region ----> IDIOMA

        # Pegar todos os spans da página
        spans = driver.find_elements(By.TAG_NAME, "span")

        # Valor padrão
        idioma = ""

        # Procurar o idioma entre os textos possíveis
        for span in spans:
            texto = span.text.strip()

            if texto == "Português" or texto == "Español" or texto == "English":
                idioma = texto
                break

        print(idioma)

        # endregion
        
        # region ----> ELEMENTO: NÚMERO DE AULAS/DURAÇÃO DO CURSO
    
        # As duas informações estão no mesmo elemento, o que torna a extração bem mais fácil
        # Porém, nem todas as páginas têm "aulas e horas" — algumas têm só "horas"
        # E em alguns casos, o XPath pode capturar um texto inválido

        try:
            # 1. Pegar o texto pelo aria-label (mais confiável)
            # Limitamos a busca ao primeiro elemento encontrado
            info = driver.find_element(
                By.XPATH,
                "(//div[contains(@aria-label, 'aulas') or contains(@aria-label, 'horas')])[1]"
            ).get_attribute("aria-label")

            # 2. Separar as partes (quando houver "e")
            partes = info.split(" e ")

            # 3. Extrair corretamente, tratando os dois casos possíveis
            # Usamos try para evitar erro caso o texto não comece com número

            try:
                # Caso 1: tem aulas E horas
                if len(partes) == 2:
                    numero_aulas = int(partes[0].split()[0])   # ex: "60 aulas"
                    duracao = int(partes[1].split()[0])        # ex: "30 horas"

                # Caso 2: tem apenas horas
                else:
                    numero_aulas = None
                    duracao = int(partes[0].split()[0])        # ex: "160 horas"

            except:
                # Caso o texto seja inválido (ex: "Conteúdo")
                numero_aulas = None
                duracao = None

        except NoSuchElementException:
            # Caso o elemento não exista
            numero_aulas = None
            duracao = None

        # 4. Imprimir (para teste)
        print(numero_aulas)
        print(duracao)
        # endregion

        # region ----> ELEMENTO: QUANTIDADE DE CONTEÚDOS (AULAS)

        # A página possui uma aba chamada "Conteúdo"
        # Precisamos garantir que essa aba está ativa antes de coletar os dados

        try:
            # 1. Clicar na aba "Conteúdo"
            aba_conteudo = driver.find_element(By.XPATH,"//button[contains(., 'Conteúdo')]")
            aba_conteudo.click()
            time.sleep(2)

        except:
            # Caso não encontre (alguns cursos já abrem direto nessa aba)
            pass

        # 2. Buscar todos os elementos que representam cada conteúdo
        # Cada aula possui um <span class="accordion__section">01, 02, 03...</span>

        conteudos = driver.find_elements(By.XPATH,"//span[contains(@class, 'accordion__section')]")

        # 3. Contar quantos conteúdos existem
        quantidade_conteudos = len(conteudos)


        # 4. Mostrar (teste)
        print(quantidade_conteudos)
        # endregion
        
        # region ----> ELEMENTO: VANTAGENS

        try:
            # 1. Clicar na aba "Vantagens"
            aba_vantagens = driver.find_element(By.XPATH, "//button[contains(., 'Vantagens')]")
            aba_vantagens.click()
            time.sleep(2)

        except:
            # Caso não encontre (alguns cursos já abrem direto nessa aba)
            pass

        # 2. Pegar o bloco da aba vantagens
        bloco_vantagens = driver.find_element(
            By.XPATH,
            "//div[@id='panel-1']//div[contains(@class, '_w-full') and contains(@class, '_line-height-lg') and contains(@class, '_text-gray-600')]")

        # 3. Pegar os parágrafos desse bloco
        paragrafos_vantagens = bloco_vantagens.find_elements(By.TAG_NAME, "p")

        # 4. Juntar tudo em uma única string
        # Usamos textContent em vez de innerText porque o conteúdo pode estar oculto (aba não ativa)
        # innerText pode retornar vazio nesses casos; textContent garante a leitura do DOM

        # Unimos todos os textos da lista em uma única string separada por espaço
        lista_textos_vantagens = []

        # Criamos uma lista vazia para armazenar os textos extraídos
        for p in paragrafos_vantagens:

            # Pegamos o conteúdo textual do parágrafo
            # Usamos textContent porque funciona mesmo se o elemento estiver oculto
            texto = p.get_attribute("textContent").strip()

            # Adicionamos o texto na lista
            lista_textos_vantagens.append(texto)

        vantagens_descricao = " ".join(lista_textos_vantagens)

        # 5. Mostrar
        print(vantagens_descricao)
        # endregion

        # region ----> ELEMENTO: NOME E TEMPO DO INSTRUTOR

        # 1. Encontrar o bloco do instrutor
        bloco_instrutor = driver.find_element(
            By.XPATH,"//div[contains(@class, 'creator_info')]")

        # 2. Pegar as duas divs internas
        infos = bloco_instrutor.find_elements(By.TAG_NAME, "div")

        # 3. Extrair os dados
        nome_instrutor = infos[0].text.strip()
        tempo_plataforma = infos[1].text.split()[0]

        # 4. Mostrar (teste)
        print(nome_instrutor)
        print(tempo_plataforma)
        # endregion
        
        # region ----> ELEMENTO: NÚMERO DE ALUNOS
    
        # 1. Pegar o texto
        # Procura um <div> que contenha “estudantes”   
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
        # endregion
        
        # region ----> ELEMENTO: NÚMERO DE AVALIAÇÕES
        
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
        # endregion
        
        # region ----> ELEMENTO: NOTA DO CURSO
    
        try:
            # 1. Pegar a nota
            nota = driver.find_element(By.XPATH, "//span[contains(@class, 'rating-total')]").text
        
            # 2. Converter para número
            nota = float(nota)
        
        except NoSuchElementException:
            nota = None
        
        # 3. Testar
        print(nota)
        # endregion
        
        # region ----> ELEMENTO: ENDEREÇO DA PÁGINA
        
        # 1. Pegar a URL atual
        url = driver.current_url
        
        # 2. Exibir
        print(url)
        # endregion

        # region ----> ELEMENTO: DETALHES

        try:
            # 1. Clicar na aba "Detalhes"
            aba_detalhes = driver.find_element(By.XPATH,"//button[contains(., 'Detalhes')]")
            aba_detalhes.click()
            time.sleep(2)

        except:
            # Caso não encontre (alguns cursos já abrem direto nessa aba)
            pass

        # 2. Pegar o bloco da aba detalhes
        bloco_detalhes = driver.find_element(
            By.XPATH,"//div[@id='panel-2']//div[contains(@class, 'product-data')]")

        # 3. Pegar os textos relevantes dentro do bloco
        textos_detalhes = bloco_detalhes.find_elements(By.XPATH, ".//div[@aria-label] | .//p")

        # 4. Juntar tudo em uma única string
        # Usamos textContent em vez de innerText porque o conteúdo pode estar oculto 
        # (aba não ativa)

        # Criamos uma lista vazia para armazenar os textos extraídos
        lista_textos_detalhes = []

        # Criamos uma lista vazia para armazenar os textos extraídos
        for texto in textos_detalhes:

            # Pegamos o conteúdo textual do elemento
            # Usamos textContent porque funciona mesmo se o elemento estiver oculto
            conteudo = texto.get_attribute("textContent").strip()

            # Adicionamos o texto na lista
            lista_textos_detalhes.append(conteudo)

        # Adicionamos o texto na lista
        detalhes_descricao = " ".join(lista_textos_detalhes)

        # 5. Mostrar (teste)
        print(detalhes_descricao)
        # endregion
                
        # region ----> ESCREVENDO A LINHA

        # Durante testes, me deparei com um problema: algumas descrições podem começar
        # com caracteres que podem ser interpretados no Excel como fórmula. Então, vamos
        # alterar o texto para que ele comece com apóstrofo, que o Excel sempre 
        # interpretará como texto.

        if vantagens_descricao.startswith(("=", "+", "-", "@")):
            vantagens_descricao = "'" + vantagens_descricao
        
        linha = [titulo, descricao, categoria, subcategoria, preco_num, idioma, 
                 numero_alunos, numero_aulas, duracao, quantidade_conteudos, 
                 vantagens_descricao, detalhes_descricao, nome_instrutor, 
                 tempo_plataforma, numero_avaliacoes, nota, url]
            
        writer.writerow(linha)        
        opcao = input("Deseja incluir mais algum curso (S/N)?: ")
        # endregion

# ENCERRANDO O PROGRAMA
print("\nArquivo criado com sucesso.")
input("Pressione ENTER para encerrar...")
driver.quit()