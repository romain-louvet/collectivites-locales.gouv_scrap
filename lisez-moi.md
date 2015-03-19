---
title: "Lisez-moi - collectivites-locales.gouv_scrap"
author: Romain Louvet
date: "Mercredi, 11 Mars, 2015"
output: html_document
---

Ce document décrit le contenu du repository "collectivites-locales.gouv_scrap", créé pour partager les scripts permettant le *scraping* des données individuelles sur les budgets des collectivités territoriales à partir du site ["collectivites-locales.gouv"](http://www.collectivites-locales.gouv.fr/) ainsi que les liens pour télécharger les bases de données mises en forme grâce à ces scripts. Ceux-ci ont été écrits en Python 3.4.

Le détail du contenu du dossier "base_finances_collectivites" est présenté ci-dessous. Il est nécessaire de télécharger ce dossier sur le bureau pour que les scripts fonctionnent. Il n'est pas nécessaire de réutiliser les scripts pour accéder aux **données obtenues**, les liens pour le téléchargement sont indiqués ci-après. Afin de cartographier ces données, des **fonds de cartes** sont également disponibles en téléchargement. Ils sont issus de la base [GEOFLA (IGN)](http://professionnels.ign.fr/geofla).

### Principes du *scraping*

```
Cette partie présente les principes généraux du scraping. Pour plus d'informations sur 
les scripts utilisés dans ce cas précis, voir la partie concernant les scripts Python.
```

La donnée publique étant amenée à être de plus en plus accessible via Internet, cela n'implique pas pour autant que cet accès permette le téléchargement d'une base de données répondant aux attentes des chercheurs en géographie, c'est-à-dire complète, organisée, et surtout géolocalisée avec précision. Bien des sites officiels proposent une consultation sélective de la données, mais pas le téléchargement de l'ensemble des informations en une seule fois. La problématique n'est de ce point de vue plus l'accès à l'information, mais plutôt sa collecte et sa mise en forme de façon organisée. Le *web scraping* apparait alors comme une solution possible.

Le *web scraping*, ou simplement *scraping* ou *crawling*, consiste à parcourir l'Internet afin de récupérer des informations à l'aide d'un programme informatique. Parmi ces automates "arpenteurs", le plus connu est sans aucun doute celui employé par Google et servant à classer les pages web en fonction du nombre de liens présents sur d'autres sites renvoyant vers elles (robot d'indexation). Mais d'autres applications sont possibles, dont notamment l'utilisation d'un *scraper* pour constituer automatiquement des bases de données (dans la mesure où les sites consultés ne mentionnent pas l'interdiction de cette pratique dans leurs conditions d'utilisation). Des outils spécifiques existent pour faciliter la création de ce type de programme, dont le plus connu est Scrapy.

La création d'une base de données à l'aide du *web scraping* est possible (facilement) lorsque les informations consultables sur un site "à l'unité" (par exemple, commune par commune) sont toutes générées selon le même format. Deux solutions existent, leur finalité est indentique ainsi que leur principe, seul la technique change légèrement. Ces solutions consistent à créer une boucle qui va permettre de consulter l'ensemble de informations individuelles disponibles sur un site et de récupérer dans le code source de la page consultée les informations recherchées. La technique diffère selon le mode d'accès aux données individuelles : si le serveur hébergeant le site génère une URL spécifique pour chaque élément de sa base de données (en PHP), la boucle du programme informatique consiste à se connecter à toutes les URL en les générants automatiquement, ce qui permet de se passer d'un navigateur ; par contre, si l'URL est toujours la même, alors il s'agit d'un serveur répondant à des requêtes en javascript pour afficher les informations disponibles dans sa base de données, le programme doit par conséquent envoyer des requêtes javascript en boucle à un navigateur connecté à une URL unique, ce qui est plus long.

Ces techniques nécessitent la connaissance *a priori* de l'ensemble des unités qui constituerons les lignes de la base de données. Le cas le plus fréquent, qui intéresse le géographe, consiste à identifier les codes géographiques utilisés (par exemple : les codes INSEE) et comment ils sont employés dans la constitution de l'URL ou de la requête javascript, puis à récupérer la liste de ces codes afin de générer automatiquement toutes les URL ou toutes les requêtes javascript permettant de collecter les données disponibles sur le site.

### Contenu du dossier "base_finances_collectivites"

###### Codes collectivités

Ce dossier contient les les codes utilisés pour collecter les données. Ces codes sont issus de la base [GEOFLA 2014 de l'IGN](http://professionnels.ign.fr/geofla) pour les communes, les départements et les régions, téléchargés en février 2015. Les codes des EPCI ainsi que des communes par EPCI ont été téléchargés sur ["collectivites-locales.gouv"](http://www.collectivites-locales.gouv.fr/), également en février 2015.

###### Documentation

Ce dossier contient la documentation téléchargée à l'adresse suivante : [http://www.collectivites-locales.gouv.fr/methodologie-des-donnees-individuelles](http://www.collectivites-locales.gouv.fr/methodologie-des-donnees-individuelles)

Ces documents détaillent la méthode de collecte des données originales, ainsi que les définitions des termes employés pour désigner les valeurs contenues dans les tableaux des données originales. Il s'agit de la documentation disponible en février 2015.

###### Scripts Python

Ce dossier contient les scripts programmés en Python 3.4 qui ont été utilisés pour collecter les informations et constituer les bases de données téléchargeables ci-dessous ("Données obtenues"). L'accès aux données n'étant que possible par requête javascript, les scripts nécessitent l'utilisation de la bibliothèque "Selenium". Chrome a été utilisé comme navigateur, le driver pour ce navigateur de la dernière version de Selenium disponible au moment de la programmation (février 2015) est fourni. Le détail du fonctionnement est accessible grâce aux commentaires dans chacun des scripts. La programmation en Python a été choisie plutôt que l'utilisation de Scrapy pour sa souplesse, et également parce que mieux connue et plus largement utilisée.

Ces scripts ont produit des fichiers csv, un par année et par thème (chiffres clés, autofinancement, investissement, etc.) qui ont été ensuite rassemblés manuellement sous la forme d'un fichier xlsx, un par thème, une feuille par année. Cette étape manuelle fut l'occasion d'un contrôle (non exhaustif) des résultats de la collecte ainsi que l'ajout d'une feuille de métadonnées.

Les données collectées n'ont pas été modifiées par les scripts, uniquement mises en forme pour être utilisables facilement avec un fond de carte dans un SIG et avec un tableur. Lorsque les données n'étaient pas disponibles, la valeur "NA" a été utilisée.

### Données obtenues

Chacune des bases possède la même organisation par thème des éléments du budget des collectivités locales telle que présentée sur le site, à savoir : ***chiffres clés, fonctionnement, investissement, fiscalité, et autofinancement***. Un fichier excel est disponible par thème et contient les données par année (une feuille par année), plus une feuille de métadonnées (dont en particulier le nom des champs). Chaque base correspond à un échelon dans les différents niveaux de collectivités territoriales et est ici présentée par ordre d'échelle, de la plus grande échelle à la plus petite :

- [budget des communes, de 2000 à 2013](https://www.dropbox.com/s/bob2cr8mhnfwb4v/coll_loc_comm2000_2013.7z?dl=0)
- budget des EPCI, de 2007 à 2013
- budget des départements, de 2008 à 2013
- budget des régions, de 2008 à 2013

Les informations disponibles varient d'une base à l'autre et selon les années. Ces données couvrent la France entière (métropole et DOM compris) à l'exception de Mayotte.

### Fonds cartographiques

Les fonds géographiques sont issus de [GEOFLA 2014 (IGN)](http://professionnels.ign.fr/geofla). Les régions ont été créées par fusion des départements. Les EPCI ont été créées par fusion des communes, après jointure du fond [GEOFLA (IGN)](http://professionnels.ign.fr/geofla) de l'année correspondante avec les compositions des EPCI par année disponible sur www.collectivites-locales.gouv.fr. Les EPCI antérieures à 2011 ont été générées à l'aide du fond [GEOFLA (IGN)](http://professionnels.ign.fr/geofla) de 2011 (les versions des années antérieures à 2011 n'étant pas disponible sur le site de l'IGN). Les traitements ont été effectués à l'aide d'ArcGis 10.

- [communes (2014), départements (2014), régions (2014) et EPCI (2007 à 2014) de métropole](https://www.dropbox.com/s/0pmx33mzzempu43/base_fi_coll_carto_metropole.7z?dl=0)
- communes (2014), départements (2014), régions (2014) et EPCI (2007 à 2014) des DOM (Mayotte exceptée)
