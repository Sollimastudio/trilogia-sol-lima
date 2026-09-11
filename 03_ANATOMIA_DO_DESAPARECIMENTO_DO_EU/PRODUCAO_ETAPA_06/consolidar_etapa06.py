#!/usr/bin/env python3
"""Consolidação pontual da ETAPA 06. Não agenda trabalho nem sobrescreve marcos.
Executar da raiz do repositório. Recusa base divergente; nunca realiza force push.
A revisão editorial foi feita antes da execução. Este script verifica estrutura
 e integridade, não qualidade literária, diagnóstico ou aprovação autoral.
"""
from pathlib import Path
import collections
import difflib
import hashlib
import json
import re

ROOT = Path('03_ANATOMIA_DO_DESAPARECIMENTO_DO_EU')
DATE = '2026-09-11'
SNAPSHOT = 'ETAPAS/06_PARTE_V_LIBERDADE_2026-09-11.md'
RX = r"\b[\wÀ-ÿ]+(?:[-’'][\wÀ-ÿ]+)*\b"
BLOCKS = [
    '17_ABERTURA_E_FUGA_COGNITIVA.md',
    '18_PROPOSITO_EMPRESTADO.md',
    '19_QUANDO_O_OUTRO_VIRA_FUNCAO.md',
    '20_AUTENTICIDADE_E_FECHAMENTO.md',
]
EXPECTED = {
    'MANUSCRITO_CANONICO.md': '02ea8037ae0a363e17a1aab8d99059c276deb58b',
    'STATUS.md': '091b514c7d361e4c21b8ec638f3d4952ac3538a1',
    'HISTORICO_ETAPAS.md': '138c850e261ef330d98b26e00b2048990b57c1b5',
    'REFERENCIAS_DE_TRABALHO.md': '42d9f91263802e9457e41811aad51789598fb415',
    'MAPA_MAE.md': '47214305d5b0aae8074ea41f5b9faf4d868cb364',
    'PROMPT_PROXIMA_ETAPA_07.md': 'a13b560a2aed37153cb8126976c655e8ccae2005',
    'PRODUCAO_ETAPA_06/17_ABERTURA_E_FUGA_COGNITIVA.md': '373468688680fc2d50653143f96c882416b6afae',
    'PRODUCAO_ETAPA_06/18_PROPOSITO_EMPRESTADO.md': 'ab382386a254ff63f36079c581a1e6657146f2f6',
    'PRODUCAO_ETAPA_06/19_QUANDO_O_OUTRO_VIRA_FUNCAO.md': 'f45c47f26cdee8949c47173ce4b2a613119093ae',
    'PRODUCAO_ETAPA_06/20_AUTENTICIDADE_E_FECHAMENTO.md': '590b1fdead79384aa5fb48cb2a42c79351caaf05',
    'PRODUCAO_ETAPA_06/REFERENCIAS_ACRESCIMO.md': 'b074d0651d609d39548b5115bbdc9dde3914e741',
}


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def words(text: str) -> int:
    return len(re.findall(RX, text))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


require(ROOT.is_dir(), 'Execute da raiz do repositório.')
require(not (ROOT / SNAPSHOT).exists(), 'Snapshot já existe. Nada será reexecutado.')
original = {}
for name, expected in EXPECTED.items():
    data = (ROOT / name).read_bytes()
    require(blob(data) == expected, f'Base divergente: {name}; releia e reconcilie.')
    original[name] = data.decode('utf-8')
old_snapshots = {
    str(p.relative_to(ROOT)): p.read_bytes()
    for p in (ROOT / 'ETAPAS').glob('*.md')
}
require(len(old_snapshots) == 7, 'Conjunto histórico divergiu do marco de leitura.')
require(blob(old_snapshots['ETAPAS/05_PARTE_IV_EU_EMPRESTADO_2026-09-10.md']) == EXPECTED['MANUSCRITO_CANONICO.md'], 'Marco 05 não corresponde à base.')
old = original['MANUSCRITO_CANONICO.md']
require(words(old) == 46591, 'Contagem da base inesperada.')
changes = []
outputs = {}


