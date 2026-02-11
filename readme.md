Gestion des produits d’une boutique
Objectifs

Ce projet vise à développer une application console permettant la gestion des produits d’une boutique. L’objectif principal est de créer un outil en Python connecté à une base de données MySQL, qui permet aux utilisateurs d’ajouter, de modifier, de supprimer ou de mettre à jour des produits. Toutes ces actions sont directement appliquées à la base de données, afin d’assurer la cohérence et la centralisation des informations.

L’application prévoit également une gestion des catégories de produits, des utilisateurs et des rôles, ainsi qu’un tableau de bord fournissant des statistiques sur le stock.

Procédure
Base de données

La base de données utilisée s’appelle gestion_stock et contient deux tables principales : produits et Categories. La table Categories contient l’identifiant et le nom des catégories de produits. La table produits contient l’identifiant du produit, son nom, son prix, la quantité en stock ainsi que la référence à la catégorie à laquelle il appartient. La relation entre ces deux tables est de type un-à-plusieurs : une catégorie peut contenir plusieurs produits.

Connexion Python – MySQL

L’application se connecte à la base de données MySQL via un connecteur Python. Cette connexion permet d’exécuter toutes les opérations CRUD (Create, Read, Update, Delete) sur les produits et les catégories, ainsi que de gérer les utilisateurs et leurs rôles.

Fonctionnalités
Pour l’administrateur

Ajouter, modifier et supprimer des produits et des catégories.

Créer des utilisateurs et définir leur rôle (admin ou caissier).

Accéder à un tableau de bord affichant :

Le produit le plus cher

La valeur totale du stock

Le nombre de produits par catégorie

Pour le caissier

Consulter uniquement la liste des produits existants dans le stock.

Aucune possibilité de modification, de suppression ou de création d’éléments.

Gestion des utilisateurs

Le système prévoit une authentification obligatoire pour tous les utilisateurs. Chaque utilisateur possède un rôle qui détermine les fonctionnalités accessibles. L’administrateur a accès à toutes les fonctionnalités, tandis que le caissier n’a accès qu’à la consultation du stock.

Organisation du projet

L’application est structurée en différentes fonctions pour chaque action : ajout de produits ou de catégories, mise à jour du stock, recherche et suppression de produits ou de catégories, création d’utilisateurs et gestion de l’authentification. Les menus sont adaptés en fonction du rôle de l’utilisateur pour garantir que chaque utilisateur n’accède qu’aux fonctionnalités qui lui sont autorisées.

Utilisation

L’application se lance en console et demande d’abord à l’utilisateur de s’authentifier. Après la connexion, le menu correspondant au rôle de l’utilisateur est affiché. L’administrateur dispose d’un menu complet, tandis que le caissier ne voit qu’une version simplifiée lui permettant uniquement de consulter la liste des produits.