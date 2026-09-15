# Skill: MOLDURA 1 — Padrão NUAKEY (aprovado, versão v6)

## Padrão salvo (15/09/2026)
| Elemento | Especificação |
|---|---|
| Moldura | Linha branca, **colada na borda (margem 8px)**, espessura 2px, cantos arredondados (raio ~12px), **gap de 40% no meio da borda inferior** (pra logo encaixar) |
| Opacidade moldura | **50%** |
| Logo | `logos/nuaky_crop.png` (NUAKY com brilho + copyright), **50% de opacidade** |
| Tamanho logo | ~39% da largura do vídeo (280px em 720px) |
| Posição logo | Centralizada (x), centro vertical em **89% da altura** (dentro do gap inferior) |
| Vídeo | Mantém áudio original, h264 CRF 19, mesmo formato/resolução |

## Como aplicar (script automático)
```bash
python3 molduras/apply_moldura.py VIDEO_ENTRADA.mp4 -o SAIDA.mp4
# com moldura customizada (ex.: nova moldura enviada):
python3 molduras/apply_moldura.py VIDEO.mp4 --moldura molduras/nova_moldura.png -o SAIDA.mp4
```
Parâmetros opcionais: `--moldura-op 0.5` `--logo-op 0.5` `--logo-w 0.39` `--logo-y 0.89` `--margem 8`

## Fluxo de entrega
1. Video entra em `videos/` (upload do usuário via GitHub)
2. Saida vai para `entregas/NUAKY_edit_vN.mp4` (commit + push)
3. Link raw enviado ao usuário

## Assets
- `frame_moldura1_720x724.png` — moldura MOLDURA 1 pronta (720x724, 50%)
- `logos/nuaky_crop.png` — logo NUAKEY (100%, opacidade ajustada no script)
- `logos/frame_720_v2.png` — cópia da moldura
