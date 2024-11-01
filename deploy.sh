#!/bin/bash
# Déploiement automatique du programme Python sur le Raspberry Pi

# Variables
source .env

# Synchronisation des fichiers
echo "Synchronisation des fichiers..."
rsync -avz --exclude='.git' --exclude='venv' $LOCAL_PATH $PI_USER@$PI_HOST:$PI_PATH

# Arrêt du programme Python en cours sur le Raspberry Pi
if ssh $PI_USER@$PI_HOST "pgrep -f 'python3 .*spot\.py' > /dev/null"; then
    echo "Arrêt des processus Python en cours sur le Raspberry Pi..."
    ssh $PI_USER@$PI_HOST "pkill -f 'python3 .*spot\.py'"
    sleep 2  # Pause pour assurer que les processus sont arrêtés
else
    echo "Aucun processus Python à arrêter."
fi

# Vérification des dépendances sur le Raspberry Pi
echo "Vérification des dépendances sur le Raspberry Pi..."
ssh $PI_USER@$PI_HOST "dpkg -l build-essential libcap-dev python3 python3-pip python3-venv fbi python3-picamzero python3-libcamera > /dev/null 2>&1 || sudo apt-get install -y build-essential libcap-dev python3 python3-pip python3-venv fbi python3-picamzero python3-libcamera"

# Création d'un environnement virtuel et installation des bibliothèques Python
if ssh $PI_USER@$PI_HOST "[ ! -d $PI_PATH/venv ]"; then
    echo "Création de l'environnement virtuel et installation des bibliothèques..."
    ssh $PI_USER@$PI_HOST "cd $PI_PATH && python3 -m venv venv --system-site-packages && source venv/bin/activate && pip install -r requirements.txt"
else
    echo "L'environnement virtuel existe déjà. Mise à jour des bibliothèques..."
    ssh $PI_USER@$PI_HOST "cd $PI_PATH && source venv/bin/activate && pip install -r requirements.txt"
fi

# Exécution du programme Python sur le Raspberry Pi dans l'environnement virtuel
echo "Exécution du programme Python sur le Raspberry Pi..."
ssh $PI_USER@$PI_HOST "cd $PI_PATH && source venv/bin/activate && nohup python3 spot.py > output.log 2>&1 &"

# Vérification que le nouveau processus est lancé
sleep 2
if ssh $PI_USER@$PI_HOST "pgrep -f 'python3 .*spot\.py' > /dev/null"; then
    echo "Nouveau processus lancé avec succès"
else
    echo "Échec du lancement du nouveau processus"
    exit 1
fi
