#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from etilt.config.conf import (
        logger,
        # KM,
        # D,
        # N_DISTANCE,
        # TERRAIN_DELTA,
        SAMPLES_PERCENTAGE,
    )

from time_advanced import (
        time_advanced,
        ta_translation
    )

from utilities.input_data import (
        get_cells_df,
        get_ta_df,
        get_period_data,
    )

from utilities.neighborhood import (
        neighborhood,
    )

def print_df(df=None):
    type_ = str(type(df))
    print(f'type_ {type_}')
    if type_ == "<class 'pandas.core.frame.DataFrame'>":
        print(df.columns)
        print(df.shape)
        print(df.head(200))
    if type_ == "<class 'pandas.core.series.Series'>":
        print(df.head(40))

'''
La idea es obtener data de un kpi, y hacer comparaciones, para el mismo kpi, entre 2 periodos.
- por ahora el periodo es un día parcial (15:00 -->)
'''
def mid_term_evaluation(kpi = None, df= None):
    logger.info(f'mid_term_evaluation:')

    l = ['Cell_Name', kpi,]
    df = df[l]
    # print_df(df=df) # debug

    result = df.groupby('Cell_Name').agg({kpi: ['mean', 'min', 'max']})
    result.reset_index(inplace=True)
    # print(result) # debug
    # print(result.columns) # debug

    return result

def kpy_study(kpi=None,period_x=None,period_y=None):
    logger.info(f'kpy_study:')

    df_x = get_period_data(period = period_x)
    # print_df(df=df_x) # debug
    # print(df_x.columns) # debug

    df_y = get_period_data(period = period_y)
    # print_df(df=df_x) # debug

    res_x = mid_term_evaluation(kpi=kpi, df=df_x)
    res_y = mid_term_evaluation(kpi=kpi, df=df_y)

    l = ['Cell_Name', 'mean_x', 'min_x', 'max_x',]
    res_x.columns = l
    # print(res_x) # debug

    l = ['Cell_Name_y', 'mean_y', 'min_y', 'max_y',]
    res_y.columns = l
    # print(res_y) # debug

    merged_df = pd.merge(res_x, res_y, how="inner", left_on='Cell_Name', right_on='Cell_Name_y').drop_duplicates()
    # print(merged_df) # debug
    # print(merged_df.columns) # debug

    l = ['Cell_Name', 'mean_x', 'min_x', 'max_x', 'mean_y', 'min_y', 'max_y']
    merged_df = merged_df[l]
    # print(merged_df) # debug
    # print(merged_df.columns) # debug

    merged_df['mean_diff_x'] = merged_df['mean_x'] - merged_df['mean_y']
    merged_df['mean_diff_pct_x'] = merged_df['mean_diff_x'] * 100 / merged_df['mean_x']

    return merged_df
    # print(merged_df) # debug
    # merged_df.to_excel(f'data/mid_term_{kpi}.xlsx', index = False)

def kpis_comparison(period_x=None,period_y=None,kpi_list=None):
    logger.info(f'kpis_comparison:')

    merged_df = None

    first_iter = True

    for kpi in kpi_list:
        kpi_df = kpy_study(kpi=kpi,period_x=period_x,period_y=period_y)
        l = list(kpi_df.columns)
        # print(l) # debug

        l = list(map(lambda x: x if x == 'Cell_Name' else f'{kpi}_{x}', l))
        # print(l) # debug
        kpi_df.columns = l

        if first_iter:
            merged_df = kpi_df
            first_iter = False
        else:
           merged_df = pd.merge(merged_df, kpi_df, how="inner", left_on='Cell_Name', right_on='Cell_Name').drop_duplicates()

        # print(merged_df) # debug
        print(merged_df.columns) # debug

    return merged_df

def ta_study(cell_df=None,data_df=None,percentaje=None,sufix=None):
    ta_df = pd.merge(cell_df, data_df, how="inner", left_on='Cell_Name', right_on='Cell_Name').drop_duplicates()
    l = ['Cell_Name', 'dateid_hour', f'ta_{percentaje}{sufix}']
    ta_df.columns = l
    return ta_df

def ta_acum(ta_df=None):
    logger.info(f'ta_acum:')

    l = ['Cell_Name', 'L_RA_TA_UE_Index0','L_RA_TA_UE_Index1',
        'L_RA_TA_UE_Index2','L_RA_TA_UE_Index3', 'L_RA_TA_UE_Index4',
        'L_RA_TA_UE_Index5', 'L_RA_TA_UE_Index6','L_RA_TA_UE_Index7',
        'L_RA_TA_UE_Index8','L_RA_TA_UE_Index9', 'L_RA_TA_UE_Index10',
        'L_RA_TA_UE_Index11',]

    ta_df_ = ta_df[l]
    ta_acum_df = ta_df_.groupby('Cell_Name').sum()
    return ta_acum_df

def ra_columns(sufix=None):
    logger.info(f'ta_columns:')
    return [f'L_RA_TA_UE_Index0{sufix}',
            f'L_RA_TA_UE_Index1{sufix}', f'L_RA_TA_UE_Index2{sufix}',
            f'L_RA_TA_UE_Index3{sufix}', f'L_RA_TA_UE_Index4{sufix}',
            f'L_RA_TA_UE_Index5{sufix}', f'L_RA_TA_UE_Index6{sufix}',
            f'L_RA_TA_UE_Index7{sufix}', f'L_RA_TA_UE_Index8{sufix}',
            f'L_RA_TA_UE_Index9{sufix}', f'L_RA_TA_UE_Index10{sufix}',
            f'L_RA_TA_UE_Index11{sufix}']

