# impmagic
## Informations
Librairie pour l'importation optimisé de module python.
Fonctionne principalement avec des décorateurs, ce qui permet de charger les modules uniquement lorsqu'ils sont nécessaires.
Toutes ces fonctions se basent sur un système de cache pour recharger plus rapidement les modules lorsqu'ils sont appelés par d'autres fonctions.

### Prérequis
- Python 3
<br>

# Installation
```console
pip install impmagic
```
<br>

# Utilisation
### Importer des modules avec un décorateur
Cette option permet d'importer les modules nécessaires à la fonction uniquement lorsque celle-ci est utilisé.
Pour son fonctionnement, il faut lui envoyer une liste ou un tuple contenant des dictionnaires d'informations.
Chaque dictionnaire doit contenir au minimum la clé module, mais peut également contenir une liste de sous-module (submodule) ou encore l'option as (comme les import classique)
```python
@impmagic.loader(
        {'module':'zpp_args'},
        {'module':'os.path', 'submodule': ['exists']}, 
        {'module':'psutil', 'as': 'psfunction'}, 
        {'module':'toml_nxs.toml', 'submodule': ['TOML'], 'as': 'TOMLnxs'}
    )
    def function(self):
	    #MyCode
```
<br>

### Importer des modules dans une fonction
Il est également possible de charger des modules dans une fonction. Pour cela, on utilise la méthode load.
Nous pouvons lui envoyer un simple str avec le nom du module, mais nous pouvons également lui envoyer les mêmes types de données que le décorateur loader.
```python
impmagic.load('os')
```
<br>

### Enlever un module importé
Il est possible de supprimer d'une fonction un module qui a été importé précédemment.
Il suffit d'appeler la méthode unload avec le nom du module en paramètre.
Par défaut, le module restera dans le cache, il faut ajouter l'option uncache=True pour le supprimer également du cache.
```python
impmagic.unload('os')
```
<br>

### Réimporter un module
Il est possible de réimporter un module déjà importé. 
Cela peut être nécessaire lorsque nous faisons des tests sur un module et que nous voulons voir les changements de suite sans avoir besoin de quitter le shell en cours.
```python
impmagic.reload('os')
```
<br>

### Utiliser un module sans l'importer
Il est possible d'utiliser un module sans avoir besoin de l'importer grâce à la méthode get.
```python
module = impmagic.get('os')
module.mkdir(dir)
```