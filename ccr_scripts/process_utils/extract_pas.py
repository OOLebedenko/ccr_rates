import pandas as pd
import numpy as np
import os


def rotate_vector_clockwise(vector, axis, theta):
    # The Rodrigues' clockwise rotation
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    axis = axis / np.linalg.norm(axis, axis=0)
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    R = np.eye(3, 3) + sin_theta * K + (1 - cos_theta) * np.dot(K, K)
    rotated_vector = np.dot(vector, R)
    return rotated_vector


def extract_csa_c_z_axis(CO_vectors, C_CA_vectors, r_id, out_dir):
    # definition of the z-axis: perpendicular to peptide plane
    C_CA_vectors /= np.linalg.norm(C_CA_vectors, axis=1)[:, np.newaxis]
    CO_vectors /= np.linalg.norm(CO_vectors, axis=1)[:, np.newaxis]
    z_axis = np.cross(CO_vectors, C_CA_vectors, axis=1)
    pd.DataFrame(z_axis, columns=["x", "y", "z"]).to_csv(
        os.path.join(out_dir, "z", "{r_id}_z_axis.csv".format(r_id=r_id)), index=False)
    return z_axis


def extract_csa_c_x_axis(CO_vectors, csa_c_z_axis, r_id, out_dir):
    # # definition of the x-axis: 38 degrees from CN to CO (rotation around z-axis)
    # # it's equvalent clockwise rotation CO on 82 degrees around z-axis
    CO_vectors /= np.linalg.norm(CO_vectors, axis=1)[:, np.newaxis]
    theta = 82 * np.pi / 180
    x_axis = np.array(
        [rotate_vector_clockwise(vector, z_axis, theta) for vector, z_axis in zip(CO_vectors, csa_c_z_axis)])
    pd.DataFrame(x_axis, columns=["x", "y", "z"]).to_csv(
        os.path.join(out_dir, "x", "{r_id}_x_axis.csv".format(r_id=r_id)), index=False)
    return x_axis


def extract_csa_c_y_axis(CO_vectors, csa_c_z_axis, r_id, out_dir):
    # # definition of the y-axis: 128 degrees from CN to CO(rotation around z-axis)]
    # # it's equvalent clockwise rotation CO on -8 degrees around z-axis
    CO_vectors /= np.linalg.norm(CO_vectors, axis=1)[:, np.newaxis]
    theta = -8 * np.pi / 180
    y_axis = np.array(
        [rotate_vector_clockwise(vector, z_axis, theta) for vector, z_axis in zip(CO_vectors, csa_c_z_axis)])
    pd.DataFrame(y_axis, columns=["x", "y", "z"]).to_csv(
        os.path.join(out_dir, "y", "{r_id}_y_axis.csv".format(r_id=r_id)), index=False)
    return y_axis
