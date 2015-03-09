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
# chiffres cles, infos communes #
#### #### #### #### #### #### ###
print("Chiffres clés et information sur les communes...")

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
output0 = data+"/infocommunes"
output1 = data+"/chiffrescles"
code_input = code_input.replace("\\","/")
output0 = output1.replace("\\",'/')
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
# PARAM = 0 = chiffres cles
part1 = "openWithPostData('tableau.php',{'ICOM':'"
part2 = "','DEP':'"
part3 = "','TYPE':'BPS','PARAM':'0','EXERCICE':'"
part4 = "'})"

for exercice in exercices:  
    sortie = output1+exercice+".csv"

    # infos
    print("..."+exercice)
    time2 = time.time()
    
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

        fichier.write("INSEE_COM;A_MILLEUROS;A_EUROHAB;A_MOYSTRATE;")
        fichier.write("B_MILLEUROS;B_EUROHAB;B_MOYSTRATE;")
        fichier.write("R_MILLEUROS;R_EUROHAB;R_MOYSTRATE;")
        fichier.write("C_MILLEUROS;C_EUROHAB;C_MOYSTRATE;")
        fichier.write("D_MILLEUROS;D_EUROHAB;D_MOYSTRATE;")
        fichier.write("E_MILLEUROS;E_EUROHAB;E_MOYSTRATE;")
        fichier.write("CAF_MILLEUROS;CAF_EUROHAB;CAF_MOYSTRATE;")
        fichier.write("ROULEMENT_MILLEUROS;ROULEMENT_EUROHAB;ROULEMENT_MOYSTRATE\n")

        # info_communes
        fichier1 = open(output0+exercice+".csv","w")
        fichier1.write("INSEE_COM;NOM;EXERCICE;POP_1JANVIER;BUDGET;STRATE;SIREN_EPCI\n")

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
                fichier.write(code+";NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;")
                fichier.write("NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA\n")

                # infos communes
                fichier1.write(code+";"+"NA"+";"+exercice+";"+"NA"+";"+"NA"+";")
                fichier1.write("NA"+";"+"NA"+"\n")
          
            else:

                # gestion d'erreur, si probleme, recharge la page
                try:       
                    trouver_nom = re.findall('<span style="font-weight:bold;font-size:12pt;color:#fe9805">(.*?)</span><span class="titre">',html_source)
            
                    trouver_pop = re.findall('Population légale en vigueur au 1er janvier de l\'EXERCICE : (.*?)\xa0Habitants \n- Budget principal seul',html_source)
            
                    trouver_budget = re.findall('\\xa0Habitants \\n- (.*?)</td>',html_source)

                    trouver_strate = re.findall('<td class="libellepetit">\tStrate : (.*?)\\n</td>\\n</tr>',html_source)
                    trouver_strate[0].replace("\xa0"," ")

                    trouver_EPCI = re.findall("SIREN\':\'(.*?)\',\'NOMDEP\'",html_source)
                
                except:
                    html_source = browser.page_source

                    trouver_nom = re.findall('<span style="font-weight:bold;font-size:12pt;color:#fe9805">(.*?)</span><span class="titre">',html_source)
                   
                    trouver_pop = re.findall('Population légale en vigueur au 1er janvier de l\'EXERCICE : (.*?)\xa0Habitants \n- Budget principal seul',html_source)
            
                    trouver_budget = re.findall('\\xa0Habitants \\n- (.*?)</td>',html_source)

                    trouver_strate = re.findall('<td class="libellepetit">\tStrate : (.*?)\\n</td>\\n</tr>',html_source)

                    trouver_EPCI = re.findall("SIREN\':\'(.*?)\',\'NOMDEP\'",html_source)
                
                    try:
                        trouver_strate[0].replace("\xa0"," ")
                    except:
                        pass

                trouver_chiffres = re.findall('<td class="montantpetit">(.*?)\xa0</td>\n',html_source)

                # gestion erreur: si ne trouve pas toutes les valeurs
                # recherchees = erreur, sinon recupere les valeurs
                if len(trouver_nom)==0:
                    trouver_nom = ["NA"]

                if len(trouver_pop )==0:
                    trouver_pop = ["NA"]
               
                if len(trouver_budget)==0:
                    trouver_budget = ["NA"]

                if len(trouver_strate)==0:
                    trouver_strate = ["NA"]
               
                if len(trouver_EPCI) == 0:
                    trouver_EPCI = ["NA"] 

                if len(trouver_chiffres)!=24:
                    fichier.write(code+";NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;")
                    fichier.write("NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA;NA\n")
                else:                  
                    A = trouver_chiffres[0:3]
                    B = trouver_chiffres[3:6]
                    R = trouver_chiffres[6:9]
                    C = trouver_chiffres[9:12]
                    D = trouver_chiffres[12:15]
                    E = trouver_chiffres[15:18]
                    CAF = trouver_chiffres[18:21]
                    ROULEMENT = trouver_chiffres[21:24]

                    fichier.write(code+";"+str(A[0])+";"+str(A[1])+";"+str(A[2])+";")
                    fichier.write(str(B[0])+";"+str(B[1])+";"+str(B[2])+";")
                    fichier.write(str(R[0])+";"+str(R[1])+";"+str(R[2])+";")
                    fichier.write(str(C[0])+";"+str(C[1])+";"+str(C[2])+";")
                    fichier.write(str(D[0])+";"+str(D[1])+";"+str(D[2])+";")
                    fichier.write(str(E[0])+";"+str(E[1])+";"+str(E[2])+";")
                    fichier.write(str(CAF[0])+";"+str(CAF[1])+";"+str(CAF[2])+";")
                    fichier.write(str(ROULEMENT[0])+";"+str(ROULEMENT[1])+";"+str(ROULEMENT[2])+"\n")

                    # infos communes
                    fichier1.write(code+";"+trouver_nom[0]+";"+exercice+";")
                    fichier1.write(trouver_pop[0]+";"+trouver_budget[0]+";")
                    fichier1.write(trouver_strate[0]+";"+trouver_EPCI[0]+"\n")
                    
        time2 = time.time() - time2
        print("Temps d'execution pour "+exercice+" : "+str(round(time2/60.0))+" min")

        browser.quit()
        fichier.close()
        fichier1.close()

time1 = time.time() - time1
print("Temps d'execution total : "+str(round(time1/60.0))+" min")
