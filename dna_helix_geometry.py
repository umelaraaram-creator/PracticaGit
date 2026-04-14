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
    def _init_(self, n_bases, config=None):
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