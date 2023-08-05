#!/usr/bin/env python
# encoding: utf-8
#
# Copyright SAS Institute
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

''' Image analysis tools '''

import sys
stdout = sys.stdout
stderr = sys.stderr

import struct
import numpy as np

sys.stdout = stdout
sys.stderr = stderr

def __reverse(a, axis=0):

    '''
    Reverses a numpy array along a given axis.

    Parameters
    ----------
    a : numpy.ndarray
        Specifies the array to be reversed.
    axis : int
        Specifies the axis.

    Returns
    -------
    :numpy.ndarray
    '''

    idx = [slice(None)] * len(a.shape)
    idx[axis] = slice(None, None, -1)
    return a[idx]

def get_image_array_from_row(image_binary, dimension, resolution, myformat, channel_count=1):

    '''
    Get a 3D image from a row.

    Parameters
    ----------
    image_binary : bytes
        Specifies the image binary.
    dimension : int
        Specifies the dimension of the image.
    resolution : numpy.ndarray
        Specifies the resolution of the image.
    myformat : str
        Specifies the format of the image.
    channel_count : int, optional
        Specifies the channel count of the image.

    Returns
    -------
    :numpy.ndarray
    '''

    num_cells = np.prod(resolution)
    if (myformat == '32S'):
        image_array = np.array(struct.unpack('=%si' % num_cells, image_binary[0:4 * num_cells]))
        image_array = np.reshape(image_array, resolution)
    elif myformat == '32F':
        image_array = np.array(struct.unpack('=%sf' % num_cells, image_binary[0:4 * num_cells]))
        image_array = np.reshape(image_array, resolution)
    elif myformat == '64F':
        image_array = np.array(struct.unpack('=%sd' % num_cells, image_binary[0:8 * num_cells]))
        image_array = np.reshape(image_array, resolution)
    elif myformat == '64U':
        image_array = np.array(struct.unpack('=%sQ' % num_cells, image_binary[0:8 * num_cells]))
        image_array = np.reshape(image_array, resolution)
    elif myformat == '16S':
        image_array = np.array(struct.unpack('=%sh' % num_cells, image_binary[0:2 * num_cells]))
        image_array = np.reshape(image_array, resolution)
    elif myformat == '16U':
        image_array = np.array(struct.unpack('=%sH' % num_cells, image_binary[0:2 * num_cells]))
        image_array = np.reshape(image_array, resolution)
    elif myformat == '8U' and channel_count==3:
        image_array = np.array(bytearray(image_binary[0:(num_cells*3)]))
        image_array = np.reshape(image_array, (resolution[0], resolution[1], 3))[:, :, 0:3]
        image_array = __reverse(image_array, 2)
    elif myformat == '8S':
        image_array = np.array(struct.unpack('=%sb' % num_cells, image_binary[0:num_cells]))
        image_array = np.reshape(image_array, resolution)
    elif myformat == '8U':
        image_array = np.array(struct.unpack('=%sB' % num_cells, image_binary[0:num_cells]))
        image_array = np.reshape(image_array, resolution)
    else:
        image_array = np.array(bytearray(image_binary))
        image_array = np.reshape(image_array, (resolution[0], resolution[1], 3))
        image_array = __reverse(image_array, 2)
    return image_array

def get_image_array(image_binaries, dimensions, resolutions, formats, n, channel_count=1):

    '''
    Get an image from a fetched array.

    Parameters
    ----------
    image_binaries : pandas.Series
        Specifies the image binaries
    dimensions : pandas.Series
        Specifies the dimensions of the images.
    resolutions : pandas.Series
        Specifies the resolutions of the images.
    formats : pandas.Series
        Specifies the image formats.
    n : int
        Specifies the dimension index.
    channel_count : int, optional
        Specifies the channel count of the image.

    Returns
    -------
    :numpy.Array
    '''

    dimension = int(dimensions[n])
    resolution = np.array(struct.unpack('=%sq' % dimension, resolutions[n][0:dimension * 8]))
    resolution = resolution[::-1]
    myformat = formats[n]
    num_cells = np.prod(resolution)
    return get_image_array_from_row(image_binaries[n], dimension, resolution, myformat, channel_count)

def convert_to_CAS_column(s):

    '''
    Convert a string to CAS column name.

    Parameters
    ----------
    s : string
        Specifies the column name to be converted.

    Returns
    -------
    : string
    '''

    s = str.replace(str.replace(s, '{', '_'), '}', '_')
    return '_'+s+'_'

def fetch_image_array(imdata, n=0, qry='', image='_image_', dim='_dimension_', res='_resolution_', ctype='_channelType_', ccount=1):

    '''
    Fetch image array from a CAS table.

    Parameters
    ----------
    imdata : string
        Specifies the image data.
    n : int
        Specifies the number of additional images.
    qry : string
        Specifies the query.
    image : string
        Specifies the image format.
    dim : string
        Specifies the image dimension.
    res : string
        Specifies the image resolution.
    ctype : string
        Specifies the channel type.
    ccount : int
        Specifies the channel count of the image.

    Returns
    -------
    :numpy.Array
    '''

    if (qry != ''):
        example_rows = imdata.query(qry).to_frame(to=n+1)
    else:
        example_rows = imdata.to_frame(to=n+1)
    medical_dimensions = example_rows[dim]
    medical_formats = example_rows[ctype]
    medical_binaries = example_rows[image]
    medical_resolutions = example_rows[res]
    return get_image_array(medical_binaries, medical_dimensions, medical_resolutions, medical_formats, n, ccount)

