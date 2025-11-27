"""
Génération de graphiques pour le cours sur l'interpolation
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange

def plot_lagrange_basis():
    """Visualiser les polynômes de base de Lagrange"""
    x = np.linspace(0, 1, 100)
    nodes = [0, 0.5, 1]  # 3 nœuds (quadratique)
    
    plt.figure(figsize=(10, 6))
    
    # Calcul manuel des bases pour n=2
    # L0 = (x-x1)(x-x2) / (x0-x1)(x0-x2)
    L0 = (x - 0.5) * (x - 1) / ((0 - 0.5) * (0 - 1))
    L1 = (x - 0) * (x - 1) / ((0.5 - 0) * (0.5 - 1))
    L2 = (x - 0) * (x - 0.5) / ((1 - 0) * (1 - 0.5))
    
    plt.plot(x, L0, 'r-', label='L₀(x) (Nœud 0)', linewidth=2)
    plt.plot(x, L1, 'g-', label='L₁(x) (Nœud 0.5)', linewidth=2)
    plt.plot(x, L2, 'b-', label='L₂(x) (Nœud 1)', linewidth=2)
    
    plt.plot(nodes, [1, 1, 1], 'ko', markersize=8)
    plt.plot(nodes, [0, 0, 0], 'ko', markersize=8, markerfacecolor='white')
    
    plt.title('Polynômes de base de Lagrange (Ordre 2)', fontsize=14)
    plt.xlabel('x')
    plt.ylabel('Lᵢ(x)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig('lagrange_basis.png', dpi=150, bbox_inches='tight')
    plt.close()

def plot_hermite_vs_lagrange():
    """Comparer Lagrange et Hermite"""
    x = np.linspace(0, 2*np.pi, 100)
    y_exact = np.sin(x)
    
    # Points de colocation (peu de points)
    nodes = np.linspace(0, 2*np.pi, 5)
    y_nodes = np.sin(nodes)
    
    # Lagrange (passe par les points)
    poly_lagrange = lagrange(nodes, y_nodes)
    y_lagrange = poly_lagrange(x)
    
    plt.figure(figsize=(12, 6))
    plt.plot(x, y_exact, 'k--', label='Fonction exacte (sin x)', linewidth=1.5, alpha=0.7)
    plt.plot(x, y_lagrange, 'b-', label='Interpolation de Lagrange', linewidth=2)
    plt.plot(nodes, y_nodes, 'ro', label='Points de colocation', zorder=5)
    
    # Illustration conceptuelle d'Hermite (tangentes)
    # On dessine des petites tangentes aux points
    scale = 0.5
    for xi, yi in zip(nodes, y_nodes):
        slope = np.cos(xi)
        dx = 0.4
        plt.arrow(xi-dx/2, yi-slope*dx/2, dx, slope*dx, 
                 color='green', width=0.03, head_width=0, alpha=0.6)
    
    # Hack pour la légende d'Hermite
    plt.plot([], [], 'g-', linewidth=4, alpha=0.6, label='Contraintes Hermite (Dérivées)')
    
    plt.title('Lagrange (Points) vs Hermite (Points + Tangentes)', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('interpolation_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()

def plot_runge_phenomenon():
    """Montrer les limites de Lagrange (Phénomène de Runge)"""
    def f(x): return 1 / (1 + 25 * x**2)
    
    x = np.linspace(-1, 1, 200)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, f(x), 'k-', linewidth=2, label='Fonction de Runge')
    
    # Lagrange ordre élevé
    for n in [5, 11]:
        nodes = np.linspace(-1, 1, n)
        y_nodes = f(nodes)
        poly = lagrange(nodes, y_nodes)
        plt.plot(x, poly(x), label=f'Lagrange N={n}')
        plt.plot(nodes, y_nodes, 'o', markersize=4)
        
    plt.ylim(-0.5, 1.5)
    plt.title('Limites de Lagrange: Phénomène de Runge', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('runge_phenomenon.png', dpi=150, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    print("Génération des graphiques d'interpolation...")
    plot_lagrange_basis()
    plot_hermite_vs_lagrange()
    plot_runge_phenomenon()
    print("✓ Images générées: lagrange_basis.png, interpolation_comparison.png, runge_phenomenon.png")