def replace_once(text: str, before: str, after: str, path: str, reason: str) -> str:
    require(text.count(before) == 1, f'Substituição ambígua ou ausente em {path}: {before[:80]}')
    changes.append({'arquivo': path, 'antes': before, 'depois': after, 'ocorrencias': 1, 'motivo': reason})
    return text.replace(before, after, 1)


revised_base = replace_once(old,
    '**Estado:** manuscrito canônico vivo — ETAPA 05',
    '**Estado:** manuscrito canônico vivo — ETAPA 06',
    'MANUSCRITO_CANONICO.md', 'Atualizar o marco de produção, sem alterar prosa anterior.')
revised_base = replace_once(revised_base,
    '**Data de consolidação desta etapa:** 10/09/2026',
    '**Data de consolidação desta etapa:** 11/09/2026',
    'MANUSCRITO_CANONICO.md', 'Registrar a data local real da ETAPA 06; manter datas históricas e de fontes.')
texts = {name: original['PRODUCAO_ETAPA_06/' + name] for name in BLOCKS}
texts[BLOCKS[1]] = replace_once(texts[BLOCKS[1]],
    'No capítulo anterior a esta parte, Sônia precisou examinar o uso de sua agenda pela associação.',
    'Na Parte IV, Sônia precisou examinar o uso de sua agenda pela associação.',
    'PRODUCAO_ETAPA_06/' + BLOCKS[1],
    'Corrigir remissão: Sônia pertence ao capítulo 14, não ao capítulo 16 imediatamente anterior à Parte V.')
texts[BLOCKS[3]] = replace_once(texts[BLOCKS[3]],
    'Ele não exige legitimamente que ela continue amando para evitar tristeza, embora possa sentir esse desejo.',
    'A tristeza dele não lhe concede o direito de exigir que ela permaneça na relação, embora possa desejar sua permanência.',
    'PRODUCAO_ETAPA_06/' + BLOCKS[3],
    'Retirar ambiguidade sintática no contracaso de Carolina; preservar sentimento legítimo e direito de manter o não.')
part = '\n\n---\n\n'.join(texts[name].strip() for name in BLOCKS) + '\n'
manuscript = revised_base.rstrip() + '\n\n---\n\n' + part
require(words(part) == 12189 and words(manuscript) == 58780, 'Contagem final diverge da revisão local.')
mb = manuscript.encode('utf-8')
require(blob(mb) == 'b8755b32b6ef28124ea151967a9b230bd2c89a24', 'Texto montado difere do revisado e previsto localmente.')
require(sha256(mb) == '52c905f8502f18a3b2a087582f71a19515f8c512b681ea5d764ad273552be637', 'SHA-256 inesperado.')
chapter_matches = list(re.finditer(r'(?m)^# CAPÍTULO (\d+)\s*$', manuscript))
require([int(m.group(1)) for m in chapter_matches] == list(range(1, 21)), 'Capítulos não estão em sequência única.')
require(re.findall(r'(?m)^# PARTE ([IVX]+) —', manuscript) == ['I', 'II', 'III', 'IV', 'V'], 'Partes inválidas.')
for title in ['# NOTA DA AUTORA', '# NOTA CONCEITUAL', '# INTRODUÇÃO']:
    require(len(re.findall(r'(?m)^' + re.escape(title) + r'\s*$', manuscript)) == 1, 'Moldura inicial ausente ou duplicada.')
require(not re.search(r'(?im)^\s*(TODO|TBD|\[INSERIR|\[A DESENVOLVER)', part), 'Marcador de prosa futura encontrado.')
per_chapter = {}
for m in chapter_matches:
    following = re.search(r'(?m)^# ', manuscript[m.end():])
    end = m.end() + following.start() if following else len(manuscript)
    per_chapter[int(m.group(1))] = words(manuscript[m.start():end])
