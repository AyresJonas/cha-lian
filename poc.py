from tinydb import TinyDB, Query
import os
# import requests
# import json


db = TinyDB("presentes.json")
db.truncate()

index = 1
for root, _, files in os.walk(".\\static\\imgs"):
    for filename in [os.path.join(root, name) for name in files]:
        item = (
            filename.replace(".\\static\\imgs\\", "")
            .replace(".jpg", "")
            .replace(".jpeg", "")
        )
        db.insert(
            {
                "_id": index,
                "item": item,
                "foto": filename.replace(".\\static", "")
                .replace("/\\", "")
                .replace("\\", "/"),
                "reservado": False,
            }
        )

        index += 1


# print(db.get(doc_id=64))
# print(db.get(Query()._id == 3))

# print(requests.post("http://localhost:5000/reservar/1").__dict__)

# az webapp up --runtime PYTHON:3.12 --sku F1 --logs --location brazilsouth --name chacasanova
