"""
Méthode 3: Serveur HTTP simple pour afficher les images
Génère les images puis crée une page HTML pour les visualiser
"""
from dolfinx import mesh
from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt
import http.server
import socketserver
import os
import webbrowser
from threading import Thread

def create_mesh_plots():
    """Crée plusieurs plots de maillage"""
    # Créer un maillage
    domain = mesh.create_rectangle(
        MPI.COMM_WORLD,
        [np.array([0, 0]), np.array([2, 1])],
        [20, 10],
        mesh.CellType.triangle
    )
    
    points = domain.geometry.x
    cells = domain.geometry.dofmap
    
    # Plot 1: Vue complète
    fig, ax = plt.subplots(figsize=(12, 6))
    for cell_idx in range(len(cells)):
        cell_vertices = cells[cell_idx]
        vertices = np.append(cell_vertices, cell_vertices[0])
        ax.plot(points[vertices, 0], points[vertices, 1], 'b-', linewidth=0.5)
    ax.plot(points[:, 0], points[:, 1], 'ro', markersize=2)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Maillage complet')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    plt.savefig('viewer_mesh_full.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    # Plot 2: Zoom
    fig, ax = plt.subplots(figsize=(12, 6))
    for cell_idx in range(len(cells)):
        cell_vertices = cells[cell_idx]
        vertices = np.append(cell_vertices, cell_vertices[0])
        ax.plot(points[vertices, 0], points[vertices, 1], 'b-', linewidth=1.5)
    ax.plot(points[:, 0], points[:, 1], 'ro', markersize=4)
    ax.set_xlim(0, 0.5)
    ax.set_ylim(0, 0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Zoom sur une région')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    plt.savefig('viewer_mesh_zoom.png', dpi=150, bbox_inches='tight')
    plt.close()

def create_html_viewer():
    """Crée une page HTML pour visualiser les images"""
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Visualiseur de Maillages FEniCS</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .image-container {
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 10px auto;
        }
        h2 {
            color: #555;
            margin-top: 0;
        }
        .info {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1>🔬 Visualiseur de Maillages FEniCS</h1>
    
    <div class="info">
        <strong>Serveur local démarré avec succès!</strong><br>
        Les images se rafraîchissent automatiquement. Relancez le script pour mettre à jour.
    </div>
    
    <div class="image-container">
        <h2>📊 Vue complète du maillage</h2>
        <img src="viewer_mesh_full.png" alt="Maillage complet">
    </div>
    
    <div class="image-container">
        <h2>🔍 Vue zoomée</h2>
        <img src="viewer_mesh_zoom.png" alt="Maillage zoomé">
    </div>
    
    <div class="info">
        <p><strong>Instructions:</strong></p>
        <ul>
            <li>Utilisez Ctrl+C dans le terminal pour arrêter le serveur</li>
            <li>Relancez le script pour générer de nouvelles images</li>
            <li>Rafraîchissez cette page (F5) pour voir les mises à jour</li>
        </ul>
    </div>
</body>
</html>
"""
    with open('viewer.html', 'w') as f:
        f.write(html_content)

def start_server(port=8000):
    """Démarre un serveur HTTP simple"""
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"\n{'='*60}")
        print(f"🌐 Serveur HTTP démarré sur le port {port}")
        print(f"📱 Ouvrez votre navigateur à: http://localhost:{port}/viewer.html")
        print(f"{'='*60}\n")
        print("Appuyez sur Ctrl+C pour arrêter le serveur\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✓ Serveur arrêté proprement")
            httpd.shutdown()

if __name__ == "__main__":
    print("Génération des images du maillage...")
    create_mesh_plots()
    print("✓ Images créées")
    
    print("Création de la page HTML...")
    create_html_viewer()
    print("✓ Page HTML créée")
    
    start_server(8000)