# def ta_percentaje_distance( row ):
#     # print(f'TA_COLUMNS={TA_COLUMNS}') # debug
#     total = 0.0
#     for i in range(1,13):
#         total += row[TA_INDEX[i]]
#     parcial_percentage = int(total * SAMPLES_PERCENTAGE / 100)
#     parcial = 0.0
#     for i in range(1,13):
#         parcial += row[TA_INDEX[i]]
#         if parcial >= parcial_percentage:
#             return num_translation[i-1]/1000

distance_index_dir = {f:i for i,f in enumerate(ta_translation)}

def ta_distance_to_percentaje_x( row ):
    index = distance_index_dir[row['ta_95_x']]
    return row[f'L_RA_TA_UE_Index{index}_%_x']

def ta_distance_to_percentaje_y( row ):
    index = distance_index_dir[row['ta_95_y']]
    return row[f'L_RA_TA_UE_Index{index}_%_y']

def main():
    logger.info(f'{__name__}:')
    period_x = '20210112'
    period_y = '20210113' # se asume period_y > period_x
    # kpi_list = ['cqi_avg', 'user_thrp_dl', 'user_avg']

    # result_df = kpis_comparison(period_x=period_x,period_y=period_y,kpi_list=kpi_list)

    # result_df.to_excel(f'data/mid_term.xlsx', index = False)
    # print(result_df) # debug

    # -------------------------------
    percentaje=95
    df_x = get_period_data(period = period_x)
    df_y = get_period_data(period = period_y)

    ta_acum_df_x = ta_acum(ta_df=df_x)
    ta_acum_df_x.reset_index(inplace=True)
    print(ta_acum_df_x) # debug
    print(ta_acum_df_x.columns) # debug

    ta_acum_df_y = ta_acum(ta_df=df_y)
    ta_acum_df_y.reset_index(inplace=True)

    ta_df_x = time_advanced(ta_df=ta_acum_df_x, percentaje=percentaje)
    print(ta_df_x) # debug
    print(ta_df_x.columns) # debug
    # l = ['Cell_Name', 'ta_95']
    l = ['Cell_Name'] + ra_columns(sufix='_%') + ['ta_95']
    ta_df_x = ta_df_x[l]
    # l = ['Cell_Name', 'ta_95_x']
    l = ['Cell_Name'] + ra_columns(sufix='_%_x') + ['ta_95_x']
    ta_df_x.columns = l
    # --------------------------------------------------------
    ta_df_x.reset_index(inplace=True)
    ta_df_x['ta_95_x_real'] = ta_df_x.apply(ta_distance_to_percentaje_x, axis=1)
    # --------------------------------------------------------
    print(ta_df_x) # debug
    print(ta_df_x.columns) # debug


    ta_df_y = time_advanced(ta_df=ta_acum_df_y, percentaje=percentaje)
    # l = ['Cell_Name', 'ta_95']
    l = ['Cell_Name'] + ra_columns(sufix='_%') + ['ta_95']
    ta_df_y = ta_df_y[l]
    # l = ['Cell_Name', 'ta_95_y']
    l = ['Cell_Name'] + ra_columns(sufix='_%_y') + ['ta_95_y']
    ta_df_y.columns = l
    # --------------------------------------------------------
    ta_df_y.reset_index(inplace=True)
    ta_df_y['ta_95_y_real'] = ta_df_y.apply(ta_distance_to_percentaje_y, axis=1)
    # --------------------------------------------------------


    ta_merged_df = pd.merge(ta_df_x, ta_df_y, how="inner", left_on='Cell_Name', right_on='Cell_Name').drop_duplicates()

    l = ['Cell_Name', 'ta_95_x', 'ta_95_x_real', 'ta_95_y','ta_95_y_real']
    ta_merged_df = ta_merged_df[l]


    ta_merged_df.to_excel(f'data/ta_merged.xlsx', index = False)
    print(ta_merged_df) # debug
    print(ta_merged_df.columns) # debug


if __name__ == '__main__':
    main()

    # df_x = get_period_data(period = period_x)
    # df_y = get_period_data(period = period_y)

    # percentaje=95
    # df_x = time_advanced(ta_df=df_x, percentaje=percentaje)
    # print(df_x) # debug
    # print(df_x.columns) # debug

    # df_y = time_advanced(ta_df=df_y, percentaje=percentaje)
    # print(df_y) # debug
    # print(df_y.columns) # debug

    # # idea:
    # # l = ['Cell_Name', 'dateid_hour', f'ta_{percentaje}']
    # # ta_x_df = df_x[l]
    # # l = ['Cell_Name']
    # # cell_df_x = result_df[l]
    # # ta_x_df = pd.merge(cell_df_x, ta_x_df, how="inner", left_on='Cell_Name', right_on='Cell_Name').drop_duplicates()
    # # l = ['Cell_Name', 'dateid_hour', f'ta_{percentaje}_x']
    # # ta_x_df.columns = l
    # # print(ta_x_df) # debug
    # # print(ta_x_df.columns) # debug


    # l = ['Cell_Name']
    # t = ['Cell_Name', 'dateid_hour', f'ta_{percentaje}']
    # ta_x_df  = ta_study(cell_df=result_df[l],data_df=df_x[t],
    #                         percentaje=percentaje,sufix='_x')
    # print(ta_x_df) # debug
    # print(ta_x_df.columns) # debug

    # ta_y_df  = ta_study(cell_df=result_df[l],data_df=df_y[t],
    #                         percentaje=percentaje,sufix='_y')
    # print(ta_y_df) # debug
    # print(ta_y_df.columns) # debug

    # ta_df = ta_merge(ta_x_df=ta_x_df,ta_y_df=ta_y_df)
    # print(ta_df) # debug
    # print(ta_df.columns) # debug

    # -------------------------------

    # result_df.to_excel(f'data/mid_term.xlsx', index = False)
    # print(result_df) # debug
