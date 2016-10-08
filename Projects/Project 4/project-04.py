import sys
#sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/home/chong/anaconda2/lib/python2.7/site-packages')

# load the library
from bs4 import BeautifulSoup
import urllib2, requests
import pandas as pd, numpy as np

# to remove column limit (default is 50. Otherwise, we'll lose some info)
pd.set_option('max_colwidth',500)

def getjobs(page, salary, location = None, base_url = 'http://www.indeed.com/jobs?q=data+scientist+'):

    global df
    global joblinks
    global joblinks2
    
    if location == None:
        locurl = ''
    else:
        locurl = '&l=' + location
    starturl = '&jt=fulltime&sort=date&start=' + str(page)
    url = base_url + dollar(salary) + locurl + starturl # get full url 
    #print url
    
    contents = BeautifulSoup(urllib2.urlopen(url), "lxml")
    contentsElements = contents.find_all('div', attrs={'class' : '  row  result'}) 
    contentsElements.extend(contents.find_all('div', attrs={'class' : 'lastRow  row  result'}))
    
    if contentsElements == []:
        return False

    seen = 0
    
    # extract job information
    for elem in contentsElements:
        #variables
        link = "http://www.indeed.com" + elem.find('a').get('href')
        #if every job on the page has been seen before at that salary, 
        #quit and go to the next salary
        if (salary, location, link) in joblinks2:
            seen += 1
            #print seen
            if seen >= len(contentsElements):
                print url #this should be the last page
                return False
        else:
            joblinks2.add((salary, location, link))
        if link in joblinks:
            continue
        
        title = elem.find('a', attrs={'class':'turnstileLink'}).attrs['title']
        descr = elem.find('span', attrs={'class':'summary', 'itemprop':'description'}).getText().strip()
        
        # bunch of helper variables
        real_salary2 = ''
        real_salary3 = ''
        uprange = False
        location = elem.find('span', attrs={'itemprop':'addressLocality'}).getText()
        post_time = elem.find('span', attrs={'class':'date'}).getText()
        
        #salary
        try:
            real_salary = elem.find('nobr').getText().replace('a year','')
            for char in real_salary:
                if char.isdigit() and uprange == False:
                    real_salary2 += char
                elif char.isdigit() and uprange == True:
                    real_salary3 += char
                elif char == '-':
                    uprange = True
                elif char.isalpha():
                    break
        except AttributeError:
            real_salary = np.nan
            
        #company
        try:
            company = elem.find('span', attrs={'itemprop':'name'}).getText().strip() #strips off whitespace 
        except AttributeError:
            company = '-'

        # add a record of job info to our data frame
        joblinks2.add((salary, link))
        joblinks.add(link)
        df = df.append({'company': company, 
                        'title': title, 
                        'link': link, 
                        'post_time': post_time,
                        'description': descr,
                        'location': location,
                        'est_salary': salary,
                        'real_salary_lower': lint(real_salary2),
                        'real_salary_upper': lint(real_salary3)
                       }, ignore_index=True)
    
    #intermediate saves
    if page % 50 == 0: 
        df.to_csv('./indeed_companies_locs.csv', encoding='utf-8')

def lint(s):
    if s == '':
        return np.nan
    else:
        return int(s)
            
def dollar(num):
    thou = num/1000
    if thou > 0:
        return '%24' + str(thou) + '%2C' + str(num)[-3:]
    else:
        return '%24' + str(num)[-3:]

def location(s):
    ss = ''
    i = 0
    for i, char in enumerate(s):
        if not (char.isalpha() or char == ' ' or char == ','):
            return
        if char == ' ':
            ss += '+'
        else:
            ss += char
        if char == ',':
            ss += '+' + s[i+2:i+4]
            break
    return ss

df = pd.read_csv('/home/chong/Documents/Exercise-Book/Projects/Project 4/indeed_companies.csv', index_col = 0)
locations = pd.Series(map(location, df['location'].unique())).unique()


df = pd.DataFrame()
joblinks = set()
joblinks2 = set()

for num in range(200000,0,-10000):
    for location in locations:
        for page in range(0,9999,10):
            #display progress
            print num, location, page, '    ' , len(joblinks), len(joblinks2)
            if location == 'North+Chicago,+IL':
                pass
            if getjobs(page, num, location=location) == False:
                break


df.to_csv('./indeed_companies_locs.csv', encoding='utf-8')
print df