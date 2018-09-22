###########
# Base Page
##########

basefmt = '''
<html>
    <head>
        <title>%s</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        %s
    </head>
    <body>%s%s</body>
</html>
'''

cssfmt = "<link rel='stylesheet' type='text/css' href='/css/%s.css'>"
jsfmt = '''<script type="text/javascript" src="/js/%s.js"></script>'''

def base(title, insides, css=[], js=[]):
    return basefmt % (title, 
                      "".join(cssfmt % c for c in css), 
                      insides,
                      "".join(jsfmt % j for j in js))
