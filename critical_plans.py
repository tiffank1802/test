import numpy as np
from random import choice
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def deviatoric(tensor):
    """
    Calculates the deviatoric part of a tensor.
    This removes the hydrostatic (volume-changing) component.
    """
    return tensor - np.trace(tensor)/3 * np.eye(3)

def tresca_norm(tensor):
    """
    Computes the Tresca norm of a tensor, defined as the difference
    between the maximum and minimum eigenvalues. This is related to the
    maximum shear stress in a material.
    """
    eigs = np.linalg.eigvalsh(tensor)
    return max(eigs) - min(eigs)

def distance(eps1, eps2):
    """
    Calculates the 'distance' between two tensors using the Tresca norm
    of their difference.
    """
    return tresca_norm(eps1 - eps2)

def compute_diameter(E):
    """
    Finds the diameter of a set of tensors E, which is the maximum
    Tresca distance between any two tensors in the set. This function uses
    an iterative algorithm to find the pair(s) of tensors that define this diameter.
    """
    if len(E) < 2:
        return None, 0
    Ecurr = list(E)
    eps_i = choice(Ecurr)
    max_dist = 0
    diameter = None
    stop = False
    while not stop:
        dists = [distance(eps_i, eps) for eps in Ecurr]
        k = np.argmax(dists)
        eps_k = Ecurr[k]
        dist_ik = dists[k]
        if dist_ik > max_dist:
            diameter = (eps_i, eps_k)
            max_dist = dist_ik
        if diameter is None:
            break
        p, q = diameter
        m = (p + q) / 2
        r = max_dist / 2
        to_keep = []
        for eps in Ecurr:
            d = distance(eps, m)
            if d >= r:
                to_keep.append(eps)
        Ecurr = to_keep
        remaining = [eps for eps in Ecurr if not np.allclose(eps, p) and not np.allclose(eps, q)]
        if len(remaining) > 0:
            dists_m = [distance(eps, m) for eps in Ecurr]
            new_k = np.argmax(dists_m)
            eps_i = Ecurr[new_k]
        else:
            stop = True
    p, q = diameter
    m = (p + q)/2
    r = max_dist / 2
    Eout = [eps for eps in E if distance(eps, m) >= r]
    Eout_without_diam = [eps for eps in Eout if not np.allclose(eps, p) and not np.allclose(eps, q)]
    if len(Eout_without_diam) == 0:
        return [(p, q)], max_dist
    else:
        list_diameters = []
        current_max = max_dist
        for eps_k in Eout:
            for eps_l in E:
                if np.allclose(eps_k, eps_l):
                    continue
                d_kl = distance(eps_k, eps_l)
                if d_kl > current_max:
                    current_max = d_kl
                    list_diameters = [(eps_k, eps_l)]
                elif np.isclose(d_kl, current_max):
                    list_diameters.append((eps_k, eps_l))
        return list_diameters, current_max

def get_critical_planes(eps1, eps2):
    """
    Calculates the normal vectors of the critical planes.
    These planes correspond to the planes of maximum shear stress range,
    determined from the eigenvectors of the difference tensor between
    the two most distant strain states.
    """
    delta = eps1 - eps2
    eigs, vecs = np.linalg.eigh(delta)
    idx = np.argsort(eigs)
    v3 = vecs[:, idx[0]]
    v1 = vecs[:, idx[2]]
    n1 = (v1 + v3) / np.linalg.norm(v1 + v3)
    n2 = (v1 - v3) / np.linalg.norm(v1 - v3)
    return n1, n2

def plot_plane(ax, n, color='b', alpha=0.2, size=1):
    """Helper function to plot a 3D plane given its normal vector 'n'."""
    if np.abs(n[0]) > 0.1:
        v1 = np.array([-n[1], n[0], 0])
    else:
        v1 = np.array([0, -n[2], n[1]])
    v1 = v1 / np.linalg.norm(v1) if np.linalg.norm(v1) > 0 else v1
    v2 = np.cross(n, v1)
    v2 = v2 / np.linalg.norm(v2) if np.linalg.norm(v2) > 0 else v2
    u, v = np.meshgrid(np.linspace(-size, size, 10), np.linspace(-size, size, 10))
    points = u[..., np.newaxis] * v1 + v[..., np.newaxis] * v2
    x = points[..., 0]
    y = points[..., 1]
    z = points[..., 2]
    ax.plot_surface(x, y, z, color=color, alpha=alpha)

def plot_critical_planes(n1, n2):
    """
    Creates and saves a 3D plot visualizing the two critical planes
    and their normal vectors.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Plot planes
    plot_plane(ax, n1, 'blue', 0.3, 1)
    plot_plane(ax, n2, 'red', 0.3, 1)
    # Plot normals
    ax.quiver(0, 0, 0, n1[0], n1[1], n1[2], color='blue', label='n1', length=1.5, arrow_length_ratio=0.2)
    ax.quiver(0, 0, 0, n2[0], n2[1], n2[2], color='red', label='n2', length=1.5, arrow_length_ratio=0.2)
    ax.set_xlim([-1.5, 1.5])
    ax.set_ylim([-1.5, 1.5])
    ax.set_zlim([-1.5, 1.5])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()
    plt.savefig('critical_planes.png')
    print("Saved plot to 'critical_planes.png'")
    plt.close()

def generate_strains(num_points=1000):
    """
    Generates a sample non-proportional, multiaxial strain history
    for demonstration purposes.
    """
    t = np.linspace(0, 1, num_points, endpoint=False)
    eps11 = 0.005 * np.cos(3 * np.pi * t)
    eps22 = -0.001 * np.cos(2 * np.pi * t)
    eps33 = 0.0075 * np.cos(4 * np.pi * t)
    eps12 = -0.002 * np.cos(5 * np.pi * t)
    eps = []
    for i in range(num_points):
        mat = np.array([[eps11[i], eps12[i], 0],
                        [eps12[i], eps22[i], 0],
                        [0, 0, eps33[i]]])
        dev = deviatoric(mat)
        eps.append(dev)
    return eps

# --- Main execution block ---

# 1. Generate a simulated history of strain tensors
E = generate_strains()

# 2. Find the diameter of the strain path, which corresponds to the
#    maximum shear strain range experienced by the material.
diameters, max_d = compute_diameter(E)

# 3. Calculate a fatigue parameter (half of the max shear strain range)
delta_gamma_over_2_percent = (max_d / 2) * 100

# 4. For each pair of points that form the diameter, calculate and
#    visualize the critical planes.
for pair in diameters:
    n1, n2 = get_critical_planes(pair[0], pair[1])
    print("Critical planes normals:")
    print(np.round(n1, 4))
    print(np.round(n2, 4))
    plot_critical_planes(n1, n2)

# 5. Print the calculated fatigue parameter.
print("Delta gamma / 2 (%):", round(delta_gamma_over_2_percent, 3))