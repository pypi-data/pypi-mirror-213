import os.path

import pandas as pd
import urllib
import json
import warnings
from .url import http_request, url_open_with_retry, url_request_string
from .str import remove_accents
import rasterio
from rasterio.transform import Affine


xyz_servers_url = {'opentopomap': 'https://opentopomap.org/{z}/{x}/{y}.png',
                   'openstreetmap': 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                   'google terrain': 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                   'esri world imagery': 'https://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}.png'}


def arcgis_rest_services_directory(server, keyword=None, verbose=True):
    resp = http_request(server, data={'f': 'json'})
    list_layers = []
    folders = resp['folders']
    services = resp['services']
    if len(folders) > 0:
        # FOLDERS
        for i in folders:
            if keyword in i or keyword is None:
                query_url_folders = f'{server}/{i}'
                if verbose:
                    print(query_url_folders)
                resp = http_request(query_url_folders, data={'f': 'json'})
                if not resp:
                    continue
                for s in resp['services']:
                    j = s['name']
                    j = j.split('/')[1]
                    t = s['type']
                    query_url_services = f'{query_url_folders}/{j}/{t}'
                    resp = http_request(query_url_services, data={'f': 'json'})

                    if 'layers' in resp.keys():
                        layers = resp['layers']
                        # LAYERS
                        for k in layers:
                            query_url_layers = f'{query_url_services}/{k["id"]}'
                            if verbose:
                                print(query_url_layers)

                            name = k['name'].lower()
                            alias = remove_accents(name)

                            resp = http_request(query_url_layers, data={'f': 'json'})
                            layer_type = resp['type']
                            list_layers.append([i, j, t, k['id'], name, alias, layer_type, query_url_layers])
                    else:
                        list_layers.append([i, j, t, '', '', '', '', ''])

        if len(services) > 0:
            # SERVICES
            for s in services:
                j = s['name']
                if keyword in j or keyword is None:
                    t = s['type']
                    query_url_services = f'{server}/{j}/{t}'
                    print(query_url_services)
                    resp = http_request(query_url_services, data={'f': 'json'})

                    if 'layers' in resp.keys():
                        layers = resp['layers']

                        # LAYERS
                        for k in layers:
                            query_url_layers = f'{query_url_services}/{k["id"]}'
                            if verbose:
                                print(query_url_layers)

                            name = k['name'].lower()
                            alias = remove_accents(name)

                            resp = http_request(query_url_layers, data={'f': 'json'})
                            layer_type = resp['type']
                            list_layers.append(['', j, t, k['id'], name, alias, layer_type, query_url_layers])
        return pd.DataFrame(list_layers, columns=['folder', 'services', 'service_type', 'id_layer', 'name', 'alias',
                                                   'layer_type', 'url'])


def esri_rest_server_geotiff(image_file, host, context='arcgis', folder=None, service=None, service_type='MapServer', layer=None,
                              resource=None, parameter=None, protocol='https', verbose=False):
    """"""  # TODO: Add docstring
    params = parameter.copy()
    params.update({'f': 'pjson'})
    metadata = esri_rest_server_metadata(host, context=context, folder=folder, service=service,
                                         service_type=service_type, layer=layer, resource=resource, operation='export',
                                         parameter=params, protocol=protocol, verbose=verbose)
    #metadata = metadata_from_esri_rest_server(server, service, params, verbose)
    # gets the request to the server
    # request = request_for_esri_rest_server(server, service, params, verbose)
    request = esri_rest_server_request(host, context=context, folder=folder, service=service,
                                         service_type=service_type, layer=layer, resource=resource, operation='export',
                                         parameter=parameter, protocol=protocol, verbose=verbose)

    # opens the response
    with url_open_with_retry(request) as response:
        img = response.read()
    if image_file[-4:] != '.tif':
        image_file = image_file + '.tif'

    with open('./.tmp.tif', 'wb') as tif:
        tif.write(img)

    dx, dy = (metadata['extent']['xmax'] - metadata['extent']['xmin']) / metadata['width'], \
             (metadata['extent']['ymax'] - metadata['extent']['ymin']) / metadata['height']

    src = rasterio.open('./.tmp.tif')
    if os.path.exists(image_file+'.aux.xml'):
        os.remove(image_file+'.aux.xml')
        if verbose:
            print(f'Pre-existing {image_file+".aux.xml"} file has been deleted.')

    with rasterio.open(image_file, 'w', driver='GTiff', dtype='uint8',
                       width=metadata['width'], height=metadata['height'], count=4,
                       crs=f"EPSG:{metadata['extent']['spatialReference']['latestWkid']}",
                       transform=Affine.translation(metadata['extent']['xmin']+dx/2,
                                                    metadata['extent']['ymax']-dy/2) * Affine.scale(dx, -dy),
                       tiled=True,
                       compress='lzw') as dataset:
        dataset.write(src.read())


