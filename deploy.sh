#!/bin/bash
# Amélioration du script de déploiement automatique du programme Python sur le Raspberry Pi

# Variables
source .env

# Synchronisation des fichiers
./transfer.sh

# Arrêt du programme Python en cours sur le Raspberry Pi
if ssh "$PI_USER@$PI_HOST" "pgrep -f 'python3 .*spot\.py' > /dev/null"; then
    echo "Arrêt des processus Python en cours sur le Raspberry Pi..."
    ssh "$PI_USER@$PI_HOST" "pkill -f 'python3 .*spot\.py'"
    sleep 2  # Pause pour s'assurer que les processus sont arrêtés
else
    echo "Aucun processus Python à arrêter."
fi

# Vérification des dépendances sur le Raspberry Pi
echo "Vérification des dépendances sur le Raspberry Pi..."
ssh "$PI_USER@$PI_HOST" << EOF
  if ! dpkg -l build-essential libcap-dev python3 python3-pip python3-venv fbi python3-picamzero python3-libcamera > /dev/null 2>&1; then
    echo "Installation des dépendances..."
    sudo apt-get update
    sudo apt-get install -y build-essential libcap-dev python3 python3-pip python3-venv fbi python3-picamzero python3-libcamera
  else
    echo "Toutes les dépendances sont déjà installées."
  fi
EOF

# Création d'un environnement virtuel et installation des bibliothèques Python
if ssh $PI_USER@$PI_HOST "[ ! -d $PI_PATH/venv ]"; then
    echo "Création de l'environnement virtuel et installation des bibliothèques..."
    ssh $PI_USER@$PI_HOST "cd $PI_PATH && python3 -m venv venv --system-site-packages && source venv/bin/activate && pip install -r requirements.txt"
else
    echo "L'environnement virtuel existe déjà. Mise à jour des bibliothèques..."
    ssh $PI_USER@$PI_HOST "cd $PI_PATH && source venv/bin/activate && pip install -r requirements.txt"
fi

# Arrêt de tous les processus Python préexistants (pour éviter les duplications)
echo "Arrêt de tous les processus Python avant de relancer le programme..."
ssh "$PI_USER@$PI_HOST" "pkill -f 'python3 .*spot\.py'" || true
sleep 2

# Exécution du programme Python sur le Raspberry Pi dans l'environnement virtuel
echo "Exécution du programme Python sur le Raspberry Pi..."
ssh "$PI_USER@$PI_HOST" "cd $PI_PATH && source venv/bin/activate && nohup python3 spot.py > spot.log 2>&1 &" || true

# Vérification que le nouveau processus est lancé
sleep 10
process_count=$(ssh "$PI_USER@$PI_HOST" "pgrep -f 'python3 .*spot\.py' | wc -l")
if [ "$process_count" -eq 1 ]; then
    echo "Nouveau processus lancé avec succès."
elif [ "$process_count" -gt 1 ]; then
    echo "Plusieurs processus détectés, un seul processus devrait être lancé. Relance en cours..."
    ssh "$PI_USER@$PI_HOST" "pkill -f 'python3 .*spot\.py' && cd $PI_PATH && source venv/bin/activate && nohup python3 spot.py > spot.log 2>&1 &" || true
    sleep 10
    process_count=$(ssh "$PI_USER@$PI_HOST" "pgrep -f 'python3 .*spot\.py' | wc -l")
    if [ "$process_count" -eq 1 ]; then
        echo "Nouveau processus relancé avec succès."
    else
        echo "Échec du relancement du processus unique."
        exit 1
    fi
else
    echo "Échec du lancement du nouveau processus."
    exit 1
fi