require({n: per_chapter[n] for n in range(17,21)} == {17:2651,18:2832,19:2971,20:2791}, 'Extensão por capítulo inesperada.')
prior_qa = json.loads((ROOT / 'QA_ETAPA_05.json').read_text(encoding='utf-8'))
require(all(per_chapter[int(n)] == v for n,v in prior_qa['palavras_por_capitulo'].items()), 'Capítulo anterior foi alterado sem previsão.')
paras = collections.Counter(p.strip() for p in re.split(r'\n\s*\n', manuscript) if words(p) >= 35)
duplicates = [{'texto': p, 'ocorrencias': c} for p,c in paras.items() if c > 1]
require(not duplicates, 'Rever parágrafos longos exatamente duplicados antes de integrar.')
for name in BLOCKS:
    if texts[name] != original['PRODUCAO_ETAPA_06/' + name]:
        outputs['PRODUCAO_ETAPA_06/' + name] = texts[name]
outputs['MANUSCRITO_CANONICO.md'] = manuscript
outputs['PARTE_V_ETAPA_06.md'] = part
outputs[SNAPSHOT] = manuscript
outputs['DIFF_TEXTO_ANTERIOR_ETAPA_06.patch'] = ''.join(difflib.unified_diff(
    old.splitlines(keepends=True), revised_base.splitlines(keepends=True),
    fromfile='ETAPA_05/MANUSCRITO_CANONICO.md', tofile='ETAPA_06/TEXTO_HERDADO_REVISADO.md'))

prompt = replace_once(original['PROMPT_PROXIMA_ETAPA_07.md'],
    'Rafaelemployee não é Davi mentorado;',
    'Rafael, o funcionário, não é Davi, o participante da formação;',
    'PROMPT_PROXIMA_ETAPA_07.md', 'Corrigir resíduo de redação em inglês e tornar explícita a distinção entre os dois casos.')
outputs['PROMPT_PROXIMA_ETAPA_07.md'] = prompt
refs = original['REFERENCIAS_DE_TRABALHO.md'] + '\n\n---\n\n' + original['PRODUCAO_ETAPA_06/REFERENCIAS_ACRESCIMO.md'].strip() + '\n'
require(refs.startswith(original['REFERENCIAS_DE_TRABALHO.md']), 'Bibliografia herdada não preservada.')
outputs['REFERENCIAS_DE_TRABALHO.md'] = refs
changes.append({'arquivo':'REFERENCIAS_DE_TRABALHO.md', 'operacao':'acrescimo', 'antes':'',
    'depois': original['PRODUCAO_ETAPA_06/REFERENCIAS_ACRESCIMO.md'],
    'motivo':'Acrescentar cinco fontes novas e ampliar o destino da R04-03 reconferida, preservando a bibliografia anterior.'})

status = original['STATUS.md']
status = replace_once(status, '**Atualizado:** 10/09/2026', '**Atualizado:** 11/09/2026', 'STATUS.md', 'Atualizar data do estado vivo.')
status = replace_once(status,
    '| Manuscrito canônico novo | ● | `MANUSCRITO_CANONICO.md` contém abertura + Partes I–IV, capítulos 1–16. |',
    '| Manuscrito canônico novo | ● | `MANUSCRITO_CANONICO.md` contém abertura + Partes I–V, capítulos 1–20. |',
    'STATUS.md', 'Registrar a extensão real integrada, sem declarar os 24 capítulos concluídos.')
status = replace_once(status,
    '| Parte V — Quando Fugir de Si Parece Liberdade | ◐ | Próxima frente: ETAPA 06, Caps. 17–20, conforme prompt específico. |',
    '| Parte V — Quando Fugir de Si Parece Liberdade | ◉ | Caps. 17–20 escritos e revisados, integrados ao marco 06; leitura autoral pendente. |',
    'STATUS.md', 'Registrar texto escrito e manter aprovação autoral pendente.')
status = replace_once(status,
    '| Parte VI — O Retorno da Autoria | ◐ | Legado forte + escrita nova de diferenciação/luto/permanecer em si. |',
    '| Parte VI — O Retorno da Autoria | ◐ | Próxima frente: ETAPA 07, Caps. 21–24 e epílogo. |',
    'STATUS.md', 'Preparar continuidade no retorno da autoria, não outra arquitetura.')
status = replace_once(status,
    '| Pesquisa e referências | ◑ | Registros das Partes II–III preservados; cinco fontes da Parte IV verificadas e registradas com limites; não se trata de revisão sistemática. |',
    '| Pesquisa e referências | ◑ | Registros anteriores preservados; Parte V com cinco fontes novas e R04-03 reconferida, todas com acesso e limites registrados; não é revisão sistemática. |',
    'STATUS.md', 'Atualizar escopo factual efetivamente consultado.')
