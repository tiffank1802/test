import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from fe_appprox1D import *
import sympy as sym

def run_simulation():
    # Parameters
    L = 1.0
    T = 2
    c = 1.0e2  # Wave speed
    Ne = 10  # Number of elements
    d = 2    # Degree of basis functions
    
    # Mesh
    nodes = np.linspace(0, L, Ne * d + 1)
    elements = [[i + j for j in range(d + 1)] for i in range(0, Ne * d, d)]
    
    # Basis functions
    phi = basis(d=d, symbolic=False)
    
    # Assemble Mass and Stiffness Matrices
    print("Assembling matrices...")
    # Mass matrix (using element_matrix)
    M, _ = assemble(nodes, elements, phi, f=None, symbolic=False, matrix_function=element_matrix)
    M = np.array(M, dtype=float)
    
    # Stiffness matrix (using element_stiffness_matrix)
    K, _ = assemble(nodes, elements, phi, f=None, symbolic=False, matrix_function=element_stiffness_matrix)
    K = np.array(K, dtype=float) * (c**2) # Scale by c^2 for wave equation u_tt - c^2 u_xx = 0
    
    # Time stepping parameters
    h = nodes[1] - nodes[0]
    dt = 0.9 * h / c  # CFL condition
    Nt = int(T / dt)
    print(f"dt = {dt}, Nt = {Nt}")
    
    # Initial conditions
    x = nodes
    u0 = np.exp(-100 * (x - 0.5)**2) # Gaussian pulse
    v0 = np.zeros_like(u0)
    
    # Arrays to store solution
    u = np.zeros((Nt + 1, len(nodes)))
    u[0] = u0
    
    # Boundary conditions (Fixed ends: u(0) = u(L) = 0)
    # We will enforce this by solving for inner nodes only or using penalty.
    # Let's use the method of removing rows/cols for fixed DOFs.
    fixed_dofs = [0, len(nodes) - 1]
    free_dofs = [i for i in range(len(nodes)) if i not in fixed_dofs]
    
    M_free = M[np.ix_(free_dofs, free_dofs)]
    K_free = K[np.ix_(free_dofs, free_dofs)]
    
    # Pre-factorize M_free for faster solution
    # For explicit scheme with consistent mass, we solve M * u_new = rhs
    
    # Initial acceleration
    # M a0 + K u0 = 0 => a0 = -M^-1 K u0
    rhs_0 = -K_free @ u0[free_dofs]
    a0_free = np.linalg.solve(M_free, rhs_0)
    
    # First step (u1) using Taylor expansion
    # u1 = u0 + dt * v0 + 0.5 * dt^2 * a0
    u[1, free_dofs] = u0[free_dofs] + dt * v0[free_dofs] + 0.5 * dt**2 * a0_free
    
    # Time loop
    print("Running simulation...")
    for n in range(1, Nt):
        # Central difference: M (u_{n+1} - 2u_n + u_{n-1})/dt^2 + K u_n = 0
        # M u_{n+1} = dt^2 (-K u_n) + M (2u_n - u_{n-1})
        
        u_n = u[n, free_dofs]
        u_nm1 = u[n-1, free_dofs]
        
        rhs = (dt**2) * (-K_free @ u_n) + M_free @ (2 * u_n - u_nm1)
        u_new_free = np.linalg.solve(M_free, rhs)
        
        u[n+1, free_dofs] = u_new_free
        
        if n % 100 == 0:
            print(f"Step {n}/{Nt}")

    # Animation
    print("Creating animation...")
    fig, ax = plt.subplots()
    line, = ax.plot(nodes, u[0], 'b-')
    ax.set_ylim(-1.2, 1.2)
    ax.set_xlim(0, L)
    ax.set_xlabel('x')
    ax.set_ylabel('u')
    ax.set_title('1D Wave Equation FEM')
    
    def update(frame):
        # Subsample frames to keep GIF size reasonable
        step = frame * 5
        if step >= Nt:
            step = Nt
        line.set_ydata(u[step])
        ax.set_title(f'Time: {step*dt:.3f}s')
        return line,

    num_frames = Nt // 5
    ani = FuncAnimation(fig, update, frames=num_frames, blit=True)
    
    ani.save('bar_simulation.gif', writer=PillowWriter(fps=30))
    print("Animation saved as bar_simulation.gif")

if __name__ == "__main__":
    run_simulation()
