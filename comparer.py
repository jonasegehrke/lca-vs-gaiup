import json
import re
import math
import csv
from progress.bar import Bar


def lca_in_gaiup ():
    with open("gaiup-results.json", "r") as gfile:
        gaiup = json.loads(gfile.read())

    with open("lca-results.json", "r") as lcafile:
        lcas = json.loads(lcafile.read())
    #write 2 new json files with the respective source in each. This ensures that they both are the same length and the same materials
    GaiupResult = []
    LCAResult = []
    for lca in lcas:
        for data in gaiup:
            gaiupID = data["link"][0].split("uuid=")[1]
            if lca["Ekstern id"] == gaiupID:
                GaiupResult.append(data)
                LCAResult.append(lca)

    GaiupFinal = json.dumps(GaiupResult, indent=2)
    LCAFinal = json.dumps(LCAResult, indent=2)
    with open('gaiup.json', 'w') as outfile:
        outfile.write(GaiupFinal)
    with open('lca.json', 'w') as outfile:
        outfile.write(LCAFinal)
#lca_in_gaiup()

def getFails(lcas, gaiup):

    total_amount_tested = len(lcas)
    amount_of_fails = 0

    with open('fail-results.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "LCA Material ID",
            "LCA Material Name",
            "Stage",
            "Oekobaudat Link",
            "LCA massValue",
            "Oekobaudat massValue",
            "massValue Difference",
            "massValue Difference Percentage",
            "LCA GWP",
            "Oekobaudat GWP",
            "GWP Difference",
            "GWP Difference Percentage",
            "LCA ODP",
            "Oekobaudat ODP",
            "ODP Difference",
            "ODP Difference Percentage",
            "LCA POCP",
            "Oekobaudat POCP",
            "POCP Difference",
            "POCP Difference Percentage",
            "LCA AP",
            "Oekobaudat AP",
            "AP Difference",
            "AP Difference Percentage",
            "LCA EP",
            "Oekobaudat EP",
            "EP Difference",
            "EP Difference Percentage",
            "LCA ADPE",
            "Oekobaudat ADPE",
            "ADPE Difference",
            "ADPE Difference Percentage",
            "LCA ADPF",
            "Oekobaudat ADPF",
            "ADPF Difference",
            "ADPF Difference Percentage",
            "LCA PERT",
            "Oekobaudat PERT",
            "PERT Difference",
            "PERT Difference Percentage",
            "LCA PENRT",
            "Oekobaudat PENRT",
            "PENRT Difference",
            "PENRT Difference Percentage",
            "LCA RSF",
            "Oekobaudat RSF",
            "RSF Difference",
            "RSF Difference Percentage",
            "LCA NRSF",
            "Oekobaudat NRSF",
            "NRSF Difference",
            "NRSF Difference Percentage",
            ])
        
        
        
        with Bar('Processing massValue Fails', max=total_amount_tested) as bar:
            for lca in lcas:
                gaiupData = next(gaiupMaterial for gaiupMaterial in gaiup if gaiupMaterial["link"][0].split("uuid=")[1] == lca["Ekstern id"])
                logged_fail = {}

                logged_fail["LCA Material ID"] = "X"
                logged_fail["Stage"] = "X"
                logged_fail["LCA Material Name"] = "X"
                logged_fail["Oekobaudat Link"] = "X"
                logged_fail["LCA massValue"] = "X"
                logged_fail["Oekobaudat massValue"] = "X"
                logged_fail["massValue Difference"] = "X"
                logged_fail["massValue Difference Percentage"] = "X"
                logged_fail["LCA GWP"] = "X"
                logged_fail["Oekobaudat GWP"] = "X"
                logged_fail["GWP Difference"] = "X"
                logged_fail["GWP Difference Percentage"] = "X"
                logged_fail["LCA ODP"] = "X"
                logged_fail["Oekobaudat ODP"] = "X"
                logged_fail["ODP Difference"] = "X"
                logged_fail["ODP Difference Percentage"] = "X"
                logged_fail["LCA POCP"] = "X"
                logged_fail["Oekobaudat POCP"] = "X"
                logged_fail["POCP Difference"] = "X"
                logged_fail["POCP Difference Percentage"] = "X"
                logged_fail["LCA AP"] = "X"
                logged_fail["Oekobaudat AP"] = "X"
                logged_fail["AP Difference"] = "X"
                logged_fail["AP Difference Percentage"] = "X"
                logged_fail["LCA EP"] = "X"
                logged_fail["Oekobaudat EP"] = "X"
                logged_fail["EP Difference"] = "X"
                logged_fail["EP Difference Percentage"] = "X"
                logged_fail["LCA ADPE"] = "X"
                logged_fail["Oekobaudat ADPE"] = "X"
                logged_fail["ADPE Difference"] = "X"
                logged_fail["ADPE Difference Percentage"] = "X"
                logged_fail["LCA ADPF"] = "X"
                logged_fail["Oekobaudat ADPF"] = "X"
                logged_fail["ADPF Difference"] = "X"
                logged_fail["ADPF Difference Percentage"] = "X"
                logged_fail["LCA PERT"] = "X"
                logged_fail["Oekobaudat PERT"] = "X"
                logged_fail["PERT Difference"] = "X"
                logged_fail["PERT Difference Percentage"] = "X"
                logged_fail["LCA PENRT"] = "X"
                logged_fail["Oekobaudat PENRT"] = "X"
                logged_fail["PENRT Difference"] = "X"
                logged_fail["PENRT Difference Percentage"] = "X"
                logged_fail["LCA RSF"] = "X"
                logged_fail["Oekobaudat RSF"] = "X"
                logged_fail["RSF Difference"] = "X"
                logged_fail["RSF Difference Percentage"] = "X"
                logged_fail["LCA NRSF"] = "X"
                logged_fail["Oekobaudat NRSF"] = "X"
                logged_fail["NRSF Difference"] = "X"
                logged_fail["NRSF Difference Percentage"] = "X"
                logged_fail["hasError"] = False

                gaiup_mass = gaiupData["declaredUnit"]["mass"]
                head, sep, tail = lca["Massefaktor"].partition(' ')

                head = head.replace(",", ".")
                gaiup_mass = gaiup_mass.replace(",", ".")
                if(head != gaiup_mass):
                    if not math.isclose(float(head), float(gaiup_mass), abs_tol = 0.1):
                        amount_of_fails = amount_of_fails + 1
                        logged_fail["hasError"] = True
                        difference = float(gaiup_mass) - float(head)
                        difference_percentage = (difference / float(head)) * 100
                        logged_fail["LCA Material ID"] = lca["Ekstern id"]
                        logged_fail["Stage"] = lca["Fase"]
                        logged_fail["LCA Material Name"] = lca["Title"]
                        logged_fail["Oekobaudat Link"] = gaiupData["link"][0]
                        logged_fail["LCA massValue"] = float(head)
                        logged_fail["Oekobaudat massValue"] = float(gaiup_mass)
                        logged_fail["massValue Difference"] = difference
                        logged_fail["massValue Difference Percentage"] = str(difference_percentage) + "%"
                
                gaiup_declared = gaiupData["declaredUnit"]["declaredValue"]
                lca_declared = re.sub(" (?=-(?= (?=[0-9])))", "", lca["Indikatorfaktor"])
                lca_declared = re.sub("(?<=-) (?=[0-9])", "", lca_declared)
                head, sep, tail = lca_declared.partition(' ')

                head = head.replace(",", ".")
                gaiup_declared = gaiup_declared.replace(",", ".")
        
                if not math.isclose(float(head), float(gaiup_declared), abs_tol = 0.01):
                    print()
                    print(float(head))
                    print(float(gaiup_declared))

                for gaiupStage in gaiupData["stages"]:
                    if lca["Fase"] == 'A1 - A3' and gaiupStage["stageType"] == 0:
                        logged_fail = checkStage(lca, gaiupStage, logged_fail)
                    elif lca["Fase"] == 'C3' and gaiupStage["stageType"] == 15:
                        logged_fail = checkStage(lca, gaiupStage, logged_fail)
                    elif lca["Fase"] == 'C4' and gaiupStage["stageType"] == 16:
                        logged_fail = checkStage(lca, gaiupStage, logged_fail)
                    elif lca["Fase"] == 'D' and gaiupStage["stageType"] == 17:
                        logged_fail = checkStage(lca, gaiupStage, logged_fail)
                    
                
                
                if logged_fail["hasError"]:
                    writer.writerow([
                        logged_fail["LCA Material ID"],
                        logged_fail["LCA Material Name"],
                        logged_fail["Stage"],
                        logged_fail["Oekobaudat Link"],
                        logged_fail["LCA massValue"],
                        logged_fail["Oekobaudat massValue"],
                        logged_fail["massValue Difference"],
                        logged_fail["massValue Difference Percentage"],
                        logged_fail["LCA GWP"],
                        logged_fail["Oekobaudat GWP"],
                        logged_fail["GWP Difference"],
                        logged_fail["GWP Difference Percentage"],
                        logged_fail["LCA ODP"],
                        logged_fail["Oekobaudat ODP"],
                        logged_fail["ODP Difference"],
                        logged_fail["ODP Difference Percentage"],
                        logged_fail["LCA POCP"],
                        logged_fail["Oekobaudat POCP"],
                        logged_fail["POCP Difference"],
                        logged_fail["POCP Difference Percentage"],
                        logged_fail["LCA AP"],
                        logged_fail["Oekobaudat AP"],
                        logged_fail["AP Difference"],
                        logged_fail["AP Difference Percentage"],
                        logged_fail["LCA EP"],
                        logged_fail["Oekobaudat EP"],
                        logged_fail["EP Difference"],
                        logged_fail["EP Difference Percentage"],
                        logged_fail["LCA ADPE"],
                        logged_fail["Oekobaudat ADPE"],
                        logged_fail["ADPE Difference"],
                        logged_fail["ADPE Difference Percentage"],
                        logged_fail["LCA ADPF"],
                        logged_fail["Oekobaudat ADPF"],
                        logged_fail["ADPF Difference"],
                        logged_fail["ADPF Difference Percentage"],
                        logged_fail["LCA PERT"],
                        logged_fail["Oekobaudat PERT"],
                        logged_fail["PERT Difference"],
                        logged_fail["PERT Difference Percentage"],
                        logged_fail["LCA PENRT"],
                        logged_fail["Oekobaudat PENRT"],
                        logged_fail["PENRT Difference"],
                        logged_fail["PENRT Difference Percentage"],
                        logged_fail["LCA RSF"],
                        logged_fail["Oekobaudat RSF"],
                        logged_fail["RSF Difference"],
                        logged_fail["RSF Difference Percentage"],
                        logged_fail["LCA NRSF"],
                        logged_fail["Oekobaudat NRSF"],
                        logged_fail["NRSF Difference"],
                        logged_fail["NRSF Difference Percentage"],
                        ])
                #bar.next()
        print(amount_of_fails)




