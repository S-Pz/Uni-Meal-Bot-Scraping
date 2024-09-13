import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from csa_ctan_maker import csa_ctan_maker

cred = credentials.Certificate(r"../Key_firebase.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

data = csa_ctan_maker("../Menus/csa_ctan.pdf")

csa = db.collection("Csa-menu")

for index in data:
    csa.add(data[index])    
