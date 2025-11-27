# 📚 Cours: Génération de Maillages dans FEniCS/DOLFINx

## 1. Introduction: Qu'est-ce qu'un maillage?

### Définition

Un **maillage** (mesh) est une discrétisation d'un domaine géométrique en éléments simples (triangles, quadrilatères, tétraèdres, hexaèdres, etc.) pour résoudre numériquement des équations aux dérivées partielles (EDP) par la méthode des éléments finis.

### Vocabulaire de base

- **Sommet (vertex)**: Point du maillage
- **Arête (edge)**: Ligne connectant deux sommets
- **Face**: Surface délimitée par des arêtes (2D ou faces de polyèdres 3D)
- **Cellule (cell)**: Élément du maillage (triangle en 2D, tétraèdre en 3D)
- **Topologie**: Structure de connectivité entre les entités
- **Géométrie**: Positions spatiales des sommets

---

## 2. Types d'éléments dans FEniCS

### En 2D

```
Triangle                    Quadrilatère
    2                          3--------2
   /|\                         |        |
  / | \                        |        |
 /  |  \                       |        |
0---+---1                      0--------1
```

### En 3D

```
Tétraèdre (4 faces)         Hexaèdre (cube)
       3                         7--------6
      /|\                       /|       /|
     / | \                     / |      / |
    /  |  \                   4--------5  |
   0---+---2                  |  3-----|--2
    \  |  /                   | /      | /
     \ | /                    |/       |/
      \|/                     0--------1
       1
```

---

## 3. Structure de données d'un maillage FEniCS

### Hiérarchie topologique

```
Dimension 0: Sommets (vertices)
Dimension 1: Arêtes (edges)
Dimension 2: Faces (2D) ou Cellules (en 2D)
Dimension 3: Cellules (en 3D)
```

### Exemple concret en 2D

```python
# Un triangle simple
Sommets: [(0,0), (1,0), (0,1)]
Arêtes:  [[0,1], [1,2], [2,0]]
Cellule: [[0,1,2]]
```

---

## 4. Méthodes de création de maillage

### 4.1 Maillages intégrés (built-in)

FEniCS peut générer automatiquement des maillages pour des géométries simples.

#### Algorithme de subdivision (2D)

Pour `create_rectangle([0,0], [1,1], [nx, ny])`:

```
Étape 1: Créer une grille régulière
    Points: (i*dx, j*dy) pour i=0..nx, j=0..ny
    où dx = 1/nx, dy = 1/ny

Étape 2: Subdiviser chaque rectangle en 2 triangles
    Rectangle [i,j]:
        Sommets: P1=(i*dx, j*dy), P2=((i+1)*dx, j*dy),
                 P3=((i+1)*dx, (j+1)*dy), P4=(i*dx, (j+1)*dy)

        Triangle 1: [P1, P2, P4]
        Triangle 2: [P2, P3, P4]

Étape 3: Construire la connectivité
    - Indexer les sommets de manière unique
    - Créer la table de connectivité cellule->sommets
```

#### Exemple visuel

```
nx=2, ny=2 donne:

4---5---6
|\2 |\4 |
| \ | \ |
|  \|  \|
1---2---3
|\0 |\1 |
| \ | \ |
|  \|  \|
0---1---2

Cellules:
0: [0,1,2]
1: [1,3,2]
2: [2,3,4]
3: [3,5,4]
4: [4,5,6]
```

### 4.2 Algorithmes de génération (Gmsh)

#### Delaunay Triangulation (2D)

```
Entrée: Ensemble de points P et contraintes de frontière

Algorithme:
1. Créer un super-triangle englobant tous les points
2. Pour chaque point p dans P:
   a. Trouver tous les triangles dont le cercle circonscrit contient p
   b. Supprimer ces triangles
   c. Créer de nouveaux triangles en connectant p aux arêtes du "trou"
3. Supprimer les triangles contenant des sommets du super-triangle
4. Raffiner jusqu'à atteindre la qualité désirée
```

**Propriété clé**: Maximise l'angle minimal de tous les triangles → évite les triangles "plats"

#### Advancing Front Method

```
1. Commencer avec les arêtes de la frontière (le "front")
2. Tant que le front n'est pas vide:
   a. Sélectionner une arête du front
   b. Créer un nouveau sommet optimal (si nécessaire)
   c. Créer un nouveau triangle
   d. Mettre à jour le front
3. Raffiner si nécessaire
```

---

## 5. Critères de qualité du maillage

### Mesures de qualité

1. **Rapport d'aspect (Aspect Ratio)**

   ```
   AR = longueur max / longueur min
   Idéal: AR ≈ 1 (triangle équilatéral)
   Acceptable: AR < 10
   ```

2. **Angle minimal**

   ```
   Pour triangles: θ_min > 30° (idéal > 40°)
   ```

3. **Critère de Delaunay**

   ```
   Le cercle circonscrit ne contient aucun autre sommet
   ```

