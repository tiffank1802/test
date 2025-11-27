"""
Méthode 4: Utiliser plotly pour des graphes interactifs dans le navigateur
Plotly génère des fichiers HTML interactifs
"""
import plotly.graph_objects as go
from dolfinx import mesh
from mpi4py import MPI
import numpy as np

def create_interactive_2d_mesh():
    """Crée un maillage 2D interactif avec Plotly"""
    # Créer un maillage
    domain = mesh.create_rectangle(
        MPI.COMM_WORLD,
        [np.array([0, 0]), np.array([2, 1])],
        [20, 10],
        mesh.CellType.triangle
    )
    
    points = domain.geometry.x
    cells = domain.geometry.dofmap
    
    # Créer la figure plotly
    fig = go.Figure()
    
    # Ajouter les arêtes des triangles
    for cell_idx in range(len(cells)):
        cell_vertices = cells[cell_idx]
        vertices = np.append(cell_vertices, cell_vertices[0])
        
        fig.add_trace(go.Scatter(
            x=points[vertices, 0],
            y=points[vertices, 1],
            mode='lines',
            line=dict(color='blue', width=0.5),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Ajouter les nœuds
    fig.add_trace(go.Scatter(
        x=points[:, 0],
        y=points[:, 1],
        mode='markers',
        marker=dict(color='red', size=3),
        name='Nœuds',
        hovertemplate='Nœud: (%{x:.3f}, %{y:.3f})<extra></extra>'
    ))
    
    # Mise en forme
    fig.update_layout(
        title='Maillage 2D Interactif (Plotly)',
        xaxis_title='x',
        yaxis_title='y',
        hovermode='closest',
        width=1200,
        height=600,
        showlegend=True,
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(scaleanchor="x", scaleratio=1, showgrid=True, gridcolor='lightgray')
    )
    
    # Sauvegarder en HTML
    fig.write_html('mesh_interactive_2d.html')
    print("✓ Fichier HTML interactif créé: mesh_interactive_2d.html")
    print("  Ouvrez ce fichier dans votre navigateur pour une visualisation interactive")
    
    # Optionnel: afficher dans le navigateur automatiquement
    # fig.show()  # Cette ligne ouvrirait le navigateur si disponible
    
    return fig

def create_interactive_3d_mesh():
    """Crée un maillage 3D interactif avec Plotly"""
    # Créer un maillage 3D
    domain = mesh.create_box(
        MPI.COMM_WORLD,
        [np.array([0, 0, 0]), np.array([1, 1, 1])],
        [5, 5, 5],
        mesh.CellType.tetrahedron
    )
    
    points = domain.geometry.x
    cells = domain.geometry.dofmap
    
    # Pour la 3D, on affiche juste les sommets et quelques arêtes
    fig = go.Figure()
    
    # Afficher les points
    fig.add_trace(go.Scatter3d(
        x=points[:, 0],
        y=points[:, 1],
        z=points[:, 2],
        mode='markers',
        marker=dict(
            size=3,
            color=points[:, 2],  # Colorer selon z
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="z")
        ),
        name='Nœuds',
        hovertemplate='(%{x:.2f}, %{y:.2f}, %{z:.2f})<extra></extra>'
    ))
    
    # Ajouter les arêtes de quelques cellules (sinon trop de lignes)
    num_cells_to_show = min(50, len(cells))
    for cell_idx in range(0, num_cells_to_show, 5):
        cell_vertices = cells[cell_idx]
        # Pour un tétraèdre, connecter les 4 sommets
        edges = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
        for edge in edges:
            v1, v2 = cell_vertices[edge[0]], cell_vertices[edge[1]]
            fig.add_trace(go.Scatter3d(
                x=[points[v1, 0], points[v2, 0]],
                y=[points[v1, 1], points[v2, 1]],
                z=[points[v1, 2], points[v2, 2]],
                mode='lines',
                line=dict(color='lightblue', width=1),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    fig.update_layout(
        title='Maillage 3D Interactif (Plotly)',
        scene=dict(
            xaxis_title='x',
            yaxis_title='y',
            zaxis_title='z',
            aspectmode='data'
        ),
        width=1000,
        height=800,
        showlegend=False
    )
    
    fig.write_html('mesh_interactive_3d.html')
    print("✓ Fichier HTML interactif créé: mesh_interactive_3d.html")
    print("  Ouvrez ce fichier dans votre navigateur (rotation 3D interactive!)")
    
    return fig

if __name__ == "__main__":
    print("Création des maillages interactifs avec Plotly...\n")
    
    create_interactive_2d_mesh()
    print()
    create_interactive_3d_mesh()
    
    print("\n" + "="*60)
    print("✓ Tous les fichiers HTML ont été créés!")
    print("="*60)
    print("\nAvantages de Plotly:")
    print("  • Zoom, pan, rotation (3D)")
    print("  • Info au survol de la souris")
    print("  • Export d'images depuis le navigateur")
    print("  • Pas besoin de serveur - juste ouvrir le HTML")
