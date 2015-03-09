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

#### #### #### #### #### ####
# fonctionnement #
#### #### #### #### #### ####
print("Fonctionnement")

# mesure performance
time1 = time.time()

## Variables
# url
url = "http://alize2.finances.gouv.fr/communes/eneuro/tableau.php"

# dossiers
home = os.path.expanduser("~")
racine = home+"/Desktop/base_finances_collectivites"
data = racine+"/data"

# fichiers
code_input = racine+"/codes_collectivites/communes/codes_communes.csv"
output1 = data+"/fonctionnement"
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

# liste dates d'exercice  
exercices = ["2013","2012","2011","2010","2009","2008","2007","2006","2005","2004","2003","2002","2001","2000"]

# requete javascript
# PARAM = 1 = fonctionnement
part1 = "openWithPostData('tableau.php',{'ICOM':'"
part2 = "','DEP':'"
part3 = "','TYPE':'BPS','PARAM':'1','EXERCICE':'"
part4 = "'})"

for exercice in exercices:
    sortie = output1+exercice+".csv"
    if os.path.isfile(sortie):
        print("... "+sortie+" existe déjà")
    else:
        # infos
        print("..."+exercice)
        time2 = time.time()

        # ouvrir Chrome
        browser = webdriver.Chrome(executable_path=racine+"\\python_scraper\\chromedriver")
        # ouvrir URL
        browser.get(url)

        # ouvrir fichier
        # fonctionnement
        fichier = open(sortie,"w")
        
        fichier.write("INSEE_COM;A_MILLEUROS;A_EUROHAB;A_MOYSTRATE;")
        fichier.write("IMPOTS_MILLEUROS;IMPOTS_EUROHAB;IMPOTS_MOYSTRATE;")
        fichier.write("AUTRES_MILLEUROS;AUTRES_EUROHAB;AUTRES_MOYSTRATE;")
        fichier.write("DOTATION_MILLEUROS;DOTATION_EUROHAB;DOTATION_MOYSTRATE;")
        fichier.write("B_MILLEUROS;B_EUROHAB;B_MOYSTRATE;")
        fichier.write("PERSONNELS_MILLEUROS;PERSONNELS_EUROHAB;PERSONNELS_MOYSTRATE;")
        fichier.write("EXTERNES_MILLEUROS;EXTERNES_EUROHAB;EXTERNES_MOYSTRATE;")
        fichier.write("FINANCIERES_MILLEUROS;FINANCIERES_EUROHAB;FINANCIERES_MOYSTRATE;")
        fichier.write("CONTINGENTS_MILLEUROS;CONTINGENTS_EUROHAB;CONTINGENTS_MOYSTRATE;")
        fichier.write("SUBVENTIONS_MILLEUROS;SUBVENTIONS_EUROHAB;SUBVENTIONS_MOYSTRATE;")
        fichier.write("R_MILLEUROS;R_EUROHAB;R_MOYSTRATE\n")
        
        i = 0
        for code in codes:
            # prevention d'erreurs
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
                fichier.write(code+";NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;")
                fichier.write("NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;")
                fichier.write("NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA\n")

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

                trouver_fonctionnement = re.findall('<td class="montantpetitV">(.*?)\xa0</td>\n',html_source)

                # gestion erreur: si ne trouver pas toutes les valeurs
                # recherchees = erreur, sinon recupere les valeurs
                if len(trouver_fonctionnement)!=33:
                    fichier.write(code+";NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;")
                    fichier.write("NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;")
                    fichier.write("NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA\n")
                else:
                    A = trouver_fonctionnement[0:3]
                    impots = trouver_fonctionnement[3:6]
                    autres = trouver_fonctionnement[6:9]
                    dotation = trouver_fonctionnement[9:12]
                    B = trouver_fonctionnement[12:15]
                    personnels = trouver_fonctionnement[15:18]
                    externes = trouver_fonctionnement[18:21]
                    financieres = trouver_fonctionnement[21:24]
                    contingents = trouver_fonctionnement[24:27]
                    subventions = trouver_fonctionnement[27:30]
                    R = trouver_fonctionnement[30:33]

                    fichier.write(code+";"+str(A[0])+";"+str(A[1])+";"+str(A[2])+";")
                    fichier.write(str(impots[0])+";"+str(impots[1])+";"+str(impots[2])+";")
                    fichier.write(str(autres[0])+";"+str(autres[1])+";"+str(autres[2])+";")
                    fichier.write(str(dotation[0])+";"+str(dotation[1])+";"+str(dotation[2])+";")
                    fichier.write(str(B[0])+";"+str(B[1])+";"+str(B[2])+";")
                    fichier.write(str(personnels[0])+";"+str(personnels[1])+";"+str(personnels[2])+";")
                    fichier.write(str(externes[0])+";"+str(externes[1])+";"+str(externes[2])+";")
                    fichier.write(str(financieres[0])+";"+str(financieres[1])+";"+str(financieres[2])+";")
                    fichier.write(str(contingents[0])+";"+str(contingents[1])+";"+str(contingents[2])+";")
                    fichier.write(str(subventions[0])+";"+str(subventions[1])+";"+str(subventions[2])+";")
                    fichier.write(str(R[0])+";"+str(R[1])+";"+str(R[2])+"\n")

        time2 = time.time() - time2
        print("Temps d'execution pour "+exercice+" : "+str(round(time2/60.0))+" min")

        browser.quit()
        fichier.close()

time1 = time.time() - time1
print("Temps d'execution total : "+str(round(time1/60.0))+" min")
