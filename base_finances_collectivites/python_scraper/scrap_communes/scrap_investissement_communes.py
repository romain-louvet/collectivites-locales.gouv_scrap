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

# mesure performance globale
time0 = time.time()

#### #### #### #### #### #### ###
#       Investissement          #
#### #### #### #### #### #### ###
print("Investissement...")

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
output1 = data+"/investissement"
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
# PARAM = 2 = investissement
part1 = "openWithPostData('tableau.php',{'ICOM':'"
part2 = "','DEP':'"
part3 = "','TYPE':'BPS','PARAM':'2','EXERCICE':'"
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
        browser = webdriver.Chrome(executable_path=racine+"/python_scraper/chromedriver")
        # ouvrir URL
        browser.get(url)

        # ouvrir fichier
        # fonctionnement
        fichier = open(sortie,"w")
        
        fichier.write("INSEE_COM;C_MILLEUROS;C_EUROHAB;C_MOYSTRATE;")
        fichier.write("EMPRNTS_MILLEUROS;EMPRNTS_EUROHAB;EMPRNTS_MOYSTRATE;")
        fichier.write("SUBVNTNS_MILLEUROS;SUBVNTNS_EUROHAB;SUBVNTNS_MOYSTRATE;")
        fichier.write("FCTVA_MILLEUROS;FCTVA_EUROHAB;FCTVA_MOYSTRATE;")
        fichier.write("BIENS_MILLEUROS;BIENS_EUROHAB;BIENS_MOYSTRATE;")
        fichier.write("D_MILLEUROS;D_EUROHAB;D_MOYSTRATE;")
        fichier.write("EQUIPMNT_MILLEUROS;EQUIPMNT_EUROHAB;EQUIPMNT_MOYSTRATE;")
        fichier.write("REMBRSMNT_MILLEUROS;REMBRSMNT_EUROHAB;REMBRSMNT_MOYSTRATE;")
        fichier.write("CHARGES_MILLEUROS;CHARGES_EUROHAB;CHARGES_MOYSTRATE;")
        fichier.write("IMMBLSTNS_MILLEUROS;IMMBLSTNS_EUROHAB;IMMBLSTNS_MOYSTRATE;")
        fichier.write("E_MILLEUROS;E_EUROHAB;E_MOYSTRATE\n")

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

                trouver_chiffres = re.findall('<td class="montantpetiti">(.*?)\xa0</td>\n',html_source)

                # gestion erreur: si ne trouver pas toutes les valeurs
                # recherchees = erreur, sinon recupere les valeurs
                if len(trouver_chiffres)!=33:
                    fichier.write(code+";NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;")
                    fichier.write("NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;")
                    fichier.write("NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA\n")
                else:
                    C = trouver_chiffres[0:3]
                    EMPRNTS = trouver_chiffres[3:6]
                    SUBVNTNS = trouver_chiffres[6:9]
                    FCTVA = trouver_chiffres[9:12]
                    BIENS = trouver_chiffres[12:15]
                    D = trouver_chiffres[15:18]
                    EQUIPMNT = trouver_chiffres[18:21]
                    REMBRSMNT = trouver_chiffres[21:24]
                    CHARGES = trouver_chiffres[24:27]
                    IMMBLSTNS = trouver_chiffres[27:30]
                    E = trouver_chiffres[30:33]

                    fichier.write(code+";"+str(C[0])+";"+str(C[1])+";"+str(C[2])+";")
                    fichier.write(str(EMPRNTS[0])+";"+str(EMPRNTS[1])+";"+str(EMPRNTS[2])+";")
                    fichier.write(str(SUBVNTNS[0])+";"+str(SUBVNTNS[1])+";"+str(SUBVNTNS[2])+";")
                    fichier.write(str(FCTVA[0])+";"+str(FCTVA[1])+";"+str(FCTVA[2])+";")
                    fichier.write(str(BIENS[0])+";"+str(BIENS[1])+";"+str(BIENS[2])+";")
                    fichier.write(str(D[0])+";"+str(D[1])+";"+str(D[2])+";")
                    fichier.write(str(EQUIPMNT[0])+";"+str(EQUIPMNT[1])+";"+str(EQUIPMNT[2])+";")
                    fichier.write(str(REMBRSMNT[0])+";"+str(REMBRSMNT[1])+";"+str(REMBRSMNT[2])+";")
                    fichier.write(str(CHARGES[0])+";"+str(CHARGES[1])+";"+str(CHARGES[2])+";")
                    fichier.write(str(IMMBLSTNS[0])+";"+str(IMMBLSTNS[1])+";"+str(IMMBLSTNS[2])+";")
                    fichier.write(str(E[0])+";"+str(E[1])+";"+str(E[2])+"\n")

        time2 = time.time() - time2
        print("Temps d'execution pour "+exercice+" : "+str(round(time2/60.0))+" min")

        browser.quit()
        fichier.close()

time1 = time.time() - time1
print("Temps d'execution total : "+str(round(time1/60.0))+" min")
