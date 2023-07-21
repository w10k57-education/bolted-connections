import pandas as pd

def web_scraping(url, sep):
    sruby = []
    for i in url:
        temp = pd.read_html(i, thousands=sep)[2]
        temp.columns = temp.iloc[0]
        temp = temp.drop(0)
        temp.index = temp['OZNACZENIE'].astype(str)
        temp = temp.iloc[:-1, 1:]
        temp.columns = ['P [mm]', 'd [mm]', 'd2 [mm]', 'd1 [mm]', 'd3 [mm]', 'A [mm2]']
        temp = temp.replace(',', '.', regex=True)
        sruby.append(temp)

    pd.concat(sruby).to_csv('sruby.csv')


if __name__ == '__main__':
    linki = ['https://www.pkm.edu.pl/index.php/polocenia-obl/51-01010002',
       'https://www.pkm.edu.pl/index.php/polocenia-obl/52-01010003',
       'https://www.pkm.edu.pl/index.php/polocenia-obl/54-01010004',
       'https://www.pkm.edu.pl/index.php/polocenia-obl/55-01010005',
       'https://www.pkm.edu.pl/index.php/polocenia-obl/56-01010006',
       'https://www.pkm.edu.pl/index.php/polocenia-obl/57-01010007',
       'https://www.pkm.edu.pl/index.php/polocenia-obl/58-01010008']

    web_scraping(linki, '.')