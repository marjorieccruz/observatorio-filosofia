"""Série histórica do ES: Ensino Médio (Censo 2015-2025) e AFD municipal (2017-2025)."""
import pandas as pd, zipfile, glob, io, re
cols = ['NU_ANO_CENSO','CO_MUNICIPIO','NO_MUNICIPIO','CO_ENTIDADE','TP_DEPENDENCIA','TP_LOCALIZACAO','TP_SITUACAO_FUNCIONAMENTO','QT_MAT_MED','QT_DOC_MED','QT_TUR_MED']
partes = []
for z in sorted(glob.glob('microdados_censo_escolar_20??.zip')):
    with zipfile.ZipFile(z) as zf:
        nome = [n for n in zf.namelist() if re.search(r'dados/microdados_ed_basica_\d{4}\.csv$', n, re.I)][0]
        with zf.open(nome) as f:
            df = pd.read_csv(f, sep=';', encoding='latin1', usecols=lambda c: c in cols+['SG_UF'], low_memory=False)
    df = df[(df.SG_UF=='ES') & (df.TP_SITUACAO_FUNCIONAMENTO==1)]
    partes.append(df.drop(columns=['SG_UF'])); print(z, len(df))
# 2025: tabelas separadas por tema
d = glob.glob('_trabalho/censo25/*/dados/')[0]
k = ['NU_ANO_CENSO','CO_MUNICIPIO','NO_MUNICIPIO','CO_ENTIDADE','TP_DEPENDENCIA','TP_LOCALIZACAO']
def ler(a, c):
    x = pd.read_csv(glob.glob(d+a)[0], sep=';', encoding='latin1', usecols=lambda n: n in k+c+['SG_UF'])
    return x[x.SG_UF=='ES'].drop(columns='SG_UF')
e25 = ler('Tabela_Docente*', ['QT_DOC_MED']).merge(ler('Tabela_Turma*', ['QT_TUR_MED']), on=k, how='outer')
try: e25 = e25.merge(ler('Tabela_Matricula*', ['QT_MAT_MED']), on=k, how='left')
except Exception as ex: print('matricula 2025 nao extraida:', ex)
partes.append(e25)
esc = pd.concat(partes, ignore_index=True)
esc = esc[esc.QT_TUR_MED.fillna(0) > 0]
dep = {1:'Federal',2:'Estadual',3:'Municipal',4:'Privada'}
esc['DEPENDENCIA'] = esc.TP_DEPENDENCIA.map(dep)
esc.to_csv('dados_processados/es_escolas_em_serie.csv', index=False)
mun = esc.groupby(['NU_ANO_CENSO','CO_MUNICIPIO','NO_MUNICIPIO']).agg(
    escolas_em=('CO_ENTIDADE','nunique'), matriculas_em=('QT_MAT_MED','sum'),
    docentes_em=('QT_DOC_MED','sum'), turmas_em=('QT_TUR_MED','sum')).reset_index()
mun.to_csv('dados_processados/es_municipios_em_serie.csv', index=False)
