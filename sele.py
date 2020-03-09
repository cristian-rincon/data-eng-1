from selenium import webdriver
import pandas as pd
from pandas import ExcelWriter
from openpyxl.workbook import Workbook
pd.set_option('display.max_rows', 5, 'display.max_columns',
              None, 'display.width', None)

browser = webdriver.Firefox()
browser.get(
    'https://www.mismarcadores.com/futbol/chile/primera-division/resultados/')

aux_ids = browser.find_elements_by_css_selector(
    '.event__match.event__match--static.event__match--oneLine')
partidos = []
for aux in aux_ids:
    partidos.append([aux.find_elements_by_css_selector('.event__participant.event__participant')[0].text,
                     aux.find_element_by_css_selector(
                         '.event__scores.fontBold').text.replace('\n', ''),
                     aux.find_elements_by_css_selector(
                         '.event__participant.event__participant')[1].text,
                     aux.get_attribute('id')])


df = pd.DataFrame(partidos)
df.rename(columns={0: 'Casa', 1: 'R 90 min', 2: 'Visitante', 3: '', 4: 'rc1', 5: 'rc2', 6: 'rc3', 7: 'rc4', 8: 'rc5',
                   9: '', 10: 'rv1', 11: 'rv2', 12: 'rv3', 13: 'rv4', 14: 'rv5',
                   15: '', 16: 'lc1', 17: 'lc2', 18: 'lc3', 19: 'lc4', 20: 'lc5',
                   21: '', 22: 'lv1', 23: 'lv2', 24: 'lv3', 25: 'lv4', 26: 'lv5',
                   }, inplace=True)
df['id'] = df['id'].apply(lambda x: x.split('_')[2])
url_aux = 'https://www.mismarcadores.com/partido/'
df['link'] = url_aux + df['id'] + '/#h2h;overall'

writer = ExcelWriter('arch2.xlsx')
df.to_excel(writer, 'Hoja1')
writer.save()
