"""
Exemple de maillages intégrés avec DOLFINx (FEniCSx)
"""
from dolfinx import mesh
from mpi4py import MPI
import numpy as np

# Maillage 2D rectangle
domain = mesh.create_rectangle(
    MPI.COMM_WORLD,
    [np.array([0, 0]), np.array([1, 1])],  # Coins du rectangle
    [32, 32],  # Nombre d'éléments en x et y
    mesh.CellType.triangle
)
print(f"Rectangle mesh: {domain.topology.index_map(2).size_local} cells")

# Maillage 3D boîte
domain_3d = mesh.create_box(
    MPI.COMM_WORLD,
    [np.array([0, 0, 0]), np.array([1, 1, 1])],  # Coins de la boîte
    [10, 10, 10],  # Nombre d'éléments
    mesh.CellType.tetrahedron
)
print(f"Box mesh: {domain_3d.topology.index_map(3).size_local} cells")

# Autres géométries disponibles:
# - create_unit_square
# - create_unit_cube
# - create_interval
