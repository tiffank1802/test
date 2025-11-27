from fe_appprox1D import *


# phi=basis(d=1, symbolic=True)
# print(phi)
# Omega_e=[.1,.2]
# A_e=element_matrix(phi,Omega_e=Omega_e,symbolic=False)
# print(A_e)

h,x=sym.symbols('h x')
nodes=[0,h,2*h]
elements=[[0,1],[1,2]]
phi=basis(d=1,symbolic=False)
f=x*(1-x)
A,b=assemble(nodes,elements,phi,f,symbolic=False)
c=compute_solution(A,b,symbolic=False)
print(b)