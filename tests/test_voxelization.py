#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import json

import pytest
import numpy as np
from scipy.spatial import ConvexHull

import kanapy
from kanapy.voxelization import *
from kanapy.entities import Ellipsoid, Simulation_Box
from kanapy.initializations import RVEcreator
from kanapy.input_output import write_dump
from kanapy.packing import particle_generator

def test_points_in_convexHull():
    outer_points = np.array([[0.3215426810286406, 0.1678336189760208, -0.2203710966001927],
                             [0.2229772524190855, -
                                 0.4213242506806965, -0.1966818060695024],
                             [0.458374538420117, -0.09914027349943322, -
                                 0.2505798421339875],
                             [-0.4954086979808367, -
                                 0.3339869997780649, -0.3195065691317492],
                             [0.4615616439483703, 0.4665423151725366,
                                 0.1766835406205464],
                             [-0.4797380864431505, 0.0419809916447671, -
                                 0.4254776681079321],
                             [-0.3392973838740004, 0.4288679723896719, -
                                 0.01599531622230571],
                             [0.1667164640191164, 0.003605551555385444, -
                                 0.4014989499947977],
                             [-0.03621271768232132, 0.3728502838619522,
                                 0.4947140370446388],
                             [-0.3411871756810576, -
                                 0.3328629143842151, -0.4270033635450559],
                             [0.3544683273457627, -
                                 0.450828987127942, -0.0827870439577727],
                             [0.3978697768392692, -0.002667689232777493,
                                 0.1641431727112673],
                             [-0.245701439441835, 0.495905311308713, -
                                 0.3194406286994373],
                             [0.161352035739787, -0.1563404972258401,
                                 0.3852604361113724],
                             [0.07214279572678994, -0.4960366976410492,
                                 0.1112227161519441],
                             [0.3210853052521919, 0.4807189479290684,
                                 0.4433501688235907],
                             [0.2724846394476338, -0.3506708492996831,
                                 0.2750346518820475],
                             [-0.4926118841325975, -0.3279366743079728,
                                 0.3683135596740186],
                             [0.2459906458351674, 0.3647787136629026, -
                                 0.1641662355178652],
                             [0.2100642609503719, -0.4499717643018549, 0.3245569875692548]])

    test_points = np.array([[0.3688830163971363, -0.1831502133823468, -0.2056387967482571],
                            [-0.1712592515826777, -0.3542439228428937,
                                0.2223876390814666],
                            [-0.3309556113844324, -0.370961861099081,
                                0.2439994981922204],
                            [-0.1004397059794885, -0.09014152417903909, -
                                0.008600084584765189],
                            [0.053091190339151, 0.3036317017894533,
                                0.1380056861210668],
                            [-0.003168473023146823, -
                                0.2525299883005488, -0.27151530400991],
                            [-0.3577162826971303, -
                                0.1375644040643837, -0.04494194644032229],
                            [0.00714666676441833, 0.1140243407469469,
                                0.407090128778564],
                            [-0.4018510635028137, 0.08917494033386464, -
                                0.2367824197158054],
                            [0.3201855824516951, 0.359077846965825,
                                0.02136723140381946],
                            [0.1190541238701475, -0.05734495917087884,
                                0.2032677509852384],
                            [0.3862800354941562, 0.2085496142586224,
                                0.09336129957191763],
                            [0.1233572616459404, 0.265491605052251, 0.117400122450106],
                            [0.1438531872293476, -
                                0.2594872752758556, -0.2026374435076839],
                            [-0.141922976953837, -
                                0.2994764654892278, -0.3009570467294725],
                            [-0.1850859398814719, 0.2606059478228967,
                                0.004159106876849283],
                            [-0.09789466634196664, -
                                0.3156603563722785, -0.303610991503681],
                            [-0.1707163766685095, -
                                0.2301452446078371, -0.05112823569320907],
                            [-0.312260808713977, -0.1674135249735914,
                                0.2808831662692904],
                            [-0.1966306233747216, 0.2291105671125563, -0.3387042454804333]])

    hull = ConvexHull(outer_points, incremental=False)
    results = points_in_convexHull(test_points, hull)

    assert all(results) == True


