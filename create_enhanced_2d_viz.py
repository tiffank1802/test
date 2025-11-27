"""
Créer une version améliorée de mesh_interactive_2d.html avec galerie d'images
"""
import plotly.graph_objects as go
from dolfinx import mesh
from mpi4py import MPI
import numpy as np
import base64
import os

def image_to_base64(image_path):
    """Convertir une image en base64 pour l'inclure dans le HTML"""
    if os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return None

def create_enhanced_2d_mesh_html():
    """Créer un maillage 2D interactif avec galerie d'images"""
    
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
    
    # Générer le HTML de base de Plotly
    plotly_html = fig.to_html(include_plotlyjs='cdn', div_id='plotly-div')
    
    # Liste des images à inclure
    images = [
        {
            'path': 'mesh_2d_rectangle.png',
            'title': 'Maillage 2D Rectangle',
            'description': 'Maillage 2D avec nœuds visibles'
        },
        {
            'path': 'mesh_2d_detailed.png',
            'title': 'Vue Détaillée',
            'description': 'Vue complète et zoom sur une région'
        },
        {
            'path': 'mesh_2d_numbered.png',
            'title': 'Maillage Numéroté',
            'description': 'Numéros de cellules et nœuds affichés'
        },
        {
            'path': 'mesh_anatomy_2x2.png',
            'title': 'Anatomie du Maillage',
            'description': 'Structure détaillée d\'un maillage 2×2'
        },
        {
            'path': 'mesh_refinement_comparison.png',
            'title': 'Comparaison Raffinements',
            'description': 'Effet du nombre d\'éléments (2×2 à 16×16)'
        },
        {
            'path': 'mesh_element_types.png',
            'title': 'Types d\'Éléments',
            'description': 'Triangles vs Quadrilatères'
        },
        {
            'path': 'mesh_quality_analysis.png',
            'title': 'Analyse de Qualité',
            'description': 'Rapport d\'aspect et angles minimaux'
        },
        {
            'path': 'viewer_mesh_full.png',
            'title': 'Vue Complète',
            'description': 'Maillage complet avec tous les détails'
        },
        {
            'path': 'viewer_mesh_zoom.png',
            'title': 'Vue Zoomée',
            'description': 'Détails d\'une région spécifique'
        }
    ]
    
    # Convertir les images en base64
    images_base64 = []
    for img_info in images:
        img_b64 = image_to_base64(img_info['path'])
        if img_b64:
            images_base64.append({
                'data': img_b64,
                'title': img_info['title'],
                'description': img_info['description']
            })
    
    # Créer le HTML complet avec galerie
    html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Maillage 2D Interactif - FEniCS</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        h1 {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            font-size: 2.5em;
        }}
        
        .plotly-container {{
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 40px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        }}
        
        .gallery-title {{
            color: white;
            font-size: 2em;
            margin: 40px 0 20px 0;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }}
        
        .gallery-item {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .gallery-item:hover {{
            transform: translateY(-8px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }}
        
        .gallery-item img {{
            width: 100%;
            height: 250px;
            object-fit: contain;
            background: white;
            padding: 10px;
        }}
        
        .gallery-item-info {{
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .gallery-item-title {{
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        
        .gallery-item-description {{
            font-size: 0.9em;
            opacity: 0.9;
            line-height: 1.4;
        }}
        
        .modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.9);
            overflow: auto;
        }}
        
        .modal-content {{
            margin: 2% auto;
            display: block;
            max-width: 95%;
            max-height: 90vh;
            object-fit: contain;
        }}
        
        .close {{
            position: absolute;
            top: 20px;
            right: 40px;
            color: #f1f1f1;
            font-size: 50px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }}
        
        .close:hover {{
            color: #bbb;
        }}
        
        .modal-caption {{
            text-align: center;
            color: #ccc;
            padding: 20px;
            font-size: 1.2em;
        }}
        
        .back-button {{
            display: inline-block;
            background: white;
            color: #667eea;
            padding: 12px 30px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: bold;
            margin: 20px;
            transition: all 0.3s;
        }}
        
        .back-button:hover {{
            background: #667eea;
            color: white;
            transform: scale(1.05);
        }}
        
        .info-box {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .info-box h3 {{
            margin-top: 0;
            color: white;
        }}
        
        @media (max-width: 768px) {{
            .gallery {{
                grid-template-columns: 1fr;
            }}
            
            h1 {{
                font-size: 1.8em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-button">← Retour à l'accueil</a>
        
        <h1>🔬 Maillage 2D Interactif</h1>
        
        <div class="info-box">
            <h3>📊 Visualisation Interactive</h3>
            <p>Cette visualisation montre un maillage 2D triangulaire généré avec FEniCS/DOLFINx. 
            Utilisez votre souris pour zoomer et explorer le maillage. Survolez les nœuds pour voir leurs coordonnées.</p>
            <ul>
                <li><strong>Éléments:</strong> 400 triangles</li>
                <li><strong>Nœuds:</strong> 231 sommets</li>
                <li><strong>Type:</strong> Maillage structuré triangulaire</li>
            </ul>
        </div>
        
        <div class="plotly-container">
            {plotly_html}
        </div>
        
        <h2 class="gallery-title">📸 Galerie d'Images - Visualisations Complémentaires</h2>
        
        <div class="info-box">
            <h3>ℹ️ À propos de cette galerie</h3>
            <p>Voici différentes visualisations du maillage 2D montrant divers aspects techniques et pédagogiques. 
            Cliquez sur une image pour la voir en grand.</p>
        </div>
        
        <div class="gallery">
"""
    
    # Ajouter les images à la galerie
    for idx, img in enumerate(images_base64):
        html_content += f"""
            <div class="gallery-item" onclick="openModal({idx})">
                <img src="data:image/png;base64,{img['data']}" alt="{img['title']}">
                <div class="gallery-item-info">
                    <div class="gallery-item-title">{img['title']}</div>
                    <div class="gallery-item-description">{img['description']}</div>
                </div>
            </div>
"""
    
    html_content += """
        </div>
    </div>
    
    <!-- Modal pour afficher les images en grand -->
    <div id="imageModal" class="modal" onclick="closeModal()">
        <span class="close">&times;</span>
        <img class="modal-content" id="modalImg">
        <div class="modal-caption" id="modalCaption"></div>
    </div>
    
    <script>
        // Données des images
        const images = [
"""
    
    # Ajouter les données des images pour JavaScript
    for idx, img in enumerate(images_base64):
        comma = "," if idx < len(images_base64) - 1 else ""
        html_content += f"""
            {{
                src: 'data:image/png;base64,{img['data']}',
                title: '{img['title']}',
                description: '{img['description']}'
            }}{comma}
"""
    
    html_content += """
        ];
        
        function openModal(index) {
            const modal = document.getElementById('imageModal');
            const modalImg = document.getElementById('modalImg');
            const caption = document.getElementById('modalCaption');
            
            modal.style.display = 'block';
            modalImg.src = images[index].src;
            caption.innerHTML = `<strong>${images[index].title}</strong><br>${images[index].description}`;
        }
        
        function closeModal() {
            document.getElementById('imageModal').style.display = 'none';
        }
        
        // Fermer avec Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeModal();
            }
        });
    </script>
</body>
</html>
"""
    
    # Sauvegarder le fichier
    with open('mesh_interactive_2d.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✓ Fichier mesh_interactive_2d.html créé avec galerie d'images")
    print(f"  - {len(images_base64)} images incluses")
    print("  - Visualisation Plotly interactive")
    print("  - Galerie modale cliquable")

if __name__ == "__main__":
    create_enhanced_2d_mesh_html()
