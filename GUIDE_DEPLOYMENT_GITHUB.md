# 🚀 Guide: Déployer des fichiers HTML interactifs sur GitHub

## Méthode 1: GitHub Pages (Recommandée) ⭐

GitHub Pages permet d'héberger gratuitement des sites web statiques directement depuis un repository GitHub.

### Étape par étape:

#### 1. Créer un repository GitHub
```bash
# Sur GitHub.com, créez un nouveau repository
# Nom: fenics-visualizations (ou autre)
# Public ou Private (Pages fonctionne avec les deux pour les comptes gratuits)
```

#### 2. Initialiser et pousser votre projet
```bash
cd /root/test

# Initialiser git (si pas déjà fait)
git init

# Créer un fichier .gitignore
cat > .gitignore << EOF
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
EOF

# Ajouter vos fichiers
git add mesh_interactive_3d.html
git add mesh_interactive_2d.html
# Ajouter d'autres fichiers si nécessaire

# Commit
git commit -m "Add interactive mesh visualizations"

# Ajouter le remote (remplacer USERNAME et REPO)
git remote add origin https://github.com/USERNAME/REPO.git

# Pousser
git branch -M main
git push -u origin main
```

#### 3. Activer GitHub Pages

**Option A: Via l'interface GitHub**
1. Allez sur votre repository → **Settings**
2. Dans le menu de gauche → **Pages**
3. Source: Sélectionnez `main` branch et `/ (root)`
4. Cliquez sur **Save**

**Option B: Via GitHub CLI**
```bash
# Installer GitHub CLI si nécessaire
# https://cli.github.com/

gh repo create fenics-visualizations --public
cd /root/test
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/USERNAME/fenics-visualizations.git
git push -u origin main

# Activer Pages
gh api repos/USERNAME/fenics-visualizations/pages -X POST -f source[branch]=main -f source[path]=/
```

#### 4. Accéder à votre site
Après quelques minutes, votre site sera disponible à:
```
https://USERNAME.github.io/REPO/mesh_interactive_3d.html
```

### Structure recommandée du repository:

```
fenics-visualizations/
├── index.html              # Page d'accueil (liste des visualisations)
├── mesh_interactive_2d.html
├── mesh_interactive_3d.html
├── README.md               # Documentation
└── images/                 # Captures d'écran pour le README
    ├── preview_2d.png
    └── preview_3d.png
```

---

## Méthode 2: GitHub Gist (Partage rapide) ⚡

Pour partager rapidement UN fichier sans créer un repository complet.

### Via l'interface web:
1. Allez sur https://gist.github.com/
2. Collez le contenu de votre HTML
3. Nommez le fichier: `mesh_interactive_3d.html`
4. Cliquez sur **Create public gist**

### Via ligne de commande:
```bash
# Installer gist CLI
sudo apt-get install gist  # ou: brew install gist

# Créer le gist
gist -p mesh_interactive_3d.html

# Retourne une URL comme: https://gist.github.com/USERNAME/abc123...
```

### Visualiser le Gist:
```
# URL brute du fichier:
https://gist.githubusercontent.com/USERNAME/GIST_ID/raw/mesh_interactive_3d.html

# Pour visualiser dans le navigateur (via service externe):
https://htmlpreview.github.io/?https://gist.githubusercontent.com/USERNAME/GIST_ID/raw/mesh_interactive_3d.html
```

---

## Méthode 3: Repository GitHub + Preview service

Si vous ne voulez pas activer GitHub Pages, utilisez un service de preview.

### 1. Pousser sur GitHub (comme Méthode 1, étapes 1-2)

### 2. Utiliser un service de preview:

#### **Option A: htmlpreview.github.io**
```
https://htmlpreview.github.io/?https://github.com/USERNAME/REPO/blob/main/mesh_interactive_3d.html
```

#### **Option B: raw.githack.com**
```
# Pour développement (mises à jour instantanées):
https://raw.githack.com/USERNAME/REPO/main/mesh_interactive_3d.html

# Pour production (CDN avec cache):
https://rawcdn.githack.com/USERNAME/REPO/COMMIT_HASH/mesh_interactive_3d.html
```

#### **Option C: GitHub.dev (VSCode en ligne)**
```
https://github.dev/USERNAME/REPO
# Puis ouvrir le fichier HTML et utiliser l'extension "Live Preview"
```

---

## Méthode 4: Solution complète avec page d'accueil

