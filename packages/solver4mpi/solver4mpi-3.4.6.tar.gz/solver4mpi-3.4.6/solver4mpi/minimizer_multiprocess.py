import numpy as np
from pyoperators import *
from scipy.optimize import minimize
import os
import multiprocess as mp
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from threading import Lock

class WrapperMPI:

    def __init__(self, comm, chi2, x0, method='TNC', tol=1e-10, options={}, verbose=False):

        ### MPI distribution
        self.comm = comm
        self.size = comm.Get_size()
        self.rank = comm.Get_rank()

        ### Minimizer
        self.chi2 = chi2
        self.x0 = x0
        self.method = method
        self.tol = tol
        self.options = options
        self.verbose = verbose

    def _split_params(self, index):

        '''
        
        Distribute the parameters across all available processes

        '''
        return np.where(index % self.size == self.rank)[0]

    def _apply_minimize(self, args):

        '''
        
        Apply the scipy.optimize.minimize method on the fun cost function.

            
        '''

        r = minimize(self.chi2, x0=self.x0, args=args, method=self.method, tol=self.tol, options=self.options)
        return r.x


    def __call__(self, index):

        res = np.zeros(index.shape)
        x_per_process = self._split_params(index)
        if self.verbose:
            print(self.rank, x_per_process)

        for ii, i in enumerate(x_per_process):
            
            start = time.time()
            res[i] = self._apply_minimize(args=(index[i]))
            end = time.time()

            if self.verbose:
                print(f'Minimized parameter {index[i]} with rank {self.rank} in {end - start:.6f} s')
        
        return self.comm.allreduce(res, op=MPI.SUM)

class DistributeMPI(WrapperMPI):

    def __init__(self, comm, ncpu, chi2, x0, method='L-BFGS-B', tol=1e-10, options={}, verbose=True):

        self.ncpu = ncpu
        WrapperMPI.__init__(self, comm, chi2, x0, method=method, tol=tol, options=options, verbose=verbose)

    def _split_params_with_cpu(self, index, cpu):

        index_per_process = self._split_params(index)
        
        chunk_size = len(index_per_process) // cpu
        chunk_rest = len(index_per_process) % cpu
        if chunk_rest != 0:
            chunk_size += 1
        index_per_process_per_cpu = np.array_split(index_per_process, chunk_size)

        return index_per_process_per_cpu


    def run(self, x):
        res = np.zeros(x.shape[0])
        
        index_per_process_per_cpu = self._split_params_with_cpu(x, self.ncpu)
        #stop
        _loop = len(index_per_process_per_cpu)

        for i in range(_loop):
            if self.verbose:
                print(self.rank, index_per_process_per_cpu[i], x[index_per_process_per_cpu[i]])
            res[index_per_process_per_cpu[i]] = self.perform(x[index_per_process_per_cpu[i]])
        self.comm.Barrier()
        if self.verbose:
            print(res)
        return self.comm.allreduce(res, op=MPI.SUM)

    def perform(self, x):
        results = Queue()  # File d'attente pour stocker les résultats
        lock = Lock()  # Verrou pour synchroniser l'accès à la file d'attente

        def minimize_wrapper(index, args):
            result = self._apply_minimize(args)
            with lock:
                results.put((index, result))  # Ajouter l'index avec le résultat

        with ThreadPoolExecutor(max_workers=self.ncpu) as executor:
            futures = [executor.submit(minimize_wrapper, index, i) for index, i in enumerate(x)]

        # Attendre la fin de toutes les tâches
        for future in futures:
            future.result()

        # Réorganiser les résultats dans l'ordre approprié
        final_results = [None] * len(x)
        while not results.empty():
            index, result = results.get()
            final_results[index] = result

        return np.concatenate(final_results)

    '''
    def perform(self, x):
        with ThreadPoolExecutor(max_workers=self.ncpu) as executor:
            futures = [executor.submit(self._apply_minimize, i) for i in x]
            results = [future.result() for future in futures]
        return np.concatenate(results)
    '''
    

class WrapperCPU:

    def __init__(self, chi2, x0, nproc=None, method='TNC', tol=1e-3, options={}, verbose=False):

        ### Do some prints
        self.verbose = verbose

        ### Minimizer
        self.chi2 = chi2
        self.x0 = x0
        self.method = method
        self.tol = tol
        self.options = options
        if nproc is None:
            self.ncpu = os.cpu_count()
        else:
            self.ncpu = nproc

        if self.verbose:
            print(f'Requested for {self.ncpu} CPUs')

    def _split_params(self, index_theta):

        '''
        
        Distribute the parameters across all available processes

        '''
        return np.where(index_theta % self.size == self.rank)[0]

    def _apply_minimize(self, args):

        '''
        
        Apply the scipy.optimize.minimize method on the fun cost function.

            
        '''

        r = minimize(self.chi2, x0=self.x0, args=args, method=self.method, tol=self.tol, options=self.options)
        return r.x

    def perform(self, x):
        
        pool = mp.Pool(processes=self.ncpu)
        results = pool.starmap(self._apply_minimize, [[param_values] for param_values in x])
        
        # Close and join results
        pool.close()
        pool.join()

        return results



"""


class WrapperMPI:

    def __init__(self, comm, chi2, x0, method='TNC', tol=1e-3, options={}, verbose=False):

        ### Do some prints
        self.verbose = verbose
        
        ### MPI distribution
        self.comm = comm
        self.size = self.comm.Get_size()
        self.rank = self.comm.Get_rank()

        ### Minimizer
        self.chi2 = chi2
        self.x0 = x0
        self.method = method
        self.tol = tol
        self.options = options

        if verbose:
            print(f'size = {self.size} and rank = {self.rank}')

    def _split_params(self, index_theta):

        '''
        
        Distribute the parameters across all available processes

        '''
        return np.where(index_theta % self.size == self.rank)[0]
    
    def _apply_minimize(self, fun, args):

        '''
        
        Apply the scipy.optimize.minimize method on the fun cost function.

            Warning : fun is the cost function and should take as free parameter theta and the id of the targeted pixel

        '''

        r = minimize(fun, x0=self.x0, args=args, method=self.method, tol=self.tol, options=self.options)
        return r.x
    
    def _joint_process(self, theta):

        '''
        
        Joint the results of all processes. After that command, all processes knows the result of the minimization.

        '''
        return self.comm.allreduce(theta, op=MPI.SUM)
        
    def perform(self, index_theta):

        '''
        
        Main function to be called. Perform the minimization on the pixel indexed by index_theta array.
        
        '''
        if len(self.x0) > 1:
            res = np.zeros((len(index_theta), len(self.x0)))
        else:
            res = np.zeros(len(index_theta))
        index_per_process = self._split_params(index_theta)
        if self.verbose:
            print(f'Doing minimization on pixel {index_per_process}')
        
        for _, index in enumerate(index_per_process):
            print(index, index_per_process)
            res[index] = self._apply_minimize(self.chi2, args=(index))
        print(res)
        
        ### Wait for all processes
        self.comm.Barrier()
 
        return self._joint_process(res)
"""