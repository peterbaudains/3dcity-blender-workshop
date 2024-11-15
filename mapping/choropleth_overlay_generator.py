import geopandas as gpd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import pandas as pd
from matplotlib.colors import ListedColormap


def export_legend(legend, filename, legend_label_dict=None, expand=[-5,-5,5,5]):
    '''
    Takes a matplotlib legend, draws the full figure to which that legend belongs, 
    cuts out the legend and saves the legend as a separate file. 
    This legend can then be added as a heads-up display UI element in your unreal project.
    See https://docs.unrealengine.com/5.2/en-US/umg-ui-designer-quick-start-guide/
    '''
    fig  = legend.figure
    fig.canvas.draw()

    if legend_label_dict is not None:
        for label in legend.get_texts():
            label.set_text(legend_label_dict[label.get_text()])
    
    bbox  = legend.get_window_extent()
    bbox = bbox.from_extents(*(bbox.extents + np.array(expand)))
    bbox = bbox.transformed(fig.dpi_scale_trans.inverted())

    fig.savefig(filename, dpi=600, bbox_inches=bbox)


if __name__=="__main__":

    path_to_shapefile = 'sample_data/CityOfLondon_Southwark_2021PopDen.gpkg'
    gdf = gpd.read_file(path_to_shapefile)
    gdf['popden_quantile'] = pd.qcut(gdf['popden'], 5, labels=['1', '2', '3', '4', '5'])
    gdf['popden_quantile_bounds'] = pd.qcut(gdf['popden'], 5)

    color_dict={'1': '#ffffcc', 
                '2': '#a1dab4', 
                '3': '#41b6c4', 
                '4': '#2c7fb8', 
                '5': '#253494'}
    legend_dict = {k:v for k,v in zip(gdf['popden_quantile'].values, gdf['popden_quantile_bounds'])}

    column_to_plot = 'popden_quantile'
    legend_filename = 'images\\popden_legend.png'
    texture_filename = 'images\\popden_texture.png'
    ue_world_origin_bng_eastings = 532000
    ue_world_origin_bng_northings = 181000

    # Set image size. Here we've doubled the default figure size.
    # It doesn't matter too much what size is used, as long as the resulting image is high-res enough 
    # (which can also be configured via the DPI setting) 
    width_inches = 12.8
    height_inches = 9.6
    dpi = 600

    fig = plt.figure(figsize=(width_inches, height_inches))
    ax = fig.add_subplot(111)

    # Plot figure
    gdf.plot(column_to_plot, 
            ax=ax, 
            categorical=True, 
            cmap=ListedColormap(color_dict.values()),
            legend=True,
            legend_kwds={'bbox_to_anchor': (2.0,1)}, # Add enough space for the to fall outside the main graph
            linewidth=0)

    # Extract legend and save as a separate file
    legend = ax.get_legend()
    export_legend(legend, filename=legend_filename, legend_label_dict=legend_dict)

    # Since we've exported the legend, we can now remove it.
    legend.remove()

    # Now we need to amend the axis and padding to ensure we can map the pixels to locations on the map
    ax.axis('scaled')
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    plt.subplots_adjust(left=0, right=1, bottom=0, top=1, hspace=0, wspace=0)

    # If you suspect the padding might be causing issues, then it can be helpful to plot a point in the lower
    # left corner for debugging purposes - a quarter circle should extend to the limit of the image with no white space
    # ax.plot(ax.get_xlim()[0], ax.get_ylim()[0], 'ro', ms=100)

    plt.savefig(texture_filename, bbox_inches='tight', pad_inches=0., dpi=dpi)

    print('The following information is needed to build the overlay texture in Blender:')
    print('LL eastings offset: %s' % ax.get_xlim()[0])
    print('LL northings offset: %s' % ax.get_ylim()[0])

    print('Eastings world origin to texture start (m): %s' % (- (ue_world_origin_bng_eastings - ax.get_xlim()[0])))
    print('Northings world origin to texture start (m): %s' % (- (ue_world_origin_bng_northings - ax.get_ylim()[0])))
    print('Texture width (m): %s' % ( (ax.get_xlim()[1] - ax.get_xlim()[0])))
    print('Text height (m): %s' % ( (ax.get_ylim()[1] - ax.get_ylim()[0])))