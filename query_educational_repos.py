
from playwright.sync_api import sync_playwright
from lxml import html
import time
import pandas as pd

user_dir = '/tmp/playwright'


def search_repos(query):
  with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(user_dir, headless=False, slow_mo=1)
    page = browser.new_page()
    page.goto("https://pt.khanacademy.org/", wait_until='domcontentloaded')

    page.click("text=Pesquisar")
    page.fill("[data-test-id=\"page-search-box\"]", f'{query}')
    page.press("[data-test-id=\"page-search-box\"]", "Enter")
    

    time.sleep(5)
    
    #page.click("[aria-label=\"Página\\ 2\"]")

    tree = page.content()
    tree = html.fromstring(page.content())

    #-------------------
    #--------scratch.mit

    page.goto("https://scratch.mit.edu/", wait_until='domcontentloaded')
      # Click [placeholder="Pesquisa"]
    page.click("[placeholder=\"Pesquisa\"]")
    # Fill [placeholder="Pesquisa"]
    page.fill("[placeholder=\"Pesquisa\"]", f'{query}')
    # Press Enter
    page.press("[placeholder=\"Pesquisa\"]", "Enter")
    
    time.sleep(5)
    tree = page.content()
    tree = html.fromstring(page.content())


    links_khan = tree.xpath('//div[@class= "gs-title"]//@href')
    links_scratch = tree.xpath('//div[@class = "thumbnail-title"]//@href')

    links_scratch = ['https://scratch.mit.edu' + x for x in links_scratch if '/users' not in x]

    dicionario = {'khan academy': links_khan, 'scratch': links_scratch}
    
    scratch = {}
    
    
    for item in links_scratch:
      page.goto(item, wait_until='domcontentloaded')
      time.sleep(5)
      tree = page.content()
      tree = html.fromstring(page.content())
      
      item_dict = {}
      
      item_dict['publisher'] = 'https://scratch.mit.edu/'
      item_dict['creator'] =  tree.xpath("//div[@class = 'title']//a/text()")
      item_dict['title'] = tree.xpath("//div[@class = 'title']//div/text()")
      item_dict['description'] =  tree.xpath( "//div[@class = 'project-description']/text()")
      item_dict['date'] = tree.xpath("//div[@class = 'share-date']//span/text()")
      item_dict['identifier'] = item

      scratch[item] = item_dict

  return scratch


dicionario = search_repos("algebra")

df = pd.DataFrame.from_dict(dicionario)

df.to_csv(index=False)




