#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from etilt.config.conf import (
        logger,
        KM,
        D,
        N_DISTANCE,
        TERRAIN_DELTA,
    )

from utilities.input_data import (
        get_cells_df,
    )

from utilities.numpy_functions import (
        haversine_distance,
        bearing,
    )

def neighborhood():
    logger.info(f'neighborhood:')
    cells_df = get_cells_df()

    l = ['SITE', 'LAT', 'LON']
    sites_df = cells_df[l].drop_duplicates()

    sites_df['key'] = 1
    merged_df = pd.merge(sites_df, sites_df, on ='key').drop("key", 1)

    merged_df = merged_df[merged_df['SITE_x'] != merged_df['SITE_y']]

    merged_df['distance_'] = haversine_distance(
                                merged_df['LAT_x'].values ,
                                merged_df['LON_x'].values,
                                merged_df['LAT_y'].values ,
                                merged_df['LON_y'].values
                                )

    merged_df['bearing_'] = bearing(
                                merged_df['LAT_x'].values ,
                                merged_df['LON_x'].values,
                                merged_df['LAT_y'].values ,
                                merged_df['LON_y'].values
                                )

    # logger.info(f'neighborhood: merged_df.columns {merged_df.columns}')
    l = ['SITE_x', 'SITE_y', 'distance_','bearing_']
    merged_df = merged_df[l]

    merged_df = merged_df[merged_df['distance_'] <= KM]

    l = ['SITE', 'CELLNAME', 'AZIMUTH']
    merged_df = pd.merge(cells_df[l], merged_df, how="inner", left_on='SITE', right_on='SITE_x')

    merged_df = merged_df[(merged_df['bearing_'] > merged_df['AZIMUTH'] - D) & (merged_df['bearing_'] < merged_df['AZIMUTH'] + D)]

    l = ['CELLNAME', 'distance_']
    merged_df.sort_values(by=l, inplace=True)

    l = ['CELLNAME']
    neighborhood_df = merged_df.groupby(l).head(N_DISTANCE)

    l = ['CELLNAME', 'AZIMUTH', 'SITE_x', 'SITE_y', 'distance_',
       'bearing_']
    return neighborhood_df[l]


if __name__ == '__main__':
    neighborhood_df = neighborhood()
