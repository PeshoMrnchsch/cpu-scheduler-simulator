from src.model.process import Process

class SimulationResult:
    def __init__ (
            self, 
            processes_completed : list[Process], 
            simulation_start:int, 
            simulation_end:int, 
            timeline: list[tuple[int, int, int]] #(start, end, process_id)
            ):
            self.processes_completed = processes_completed
            self.simulation_start = simulation_start
            self.simulation_end = simulation_end
            self.timeline = timeline
            
    