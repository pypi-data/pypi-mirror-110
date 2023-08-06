
# Python package for remote sensing image fusion

The fusion of remote sensing images allows the enhancemente of their spatial and temporal characteristics. The application of these techniques in the field of Earth observation is still limited because of the complexity of the different algorithms developed with this purpose.
This package includes two source codes (cited below) with the implementation of two remote sensing fusion algorithms: STARFM, ESTARFM. 
It can be used as a template, as it includes a common part to open and process the imported images, that can be used by a third  fusing algorithm.
The aim of this package is to make these products more accessible to users, providing them with a simple package that takes .tif images, and applies the selected algorithm to get a .tif fused result.
To implement the starfm method: starfm().
To implement the estarfm method: estarfm().   
  


# Open source code references:
    1. Mileva, N., Mecklenburg, S. & Gascon, F. (2018). New tool for spatiotemporal image fusion in remote sensing - a case study approach using Sentinel-2 and Sentinel-3 data. In Bruzzone, L. & Bovolo, F. (Eds.), SPIE Proceedings Vol. 10789: Image and Signal Processing for Remote Sensing XXIV. Berlin, Germany: International Society for Optics and Photonics. doi: 10.1117/12.2327091; https://doi.org/10.1117/12.2327091

    2. Zhu, Xiaolin. Polyu remote sensing intelligence for dynamic Earth; https://xiaolinzhu.weebly.com/open-source-code.html
