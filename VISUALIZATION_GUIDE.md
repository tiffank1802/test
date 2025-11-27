# Guide des Méthodes de Visualisation dans Docker

## 🎯 Résumé des Options

### **Méthode 1: WebAgg (Recommandé pour matplotlib)**
```bash
python visualize_interactive_webagg.py
```
- ✅ Fonctionne dans Docker sans configuration X11
- ✅ Interface web simple
- ✅ Accès via http://localhost:8988
- ⚠️  Nécessite de mapper le port si Docker

**Configuration Docker:**
```bash
docker run -p 8988:8988 your_image python visualize_interactive_webagg.py
```

---

### **Méthode 2: Jupyter Lab (Meilleur pour développement)**
```bash
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```
- ✅ Interface complète pour développement
- ✅ Supporte widgets interactifs
- ✅ Peut sauvegarder et partager notebooks

**Configuration Docker:**
```bash
docker run -p 8888:8888 your_image
```

**Installation:**
```bash
pip install jupyterlab ipympl
```

---

### **Méthode 3: Serveur HTTP Simple (Le plus simple)**
```bash
python visualize_http_server.py
```
- ✅ Très simple, pas de dépendances supplémentaires
- ✅ Page HTML customisée
- ✅ Accès via http://localhost:8000/viewer.html
- ⚠️  Images statiques (pas interactif comme WebAgg)

**Configuration Docker:**
```bash
docker run -p 8000:8000 your_image python visualize_http_server.py
```

---

### **Méthode 4: Plotly (Meilleur pour interactivité)**
```bash
python visualize_plotly.py
```
- ✅ Très interactif (zoom, pan, rotate)
- ✅ Fichiers HTML autonomes
- ✅ Pas besoin de serveur actif
- ✅ Info au survol
- ⚠️  Fichiers HTML plus lourds

**Installation:**
```bash
pip install plotly
```

Ouvrez simplement les fichiers HTML générés dans votre navigateur!

---

## 🐳 Configuration Docker Complète

### Dockerfile exemple
```dockerfile
FROM dolfinx/dolfinx:stable

# Installer les outils de visualisation
RUN pip install plotly jupyterlab ipympl

# Exposer les ports nécessaires
EXPOSE 8000 8888 8988

WORKDIR /root/test
```

### docker-compose.yml exemple
```yaml
version: '3'
services:
  fenics:
    build: .
    ports:
      - "8000:8000"   # Serveur HTTP
      - "8888:8888"   # Jupyter
      - "8988:8988"   # WebAgg
    volumes:
      - ./:/root/test
    command: bash
```

---

## 📋 Comparaison Rapide

| Méthode | Interactivité | Setup | Performance | Use Case |
|---------|--------------|-------|-------------|----------|
| WebAgg | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Viz rapide |
| Jupyter | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Développement |
| HTTP | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Partage simple |
| Plotly | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Présentation |

---

## 🚀 Commandes Rapides

```bash
# Test WebAgg
python visualize_interactive_webagg.py

# Test Plotly (plus simple)
python visualize_plotly.py
# Puis ouvrez mesh_interactive_2d.html dans votre navigateur

# Serveur HTTP
python visualize_http_server.py
# Ouvrez http://localhost:8000/viewer.html

# Jupyter
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root
```

---

## ⚡ Recommandation

**Pour Docker, je recommande dans cet ordre:**

1. **Plotly** - Le plus simple, fichiers HTML autonomes
2. **Serveur HTTP** - Bon compromis simplicité/fonctionnalité  
3. **Jupyter Lab** - Si vous développez beaucoup
4. **WebAgg** - Alternative légère à Jupyter
