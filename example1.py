from lib import pypinterest
import re
import operator

"""Check how pins are stored/distributed in Pinterest's cache servers"""
if __name__ == '__main__':

    #create a client instance, make sure hte email address, user name and password are correct
    myclient = pypinterest.Client('EMAIL', 'USERNAME', 'PASSWORD')
    stat = dict()

    for category in ['architecture', 'art', 'cars_motorcycles', 'design', 'diy_crafts', 'education', 'film_music_books', 'fitness', 'food_drink', 'gardening', 'geek', 'hair_beauty', 'history', 'holidays', 'home', 'humor', 'kids', 'mylife', 'women_apparel', 'men_apparel', 'outdoors', 'people', 'pets', 'photography', 'prints_posters', 'products', 'science', 'sports', 'technology', 'travel_places', 'wedding_events', 'other']:
        
        print 'gathering pins...'
        allpins =  myclient.getallpins(category, 0, 20)

        print 'read pins\' info...'
        for eachpin in allpins:
            try:
                url = myclient.readpin(eachpin)['image']
            except pypinterest.pypinterestError, e:
                continue

            host = re.sub('/upload/[^.]*', '', url).replace('http://', '').replace('https://', '')[:-4]
            if host in stat:
                stat[host] += 1
            else:
                stat[host] = 1

    for key, value in sorted(stat.iteritems(), key=lambda (k,v): (v,k)):
        print "%s: %s" % (key, value)
    print '\n\n'

#that's it
#have fun!