status = replace_once(status, '### Marco atual — ETAPA 05', '### Marco histórico — ETAPA 05', 'STATUS.md', 'Preservar o marco anterior como histórico.')
old_tail = status[status.index('## ETAPA ATIVA / PRÓXIMA'):]
new_tail = f'''### Marco atual — ETAPA 06

**ETAPA 06 — Parte V: Quando Fugir de Si Parece Liberdade:** escrita, revisão e integração executadas; leitura e aprovação autoral pendentes.

- Parte V: 12.189 palavras, incluindo abertura e fechamento.
- Manuscrito acumulado: 58.780 palavras; capítulos 1–20.
- Capítulos novos: 17 — 2.651; 18 — 2.832; 19 — 2.971; 20 — 2.791.
- Snapshot: `{SNAPSHOT}`.
- Git blob: `{blob(mb)}`.
- SHA-256: `{sha256(mb)}`.
- Sete arquivos históricos anteriores de ETAPAS preservados byte a byte.
- Registros: `REGISTRO_EDITORIAL_ETAPA_06.md`, `REVISOES_ETAPA_06.json`, `QA_ETAPA_06.json`, diff do cabeçalho e referências atualizadas.

## ETAPA ATIVA / PRÓXIMA

**ETAPA 07 — PARTE VI: O RETORNO DA AUTORIA + EPÍLOGO**

Executar `PROMPT_PROXIMA_ETAPA_07.md`: abertura, capítulos 21–24, fechamento da Parte VI e epílogo. Diferenciar pessoa, herança e performance; reconhecer perdas sem impor fases clínicas; sustentar autoria sem personagem perfeito. Revisar o conjunto e preparar a ETAPA 08 de lapidação global.

**Execução editorial não equivale a aprovação autoral, validação clínica, conclusão dos 24 capítulos ou liberação para publicação.**
'''
status = replace_once(status, old_tail, new_tail, 'STATUS.md', 'Encerrar produção 06 e abrir 07; manter todos os marcos anteriores e limites da conclusão.')
outputs['STATUS.md'] = status

mapa = original['MAPA_MAE.md']
mapa = replace_once(mapa,
    '**Arquitetura consolidada na ETAPA 01; produção atualizada até a ETAPA 05**',
    '**Arquitetura consolidada na ETAPA 01; produção atualizada até a ETAPA 06**',
    'MAPA_MAE.md', 'Atualizar apenas o progresso, sem mudar seis partes e 24 capítulos.')
mapa = replace_once(mapa, '**Data:** 10/09/2026', '**Data:** 11/09/2026', 'MAPA_MAE.md', 'Data do arquivo vivo.')
old_state = mapa[mapa.index('# 10. ESTADO'):]
new_state = '''# 10. ESTADO

ETAPAS 00 e 01 preservadas; ETAPAS 02–06 com escrita e revisão executadas. O manuscrito vivo contém abertura e Partes I–V, capítulos 1–20, totalizando 58.780 palavras lexicais. Aprovação autoral e publicação continuam pendentes.

A arquitetura de seis partes e 24 capítulos não foi alterada. Permanecem as distinções de fusão científica/metáfora autoral, aprendizagem/ocupação e dependência material/adesão. A Parte V acrescenta atividade/função, propósito, reconhecimento do outro e responsabilidade sem culpar quem sofreu violência. Personagens anteriores preservados; nova remissão a Sônia corrigida para Parte IV.

Próxima frente: **ETAPA 07 — Parte VI: O Retorno da Autoria + Epílogo**, capítulos 21–24. Seguir `PROMPT_PROXIMA_ETAPA_07.md`, `STATUS.md` e `QA_ETAPA_06.json`. O fechamento da redação não substitui a lapidação global e a aprovação de Sol.
'''
mapa = replace_once(mapa, old_state, new_state, 'MAPA_MAE.md', 'Atualizar estado da produção e próxima etapa, preservando todo o mapa conceitual anterior.')
outputs['MAPA_MAE.md'] = mapa

