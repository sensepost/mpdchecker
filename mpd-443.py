import httplib
import urlparse
import re
import sys

levellimit=4
urllist = {}
topurl = ""

def scan(url,level):
  global levellimit
  global urllist
  global topurl
  
  if topurl=="":
     topurl=url
     
  u = urlparse.urlparse(url)
    
  if not level<levellimit:
     return  
  if urllist.has_key(url)==True:
     return   
  
  print level,u.hostname,u.path,url,   
  try:
    conn = httplib.HTTPSConnection(""+u.hostname)
    conn.request("OPTIONS", u.path,headers={'User-Agent': 'lol','Accept': '*/*'})
    r1 = conn.getresponse()
    header=r1.getheader("Allow")
    conn = httplib.HTTPSConnection(u.hostname)
    conn.request("GET", u.path,headers={'User-Agent': 'lol','Accept': '*/*'})
    r1 = conn.getresponse()
    body= r1.read()
    urllist[url]=header  
    print '   O'
    uu={}
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', body)
    for s in urls:
        if s.find(topurl)>-1 or s.find("https://")==-1:
           uu[s]="luvly"
           
    for key,value in uu.items():
        if key[0]!="/" and key.find("https://")==-1:
           key="/"+key        
        if key.find("https://")==-1:
           scan("https://"+u.hostname+key,level+1)
        else:
           scan(key,level+1)

  except:
    print '   X'
    pass    
        
levellimit=int(sys.argv[2])        
scan(sys.argv[1],1)

print "results"        
for key, value in urllist.items():
  print key,'\t\t',value