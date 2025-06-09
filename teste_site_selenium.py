from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configurações
CHROMEDRIVER_PATH = './C:/teste_site_selelenium'
BASE_URL = 'https://www.arvel.com.br/'

driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

def acessar_pagina(url):
    driver.get(url)
    time.sleep(2)
    driver.get_screenshot_as_file('teste-evidencias10.png')


def testar_formulario_cadastro():

    print("Testando formulário de cadastro...")
    acessar_pagina(BASE_URL + 'cadastre-se/')
    # Campos observados na página
    nome = wait.until(EC.presence_of_element_located((By.NAME, 'FNAME')))
    email = driver.find_element(By.NAME, 'EMAIL')

    nome.send_keys('Teste Automático')
    email.send_keys('teste@exemplo.com')
    email.send_keys(Keys.RETURN)
    time.sleep(3)
    print("Formulário de cadastro submetido.")
    driver.get_screenshot_as_file('teste-evidencias20.png')

def testar_formulario_fale_conosco():
    print("Testando formulário de fale conosco...")
    acessar_pagina(BASE_URL + 'fale-conosco/')

    # Aceita o aviso de cookies via JS (caso ele esteja ativo mas invisível)
    driver.execute_script("document.cookie = 'cookie_notice_accepted=true; path=/';")
    driver.refresh()
    time.sleep(2)

    nome = wait.until(EC.presence_of_element_located((By.NAME, 'cf7s-name')))
    email = driver.find_element(By.NAME, 'cf7s-email-address')
    mensagem = driver.find_element(By.NAME, 'cf7s-message')

    nome.send_keys('Teste Automático')
    email.send_keys('teste@exemplo.com')
    mensagem.send_keys('Mensagem de teste automático.')
    # Localize e clique no botão enviar explicitamente pelo seletor da classe
    botao_enviar = driver.find_element(By.CSS_SELECTOR, 'input.wpcf7-form-control.wpcf7-submit.has-spinner')
    botao_enviar.click()

    time.sleep(2)
    print("Formulário fale conosco submetido.")

    # 🆕 Força scroll inicial para liberar visualização de mensagem
    driver.execute_script("window.scrollBy(0, 400);")
    time.sleep(1)

    # 🆕 Aguarda a mensagem de sucesso VISÍVEL
    msg_sucesso = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'wpcf7-response-output')))

    # Scroll específico até a mensagem
    driver.execute_script("arguments[0].scrollIntoView(true);", msg_sucesso)
    time.sleep(2)

    print("Mensagem de sucesso:", msg_sucesso.text.strip())
    driver.get_screenshot_as_file('teste-evidencias30.png')

def testar_navegacao_fiscal_tributario():
    print("Testando navegação na página Fiscal e Tributário...")
    acessar_pagina(BASE_URL + 'fiscal-e-tributario/')

    # Primeiro, coleta todos os textos e hrefs ANTES de navegar
    menu = wait.until(EC.presence_of_element_located((By.ID, 'menu-servicos')))
    abas = menu.find_elements(By.TAG_NAME, 'a')

    # Mapeia todos os elementos em uma lista imutável
    abas_info = [(a.text, a.get_attribute('href')) for a in abas]

    # Agora pode navegar sem quebrar o DOM

    c = 0
    for texto, href in abas_info:
        print(f"Visitando aba: {texto} - {href}")
        c++
        driver.get(href)
        time.sleep(2)
        driver.get_screenshot_as_file('teste-evidencias.png')

    print("Navegação Fiscal e Tributário concluída.")

def testar_navegacao_todas_paginas():
    print("Testando navegação em todas as páginas do menu principal...")
    acessar_pagina(BASE_URL)

    # Menu principal no topo, links <a> dentro de nav
    menu_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.mk-header-nav-container a')))

    # Pega os links únicos e válidos (que apontam para o próprio site)
    urls = set()
    for link in menu_links:
        href = link.get_attribute('href')
        if href and BASE_URL in href:
            urls.add(href)

    for url in urls:
        print(f"Acessando: {url}")
        driver.get(url)
        time.sleep(2)
        driver.get_screenshot_as_file('teste-evidencias.png')

    print("Navegação em todas as páginas concluída.")

def verificar_links_uteis():
    print("Verificando links úteis...")
    links_uteis = [
        'https://www.arvel.com.br/mei-precisa-de-inscricao-no-seu-estado/',
        'https://www.arvel.com.br/como-tirar-o-numero-do-pis-para-um-novo-empregado/',
        'https://www.arvel.com.br/4-golpes-mais-aplicados-utilizando-o-pix/'
    ]
    for link in links_uteis:
        driver.get(link)
        time.sleep(2)
        titulo = driver.title
        assert titulo != '', f"Erro: título vazio na página {link}"
        print(f"Link útil acessado com sucesso: {link}")
        driver.get_screenshot_as_file('teste-evidencias.png')
    print("Verificação dos links úteis concluída.")

try:
    acessar_pagina(BASE_URL)
    testar_formulario_cadastro()
    testar_formulario_fale_conosco()
    testar_navegacao_fiscal_tributario()
    testar_navegacao_todas_paginas()
    verificar_links_uteis()
finally:
    driver.quit()
    print("Todos os testes foram finalizados e navegador fechado.")
