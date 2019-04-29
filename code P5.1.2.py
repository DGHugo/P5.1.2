from flask import Flask
from flask_ask import Ask, statement, question
import datetime

app = Flask(_name_)
ask = Ask(app, '/')

agenda = []
for x in range(12):  # création de l'agenda avec 12 mois, 31 jours par mois et 24h par jour
    agenda.append([])
    for y in range(31):
        agenda[x].append([])
        for z in range(24):
            agenda[x][y].append("")

for e in range(3):
    agenda[1].pop(e)

agenda[3].pop(1)  # ajustement des tailles de certains mois
agenda[5].pop(1)
agenda[8].pop(1)
agenda[10].pop(1)

liste_mois = {"janvier": 1, "fevrier": 2, "février": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6, "juillet": 7,
              "aout": 8, "septembre": 9, "octobre": 10, "novembre": 11, "decembre": 12}


def plus_frequent(l):  # fonction qui nous permettra de sortir l'activité la plus présente dans l'agenda

    d = {}
    seen = []
    for x in range(len(l)):
        count = 0
        if l[x] in seen:
            pass
        else:
            for y in range(len(l)):
                if l[y] == l[x]:
                    count += 1
            seen.append(l[y])
            d[x] = count

    maxi = -float('inf')
    maxi_key = ""
    for key in d.keys():

        if d[key] > maxi:
            maxi = d[key]
            maxi_key = key
    return l[maxi_key]


def n_plus_frequents(l, n):  # fonction qui nous permettra de sortir les n activités favorites
    new_l = []
    l2 = l.copy()
    for x in range(n):
        temp = plus_frequent(l2)
        new_l.append(temp)
        while temp in l2:
            l2.remove(temp)
    return new_l


def find_month(n):
    for k in liste_mois.keys():
        if liste_mois[k] == n:
            return k


now = datetime.datetime.now()

day = now.day
month = find_month(now.month)


@ask.launch
def start():  # question d'alexa lorsqu'on appelle le skill "agenda"
    return question('Que puis je faire pour vous?')


@ask.intent('ajouter')  # fonction pour ajouter n'importe quelle activité à l'agenda au jour demandé
def ajouter(activity, jour, mois, heure):
    a = str(activity)
    j = int(jour)
    h = int(heure)
    m = int(liste_mois[mois])

    if str(activity) == "rien":
        agenda[m][j][h] = ""
        return statement("je note")
    else:
        agenda[m][j][h] = a
        return statement("je note ça")


@ask.intent('rappel_jour')  # rappelle a l'utilisateur toutes ses activités du jour
def rappel_jour(jour, mois):
    j = int(jour)
    m = int(liste_mois[mois])
    s = ""
    for x in range(len(agenda[m][j])):
        if agenda[m][j][x] is not "":
            if x == len(agenda[m][j]) - 1:
                s += str(x) + " heure : " + str(agenda[m][j][x]) + " ."
            else:
                s += str(x) + " heure : " + str(agenda[m][j][x]) + ", "
    return statement(s)


@ask.intent('rappel_heure')  # l'utilisateur demande a alexa ce qu'il a a une heure précise et alexa lui répond
def rappel_heure(jour, mois, heure):
    j = int(jour)
    h = int(heure)
    m = int(liste_mois[mois])
    if agenda[m][j][h] == "":
        return statement("vous n'avez rien de prévu le {} {} à {} heure".format(j, m, h))
    return statement("vous avez {}".format(str(agenda[m][j][h])))


@ask.intent('question_date')  # l'utilisateur demande a alexa quelle jour est-il
def date():
    return statement("nous sommes le {} {}".format(day, month))


@ask.intent('proposition')
def proposition(nombre):  # l'utilisateur demande des propositions d'activités
    number = int(nombre)
    activities = []

    empty = True
    for x in range(12):
        for y in range(len(agenda[x])):
            for z in range(24):
                if agenda != None:
                    activities.append(agenda[x][y][z])
                    empty = False

    activities = n_plus_frequents(activities, number+1)
    activities.pop(0)
    s = " "
    for x in range(len(activities)):
        if x == len(activities) - 1:
            s += activities[x] + " ."
        else:
            s += activities[x] + " ,"

    return statement("d'habitude vos {} activités favorites sont : {}".format(number,s))


if _name_ == '_main_':
    app.run()