# 3D City and Geospatial Data Visualisation in Blender

This repository contains supporting code for a workshop on visualising geospatial data in 3D city models using Blender.

The workshop aims to take participants through the following three tasks:

1. Introduction to Blender, 3d city import from fbx and creating a first render.
2. Create a choropleth map and overlay this on the 3D city model
3. Plot data points within the 3D city model coloured according an attribute value.

## 3D city data

We will use the 3D city data provided by [AccuCities](https://accucities.com). A sample 3D tile of London can be requested by filling in the form at the bottom of [this page](https://accucities.com/3d-city-models-gallery/). The scripts contained in this repository will use this sample file.

## Dependencies

To participate in the workshop, participants should have the following software:

- [Blender](https://www.blender.org) version 4.2, with FBX extension enabled and [Dynamic Sky](https://extensions.blender.org/add-ons/dynamic-sky/) add-on installed.
- [Conda](https://docs.conda.io)
- Geopandas 1.0.1 (installed via conda command, below)
- Matplotlib 3.9.2 (installed via conda command, below).

## Conda environment for map construction

To run the `choropleth_overlay_generator.py` function, a dedicated conda environment with the required geospatial dependencies. The conda command is as follows:

`conda create --name 3dcity-workshop-env --channel conda-forge geopandas matplotlib`

## Data acknowledgements

This repository contains sample data from the 2021 Census downloaded from [nomisweb](https://www.nomisweb.co.uk), geospatial boundaries obtained from the [ONS Open Geography Portal](https://geoportal.statistics.gov.uk/) and [Food Hygiene Rating Data](https://ratings.food.gov.uk) from the Food Standards Agency. Contains public sector information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
