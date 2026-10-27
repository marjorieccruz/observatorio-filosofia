# Observatório do Ensino de Filosofia

Protótipo de painel de dados sobre o ensino de filosofia na educação básica, começando pelo Espírito Santo.

- `scripts/`: leitura dos arquivos originais do INEP (Censo Escolar e AFD), que ficam fora do repositório.
- `dados/`: tabelas processadas usadas pelo site.
- `*.qmd`: páginas do site (Quarto).
- `docs/`: site gerado, publicado pelo GitHub Pages.

Para atualizar: rodar os scripts na pasta com os zips do INEP, copiar `dados_processados/*.csv` para `dados/` e executar `quarto render`.
