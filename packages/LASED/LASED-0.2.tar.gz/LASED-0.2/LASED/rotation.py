'''
This is a file to define functions for rotating density matrices in the QED simulation of
a laser-atom system.
Author: Manish Patel
Date created: 12/05/2021
'''

from density_matrix import *
import numpy as np
import math
import copy

def wigner_D(J, alpha, beta, gamma):
    '''
    Calculates the Wigner D-matrix for rotation by Eueler angles (alpha, beta, gamma).
    Inputs:
        J: total angular momentum quantum number of the state which will be rotated with the 
        resulting D-matrix
        alpha: rotation around z-axis
        beta: rotation about the y'-axis
        gamma: rotation about the z''-axis
    Returns:
        A square matrix of size 2J+1
    '''
    size = 2*J+1  # Number of sub-states
    m = np.linspace(-J, J, size, dtype=int)  # Projections of J
    D = np.zeros((size, size), dtype = np.complex)  # Set up D-matrix
    for i, mp in enumerate(m):
        for j, mpp in enumerate(m):
            alpha_const = math.cos(-mp*alpha)+1.j*math.sin(-mp*alpha)
            gamma_const = math.cos(-mpp*gamma)+1.j*math.sin(-mpp*gamma)
            D[i, j] = alpha_const*small_Wigner_D(J, beta, mp, mpp)*gamma_const
    return D

def small_Wigner_D(J, beta, mp, m):
    '''
    Calculates the small Wigner D-matrix elements for rotation by Euler angles (alpha, beta, gamma)
    '''
    const = np.sqrt((math.factorial(J+mp))*math.factorial(J-mp)*math.factorial(J+m)*math.factorial(J-m))
    d_sum = 0
    # Define limits so sum does not contain negative factorials
    s_max = min(J+m, J-mp)
    s_min = max(0, m-mp)
    sum_index = np.linspace(s_min, s_max, )
    for s in range(s_min, s_max+1):  # Have to go to s_max+1 or will miss out on the s_max value
        numerator = np.power(-1, mp - m + s)*np.power(math.cos(beta/2), 2*J+m-mp-2*s)*np.power(math.sin(beta/2), mp-m+2*s)
        denominator = math.factorial(J+m-s)*math.factorial(s)*math.factorial(mp-m+s)*math.factorial(J-mp-s)
        d_sum += numerator/denominator
    
    return const*d_sum

'''
Rotates a density matrix by the wigner D-matrix determined by Euler angles (alpha, beta, gamma).
(rho_newframe) = (D)(rho)(D*). The z-y-z convention is used where alpha rotates around the z-axis,
then beta rotates around the new y-axis, and gamma rotates around the new z-axis
'''
def rotation(rho, J, alpha, beta, gamma):
    D_matrix = np.transpose(wigner_D(J, alpha, beta, gamma))
    D_conj = np.transpose(np.conj(D_matrix))
    return np.dot(D_matrix, np.dot(rho, D_conj))


'''
Rotate the excited and ground state populations by the Euler angles alpha, beta, gamma
'''
def rotateInitialMatrix(flat_rho, n, E, G, alpha, beta, gamma):
    # Make a copy to return
    rotated_rho = copy.deepcopy(flat_rho)
    # Rotate the excited state populations and atomic coherences
    J_E = JNumber(E)
    rotated_excited_rho = rotation(getSingleStateMatrix(rotated_rho, n, E), J_E, alpha, beta, gamma)
    appendDensityMatrixToFlatCoupledMatrix(rotated_rho, rotated_excited_rho, E, n)
    
    # Rotate the ground state populations and atomic coherences
    J_G = JNumber(G)
    rotated_ground_rho = rotation(getSingleStateMatrix(rotated_rho, n, G), J_G, alpha, beta, gamma)
    appendDensityMatrixToFlatCoupledMatrix(rotated_rho, rotated_ground_rho, G, n)
    
    return rotated_rho