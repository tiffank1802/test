import sympy as sym
import numpy as np
from numpy import linspace, tanh, pi, sin
import matplotlib.pyplot as plt
import scipy.integrate

def least_square(f, psi, Omega):
    N = len(psi) - 1
    A = sym.zeros(N + 1, N + 1)
    b = sym.zeros(N + 1, 1)
    x = sym.Symbol('x')
    for i in range(N + 1):
        for j in range(i, N + 1):
            A[i, j] = sym.integrate(psi[i] * psi[j], (x, Omega[0], Omega[1]))
            A[j, i] = A[i, j]  # Symmetric matrix
        b[i, 0] = sym.integrate(f * psi[i], (x, Omega[0], Omega[1]))
    c = A.LUsolve(b)
    u = 0
    for i in range(N + 1):
        u += c[i, 0] * psi[i]
    return u, c
def regression(f, psi, points):
    N = len(psi) - 1
    m = len(points)
    
    # Convert to numpy arrays for vectorized operations
    points = np.array(points)
    
    # Create lambda functions
    x = sym.Symbol('x')
    f_f = sym.lambdify([x], f, modules='numpy')
    psi_f = [sym.lambdify([x], psi[i], modules='numpy') for i in range(N + 1)]
    
    # Build psi_matrix properly - ensure all outputs are 1D arrays of the same length
    psi_matrix = np.zeros((m, N + 1))
    for i in range(N + 1):
        psi_val = psi_f[i](points)
        # Ensure we have a 1D array of the correct length
        if np.isscalar(psi_val):
            psi_matrix[:, i] = psi_val  # Broadcast scalar to all points
        else:
            psi_matrix[:, i] = psi_val.flatten()[:m]  # Take first m elements
    
    # Evaluate f at all points
    f_values = f_f(points)
    
    # Build normal equations: B = psi_matrix^T @ psi_matrix, d = psi_matrix^T @ f_values
    B = psi_matrix.T @ psi_matrix
    d = psi_matrix.T @ f_values.reshape(-1, 1)
    
    # Solve for coefficients
    c = np.linalg.solve(B, d)
    
    # Build approximation function
    u = sum(c[i, 0] * psi[i] for i in range(N + 1))
    
    return u, c

def comparison_plot(f, u, Omega, filename='tmp.pdf'):
    x = sym.Symbol('x')
    f_f = sym.lambdify([x], f, modules='numpy')
    u_f = sym.lambdify([x], u, modules='numpy')
    resolution = 401
    xcoor = linspace(Omega[0], Omega[1], resolution)
    exact = f_f(xcoor)
    approx = u_f(xcoor)
    
    plt.plot(xcoor, approx)
    plt.plot(xcoor, exact)
    plt.legend(['approximation', 'exact'])
    plt.savefig(filename)
    plt.close()

def traperzoidal(values, dx):
    return dx * (np.sum(values) - 0.5 * (values[0] + values[-1]))

def least_squares_numerical(f, psi, N, x, integration_method='scipy', orthogonal_basis=False):
    A = np.zeros((N + 1, N + 1))
    b = np.zeros(N + 1)
    Omega = [x[0], x[-1]]
    dx = x[1] - x[0]
    
    for i in range(N + 1):
        j_limit = i + 1 if orthogonal_basis else N + 1
        for j in range(i, j_limit):
            print('(%d,%d)' % (i, j))
            
            if integration_method == 'scipy':
                def integrand_ij(x_val):
                    return psi(x_val, i) * psi(x_val, j)
                A_ij = scipy.integrate.quad(integrand_ij, Omega[0], Omega[1], 
                                          epsabs=1e-9, epsrel=1e-9)[0]
            elif integration_method == 'sympy':
                def integrand_ij(x_val):
                    return psi(x_val, i) * psi(x_val, j)
                A_ij = scipy.integrate.quad(integrand_ij, Omega[0], Omega[1])[0]
            else:
                values = psi(x, i) * psi(x, j)
                A_ij = traperzoidal(values, dx)
            
            A[i, j] = A_ij
            if i != j:
                A[j, i] = A_ij
        
        # Compute b[i]
        if integration_method in ['scipy', 'sympy']:
            def integrand_b(x_val):
                return f(x_val) * psi(x_val, i)
            b_i = scipy.integrate.quad(integrand_b, Omega[0], Omega[1], 
                                     epsabs=1e-9, epsrel=1e-9)[0]
        else:
            values = f(x) * psi(x, i)
            b_i = traperzoidal(values, dx)
        b[i] = b_i
    



    # Solve for coefficients
    if orthogonal_basis:
        c = b / np.diag(A)
    else:
        c = np.linalg.solve(A, b)

