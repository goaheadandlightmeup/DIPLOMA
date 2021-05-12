import request
    
    url = "http://195.133.144.86:4200//Half-coupling1.f3d"
    wayfile = 'C:/Desktop/test'
    r = requests.get(url)

    if r:
         print('Response OK')
    else:
        print('Response Failed')

    open(wayfile,'wb').write(r.content)