4. **Taille des éléments**
   ```
   h = diamètre de l'élément
   Doit varier graduellement (pas de changements brusques)
   ```

---

## 6. Processus complet dans FEniCS

### 6.1 Création directe (simple)

```python
from dolfinx import mesh
from mpi4py import MPI
import numpy as np

# 1. Définir les paramètres
points_debut = np.array([0, 0])
points_fin = np.array([1, 1])
nx, ny = 10, 10  # Nombre d'éléments

# 2. FEniCS génère automatiquement:
#    - Les sommets (grid régulière)
#    - Les cellules (triangulation)
#    - La connectivité (tables d'adjacence)
domain = mesh.create_rectangle(
    MPI.COMM_WORLD,
    [points_debut, points_fin],
    [nx, ny],
    mesh.CellType.triangle
)
```

### 6.2 Avec Gmsh (complexe)

```python
import gmsh

# 1. Initialisation
gmsh.initialize()
gmsh.model.add("geometry")

# 2. Définir la géométrie (via API ou script .geo)
#    - Créer les points
#    - Créer les courbes
#    - Créer les surfaces
#    - Définir les contraintes de taille

# 3. Gmsh génère le maillage:
#    a. Analyse de la géométrie
#    b. Discrétisation des courbes (1D)
#    c. Triangulation des surfaces (2D)
#    d. Tétraédrisation des volumes (3D)
gmsh.model.mesh.generate(2)  # 2 = dimension

# 4. Import dans FEniCS
from dolfinx.io import gmshio
domain, markers, facet_markers = gmshio.model_to_mesh(
    gmsh.model, MPI.COMM_WORLD, 0, gdim=2
)

gmsh.finalize()
```

---

## 7. Raffinement de maillage

### Raffinement uniforme

```
Chaque cellule est subdivisée en 4 sous-cellules

Triangle parent:        Triangles enfants:
    2                       2
   /|\                     /|\
  / | \                   4-+-5
 /  |  \                 /|\ /|\
0---+---1               0-+-3-+-1
```

### Raffinement adaptatif

Basé sur un estimateur d'erreur:

```python
# Pseudo-code
while erreur > tolérance:
    1. Calculer la solution
    2. Estimer l'erreur locale par élément
    3. Marquer les éléments à raffiner (erreur > seuil)
    4. Raffiner ces éléments
    5. Recalculer
```

---

## 8. Stockage et représentation en mémoire

### Structure de données dans FEniCS

```python
# Topologie (connectivité)
topology = {
    0: {  # Sommets
        'count': N_vertices,
        'connectivity': index_map
    },
    1: {  # Arêtes
        'count': N_edges,
        'vertex_connectivity': [[v1, v2], ...],
        'cell_connectivity': [[c1, c2], ...]  # cellules adjacentes
    },
    2: {  # Cellules (en 2D)
        'count': N_cells,
        'vertex_connectivity': [[v1, v2, v3], ...]  # pour triangles
    }
}

# Géométrie (coordonnées)
geometry = {
    'x': [[x1, y1], [x2, y2], ...],  # Coordonnées des sommets
    'dofmap': index_map  # Mapping DOF local -> global
}
```

### Exemple concret

```python
domain = create_rectangle(..., [2, 2])

# Accès aux données:
num_vertices = domain.topology.index_map(0).size_local
num_cells = domain.topology.index_map(2).size_local

# Coordonnées des sommets
coords = domain.geometry.x  # Array numpy

# Connectivité cellule->sommets
dofmap = domain.geometry.dofmap  # Array 2D
```

---

## 9. Parallélisation du maillage

FEniCS utilise MPI pour le calcul parallèle:

```
Processus 0        Processus 1        Processus 2
+--------+         +--------+         +--------+
|  Part  |         |  Part  |         |  Part  |
|   0    | <-----> |   1    | <-----> |   2    |
+--------+         +--------+         +--------+

Chaque processus:
- Possède une partie du maillage
- Connaît les cellules "fantômes" des voisins
- Communique aux interfaces
```

---

## 10. Points clés à retenir

1. **Un maillage = Topologie + Géométrie**

   - Topologie: Connectivité (qui est connecté à qui)
   - Géométrie: Positions dans l'espace

2. **Qualité du maillage = Qualité de la solution**

   - Éléments trop déformés → erreurs numériques
   - Maillage trop grossier → perte de précision
   - Maillage trop fin → coût calculatoire élevé

3. **Choix de la méthode**

   - Géométrie simple → maillages intégrés FEniCS
   - Géométrie complexe → Gmsh
   - Raffinement adaptatif → selon l'erreur locale

4. **Types d'éléments**
   - Triangles/Tétraèdres: Plus flexibles, maillages non structurés
   - Quadrilatères/Hexaèdres: Plus précis pour problèmes alignés

---

## Références et ressources

- Documentation FEniCSx: https://docs.fenicsproject.org
- Gmsh documentation: https://gmsh.info
- "The Finite Element Method" par Larson & Bengzon
- "Mesh Generation" par P.-L. George
