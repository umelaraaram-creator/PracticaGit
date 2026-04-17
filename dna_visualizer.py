"""
Visualizes the double helix in interactive 3D (rotate and zoom with the mouse).
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class DNAVisualizer:
    def __init__(self, geometry, sequence):
        self.geometry = geometry
        self.sequence = sequence
        self.base_colors = {'A': 'green', 'T': 'yellow', 'C': 'cyan', 'G': 'magenta'}

    def _create_3d_axes(self):
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, projection='3d')
        return fig, ax

    def _plot_strand(self, ax, helix, outer_color, inner_color, label):
        x_vals, y_vals, z_vals = zip(*helix)
        ax.plot(x_vals, y_vals, z_vals,
                color=outer_color, linewidth=7, alpha=0.28,
                solid_capstyle='round')
        ax.plot(x_vals, y_vals, z_vals,
                color=inner_color, linewidth=3.2, alpha=0.98,
                solid_capstyle='round', label=label)
        ax.plot(x_vals, y_vals, z_vals,
                color='white', linewidth=0.9, alpha=0.22,
                solid_capstyle='round')

    def _plot_helices(self, ax):
        self._plot_strand(ax, self.geometry.helix1,
                          outer_color='#93c5fd', inner_color='#2563eb', label='Helix 1')
        self._plot_strand(ax, self.geometry.helix2,
                          outer_color='#fda4af', inner_color='#dc2626', label='Helix 2')

    def _plot_base_pairs(self, ax):
        seq = getattr(self.sequence, 'sequence', '') if self.sequence is not None else ''
        complementary_seq = self.sequence.get_complementary()
        base_pairs = self.geometry.base_pairs
        for i, pair in enumerate(base_pairs):
            (x1, y1, z1), (x2, y2, z2) = pair
            base = seq[i % len(seq)] if seq else None
            color = self.base_colors.get(base, 'gray')
            ax.plot([x1, x2], [y1, y2], [z1, z2], color=color, linewidth=3, alpha=0.9)
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            mid_z = (z1 + z2) / 2
            ax.scatter([mid_x], [mid_y], [mid_z], color=color, s=20)

    def _configure_axes(self, ax):
        pass

    def _add_legend(self, ax):
        pass

    def plot(self):
        _, ax = self._create_3d_axes()
        self._plot_helices(ax)
        self._plot_base_pairs(ax)
        self._configure_axes(ax)
        self._add_legend(ax)
        plt.show(block=True)