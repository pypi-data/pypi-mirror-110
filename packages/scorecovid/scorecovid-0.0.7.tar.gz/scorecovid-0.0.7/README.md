# score-covid-19-policy
You must create a file called countries for scoring individual policies of countries.

Country names must be separated by comma.
<pre>
$ cat countries
South Korea,India,Brazil,France,New Zealand,Taiwan,Sweden,Japan,United States,Canada,United Kingdom,Israel
</pre>

# How to install and run scorecovid
<pre>
$ pip install scorecovid

$ scorecovid
score is created in result.csv
date is  2021-06-11
                deaths  population  score
country
New Zealand         26           4      6
Taiwan             385          23     16
South Korea       1982          51     38
Japan            13936         126    110
India           367081        1380    266
Canada           25863          37    699
Israel            6428           8    803
Sweden           14574          10   1457
France          110506          65   1700
United States   599472         331   1811
United Kingdom  128148          67   1912
Brazil          484235         212   2284

</pre>

# How to handle errors
<pre>
For example, "ImportError: lxml not found, please install it"
$ pip install lxml

</pre>

# How scorecovid can score indivisual policies against covid-19?
Scoring of individual policies against covid-19 is calculated by dividing the total number of deaths due to covid-19 by the population (in millions).
The most recent values for total number of deaths and population are scraped from the Web sites.

# scorecovid.py
$ cat scorecovid.py
<pre>
import requests,re
import pandas as pd

def main():
 url='https://www.worldometers.info/world-population/population-by-country/'
 print('scraping population...')
 page=requests.get(url)
 df = pd.read_html(page.text)[0]
 df.columns.values[1]='Country'
 df.columns.values[2]='Population'
 #df = pd.read_html(page.text,flavor='html5lib')[0]
 df.to_csv('pop.csv')
 print('pop.csv was created')

 print('downloading total_deaths.csv file')
 import subprocess as sp
 sp.call("wget https://github.com/owid/covid-19-data/raw/master/public/data/jhu/total_deaths.csv",shell=True)
 p=pd.read_csv('total_deaths.csv')
 date=p['date'][len(p)-1]

#
#from urllib.request import Request, urlopen
#url='https://www.worldometers.info/coronavirus/#nav-today/'
#print('scraping deaths informationi...')
#req = Request(url, headers={'User-Agent': 'Firefox/76.0.1'})
#page = re.sub(r'<.*?>', lambda g: g.group(0).upper(), urlopen(req).read().decode('utf-8') )
#df = pd.read_html(page)[0]
#df.to_csv('deaths.csv')
#print('deaths.csv was created')
#

 print('countries file was read...')
 d=open('countries').read().strip()
 print('scoring the following ',len(d),' countries...')
 d=d.split(',')
 print(d)

 dd=pd.DataFrame(
  {
   "country": d,
   "deaths": range(len(d)),
   "population": range(len(d)),
   "score": range(len(d)),
  })

 pp=pd.read_csv('pop.csv')
 print('calculating scores of countries\n')
 print('score is created in result.csv')
 print('date is ',date)

 for i in d:
 # print(p[i][len(p)-1])
  dd.loc[dd.country==i,'deaths']=int(p[i][len(p)-1])
 # print(pp.loc[pp.Country==i,'Population'])
  dd.loc[dd.country==i,'population']=int(pp.loc[pp.Country==i,'Population']/1000000)
  dd.loc[dd.country==i,'score']=int(dd.loc[dd.country==i,'deaths']/dd.loc[dd.country==i,'population'])
 dd=dd.sort_values(by=['score'])
 dd.to_csv('result.csv',index=False)
 dd=pd.read_csv('result.csv',index_col=0)
 print(dd)
# sp.call("rm total_deaths.csv pop.csv",shell=True)

if __name__ == "__main__":
 main()
</pre>
