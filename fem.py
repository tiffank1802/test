from test import *
# f1=sym.sin(.5*sym.pi*x)
# f2=sym.sin(2*sym.pi*x)
# phi=4*f1-.5*f2
# xcoor=np.linspace(0,4,401)
# F1=sym.lambdify([x],f1)
# F2=sym.lambdify([x],f2)
# PHI=sym.lambdify([x],phi)
# plt.plot(xcoor,F1(xcoor))
# plt.plot(xcoor,F2(xcoor))
# plt.plot(xcoor,PHI(xcoor))
# plt.legend(['$\\psi_1$','$\\psi_2$','u=$4\\psi_1-0.5\\psi_2$'])
# plt.savefig('symbolic_vs_numeric.pdf')
# plt.close()

nodes = [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1.0]
elements = [[0, 1, 2], [2, 3, 4], [4, 5, 6], [6, 7, 8]]
i=1
x=sym.Symbol('x')
p=[]
num = 0  # Initialize counter outside loop

for e in elements:
    points = [nodes[e[i]] for i in range(3)]
    p_elem = [Lagrange_polynomials(x, i, points) for i in range(3)]
    xx = np.linspace(points[0], points[2], 101)  # Use element's actual range
    P0 = sym.lambdify([x], p_elem[0])
    P1 = sym.lambdify([x], p_elem[1])
    P2 = sym.lambdify([x], p_elem[2])
    
    plt.subplot(2, 2, num+1)  # Create subplot for current element
    plt.plot(xx, P0(xx), label='$\\phi_{}$'.format(e[0]))
    plt.plot(xx, P1(xx), label='$\\phi_{}$'.format(e[1]))
    plt.plot(xx, P2(xx), label='$\\phi_{}$'.format(e[2]))
    plt.legend()
    plt.title('Element {}'.format(num))
    plt.xlabel('x')
    plt.ylabel('$\\phi_i(x)$')
    plt.grid()
    num += 1
plt.suptitle('Lagrange basis functions for all elements')  # Add main title
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust subplot spacing, leave room for suptitle
plt.savefig('lagrange_basis_all_elements.pdf')
plt.close()