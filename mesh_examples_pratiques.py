"""
Exemples pratiques illustrant les concepts du cours sur les maillages
"""
from dolfinx import mesh
from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt

print("="*70)
print("EXEMPLES PRATIQUES: Structure d'un maillage FEniCS")
print("="*70)

# =============================================================================
# Exemple 1: Anatomie d'un maillage simple
# =============================================================================
print("\n" + "="*70)
print("Exemple 1: Anatomie d'un maillage 2x2")
print("="*70)

domain = mesh.create_rectangle(
    MPI.COMM_WORLD,
    [np.array([0, 0]), np.array([1, 1])],
    [2, 2],  # Maillage 2x2
    mesh.CellType.triangle
)

# Extraire les informations
print("\n📊 GÉOMÉTRIE:")
print(f"  - Coordonnées des sommets (geometry.x):")
coords = domain.geometry.x
for i, coord in enumerate(coords):
    print(f"      Sommet {i}: ({coord[0]:.2f}, {coord[1]:.2f})")

print(f"\n  - Nombre total de sommets: {len(coords)}")

print("\n📐 TOPOLOGIE:")
# Créer les entités topologiques avant d'y accéder
domain.topology.create_entities(0)  # Sommets
domain.topology.create_entities(1)  # Arêtes
domain.topology.create_entities(2)  # Cellules

# Nombre d'entités de chaque dimension
num_vertices = domain.topology.index_map(0).size_local
num_edges = domain.topology.index_map(1).size_local
num_cells = domain.topology.index_map(2).size_local

print(f"  - Dimension 0 (sommets): {num_vertices}")
print(f"  - Dimension 1 (arêtes):  {num_edges}")
print(f"  - Dimension 2 (cellules): {num_cells}")

print("\n🔗 CONNECTIVITÉ:")
print("  - Cellule → Sommets (dofmap):")
dofmap = domain.geometry.dofmap
for i, cell_vertices in enumerate(dofmap):
    vertex_coords = coords[cell_vertices]
    print(f"      Cellule {i}: sommets {cell_vertices.tolist()}")
    print(f"                  coords: {[(v[0], v[1]) for v in vertex_coords]}")

# Visualiser
fig, ax = plt.subplots(figsize=(8, 8))

# Dessiner les cellules
for i, cell_vertices in enumerate(dofmap):
    vertices = np.append(cell_vertices, cell_vertices[0])
    ax.plot(coords[vertices, 0], coords[vertices, 1], 'b-', linewidth=2)
    
    # Numéro de cellule au centre
    center = np.mean(coords[cell_vertices], axis=0)
    ax.text(center[0], center[1], f'C{i}', ha='center', va='center',
            fontsize=14, color='red', weight='bold',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

# Dessiner et numéroter les sommets
ax.plot(coords[:, 0], coords[:, 1], 'ko', markersize=12)
for i, coord in enumerate(coords):
    ax.text(coord[0], coord[1], f'  V{i}', fontsize=12, color='blue', weight='bold')

ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('y', fontsize=12)
ax.set_title('Anatomie d\'un maillage 2x2\n(C=Cellule, V=Sommet)', fontsize=14, weight='bold')
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)
plt.savefig('mesh_anatomy_2x2.png', dpi=150, bbox_inches='tight')
print("\n✓ Visualisation sauvegardée: mesh_anatomy_2x2.png")
plt.close()

# =============================================================================
# Exemple 2: Effet du raffinement
# =============================================================================
print("\n" + "="*70)
print("Exemple 2: Effet du nombre d'éléments")
print("="*70)

resolutions = [2, 4, 8, 16]
fig, axes = plt.subplots(2, 2, figsize=(14, 14))

for idx, (ax, n) in enumerate(zip(axes.flat, resolutions)):
    domain = mesh.create_rectangle(
        MPI.COMM_WORLD,
        [np.array([0, 0]), np.array([1, 1])],
        [n, n],
        mesh.CellType.triangle
    )
    
    coords = domain.geometry.x
    dofmap = domain.geometry.dofmap
    
    # Dessiner le maillage
    for cell_vertices in dofmap:
        vertices = np.append(cell_vertices, cell_vertices[0])
        ax.plot(coords[vertices, 0], coords[vertices, 1], 'b-', linewidth=0.5)
    
    ax.plot(coords[:, 0], coords[:, 1], 'ro', markersize=2)
    
    num_cells = domain.topology.index_map(2).size_local
    num_vertices = len(coords)
    
    ax.set_title(f'{n}×{n} éléments\n{num_cells} cellules, {num_vertices} sommets',
                 fontsize=12, weight='bold')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    
    print(f"\n  {n}×{n}: {num_cells:4d} cellules, {num_vertices:4d} sommets")

plt.tight_layout()
plt.savefig('mesh_refinement_comparison.png', dpi=150, bbox_inches='tight')
print("\n✓ Visualisation sauvegardée: mesh_refinement_comparison.png")
plt.close()

# =============================================================================
# Exemple 3: Types d'éléments (Triangles vs Quadrilatères)
# =============================================================================
print("\n" + "="*70)
print("Exemple 3: Comparaison Triangles vs Quadrilatères")
print("="*70)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Triangles
domain_tri = mesh.create_rectangle(
    MPI.COMM_WORLD,
    [np.array([0, 0]), np.array([1, 1])],
    [4, 4],
    mesh.CellType.triangle
)

coords_tri = domain_tri.geometry.x
dofmap_tri = domain_tri.geometry.dofmap

for cell_vertices in dofmap_tri:
    vertices = np.append(cell_vertices, cell_vertices[0])
    ax1.plot(coords_tri[vertices, 0], coords_tri[vertices, 1], 'b-', linewidth=1.5)

