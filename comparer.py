import json
import re
import math
import csv

with open("gaiup-results.json", "r") as gfile:
    gaiup = json.loads(gfile.read())

with open("lca-results.json", "r") as lcafile:
    lcas = json.loads(lcafile.read())
amount_of_lca = 0
amount_of_fails = 0

with open('fail-results.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    for lca in lcas:
        for data in gaiup:
            gaiupID = data["link"][0].split("uuid=")[1]
            if lca["Ekstern id"] == gaiupID:
                amount_of_lca = amount_of_lca + 1
                gaiup_mass = data["declaredUnit"]["mass"]
                lca_space_index = lca["Massefaktor"].index(' ')
                head, sep, tail = lca["Massefaktor"].partition(' ')

                head = head.replace(",", ".")
                gaiup_mass = gaiup_mass.replace(",", ".")
                if(head != gaiup_mass):
                    if math.isclose(float(head), float(gaiup_mass), abs_tol = 0.1):
                        continue
                    amount_of_fails = amount_of_fails +1
                    print("fail!")
                    writer.writerow([float(head),float(gaiup_mass)])



print("fails: ", amount_of_fails)
print("len: ", amount_of_lca)

p = amount_of_fails/amount_of_lca
p1 = p *100
print(p1, "%","failed")




