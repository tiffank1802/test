"""
Importer des maillages depuis des fichiers CAO ou autres formats
"""
import gmsh
from dolfinx.io import gmshio
from mpi4py import MPI

# Méthode 1: Importer un fichier STEP/IGES (CAO)
# ------------------------------------------------
gmsh.initialize()
gmsh.model.add("imported_geometry")

# Importer un fichier CAO (nécessite OpenCASCADE)
# gmsh.model.occ.importShapes("geometry.step")
# gmsh.model.occ.synchronize()

# Méthode 2: Importer un maillage MSH existant
# ---------------------------------------------
# gmsh.merge("existing_mesh.msh")

# Méthode 3: Créer programmatiquement avec des booléens
# ------------------------------------------------------
# Rectangle
rect = gmsh.model.occ.addRectangle(0, 0, 0, 2, 1)

# Cercle à soustraire
circle = gmsh.model.occ.addDisk(0.5, 0.5, 0, 0.2, 0.2)

# Opération booléenne: différence
result = gmsh.model.occ.cut([(2, rect)], [(2, circle)])

gmsh.model.occ.synchronize()

# Marquage des frontières
# Vous pouvez identifier les frontières par leur position
surfaces = gmsh.model.getEntities(dim=2)
gmsh.model.addPhysicalGroup(2, [s[1] for s in surfaces], 1, name="domain")

curves = gmsh.model.getEntities(dim=1)
# Identifier les courbes par leur bounding box
for curve in curves:
    com = gmsh.model.occ.getCenterOfMass(1, curve[1])
    # Exemple: marquer les bords selon leur position
    if abs(com[0]) < 1e-6:  # Bord gauche
        gmsh.model.addPhysicalGroup(1, [curve[1]], 10, name="left")
    # etc.

gmsh.model.mesh.generate(2)

domain, cell_markers, facet_markers = gmshio.model_to_mesh(
    gmsh.model, MPI.COMM_WORLD, 0, gdim=2
)

gmsh.finalize()

print(f"Import réussi: {domain.topology.index_map(2).size_local} cellules")
