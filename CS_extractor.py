import trimesh
import numpy as np 
import polyscope as ps
from pygel3d import hmesh, graph 

MESH_PATH = "./meshes/arissa_0.obj"

def get_cs(filename):
	mesh = hmesh.load(filename)
	graph_from_mesh = graph.from_mesh(mesh)
	curve_skeleton, cs_corresp = graph.LS_skeleton_and_map(graph_from_mesh)
	print("\n")
	print(f"Shape of curve_skeleton: {type(curve_skeleton)}, shape of cs_corresp: {type(cs_corresp)}")

	# get the joints of the curve skeleton
	gel_joints = curve_skeleton.positions()
	joints = gel_joints.shape[0] # joints = 160 [shape(160,3)]
	print(f"joint shape: {gel_joints.shape}, total joints: {gel_joints.shape[0]}, type: {type(gel_joints)}")


	cs_corresp = np.array(cs_corresp).shape[0] # shape = (2455, )
	print(f"corresp shape: {cs_corresp}, type: {type(cs_corresp)}")

	# converting the joints in a np array
	gel_joints = np.array(gel_joints)
	print(f"Type of GEL joints: {type(gel_joints)}")

	# getting the edges
	all_edges = []
	for j1 in range(joints):
		edges = curve_skeleton.neighbors(j1)
		# all_edges.append(edges)
		# print(f"Edges in the curve_skeleton are: {edges}")
		for j2 in edges:
			all_edges.append((j1, j2))

	all_edges = np.array(all_edges)
	# print(final_edges)
	print(f"Type of the Egdes: {type(all_edges)}, shape: {all_edges.shape}")

	return all_edges, gel_joints



get_cs(MESH_PATH)



def load_mesh(filename):
	mesh = trimesh.load_mesh(filename)
	vertices = mesh.vertices
	faces = mesh.faces
	all_edges, gel_joints = get_cs(MESH_PATH)


	ps.init()

	ps.register_curve_network("Vertices", gel_joints, all_edges)

	ps.show()

load_mesh(MESH_PATH)


def test_func():
	ps.init()
	nodes = np.random.rand(100, 3)
	edges = np.random.randint(0, 100, size=(250,2))

	# visualize!
	ps_net = ps.register_curve_network("my network", nodes, edges)
	ps.show()

# test_func()