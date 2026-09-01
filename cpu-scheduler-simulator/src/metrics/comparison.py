from copy import deepcopy

from src.simulator import Simulator
from src.model.workload import Workload
from src.scheduler_algorithms.SchedulerInterface import SchedulerInterface
from src.metrics.metrics import Metrics


class Comparison:
    def __init__(self, workload: Workload, algorithms : list[SchedulerInterface]):
        self.workload = workload
        self.algorithms = algorithms
        
    def compare(self):
        # Store metrics and simulation results for each algorithm
        comparison_results = {} 
        
        for alg in self.algorithms:
            # Copy workload so each algorithm gets an independent simulation
            copy_processes = deepcopy(self.workload.processes)
            copy_workload = Workload(copy_processes)
           
           # Run the simulation and calculate its metrics
            sim = Simulator(workload=copy_workload, scheduler=alg)
            sim_result = sim.run()
            sim_metrics= Metrics(result=sim_result)
            
            # Keep both metrics and the full simulation result
            # under the algorithm's name
            comparison_results[alg.get_name()] = {
                "metrics":sim_metrics.calculate(),
                "result": sim_result
            }
        
        return comparison_results             
       
            
