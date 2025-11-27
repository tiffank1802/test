"""
Utilisation de Gmsh pour créer des maillages complexes pour FEniCS
Gmsh est l'outil standard pour les géométries complexes
"""
import gmsh
from dolfinx.io import gmshio
from mpi4py import MPI
import numpy as np

# Initialiser Gmsh
gmsh.initialize()
gmsh.model.add("complex_structure")

# Exemple 1: Disque avec trou (2D)
# ----------------------------------
lc = 0.1  # Taille caractéristique des éléments

# Centre du disque extérieur
gmsh.model.geo.addPoint(0, 0, 0, lc, 1)

# Points du cercle extérieur (rayon 1)
gmsh.model.geo.addPoint(1, 0, 0, lc, 2)
gmsh.model.geo.addPoint(0, 1, 0, lc, 3)
gmsh.model.geo.addPoint(-1, 0, 0, lc, 4)
gmsh.model.geo.addPoint(0, -1, 0, lc, 5)

# Arcs du cercle extérieur
gmsh.model.geo.addCircleArc(2, 1, 3, 1)
gmsh.model.geo.addCircleArc(3, 1, 4, 2)
gmsh.model.geo.addCircleArc(4, 1, 5, 3)
gmsh.model.geo.addCircleArc(5, 1, 2, 4)

# Curve loop extérieure
gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 1)

# Trou intérieur (rayon 0.3)
gmsh.model.geo.addPoint(0.3, 0, 0, lc, 10)
gmsh.model.geo.addPoint(0, 0.3, 0, lc, 11)
gmsh.model.geo.addPoint(-0.3, 0, 0, lc, 12)
gmsh.model.geo.addPoint(0, -0.3, 0, lc, 13)

gmsh.model.geo.addCircleArc(10, 1, 11, 10)
gmsh.model.geo.addCircleArc(11, 1, 12, 11)
gmsh.model.geo.addCircleArc(12, 1, 13, 12)
gmsh.model.geo.addCircleArc(13, 1, 10, 13)

# Curve loop intérieure
gmsh.model.geo.addCurveLoop([10, 11, 12, 13], 2)

# Surface avec trou
gmsh.model.geo.addPlaneSurface([1, 2], 1)

# Synchroniser
gmsh.model.geo.synchronize()

# Définir des groupes physiques (pour les conditions aux limites)
gmsh.model.addPhysicalGroup(1, [1, 2, 3, 4], 1, name="outer_boundary")
gmsh.model.addPhysicalGroup(1, [10, 11, 12, 13], 2, name="inner_boundary")
gmsh.model.addPhysicalGroup(2, [1], 1, name="domain")

# Générer le maillage 2D
gmsh.model.mesh.generate(2)

# Optionnel: raffiner le maillage
# gmsh.model.mesh.refine()

# Sauvegarder (optionnel)
gmsh.write("disk_with_hole.msh")

# Importer dans DOLFINx
domain, cell_markers, facet_markers = gmshio.model_to_mesh(
    gmsh.model, MPI.COMM_WORLD, 0, gdim=2
)

print(f"Nombre de cellules: {domain.topology.index_map(2).size_local}")
print(f"Nombre de facettes marquées: {len(facet_markers.values)}")

# Finaliser Gmsh
gmsh.finalize()

# Maintenant vous pouvez utiliser 'domain' dans vos calculs FEniCS
# avec 'facet_markers' pour appliquer les conditions aux limites
