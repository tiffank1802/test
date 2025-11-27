#!/bin/bash

# Script de déploiement automatique sur GitHub
# Usage: ./deploy.sh

set -e  # Arrêter en cas d'erreur

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
echo -e "${BLUE}🚀 Script de déploiement GitHub${NC}"
echo ""

# Demander les informations si elles ne sont pas définies
if [ -z "$GITHUB_USERNAME" ]; then
    read -p "Entrez votre nom d'utilisateur GitHub: " GITHUB_USERNAME
fi

if [ -z "$REPO_NAME" ]; then
    read -p "Entrez le nom du repository: " REPO_NAME
fi

# Vérifier si git est installé
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git n'est pas installé. Veuillez l'installer d'abord.${NC}"
    exit 1
fi

# Initialiser git si nécessaire
if [ ! -d .git ]; then
    echo -e "${YELLOW}📦 Initialisation du repository Git...${NC}"
    git init
    git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git
    echo -e "${GREEN}✓ Repository initialisé${NC}"
else
    echo -e "${GREEN}✓ Repository Git déjà initialisé${NC}"
fi

# Créer .gitignore si nécessaire
if [ ! -f .gitignore ]; then
    echo -e "${YELLOW}📝 Création du .gitignore...${NC}"
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter
.ipynb_checkpoints
*.ipynb

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Fichiers temporaires
*.tmp
*.bak
*.log

# Ne pas inclure les gros fichiers MSH
*.msh
*.mesh

# Ne pas inclure les résultats volumineux
out_*/
results/
EOF
    echo -e "${GREEN}✓ .gitignore créé${NC}"
fi

# Mettre à jour le README avec les vrais URLs
if [ -f README.md ]; then
    echo -e "${YELLOW}📝 Mise à jour du README avec vos informations...${NC}"
    sed -i.bak "s/USERNAME/$GITHUB_USERNAME/g" README.md
    sed -i.bak "s/REPO/$REPO_NAME/g" README.md
    rm -f README.md.bak
    echo -e "${GREEN}✓ README mis à jour${NC}"
fi

# Mettre à jour index.html
if [ -f index.html ]; then
    echo -e "${YELLOW}📝 Mise à jour de index.html...${NC}"
    sed -i.bak "s|https://github.com\"|https://github.com/$GITHUB_USERNAME/$REPO_NAME\"|g" index.html
    rm -f index.html.bak
    echo -e "${GREEN}✓ index.html mis à jour${NC}"
fi

# Ajouter les fichiers
echo ""
echo -e "${YELLOW}📋 Fichiers à committer:${NC}"
git add -A
git status --short

# Demander confirmation
echo ""
read -p "Voulez-vous continuer avec le commit et le push? (o/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Oo]$ ]]; then
    echo -e "${YELLOW}⚠️  Déploiement annulé${NC}"
    exit 0
fi

# Commit
COMMIT_MSG="Update visualizations - $(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo -e "${YELLOW}📝 Création du commit: ${COMMIT_MSG}${NC}"
git commit -m "$COMMIT_MSG" || echo -e "${YELLOW}⚠️  Rien à committer${NC}"

# Vérifier la branche
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" != "main" ]; then
    echo -e "${YELLOW}📌 Changement vers la branche main...${NC}"
    git branch -M main
fi

# Push
echo ""
echo -e "${YELLOW}⬆️  Push vers GitHub...${NC}"
if git push -u origin main; then
    echo -e "${GREEN}✅ Push réussi!${NC}"
else
    echo -e "${RED}❌ Erreur lors du push.${NC}"
    echo -e "${YELLOW}💡 Si c'est votre premier push, assurez-vous d'avoir:${NC}"
    echo "   1. Créé le repository sur GitHub.com"
    echo "   2. Configuré votre authentification Git (token ou SSH)"
    echo ""
    echo "Pour configurer un token:"
    echo "   git remote set-url origin https://TOKEN@github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    exit 1
fi

# Informations finales
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Déploiement terminé avec succès!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}📱 Prochaines étapes:${NC}"
echo ""
echo "1. Activer GitHub Pages:"
echo "   → Allez sur: https://github.com/$GITHUB_USERNAME/$REPO_NAME/settings/pages"
echo "   → Source: Sélectionnez 'main' branch et '/ (root)'"
echo "   → Cliquez sur 'Save'"
echo ""
echo "2. Votre site sera disponible dans quelques minutes à:"
echo -e "   ${GREEN}https://$GITHUB_USERNAME.github.io/$REPO_NAME/${NC}"
echo ""
echo "3. URLs directes:"
echo "   • Page d'accueil: https://$GITHUB_USERNAME.github.io/$REPO_NAME/"
echo "   • Maillage 2D: https://$GITHUB_USERNAME.github.io/$REPO_NAME/mesh_interactive_2d.html"
echo "   • Maillage 3D: https://$GITHUB_USERNAME.github.io/$REPO_NAME/mesh_interactive_3d.html"
echo ""
echo -e "${YELLOW}💡 Astuce: Ajoutez une étoile ⭐ à votre repository pour le rendre plus visible!${NC}"
echo ""