@pytest.fixture
def dec_info():
    node_test = [[1., 0., 1.], [1., 0., 0.], [0., 0., 0.], [0., 0., 1.], [1., 1., 1.], [1., 1., 0.], [0., 1., 0.], 
             [0., 1., 1.], [2., 0., 1.], [2., 0., 0.], [2., 1., 1.], [2., 1., 0.], [3., 0., 1.], [3., 0., 0.], 
             [3., 1., 1.], [3., 1., 0.], [1., 2., 1.], [1., 2., 0.], [0., 2., 0.], [0., 2., 1.], [2., 2., 1.], 
             [2., 2., 0.], [3., 2., 1.], [3., 2., 0.], [1., 3., 1.], [1., 3., 0.], [0., 3., 0.], [0., 3., 1.],
             [2., 3., 1.], [2., 3., 0.], [3., 3., 1.], [3., 3., 0.], [1., 0., 2.], [0., 0., 2.], [1., 1., 2.], 
             [0., 1., 2.], [2., 0., 2.], [2., 1., 2.], [3., 0., 2.], [3., 1., 2.], [1., 2., 2.], [0., 2., 2.], 
             [2., 2., 2.], [3., 2., 2.], [1., 3., 2.], [0., 3., 2.], [2., 3., 2.], [3., 3., 2.], [1., 0., 3.], 
             [0., 0., 3.], [1., 1., 3.], [0., 1., 3.], [2., 0., 3.], [2., 1., 3.], [3., 0., 3.], [3., 1., 3.], 
             [1., 2., 3.], [0., 2., 3.], [2., 2., 3.], [3., 2., 3.], [1., 3., 3.], [0., 3., 3.], [2., 3., 3.], 
             [3., 3., 3.]]

    elmt_test = {1: [1, 2, 3, 4, 5, 6, 7, 8], 2: [9, 10, 2, 1, 11, 12, 6, 5], 3: [13, 14, 10, 9, 15, 16, 12, 11],
                 4: [5, 6, 7, 8, 17, 18, 19, 20], 5: [11, 12, 6, 5, 21, 22, 18, 17], 6: [15, 16, 12, 11, 23, 24, 22, 21],
                 7: [17, 18, 19, 20, 25, 26, 27, 28], 8: [21, 22, 18, 17, 29, 30, 26, 25], 9: [23, 24, 22, 21, 31, 32, 30, 29],
                 10: [33, 1, 4, 34, 35, 5, 8, 36], 11: [37, 9, 1, 33, 38, 11, 5, 35], 12: [39, 13, 9, 37, 40, 15, 11, 38],
                 13: [35, 5, 8, 36, 41, 17, 20, 42], 14: [38, 11, 5, 35, 43, 21, 17, 41], 15: [40, 15, 11, 38, 44, 23, 21, 43],
                 16: [41, 17, 20, 42, 45, 25, 28, 46], 17: [43, 21, 17, 41, 47, 29, 25, 45], 18: [44, 23, 21, 43, 48, 31, 29, 47],
                 19: [49, 33, 34, 50, 51, 35, 36, 52], 20: [53, 37, 33, 49, 54, 38, 35, 51], 21: [55, 39, 37, 53, 56, 40, 38, 54],
                 22: [51, 35, 36, 52, 57, 41, 42, 58], 23: [54, 38, 35, 51, 59, 43, 41, 57], 24: [56, 40, 38, 54, 60, 44, 43, 59],
                 25: [57, 41, 42, 58, 61, 45, 46, 62], 26: [59, 43, 41, 57, 63, 47, 45, 61], 27: [60, 44, 43, 59, 64, 48, 47, 63]}

    center_test = {1: (0.5, 0.5, 0.5), 2: (1.5, 0.5, 0.5), 3: (2.5, 0.5, 0.5), 4: (0.5, 1.5, 0.5),
                   5: (1.5, 1.5, 0.5), 6: (2.5, 1.5, 0.5), 7: (0.5, 2.5, 0.5), 8: (1.5, 2.5, 0.5),
                   9: (2.5, 2.5, 0.5), 10: (0.5, 0.5, 1.5), 11: (1.5, 0.5, 1.5), 12: (2.5, 0.5, 1.5),
                   13: (0.5, 1.5, 1.5), 14: (1.5, 1.5, 1.5), 15: (2.5, 1.5, 1.5), 16: (0.5, 2.5, 1.5),
                   17: (1.5, 2.5, 1.5), 18: (2.5, 2.5, 1.5), 19: (0.5, 0.5, 2.5), 20: (1.5, 0.5, 2.5),
                   21: (2.5, 0.5, 2.5), 22: (0.5, 1.5, 2.5), 23: (1.5, 1.5, 2.5), 24: (2.5, 1.5, 2.5),
                   25: (0.5, 2.5, 2.5), 26: (1.5, 2.5, 2.5), 27: (2.5, 2.5, 2.5)}

    return node_test, elmt_test, center_test


@pytest.fixture
def SBox(mocker):
    sb = mocker.MagicMock()

    # Define attributes to mocker object
    sb.w, sb.h, sb.d = 3, 3, 3
    sb.sim_ts = 0
    sb.left, sb.top, sb.front = 0, 0, 0
    sb.right, sb.bottom, sb.back = 3, 3, 3

    return sb


