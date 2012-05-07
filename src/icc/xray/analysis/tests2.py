import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

class MatrixBrowser(object):

    def __init__(self, matrix, matrix_ax, connections):
        self.matrix = matrix
        self.matrix_ax = matrix_ax
        self.con = connections
        self.index = (0, 0)
        self.rect = patches.Rectangle((0, 0), 1.1, 1.1,
                    linewidth=3, fill=False, visible=False)
        self.con_rects = self.add_connection_rects()

    def add_connection_rects(self):
        max_cons = max([len(_) for _ in self.con.values()])
        rects = []
        for con in range(max_cons):
            con_rect = patches.Rectangle((0, 0), 1.1, 1.1, linewidth=5,
                        fill=False, visible=False, edgecolor='red')
            rects.append(con_rect)
            self.matrix_ax.add_patch(con_rect)
        return rects

    def update_connections(self, event):
        current_ax = event.inaxes
        cx = event.xdata
        cy = event.ydata
        # only if the cursor is on the matrix ax
        if current_ax == self.matrix_ax:
            rx = round(abs(cx))
            ry = round(abs(cy))
            if not self.index == (rx, ry):
                # make every previous rect invisible
                for rect in self.con_rects:
                    rect.set_visible(False)
                cons = self.con.get((rx, ry), [])
                for rect, con in zip(self.con_rects, cons):
                    rect.set_xy((con[0] - 0.55, con[1] - 0.55))
                    rect.set_visible(True)
                self.index = (rx, ry)
            self.rect.set_visible(True)
            self.rect.set_xy((rx - 0.55, ry - 0.55))
        else:
            self.rect.set_visible(False)
        plt.draw()

def main(matrix, connections):
    fig, ax = plt.subplots()
    im = ax.matshow(matrix, aspect='auto', cmap=plt.cm.winter)
    plt.colorbar(im, use_gridspec=True)
    browser = MatrixBrowser(matrix, ax, connections)
    ax.add_patch(browser.rect)
    fig.canvas.mpl_connect('motion_notify_event', browser.update_connections)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    matrix = np.random.rand(15, 15) * 10
    connections = {(0, 0): [(1, 1), (2, 2), (10, 2), (8, 5)],
                   (3, 2): [(3, 3)],
                   (14, 14): [(0, 0), (0, 14), (14, 0)]}
    main(matrix, connections)
