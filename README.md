# Twitter Sentiment
## Dépendances
- Python 3.X
- Une version récente de stanza
- Un modèle français pour stanza

## Utilisation
Lancer sentiment.py pour le logiciel principal d'analyse Twitter, ou pour tester l'analyse de sentiment avec des phrases personnalisées.

Lancer analyse.py pour effectuer des tests de l'analyse de sentiment sur des jeux des données préfaits, a savoir : des phrases comportant de l'ironie, des phrases comportant des négations, un jeu de tweets comportant "#haine" et un jeu de tweets comportant le "#bonheur".

Par défaut, ces deux fichiers utiliseront le chemin par defaut des modèles de langue stanza. Si vos modèles ne sont pas au chemin par défaut, vous pouvez précisez le chemin du dossier `stanza_resources` en paramétrant la variable d'environnement DATA_DIR.
Par exemple:

`DATA_DIR=/un/autre/chemin/stanza_resources python3 sentiment.py`