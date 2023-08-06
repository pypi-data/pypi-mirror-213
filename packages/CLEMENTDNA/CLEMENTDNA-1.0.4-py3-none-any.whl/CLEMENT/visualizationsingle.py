import palettable
import matplotlib
import seaborn as sns
import numpy as np
from scipy.stats import kde
import extract
from sklearn.decomposition import TruncatedSVD, PCA
from mpl_toolkits import mplot3d


def drawfigure_1d(membership, output_suptitle, output_filename, np_vaf, samplename_dict, includefp, fp_index, makeone_index, **kwargs):
    vivid_10 = palettable.cartocolors.qualitative.Vivid_10.mpl_colors
    bdo = palettable.lightbartlein.diverging.BlueDarkOrange18_18.mpl_colors
    tabl = palettable.tableau.Tableau_20.mpl_colors
    Gr_10 = palettable.scientific.sequential.GrayC_20.mpl_colors
    colorlist = [i for i in tabl]

    # font_dir = "/home/goldpm1/miniconda3/envs/cnvpytor/lib/python3.7/site-packages/matplotlib/mpl-data/fonts/ttf/"
    # font_dirs = matplotlib.font_manager.findSystemFonts(fontpaths=font_dir, fontext='ttf')
    # for font in font_dirs:
    #     matplotlib.font_manager.fontManager.addfont(font)
    #print (matplotlib.font_manager.FontProperties(fname = font).get_name())

    matplotlib.rcParams["font.family"] =  kwargs["FONT_FAMILY"]
    matplotlib.pyplot.style.use("seaborn-white")

    if includefp == True:
        colorlist[ fp_index ] = Gr_10[8]       
    
    fig, ax = matplotlib.pyplot.subplots (figsize = (6, 6))
    matplotlib.pyplot.suptitle(output_suptitle, fontsize = 20)


    max_y = 0

    x = np.linspace(0, 2, 200)

    for k in sorted(list(set(membership))):  
        np_vaf_new_index, np_vaf_new = extract.npvaf(np_vaf, membership, k)
        
        try:
            kde_np_vaf_new = kde.gaussian_kde(np_vaf_new[:, 0] * 2)
            weight = len(np_vaf_new) / len(np_vaf)

            y = kde_np_vaf_new(x) * weight
            if max_y < np.max(y):
                max_y = np.max(y)

            if k in makeone_index:
                ax.plot(x, y, color=colorlist[k], linewidth=5, label=samplename_dict[k])
            else:
                ax.plot(x, y, color=colorlist[k], linewidth=5, label=samplename_dict[k],  linestyle="-.")

            #ax.plot(x, y, color=colorlist[k], label=samplename_dict[k], linewidth = 5)
            ax.text(np.argmax(y) / 100, np.max(y) * 1.08, "{} (n = {})".format(np.argmax(y) / 100,  np.bincount(membership)[k]), verticalalignment='top', ha = "center", fontdict = {"fontsize": 16, "fontweight" : "bold"})
        except:
            continue

    ax.axis([0,  1,  0,  max_y * 1.3])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_linewidth (3)
    ax.legend()

    ax.set_xlabel("Mixture ( = VAF * 2)", fontdict = {"fontsize" : 14})
    ax.set_ylabel("Density", fontdict = {"fontsize" : 14})

    if output_filename != "NotSave":
        matplotlib.pyplot.savefig(output_filename)
    matplotlib.pyplot.show()




