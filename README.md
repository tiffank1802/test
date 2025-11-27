# 🔬 Visualisations de Maillages FEniCS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

Visualisations interactives de maillages générés avec **DOLFINx/FEniCS** et **Plotly**.

## 🌐 Démos en ligne

> 🚀 **Remplacez `tittank1802` et `test` par vos vrais noms GitHub après déploiement**

- 🏠 [Page d'accueil](https://tittank1802.github.io/test/)
- 📐 [Maillage 2D interactif](https://tittank1802.github.io/test/mesh_interactive_2d.html)
- 🎲 [Maillage 3D interactif](https://tittank1802.github.io/test/mesh_interactive_3d.html)

![Preview](images/preview.png)

## ✨ Fonctionnalités

- ✅ **Visualisations interactives** - Zoom, pan, rotation 3D
- ✅ **Informations au survol** - Coordonnées des nœuds affichées
- ✅ **Export d'images** - Haute résolution depuis le navigateur
- ✅ **Aucune installation** - Fonctionne directement dans le navigateur
- ✅ **Responsive** - S'adapte à tous les écrans

## 🎯 Exemples

### Maillage 2D - Triangulaire
- 20×10 éléments
- 400 triangles
- Exploration interactive

### Maillage 3D - Tétraédrique
- Boîte unitaire
- Éléments tétraédriques
- Rotation 360° complète

## 🛠️ Technologies utilisées

- **[DOLFINx](https://fenicsproject.org/)** - Bibliothèque de calcul par éléments finis
- **[Plotly](https://plotly.com/python/)** - Graphiques interactifs
- **Python 3.12+**
- **NumPy** - Calculs numériques

## 📦 Installation locale

### Prérequis
```bash
# Option 1: Avec Docker (recommandé)
docker pull dolfinx/dolfinx:stable

# Option 2: Installation manuelle
# Suivre: https://github.com/FEniCS/dolfinx#installation
```

### Installation des dépendances
```bash
pip install fenics-dolfinx plotly numpy matplotlib
```

### Génération des visualisations
```bash
# Cloner le repository
git clone https://github.com/tittank1802/test.git
cd test

# Générer les fichiers HTML
python visualize_plotly.py

# Les fichiers mesh_interactive_2d.html et mesh_interactive_3d.html sont créés
# Ouvrez-les dans votre navigateur
```

## 📁 Structure du projet

```
fenics-visualizations/
├── index.html                      # Page d'accueil
├── mesh_interactive_2d.html        # Visualisation 2D
├── mesh_interactive_3d.html        # Visualisation 3D
├── visualize_plotly.py             # Script de génération
├── mesh_examples_pratiques.py      # Exemples pédagogiques
├── README.md                       # Ce fichier
├── GUIDE_DEPLOYMENT_GITHUB.md      # Guide de déploiement
├── COURS_MAILLAGE_FENICS.md        # Cours théorique
└── images/                         # Captures d'écran
    ├── preview.png
    ├── mesh_2d_detailed.png
    └── mesh_3d_quality.png
```

## 🚀 Déploiement sur GitHub Pages

### Méthode rapide

```bash
# 1. Créer un nouveau repository sur GitHub.com

# 2. Dans votre terminal
git init
git add .
git commit -m "Initial commit - FEniCS visualizations"
git branch -M main
git remote add origin https://github.com/tittank1802/test.git
git push -u origin main

# 3. Activer GitHub Pages
# Allez sur: Settings → Pages → Source: main branch
```

### Script automatique

Utilisez le script fourni :
```bash
chmod +x deploy.sh
./deploy.sh
```

Voir le [Guide de déploiement complet](GUIDE_DEPLOYMENT_GITHUB.md) pour plus de détails.

## 📚 Documentation

- **[Guide de déploiement](GUIDE_DEPLOYMENT_GITHUB.md)** - Comment publier sur GitHub
- **[Cours sur les maillages](COURS_MAILLAGE_FENICS.md)** - Théorie et algorithmes
- **[Guide de visualisation](VISUALIZATION_GUIDE.md)** - Options de visualisation dans Docker

## 🎓 Apprendre plus

### Tutoriels FEniCS
- [Documentation officielle FEniCSx](https://docs.fenicsproject.org)
- [The FEniCS Book](https://fenicsproject.org/book/)
- [DOLFINx Tutorial](https://jsdokken.com/dolfinx-tutorial/)

### Génération de maillages
- [Documentation Gmsh](https://gmsh.info/)
- [Cours complet sur les maillages](COURS_MAILLAGE_FENICS.md) (inclus dans ce repo)

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Idées de contributions
- [ ] Ajouter d'autres types de maillages (hexaèdres, prismes)
- [ ] Implémenter le raffinement adaptatif
- [ ] Ajouter des analyses de qualité
- [ ] Créer des animations de déformation
- [ ] Visualiser des solutions EDP

## 📝 License

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👤 Auteur

**Votre Nom**

- GitHub: [@tittank1802](https://github.com/tittank1802)
- Email: votre.email@example.com

## 🙏 Remerciements

- [FEniCS Project](https://fenicsproject.org/) - Pour la bibliothèque exceptionnelle
- [Plotly](https://plotly.com/) - Pour les visualisations interactives
- La communauté FEniCS pour le support et les exemples

## 📊 Statistiques

![GitHub stars](https://img.shields.io/github/stars/tittank1802/test?style=social)
![GitHub forks](https://img.shields.io/github/forks/tittank1802/test?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/tittank1802/test?style=social)

---

<p align="center">
  Fait avec ❤️ pour la communauté FEniCS
</p>