history_add = f'''\n---\n\n## ETAPA 06 — PARTE V: QUANDO FUGIR DE SI PARECE LIBERDADE

**Data local:** 11/09/2026.  
**Entrada:** Abertura + Partes I–IV, 46.591 palavras, capítulos 1–16; blob `{EXPECTED['MANUSCRITO_CANONICO.md']}`.  
**Estado:** escrita, revisão e integração executadas; leitura e aprovação autoral pendentes.

### Corpo de livro

Escritos abertura (423 palavras), capítulo 17 (2.651), capítulo 18 (2.832), capítulo 19 (2.971), capítulo 20 (2.791) e fechamento (521). Parte V integral: 12.189 palavras. Manuscrito acumulado: 58.780. Método lexical Unicode herdado, incluindo títulos e chamadas autor-data, não paginação.

Renato permite distinguir descanso e adiamento; Rute e Dalva, finalidade e necessidade de função; Henrique e André, amizade e utilidade; Bárbara e Camila, decisão legítima e execução com efeitos evitáveis. Carolina e Aline sustentam contracasos. Nenhum episódio foi atribuído à biografia de Sol.

### Revisão e legado

Consultados por função antigos capítulos 18–21, trechos do 3 e início do 24, além de passagens de pertencimento. Preservados benefícios reais do alívio, missão recebida que pode tornar-se própria, função relacional legítima, humanidade sem concessão de acesso e responsabilidade sem culpa pela violência. O legado não foi alterado.

Corrigida no novo capítulo 18 a remissão a Sônia (Parte IV, capítulo 14); esclarecida uma frase do contracaso de Carolina. No manuscrito herdado, apenas cabeçalho de etapa/data mudou: a prosa dos capítulos 1–16 permanece literal. Corrigido resíduo de redação no prompt 07. Controle e bibliografia atualizados com registro de mudanças.

Cinco fontes novas foram verificadas; Ryan/Deci (R04-03) foi reconferida e recebeu uso adicional. Acesso limitado a resumos dos autores/metadados dos artigos e HTML oficial da OMS, explicitado nas referências. Sem validação clínica ou revisão sistemática.

### Integridade

Snapshot integral `{SNAPSHOT}`. Git blob `{blob(mb)}`; SHA-256 `{sha256(mb)}`. Vinte capítulos, cinco partes e molduras iniciais preservados. Sete arquivos históricos anteriores de ETAPAS intactos. Histórico anterior mantido integralmente por acréscimo. QA e diff distinguem contagem/estrutura de revisão editorial.

### Pendências

Leitura autoral; Parte VI e epílogo; lapidação global de cadência, redundâncias, bibliografia e termos; figuras legadas sem inspeção visual nesta etapa; diagramação e validação de formatos de publicação.

### Próxima frente

ETAPA 07 — Parte VI: O Retorno da Autoria + Epílogo. Seguir `PROMPT_PROXIMA_ETAPA_07.md` e preparar ETAPA 08 após a primeira redação completa. Nenhuma publicação foi autorizada por este registro.
'''
outputs['HISTORICO_ETAPAS.md'] = original['HISTORICO_ETAPAS.md'] + history_add
changes.append({'arquivo':'HISTORICO_ETAPAS.md','operacao':'acrescimo','antes':'','depois':history_add,'motivo':'Preservar integralmente a história anterior e adicionar o marco 06.'})

