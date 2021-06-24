import os
from pymongo import MongoClient

user = os.environ.get('USER')
password = os.environ.get('PASS')
database = os.environ.get('DATA')
main = os.environ.get('MAIN')
streamers = os.environ.get('STREAM')
emoji = os.environ.get('EMOJI')
shop = os.environ.get('SHOP')

cluster = MongoClient(f'mongodb+srv://{user}:{password}@cluster0.tta6a.mongodb.net/{database}?retryWrites=true&w=majority')
db = cluster[f'{database}']
coll = db[f'{main}']
colls = db[f'{emoji}']
collst = db[f'{streamers}']
collsp = db[f'{shop}']