def checkStage(lca, gaiupStage, logged_fail):
    #GWP
    gaiupValue = gaiupStage["measures"]["GWP"]
    lcaValue = re.sub(" (?=-(?= (?=[0-9])))", "", lca["Indikatorer"]["GWP"])
    lcaValue = re.sub("(?<=-) (?=[0-9])", "", lcaValue)
    head, sep, tail = lcaValue.partition(' ')

    head = head.replace(",", ".")
    gaiupValue = gaiupValue.replace(",", ".")
    if not math.isclose(float(head), float(gaiupValue), abs_tol=0.1):
        difference = float(gaiupValue) - float(head)
        difference_percentage = (difference / float(head)) * 100
        logged_fail["hasError"] = True
        logged_fail["LCA GWP"] = float(head) 
        logged_fail["Oekobaudat GWP"] = float(gaiupValue)
        logged_fail["GWP Difference"] = difference
        logged_fail["GWP Difference Percentage"] = str(difference_percentage) + "%"

    #ODP    
    gaiupValue = gaiupStage["measures"]["ODP"]
    lcaValue = re.sub(" (?=-(?= (?=[0-9])))", "", lca["Indikatorer"]["ODP"])
    lcaValue = re.sub("(?<=-) (?=[0-9])", "", lcaValue)
    head, sep, tail = lcaValue.partition(' ')

    head = head.replace(",", ".")
    gaiupValue = gaiupValue.replace(",", ".")
    if not math.isclose(float(head), float(gaiupValue), abs_tol=0.1):
        difference = float(gaiupValue) - float(head)
        difference_percentage = (difference / float(head)) * 100
        logged_fail["hasError"] = True
        logged_fail["LCA ODP"] = float(head) 
        logged_fail["Oekobaudat ODP"] = float(gaiupValue)
        logged_fail["ODP Difference"] = difference
        logged_fail["ODP Difference Percentage"] = str(difference_percentage) + "%"

    #POCP
    gaiupValue = gaiupStage["measures"]["POCP"]
    lcaValue = re.sub(" (?=-(?= (?=[0-9])))", "", lca["Indikatorer"]["POCP"])
    lcaValue = re.sub("(?<=-) (?=[0-9])", "", lcaValue)
    head, sep, tail = lcaValue.partition(' ')

    head = head.replace(",", ".")
    gaiupValue = gaiupValue.replace(",", ".")
    if not math.isclose(float(head), float(gaiupValue), abs_tol=0.1):
        difference = float(gaiupValue) - float(head)
        difference_percentage = (difference / float(head)) * 100
        logged_fail["hasError"] = True
        logged_fail["LCA POCP"] = float(head) 
        logged_fail["Oekobaudat POCP"] = float(gaiupValue)
        logged_fail["POCP Difference"] = difference
        logged_fail["POCP Difference Percentage"] = str(difference_percentage) + "%"

    #AP
    gaiupValue = gaiupStage["measures"]["AP"]
    lcaValue = re.sub(" (?=-(?= (?=[0-9])))", "", lca["Indikatorer"]["AP"])
    lcaValue = re.sub("(?<=-) (?=[0-9])", "", lcaValue)
    head, sep, tail = lcaValue.partition(' ')

    head = head.replace(",", ".")
    gaiupValue = gaiupValue.replace(",", ".")
    if not math.isclose(float(head), float(gaiupValue), abs_tol=0.1):
        difference = float(gaiupValue) - float(head)
        difference_percentage = (difference / float(head)) * 100
        logged_fail["hasError"] = True
        logged_fail["LCA AP"] = float(head) 
        logged_fail["Oekobaudat AP"] = float(gaiupValue)
        logged_fail["AP Difference"] = difference
        logged_fail["AP Difference Percentage"] = str(difference_percentage) + "%"

    #EP
    gaiupValue = gaiupStage["measures"]["EP"]
    lcaValue = re.sub(" (?=-(?= (?=[0-9])))", "", lca["Indikatorer"]["EP"])
    lcaValue = re.sub("(?<=-) (?=[0-9])", "", lcaValue)
    head, sep, tail = lcaValue.partition(' ')

    head = head.replace(",", ".")
    gaiupValue = gaiupValue.replace(",", ".")
    if not math.isclose(float(head), float(gaiupValue), abs_tol=0.1):
        difference = float(gaiupValue) - float(head)
        difference_percentage = (difference / float(head)) * 100
        logged_fail["hasError"] = True
        logged_fail["LCA EP"] = float(head) 
        logged_fail["Oekobaudat EP"] = float(gaiupValue)
        logged_fail["EP Difference"] = difference
        logged_fail["EP Difference Percentage"] = str(difference_percentage) + "%"
    
    #ADPE
    gaiupValue = gaiupStage["measures"]["ADPE"]
    lcaValue = re.sub(" (?=-(?= (?=[0-9])))", "", lca["Indikatorer"]["ADPE"])
    lcaValue = re.sub("(?<=-) (?=[0-9])", "", lcaValue)
    head, sep, tail = lcaValue.partition(' ')

    head = head.replace(",", ".")
    gaiupValue = gaiupValue.replace(",", ".")
    if not math.isclose(float(head), float(gaiupValue), abs_tol=0.1):
        difference = float(gaiupValue) - float(head)
        difference_percentage = (difference / float(head)) * 100
        logged_fail["hasError"] = True
        logged_fail["LCA ADPE"] = float(head) 
        logged_fail["Oekobaudat ADPE"] = float(gaiupValue)
        logged_fail["ADPE Difference"] = difference
        logged_fail["ADPE Difference Percentage"] = str(difference_percentage) + "%"
    
    #ADPF
    gaiupValue = gaiupStage["measures"]["ADPF"]
    lcaValue = re.sub(" (?=-(?= (?=[0-9])))", "", lca["Indikatorer"]["ADPF"])
    lcaValue = re.sub("(?<=-) (?=[0-9])", "", lcaValue)
    head, sep, tail = lcaValue.partition(' ')

    head = head.replace(",", ".")
    gaiupValue = gaiupValue.replace(",", ".")
    if not math.isclose(float(head), float(gaiupValue), abs_tol=0.1):
        difference = float(gaiupValue) - float(head)
        difference_percentage = (difference / float(head)) * 100
        logged_fail["hasError"] = True
        logged_fail["LCA ADPF"] = float(head) 
        logged_fail["Oekobaudat ADPF"] = float(gaiupValue)
        logged_fail["ADPF Difference"] = difference
        logged_fail["ADPF Difference Percentage"] = str(difference_percentage) + "%"
    
    #PERT
    gaiupValue = gaiupStage["measures"]["PERT"]
    lcaValue = re.sub(" (?=-(?= (?=[0-9])))", "", lca["Indikatorer"]["PERT"])
    lcaValue = re.sub("(?<=-) (?=[0-9])", "", lcaValue)
    head, sep, tail = lcaValue.partition(' ')

    head = head.replace(",", ".")
    gaiupValue = gaiupValue.replace(",", ".")
    if not math.isclose(float(head), float(gaiupValue), abs_tol=0.1):
        difference = float(gaiupValue) - float(head)
        difference_percentage = (difference / float(head)) * 100
        logged_fail["hasError"] = True
        logged_fail["LCA PERT"] = float(head) 
        logged_fail["Oekobaudat PERT"] = float(gaiupValue)
        logged_fail["PERT Difference"] = difference
        logged_fail["PERT Difference Percentage"] = str(difference_percentage) + "%"

    #PENRT
    gaiupValue = gaiupStage["measures"]["PENRT"]
    lcaValue = re.sub(" (?=-(?= (?=[0-9])))", "", lca["Indikatorer"]["PENRT"])
    lcaValue = re.sub("(?<=-) (?=[0-9])", "", lcaValue)
    head, sep, tail = lcaValue.partition(' ')

    head = head.replace(",", ".")
    gaiupValue = gaiupValue.replace(",", ".")
    if not math.isclose(float(head), float(gaiupValue), abs_tol=0.1):
        difference = float(gaiupValue) - float(head)
        difference_percentage = (difference / float(head)) * 100
        logged_fail["hasError"] = True
        logged_fail["LCA PENRT"] = float(head) 
        logged_fail["Oekobaudat PENRT"] = float(gaiupValue)
        logged_fail["PENRT Difference"] = difference
        logged_fail["PENRT Difference Percentage"] = str(difference_percentage) + "%"

    #RSF
    gaiupValue = gaiupStage["measures"]["RSF"]
    lcaValue = re.sub(" (?=-(?= (?=[0-9])))", "", lca["Indikatorer"]["RSF"])
    lcaValue = re.sub("(?<=-) (?=[0-9])", "", lcaValue)
    head, sep, tail = lcaValue.partition(' ')

    head = head.replace(",", ".")
    gaiupValue = gaiupValue.replace(",", ".")
    if not math.isclose(float(head), float(gaiupValue), abs_tol=0.1):
        difference = float(gaiupValue) - float(head)
        difference_percentage = (difference / float(head)) * 100
        logged_fail["hasError"] = True
        logged_fail["LCA RSF"] = float(head) 
        logged_fail["Oekobaudat RSF"] = float(gaiupValue)
        logged_fail["RSF Difference"] = difference
        logged_fail["RSF Difference Percentage"] = str(difference_percentage) + "%"

    #NRSF
    gaiupValue = gaiupStage["measures"]["NRSF"]
    lcaValue = re.sub(" (?=-(?= (?=[0-9])))", "", lca["Indikatorer"]["NRSF"])
    lcaValue = re.sub("(?<=-) (?=[0-9])", "", lcaValue)
    head, sep, tail = lcaValue.partition(' ')

    head = head.replace(",", ".")
    gaiupValue = gaiupValue.replace(",", ".")
    if not math.isclose(float(head), float(gaiupValue), abs_tol=0.1):
        difference = float(gaiupValue) - float(head)
        difference_percentage = (difference / float(head)) * 100
        logged_fail["hasError"] = True
        logged_fail["LCA NRSF"] = float(head) 
        logged_fail["Oekobaudat NRSF"] = float(gaiupValue)
        logged_fail["NRSF Difference"] = difference
        logged_fail["NRSF Difference Percentage"] = str(difference_percentage) + "%"
    return logged_fail
def runMatchTest():
    with open("gaiup.json", "r") as gfile:
        gaiup = json.loads(gfile.read())

    with open("lca.json", "r") as lcafile:
        lcas = json.loads(lcafile.read())

    getFails(lcas, gaiup)

runMatchTest()
""" 
print("fails: ", amount_of_fails)
print("len: ", amount_of_lca)

p = amount_of_fails/amount_of_lca
p1 = p *100
print(p1, "%","failed") """




