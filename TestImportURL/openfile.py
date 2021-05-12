import requests

url = "http://195.133.144.86:4200//Half-coupling1.f3d"
wayfile = 'C:/Users/Xylia/Desktop/test/HC.f3d'

model = requests.get(url)

if model:
    print('Response OK')
else:
    print('Response Failed')

open(wayfile,'wb').write(model.content)
