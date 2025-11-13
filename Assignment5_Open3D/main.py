import time
import numpy as np
import open3d as o3d

def show(obj_list, title="View", width=960, height=720, background="White"):
    if not isinstance(obj_list, list):
        obj_list = [obj_list]
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name=title, width=width, height=height)
    try:
        for o in obj_list:
            vis.add_geometry(o)
        opt = vis.get_render_option()

        # Choose background
        if background.lower() == "white":
            opt.background_color = np.array([1.0, 1.0, 1.0])
        elif background.lower() == "light":
            opt.background_color = np.array([0.9, 0.9, 0.9])
        else:
            opt.background_color = np.array([0.03, 0.03, 0.03])

        opt.mesh_show_back_face = True
        opt.light_on = False
        opt.point_size = 2.0
        vis.run()
    finally:
        vis.destroy_window()
        time.sleep(0.12)

# --- Header ---
print("Data Visualization Assignment #5 — Open3D Project")
print("Author: Ziaulhaq Parsa")
print("Model: IronMan.obj\n")

# ===== Step 1: Load and visualize the model =====
mesh = o3d.io.read_triangle_mesh("IronMan/IronMan.obj")
show(mesh, "Step 1: Original Model")
print("STEP 1: Loading and Visualization")
print("Vertices:", len(mesh.vertices))
print("Triangles:", len(mesh.triangles))
print("Has colors:", mesh.has_vertex_colors())
print("Has normals:", mesh.has_vertex_normals())

# ===== Step 2: Convert to point cloud (with extra info) =====
pcd = mesh.sample_points_uniformly(number_of_points=50000)
# estimate normals for point cloud (needed later and useful to report)
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))

# bounding box and basic stats
bbox_pcd = pcd.get_axis_aligned_bounding_box()
min_bound = bbox_pcd.min_bound
max_bound = bbox_pcd.max_bound
extent = bbox_pcd.get_extent()

show(pcd, "Step 2: Point Cloud (sampled)")
print("\nSTEP 2: Conversion to Point Cloud")
print("Points:", len(pcd.points))
print("Has colors:", pcd.has_colors())
print("Has normals:", pcd.has_normals())
print("Normals count:", len(pcd.normals))
print("Point cloud bounding box min:", min_bound)
print("Point cloud bounding box max:", max_bound)
print("Point cloud extent (x,y,z):", extent)

# ===== Step 3: Surface reconstruction (Poisson) =====
# ensure normals are available for Poisson
if not pcd.has_normals():
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
mesh_recon, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=9)
bbox = mesh_recon.get_axis_aligned_bounding_box()
mesh_crop = mesh_recon.crop(bbox)
show(mesh_crop, "Step 3: Surface Reconstruction")
print("\nSTEP 3: Surface Reconstruction")
print("Vertices:", len(mesh_crop.vertices))
print("Triangles:", len(mesh_crop.triangles))
print("Has colors:", mesh_crop.has_vertex_colors())

# ===== Step 4: Voxelization (with extra info) =====
voxel_size = 0.05
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=voxel_size)
show(voxel_grid, "Step 4: Voxelization")
voxels = voxel_grid.get_voxels()
print("\nSTEP 4: Voxelization")
print("Voxel size used:", voxel_size)
print("Approx. voxels (occupied):", len(voxels))
# show sample voxel grid indices (first 8) for quick verification
sample_indices = [v.grid_index for v in voxels[:8]]
print("Sample voxel grid indices (first 8):", sample_indices)
# bounding box of voxel grid (constructed from the pcd bbox)
bbox_vox = voxel_grid.get_axis_aligned_bounding_box()
print("Voxel grid bounding box min:", bbox_vox.min_bound)
print("Voxel grid bounding box max:", bbox_vox.max_bound)

# ===== Step 5: Add a plane =====
plane = o3d.geometry.TriangleMesh.create_box(width=2, height=0.01, depth=2)
plane.translate((0, -0.5, 0))
plane.paint_uniform_color([0.7, 0.7, 0.7])  # light gray plane (still visible on dark bg)
bbox_mesh = mesh_crop.get_axis_aligned_bounding_box()
bbox_mesh.color = (1, 0, 0)
show([mesh_crop, plane, bbox_mesh], "Step 5: Plane Added")
print("\nSTEP 5: Plane Added")