report = f'''# REGISTRO EDITORIAL — ETAPA 06

**Livro:** Anatomia do Desaparecimento do Eu / Fuga Identitária.  
**Autora:** Sol Lima.  
**Data local:** 11/09/2026.  
**Estado:** escrita, revisão e integração executadas; aprovação autoral e publicação pendentes.

## 1. Entrega mensurável

| Bloco | Palavras lexicais |
|---|---:|
| Abertura + Partes I–IV herdadas | 46.591 |
| Texto herdado após atualização de cabeçalho | 46.591 |
| Abertura da Parte V | 423 |
| Capítulo 17 — Fuga cognitiva | 2.651 |
| Capítulo 18 — Propósito emprestado | 2.832 |
| Capítulo 19 — Quando o outro vira função | 2.971 |
| Capítulo 20 — Autenticidade sem responsabilidade | 2.791 |
| Fechamento da Parte V | 521 |
| Parte V integral | 12.189 |
| Manuscrito acumulado | 58.780 |

Regex lexical Unicode herdada; inclui títulos e chamadas autor-data. O texto inicial dos quatro blocos tinha 12.188 palavras; duas correções produzem 12.189. Não se infere paginação de bytes. Nenhum capítulo foi substituído por uma sinopse.

## 2. O que foi escrito

**17:** Renato começa assistindo a uma série por descanso legítimo e usa a continuação para adiar uma conversa possível sobre uma atividade compartilhada. A reflexão distingue lazer, alívio, preparação, impedimento material e adiamento. Aline preserva o jogo como prazer, sem dever de produtividade. Critérios clínicos de jogos são delimitados, não transportados a toda rotina.

**18:** Rute conclui uma turma de leitura; Dalva envia uma carta sem precisar da professora. O êxito abre ambivalência e permite distinguir finalidade, função e valor pessoal. Missão recebida não é falsa por origem; motivos misturados não são fraude. O capítulo não exige testemunho público ou missão salvadora de quem sofreu. A reconstrução profunda permanece para Parte VI.

**19:** Henrique procura André como revisor e demora a ouvir a mudança importante na vida do amigo. O foco passa da necessidade de espelho ao efeito sobre quem foi reduzido a função. Relações profissionais delimitadas e assimetrias temporárias não são desumanização por definição. O contracaso da designer mantém fronteiras sem negar dignidade. Reconhecer humanidade não obriga a proximidade com quem ameaça.

**20:** Bárbara deseja encerrar as oficinas, mas anuncia antes de conversar sobre compromissos próximos com Camila. A decisão pode ser legítima e seu método ainda exigir reparação. Não há violência ou coerção nesse caso; saídas emergenciais não são usadas como exemplos de irresponsabilidade. Carolina conserva uma recusa necessária sem exigir que o ex-parceiro aprove. Reparação não compra absolvição.

**Moldura:** os cadernos de estudo e a pergunta ainda sem conversa abrem a parte. O fechamento retorna à possibilidade de usar até o livro como adiamento e prepara desidentificação, luto e sustentação, sem entregar uma identidade pronta.

## 3. Auditoria acumulada — Abertura + Partes I–V

A revisão confrontou a progressão conceitual, os casos, remissões, uso de fontes, redundâncias e fronteiras. Os capítulos novos avançam da vida organizada pelo Eu emprestado para saídas aparentes que podem conservar sua função. As notas iniciais continuam não diagnósticas. Fusão científica não foi redefinida como apagamento pessoal. Dependência material não foi confundida com adesão interna.

O capítulo 17 não repete Marina: ela reage a sinais antigos; Renato utiliza uma atividade para adiar uma resposta que pode reconhecer. O 18 não repete a agenda de Sônia: o conflito aparece quando a missão obtém um resultado e já não exige a mesma posição. O 19 não repete a terceirização do espelho: examina o espaço retirado do outro. O 20 aproxima-se deliberadamente da fronteira de Luiza sobre compromissos, mas avança para anúncio público, terceiros afetados e reparação com consequências, não apenas emprego impreciso de uma palavra.

A Parte V preserva contracasos e a legitimidade de descanso, propósito compartilhado, funções profissionais e recusa segura. As cenas não resolvem magicamente relações nem tornam sofrimento prova de má decisão. Não foram acrescentados episódios biográficos de Sol. Morte em Vida conserva autópsia, perdão/autoperdão e Sepultamento Simbólico; Reposicione-se conserva sua arquitetura metodológica.

## 4. Alterações efetivas

A prosa anterior ao capítulo 17 não exigiu substituição nesta rodada; manteve-se literal, com duas atualizações apenas no cabeçalho do arquivo vivo. Não se inventou uma correção estrutural para justificar revisão.

No capítulo 18, Sônia era referida como se estivesse no capítulo imediatamente anterior à parte; a remissão passa a Parte IV. No capítulo 20, uma frase ambígua sobre Carolina foi reescrita para separar tristeza e direito de exigir permanência. O prompt 07 recebeu correção de um resíduo de redação em inglês. Metadados, estado, referências e histórico foram sincronizados. `REVISOES_ETAPA_06.json` preserva antes/depois/motivo; o diff do texto herdado contém apenas cabeçalho.

Há ecos semânticos deliberados, sobretudo sobre autoria não ser autossuficiência. O teste de duplicação exata de parágrafos com pelo menos 35 palavras não encontrou repetições; isso não prova ausência de redundância conceitual. A maior fragmentação das primeiras partes e a frequência de ressalvas/metadiscurso permanecem como tarefas da lapidação global. Não foram reescritas páginas inteiras apenas por preferência tardia de ritmo.

## 5. Patrimônio reaproveitado

Fonte legada: Camada 11 de `Sollimastudio/fuga-identit-ria-`, blob `d7f0b2dda2e1c07e870d5365bca59e32b385312a`.

Antigos 18–21 forneceram distinções entre atividade e função, propósito e identidade total, pessoa e utilidade, direito e responsabilidade. Trechos do antigo 3 reforçam alívio sem diagnóstico automático; o início do 24 conserva finalidade construída em vez de missão pronta. Passagens do antigo 23 contribuíram como contraste de vínculo e saída. Não houve nova auditoria integral de todo o legado nem inspeção de figuras. A arquitetura antiga não foi transportada.

Os novos casos foram escritos para funções específicas. Nomes do legado como Helena e Lívia não foram usados para transplantar biografias incompatíveis. As cenas atuais permanecem compostas, não evidências empíricas.

## 6. Fontes e limites

`REFERENCIAS_DE_TRABALHO.md` recebeu R06-01 a R06-05 e nota de ampliação da R04-03 já existente. Sonnentag/Fritz: recuperação; Sirois/Pychyl: regulação de humor e procrastinação; OMS: condição clínica específica; Sheldon/Elliot: metas autoconcordantes; Gruenfeld e colegas: poder e utilidade de alvos sociais; Ryan/Deci: autonomia junto de competência e vínculo.

A consulta aos artigos foi por resumo primário dos autores e metadados; não se declara leitura integral. O documento oficial da OMS foi consultado em HTML. Não houve atualização de estatísticas de plataformas, aplicação jurídica a casos reais, ensaio clínico ou revisão sistemática. O ensaio não usa pesquisa como validação automática de suas metáforas. A bibliografia anterior foi preservada, não declarada externamente revalidada nesta etapa.

## 7. Integridade

- Base: `{EXPECTED['MANUSCRITO_CANONICO.md']}`.
- Manuscrito e snapshot: `{blob(mb)}`.
- SHA-256: `{sha256(mb)}`.
- Bytes: {len(mb)}.
- Snapshot: `{SNAPSHOT}`.
- Vinte capítulos em sequência, cinco partes, notas e introdução.
- Sete arquivos históricos anteriores de ETAPAS preservados.
- Histórico e referências anteriores conservados por acréscimo.

O QA verifica estrutura, contagem e integridade, não validação clínica, ausência total de redundância ou aprovação literária de Sol. A recuperação e conferência posterior ao salvamento devem constar de `VERIFICACAO_FINAL_ETAPA_06.md`.

A rotina de GitHub Actions usada para exportar e integrar é temporária e deve ser removida após a conferência. O script é um registro reproduzível que recusa base divergente e snapshot existente, não uma automação permanente.

## 8. Próxima execução e pendências

ETAPA 07 — Parte VI: O Retorno da Autoria + Epílogo, conforme prompt específico. A primeira redação dos 24 capítulos só estará completa depois dessa escrita. Permanecem leitura/aprovação de Sol, lapidação global, bibliografia final, revisão visual de figuras, diagramação e validação dos formatos. Nenhum PDF, DOCX, EPUB ou KPF foi produzido ou validado nesta etapa.
'''
outputs['REGISTRO_EDITORIAL_ETAPA_06.md'] = report
qa = {
    'etapa':'06', 'data_local':DATE, 'escopo':'Abertura e Partes I–V; capítulos 1–20',
    'metodo_contagem':'regex lexical Unicode '+RX+'; inclui títulos e chamadas autor-data; não equivale a páginas',
    'palavras_base':words(old), 'palavras_base_apos_revisao':words(revised_base),
    'palavras_parte_V_antes_revisao':sum(words(original['PRODUCAO_ETAPA_06/'+n]) for n in BLOCKS),
    'palavras_parte_V':words(part), 'palavras_manuscrito':words(manuscript),
    'palavras_abertura_parte_V':words(part[:part.index('# CAPÍTULO 17')]),
    'palavras_fechamento_parte_V':words(part[part.index('# FECHAMENTO DA PARTE V'):]),
    'palavras_por_capitulo':per_chapter, 'bytes_manuscrito':len(mb),
    'git_blob_base':EXPECTED['MANUSCRITO_CANONICO.md'],
    'git_blob_manuscrito_e_snapshot':blob(mb), 'sha256_manuscrito_e_snapshot':sha256(mb),
    'snapshot':SNAPSHOT, 'snapshot_identico':True, 'capitulos':list(range(1,21)),
    'partes':['I','II','III','IV','V'],
    'snapshots_anteriores_sha256':{n:sha256(v) for n,v in old_snapshots.items()},
    'blocos_de_entrada':{n:EXPECTED['PRODUCAO_ETAPA_06/'+n] for n in BLOCKS},
    'blocos_revisados':{n:{'git_blob_sha':blob(texts[n].encode()),'palavras':words(texts[n])} for n in BLOCKS},
    'alteracoes_documentadas':len(changes),
    'prosa_anterior_alterada':False, 'cabecalho_anterior_alterado':True,
    'paragrafos_exatamente_duplicados_35_palavras':duplicates,
    'aprovacao_autoral':False,'publicacao_aprovada':False,
    'limites':'QA estrutural e revisão editorial; não validação clínica, revisão sistemática, prova de ausência de redundância semântica ou liberação de publicação.'
}
outputs['REVISOES_ETAPA_06.json'] = json.dumps({'etapa':'06','data_local':DATE,'substituicoes_e_acrescimos':changes}, ensure_ascii=False, indent=2)+'\n'
outputs['QA_ETAPA_06.json'] = json.dumps(qa, ensure_ascii=False, indent=2)+'\n'
# Não sobrescrever um marco independente criado depois da leitura.
for name in outputs:
    if name not in EXPECTED:
        require(not (ROOT/name).exists(), f'Entrega já existe: {name}; interrompido.')
