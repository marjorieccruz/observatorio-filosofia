# Observatório do Ensino de Filosofia

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23695823.svg)](https://doi.org/10.5281/zenodo.23695823)

Protótipo de painel de dados sobre o ensino de filosofia na educação básica, começando pelo Espírito Santo.

- `scripts/`: leitura dos arquivos originais do INEP (Censo Escolar e AFD), que ficam fora do repositório.
- `dados/`: tabelas processadas usadas pelo site.
- `*.qmd`: páginas do site (Quarto).
- `docs/`: site gerado, publicado pelo GitHub Pages.

Para atualizar: rodar os scripts na pasta com os zips do INEP, copiar `dados_processados/*.csv` para `dados/` e executar `quarto render`.

## Como citar

Da Cruz, M. (2026). *Observatório do Ensino de Filosofia: protótipo (Espírito Santo)* (v0.1.0) [Software]. Zenodo. https://doi.org/10.5281/zenodo.23695823
