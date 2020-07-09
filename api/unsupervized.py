import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.cluster.hierarchy as shc

def dendrogram(df, meta, transp='off', scale=True, color_block='', xlabel='',
               filename=None, row_cluster=True, col_cluster=True, cmap='Blues'):
    sns.set(font_scale=0.7)
    if scale:
        df = (df-df.mean())/df.std()

    if transp=='on':
        df = df.T
        color_block = ''

    if color_block:
        pal = sns.cubehelix_palette(meta[color_block].unique().size,
                                    light=.9, dark=.1,
                                    reverse=True, start=1,
                                    rot=-2)
        minha_paleta = dict(zip(meta[color_block].unique(), pal))
        cores_linhas = meta[color_block].map(minha_paleta)
        cg = sns.clustermap(df, metric="canberra", method="ward",
                            cmap=cmap,  row_colors=cores_linhas)
    else:
        cg = sns.clustermap(df, metric="canberra", method="ward",
                            cmap=cmap, row_cluster=row_cluster,
                            col_cluster=col_cluster)
    # , xticklabels=False
    ax = cg.ax_heatmap
    ax.set_xlabel(xlabel)
    if filename is not None:
        with PdfPages(filename) as pdf:
            pdf.savefig()
            plt.close()

