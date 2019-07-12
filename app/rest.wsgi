import os
activate_this = '/var/www/python/RESTAPIImoveis/bin/activate_this.py'
path = '/var/www/python/RESTAPIImoveis/app/'
if 'programacao' in os.environ['PATH']:
    activate_this = '/home/programacao/Python/API/RESTAPIImoveis/bin/activate_this.py'
    path = '/home/programacao/Python/API/RESTAPIImoveis/app/'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
import sys
sys.path.insert(0,path)
os.system('python --version')
sys.stdout = sys.stderr
from index import app as application
