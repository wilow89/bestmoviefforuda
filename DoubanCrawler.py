#!/usr/bin/python
# encoding:utf-8

"""
import ***
"""
import expanddouban
from bs4 import BeautifulSoup
import codecs

"""
init tuple of movie
we also can use class:

class Movie(object):
    name = ''
    rate = 0
    location = ''
    category = ''
    info_link = ''
    cover_link = ''
    def __init__(self, mvname, mvrate, mvlocation, mvcategory, mvinfo_link, mvcover_link):
        self.name = mvname
        self.rate = mvrate
        self.location = mvlocation
        self.category = mvcategory
        self.info_link = mvinfo_link
        self.cover_link = mvcover_link
    def writetofile(self, filename):
        with codecs.open('{}.csv'.format(filename), 'a', "utf-8") as f:
            f.write('{},{},{},{},{},{}\n'
                    .format(self.name, self.rate, self.location, self.category, self.info_link, self.cover_link))
                    
or dictionary
    name = ''
    rate = 0
    location = ''
    category = ''
    info_link = ''
    cover_link = ''
    movie = {'name':name, 'rate':rate, 'location':location, 'category':category,
            'info_link':info_link, 'cover_link':cover_link}
or tuple
    name = ''
    rate = 0
    location = ''
    category = ''
    info_link = ''
    cover_link = ''
    movie = (name, rate, location, category, info_link, cover_link)

In this project I choose dictionary.
"""

"""
return a string corresponding to the URL of douban movie lists given category and location.
"""
def getMovieUrl(category = None, location = None):
    url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影'
    if category == '全部类型':
        category = None
    if location == '全部地区':
        location = None
    if category != None:
        url += ',' + category
    if location != None:
        url += ',' + location
    return url

"""
use movie class that we defined before in annotation
return movie info
"""
def getMovieInfo(item, lscategory, lslocation):
    name = item.find(class_ = 'title').string
    rate = item.find(class_ = 'rate').string
    location = lslocation
    category = lscategory
    info_link = item.get('href')
    cover_link = item.img.get('src')
    # movieinfo = Movie(name, rate, location, category, info_link, cover_link) when we use class
    # movieinfo = (name, rate, location, category, info_link, cover_link) when we use tuple
    movieinfo = {'name':name, 'rate':rate, 'location':location, 'category':category,
                 'info_link':info_link, 'cover_link':cover_link}
    return movieinfo

"""
return a list of Movie objects with the given category and location.
"""
def getMovies(category = None, location = None):
    # init list
    movielist = list()
    # get movie url
    url = getMovieUrl(category, location)
    # get all html info
    html = expanddouban.getHtml(url, True)
    # change html to a soup
    soup = BeautifulSoup(html, "html.parser")
    # find the first movie item
    item = soup.find(id = "app").find(class_ = "list-wp").find("a", recursive=False)
    while item != None:
    # get move info
        info = getMovieInfo(item, category, location)
    # add info to movie list
        movielist.append(info)
    # move to next movie item
        item = item.next_sibling
    # return list
    return movielist

"""
write list to file, filename is use for the file name that we store
"""
def writelisttofile(filename, movielist):
    with codecs.open('{}.csv'.format(filename), 'a', "utf-8") as f:
        for movie in movielist:
            # write movie info one by one
            f.write("{},{},{},{},{},{}\n".format(movie['name'], movie['rate'],
                    movie['location'], movie['category'],
                    movie['info_link'], movie['cover_link']))

"""

"""
def getalllocations():
    loclist = list()
    url = getMovieUrl('剧情', '大陆')
    html = expanddouban.getHtml(url, True)
    soup = BeautifulSoup(html, "html.parser")
    loc = soup.find(id = 'app').find(class_ = 'category').next_sibling.next_sibling.li
    while loc != None:
        loclist.append(loc.string)
        loc = loc.next_sibling
    return loclist

"""

"""
def writeratiotofile(filename, category, summarylist, howmany):
    with codecs.open('{}.txt'.format(filename), 'a', "utf-8") as f:
        f.write("In category {} which have {} movies in score 9-10.\n".format(category, summarylist[0][1]))
        for num in range(1, howmany+1):
            f.write("{}st: movies in {} have {} movies is {:.2%} percent\n"
                    .format(num, summarylist[num][0], summarylist[num][1], summarylist[num][1]/summarylist[0][1]))



"""
no use:

def getallcategorys(soup):
    catlist = list()
    cate = soup.find(id = 'app').find(class_ = 'category').next_sibling.li
    while cate != None:
        catlist.append(cate.string)
        cate = cate.next_sibling
    return catlist
"""

"""
test for myself:
print(getMovieUrl('剧情','美国'))
url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,剧情,美国"
html = expanddouban.getHtml(url, True)
movies[0] = ("肖申克的救赎",9.6,"美国","剧情","https://movie.douban.com/subject/1292052/","https://img3.doubanio.com/view/movie_poster_cover/lpst/public/p480747492.jpg")
print(movies)
print(getMovies('剧情','美国'))
print(writelisttofile("movie",getMovies('剧情','美国')))
print(len(getMovies('剧情','英国')))
url = getMovieUrl('剧情','大陆')
html = expanddouban.getHtml(url, True)
soup = BeautifulSoup(html, "html.parser")
print(getallcategorys(soup))
print(getalllocations(soup))
"""

"""
main test:
"""
"""
best_cates = ['剧情', '文艺', '科幻']
locations = getalllocations()
for category in best_cates:
    summary = dict()
    numofallmovies = 0
    for location in locations:
        movies = getMovies(category, location)
        thiscatemovies = len(movies)
        summary[location] = thiscatemovies
        if location != '全部地区':
            writelisttofile("movie", movies)
            numofallmovies += thiscatemovies
    summary['全部地区'] = numofallmovies
    summary = sorted(summary.items(), key = lambda item:item[1], reverse=True)
    writeratiotofile("output", category, summary, 3)
    del summary
"""
i = 0.6934
print("{:.2%}".format(i))