#!/usr/bin/python3
# display CGI environment variables etc.

# import os, sys, cgi,  urlparse
import os, sys, cgi
import phileas
print ("Content-type: text/html")
print ()
print ("""<!DOCTYPE html PUBLIC
   "-//W3C//DTD XHTML 1.0 Transitional//EN"
   "DTD/xhtml1-transitional.dtd">""")

print ("""
<html xmlns = "http://www.w3.org/1999/xhtml" xml:lang="en"
   lang="en">
   <head><title>Environment Variables</title></head>
      <body><table style = "border: 0">""")

print (phileas.__file__)
print ("pwd=", os.getcwd())
print ("sys.argv=", sys.argv)
print ("sys.path=", sys.path)
print ('----------------------')
print ('----------------------')
print (dir(phileas))
print ('----------------------')

for rowIndex, item in enumerate(os.environ.keys()):
    backgroundColor = ("white", "lightgrey")[rowIndex % 2]
    print ("""<tr style = "background-color: %s">
    <td>%s</td><td>%s</td></tr>""" \
          % ( backgroundColor, item,
              cgi.escape( os.environ[ item ] ) ))
print ("""</table></body></html>""")
print (cgi.parse_qs(os.environ.get("QUERY_STRING",  '&'.join(sys.argv[1:]))))
##print urlparse.parse_qs(os.environ.get("QUERY_STRING",  '&'.join(sys.argv[1:])))
