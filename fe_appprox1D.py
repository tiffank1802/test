import sympy as sym
import numpy as np
sym.init_printing()
def basis(d,point_distribution='uniform',symbolic=False):
    """
    Return all local basis functions phi as functions of the local point X
    in a 1D element with d+1 nodes.
    If symbolic=True, return expressions as sympy expressions, else return Python
    functions of X.
    point_distribution can be 'uniform' or 'Chebyshev'.
    """
    X=sym.Symbol('X')
    if d==0:
        phi_sym=[1]
    else:
        if point_distribution=='uniform':
            if symbolic:
                # compute symbolic nodes
                h=sym.Rational(2,d)
                nodes=[-1 + i*h for i in range(d+1)]
            else:
                nodes=np.linspace(-1,1,d+1)
        elif point_distribution=='Chebyshev':
            # Just numeric nodes
            nodes=Chebyshev_nodes(-1,1,d)
        phi_sym=[Lagrange_polynomials(X,r,nodes) for r in range(d+1)]
    # Transform to python functions
    phi_num=[sym.lambdify([X],phi_sym[r], modules='numpy') for r in range(d+1)]
    return phi_sym if symbolic else phi_num

def Lagrange_polynomials(x,i,points):
    p=1
    for k in range(len(points)):
        if k!=i:
            p*=(x-points[k])/(points[i]-points[k])
    return p
 
def element_matrix(phi,Omega_e, symbolic=True):
    n=len(phi)
    if symbolic:
        A_e=sym.zeros(n,n)
    else:
        A_e=np.zeros((n,n), dtype=object)
        
    X=sym.Symbol('X')
    if symbolic:
        h=sym.Symbol('h')
    else:
        h=Omega_e[1]-Omega_e[0]
    detJ=h/2
    for r in range(n):
        phi_r = phi[r](X) if callable(phi[r]) else phi[r]
        for s in range(r,n):
            phi_s = phi[s](X) if callable(phi[s]) else phi[s]
            val = sym.integrate(phi_r*phi_s*detJ,(X,-1,1))
            # if not symbolic:
            #     val = float(val) # Removed to allow symbolic expressions
            A_e[r,s]=val
            A_e[s,r]=A_e[r,s]
    return A_e

def element_vector(f,phi,Omega_e, symbolic=True):
    n=len(phi)
    if symbolic:
        b_e=sym.zeros(n,1)
    else:
        b_e=np.zeros(n, dtype=object)
        
    X=sym.Symbol('X')
    x=sym.Symbol('x') # Global coordinate

    if symbolic:
        h=sym.Symbol('h')
    else:
        h=Omega_e[1]-Omega_e[0]
    detJ=h/2
    
    # Coordinate mapping x -> X
    # x = (Omega_e[0] + Omega_e[1])/2 + h/2 * X
    # or x = Omega_e[0]*(1-X)/2 + Omega_e[1]*(1+X)/2
    x_map = Omega_e[0]*(1-X)/2 + Omega_e[1]*(1+X)/2
    
    if hasattr(f, 'subs'):
        f_mapped = f.subs(x, x_map)
    elif callable(f):
        f_mapped = f(x_map)
    else:
        f_mapped = f

    for r in range(n):
        phi_r = phi[r](X) if callable(phi[r]) else phi[r]
        integrand_expr = f_mapped * phi_r * detJ
        
        I = sym.integrate(integrand_expr, (X, -1, 1))
        # if not symbolic:
        #     I = float(I) # Removed
            
        if symbolic:
            b_e[r] = I
        else:
            b_e[r] = I
    return b_e

def element_stiffness_matrix(phi, Omega_e, symbolic=True):
    n = len(phi)
    if symbolic:
        K_e = sym.zeros(n, n)
    else:
        K_e = np.zeros((n, n), dtype=object)

    X = sym.Symbol('X')
    if symbolic:
        h = sym.Symbol('h')
    else:
        h = Omega_e[1] - Omega_e[0]
    
    # detJ = dx/dX = h/2
    # d/dx = (d/dX) * (dX/dx) = (d/dX) * (2/h)
    detJ = h / 2
    inv_detJ = 2 / h

    for r in range(n):
        phi_r = phi[r](X) if callable(phi[r]) else phi[r]
        dphi_r = sym.diff(phi_r, X)
        for s in range(r, n):
            phi_s = phi[s](X) if callable(phi[s]) else phi[s]
            dphi_s = sym.diff(phi_s, X)
            
            # Integral of (dphi_r/dx * dphi_s/dx) * detJ dX
            # = (dphi_r/dX * inv_detJ) * (dphi_s/dX * inv_detJ) * detJ
            # = dphi_r/dX * dphi_s/dX * inv_detJ
            
            integrand = dphi_r * dphi_s * inv_detJ
            val = sym.integrate(integrand, (X, -1, 1))
            
            K_e[r, s] = val
            K_e[s, r] = K_e[r, s]
    return K_e

def assemble(nodes, elements, phi, f, symbolic=True, matrix_function=element_matrix):
    N_n, N_e = len(nodes), len(elements)
    if symbolic:
        A = sym.zeros(N_n, N_n)
        b = sym.zeros(N_n, 1)
    else:
        A = np.zeros((N_n, N_n), dtype=object)
        b = np.zeros(N_n, dtype=object)
    for e in range(N_e):
        Omega_e = [nodes[elements[e][0]], nodes[elements[e][-1]]]
        A_e = matrix_function(phi, Omega_e, symbolic=symbolic)
        
        # Only compute load vector if f is provided (not None)
        if f is not None:
            b_e = element_vector(f, phi, Omega_e, symbolic=symbolic)
        else:
            b_e = sym.zeros(len(phi), 1) if symbolic else np.zeros(len(phi), dtype=object)

        for r in range(len(elements[e])):
            for s in range(len(elements[e])):
                A[elements[e][r], elements[e][s]] += A_e[r, s]
            if f is not None:
                b[elements[e][r]] += b_e[r]
    return A, b
def compute_solution(A,b,symbolic=True):
    if symbolic:
        c=A.LUsolve(b)
    else:
        if hasattr(A, 'dtype') and A.dtype == object:
            A_sym = sym.Matrix(A)
            b_sym = sym.Matrix(b)
            c = A_sym.LUsolve(b_sym)
            c = np.array(c).flatten()
        else:
            c=np.linalg.solve(A,b)
    return c

    
    