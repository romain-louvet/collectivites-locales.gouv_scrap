---
title: "Lisez-moi - collectivites-locales.gouv_scrap"
author: Romain Louvet
date: "Lundi, 10 Mars, 2015"
output: html_document
---

Ce document décrit le contenu du repository "collectivites-locales.gouv_scrap", créé pour partager les scripts permettant le *scraping* des données individuelles sur les budgets des collectivités territoriales à partir du site ["collectivites-locales.gouv"](http://www.collectivites-locales.gouv.fr/). Ces scripts ont été écrits en Python 3.4.

Le détail du contenu du dossier "base_finances_collectivites" est présenté ci-dessous. Il est nécessaire de télécharger ce dossier sur le bureau pour que les scripts fonctionnent. Il n'est pas nécessaire de réutiliser les scripts pour accéder aux **données obtenues**, les liens pour le téléchargement sont indiqués ci-après. Afin de cartographier ces données, des **fonds de cartes** sont également disponibles en téléchargement. Ils sont issus de la base GEOFLA (IGN).

### Principes du *scraping*

'''Cette partie présente les principes généraux du scraping. Pour plus d'information sur les scripts utilisés dans ce cas précis, voir la partie concernant les scripts Python.'''

La donnée publique étant amenée à être de plus en plus accessible via Internet, cela n'implique pas nécessairement pour autant que cet accès permette un téléchargement d'une base de données complète, organisée, et surtout géolocalisée avec précision, répondant aux attentes des chercheurs en géographie. Bien des sites officiels proposent une consultation sélective de la données, mais pas le téléchargement de l'ensemble des informations en une seule fois. La problématique n'est de ce point de vue plus l'accès à l'information, mais plutôt sa collecte et sa mise en forme de façon organisée. Le *web scraping* est une solution possible à cette problématique.

Le *web scraping*, ou simplement *scraping* et également *crawling*, consiste à parcourir l'Internet afin de récupérer des informations à l'aide d'un programme informatique. Cette méthode peut servir notamment à constituer automatiquement des bases de données, dans la mesure où les sites consultés ne mentionnent pas l'interdiction de cette pratique dans leurs conditions d'utilisation.

Le *web scraping* est possible lorsque les informations consultables sur un site "à l'unité" (par exemple, commune par commune) sont toutes générées selon le même format. Deux solutions existent, leur finalité est indentique ainsi que leur principe, seul la technique change légèrement. Ces solutions consistent à créer une boucle qui va permettre de consulter l'ensemble de informations individuelles disponibles sur un site et de récupérer dans le code source de la page consultée les informations recherchées. La technique diffère selon le mode d'accès aux données individuelles : si le serveur hébergeant le site génère une URL spécifique pour chaque élément de sa base de données (en PHP), la boucle du programme informatique consiste à se connecter à toutes les URL en les générants automatiquement, ce qui permet de se passer d'un navigateur ; par contre, si l'URL est toujours la même, alors il s'agit d'un serveur répondant à des requêtes en javascript pour afficher les informations disponibles dans sa base de données, le programme doit par conséquent envoyer des requêtes javascript en boucle à un navigateur, ce qui est plus long.

Ces techniques nécessitent la connaissance a priori de l'ensemble des unités qui constituerons les lignes de la base de données. Le cas le plus fréquent, qui intéresse le géographe, consiste à identifier les codes géographiques utilisés (par exemple : les codes INSEE) et comment ils sont employés dans la constitution de l'URL ou de la requête javascript, puis à récupérer la liste de ces codes pour pouvoir générer automatiquement toutes les URL ou toute les requêtes javascript permettant de collecter les données disponibles sur le site.

### Contenu du dossier "base_finances_collectivites"

###### Codes collectivités

Les codes utilisés pour collecter les données sont issus de la base GEOFLA 2014 de l'IGN pour les communes, les départements et les régions.

###### Documentation

La documentation a été téléchargée à l'adresse suivante : [http://www.collectivites-locales.gouv.fr/methodologie-des-donnees-individuelles](http://www.collectivites-locales.gouv.fr/methodologie-des-donnees-individuelles)

Ces documents détaillent la méthode de collecte des données originales, ainsi que les définitions des termes employés pour désigner les valeurs contenues dans les tableaux.

###### Scripts Python

### Données obtenues

- [budget des communes, de 2000 à 2013](https://www.dropbox.com/s/bob2cr8mhnfwb4v/coll_loc_comm2000_2013.7z?dl=0)
- budget des EPCI, de 2007 à 2013
- budget des départements, de 2008 à 2013
- budget des régions, de 2008 à 2013

### Fonds cartographiques

- [communes (2014), départements (2014), régions (2014) et EPCI (2007 à 2014) de métropole](https://www.dropbox.com/s/0pmx33mzzempu43/base_fi_coll_carto_metropole.7z?dl=0)
- [communes (2014), départements (2014), régions (2014) et EPCI (2007 à 2014) des DOM (Mayotte exceptée)]()
