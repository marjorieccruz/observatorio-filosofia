"""Extrai indicadores de filosofia do ES a partir do Censo Escolar e do AFD (escolas)."""
import pandas as pd, glob, sys
ANO = int(sys.argv[1]) if len(sys.argv) > 1 else 2025
d = glob.glob(f'_trabalho/censo{str(ANO)[2:]}/*/dados/')[0]
id_cols = ['NU_ANO_CENSO','NO_MUNICIPIO','CO_MUNICIPIO','NO_ENTIDADE','CO_ENTIDADE','TP_DEPENDENCIA','TP_LOCALIZACAO']
def ler(arq, extra):
    df = pd.read_csv(glob.glob(d+arq)[0], sep=';', encoding='latin1', usecols=lambda c: c in id_cols+extra+['SG_UF'])
    return df[df.SG_UF=='ES'].drop(columns='SG_UF')
doc = ler('Tabela_Docente*', ['QT_DOC_MED','QT_DOC_BAS_DISC_FILOSOFIA','QT_DOC_BAS_DISC_SOCIOLOGIA'])
tur = ler('Tabela_Turma*', ['QT_TUR_MED','QT_TUR_BAS_DISC_FILOSOFIA','QT_TUR_BAS_DISC_SOCIOLOGIA'])
esc = doc.merge(tur, on=id_cols, how='outer')
arq_afd = glob.glob(f'_trabalho/afd{str(ANO)[2:]}/*/*.xlsx')[0]
bruto = pd.read_excel(arq_afd, header=None, nrows=20)
linha = bruto.index[bruto[0]=='NU_ANO_CENSO'][0]  # linha do cabecalho varia entre anos
afd = pd.read_excel(arq_afd, header=linha)
afd = afd[afd.SG_UF=='ES'][['CO_ENTIDADE']+[f'MED_CAT_{i}' for i in range(1,6)]]
afd = afd.replace('--', pd.NA)
esc = esc.merge(afd, on='CO_ENTIDADE', how='left')
dep = {1:'Federal',2:'Estadual',3:'Municipal',4:'Privada'}
esc['DEPENDENCIA'] = esc.TP_DEPENDENCIA.map(dep)
esc = esc[(esc.QT_TUR_MED.fillna(0)>0) | (esc.QT_DOC_BAS_DISC_FILOSOFIA.fillna(0)>0)]
esc['TEM_FILOSOFIA'] = esc.QT_TUR_BAS_DISC_FILOSOFIA.fillna(0) > 0
esc.to_csv(f'dados_processados/es_escolas_{ANO}.csv', index=False)
mun = esc.groupby(['CO_MUNICIPIO','NO_MUNICIPIO']).agg(
    escolas_com_em=('QT_TUR_MED', lambda s: (s.fillna(0)>0).sum()),
    escolas_com_filosofia=('TEM_FILOSOFIA','sum'),
    docentes_filosofia=('QT_DOC_BAS_DISC_FILOSOFIA','sum'),
    turmas_filosofia=('QT_TUR_BAS_DISC_FILOSOFIA','sum'),
    turmas_em=('QT_TUR_MED','sum'),
    docentes_sociologia=('QT_DOC_BAS_DISC_SOCIOLOGIA','sum'),
    afd_em_grupo1_medio=('MED_CAT_1', lambda s: pd.to_numeric(s, errors='coerce').mean()),
).reset_index()
mun.insert(0,'ANO',ANO)
mun.to_csv(f'dados_processados/es_municipios_{ANO}.csv', index=False)
print(len(esc),'escolas;', len(mun),'municipios'); print(mun.describe().round(1).T)
