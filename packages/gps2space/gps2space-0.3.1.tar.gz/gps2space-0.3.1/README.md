Many data are not readily in spatial format. For example, data from wearable devices, surveys, and social media platforms such as Facebook and Twitter have GPS location information, but usually in raw Lat/Long format. For social scientists who do not have strong background in Geographic Information System (GIS), compiling and analyzing spatial data from the aforementioned sources can be tedious and error-prone. `GPS2space` is an open source solution to this issue.

The primary goals of `GPS2space` are:

- to build spatial data from raw Lat/Long coordinate pairs and make the process less painful for social scientists with little GIS background
- to build minimum bounding geometry from Points using buffer, convex hull methods, and use activity space as building box to calculate shared space at different scales
- to calculate the nearest distance from user-defined landmarks

`GPS2space` can be used in studies such as mobility, behavioral science, transportation, etc. For more information, please see the [Documentation](https://gps2space.readthedocs.io/en/latest/)

Currently, `GPS2space` has the following functionalities:

- `geodf.df_to_gdf`: This function builds unprojected GeoDataFrame from DataFrame with Lat/Long coordinate pairs
- `space.buffer_spa`: This function calculates buffer-based activity space with user-defined level of aggregation, buffer distance, and projection
- `space.convex_space`: This function calculates convex hull-based activity space with user-defined level of aggregation and projection
- `dist.dist_to_point`: This function calculates nearest Point-Point distance with user-defined projection
- `dist.dist_to_poly`: This function calculates nearest Point-Polygon distance with user-defined projection and search radius

`GPS2space` relies on [GeoPandas](https://geopandas.org/), [Shapely](https://shapely.readthedocs.io/en/latest/), and [SciPy](https://www.scipy.org/).
