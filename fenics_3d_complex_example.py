"""
Exemple de structure 3D complexe: cylindre avec cavité
"""
import gmsh
from dolfinx.io import gmshio
from mpi4py import MPI

gmsh.initialize()
gmsh.model.add("cylinder_cavity")

# Paramètres
R_outer = 1.0  # Rayon extérieur
R_inner = 0.3  # Rayon de la cavité
H = 2.0        # Hauteur
lc = 0.2       # Taille des éléments

# Créer un cylindre avec une cavité sphérique
# Cylindre extérieur
cylinder = gmsh.model.occ.addCylinder(0, 0, 0, 0, 0, H, R_outer)

# Sphère intérieure (cavité)
sphere = gmsh.model.occ.addSphere(0, 0, H/2, R_inner)

# Soustraire la sphère du cylindre
result = gmsh.model.occ.cut([(3, cylinder)], [(3, sphere)])

# Synchroniser
gmsh.model.occ.synchronize()

# Définir groupes physiques
# Volume
volumes = gmsh.model.getEntities(dim=3)
gmsh.model.addPhysicalGroup(3, [v[1] for v in volumes], 1, name="volume")

# Surfaces
surfaces = gmsh.model.getEntities(dim=2)
gmsh.model.addPhysicalGroup(2, [s[1] for s in surfaces], 1, name="boundary")

# Options de maillage
gmsh.option.setNumber("Mesh.CharacteristicLengthMin", lc)
gmsh.option.setNumber("Mesh.CharacteristicLengthMax", lc)

# Générer le maillage 3D
gmsh.model.mesh.generate(3)

# Sauvegarder
gmsh.write("cylinder_cavity.msh")

# Importer dans DOLFINx
domain, cell_markers, facet_markers = gmshio.model_to_mesh(
    gmsh.model, MPI.COMM_WORLD, 0, gdim=3
)

print(f"Nombre de tétraèdres: {domain.topology.index_map(3).size_local}")

gmsh.finalize()
