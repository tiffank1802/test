# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.18.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Implementation
#
# Author: Jørgen Schartum Dokken
#
# This implementation is an adaptation of the work in {cite}`fundamentals-FenicsTutorial` to DOLFINx.
#
# In this section, you will learn:
# - How to use the built-in meshes in DOLFINx
# - How to create a spatially varying Dirichlet boundary conditions on the whole domain boundary
# - How to define a weak formulation of your PDE
# - How to solve the resulting system of linear equations
# - How to visualize the solution using a variety of tools
# - How to compute the $L^2(\Omega)$ error and the error at mesh vertices

# The Poisson problem has so far featured a general domain $\Omega$ and general functions $u_D$ for
# the boundary conditions and $f$ for the right hand side.
# Therefore, we need to make specific choices of $\Omega, u_D$ and $f$.
# A wise choice is to construct a problem  with a known analytical solution,
# so that we can check that the computed solution is correct.
# The primary candidates are lower-order polynomials.
# The continuous Galerkin finite element spaces of degree $r$ will exactly reproduce polynomials of degree $r$.
#  We use this fact to construct a quadratic function in $2D$. In particular we choose
#
# $$
# \begin{align}
#  u_e(x,y)=1+x^2+2y^2
#  \end{align}
# $$
#
# Inserting $u_e$ in the original boundary problem, we find that
#
# $$
# \begin{align}
#     f(x,y)= -6,\qquad u_D(x,y)=u_e(x,y)=1+x^2+2y^2,
# \end{align}
# $$
#
# regardless of the shape of the domain as long as we prescribe
# $u_e$ on the boundary.
#
# For simplicity, we choose the domain to be a unit square $\Omega=[0,1]\times [0,1]$

# A major difference between a traditional FEniCS code and a FEniCSx code,
# is that one is not advised to use the wildcard import.

# ## Generating simple meshes
# The next step is to define the discrete domain, _the mesh_.
# We do this by importing one of the built-in mesh generators.
# We will build a {py:func}`unit square mesh<dolfinx.mesh.create_unit_square>`, i.e. a mesh spanning $[0,1]\times[0,1]$.

from mpi4py import MPI
from dolfinx import mesh
import numpy

domain = mesh.create_unit_square(MPI.COMM_WORLD, 8, 8, mesh.CellType.quadrilateral)

# ## Defining the finite element function space
# Once the mesh has been created, we can create the finite element function space $V$.

from dolfinx import fem

V = fem.functionspace(domain, ("Lagrange", 1))

# ## Dirichlet boundary conditions
# Next, we create a function that will hold the Dirichlet boundary data, and use interpolation to
# fill it with the appropriate data.

uD = fem.Function(V)
uD.interpolate(lambda x: 1 + x[0]**2 + 2 * x[1]**2)

# Identify boundary facets and create boundary condition
tdim = domain.topology.dim
fdim = tdim - 1
domain.topology.create_connectivity(fdim, tdim)
boundary_facets = mesh.exterior_facet_indices(domain.topology)
boundary_dofs = fem.locate_dofs_topological(V, fdim, boundary_facets)
bc = fem.dirichletbc(uD, boundary_dofs)

# ## Defining the trial and test function
import ufl

u = ufl.TrialFunction(V)
v = ufl.TestFunction(V)

# ## Defining the source term
from dolfinx import default_scalar_type

f = fem.Constant(domain, default_scalar_type(-6))

# ## Defining the variational problem
a = ufl.dot(ufl.grad(u), ufl.grad(v)) * ufl.dx
L = f * v * ufl.dx

# ## Forming and solving the linear system
from dolfinx.fem.petsc import LinearProblem

problem = LinearProblem(
    a,
    L,
    bcs=[bc],
    petsc_options={"ksp_type": "preonly", "pc_type": "lu"},
    petsc_options_prefix="Poisson",
)
uh = problem.solve()

# ## Computing the error
V2 = fem.functionspace(domain, ("Lagrange", 2))
uex = fem.Function(V2, name="u_exact")
uex.interpolate(lambda x: 1 + x[0]**2 + 2 * x[1]**2)

# Compute L2 error
L2_error = fem.form(ufl.inner(uh - uex, uh - uex) * ufl.dx)
error_local = fem.assemble_scalar(L2_error)
error_L2 = numpy.sqrt(domain.comm.allreduce(error_local, op=MPI.SUM))

# Compute max error
error_max = numpy.max(numpy.abs(uD.x.array - uh.x.array))

# Print errors
if domain.comm.rank == 0:
    print(f"Error_L2 : {error_L2:.2e}")
    print(f"Error_max : {error_max:.2e}")

# ## Plotting the mesh using pyvista
try:
    import pyvista
    from dolfinx import plot
    
    domain.topology.create_connectivity(tdim, tdim)
    topology, cell_types, geometry = plot.vtk_mesh(domain, tdim)
    grid = pyvista.UnstructuredGrid(topology, cell_types, geometry)
    
    plotter = pyvista.Plotter()
    plotter.add_mesh(grid, show_edges=True)
    plotter.view_xy()
    if not pyvista.OFF_SCREEN:
        plotter.show()
    else:
        figure = plotter.screenshot("fundamentals_mesh.png")
        print("Mesh plot saved as fundamentals_mesh.png")
    
    # Plot the solution
    u_topology, u_cell_types, u_geometry = plot.vtk_mesh(V)
    u_grid = pyvista.UnstructuredGrid(u_topology, u_cell_types, u_geometry)
    u_grid.point_data["u"] = uh.x.array.real
    u_grid.set_active_scalars("u")
    
    u_plotter = pyvista.Plotter()
    u_plotter.add_mesh(u_grid, show_edges=True)
    u_plotter.view_xy()
    if not pyvista.OFF_SCREEN:
        u_plotter.show()
    else:
        u_plotter.screenshot("fundamentals_solution.png")
        print("Solution plot saved as fundamentals_solution.png")
        
except ImportError:
    print("PyVista not available for plotting")

# ## Save results for external post-processing
from dolfinx import io
from pathlib import Path

results_folder = Path("results")
results_folder.mkdir(exist_ok=True, parents=True)
filename = results_folder / "fundamentals"

# Save using VTXWriter
with io.VTXWriter(domain.comm, filename.with_suffix(".bp"), [uh]) as vtx:
    vtx.write(0.0)

# Save using XDMFFile
with io.XDMFFile(domain.comm, filename.with_suffix(".xdmf"), "w") as xdmf:
    xdmf.write_mesh(domain)
    xdmf.write_function(uh)

if domain.comm.rank == 0:
    print("Results saved to results/fundamentals.bp and results/fundamentals.xdmf")