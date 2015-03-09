#!/usr/bin/env python
# -*- coding: utf-8 -*-

# cf. http://koaning.github.io/html/scapingdynamicwebsites.html
# et: https://selenium-python.readthedocs.org/index.html
#
# Compatibilité : version Python 3.4, Windows
#
# installer selenium : dans cmd.exe : C:\Python34\Scripts\pip.exe install selenium
#
# Auteur : R. Louvet, doctorant - Université d'Avignon (UMR ESPACE)
#
# Ce programme permet de récupérer les données individuelles
# sur les budgets des collectivités locales disponibles sur le
# site "http://www.collectivites-locales.gouv.fr/"

# bibliotheque python
from selenium import webdriver
import re
import time
import os

#### #### #### #### #### #### ###
#           endettement         #
#### #### #### #### #### #### ###
print("Endettement...")

# mesure performance
time1 = time.time()

### Variables
# url
url = "http://alize2.finances.gouv.fr/communes/eneuro/tableau.php"

# dossiers
home = os.path.expanduser("~")
racine = home+"/Desktop/base_finances_collectivites"
data = racine+"/data"

# fichiers
code_input = racine+"/codes_collectivites/communes/codes_communes.csv"
output1 = data+"/endettement"
code_input = code_input.replace("\\","/")
output1 = output1.replace("\\",'/')

# a partir des codes geofla, codes communes et codes departements
try:
    fichier = open(code_input,"r")
except:
    code_input = code_input.replace("Desktop","Bureau")
    output1 = output1.replace("Desktop","Bureau")
    racine = racine.replace("Desktop","Bureau")
    fichier = open(code_input,"r")
    
lire = fichier.read()
codes = lire.split("\n")

# liste dates d'exercice  
exercices = ["2013","2012","2011","2010","2009","2008","2007","2006","2005","2004","2003","2002","2001","2000"]

# requete javascript
# PARAM = 5 = endettement
part1 = "openWithPostData('tableau.php',{'ICOM':'"
part2 = "','DEP':'"
part3 = "','TYPE':'BPS','PARAM':'5','EXERCICE':'"
part4 = "'})"

for exercice in exercices:  
    sortie = output1+exercice+".csv"

    # infos
    print("..."+exercice)
    time2 = time.time()

    # liste des libelles, par exercices
    libelles = []
    libelles0 = []

    if os.path.isfile(sortie):
        print("... "+sortie+" existe déjà")
    else:       
        # ouvrir Chrome
        browser = webdriver.Chrome(executable_path=racine+"\\python_scraper\\chromedriver")
        # ouvrir URL
        browser.get(url)

        # ouvrir fichier
        # chiffres cles
        fichier = open(sortie,"w")

        i = 0    
        for code in codes:
            # eviter les erreurs...
            i = i + 1
            if i == 1000:
                browser.quit()
                time.sleep(5)
                browser = webdriver.Chrome(executable_path=racine+"\\python_scraper\\chromedriver")
                browser.get(url)
                i = 0
       
            departement = "0"+code[0:2]
            commune = code[2:6]

            # nb: pas de données pour Mayotte (976)
            if departement == "097":
                if code[0:3]=="971":
                    departement = "101"
                if code[0:3]=="973":
                    departement = "102"
                if code[0:3]=="972":
                    departement = "103"
                if code[0:3]=="974":
                    departement = "104"
                
            browser.execute_script(part1+commune+part2+departement+part3+exercice+part4)  
            html_source = browser.page_source
       
            # gestion erreur: test si requete avec resultat, sinon passe
            # si oui, recherche les infos
            if "Données non disponibles" in html_source:
                fichier.write(code+";NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA")
                fichier.write(";NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA\n")
                
            else:
                # gestion d'erreur, si probleme, recharge la page
                try:       
                    trouver_EPCI = re.findall("SIREN\':\'(.*?)\',\'NOMDEP\'",html_source)                
                except:
                    html_source = browser.page_source
                    trouver_EPCI = re.findall("SIREN\':\'(.*?)\',\'NOMDEP\'",html_source)
                
                    try:
                        trouver_strate[0].replace("\xa0"," ")
                    except:
                        pass

                trouver_libelles = re.findall('<td class="libellepetitd">(.*?)</td>\n',html_source)
                trouver_chiffres = re.findall('<td class="montantpetitd">(.*?)\xa0</td>\n',html_source)

                # gestion erreur: si ne trouve pas toutes les valeurs
                # recherchees = erreur, sinon recupere les valeurs
                if len(trouver_chiffres)==0:
                    fichier.write(code+";NA;NA;NA;NA;NA;NA\n")

                else:
                    fichier.write(code+";")

                    trouver_libelles1 = []              
                    for lib in trouver_libelles:
                        if lib in libelles0:
                            trouver_libelles1.append(lib+"_MILLEUROS")
                            trouver_libelles1.append(lib+"_EUROHAB")
                            trouver_libelles1.append(lib+"_MOYSTRATE")                          
                        else:
                            libelles0.append(lib)
                            
                            libelles.append(lib+"_MILLEUROS")
                            libelles.append(lib+"_EUROHAB")
                            libelles.append(lib+"_MOYSTRATE")

                            trouver_libelles1.append(lib+"_MILLEUROS")
                            trouver_libelles1.append(lib+"_EUROHAB")
                            trouver_libelles1.append(lib+"_MOYSTRATE")

                    colonnes = []
                    for lib in libelles:
                        x = libelles.index(lib)
                        try:
                            i = trouver_libelles1.index(lib)
                            y = trouver_chiffres[i]
                        except:
                            y = "NA"
                        colonnes.append(y)

                    k = len(colonnes)
                    j = 1
                    for chiffre in colonnes:
                        if j == k:
                            fichier.write(chiffre+"\n")
                        else:
                            fichier.write(chiffre+";")
                        j = j + 1

        fichier.write("INSEE_COM;")
        k = len(libelles)
        j = 1
        for lib in libelles:
            if j == k:
                fichier.write(lib+"\n")
            else:
                fichier.write(lib+";")
            j = j + 1
                                  
        time2 = time.time() - time2
        print("Temps d'execution pour "+exercice+" : "+str(round(time2/60.0))+" min")

        browser.quit()
        fichier.close()

time1 = time.time() - time1
print("Temps d'execution total : "+str(round(time1/60.0))+" min")
