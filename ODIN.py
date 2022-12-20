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
def scan():
    # Make an HTTP request to get the page's source code
    response = requests.get(url)
    html = response.text

    # Use regular expressions to search for links with a .js or .json extension
    js_regex = r'(?:https?://|/)(?:[\w-]+\.)*[\w-]+(?:\.js(?:\?\S+)?)?'
    json_regex = r'(?:https?://|/)(?:[\w-]+\.)*[\w-]+(?:\.json(?:\?\S+)?)?'

    # Use regular expressions to search for links with a .wp or .wp-json extension
    wp_regex = r'(?:https?://|/)(?:[\w-]+\.)*[\w-]+(?:/wp(?:\?\S+)?)?'
    wp_json_regex = r'(?:https?://|/)(?:[\w-]+\.)*[\w-]+(?:/wp-json(?:\?\S+)?)?'

    # Use regular expressions to search for links named amazonaws.com
    aws_regex =  r"https?://[^/]*amazonaws\.com[^\s]*"

    # Search filter
    js_links = re.findall(js_regex, html)
    json_links = re.findall(json_regex, html)

    wp_links = re.findall(wp_regex, html)
    wp_json_links = re.findall(wp_json_regex, html)

    aws_links = re.findall(aws_regex, html)

    # remove duplicates
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

    # Print the links with JS extension found
    print('\n★ JS links found:')
    for js_link in full_js_links:
        if '.js' in js_link:
            print(js_link)

    # Print the links with found JS extensions and API keywords
    print('\n★ JS links with API word found:')
    for js_link in full_js_links:
      if '.js' in js_link:
        response = requests.get(js_link)
        js_code = response.text
        if re.search('404',js_code):
            break
        if re.search('api', js_code):
            print(f'{js_link}')

    # Print the links with found JSON extensions
    print('\n★ Found JSON links:')
    for json_link in full_json_links:
      if '.json' in json_link:
        response = requests.get(json_link)
        json_code = response.text
        if re.search('404',json_code):
            break
        if re.search('.json', json_code):
            print(f'{json_link}')

    #Print the links with found JSON extensions and API keywords
    print('\n★ Found JSON links with the word API:')
    for json_link in full_json_links:
      if '.json' in json_link:
        response = requests.get(json_link)
        json_code = response.text
        if re.search('404',json_code):
            break
        if re.search('api', json_code):
            print(f'{json_link}')

    # Print the links with found WP extensions
    print('\n★ Found WP Links:')
    for wp_link in full_wp_links:
        if 'wp' in wp_link:
            print(wp_link)

    # Print the links with found AWS extensions
    print('\n★ AWS links found on main page:')
    for aws_link in full_aws_links:
      aws_link = aws_link.replace("></script>","").replace('"', "",).replace(",", "").replace("'", "")
      print(aws_link)

    #Print the links with found JS extensions and AWS keyword
    print('\n★ JS links with the word AWS found:')
    for js_link in full_js_links:
        if '.js' in js_link:
          response = requests.get(js_link)
          links = re.findall(aws_regex, js_code)
          for link in links:
            print(link+'\n')

    #Print the links with found JSON extensions and AWS keyword
    print('\n★ Found JSON links with the word AWS::')
    for json_link in full_json_links:
      if '.json' in json_link:
        response = requests.get(json_link)
        links = re.findall(aws_regex, json_code)
        for link in links:
          print(link+'\n')
          print ("=-=-=-=-=-=-=-=-=-=-=-=-=")

# Menu
print("""Choose a scan option:
★ 1 - Scan unique URL (Usage: https://example.com.br)
★ 2 - Scan multiple URLs contained in a domains.txt file (Usage: https://example.com.br)
\n""")

# Get the scan option chosen by the user
option = int(input("★ Enter the desired option: "))

# Check which option was chosen and scan the URL or URLs contained in the .txt file
if option == 1:
    url = input("Enter the URL to be scanned: ")
    print("\n =-=-=-=-=-=-=-=-=-=-=-=-=")
    print(f"★ Scanning URL: {url}\n")
    scan()

elif option == 2:
    # Open the .txt file and read the contents line by line
    with open('domains.txt', 'r') as f:
        lines = f.readlines()
    # Loop through each line of the file
    for line in lines:
        # Remove the newline character from the current line
        url = line.strip()
        print ("\n =-=-=-=-=-=-=-=-=-=-=-=-=")
        print (f"★ Scanning URL: {url}")
        scan()