def test_create_voxels(dec_info, SBox):

    box = SBox
    nodeDict, elmtDict, vox_centerDict = create_voxels(box, (3,3,3))

    assert (dec_info[0] == nodeDict).all()
    assert dec_info[1] == elmtDict
    assert dec_info[2] == vox_centerDict


def test_assign_voxels_to_ellipsoid(dec_info):

    # Initialize the Ellipsoids
    ell1 = Ellipsoid(1, 1, 0.5, 0.75, 2.0, 1.5, 1.5,
                     np.array([0.52532199, 0., -0., 0.85090352]))
    ell2 = Ellipsoid(2, 1.9, 1.68, 2.6, 2.0, 1.5, 1.5,
                     np.array([0.52532199, 0., -0., 0.85090352]))
    ells = [ell1, ell2]    

    assign_voxels_to_ellipsoid(dec_info[2], ells, dec_info[1])

    ref1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16]
    ref2 = [14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

    assert set(ell1.inside_voxels) == set(ref1)
    assert set(ell2.inside_voxels) == set(ref2)


def test_reassign_shared_voxels(dec_info):

    # Initialize the Ellipsoids
    ell1 = Ellipsoid(1, 1, 0.5, 0.75, 2.0, 1.5, 1.5,
                     np.array([0.52532199, 0., -0., 0.85090352]))
    ell2 = Ellipsoid(2, 1.9, 1.68, 2.6, 2.0, 1.5, 1.5,
                     np.array([0.52532199, 0., -0., 0.85090352]))

    # Update the ellipsoid dictionary of ficture function
    ell1.inside_voxels.extend([1, 2, 3, 4, 5, 10, 11, 13, 14, 7, 16, 8, 19, 6])
    ell2.inside_voxels.extend([12, 14, 15, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 16, 19, 9])

    ells = [ell1, ell2]

    reassign_shared_voxels(dec_info[2], ells, dec_info[1])

    #ref1 = [1, 2, 3, 4, 5, 10, 11, 13, 7, 8, 6, 19]
    #ref2 = [12, 15, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 9, 16, 14]
    ref1 = [1, 2, 3, 4, 5, 10, 11, 13, 7, 8, 6]
    ref2 = [12, 15, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 9, 16, 14, 19]

    assert set(ref1) == set(ell1.inside_voxels)
    assert set(ref2) == set(ell2.inside_voxels)


def test_voxelizationRoutine():    

    # create a temporary input file for user defined statistics
    cwd = os.getcwd()    
    json_dir = cwd + '/json_files'
    dump_dir = cwd + '/dump_files'
    stat_inp = cwd + '/input_test.json'
            
    # create an temporary 'json' directory for reading files from
    to_write = {'Grain type': 'Elongated', 'Equivalent diameter': {'std': 0.531055, 'mean': 2.76736, 'cutoff_min': 1.0, 'cutoff_max': 2.0},
                'Aspect ratio': {'std':0.3, 'mean': 2.5, 'cutoff_min': 2.0, 'cutoff_max': 4.0}, 'Tilt angle': {'std': 28.8, 'mean': 87.4, 
                "cutoff_min": 75.0, "cutoff_max": 105.0}, 'RVE': {"sideX": 3,"sideY": 3,"sideZ": 3,"Nx": 15,"Ny": 15,"Nz": 15},
                'Simulation': {'periodicity': 'True', 'output_units': 'mm'},
                'Phase': {'Name': 'XXXX', 'Number': 0, 'Volume fraction': 1.0}}

    rve_data = {'Periodic' : False}
    #with open(stat_inp, 'w') as outfile:
    #    json.dump(to_write, outfile, indent=2) 

    RVEcreator(to_write, save_files=True)   

    # create a temporary 'dump' directory for reading files from
    with open(json_dir + '/RVE_data.json') as json_file:
        RVE_data = json.load(json_file)
        
    with open(json_dir + '/particle_data.json') as json_file:
        particle_data = json.load(json_file)
                                    
    sim_box = Simulation_Box(RVE_data['RVE_sizeX'], RVE_data['RVE_sizeY'], RVE_data['RVE_sizeZ'])
    sim_box.sim_ts = 500
    ph = {
        'Phase name': ['Simulanium'] * particle_data['Number'],
        'Phase number': [0] * particle_data['Number'],
    }
    Particles = particle_generator(particle_data, ph, sim_box, rve_data)
    
    #write_dump(Particles, simbox)

    voxelizationRoutine(RVE_data, Particles, sim_box, save_files=True)

    assert os.path.isfile(json_dir + '/nodes_v.csv')
    assert os.path.isfile(json_dir + '/elmtDict.json')
    assert os.path.isfile(json_dir + '/elmtSetDict.json')

    #os.remove(stat_inp)  
    shutil.rmtree(json_dir)
    shutil.rmtree(dump_dir)
