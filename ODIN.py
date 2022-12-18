import re
import requests

print ("""                                                                                                         
              ;                              
       :      ED.                            
      t#,     E#Wi             L.            
     ;##W.    E###G.       t   EW:        ,ft
    :#L:WE    E#fD#W;      Ej  E##;       t#E
   .KG  ,#D   E#t t##L     E#, E###t      t#E
   EE    ;#f  E#t  .E#K,   E#t E#fE#f     t#E
  f#.     t#i E#t    j##f  E#t E#t D#G    t#E
  :#G     GK  E#t    :E#K: E#t E#t  f#E.  t#E
   ;#L   LW.  E#t   t##L   E#t E#t   t#K: t#E
    t#f f#:   E#t .D#W;    E#t E#t    ;#W,t#E
     f#D#;    E#tiW#G.     E#t E#t     :K#D#E
      G#t     E#K##i       E#t E#t      .E##E
       t      E##D.        E#t ..         G#E
              E#t          ,;.             fE
              L:                            ,
              
By: Raphael (Schem4) Fiorin
""")
url = input("★ Scanear URL: ")

# Faz uma solicitação HTTP para obter o código-fonte da página
response = requests.get(url)
html = response.text

# Usa expressões regulares para procurar por links com extensão .js ou .json
js_regex = r'(?:https?://|/)(?:[\w-]+\.)*[\w-]+(?:\.js(?:\?\S+)?)?'
json_regex = r'(?:https?://|/)(?:[\w-]+\.)*[\w-]+(?:\.json(?:\?\S+)?)?'

# Usa expressões regulares para procurar por links com extensão .wp ou .wp-json
wp_regex = r'(?:https?://|/)(?:[\w-]+\.)*[\w-]+(?:/wp(?:\?\S+)?)?'
wp_json_regex = r'(?:https?://|/)(?:[\w-]+\.)*[\w-]+(?:/wp-json(?:\?\S+)?)?'

# Usa expressões regulares para procurar por links com nome amazonaws.com
aws_regex =  r"https?://[^/]*amazonaws\.com[^\s]*"

# Filtro de pesquisa
js_links = re.findall(js_regex, html)
json_links = re.findall(json_regex, html)

wp_links = re.findall(wp_regex, html)
wp_json_links = re.findall(wp_json_regex, html)

aws_links = re.findall(aws_regex, html)

# Remove duplicatas
def get_full_links(base_url, links):
    full_links = set()
    for link in links:
        if link.startswith('/'):
            full_links.add(base_url + link)
        else:
            full_links.add(link)
    return full_links

full_js_links = get_full_links(url, js_links)
full_json_links = get_full_links(url, json_links)
full_wp_links = get_full_links(url, wp_links)
full_aws_links = get_full_links(url, aws_links)

# Imprime os links com extenções JS encontradas
print('\n★ Links JS encontrados:')
for js_link in full_js_links:
    if '.js' in js_link:
        print(js_link)

# Imprime os links com extenções JS e palavra chave API encontradas
print('\n★ Links JS com a palavra API encontrados:')
for js_link in full_js_links:
  if '.js' in js_link:
    response = requests.get(js_link)
    js_code = response.text
    if re.search('404',js_code):
        break
    if re.search('api', js_code):
        print(f'{js_link}')

# Imprime os links com extenções JSON encontradas
print('\n★ Links JSON encontrados:')
for json_link in full_json_links:
  if '.json' in json_link:
    response = requests.get(json_link)
    json_code = response.text
    if re.search('404',json_code):
        break
    if re.search('.json', json_code):
        print(f'{json_link}')

#Imprime os links com extenções JSON e palavra chave API encontradas
print('\n★ Links JSON com a palavra API encontrados:')
for json_link in full_json_links:
  if '.json' in json_link:
    response = requests.get(json_link)
    json_code = response.text
    if re.search('404',json_code):
        break
    if re.search('api', json_code):
        print(f'{json_link}')

# Imprime os links com extenções WP encontradas
print('\n★ Links WP encontrados:')
for wp_link in full_wp_links:
    if 'wp' in wp_link:
        print(wp_link)

# Imprime os links com extenções AWS encontradas
print('\n★ Links AWS encontrados na pagina principal:')
for aws_link in full_aws_links:
  aws_link = aws_link.replace("></script>","").replace('"', "",).replace(",", "").replace("'", "")
  print(aws_link)

#Imprime os links com extenções JS e palavra chave AWS encontradas        
print('\n★ Links JS com a palavra AWS encontrados:')
for js_link in full_js_links:
    if '.js' in js_link:
      response = requests.get(js_link)
      links = re.findall(aws_regex, js_code)
      for link in links:
        print(link+'\n')

#Imprime os links com extenções JSON e palavra chave AWS encontradas        
print('\n★ Links JSON com a palavra AWS encontrados:')
for json_link in full_json_links:
  if '.json' in json_link:
    response = requests.get(json_link)
    links = re.findall(aws_regex, json_code)
    for link in links:
      print(link+'\n')