manifest_name = 'ARQUIVOS_INTEGRACAO_ETAPA_06.json'
require(not (ROOT/manifest_name).exists(), 'Manifesto do marco já existe.')
manifest = {n:{'git_blob_sha':blob(t.encode()),'sha256':sha256(t.encode()),'bytes':len(t.encode())} for n,t in outputs.items()}
outputs[manifest_name] = json.dumps({'etapa':'06','data_local':DATE,'arquivos':manifest,'observacao':'Não inclui a si mesmo; conteúdos de leitura e script já versionados antes da integração.'},ensure_ascii=False,indent=2)+'\n'
# Toda validação prévia terminou; escritas confinadas ao Livro 3.
for name,text in outputs.items():
    target=ROOT/name
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(text.encode('utf-8'))
require((ROOT/SNAPSHOT).read_bytes() == (ROOT/'MANUSCRITO_CANONICO.md').read_bytes(), 'Snapshot difere após escrita.')
for name,data in old_snapshots.items():
    require((ROOT/name).read_bytes() == data, f'Marco histórico alterado: {name}')
require((ROOT/'HISTORICO_ETAPAS.md').read_text().startswith(original['HISTORICO_ETAPAS.md']), 'Histórico anterior foi truncado.')
require((ROOT/'REFERENCIAS_DE_TRABALHO.md').read_text().startswith(original['REFERENCIAS_DE_TRABALHO.md']), 'Referências anteriores foram truncadas.')
print(json.dumps({'etapa':'06','palavras':words(manuscript),'parte_V':words(part),'blob':blob(mb),'sha256':sha256(mb),'snapshot_identico':True,'arquivos_escritos':len(outputs)},ensure_ascii=False))