# ===== Step 6: Surface Clipping =====
points = np.asarray(pcd.points)
mask = points[:, 1] < 0  # keep points below plane (Y < 0)
clipped_pcd = o3d.geometry.PointCloud()
clipped_pcd.points = o3d.utility.Vector3dVector(points[mask])
# estimate normals for clipped cloud for better visualization later
if len(clipped_pcd.points) > 0:
    clipped_pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
show(clipped_pcd, "Step 6: Clipped Point Cloud")
print("\nSTEP 6: Surface Clipping")
print("Remaining vertices:", len(clipped_pcd.points))

# ===== Step 7: Color gradient + extremes =====
z_vals = np.asarray(clipped_pcd.points)[:, 2] if len(clipped_pcd.points) > 0 else np.array([])
if z_vals.size > 0:
    colors = (z_vals - z_vals.min()) / (z_vals.ptp() if z_vals.ptp() != 0 else 1.0)
    clipped_pcd.colors = o3d.utility.Vector3dVector(np.c_[colors, 0.5 * colors, 1 - colors])
    min_idx = np.argmin(z_vals)
    max_idx = np.argmax(z_vals)
    min_point = np.asarray(clipped_pcd.points)[min_idx]
    max_point = np.asarray(clipped_pcd.points)[max_idx]
    sphere_min = o3d.geometry.TriangleMesh.create_sphere(radius=0.05)
    sphere_min.translate(min_point)
    sphere_min.paint_uniform_color([1, 0, 0])
    sphere_max = o3d.geometry.TriangleMesh.create_sphere(radius=0.05)
    sphere_max.translate(max_point)
    sphere_max.paint_uniform_color([0, 1, 0])
    show([clipped_pcd, sphere_min, sphere_max], "Step 7: Gradient and Extremes")
    print("\nSTEP 7: Color and Extremes")
    print("Min point (Z):", min_point)
    print("Max point (Z):", max_point)
else:
    print("\nSTEP 7: No points in clipped cloud to compute gradient/extrema.")

# ===== Bonus: Animated color gradient (single window update, lighting off) =====
print("\nBONUS: Animated gradient (visual effect)")
if len(clipped_pcd.points) > 0:
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="Bonus Animation", width=960, height=720)
    try:
        vis.add_geometry(clipped_pcd)
        opt = vis.get_render_option()
        opt.background_color = np.array([0.02, 0.02, 0.02])
        opt.light_on = False
        try:
            opt.point_size = 2.0
        except Exception:
            pass
        for i in np.linspace(0, 1, 12):
            color_anim = np.c_[colors * i, 0.5 * colors, 1 - colors * i]
            clipped_pcd.colors = o3d.utility.Vector3dVector(color_anim)
            vis.update_geometry(clipped_pcd)
            vis.poll_events()
            vis.update_renderer()
            time.sleep(0.12)
    finally:
        vis.destroy_window()
        time.sleep(0.12)
else:
    print("BONUS: skipped animated gradient (no clipped points).")

# ===== Save outputs and final summary =====
o3d.io.write_triangle_mesh("output_step3_surface.ply", mesh_crop)
o3d.io.write_point_cloud("output_step2_pointcloud.ply", pcd)
o3d.io.write_voxel_grid("output_step4_voxels.ply", voxel_grid)

print("\n=== SUMMARY REPORT ===")
print(f"Original vertices: {len(mesh.vertices)}")
print(f"Point cloud points: {len(pcd.points)}")
print(f"Reconstructed triangles: {len(mesh_crop.triangles)}")
print(f"Voxel count: {len(voxel_grid.get_voxels())}")
print(f"Clipped vertices: {len(clipped_pcd.points)}")
if z_vals.size > 0:
    print(f"Z range: {min_point[2]:.2f} to {max_point[2]:.2f}")