def Lagrange_polynomials(x,i,points):
    p=1
    for k in range(len(points)):
        if k!=i:
            p*=(x-points[k])/(points[i]-points[k])
    return p

def Lagrange_polynomials_01(x,N):
    if isinstance(x,sym.Symbol):
        h= sym.Rational(1,N-1)
    else:
        h=1.0/(N-1)
    points=[i*h for i in range(N)]
    psi=[Lagrange_polynomials(x,i, points) for i in range(N)]
    return psi, points


    # Build the approximation function
    def u_func(x_vals):
        result = np.zeros_like(x_vals)
        for i in range(N + 1):
            result += c[i] * psi(x_vals, i)
        return result
    
    u = u_func(x)
    return u, c

def save_plot_to_file(x, exact_func, approx_values, filename='least_squares_approximation.pdf'):
    """Save the comparison plot to a file"""
    plt.figure(figsize=(10, 6))
    plt.plot(x, exact_func(x), 'b-', linewidth=2, label='Exact: tanh(x-pi)')
    plt.plot(x, approx_values, 'r--', linewidth=2, label='Approximation')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.title('Least Squares Approximation')
    plt.grid(True)
    
    # Save to file
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Plot saved as {filename}")
def interpolation(f, psi, points):
    N = len(psi) - 1
    A = sym.zeros(N+1, N+1)
    b = sym.zeros(N+1, 1)
    psi_sym = psi # save symbolic expression
    # Turn psi and f into Python functions
    x = sym.Symbol('x')
    psi = []
    for i in range(N+1):
        psi.append(sym.lambdify([x], psi_sym[i]))
    f_f = sym.lambdify([x], f)
    for i in range(N+1):
        for j in range(N+1):    
            A[i,j] = psi[j](points[i])
        b[i,0] = f_f(points[i])
    c = A.LUsolve(b)
    # c is a sympy Matrix object, turn to list
    c = [sym.simplify(c[i,0]) for i in range(c.shape[0])]
    u = sym.simplify(sum(c[i]*psi_sym[i] for i in range(N+1)))
    return u, c
# Test the function
def psi(x, i):
    return np.sin((i + 1) * x)

# Create sample data
# x = linspace(0, 2 * pi, 501)
# N = 10  # Reduced for better stability
# f_func = lambda x: tanh(x - pi)

# # Call the function - using trapezoidal method for array-based computation
# u, c = least_squares_numerical(f_func, psi, N, x, 
#                               integration_method='trapezoidal', 
#                               orthogonal_basis=False)

# # Save the plot to a file
# save_plot_to_file(x, f_func, u, 'least_squares_approximation.pdf')

# # You can also save in different formats
# save_plot_to_file(x, f_func, u, 'least_squares_approximation.png')  # PNG format
# save_plot_to_file(x, f_func, u, 'least_squares_approximation.jpg')  # JPG format

# print("Coefficients:", c)
# print("Plot has been saved to 'least_squares_approximation.pdf'")

x=sym.Symbol('x')
# f=10*(x-1)**2-1
# psi=[1,x]
# Omega=[1,2]
# m_values=[2-1,8-1,64-1]
# # Create m+3 points and use the inner m+1 points 
# for m in m_values:
#     points=np.linspace(Omega[0],Omega[1],m+3)[1:-1]
#     u,c=regression(f,psi,points)
#     filename='regression_m=%d.pdf'%m
#     comparison_plot(f,u,Omega,filename)
# x=0.5
# psi, points= Lagrange_polynomials_01(x,N=3)
# print(psi)
# print(points)

# for N in [2, 4, 5, 6, 8, 10, 12]:
#     f = x**2
#     psi, points = Lagrange_polynomials_01(x, N)
#     u=interpolation(f, psi, points)
#     comparison_plot(f, u, [0, 1], filename='interpolation_f=x^2_N=%d.pdf'%N)
# f = sym.sin(2*sym.pi*x)
# N=4
# f = sym.sin(2*sym.pi*x)
# psi, points = Lagrange_polynomials_01(x, N)
# Omega=[0, 1]
# u, c = least_square(f, psi, Omega)
# comparison_plot(f, u, Omega)
# u, c = interpolation(f, psi, points)
# comparison_plot(f, u, Omega)