ax1.plot(coords_tri[:, 0], coords_tri[:, 1], 'ro', markersize=6)
ax1.set_title('Maillage Triangulaire\n(2 triangles par carré)',
              fontsize=14, weight='bold')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.3)

# Quadrilatères
domain_quad = mesh.create_rectangle(
    MPI.COMM_WORLD,
    [np.array([0, 0]), np.array([1, 1])],
    [4, 4],
    mesh.CellType.quadrilateral
)

coords_quad = domain_quad.geometry.x
dofmap_quad = domain_quad.geometry.dofmap

for cell_vertices in dofmap_quad:
    vertices = np.append(cell_vertices, cell_vertices[0])
    ax2.plot(coords_quad[vertices, 0], coords_quad[vertices, 1], 'g-', linewidth=1.5)

ax2.plot(coords_quad[:, 0], coords_quad[:, 1], 'ro', markersize=6)
ax2.set_title('Maillage Quadrilatéral\n(1 quadrilatère par carré)',
              fontsize=14, weight='bold')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.3)

print(f"\n  Triangles:      {domain_tri.topology.index_map(2).size_local} cellules")
print(f"  Quadrilatères:  {domain_quad.topology.index_map(2).size_local} cellules")

plt.tight_layout()
plt.savefig('mesh_element_types.png', dpi=150, bbox_inches='tight')
print("\n✓ Visualisation sauvegardée: mesh_element_types.png")
plt.close()

# =============================================================================
# Exemple 4: Calcul de qualité du maillage
# =============================================================================
print("\n" + "="*70)
print("Exemple 4: Analyse de la qualité du maillage")
print("="*70)

domain = mesh.create_rectangle(
    MPI.COMM_WORLD,
    [np.array([0, 0]), np.array([2, 1])],
    [8, 4],
    mesh.CellType.triangle
)

coords = domain.geometry.x
dofmap = domain.geometry.dofmap

# Calculer le rapport d'aspect pour chaque triangle
aspect_ratios = []
angles_min = []

for cell_vertices in dofmap:
    # Récupérer les coordonnées
    v0, v1, v2 = coords[cell_vertices]
    
    # Calculer les longueurs des côtés
    a = np.linalg.norm(v1 - v0)
    b = np.linalg.norm(v2 - v1)
    c = np.linalg.norm(v0 - v2)
    
    # Rapport d'aspect
    max_len = max(a, b, c)
    min_len = min(a, b, c)
    ar = max_len / min_len if min_len > 0 else float('inf')
    aspect_ratios.append(ar)
    
    # Angle minimal (loi des cosinus)
    angles = []
    for side1, side2, opposite in [(a, c, b), (a, b, c), (b, c, a)]:
        cos_angle = (side1**2 + side2**2 - opposite**2) / (2 * side1 * side2)
        cos_angle = np.clip(cos_angle, -1, 1)  # Pour éviter erreurs numériques
        angle = np.arccos(cos_angle) * 180 / np.pi
        angles.append(angle)
    angles_min.append(min(angles))

print(f"\n📏 STATISTIQUES DE QUALITÉ:")
print(f"  Rapport d'aspect:")
print(f"    - Minimum:  {min(aspect_ratios):.2f}")
print(f"    - Maximum:  {max(aspect_ratios):.2f}")
print(f"    - Moyenne:  {np.mean(aspect_ratios):.2f}")
print(f"    - Idéal:    1.00 (triangle équilatéral)")
print(f"\n  Angle minimal:")
print(f"    - Minimum:  {min(angles_min):.1f}°")
print(f"    - Maximum:  {max(angles_min):.1f}°")
print(f"    - Moyenne:  {np.mean(angles_min):.1f}°")
print(f"    - Acceptable: > 30°")

# Visualiser avec code couleur
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Visualisation par rapport d'aspect
for cell_vertices, ar in zip(dofmap, aspect_ratios):
    vertices = np.append(cell_vertices, cell_vertices[0])
    color = plt.cm.RdYlGn_r((ar - 1) / 2)  # Rouge=mauvais, Vert=bon
    ax1.fill(coords[vertices, 0], coords[vertices, 1], color=color, alpha=0.7, edgecolor='black')

ax1.set_title('Rapport d\'aspect\n(Vert=bon, Rouge=mauvais)', fontsize=14, weight='bold')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_aspect('equal')

# Visualisation par angle minimal
for cell_vertices, angle in zip(dofmap, angles_min):
    vertices = np.append(cell_vertices, cell_vertices[0])
    color = plt.cm.RdYlGn((angle - 30) / 30)  # Normalisé autour de 30-60°
    ax2.fill(coords[vertices, 0], coords[vertices, 1], color=color, alpha=0.7, edgecolor='black')

ax2.set_title('Angle minimal\n(Vert=bon, Rouge=mauvais)', fontsize=14, weight='bold')
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_aspect('equal')

plt.tight_layout()
plt.savefig('mesh_quality_analysis.png', dpi=150, bbox_inches='tight')
print("\n✓ Visualisation sauvegardée: mesh_quality_analysis.png")
plt.close()

print("\n" + "="*70)
print("✓ Tous les exemples ont été générés avec succès!")
print("="*70)
print("\nFichiers créés:")
print("  1. mesh_anatomy_2x2.png - Anatomie détaillée")
print("  2. mesh_refinement_comparison.png - Effet du raffinement")
print("  3. mesh_element_types.png - Types d'éléments")
print("  4. mesh_quality_analysis.png - Analyse de qualité")
