import numpy as np

class TrafficSignalOptimizer:
    def __init__(self):
        # Weights for different vehicle types (PCU - Passenger Car Unit)
        self.weights = {
            'car': 1.0,
            'motorcycle': 0.5,
            'bus': 3.0,
            'truck': 2.5
        }
        
        # Webster's Method Constants
        # Saturation Flow: Max capacity of a lane in PCU per minute
        # Typically ~1800 PCU/hr = 30 PCU/min
        self.saturation_flow = 30.0 
        
        # Lost time per phase (Yellow + All-Red) in seconds
        self.lost_time_per_phase = 4
        
        # Constraints
        self.min_green_time = 10
        self.min_cycle_time = 60
        self.max_cycle_time = 150
        
    def calculate_traffic_density(self, counts):
        """
        Calculate weighted traffic density (PCU) for a lane.
        """
        density = 0
        for vehicle_type, count in counts.items():
            weight = self.weights.get(vehicle_type, 1.0)
            density += count * weight
        return density

    def optimize_signals(self, lane_counts):
        """
        Calculate optimal signal timings using Webster's Method.
        """
        # 1. Calculate Flow Ratios (y) for each lane
        # y = Flow / Saturation_Flow
        # We assume the 'counts' are from a snapshot representing ~1 minute of arrival flow for simplicity
        # In a real system, this would be flow_rate over 15 mins.
        
        lane_data = {}
        Y = 0 # Sum of critical flow ratios
        
        for lane, counts in lane_counts.items():
            pcu_count = self.calculate_traffic_density(counts)
            
            # Flow ratio y
            y = pcu_count / self.saturation_flow
            
            lane_data[lane] = {
                'pcu': pcu_count,
                'y': y
            }
            Y += y
            
        # 2. Calculate Optimal Cycle Length (Co)
        # Webster's Formula: Co = (1.5 * L + 5) / (1 - Y)
        # L = Total lost time = lost_time_per_phase * number_of_phases (4)
        
        L = self.lost_time_per_phase * 4
        
        # Safety check: If Y is too close to 1 (oversaturation), the formula explodes.
        # We cap Y at 0.95 for calculation stability.
        Y_clamped = min(Y, 0.95)
        
        if Y_clamped > 0:
            optimal_cycle = (1.5 * L + 5) / (1 - Y_clamped)
        else:
            optimal_cycle = self.min_cycle_time
            
        # Clamp cycle time to min/max limits
        cycle_time = max(self.min_cycle_time, min(self.max_cycle_time, int(optimal_cycle)))
        
        # 3. Calculate Available Green Time
        # Total Green = Cycle - Total Lost Time
        total_effective_green = cycle_time - L
        
        results = {
            'cycle_time': cycle_time,
            'lanes': {},
            'saturation_degree': Y # Useful metric
        }
        
        # 4. Distribute Green Time
        # g_i = (y_i / Y) * Total_Green
        
        allocated_green_sum = 0
        
        for lane in lane_counts.keys():
            y = lane_data[lane]['y']
            
            if Y > 0:
                raw_green = (y / Y) * total_effective_green
            else:
                raw_green = total_effective_green / 4
                
            # Enforce minimum green
            green_time = max(self.min_green_time, int(round(raw_green)))
            
            # Calculate Red Time: Cycle - Green - Yellow (for this lane)
            # Note: In a 4-phase system, Red = Cycle - Green - Yellow is correct for that specific lane's perspective
            red_time = cycle_time - green_time - self.lost_time_per_phase
            
            results['lanes'][lane] = {
                'green_time': green_time,
                'red_time': red_time,
                'yellow_time': self.lost_time_per_phase,
                'density_score': lane_data[lane]['pcu'],
                'flow_ratio': round(y, 3)
            }
            allocated_green_sum += green_time
            
        # Recalculate actual cycle time based on enforced minimums
        results['actual_cycle_time'] = allocated_green_sum + L
            
        return results
