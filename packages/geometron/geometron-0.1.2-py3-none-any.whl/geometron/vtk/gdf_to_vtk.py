from shapely.geometry import Point, LineString, Polygon
from pandas.api.types import is_numeric_dtype
import pyvista as pv
import numpy as np
import itertools


def gdf_to_ug(gdf, elevation='z'):
    """ Transforms a geopandas geodataframe into a pyvista unstructured grid
    Index and fields are added to the grid as cell scalar arrays if they are numeric

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        A geodataframe with unique index values

    elevation : str
        Column name for the elevation field, if geometry is 3D, this value will be ignored

    Returns
    -------
    pv.core.pointset.UnstructuredGrid
        A pyvista unstructured grid containing Points, LineStrings and Polygons with elevation as point data and other
        numeric values stored in columns as cell data arrays
    """

    points = []
    point_cells = []
    tubes = {}
    point_data = []
    k = 0
    point_idx = 0
    # iterate over the rows
    for idx, row in gdf.iterrows():
        if isinstance(row.geometry, Point):
            if row.geometry.has_z:
                x, y, z = row.geometry.x, row.geometry.y, row.geometry.z
            else:
                x, y, z = row.geometry.x, row.geometry.y, row[elevation]
            points.append([x, y, z])
            if row.geometry.has_z:
                point_data.append(row.geometry.z)
            else:
                point_data.append(row[elevation])
            point_cells.append([1, point_idx])
            point_idx += 1

        elif isinstance(row.geometry, LineString) or isinstance(row.geometry, Polygon):
            line_vertices = []

            # iterate over the vertices
            if isinstance(row.geometry, LineString):
                number_of_vertices = len(list(row.geometry.coords))
                if row.geometry.has_z:
                    vertices = list(row.geometry.coords)
                else:
                    vertices = zip(row.geometry.xy[0], row.geometry.xy[1], itertools.repeat(row[elevation]))
            elif isinstance(row.geometry, Polygon):
                number_of_vertices = len(list(row.geometry.exterior.coords))
                if row.geometry.has_z:  # TODO: Can we handle Polygons with holes?
                    vertices = list(row.geometry.exterior.coords)
                else:
                    vertices = zip(row.geometry.exterior.xy[0], row.geometry.exterior.xy[1],
                                   itertools.repeat(row[elevation]))
            else:
                print(f'Invalid geometry type : {type(row.geometry)}')
                return
            for vertex in vertices:
                line_vertices.append([vertex[0], vertex[1], vertex[2]])
            line_vertices = np.array(line_vertices)

            # get the number of vertices and create a cell sequence

            line_cells = np.array([number_of_vertices] + [i for i in range(number_of_vertices)])
            unstructured_grid = pv.UnstructuredGrid(line_cells, np.array([4]), line_vertices)
            # we can add some values to the point
            if row.geometry.has_z:
                if isinstance(row.geometry, Point):
                    unstructured_grid.point_data['Elevation'] = row.geometry.z
                elif isinstance(row.geometry, LineString):
                    unstructured_grid.point_data['Elevation'] = [i[2] for i in row.geometry.coords]
                elif isinstance(row.geometry, Polygon):
                    unstructured_grid.point_data['Elevation'] = [i[2] for i in row.geometry.exterior.coords]
            else:
                unstructured_grid.cell_data['Elevation'] = row[elevation]
            tubes[str(k)] = unstructured_grid
            k += 1

    if len(points) > 0:
        # Create an unstructured grid object for all the points and associate data
        unstructured_grid = pv.UnstructuredGrid(np.array(point_cells), np.array([1] * len(points)), np.array(points))
        unstructured_grid.point_data['Elevation'] = point_data

        # Merge tubes created from lines and
        tubes[str(k)] = unstructured_grid

    blocks = pv.MultiBlock(tubes)
    unstructured_grid = blocks.combine()

    if is_numeric_dtype(gdf.index):
        unstructured_grid['index'] = [i for i in gdf.index]
    for column in gdf.columns:
        if column != 'geometry':
            if is_numeric_dtype(gdf[column]):
                unstructured_grid[column] = gdf[column].values
    return unstructured_grid
