"""AFD municipal do ES, Ensino Medio, 2017-2025."""
import pandas as pd, zipfile, glob, io, re
# AFD municipal, Ensino Médio, total de localização e dependência
afd = []
for z in sorted(glob.glob('AFD_20??_MUNICIPIOS.zip')):
    with zipfile.ZipFile(z) as zf:
        nome = [n for n in zf.namelist() if n.endswith('.xlsx') and '~$' not in n][0]
        b = io.BytesIO(zf.read(nome))
    bruto = pd.read_excel(b, header=None, nrows=20)
    lin = bruto.index[bruto[0].astype(str).str.lower().isin(['nu_ano_censo','ano'])].max()
    b.seek(0); x = pd.read_excel(b, header=lin)
    # nomes mudam entre anos (2017: ano/sigla/AFD_MED1; depois: NU_ANO_CENSO/SG_UF/MED_CAT_1); usamos posicao
    base = x.iloc[:, :7].copy(); base.columns = ['NU_ANO_CENSO','NO_REGIAO','SG_UF','CO_MUNICIPIO','NO_MUNICIPIO','NO_CATEGORIA','NO_DEPENDENCIA']
    cat = [c for c in x.columns if re.fullmatch(r'(MED_CAT_|AFD_MED)\d', str(c), re.I)]
    for i, c in enumerate(cat, 1): base[f'MED_CAT_{i}'] = x[c]
    x = base[base.SG_UF=='ES'].drop(columns=['NO_REGIAO','SG_UF'])
    afd.append(x); print(z, len(x), x.NO_CATEGORIA.unique(), x.NO_DEPENDENCIA.unique())
afd = pd.concat(afd).replace('--', pd.NA)
afd.to_csv('dados_processados/es_afd_municipios_medio.csv', index=False)
