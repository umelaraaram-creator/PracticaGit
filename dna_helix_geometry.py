import numpy as np

DNA_CONFIG = {
    'bases_per_turn': 10.5,
    'z_step': 0.34,
    'radius': 1.0,
    'angle_step': 0.6,
    'strand_offset': 2 * np.pi / 3,
    'smooth_per_base': 10,
}

class DNAHelixGeometry:
    def __init__(self, n_bases, config=None):
        if config is None:
            config = DNA_CONFIG
        self.config = {
            'bases_per_turn': config['bases_per_turn'],
            'z_step': config['z_step'],
            'radius': config['radius'],
            'angle_step': config['angle_step'],
            'strand_offset': config.get('strand_offset', np.pi),
            'smooth_per_base': config.get('smooth_per_base', 10),
        }
        self.n_bases = int(n_bases)
        if self.n_bases <= 0:
            raise ValueError("n_bases must be a positive integer.")
        self.n_turns = self.n_bases / self.config['bases_per_turn']
        self.helix1 = []
        self.helix2 = []
        self.base_pairs = []
        self.calculate_geometry()

def _calculate_strands(self):
        total_angle = self.n_bases * self.config['angle_step']
        total_z = self.n_bases * self.config['z_step']
        n_smooth = self.n_bases * self.config['smooth_per_base']
        
        theta_smooth = np.linspace(0, total_angle, n_smooth)
        z_smooth = np.linspace(0, total_z, n_smooth)
        
        x1 = self.config['radius'] * np.cos(theta_smooth)
        y1 = self.config['radius'] * np.sin(theta_smooth)
        
        x2 = self.config['radius'] * np.cos(theta_smooth + self.config['strand_offset'])
        y2 = self.config['radius'] * np.sin(theta_smooth + self.config['strand_offset'])
        
        self.helix1 = list(zip(x1, y1, z_smooth))
        self.helix2 = list(zip(x2, y2, z_smooth))