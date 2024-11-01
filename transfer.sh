# Variables
source .env

# Synchronisation des fichiers
echo "Synchronisation des fichiers..."
rsync -avz --exclude='.git' --exclude='venv' $LOCAL_PATH $PI_USER@$PI_HOST:$PI_PATH