def drawfigure_2d(membership, output_suptitle, output_filename, np_vaf, samplename_dict, includefp, fp_index, dimensionreduction="None",  **kwargs):
    vivid_10 = palettable.cartocolors.qualitative.Vivid_10.mpl_colors
    bdo = palettable.lightbartlein.diverging.BlueDarkOrange18_18.mpl_colors
    tabl = palettable.tableau.Tableau_20.mpl_colors
    Gr_10 = palettable.scientific.sequential.GrayC_20.mpl_colors
    colorlist = [i for i in tabl]
    
    # font_dir = "/home/goldpm1/miniconda3/envs/cnvpytor/lib/python3.7/site-packages/matplotlib/mpl-data/fonts/ttf/"
    # font_dirs = matplotlib.font_manager.findSystemFonts(fontpaths=font_dir, fontext='ttf')
    # for font in font_dirs:
    #     matplotlib.font_manager.fontManager.addfont(font)
    #print (matplotlib.font_manager.FontProperties(fname = font).get_name())

    matplotlib.rcParams["font.family"] =  kwargs["FONT_FAMILY"]
    matplotlib.pyplot.style.use("seaborn-white")

    fig, ax = matplotlib.pyplot.subplots (figsize = (6, 6))
    
    if dimensionreduction == "SVD":
        print("SVD → 2D")
        tsvd = TruncatedSVD(n_components=2)
        tsvd.fit(np_vaf)
        np_vaf = tsvd.transform(np_vaf)
        ax.axis([np.min(np_vaf[:, 0]) * 2.1,  np.max(np_vaf[:, 0]) *  2.1,  np.min(np_vaf[:, 1]) * 2.1,  np.max(np_vaf[:, 1]) * 2.1])
        ax.set_xlabel("SVD1", fontdict = {"fontsize" : 14})
        ax.set_ylabel("SVD2", fontdict = {"fontsize" : 14})
    elif dimensionreduction == "PCA":
        print("PCA → 2D")
        pca = PCA(n_components=2)
        pca.fit(np_vaf)
        np_vaf = pca.transform(np_vaf)
        ax.axis([np.min(np_vaf[:, 0]) * 2.1,  np.max(np_vaf[:, 0]) * 2.1,  np.min(np_vaf[:, 1]) * 2.1,  np.max(np_vaf[:, 1]) * 2.1])
        ax.set_xlabel("PC1", fontdict = {"fontsize" : 14})
        ax.set_ylabel("PC2", fontdict = {"fontsize" : 14})
    else:
        ax.axis([0,  np.max(np_vaf[:, :]) * 2.1, 0,  np.max(np_vaf[:, :]) * 2.1])
        ax.set_xlabel("Mixture ( = VAF x 2) of Sample 1", fontdict = {"fontsize" : 14})
        ax.set_ylabel("Mixture ( = VAF x 2) of Sample 2", fontdict = {"fontsize" : 14})


    #matplotlib.pyplot.suptitle("{}  (n = {})".format(output_filename, len(membership)), fontsize = "large")
    #print (membership)

    fig.suptitle(output_suptitle, fontsize = 20)

    if includefp == True:
        outlier_color_num = samplename_dict[ fp_index ] 
        colorlist [ outlier_color_num ] = Gr_10[8]

    ax.scatter(np_vaf[:, 0] * 2, np_vaf[:, 1] * 2, color=[colorlist[samplename_dict[k]] for k in membership], s = 40)


    if (dimensionreduction != "SVD") & ( dimensionreduction != "PCA" ):
        for sample_index, sample in enumerate(samplename_dict):
            if sample not in set(membership):
                continue

            x_mean = round(np.mean(np_vaf[[x for x in range( len(membership)) if membership[x] == sample]][:, 0] * 2), 2)
            y_mean = round(np.mean(np_vaf[[x for x in range( len(membership)) if membership[x] == sample]][:, 1] * 2), 2)

            ax.text(x_mean, y_mean, "{0}".format([x_mean, y_mean]), verticalalignment='top', ha = "center", fontdict = {"fontsize": 16, "fontweight" : "bold"})
            ax.scatter(x_mean, y_mean, marker='*', color=colorlist[samplename_dict[sample]], edgecolor='black', s=220, label=str(sample) + " : " + str(list(membership).count(sample)))
            ax.legend()

    if output_filename != "NotSave":
        fig.savefig(output_filename)
    #matplotlib.pyplot.show()

def main(output_filename, np_vaf, membership_answer, **kwargs):
    global NUM_BLOCK_INPUT, NUM_BLOCK, RANDOM_PICK, NUM_MUTATION, FP_RATIO, INPUT_DIR, OUTPUT_DIR

    NUM_BLOCK_INPUT = kwargs["NUM_BLOCK_INPUT"]
    NUM_BLOCK = kwargs["NUM_BLOCK"]
    RANDOM_PICK = kwargs["RANDOM_PICK"]
    NUM_MUTATION = RANDOM_PICK
    FP_RATIO = kwargs["FP_RATIO"]
    INPUT_DIR = "/data/project/Alzheimer/EM_cluster/pilot/04.EM_input/"
    OUTPUT_DIR = "./output/"

    if NUM_BLOCK == 2:
        drawfigure_2d(membership_answer, output_filename, np_vaf)
    # if NUM_BLOCK == 3:
    #     drawfigure_3d(membership_answer, output_filename, np_vaf)
