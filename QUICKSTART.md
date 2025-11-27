# 🚀 Guide de Démarrage Rapide

## Déployer vos visualisations en 5 minutes !

### Étape 1: Préparer vos fichiers ✅

Vos fichiers sont déjà prêts dans `/root/test/`:
- ✅ `index.html` - Page d'accueil
- ✅ `mesh_interactive_2d.html` - Visualisation 2D
- ✅ `mesh_interactive_3d.html` - Visualisation 3D
- ✅ `README.md` - Documentation
- ✅ `.gitignore` - Fichiers à ignorer
- ✅ `deploy.sh` - Script de déploiement

---

### Étape 2: Créer un repository GitHub

#### Option A: Interface web (recommandé pour débutants)
1. Allez sur https://github.com/new
2. Nom du repository: `fenics-visualizations` (ou autre nom)
3. Description: "Interactive FEniCS mesh visualizations"
4. Public ✅
5. **NE PAS** cocher "Initialize with README"
6. Cliquez sur "Create repository"

#### Option B: GitHub CLI (pour utilisateurs avancés)
```bash
gh repo create fenics-visualizations --public --description "Interactive FEniCS mesh visualizations"
```

---

### Étape 3: Déployer avec le script automatique 🎯

```bash
cd /root/test
./deploy.sh
```

Le script va vous demander:
- Votre nom d'utilisateur GitHub
- Le nom du repository

Puis il va automatiquement:
1. ✅ Initialiser Git
2. ✅ Créer le .gitignore
3. ✅ Mettre à jour les URLs dans README et index.html
4. ✅ Faire le commit
5. ✅ Pousser vers GitHub

---

### Étape 4: Activer GitHub Pages

#### Via l'interface web:
1. Allez sur votre repository: `https://github.com/VOTRE-USERNAME/VOTRE-REPO`
2. Cliquez sur **Settings** (en haut à droite)
3. Dans le menu de gauche, cliquez sur **Pages**
4. Sous "Source":
   - Branch: Sélectionnez `main`
   - Folder: Sélectionnez `/ (root)`
5. Cliquez sur **Save**
6. ✅ Un message apparaîtra: "Your site is ready to be published at..."

#### Via GitHub CLI:
```bash
gh api repos/VOTRE-USERNAME/VOTRE-REPO/pages \
  -X POST \
  -f source[branch]=main \
  -f source[path]=/
```

---

### Étape 5: Accéder à votre site 🎉

Après 2-5 minutes, votre site sera en ligne à:
```
https://VOTRE-USERNAME.github.io/VOTRE-REPO/
```

**URLs directes:**
- 🏠 Accueil: `https://VOTRE-USERNAME.github.io/VOTRE-REPO/`
- 📐 Maillage 2D: `https://VOTRE-USERNAME.github.io/VOTRE-REPO/mesh_interactive_2d.html`
- 🎲 Maillage 3D: `https://VOTRE-USERNAME.github.io/VOTRE-REPO/mesh_interactive_3d.html`

---

## 🔧 Déploiement manuel (alternative)

Si le script automatique ne fonctionne pas:

```bash
cd /root/test

# 1. Initialiser Git
git init
git branch -M main

# 2. Configurer le remote (remplacer USERNAME et REPO)
git remote add origin https://github.com/USERNAME/REPO.git

# 3. Ajouter les fichiers
git add index.html mesh_interactive_*.html README.md .gitignore LICENSE

# 4. Commit
git commit -m "Initial commit - FEniCS visualizations"

# 5. Push
git push -u origin main
```

Puis activez GitHub Pages comme à l'Étape 4.

---

## 📝 Mises à jour futures

Pour mettre à jour votre site après modifications:

```bash
cd /root/test

# Regénérer les visualisations si nécessaire
python visualize_plotly.py

# Déployer les changements
git add .
git commit -m "Update visualizations"
git push

# Les changements apparaîtront sur votre site dans quelques minutes
```

Ou utilisez simplement:
```bash
./deploy.sh
```

---

## ⚠️ Problèmes courants

### "Permission denied" lors du push
**Solution**: Configurez l'authentification GitHub

#### Avec token (recommandé):
```bash
# Créez un Personal Access Token sur GitHub.com:
# Settings → Developer settings → Personal access tokens → Generate new token
# Permissions: repo (toutes les cases)

# Puis configurez:
git remote set-url origin https://VOTRE-TOKEN@github.com/USERNAME/REPO.git
```

#### Avec SSH:
```bash
# Générer une clé SSH
ssh-keygen -t ed25519 -C "votre.email@example.com"

# Ajouter la clé à GitHub:
# Settings → SSH and GPG keys → New SSH key

# Changer l'URL remote
git remote set-url origin git@github.com:USERNAME/REPO.git
```

### Le site n'apparaît pas
1. Vérifiez que GitHub Pages est activé (Settings → Pages)
2. Attendez 5-10 minutes (premier déploiement)
3. Vérifiez l'URL (doit être en minuscules)
4. Consultez l'onglet "Actions" pour voir si le déploiement a réussi

### Fichiers trop volumineux
Si `mesh_interactive_3d.html` est > 100MB:
```python
# Dans visualize_plotly.py, réduire le nombre d'éléments:
domain = mesh.create_box(
    MPI.COMM_WORLD,
    [np.array([0, 0, 0]), np.array([1, 1, 1])],
    [3, 3, 3],  # Au lieu de [5, 5, 5]
    mesh.CellType.tetrahedron
)
```

---

## 🎯 Checklist de déploiement

- [ ] Repository créé sur GitHub
- [ ] Authentification Git configurée (token ou SSH)
- [ ] Script `deploy.sh` exécuté avec succès
- [ ] Push réussi vers GitHub
- [ ] GitHub Pages activé (Settings → Pages)
- [ ] Site accessible (attendez 5 minutes)
- [ ] URLs testées et fonctionnelles
- [ ] README mis à jour avec les vrais URLs
- [ ] Étoile ⭐ ajoutée au repository FEniCS !

---

## 📞 Besoin d'aide ?

- 📖 [Guide complet de déploiement](GUIDE_DEPLOYMENT_GITHUB.md)
- 🌐 [Documentation GitHub Pages](https://docs.github.com/en/pages)
- 💬 [Forum FEniCS](https://fenicsproject.discourse.group/)
- 🐛 [Issues GitHub](https://github.com/USERNAME/REPO/issues)

---

<p align="center">
  <strong>Bon déploiement ! 🚀</strong>
</p>
