import pysm3
import pysm3.units as u
from pysm3 import utils
import healpy as hp
import matplotlib.pyplot as plt
from minimizer_multiprocess import *
import sys
import time
import pickle
from functools import partial
import os

os.environ['OMP_NUM_THREADS'] = '10'

sys.path.append('/Users/mregnier/Desktop/Libs/qubic/qubic/scripts/MapMaking')

import component_model as c
import mixing_matrix as mm

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

def _scale_components_1pix(beta, ipix, mref, allnus):

    components = c.Dust(nu0=nu0, temp=20)
    A_ev = mm.MixingMatrix(components).evaluator(allnus)
    Aev = A_ev(beta)
    nf, nc = Aev.shape
    m_nu = np.zeros((nf, 3))
    for i in range(3): #Nstk
        m_nu[:, i] = Aev @ np.array([mref[ipix, i]])

    return m_nu

nside = 8
sky=pysm3.Sky(nside=nside, preset_strings=['d0'], output_unit="uK_CMB")
nu0 = 150
mref = np.array(sky.get_emission(nu0 * u.GHz, None).T * utils.bandpass_unit_conversion(nu0*u.GHz, None, u.uK_CMB))


allnus = np.array([140, 150, 160])
m_nu = np.zeros((len(allnus), 12*nside**2, 3))

np.random.seed(1)
beta = np.random.normal(1.54, 0.1, 12*nside**2)
for j in range(12*nside**2):
    m_nu[:, j, :] = _scale_components_1pix(beta[j], j, mref, allnus)

def chi2(x, ipix, mref, m_nu, allnus):

    #map_beta[ipix] = x
    m_nu_fake = _scale_components_1pix(x, ipix, mref, allnus)
    
    return np.sum((m_nu_fake - m_nu[:, ipix, :])**2)

index_beta = np.array([4,12,13,20,21,27,28,29,35,36,43])#np.arange(50, 60, 1)

chi2_partial = partial(chi2, mref=mref, m_nu=m_nu, allnus=allnus)
cpu = 2
#wrap = WrapperMPI(comm, chi2_partial, x0=np.ones(1)*1.5, method='TNC', tol=1e-10, options={}, verbose=True)
wrap = DistributeMPI(comm, cpu, chi2_partial, x0=np.ones(1)*1.5, method='TNC', tol=1e-10)
#print(index_per_process_per_cpu)
start = time.time()
a = wrap.run(index_beta)

end = time.time()
if rank == 0:
    print(a)
    print(beta[index_beta])
    print(np.mean(a - beta[index_beta]))
    print(f'Execution time : {end - start} s')




'''
if rank == 0:
    start = time.time()
    beta_i = run(index_beta, 5, chi2_partial, x0=np.ones(1), method='L-BFGS-B', tol=1e-6, options={}, verbose=True)#WrapperCPU(chi2_partial, x0=np.ones(1), nproc=2, verbose=True, tol=1e-20, method='TNC').perform(index_beta)
    end = time.time()
    print(f'Execution time : {end - start} s')
    print(f'Residuals :', beta_i - beta[:len(index_beta)])
    print(f'estimated :', beta_i)
    print(f'true :', beta[:len(index_beta)])
    print(f'Execution time : {end - start} s')
'''





#if comm.Get_rank() == 0:
#    print(f'Execution time : {end - start} s')
#    print(f'Residuals :', beta_est - beta[:5])
#    print(f'estimated :', beta_est)
#    print(f'true :', beta[:5])




