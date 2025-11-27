# 🔧 Guide de dépannage - GitHub Pages

## Votre situation actuelle

**Username**: `tittank1802`  
**Repository**: `test`  
**Status**: Push réussi ✅, mais GitHub Pages pas accessible

---

## ✅ Étapes pour activer GitHub Pages

### Méthode 1: Via l'interface web (Recommandé)

1. **Allez sur votre repository**:
   ```
   https://github.com/tittank1802/test
   ```

2. **Cliquez sur "Settings"** (en haut à droite du repository)

3. **Dans le menu de gauche**, cherchez et cliquez sur **"Pages"**

4. **Sous "Source"**:
   - Branch: Sélectionnez **`main`** (ou `master`)
   - Folder: Sélectionnez **`/ (root)`**
   
5. **Cliquez sur "Save"**

6. **Attendez 2-5 minutes**

7. **Rafraîchissez la page** - Vous verrez:
   ```
   Your site is published at https://tittank1802.github.io/test/
   ```

### Méthode 2: Via GitHub CLI

```bash
# Si vous avez GitHub CLI installé
gh api repos/tittank1802/test/pages \
  -X POST \
  -f source[branch]=main \
  -f source[path]=/
```

---

## ⚠️ Problèmes courants et solutions

### 1. Repository privé
**Symptôme**: GitHub Pages n'apparaît pas dans Settings  
**Solution**: 
- Le repository doit être **Public** pour GitHub Pages (compte gratuit)
- Allez dans Settings → "Change repository visibility" → "Make public"

### 2. "Pages" n'apparaît pas dans le menu
**Symptôme**: Pas d'option "Pages" dans Settings  
**Cause**: Repository privé sur compte gratuit  
**Solutions**:
- Rendre le repository public, OU
- Passer à GitHub Pro (payant), OU
- Utiliser une alternative (voir ci-dessous)

### 3. Erreur 404 sur le site
**Symptôme**: Le lien donne "404 Not Found"  
**Solutions**:
- Attendez 5-10 minutes (premier déploiement)
- Vérifiez que `index.html` existe à la racine
- Vérifiez l'URL (doit être en minuscules)
- Consultez l'onglet "Actions" pour voir les erreurs

### 4. Site vide ou cassé
**Symptôme**: La page charge mais rien ne s'affiche  
**Solutions**:
- Ouvrez la console du navigateur (F12)
- Vérifiez les erreurs JavaScript
- Assurez-vous que `mesh_interactive_2d.html` et `mesh_interactive_3d.html` existent

---

## 🔍 Vérifications à faire

### Vérification 1: Repository public ?
```bash
# Allez sur: https://github.com/tittank1802/test
# En haut à gauche, voyez-vous "Public" ou "Private" ?
```

### Vérification 2: Fichiers présents ?
```bash
cd /root/test
git add mesh_interactive_2d.html mesh_interactive_3d.html
git commit -m "Add mesh visualizations"
git push
```

### Vérification 3: GitHub Actions
1. Allez sur: `https://github.com/tittank1802/test/actions`
2. Vérifiez s'il y a des erreurs

---

## 🎯 Solutions alternatives (si GitHub Pages ne fonctionne pas)

### Alternative 1: GitHub Gist + htmlpreview.github.io

**Avantages**: Gratuit, fonctionne avec repository privé, ultra rapide

#### Étape par étape:
1. **Créer un Gist**:
   - Allez sur https://gist.github.com/
   - Collez le contenu de `index.html`
   - Nom: `index.html`
   - Créez "Public gist"

2. **Cliquez sur "Raw"** pour obtenir l'URL brute

3. **Utilisez htmlpreview.github.io**:
   ```
   https://htmlpreview.github.io/?https://gist.githubusercontent.com/tittank1802/GIST-ID/raw/index.html
   ```

4. **Répétez pour les autres fichiers**

### Alternative 2: raw.githack.com

**Avantages**: Plus rapide que htmlpreview, fonctionne avec repos privés (si lien partagé)

```
https://raw.githack.com/tittank1802/test/main/index.html
https://raw.githack.com/tittank1802/test/main/mesh_interactive_2d.html
https://raw.githack.com/tittank1802/test/main/mesh_interactive_3d.html
```

### Alternative 3: Netlify Drop

**Avantages**: Très simple, glisser-déposer

1. Allez sur https://app.netlify.com/drop
2. Glissez-déposez votre dossier `/root/test`
3. Netlify génère une URL instantanément
4. **Gratuit et sans compte nécessaire !**

### Alternative 4: Vercel

**Avantages**: Intégration Git, domaine gratuit

```bash
# Installer Vercel CLI
npm install -g vercel

# Déployer
cd /root/test
vercel

# Suivre les instructions
```

### Alternative 5: Hébergement local partagé

Si vous voulez juste partager rapidement:

```bash
# Déjà en cours d'exécution !
python visualize_http_server.py
# Accessible sur: http://localhost:8000/viewer.html
```

Puis utilisez **ngrok** pour partager:
```bash
# Installer ngrok
snap install ngrok

# Partager
ngrok http 8000

# Vous obtenez une URL publique comme:
# https://abc123.ngrok.io
```

---

## 📋 Checklist de dépannage

Cochez ce que vous avez essayé:

- [ ] Repository est public ?
- [ ] Settings → Pages accessible ?
- [ ] Source configurée à `main` branch et `/` folder ?
- [ ] Attendu 5-10 minutes ?
- [ ] Fichiers HTML poussés sur GitHub ?
- [ ] Vérifié l'onglet Actions pour erreurs ?
- [ ] Testé les URLs alternatives ci-dessus ?

---

## 🆘 Commandes de diagnostic

### Vérifier le status du repository
```bash
cd /root/test
git status
git remote -v
```

### Pousser les fichiers HTML manquants
```bash
cd /root/test
git add mesh_interactive_2d.html mesh_interactive_3d.html
git add mesh_2d_*.png mesh_3d_*.png  # Images optionnelles
git commit -m "Add visualization files"
git push
```

### Vérifier la taille des fichiers
```bash
ls -lh *.html
# Si > 100 MB, GitHub rejettera
```

---

## 💡 Prochaines étapes recommandées

1. **Essayez d'abord**: Rendre le repository public si privé
2. **Si ça ne marche pas**: Utilisez raw.githack.com (le plus simple)
3. **Pour du long terme**: Netlify ou Vercel
4. **Pour partager rapidement**: ngrok + serveur local

---

## 📞 Besoin d'aide supplémentaire ?

**Dites-moi**:
1. Le repository est-il public ou privé ?
2. Voyez-vous l'option "Pages" dans Settings ?
3. Y a-t-il des erreurs dans l'onglet Actions ?

Je pourrai vous guider plus précisément !