### Créer une belle page d'accueil (index.html):

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualisations de Maillages FEniCS</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        h1 {
            text-align: center;
            font-size: 3em;
            margin-bottom: 10px;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2em;
            opacity: 0.9;
            margin-bottom: 40px;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-top: 40px;
        }
        .card {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        .card:hover {
            transform: translateY(-10px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
        }
        .card h2 {
            margin-top: 0;
            font-size: 1.8em;
        }
        .card p {
            opacity: 0.9;
            line-height: 1.6;
        }
        .btn {
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 12px 30px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            margin-top: 15px;
            transition: background 0.3s, color 0.3s;
        }
        .btn:hover {
            background: #667eea;
            color: white;
        }
        .icon {
            font-size: 3em;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔬 Visualisations FEniCS</h1>
        <p class="subtitle">Maillages interactifs créés avec la méthode des éléments finis</p>
        
        <div class="grid">
            <div class="card" onclick="window.location.href='mesh_interactive_2d.html'">
                <div class="icon">📐</div>
                <h2>Maillage 2D</h2>
                <p>Visualisation interactive d'un maillage 2D triangulaire. Zoomez et explorez la structure du maillage.</p>
                <a href="mesh_interactive_2d.html" class="btn">Voir la démo 2D →</a>
            </div>
            
            <div class="card" onclick="window.location.href='mesh_interactive_3d.html'">
                <div class="icon">🎲</div>
                <h2>Maillage 3D</h2>
                <p>Visualisation 3D interactive avec rotation complète. Explorez le maillage tétraédrique de tous les angles.</p>
                <a href="mesh_interactive_3d.html" class="btn">Voir la démo 3D →</a>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 50px; opacity: 0.8;">
            <p>Créé avec DOLFINx et Plotly</p>
            <p>
                <a href="https://github.com/USERNAME/REPO" style="color: white;">
                    📦 Voir le code source sur GitHub
                </a>
            </p>
        </div>
    </div>
</body>
</html>
```

---

## Comparaison des méthodes:

| Méthode | Simplicité | Vitesse | URL propre | Recommandé pour |
|---------|-----------|---------|------------|-----------------|
| **GitHub Pages** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ✅ | Projets sérieux |
| **GitHub Gist** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ❌ | Partage rapide |
| **htmlpreview.github.io** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ❌ | Tests rapides |
| **raw.githack.com** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ | Alternative à Pages |

---

## Script automatique pour déploiement

Créez ce script `deploy.sh`:

```bash
#!/bin/bash

echo "🚀 Déploiement sur GitHub..."

# Configuration (à modifier)
USERNAME="votre-username"
REPO="fenics-visualizations"

# Initialiser si nécessaire
if [ ! -d .git ]; then
    git init
    git remote add origin https://github.com/$USERNAME/$REPO.git
fi

# Ajouter les fichiers
git add mesh_interactive_*.html
git add index.html
git add README.md
git add images/*.png 2>/dev/null || true

# Commit
echo "📝 Création du commit..."
git commit -m "Update visualizations - $(date +%Y-%m-%d)"

# Push
echo "⬆️  Push vers GitHub..."
git push origin main

# Afficher l'URL
echo ""
echo "✅ Déploiement terminé!"
echo "📱 Votre site sera disponible dans quelques minutes à:"
echo "   https://$USERNAME.github.io/$REPO/"
```

---

## README.md suggéré:

```markdown
# 🔬 Visualisations de Maillages FEniCS

Visualisations interactives de maillages générés avec DOLFINx/FEniCS.

## 🌐 Démos en ligne

- [Maillage 2D interactif](https://USERNAME.github.io/REPO/mesh_interactive_2d.html)
- [Maillage 3D interactif](https://USERNAME.github.io/REPO/mesh_interactive_3d.html)

## ✨ Fonctionnalités

- ✅ Visualisations interactives (zoom, pan, rotation)
- ✅ Informations au survol de la souris
- ✅ Export d'images haute résolution
- ✅ Aucune installation requise

## 🛠️ Technologies utilisées

- [DOLFINx](https://fenicsproject.org/) - Génération de maillages
- [Plotly](https://plotly.com/) - Visualisations interactives
- Python 3.12+

## 📦 Installation locale

```bash
pip install fenics-dolfinx plotly
python visualize_plotly.py
```

## 📝 License

MIT
```

---

## Conseils importants:

1. **Taille des fichiers**: GitHub Pages a une limite de 100 MB par fichier
   - Si votre HTML est trop gros, réduisez le nombre de points du maillage
   
2. **Sécurité**: Ne commitez JAMAIS de tokens ou mots de passe
   - Utilisez `.gitignore` pour les fichiers sensibles

3. **Performance**: 
   - Les fichiers HTML Plotly peuvent être lourds (plusieurs MB)
   - Pour de gros maillages, considérez un hébergement dédié

4. **Mise à jour**:
   ```bash
   git add .
   git commit -m "Update meshes"
   git push
   # GitHub Pages se met à jour automatiquement en quelques minutes
   ```

---

## 🎯 Résumé rapide

**Pour partager rapidement** → GitHub Gist + htmlpreview.github.io  
**Pour un projet sérieux** → GitHub Pages avec index.html  
**Pour un portfolio** → GitHub Pages + domaine personnalisé
