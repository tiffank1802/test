"""
Visualisation et sauvegarde de maillages FEniCS 2D avec matplotlib
"""
from dolfinx import mesh
from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt

# Créer un maillage 2D
domain = mesh.create_rectangle(
    MPI.COMM_WORLD,
    [np.array([0, 0]), np.array([2, 1])],
    [20, 10],
    mesh.CellType.triangle
)

# Extraire les points et les cellules
points = domain.geometry.x
cells = domain.geometry.dofmap

# Créer la figure
fig, ax = plt.subplots(figsize=(12, 6))

# Dessiner les triangles
for cell_idx in range(len(cells)):
    cell_vertices = cells[cell_idx]
    # Fermer le triangle en ajoutant le premier point à la fin
    vertices = np.append(cell_vertices, cell_vertices[0])
    ax.plot(points[vertices, 0], points[vertices, 1], 'b-', linewidth=0.5)

# Dessiner les nœuds
ax.plot(points[:, 0], points[:, 1], 'ro', markersize=2)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Maillage 2D - Rectangle')
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)

# Sauvegarder
plt.savefig('mesh_2d_rectangle.png', dpi=300, bbox_inches='tight')
print("Maillage 2D sauvegardé dans: mesh_2d_rectangle.png")
plt.close()

# Exemple 2: Maillage avec plus de détails
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Vue 1: Maillage complet
for cell_idx in range(len(cells)):
    cell_vertices = cells[cell_idx]
    vertices = np.append(cell_vertices, cell_vertices[0])
    ax1.plot(points[vertices, 0], points[vertices, 1], 'b-', linewidth=0.5)
ax1.plot(points[:, 0], points[:, 1], 'ro', markersize=2)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_title('Maillage complet')
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.3)

# Vue 2: Zoom sur une région
for cell_idx in range(len(cells)):
    cell_vertices = cells[cell_idx]
    vertices = np.append(cell_vertices, cell_vertices[0])
    ax2.plot(points[vertices, 0], points[vertices, 1], 'b-', linewidth=1.0)
ax2.plot(points[:, 0], points[:, 1], 'ro', markersize=4)
ax2.set_xlim(0, 0.5)
ax2.set_ylim(0, 0.5)
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_title('Zoom sur une région')
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('mesh_2d_detailed.png', dpi=300, bbox_inches='tight')
print("Maillage détaillé sauvegardé dans: mesh_2d_detailed.png")
plt.close()

# Exemple 3: Afficher les numéros de cellules (pour petit maillage)
domain_small = mesh.create_rectangle(
    MPI.COMM_WORLD,
    [np.array([0, 0]), np.array([1, 1])],
    [4, 4],
    mesh.CellType.triangle
)

points_small = domain_small.geometry.x
cells_small = domain_small.geometry.dofmap

fig, ax = plt.subplots(figsize=(10, 10))

# Dessiner les triangles
for cell_idx in range(len(cells_small)):
    cell_vertices = cells_small[cell_idx]
    vertices = np.append(cell_vertices, cell_vertices[0])
    ax.plot(points_small[vertices, 0], points_small[vertices, 1], 'b-', linewidth=1.5)
    
    # Calculer le centre de la cellule
    center = np.mean(points_small[cell_vertices], axis=0)
    ax.text(center[0], center[1], str(cell_idx), ha='center', va='center', 
            fontsize=8, color='red', weight='bold')

# Dessiner les nœuds avec numéros
ax.plot(points_small[:, 0], points_small[:, 1], 'ko', markersize=8)
for i, point in enumerate(points_small):
    ax.text(point[0], point[1], f'  {i}', fontsize=7, color='blue')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Maillage avec numéros de cellules et nœuds')
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)

plt.savefig('mesh_2d_numbered.png', dpi=300, bbox_inches='tight')
print("Maillage numéroté sauvegardé dans: mesh_2d_numbered.png")
plt.close()

print("\nTous les fichiers ont été créés avec succès!")
