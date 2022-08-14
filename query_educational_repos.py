
from playwright.sync_api import sync_playwright
from lxml import html
import time

user_dir = '/tmp/playwright'


def search_repos(query):
  with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(user_dir, headless=False, slow_mo=1000)
    page = browser.new_page()
    page.goto("https://pt.khanacademy.org/", wait_until='domcontentloaded')

    page.click("text=Pesquisar")
    page.fill("[data-test-id=\"page-search-box\"]", f'{query}')
    page.press("[data-test-id=\"page-search-box\"]", "Enter")
    

    time.sleep(5)
    
    #page.click("[aria-label=\"Página\\ 2\"]")

    tree = page.content()
    tree = html.fromstring(page.content())

    page.goto("https://scratch.mit.edu/", wait_until='domcontentloaded')
      # Click [placeholder="Pesquisa"]
    page.click("[placeholder=\"Pesquisa\"]")
    # Fill [placeholder="Pesquisa"]
    page.fill("[placeholder=\"Pesquisa\"]", f'{query}')
    # Press Enter
    page.press("[placeholder=\"Pesquisa\"]", "Enter")
    
    time.sleep(5)
    tree2 = page.content()
    tree2 = html.fromstring(page.content())


  resultados = tree.xpath('//div[@class= "gs-title"]//@href')
  resultados2 = tree2.xpath('//div[@class = "thumbnail-title"]//@href')

  resultados2 = ['https://scratch.mit.edu' + x for x in resultados2]

  dicionario = {'khan academy': resultados, 'scratch': resultados2}

  print(dicionario['khan academy'])
  print(dicionario['scratch'])



search_repos("algebra")
