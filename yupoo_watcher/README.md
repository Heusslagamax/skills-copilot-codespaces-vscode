# Yupoo Watcher

Ce projet contient un script Python qui surveille le site Yupoo de TopHotFashion et envoie une notification Telegram lorsqu'un nouvel album est publié.

## Prérequis

- Python 3.8 ou plus
- [pip](https://pip.pypa.io/en/stable/)
- Un bot Telegram et votre `chat_id`

## Installation

1. Clonez ce dépôt.
2. Copiez le fichier `.env.example` en `.env` et renseignez votre `TELEGRAM_TOKEN` et `TELEGRAM_CHAT_ID`.
3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

Lancez simplement le script :

```bash
python watcher.py
```

Le script vérifie toutes les 5 minutes si de nouveaux albums sont publiés. Les notifications envoyées sont consignées dans `log.txt`.

## Fichiers

- `watcher.py` : script principal.
- `.env` : variables d'environnement (à créer à partir de `.env.example`).
- `seen_albums.txt` : historique local des albums déjà signalés.
- `log.txt` : journal des notifications.

