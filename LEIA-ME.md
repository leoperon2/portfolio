# Portfólio — Leopoldo Peron

Site estático publicado no GitHub Pages: https://leoperon2.github.io/portfolio/

## Estrutura (idiomas)
| Idioma | Endereço | Arquivo |
|---|---|---|
| Português (principal) | `/portfolio/` | `index.html` |
| English | `/portfolio/en/` | `en/index.html` |
| Español | `/portfolio/es/` | `es/index.html` |
| Italiano | `/portfolio/it/` | `it/index.html` |

Ordem das bandeiras: PT, EN, ES, IT. `/pt/` só redireciona para a raiz.
Imagens e vídeos ficam em `img/`; as páginas dentro de subpastas usam `../img/...`.

## Fonte da verdade
**Este repositório é a versão oficial.** As quatro páginas foram ajustadas direto aqui
(layout, galerias, vídeos, textos). O gerador antigo do PC (`build.py`, `template.html`,
`traducoes.txt`, `i18n.py`) NÃO conhece essas mudanças: rodar `python build.py` + `publicar.py`
e enviar `publicar/` sobrescreveria o site com a versão antiga, com português na raiz.

## Como atualizar
Peça as mudanças ao Claude (edita, publica no `main` e mantém os 4 idiomas iguais).
Para voltar uma versão: histórico de commits no GitHub.

## Lançamento
`robots.txt` bloqueia buscadores enquanto o site é rascunho. No lançamento, trocar por
`User-agent: *` + `Allow: /` e remover qualquer `<meta name="robots" content="noindex">`.
