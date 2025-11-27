"""
Visualisation et sauvegarde de maillages FEniCS 3D avec pyvista
"""
from dolfinx import mesh, plot
from mpi4py import MPI
import numpy as np
import pyvista as pv

# Créer un maillage 3D
domain = mesh.create_box(
    MPI.COMM_WORLD,
    [np.array([0, 0, 0]), np.array([1, 1, 1])],
    [8, 8, 8],
    mesh.CellType.tetrahedron
)

# Créer un objet pyvista à partir du maillage DOLFINx
topology, cell_types, geometry = plot.vtk_mesh(domain, domain.topology.dim)
grid = pv.UnstructuredGrid(topology, cell_types, geometry)

# Méthode 1: Vue simple du maillage
plotter = pv.Plotter(off_screen=True)
plotter.add_mesh(grid, show_edges=True, color='lightblue', opacity=0.8)
plotter.add_axes()
plotter.view_isometric()
plotter.screenshot('mesh_3d_simple.png', window_size=[1920, 1080])
plotter.close()
print("Maillage 3D simple sauvegardé dans: mesh_3d_simple.png")

# Méthode 2: Vue avec les arêtes mises en évidence
plotter = pv.Plotter(off_screen=True)
plotter.add_mesh(grid, show_edges=True, edge_color='black', 
                 color='white', opacity=0.3, line_width=1)
plotter.add_axes()
plotter.camera_position = 'iso'
plotter.screenshot('mesh_3d_edges.png', window_size=[1920, 1080])
plotter.close()
print("Maillage 3D avec arêtes sauvegardé dans: mesh_3d_edges.png")

# Méthode 3: Vues multiples
plotter = pv.Plotter(shape=(2, 2), off_screen=True)

# Vue 1: Isométrique
plotter.subplot(0, 0)
plotter.add_mesh(grid, show_edges=True, color='cyan')
plotter.add_text("Vue isométrique", font_size=10)
plotter.view_isometric()

# Vue 2: Vue de face
plotter.subplot(0, 1)
plotter.add_mesh(grid, show_edges=True, color='yellow')
plotter.add_text("Vue de face", font_size=10)
plotter.view_xy()

# Vue 3: Vue de côté
plotter.subplot(1, 0)
plotter.add_mesh(grid, show_edges=True, color='magenta')
plotter.add_text("Vue de côté", font_size=10)
plotter.view_xz()

# Vue 4: Vue de dessus
plotter.subplot(1, 1)
plotter.add_mesh(grid, show_edges=True, color='lightgreen')
plotter.add_text("Vue de dessus", font_size=10)
plotter.view_yz()

plotter.screenshot('mesh_3d_multiview.png', window_size=[2400, 2400])
plotter.close()
print("Maillage 3D multi-vues sauvegardé dans: mesh_3d_multiview.png")

# Méthode 4: Maillage avec transparence et qualité
plotter = pv.Plotter(off_screen=True)
plotter.add_mesh(grid, show_edges=True, edge_color='navy', 
                 color='lightblue', opacity=0.5, line_width=0.5)
plotter.add_axes()
plotter.add_text("Maillage 3D - Boîte unitaire", position='upper_left', font_size=12)

# Ajouter des informations
num_cells = domain.topology.index_map(domain.topology.dim).size_local
num_vertices = domain.topology.index_map(0).size_local
info_text = f"Cellules: {num_cells}\nSommets: {num_vertices}"
plotter.add_text(info_text, position='lower_right', font_size=10)

plotter.camera_position = [(2, 2, 2), (0.5, 0.5, 0.5), (0, 0, 1)]
plotter.screenshot('mesh_3d_quality.png', window_size=[1920, 1080])
plotter.close()
print("Maillage 3D haute qualité sauvegardé dans: mesh_3d_quality.png")

# Méthode 5: Coupe du maillage
plotter = pv.Plotter(off_screen=True)

# Créer une coupe au milieu
slice_mesh = grid.slice(normal=[1, 0, 0], origin=[0.5, 0.5, 0.5])

plotter.add_mesh(grid, show_edges=True, opacity=0.2, color='lightgray')
plotter.add_mesh(slice_mesh, show_edges=True, color='red', edge_color='darkred')
plotter.add_axes()
plotter.add_text("Coupe du maillage (x=0.5)", position='upper_left', font_size=12)
plotter.view_isometric()
plotter.screenshot('mesh_3d_slice.png', window_size=[1920, 1080])
plotter.close()
print("Maillage 3D avec coupe sauvegardé dans: mesh_3d_slice.png")

print("\nTous les fichiers 3D ont été créés avec succès!")
print("\nPour visualiser interactivement, utilisez:")
print("  plotter.show() au lieu de plotter.screenshot()")
