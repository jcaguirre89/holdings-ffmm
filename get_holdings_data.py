import requests
import pandas as pd
from io import StringIO
from argparse import ArgumentParser

URL = 'http://www.cmfchile.cl/institucional/estadisticas/ffm_download.php'

columns_EXTR = {
    'Run Fondo': 'run_fondo',
    'Nombre Fondo': 'nombre_fondo',
    'FFM_6020100': 'nemotecnico',
    'FFM_6020200': 'nombre_emisor',
    'FFM_6020300': 'pais_emisor',
    'FFM_6020400': 'tipo_instrumento',
    'FFM_6020500': 'fecha_vencimiento_instrumento',
    'FFM_6020600': 'situacion_instrumento',
    'FFM_6020700': 'clasificacion_riesgo',
    'FFM_6020800': 'codigo_grupo_empresarial',
    'FFM_6020900': 'cantidad_unidades',
    'FFM_6021000': 'tipo_unidades',
    'FFM_tir_6021111': 'TIR',
    'FFM_par_6021111': 'valor_par',
    'FFM_rel_6021111': 'valor_relevante',
    'FFM_6021112': 'codigo_valorizacion',
    'FFM_6021113': 'base_tasa',
    'FFM_6021114': 'tipo_interes',
    'FFM_6021200': 'valorizacion_al_cierre_en_miles',
    'FFM_6021300': 'codigo_moneda_valorizacion',
    'FFM_6021400': 'codigo_pais_transaccion',
    'FFM_6021511': 'porcentaje_capital_emisor',
    'FFM_6021512': 'porcentaje_activos_emisor',
    'FFM_6021513': 'porcentaje_activos_fondo'
}

columns_NACI = {
    'Run Fondo': 'run_fondo',
    'Nombre Fondo': 'nombre_fondo',
    'FFM_6010100': 'nemotecnico',
    'FFM_6010211': 'rut_emisor',
    'FFM_6010212': 'digito_verificador_rut_emisor',
    'FFM_6010300': 'pais_emisor',
    'FFM_6010400': 'tipo_instrumento',
    'FFM_6010500': 'fecha_vencimiento_instrumento',
    'FFM_6010600': 'situacion_instrumento',
    'FFM_6010700': 'clasificacion_riesgo',
    'FFM_6010800': 'codigo_grupo_empresarial',
    'FFM_6010900': 'cantidad_unidades',
    'FFM_6011000': 'tipo_unidades',
    'FFM_TIR_6011111': 'TIR',
    'FFM_PAR_6011111': 'valor_par',
    'FFM_REL_6011111': 'valor_relevante',
    'FFM_6011112': 'codigo_valorizacion',
    'FFM_6011113': 'base_tasa',
    'FFM_6011114': 'tipo_interes',
    'FFM_6011200': 'valorizacion_al_cierre_en_miles',
    'FFM_6011300': 'codigo_moneda_valorizacion',
    'FFM_6011400': 'codigo_pais_transaccion',
    'FFM_6011511': 'porcentaje_capital_emisor',
    'FFM_6011512': 'porcentaje_activos_emisor',
    'FFM_6011513': 'porcentaje_activos_fondo'
}


def get_holdings(month, year, portfolio):
    """
    gets holdings data for all mutual funds in Chile for a given month/year
    combination
    :param: month: `str`: zero-padded number from 1 to 12.
    :param: year: `str`: year to search
    :param: portfolio: `str`: one of: 
        - 'NACI'
        - 'EXTR'
    """
    # TODO: Perform validation on args
    body = {'aa': year, 'mm': month, 'cartera': portfolio}
    s = requests.Session()
    # requests without user-agent in headers are forbidden
    headers = {
        'User-Agent':
        ('Mozilla/5.0 (Macintosh;'
         'Intel Mac OS X 10_11_5) AppleWebKit/537.36'
         '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')
    }
    resp = s.post(URL, data=body, headers=headers)
    data = resp.content.decode('utf-8-sig')
    df = pd.read_csv(StringIO(data), sep=';')

    df['month'] = month
    df['year'] = year
    df['portfolio'] = portfolio

    return df


def _rename_cols(df):
    """ cleans df with holdings data """
    df = df.copy()
    portfolio = df.iloc[0]['portfolio']
    if portfolio == 'EXTR':
        rename_cols = columns_EXTR
    else:
        rename_cols = columns_NACI

    df.rename(columns=rename_cols, inplace=True)
    return df


def save_holdings(df):
    """ save holdings """
    # TODO: switch to SQL
    df.to_csv(f'data/out.csv')


def _build_parser():
    parser = ArgumentParser()
    parser.add_argument('--month',
                        type=str,
                        dest='month',
                        help='month of the year',
                        required=True)
    parser.add_argument('--year',
                        type=str,
                        dest='year',
                        help='Year',
                        required=True)
    return parser


def clean_holdings(month, year):
    """ cleans holdings """
    national = get_holdings(month=month, year=year, portfolio='NACI')
    national = _rename_cols(national)
    foreign = get_holdings(month=month, year=year, portfolio='EXTR')
    foreign = _rename_cols(foreign)

    df = pd.concat([national, foreign], sort=False)
    print(df.head())

    df.sort_values('run_fondo', axis=1, inplace=True)

    return df


def main():
    """ main function """
    parser = _build_parser()
    options = parser.parse_args()
    month = options.month
    year = options.year

    df = clean_holdings(month, year)

    save_holdings(df)


if __name__ == '__main__':
    main()
