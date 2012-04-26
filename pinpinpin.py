import urllib, urllib2, cookielib, httplib
import os, re
from urllib2 import Request, urlopen, URLError, HTTPError
from BeautifulSoup import BeautifulSoup
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from sets import Set






class pinpinpinError(Exception):
    """Base class for pinpinpin errors"""






class Client(object):
    """The main wrapper"""
    def __init__(self, email, username, password, useragent='Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'):
            self.email = email
            self.username = username
            self.password = password
            self.csrf = -1
            self.cj = None
            self.useragent = useragent
            self.islogin = False






    def login(self):
        """Basic Authenticaiton (No OAuth supported)"""
        login_url = 'https://pinterest.com/login/'
        cj = cookielib.LWPCookieJar()
        if os.path.isfile(self.username+'.cookie'):
            cj.revert(self.username+'.cookie', False, False)

            #TODO check if it is expired
            for x in cj:
                if x.name == 'csrftoken':
                    self.csrf = x.value
                    self.cj = cj

            print 'Login successful via cookie'
            self.islogin = True
            return

        else:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

            # need the CSRF token from the login form that allows one to login
            try:
                login_form = BeautifulSoup(opener.open(login_url).read())
            except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
                raise pinpinpinError('Error in login(): ' + str(e))

            csrf = login_form.find('input', attrs={'name': 'csrfmiddlewaretoken'}).attrMap

            # sign in by sending the correct credentials to the login form
            opener.addheaders = [
            				("User-agent", self.useragent),
            				('Content-Type', 'application/x-www-form-urlencoded'),
            				("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
                            ("Accept-Encoding", "gzip, deflate"),
            				('Referer', 'http://pinterest.com/'),
                            ('X-CSRFToken', csrf['value'])]
        	
            login_data = urllib.urlencode({'email' : self.email, 'password' : self.password, 'csrfmiddlewaretoken':csrf['value']})

            try:
                req = urllib2.Request(login_url, login_data)
                raw_html = opener.open(req).read()
            except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
                raise pinpinpinError('Error in login(): ' + str(e))

            #test if the login was successful
            for c in cj:
                if (c.name == '_pinterest_sess') and len(c.value)>160:  #success login returns a longer string
                    print 'Login successful'
                    self.islogin = True
                    cj.save(self.username+'.cookie', False, False)
                    self.csrf = csrf['value']
                    self.cj = cj
                    return

            print 'Login failed'
            return






    def getboards(self):
        """Read boards from the user"""
        if self.islogin == False:
            raise pinpinpinError('Error in getboards(): You are not logged in.')

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        opener.addheaders = [
                        ("User-agent", self.useragent),
                        ('Content-Type', 'application/x-www-form-urlencoded'),
                        ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
                        ('Referer', 'http://pinterest.com/')]
        try:
            req = urllib2.Request('https://pinterest.com/'+self.username)
            data = opener.open(req).read()
        except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
            raise pinpinpinError('Error in getboards():'+ str(e))


        myboardnos = list()
        myboardnames = list()

        for x in re.findall(r'<li data="[^/]*</span>', data):
            for y in re.findall(r'<li data="[0-9]*">', x):
                myboardnos.append( y.replace('<li data="','').replace('">', '').strip() )
            for y in re.findall(r'<span>[^<]*</span>', x):
                myboardnames.append( y.replace('<span>','').replace('</span>', '').strip() )

        myboards = dict()
        for x in myboardnames:
            myboards[x] = myboardnos[myboardnames.index(x)]
        return myboards






    def createboard(self, boardname, boardcategory='other'):
        """Create board for the user"""

        if self.islogin == False:
            raise pinpinpinError('Error in createboard(): You are not logged in.')

        if boardcategory not in Set(['architecture', 'art', 'cars_motorcycles', 'design', 'diy_crafts', 'education', 'film_music_books', 'fitness', 'food_drink', 'gardening', 'geek', 'hair_beauty', 'history', 'holidays', 'home', 'humor', 'kids', 'mylife', 'women_apparel', 'men_apparel', 'outdoors', 'people', 'pets', 'photography', 'prints_posters', 'products', 'science', 'sports', 'technology', 'travel_places', 'wedding_events', 'other']):
            boardcategory = 'other'

        create_url = 'http://pinterest.com/board/create/'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        opener.addheaders = [
                        ("User-agent", self.useragent),
                        ('Content-Type', 'application/x-www-form-urlencoded'),
                        ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
                        ("Accept-Encoding", "gzip, deflate"),
                        ("X-Requested-With", "XMLHttpRequest"),     # without this, 404 will happen
                        ('Referer', 'http://pinterest.com/'),
                        ('X-CSRFToken', self.csrf)]
        data = urllib.urlencode({   'name' : boardname, 
                                    'category' : boardcategory, 
                                    'collaborator': 'me'})      #TODO Add another pinner
        try:
            req = urllib2.Request(create_url, data)
            raw_html = opener.open(req).read()
        except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
            raise pinpinpinError('Error in createboard():'+ str(e))
        
        print '[',boardname, '] in [', boardcategory, '] has been created!'
        return True





    #TODO
    def deleteboard(boardid):
        pass






    def searchpins(self, keyword):
        """search for pins by a keyword"""
        #TODO scorll down to get more results

        keyword = re.sub('\s *', '+', keyword)

        try:
            response = urllib2.urlopen('http://pinterest.com/search/?q='+keyword)
            #headers = response.info()
            data = response.read()
        except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
            raise pinpinpinError('Error in searchpins():'+ str(e))


        postids = list(Set(re.findall(r'<div class="pin" data-id="\d*" ', data)))
        postids = [postid.replace('<div class="pin" data-id="','').replace('" ','').strip() for postid in postids]


        postcontents = list(Set(re.findall(r'" alt=".*" class="PinImageImg" style="height:', data)))
        postcontents = [postcontent.replace('" alt="','').replace('" class="PinImageImg" style="height:','').strip() for postcontent in postcontents]

        return postids, postcontents






    def post(self, boardno, postname, pic_url, link=' ', content=' '):
        """Post a pin"""

        if self.islogin == False:
            raise pinpinpinError('Error in post(): You are not logged in.')

        post_url = 'https://pinterest.com/pin/create/bookmarklet/'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

        myrefer = 'http://pinterest.com/pin/create/bookmarklet/?' + \
                    urllib.urlencode({'media' : pic_url, 
                                        'url' : link, 
                                        'title': postname,
                                        'is_video': 'false',
                                        'description': ''})

        opener.addheaders = [
                        ("User-agent", self.useragent),
                        ('Content-Type', 'application/x-www-form-urlencoded'),
                        ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
                        ('Referer', myrefer),
                        ("Accept-Encoding", "gzip,deflate,sdch"),
                        ("Accept-Language", "en-US,en;q=0.8"),
                        ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')]
        
        ad_data = urllib.urlencode({'board' : boardno, 
                                    'title' : postname, 
                                    'media_url': pic_url,
                                    'url': link,
                                    'caption': content,
                                    'csrfmiddlewaretoken': self.csrf})

        try:
            req = urllib2.Request(post_url, ad_data)
            raw_html = opener.open(req).read()
        except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
            raise pinpinpinError('Error in pinpin():' + str(e))

        print 'Posted!'





    #TODO
    def deletepost(postid):
        pass




    def repin(self, boardno, postid, content):
        """repin a pin"""

        if self.islogin == False:
            raise pinpinpinError('Error in repin(): You are not logged in.')

        repin_url = 'http://pinterest.com/pin/' + postid + '/repin/'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

        opener.addheaders = [
    					('X-Requested-With', 'XMLHttpRequest'),
    					('X-CSRFToken', self.csrf),
                        ("User-Agent", self.useragent),
                        ("Content-Type", "application/x-www-form-urlencoded"),
                        ("Accept", "application/json, text/javascript, */*; q=0.01"),
                        ('Referer', 'http://pinterest.com'),
                        ("Accept-Encoding", "gzip,deflate,sdch"),
                        ("Accept-Language", "en-US,en;q=0.8"),
                        ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')]

        repin_data = urllib.urlencode({ 'board' : boardno, 
                                        'id' : postid, 
                                        'tags' : '', 
                                        'replies': '',
                                        'details': content,
                                        'buyable': '',
                                        'csrfmiddlewaretoken':self.csrf})

        try:
            req = urllib2.Request(repin_url, repin_data)
            data = opener.open(req).read()
        except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
            raise pinpinpinError('Error in repin():'+ str(e))

    	print 'Repined'







    def like(self, postid):
        """Like someone's pin"""

        if self.islogin == False:
            raise pinpinpinError('Error in like(): You are not logged in.')

        like_url = 'http://pinterest.com/pin/'+postid+'/like/'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

        opener.addheaders = [
    					('X-Requested-With', 'XMLHttpRequest'),
    					('X-CSRFToken', self.csrf),
                        ("User-agent", self.useragent),
                        ("Accept", "application/json, text/javascript, */*; q=0.01"),
                        ('Referer', 'http://pinterest.com'),
                        ("Accept-Encoding", "gzip,deflate,sdch"),
                        ("Accept-Language", "en-US,en;q=0.8"),
                        ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')]

        try:
            req = urllib2.Request(like_url)
            data = opener.open(req).read()
        except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
            raise pinpinpinError('Error in like():'+ str(e))

        print 'Liked'



