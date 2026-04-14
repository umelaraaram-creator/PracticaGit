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
        ax.plot(
            x_vals,
            y_vals,
            z_vals,
            color=outer_color,
            linewidth=7,
            alpha=0.28,
            solid_capstyle='round',
        )
        ax.plot(
            x_vals,
            y_vals,
            z_vals,
            color=inner_color,
            linewidth=3.2,
            alpha=0.98,
            solid_capstyle='round',
            label=label,
        )
        ax.plot(
            x_vals,
            y_vals,
            z_vals,
            color='white',
            linewidth=0.9,
            alpha=0.22,
            solid_capstyle='round',
        )

    def _make_base_plate(self, start, end, width):
        start = np.array(start)
        end = np.array(end)
        direction = end - start
        direction_norm = np.linalg.norm(direction)
        if direction_norm == 0:
            return None

        direction = direction / direction_norm
        z_axis = np.array([0.0, 0.0, 1.0])
        normal = np.cross(direction, z_axis)
        normal_norm = np.linalg.norm(normal)
        if normal_norm < 1e-8:
            normal = np.array([1.0, 0.0, 0.0])
        else:
            normal = normal / normal_norm

        offset = normal * (width / 2)
        return [
            start - offset,
            start + offset,
            end + offset,
            end - offset,
        ]

    def _plot_helices(self, ax):
        self._plot_strand(ax, self.geometry.helix1, outer_color='#93c5fd', inner_color='#2563eb', label='Helix 1')
        self._plot_strand(ax, self.geometry.helix2, outer_color='#fda4af', inner_color='#dc2626', label='Helix 2')

    def _plot_base_pairs(self, ax):
        seq = self.sequence.sequence
        complementary_seq = self.sequence.get_complementary()
        base_plate_width = 0.14 * self.geometry.config['radius']

        for i, ((x1, y1, z1), (x2, y2, z2)) in enumerate(self.geometry.base_pairs):
            base = seq[i % len(seq)]
            complementary_base = complementary_seq[i % len(complementary_seq)]
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            mid_z = (z1 + z2) / 2

            first_half = self._make_base_plate((x1, y1, z1), (mid_x, mid_y, mid_z), base_plate_width)
            second_half = self._make_base_plate((mid_x, mid_y, mid_z), (x2, y2, z2), base_plate_width)
            if first_half is not None:
                ax.add_collection3d(Poly3DCollection(
                    [first_half],
                    facecolors=self.base_colors.get(base, 'gray'),
                    edgecolors='none',
                    alpha=0.9,
                ))
            if second_half is not None:
                ax.add_collection3d(Poly3DCollection(
                    [second_half],
                    facecolors=self.base_colors.get(complementary_base, 'gray'),
                    edgecolors='none',
                    alpha=0.9,
                ))

    def _configure_axes(self, ax):
        ax.set_xlabel('X (nm)')
        ax.set_ylabel('Y (nm)')
        ax.set_zlabel('Z (nm)')
        ax.set_title('DNA Double Helix (3D) - Real Dimensions')
        ax.view_init(elev=20, azim=45)

        # Turn off the grid and background panes while keeping the axes.
        ax.grid(False)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('none')
        ax.yaxis.pane.set_edgecolor('none')
        ax.zaxis.pane.set_edgecolor('none')

    def _add_legend(self, ax):
        helix_handles, helix_labels = ax.get_legend_handles_labels()
        base_handles = [
            Patch(facecolor=self.base_colors['A'], edgecolor='none', label='A'),
            Patch(facecolor=self.base_colors['T'], edgecolor='none', label='T'),
            Patch(facecolor=self.base_colors['C'], edgecolor='none', label='C'),
            Patch(facecolor=self.base_colors['G'], edgecolor='none', label='G'),
        ]
        ax.legend(helix_handles + base_handles, helix_labels + ['A', 'T', 'C', 'G'])

    def plot(self):
        _, ax = self._create_3d_axes()
        self._plot_helices(ax)
        self._plot_base_pairs(ax)
        self._configure_axes(ax)
        self._add_legend(ax)

        plt.show()
