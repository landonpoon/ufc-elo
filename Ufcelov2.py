import csv

datafile = "ufcelodata1.csv"

with open("ufcelodata1.csv", "r") as csvfile:
    MyStockDF=csv.reader(csvfile)
    list_of_rows = [r for r in MyStockDF]

headers = list_of_rows.pop(0)

k = 32

fighters = dict()

for row in list_of_rows:
    #creating fighters
    if row[2] not in fighters:
        fighters[row[2]] = 1000
    if row[3] not in fighters:
        fighters[row[3]] = 1000

    rred = fighters[row[2]]
    rblue = fighters[row[3]]

    if row[5]!="" and row[6]!="":
        #age and color
        bageminusrage = int(row[5])-int(row[6])

        erageoutcome = 0.0141*bageminusrage+0.5

        #equation
        elodiff= rred-rblue
        ered = 0.8*(1/((10**((-elodiff)/400))+1)) + 0.2*erageoutcome
        eblue = 1-ered
    else:
        elodiff= rred-rblue
        ered = (1/((10**((-elodiff)/400))+1))
        eblue = 1-ered

    #adjustments based on win
    if row[4]=="Red":
        rred = rred+k*(1-ered)
        rblue = rblue+k*(0-eblue)
    elif row[4]=="Blue":
        rred = rred+k*(0-ered)
        rblue = rblue+k*(1-eblue)
    elif row[4] =="Draw":
        rred = rred+k*(0.5-ered)
        rblue = rblue+k*(0.5-eblue)

    fighters[row[2]] = rred
    fighters[row[3]] = rblue


def writepart():
    with open("dictionary.csv", "w") as outputfile:
        fieldnames = ["Fighter", "Elo"]
        writer = csv.DictWriter(outputfile, fieldnames=fieldnames)

        writer.writeheader()
        for fighter in fighters:
            writer.writerow({"Fighter": fighter, "Elo": str(fighters[fighter])})

def lookuppart():
    redfighter = input("Enter red fighter name: ")
    redage = int(input("Enter red fighter age: "))
    bluefighter = input("Enter blue fighter name: ")
    blueage = int(input("Enter blue fighter age: "))

    try:
        redelo = fighters[redfighter]
        blueelo = fighters[bluefighter]

        #age
        bageminusrage = blueage-redage

        erageoutcome = 0.0141*bageminusrage+0.6746

        #equation
        elodiff= redelo-blueelo
        ered = 0.8*(1/((10**((-elodiff)/400))+1)) + 0.2*erageoutcome
        eblue = 1-ered

        print(redfighter, ered)
        print(bluefighter, eblue)

    except:
        print("Error. Fighters not found.")

def main():
    writepart()
    lookuppart()

main()
