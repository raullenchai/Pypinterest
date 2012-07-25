import urllib, urllib2, cookielib, httplib
import os, re
from BeautifulSoup import BeautifulSoup




class pypinterestError(Exception):
    def __init__(self, description):
        self.description = description

    def __str__(self):
        return self.description




"""Workaround for using DELETE with urllib2"""
class RequestWithMethod(urllib2.Request):
    def __init__(self, url, method, data=None, headers={},\
        origin_req_host=None, unverifiable=False):
        self._method = method
        urllib2.Request.__init__(self, url, data=None, headers={},\
                 origin_req_host=None, unverifiable=False)

    def get_method(self):
        return self._method



"""Main wrapper"""
class Client(object):
    def __init__(self, email, username, password, useragent=r'Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)'):
            self.email = email
            self.username = username
            self.password = password
            self.csrf = -1
            self.cj = None
            self.useragent = useragent
            self.islogin = False
            self.base = r'https://pinterest.com'

    """Basic Authenticaiton"""
    def auth(self):
        if self.islogin == False:
            url = self.base + r'/login/'
            cj = cookielib.LWPCookieJar()
            if os.path.isfile(self.username+'.cookie'):
                cj.revert(self.username+'.cookie', False, False)

                #check if it is expired
                for x in cj:
                    if x.name == 'csrftoken':
                        self.csrf = x.value
                        self.cj = cj

                #print 'Login successful via cookie'
                self.islogin = True
                return

            else:
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
                try:
                    login_form = BeautifulSoup(opener.open(url).read())
                except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
                    raise pinpinpinError('Error in login(): ' + str(e))

                csrf = login_form.find('input', attrs={'name': 'csrfmiddlewaretoken'}).attrMap

                opener.addheaders = [
                                ("User-agent", self.useragent),
                                ('Content-Type', 'application/x-www-form-urlencoded'),
                                ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
                                ("Accept-Encoding", "gzip, deflate"),
                                ('Referer', 'http://pinterest.com/'),
                                ('X-CSRFToken', csrf['value'])]
                
                login_data = urllib.urlencode({'email' : self.email, 'password' : self.password, 'csrfmiddlewaretoken':csrf['value']})

                try:
                    req = urllib2.Request(url, login_data)
                    raw_html = opener.open(req).read()
                except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
                    raise pinpinpinError('Error in login(): ' + str(e))

                #test if the login was successful
                for c in cj:
                    print c
                    if (c.name == '_pinterest_sess') and len(c.value)>160:  #success login returns a longer string, but it is hard to tell exactly TODO
                        #print 'Login successful'
                        self.islogin = True
                        cj.save(self.username+'.cookie', False, False)
                        self.csrf = csrf['value']
                        self.cj = cj
                        return

                #print 'Login failed'
                raise pinpinpinError('Error in login(): ' + str(e))
                return
        else:
            return


    """Read boards from the user"""
    def getboards(self):
        self.auth()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        opener.addheaders = [
                        ("User-agent", self.useragent),
                        ('Content-Type', 'application/x-www-form-urlencoded'),
                        ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
                        ('Referer', 'http://pinterest.com/')]
        try:
            req = urllib2.Request(self.base + r'/' + self.username)
            data = opener.open(req).read()
        except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
            raise pypinterestError('Error in getboards():'+ str(e))
            return None

        boardnums = list()
        boardnames = list()

        for x in re.findall(r'<li data="[^/]*</span>', data):
            for y in re.findall(r'<li data="[0-9]*">', x):
                boardnums.append( y.replace('<li data="','').replace('">', '').strip() )
            for y in re.findall(r'<span>[^<]*</span>', x):
                boardnames.append( y.replace('<span>','').replace('</span>', '').strip() )

        boards = dict()
        for x in boardnames:
            boards[x] = boardnums[boardnames.index(x)]

        return boards


    """Create board for the user"""
    def createboard(self, boardname, boardcategory='other'):
        self.auth()
        if boardcategory not in set(['architecture', 'art', 'cars_motorcycles', 'design', 'diy_crafts', 'education', 'film_music_books', 'fitness', 'food_drink', 'gardening', 'geek', 'hair_beauty', 'history', 'holidays', 'home', 'humor', 'kids', 'mylife', 'women_apparel', 'men_apparel', 'outdoors', 'people', 'pets', 'photography', 'prints_posters', 'products', 'science', 'sports', 'technology', 'travel_places', 'wedding_events', 'other']):
            boardcategory = 'other'

        url = self.base + r'/board/create/'
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
                                    'collaborator': 'me'})
        try:
            req = urllib2.Request(url, data)
            status = opener.open(req).read()
        except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
            raise pypinterestError('Error in createboard():'+ str(e))
            return None
        
        return status


    """Delete a board"""
    def deleteboard(self, boardname):
        self.auth()
        url = self.base + r'/' + self.username + r'/' + boardname + r'/' + 'settings/'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        opener.addheaders = [
                    ('X-Requested-With', 'XMLHttpRequest'),
                    ('X-CSRFToken', self.csrf),
                    ("User-agent", self.useragent),
                    ("Accept", "application/json, text/javascript, */*; q=0.01"),
                    ('Referer', self.base + self.username + r'/' + boardname + r'/' + 'settings/'),
                    ("Accept-Encoding", "gzip,deflate,sdch"),
                    ("Accept-Language", "en-US,en;q=0.8"),
                    ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')]
        try:
            req = RequestWithMethod(url, 'DELETE')
            status = opener.open(req).read()
        except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
            raise pypinterestError('Error in deleteboard():'+ str(e))
            return None

        return status



    """Search for pins by a keyword, infinite scroll supported"""
    def searchpins(self, keyword, page_num=1):
        keyword = re.sub('\s *', '+', keyword)
        postids = list()
        for page in xrange(page_num):
            try:
                data = urllib2.urlopen(self.base + r'/search/?q=' + keyword + '&page=' + str(page+1)).read()
            except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
                break
                #raise pypinterestError('Error in searchpins():'+ str(e))

            _tmp_postids = list(set(re.findall(r'<div class="pin" data-id="\d*" ', data)))
            postids += [_tmp_postid.replace('<div class="pin" data-id="','').replace('" ','').strip() for _tmp_postid in _tmp_postids]

        return postids


    """Read contents from a pin"""
    def readpin(self, pinid):
        url = self.base + r'/pin/' + pinid + '/'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        opener.addheaders = [
                        ("User-agent", self.useragent),
                        ('Content-Type', 'application/x-www-form-urlencoded'),
                        ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
                        ('Referer', 'http://pinterest.com/')]
        try:
            req = urllib2.Request(url)
            data = opener.open(req).read()
        except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
            raise pypinterestError('Error in readpin():'+ str(e))
            return None

        info = dict()

        for x in re.findall(r'<meta property="og:title" content="[^>]*/>', data):
            info['title'] = x.replace(r'<meta property="og:title" content="', '').replace('"/>','').strip()
        for x in re.findall(r'<meta property="og:description" content="[^>]*/>', data):
            info['description']  = x.replace(r'<meta property="og:description" content="', '').replace('"/>','').strip()
        for x in re.findall(r'<meta property="og:image" content="[^>]*/>', data):
            info['image'] = x.replace(r'<meta property="og:image" content="', '').replace('"/>','').strip()
        for x in re.findall(r'<meta property="pinterestapp:pinboard" content="[^>]*/>', data):
            info['pinboard'] = x.replace(r'<meta property="pinterestapp:pinboard" content="', '').replace('"/>','').strip()
        for x in re.findall(r'<meta property="pinterestapp:pinner" content="[^>]*/>', data):
            info['pinner'] = x.replace(r'<meta property="pinterestapp:pinner" content="', '').replace('"/>','').strip()
        for x in re.findall(r'<meta property="pinterestapp:source" content="[^>]*/>', data):
            info['source'] = x.replace(r'<meta property="pinterestapp:source" content="', '').replace('"/>','').strip()
        for x in re.findall(r'<meta property="pinterestapp:likes" content="[^>]*/>', data):
            info['likes'] = x.replace(r'<meta property="pinterestapp:likes" content="', '').replace('"/>','').strip()
        for x in re.findall(r'<meta property="pinterestapp:repins" content="[^>]*/>', data):
            info['repins'] = x.replace(r'<meta property="pinterestapp:repins" content="', '').replace('"/>','').strip()
        for x in re.findall(r'<meta property="pinterestapp:comments" content="[^>]*/>', data):
            info['comments'] = x.replace(r'<meta property="pinterestapp:comments" content="', '').replace('"/>','').strip()
        for x in re.findall(r'<meta property="pinterestapp:actions" content="[^>]*/>', data):
            info['actions'] = x.replace(r'<meta property="pinterestapp:actions" content="', '').replace('"/>','').strip()

        return info


    """Post a pin"""
    def pin(self, boardno, postname, pic_url, link=' ', content=' '):
        self.auth()
        url = self.base + r'/pin/create/bookmarklet/'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

        myrefer = self.base + r'/pin/create/bookmarklet/?' + \
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
        
        data = urllib.urlencode({'board' : boardno, 
                                    'title' : postname, 
                                    'media_url': pic_url,
                                    'url': link,
                                    'caption': content,
                                    'csrfmiddlewaretoken': self.csrf})
        try:
            req = urllib2.Request(url, data)
            opener.open(req).read()
            status = 'Pinned!'
        except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
            raise pypinterestError('Error in pin():' + str(e))
            return None

        return status


    """Delete a pin"""
    def deletepin(self, pinid):
        self.auth()
        url = self.base + r'/pin/' + pinid + r'/delete/'
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        opener.addheaders = [
                    ('X-Requested-With', 'XMLHttpRequest'),
                    ('X-CSRFToken', self.csrf),
                    ("User-agent", self.useragent),
                    ("Accept", "application/json, text/javascript, */*; q=0.01"),
                    ('Referer', self.base + r'/pin/' + pinid + r'/edit'),
                    ("Accept-Encoding", "gzip,deflate,sdch"),
                    ("Accept-Language", "en-US,en;q=0.8"),
                    ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')]
        try:
            req = urllib2.Request(url, urllib.urlencode({}))
            status = opener.open(req).read()
        except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
            raise pypinterestError('Error in deletepin():'+ str(e))
            return None

        return status


    """Repin a pin"""
    def repin(self, boardno, pinid, content):
        self.auth()
        url = self.base + r'/pin/' + pinid + r'/repin/'
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
        data = urllib.urlencode({ 'board' : boardno, 
                                        'id' : pinid, 
                                        'tags' : '', 
                                        'replies': '',
                                        'details': content,
                                        'buyable': '',
                                        'csrfmiddlewaretoken':self.csrf})
        try:
            req = urllib2.Request(url, data)
            status = opener.open(req).read()
        except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
            raise pypinterestError('Error in repin():'+ str(e))
            return None

        return status


    """Like a particular pin"""
    def like(self, pinid):
        self.auth()
        url = self.base + r'/pin/' + pinid + r'/like/'
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
            req = urllib2.Request(url)
            status = opener.open(req).read()
        except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
            raise pypinterestError('Error in like():'+ str(e))
            return None

        return status


    """UnLike a particular pin"""
    def unlike(self, pinid):
        self.auth()
        url = self.base + r'/pin/' + pinid + r'/like/'
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

        data = urllib.urlencode({ 'unlike' : '1' })
        try:
            req = urllib2.Request(url, data)
            status = opener.open(req).read()
        except (urllib2.URLError, urllib2.HTTPError, httplib.HTTPException), e:
            raise pypinterestError('Error in unlike():'+ str(e))
            return None

        return status