# PROTOCOLO DE VERSIONAMENTO — TRILOGIA SOL LIMA

## Objetivo
Garantir que cada avanço importante da trilogia seja rastreável, comparável e recuperável, sem depender apenas da memória do chat.

## Duas camadas de segurança
1. **Histórico do Git:** toda alteração relevante deve gerar commit descritivo. A versão anterior continua recuperável pelo histórico do repositório.
2. **Snapshots de etapa:** ao concluir um marco importante, criar uma cópia imutável dentro de `ETAPAS/` com nome sequencial e data. Essa cópia nunca é sobrescrita.

## Regra dos arquivos vivos
Arquivos como `MAPA_MAE.md`, `MAPA_VISUAL.md`, `STATUS.md` e manuscritos em desenvolvimento representam sempre o estado canônico atual e podem evoluir.

## Regra dos snapshots
Antes de iniciar uma nova fase estrutural, salvar o estado anterior em:

`<PASTA_DO_LIVRO>/ETAPAS/NN_NOME_DA_ETAPA_AAAA-MM-DD.md`

Exemplos:
- `00_ESTRUTURA_BASE_2026-09-10.md`
- `01_AUDITORIA_DO_METODO_2026-09-11.md`
- `02_ARQUITETURA_CAPITULOS_2026-09-13.md`
- `03_MANUSCRITO_ALFA_2026-09-20.md`

Snapshots são históricos. Nunca editar um snapshot antigo para fazê-lo parecer atual.

## Histórico legível
Cada livro deve manter `HISTORICO_ETAPAS.md` contendo:
- número e nome da etapa;
- data;
- estado de entrada;
- mudanças realizadas;
- decisões principais;
- pendências;
- arquivo/snapshot correspondente;
- próxima etapa.

## Status
Usar:
- ⬜ vazio
- ◐ em apuração
- ◑ estruturado
- ● escrito
- ◉ em revisão
- ✓ fechado

## Regra para chats paralelos
Antes de editar um arquivo vivo:
1. reler o arquivo atual no GitHub;
2. reler `HISTORICO_ETAPAS.md` do livro;
3. confirmar qual etapa está ativa;
4. trabalhar apenas na pasta da frente designada;
5. ao concluir um marco, atualizar `STATUS.md` e `HISTORICO_ETAPAS.md` e criar snapshot antes de iniciar a etapa seguinte.

## Regra de segurança editorial
Nenhuma etapa concluída deve desaparecer por reescrita silenciosa. Se uma decisão for substituída, registrar o que mudou e por quê.

## Princípio
**O arquivo vivo mostra onde estamos. O snapshot mostra de onde viemos. O commit prova o que mudou.**

Versão inicial: 10/09/2026.