def geotiff_from_esri_rest_server(image_file, server, service, params, verbose=False):
    """"""  # TODO: Add docstring
    p = params.copy()
    p.update({'f': 'pjson'})
    warnings.warn('API has changed. Use esri_rest_server_geotiff', DeprecationWarning)
    print('Deprecation Warning: API has changed. Use esri_rest_server_geotiff instead!')
    metadata = metadata_from_esri_rest_server(server, service + '/export', p, verbose)
    # gets the request to the server
    request = request_for_esri_rest_server(server, service, params, verbose)
    # opens the response
    with url_open_with_retry(request) as response:
        img = response.read()
    if image_file[-4:] != '.tif':
        image_file = image_file + '.tif'

    with open('./.tmp.tif', 'wb') as tif:
        tif.write(img)

    dx, dy = (metadata['extent']['xmax'] - metadata['extent']['xmin']) / metadata['width'], \
             (metadata['extent']['ymax'] - metadata['extent']['ymin']) / metadata['height']

    src = rasterio.open('./.tmp.tif')
    with rasterio.open(image_file, 'w', driver='GTiff', dtype='uint8',
                       width=metadata['width'], height=metadata['height'], count=4,
                       crs=f"EPSG:{metadata['extent']['spatialReference']['latestWkid']}",
                       transform=Affine.translation(metadata['extent']['xmin'],
                                                    metadata['extent']['ymax']) * Affine.scale(dx, -dy),
                       tiled=True,
                       compress='lzw') as dataset:
        dataset.write(src.read())


# def metadata_from_esri_rest_server(server, service, params, verbose=False):
#     """"""  # TODO: Add docstring
#     p = params.copy()
#     p['f'] = 'json'
#     json_params = urllib.parse.urlencode(p).encode("utf-8")
#     return json.loads(url_open_with_retry(urllib.request.Request(f'{server}{service}/export?',
#                                                                  data=json_params)).read())


def params_for_value_extraction(geom, geom_crs, layer=0, buffer=10, size=100, dpi=96):

    # Extent or bounding box of the map
    xmin, ymin, xmax, ymax = geom.buffer(buffer).bounds

    # Image display parameters
    width = size
    height = size

    # Parameters (Map service - Identify operation)
    params = {'f': 'json',
              'geometry': f'{geom.x},{geom.y}', # Required
              'geometryType': 'esriGeometryPoint',
              'sr': {'wkid': geom_crs},
              'layerDefs': '',
              'layers': f'visible:{layer}',
              'tolerance': 10, # Required
              'mapExtent': f'{xmin},{ymin},{xmax},{ymax}', # Required
              'imageDisplay': f'{width}, {height},{dpi}', # Required
              'returnGeometry': 'True'
             }


def request_for_esri_rest_server(server, service, params, verbose=True):
    """ Creates a request to an ESRI REST API server

        Parameters
        ----------
        server: str
            server address
        service: str
            name of the service
        params: dict
            parameters dictionary
        verbose: bool
            verbose output if True

        Returns
        -------
    https://<host>/<context>/rest/services/<folderName>/<serviceName>/<ServiceType>/<layer>/<resource>/<operation>?<parameter=value>

    """  # TODO: Complete docstring
    warnings.warn('API has changed. Use esri_rest_server_request', DeprecationWarning)
    print('Deprecation Warning: API has changed. Use esri_rest_server_request instead!')
    protocol, s = server.split('://')
    host, context = s.split('/')[:2]
    serv, service_type = service.rsplit('/', 1)
    data = urllib.parse.urlencode(params).encode("utf-8")
    query_url = f'{server}{serv}/{service_type}/export?'
    request = urllib.request.Request(query_url, data=data)
    if verbose:
        print(f"url:\n{url_request_string(request)}\n")
    return request


def transitional_conversion(server, service):

    protocol, s = server.split('://')
    host, context = s.split('/')[:2]
    serv, service_type = service.rsplit('/', 1)
    return [protocol, host, context, serv, service_type]

def metadata_from_esri_rest_server(server, service, params, verbose=False):
    """"""  # TODO: Add docstring
    warnings.warn('API has changed. Use esri_rest_server_metadata', DeprecationWarning)
    print('Deprecation Warning: API has changed. Use esri_rest_server_metadata instead!')
    protocol, host, context, serv, service_type = transitional_conversion(server, service)
    p = params.copy()
    p['f'] = 'json'
    request = esri_rest_server_request(host, context=context, service=serv, service_type=service_type,
                                       parameter=p, protocol=protocol, verbose=verbose)
    return json.loads(url_open_with_retry(request).read())


def esri_rest_server_metadata(host, context='arcgis', folder=None, service=None, service_type='MapServer', layer=None,
                              resource=None, operation='', parameter={'f': 'pjson'}, protocol='https', verbose=True):

    """ Get metata from an ESRI REST server
    
    Parameters
    ----------
    host
    context
    folder
    service
    service_type
    layer
    resource
    operation
    parameter
    protocol
    verbose

    Returns
    -------

    """  # TODO: Improve docstring
    request = esri_rest_server_request(host, context='arcgis', folder=folder, service=service,
                                       service_type=service_type, layer=layer, resource=resource, operation=operation,
                                       parameter=parameter, protocol=protocol, verbose=verbose)
    return json.loads(url_open_with_retry(request).read())


def esri_rest_server_request(host, context='arcgis', folder=None, service=None, service_type=None, layer=None,
                             resource=None, operation='', parameter={'f': 'pjson'}, protocol='https', verbose=True):
    """ Creates a request to an ESRI REST API server

        Parameters
        ----------
        verbose
        protocol
        parameter
        operation
        resource
        layer
        service_type
        service
        folder
        context
        host: str
            host address

        Returns
        -------
            https://<host>/<context>/rest/services/<folderName>/<serviceName>/<ServiceType>/<layer>/<resource>/<operation>?<parameter=value>

    """  # TODO: Improve docstring
    data = urllib.parse.urlencode(parameter).encode('utf-8')
    l = [host, context, 'rest', 'services', folder, service, service_type, layer, resource, f'{operation}?']
    query_url = '/'.join([i for i in l if i is not None])
    query_url = f'{protocol}://{query_url}'
    request = urllib.request.Request(query_url, data=data)
    if verbose:
        print(f'url:\n{url_request_string(request)}\n')
    return request
