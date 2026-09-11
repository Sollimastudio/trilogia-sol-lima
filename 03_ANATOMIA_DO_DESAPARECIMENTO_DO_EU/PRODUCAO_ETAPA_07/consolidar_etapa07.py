#!/usr/bin/env python3
"""Consolidação pontual da ETAPA 07; sem rede, credenciais ou força de push."""
from pathlib import Path
import collections
import difflib
import hashlib
import json
import re
import sys

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('03_ANATOMIA_DO_DESAPARECIMENTO_DO_EU')
SNAP = 'ETAPAS/07_PARTE_VI_EPILOGO_2026-09-11.md'
P = 'PRODUCAO_ETAPA_07/'
PATTERN = r"\b[\wÀ-ÿ]+(?:[-’'][\wÀ-ÿ]+)*\b"
EXPECTED = {
 'MANUSCRITO_CANONICO.md': 'b8755b32b6ef28124ea151967a9b230bd2c89a24',
 'STATUS.md': '95f4b538514ba45f3aa48c99f2f172f51547c8a3',
 'HISTORICO_ETAPAS.md': 'a951c3eba8c264f46201c41ee13fe3c9e8863535',
 'MAPA_MAE.md': '95abe3a4995a76797708a2a5a3a88f53e69cd1bb',
 'REFERENCIAS_DE_TRABALHO.md': 'e931c4d2e390fcdda81319ee838b986b97e0a3c5',
 'PROMPT_PROXIMA_ETAPA_08.md': 'f18928f6d9293b0ff97348b2830f11673e88b756',
 'ETAPAS/00_ESTRUTURA_BASE_2026-09-10.md': '14ac78e7ebe71d81f7acfc028de5f74e751e9d43',
 'ETAPAS/01_AUDITORIA_CONSOLIDACAO_2026-09-10.md': '2a51d605b50f253ea291999cc9ba65214f8a687e',
 'ETAPAS/02_ABERTURA_PARTE_I_2026-09-10.md': '13265d2d5f671c30441cdd51b4b3587e8da93617',
 'ETAPAS/03_PARTE_II_BLOCO_PRODUCAO_2026-09-10.md': '0bd3bcebb6e73abcd2ee29f6d4a08f3fee053bf4',
 'ETAPAS/03_PARTE_II_ESPELHOS_2026-09-10.md': 'a34f0038fd6339846c257c46a88050f55052b7c5',
 'ETAPAS/04_PARTE_III_ANATOMIA_OCUPACAO_2026-09-10.md': '5bdf895efd012b9b3c6b62d2b322971b264b9e29',
 'ETAPAS/05_PARTE_IV_EU_EMPRESTADO_2026-09-10.md': '02ea8037ae0a363e17a1aab8d99059c276deb58b',
 'ETAPAS/06_PARTE_V_LIBERDADE_2026-09-11.md': 'b8755b32b6ef28124ea151967a9b230bd2c89a24',
 P+'21_ABERTURA_E_DESIDENTIFICACAO.md': 'cdd010a7d644ac1d7455985a75b1113823279625',
 P+'22_HERANCA_E_PERFORMANCE.md': 'b595f5f8fa930eb7cd473cbf648567d112162a89',
 P+'23_LUTO_E_PERTENCIMENTO.md': 'c7f7f864f4ac1e313a61c02fe4481b201062c24b',
 P+'24_PERMANECER_EM_SI.md': 'f5e84bcf14c5aaa3f40a9534484b5078a24a4341',
 P+'99_FECHAMENTO_E_EPILOGO.md': 'fbb33288ac4cd6412ed3ba9c50fc9da473dffc3b',
 P+'REFERENCIAS_ACRESCIMO.md': '93e4fe1c3eb56aaa6a85d59690f4ab9d6398d56c',
}

def git_blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def words(text):
    return len(re.findall(PATTERN, text))

def fmt(number):
    return f'{number:,}'.replace(',', '.')

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def encode_json(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2)+'\n'

original = {}
for rel, expected in EXPECTED.items():
    data = (ROOT/rel).read_bytes()
    require(git_blob(data) == expected, 'Base divergente; interrompido: '+rel)
    original[rel] = data
require(not (ROOT/SNAP).exists(), 'Snapshot já existe; não sobrescrever.')
require(not (ROOT/'QA_ETAPA_07.json').exists(), 'Marco 07 já existe; revisar antes de repetir.')
texts = {rel: data.decode('utf-8') for rel, data in original.items()}
revisions = []

def replace(rel, old, new, reason, category):
    require(texts[rel].count(old) == 1, 'Substituição não unívoca: '+rel+' / '+old[:75])
    texts[rel] = texts[rel].replace(old, new, 1)
    revisions.append(dict(arquivo=rel, operacao='substituicao', categoria=category,
                          antes=old, depois=new, ocorrencias=1, motivo=reason))

def append(rel, addition, reason):
    old = texts[rel]
    texts[rel] = old+addition
    revisions.append(dict(arquivo=rel, operacao='acrescimo', categoria='registro',
                          antes='', depois=addition, prefixo_anterior_preservado=True,
                          antes_git_blob=git_blob(old.encode()), motivo=reason))

replace('MANUSCRITO_CANONICO.md',
        '**Estado:** manuscrito canônico vivo — ETAPA 06',
        '**Estado:** manuscrito canônico vivo — ETAPA 07',
        'Atualizar etapa; a data 11/09/2026 continua correta.', 'cabecalho')
replace(P+'21_ABERTURA_E_DESIDENTIFICACAO.md',
        'O capítulo não encerra sua história. Devolve-lhe algo menor e mais decisivo:',
        'Aquela conversa não encerra sua história. Devolve-lhe algo menor e mais decisivo:',
        'Retomar a ocorrência de Rute, reduzindo metadiscurso sem alterar a cena.', 'prosa_nova')
replace(P+'23_LUTO_E_PERTENCIMENTO.md',
        'Iyer e colegas acompanharam estudantes na transição para a universidade em dois estudos longitudinais. Múltiplos pertencimentos e a compatibilidade percebida entre identidades antigas e novas participaram da adaptação e da identificação com o novo grupo.',
        'Em dois estudos longitudinais, Iyer e colegas examinaram estudantes antes da entrada na universidade e dois meses depois. Múltiplos pertencimentos e compatibilidade percebida entre identidades antigas e novas estiveram associados à identificação com o novo grupo, por sua vez relacionada ao bem-estar.',
        'Precisar intervalo observado e relações investigadas, sem generalizar a transição estudantil para saída de coerção.', 'prosa_nova')

names = ['21_ABERTURA_E_DESIDENTIFICACAO.md', '22_HERANCA_E_PERFORMANCE.md',
         '23_LUTO_E_PERTENCIMENTO.md', '24_PERMANECER_EM_SI.md', '99_FECHAMENTO_E_EPILOGO.md']
new = '\n\n---\n\n'.join(texts[P+n].strip() for n in names)+'\n'
base = texts['MANUSCRITO_CANONICO.md']
manuscript = base.rstrip()+'\n\n---\n\n'+new
require(words(original['MANUSCRITO_CANONICO.md'].decode()) == 58780, 'Contagem da base inesperada.')
require(base.split('# NOTA DA AUTORA', 1)[1] == original['MANUSCRITO_CANONICO.md'].decode().split('# NOTA DA AUTORA', 1)[1], 'Prosa anterior alterada fora do escopo.')
heads = list(re.finditer(r'(?m)^# CAPÍTULO (\d+)\s*$', manuscript))
require([int(m.group(1)) for m in heads] == list(range(1,25)), 'Capítulos fora de sequência ou duplicados.')
require(re.findall(r'(?m)^# PARTE ([IVX]+) —', manuscript) == ['I','II','III','IV','V','VI'], 'Partes inconsistentes.')
require(len(re.findall(r'(?m)^# EPÍLOGO —', manuscript)) == 1, 'Epílogo ausente/duplicado.')
for heading in ['# NOTA DA AUTORA', '# NOTA CONCEITUAL', '# INTRODUÇÃO']:
    require(manuscript.count(heading) == 1, 'Moldura ausente/duplicada: '+heading)
counts = {}
for m in heads:
    stop = re.search(r'(?m)^# ', manuscript[m.end():])
    end = m.end()+stop.start() if stop else len(manuscript)
    counts[m.group(1)] = words(manuscript[m.start():end])
new_words, total_words = words(new), words(manuscript)
opening_words = words(new[:new.index('# CAPÍTULO 21')])
closing_words = words(new[new.index('# FECHAMENTO DA PARTE VI'):new.index('# EPÍLOGO —')])
epilogue_words = words(new[new.index('# EPÍLOGO —'):])
require(11000 <= new_words <= 16000, 'Conferir extensão da nova parte.')
for chapter in range(21,25):
    require(counts[str(chapter)] >= 2600, 'Capítulo novo abaixo do desenvolvimento previsto.')
require(800 <= epilogue_words <= 1400, 'Conferir epílogo.')
require(total_words == words(base)+new_words, 'Contagens não fecham.')
blob, digest = git_blob(manuscript.encode()), sha256(manuscript.encode())
paragraphs = [re.sub(r'\s+', ' ', x.strip()) for x in manuscript.split('\n\n') if words(x)>=35]
duplicates = [{'ocorrencias': c, 'texto': p} for p,c in collections.Counter(paragraphs).items() if c>1]

append('REFERENCIAS_DE_TRABALHO.md', '\n\n---\n\n'+texts[P+'REFERENCIAS_ACRESCIMO.md'].rstrip()+'\n',
       'Três referências novas R07-01 a R07-03; R04-03 reconferida com novo destino, sem alegar revisão sistemática.')
replace('STATUS.md',
        '`MANUSCRITO_CANONICO.md` contém abertura + Partes I–V, capítulos 1–20.',
        '`MANUSCRITO_CANONICO.md` contém abertura + Partes I–VI, capítulos 1–24 e epílogo; primeira redação completa, aprovação autoral pendente.',
        'Registrar extensão real do corpo escrito.', 'controle')
replace('STATUS.md',
        '| Parte VI — O Retorno da Autoria | ◐ | Próxima frente: ETAPA 07, Caps. 21–24 e epílogo. |',
        '| Parte VI — O Retorno da Autoria | ◉ | Caps. 21–24 escritos, revisados e integrados; snapshot da ETAPA 07 preservado. |',
        'Atualizar produção sem declarar aprovação de Sol.', 'controle')
replace('STATUS.md',
        '| Epílogo | ◐ | Epílogo legado preservado como base; fechamento precisa terminar em presença identitária sustentável. |',
        '| Epílogo | ◉ | O lugar que só você pode ocupar escrito; imagem da lista/pasta/mesa, sem identidade pronta nem ponte invertida ao Livro 2. |',
        'Registrar epílogo efetivamente escrito.', 'controle')
replace('STATUS.md',
        '| Pesquisa e referências | ◑ | Registros anteriores preservados; Parte V com cinco fontes novas e R04-03 reconferida, todas com acesso e limites registrados; não é revisão sistemática. |',
        '| Pesquisa e referências | ◑ | Registros preservados; Parte VI com três referências novas e R04-03 reconferida; bibliografia final e auditoria global na ETAPA 08. |',
        'Registrar pesquisa utilizada e limite da verificação.', 'controle')
replace('STATUS.md', '### Marco atual — ETAPA 06', '### Marco histórico — ETAPA 06',
        'Preservar números e hashes da etapa anterior como históricos.', 'controle')
status_tail = '''## ETAPA ATIVA / PRÓXIMA

**ETAPA 07 — PARTE VI: O RETORNO DA AUTORIA + EPÍLOGO**

Executar `PROMPT_PROXIMA_ETAPA_07.md`: abertura, capítulos 21–24, fechamento da Parte VI e epílogo. Diferenciar pessoa, herança e performance; reconhecer perdas sem impor fases clínicas; sustentar autoria sem personagem perfeito. Revisar o conjunto e preparar a ETAPA 08 de lapidação global.

**Execução editorial não equivale a aprovação autoral, validação clínica, conclusão dos 24 capítulos ou liberação para publicação.**'''
new_tail = f'''### Marco atual — ETAPA 07

**ETAPA 07 — Parte VI: O Retorno da Autoria + Epílogo:** escrita, revisão e integração executadas; primeira redação dos 24 capítulos completa, aprovação de Sol pendente.

- Parte VI e epílogo: {fmt(new_words)} palavras; manuscrito: {fmt(total_words)}.
- Capítulos 21–24: {', '.join(str(i)+' — '+fmt(counts[str(i)]) for i in range(21,25))}.
- Abertura: {opening_words}; fechamento: {closing_words}; epílogo: {fmt(epilogue_words)}.
- Snapshot: `{SNAP}`.
- Git blob: `{blob}`.
- SHA-256: `{digest}`.
- Oito arquivos históricos de ETAPAS preservados. Prosa anterior mantida; somente o cabeçalho avança.
- Registros: `REGISTRO_EDITORIAL_ETAPA_07.md`, `REVISOES_ETAPA_07.json`, `QA_ETAPA_07.json`, diff e referências.
- A conferência posterior ao salvamento será registrada em `VERIFICACAO_FINAL_ETAPA_07.md`.

## ETAPA ATIVA / PRÓXIMA

**ETAPA 08 — AUDITORIA GLOBAL, LAPIDAÇÃO E PREPARAÇÃO EDITORIAL**

Executar `PROMPT_PROXIMA_ETAPA_08.md`: revisar e lapidar o livro acumulado, conferir alegações e bibliografia, avaliar o estado real das figuras e preparar acabamento sem declarar publicação autorizada.

**Primeira redação completa não equivale a aprovação autoral, validação clínica, revisão visual das figuras ou liberação para publicação.**'''
replace('STATUS.md', status_tail, new_tail, 'Encerrar produção do corpo e abrir lapidação global.', 'controle')
replace('MAPA_MAE.md',
        '**Função:** portal de desidentificação. Retirar mentalmente grupo, papel, título, audiência, relacionamento e missão para observar o que depende deles.',
        '**Função:** portal de desidentificação. Suspender a prioridade de uma definição para observar o que ela vinha respondendo; não simular perdas reais nem retirar vínculos, cuidado ou recursos de segurança.',
        'Alinhar a função do capítulo 21 à delimitação realizada na prosa e no prompt 07.', 'controle')
map_start = texts['MAPA_MAE.md'].index('# 10. ESTADO')
old_state = texts['MAPA_MAE.md'][map_start:].rstrip()
new_state = f'''# 10. ESTADO

ETAPAS 00–06 preservadas; ETAPA 07 com abertura da Parte VI, capítulos 21–24, fechamento e epílogo escritos, revisados e integrados. A primeira redação acumulada está completa: {fmt(total_words)} palavras lexicais, notas iniciais, introdução, seis partes, 24 capítulos e epílogo.

A Parte VI e o epílogo acrescentam {fmt(new_words)} palavras. A arquitetura não foi substituída. Rute, Ana, Davi e Augusto retornam em situações novas; não foram inventados episódios biográficos de Sol. A auditoria identitária é autoral e não pontuada. O luto de funções não é diagnóstico; sustentação não promete imunidade, cura ou personagem perfeito.

O legado continua preservado. A prosa anterior permaneceu intacta; o cabeçalho avança e duas formulações novas foram refinadas. Aprovação autoral, lapidação global, bibliografia final, figuras, diagramação e formatos de publicação continuam pendentes.

Próxima frente: **ETAPA 08 — Auditoria Global, Lapidação e Preparação Editorial**, conforme `PROMPT_PROXIMA_ETAPA_08.md`, `STATUS.md` e `QA_ETAPA_07.json`. Não publicar nem declarar aprovação a partir da conclusão da primeira redação.'''
replace('MAPA_MAE.md', old_state, new_state, 'Atualizar progresso e pendências, preservando a arquitetura.', 'controle')
history = f'''\n\n---

## ETAPA 07 — PARTE VI: O RETORNO DA AUTORIA + EPÍLOGO

**Data local:** 11/09/2026. **Estado:** primeira redação acumulada completa; leitura e aprovação autoral pendentes.

Escritos abertura da Parte VI, capítulos 21–24, fechamento e epílogo. A nova produção soma {fmt(new_words)} palavras; o manuscrito acumulado soma {fmt(total_words)}. Método lexical herdado, incluindo títulos e chamadas autor-data; sem inferência de páginas.

Rute distingue pessoa de função; Ana aplica uma auditoria não pontuada a uma ocorrência familiar; Davi reconhece perdas e recursos de um pertencimento ainda em revisão; Augusto corrige uma interferência sem fabricar identidade perfeita. O epílogo devolve tamanho à voz do livro e encerra com pasta, mesa e cadeira, não com o método do Livro 2.

Revisão acumulada de progressão, remissões, personagens, redundâncias e fronteiras. Não foram substituídos trechos da prosa herdada; somente o cabeçalho foi atualizado. Duas correções novas: retorno à conversa de Rute em lugar de metadiscurso e delimitação mais precisa do estudo de Iyer e colegas. O mapa do capítulo 21 foi alinhado ao experimento mental sem perdas forçadas.

Três referências novas, R07-01 a R07-03, e R04-03 reconferida. Consulta a resumos primários/metadados, não leitura integral dos artigos nem revisão sistemática da bibliografia acumulada. Casos compostos não foram apresentados como evidência empírica.

Snapshot: `{SNAP}`. Manuscrito e snapshot: `{blob}`. SHA-256: `{digest}`. Oito arquivos históricos anteriores mantidos. Histórico e referências preservados por acréscimo.

Registros: manuscrito, Parte VI/epílogo separado, registro editorial, revisões, diff, referências, QA, STATUS, mapa-mãe e `PROMPT_PROXIMA_ETAPA_08.md`. Verificação posterior ao salvamento em documento próprio.

**Próxima frente:** ETAPA 08 — auditoria global e lapidação efetiva. Permanecem aprovação de Sol, bibliografia final, avaliação visual de figuras, diagramação e validação de formatos. Nenhum DOCX, PDF, EPUB ou KPF foi produzido ou validado nesta etapa.
'''
append('HISTORICO_ETAPAS.md', history, 'Preservar o histórico anterior integralmente e acrescentar o novo marco.')

record = f'''# REGISTRO EDITORIAL — ETAPA 07

**Autora:** Sol Lima. **Livro:** Anatomia do Desaparecimento do Eu / Fuga Identitária.  
**Data:** 11/09/2026, America/Sao_Paulo.  
**Estado:** primeira redação completa; execução editorial não é aprovação autoral/publicação.

## 1. Entrega concreta

| Bloco | Palavras lexicais |
|---|---:|
| Base herdada e preservada | 58.780 |
| Abertura da Parte VI | {fmt(opening_words)} |
| Capítulo 21 | {fmt(counts['21'])} |
| Capítulo 22 | {fmt(counts['22'])} |
| Capítulo 23 | {fmt(counts['23'])} |
| Capítulo 24 | {fmt(counts['24'])} |
| Fechamento da Parte VI | {fmt(closing_words)} |
| Epílogo | {fmt(epilogue_words)} |
| Parte VI + epílogo | {fmt(new_words)} |
| Manuscrito acumulado | {fmt(total_words)} |

Contagem lexical Unicode herdada, incluindo títulos e chamadas autor-data. Não equivale a paginação. A produção inicial tinha 13.615 palavras; as duas revisões da prosa nova produzem o total acima. Todos os blocos são prosa escrita, não sinopses.

## 2. Progressão entregue

**21:** Rute abre uma manhã sem aula e suspende a mensagem que criaria novas tarefas para os antigos alunos. A função continua verdadeira sem responder pela pessoa inteira. A suspensão mental é delimitada: não pede imaginar mortes, perder moradia ou retirar apoio.

**22:** Ana aceitou consultar um restaurante e recebe tarefas adicionais. O caderno distingue ocorrência, repertório recebido, benefício, exigência, endosso atual, contexto e alcance. Os campos são sobrepostos, autorais e não pontuados. O contracaso conserva uma herança examinada; mudança não recebe aprovação automática.

**23:** Davi vê uma fotografia do grupo que continua sem sua participação igual à anterior. Conserva clientes e dependências ainda em exame. Crachá, projetos e conversa com colega externo mostram perda sem negação de todo benefício. Um coral distingue requisitos legítimos de função de retirada de dignidade. Não se prescrevem estágios de luto, perdão ou reconciliação.

**24:** Augusto volta a ser procurado diretamente e retoma uma negociação já delegada. Corrige a consequência diante da colega e do cliente. Sua experiência continua útil sem justificar comando total. A repetição não apaga todo avanço nem dá direito a absolvição. O perigo novo é representar a pessoa plenamente autoral.

**Fechamento e epílogo:** a voz do livro volta ao tamanho de uma voz. A lista guardada de Rute, a pasta que deixa espaço na mesa e a cadeira encerram por imagem. Não há procissão de todos os personagens, novo fato biográfico de Sol, promessa de cura ou venda de método.

## 3. Auditoria do conjunto — Abertura + Partes I–VI + Epílogo

As perguntas avançam de papéis e funcionamento a espelhos, incorporação, consequências e saídas aparentes; a Parte VI recebe a tarefa de diferenciar, reconhecer perdas e sustentar participação. Não elimina influências nem procura essência pura. A promessa da Nota da Autora de não definir o leitor retorna no capítulo 24 e no epílogo.

Os retornos foram confrontados com os episódios de origem: Ana do capítulo 6, Davi de 10/12, Augusto do 16 e Rute do 18. Marina continua profissional e Lívia criadora; Helena não recebeu a história de Vera. O capítulo 24 dialoga com o automatismo do 15, mas trata da manutenção da mudança e do risco de uma nova identidade de perfeição. O 22 aplica perguntas a uma ocorrência, sem recriar o método de acordos do Livro 2.

**Fronteiras:** Morte em Vida conserva biografia, autópsia, perdão/autoperdão e Sepultamento Simbólico. Reposicione-se conserva sua arquitetura metodológica. O final não manda o leitor para um suposto Livro 2 futuro, não reutiliza a descida da Árvore e não altera o Universo Mestre.

**Redundâncias:** permanecem ecos de autoria não ser autossuficiência, segurança e proporcionalidade; alguns são estruturais, outros merecem condensação global. A cadência mais fragmentada dos primeiros capítulos e a frequência de metadiscurso foram registradas para a ETAPA 08, sem reescrever capítulos inteiros por preferência tardia. Ausência de duplicação exata não significa ausência de repetição semântica.

**Rigor e segurança:** preservadas fusão científica/metáfora, influência/ocupação e dependência material/adesão. Não se mede identidade por clareza verbal ou independência. Não há exercício clínico de exposição, prazo de superação nem apelo a confrontar quem oferece risco. Afirmações empíricas novas são delimitadas à evidência consultada; o ensaio não é um instrumento validado.

## 4. Alterações efetivas

A prosa herdada das notas e capítulos 1–20 foi mantida literalmente. O diff da base registra apenas o cabeçalho ETAPA 06 para 07; a data permanece 11/09/2026. Na prosa nova foram aplicadas duas substituições: retirar o metadiscurso que atribuía ao capítulo a ação de uma conversa de Rute; especificar população, intervalo e relações do estudo de Iyer e colegas. O mapa do capítulo 21 passou a descrever suspensão de prioridade, não simulação de perdas.

`REVISOES_ETAPA_07.json` conserva cada antes/depois/motivo. Atualizações de status, mapa e acréscimos de referências/histórico são classificados como controle, não anunciados como correções de capítulos.

## 5. Patrimônio reaproveitado

Fonte legada: Camada 11 de `Sollimastudio/fuga-identit-ria-`, blob `d7f0b2dda2e1c07e870d5365bca59e32b385312a`. Consultados trechos dos antigos capítulos 22–24 e epílogo, com continuidade dos princípios de 1–3 e 19 já migrados. Não se declarou nova leitura integral de todo o legado.

A Auditoria Metacognitiva foi condensada e aplicada a Ana, sem transportar todas as listas. Pertencimento com diferença, gratidão sem imunidade, luto, direção revisável, recursos materiais e contribuição sem posse foram preservados por função. A antiga convocação final POSICIONE-SE e exercícios extensos do Livro 2 não foram recuperados. Figuras antigas não foram inspeccionadas nem aprovadas nesta execução. O legado não foi alterado.

## 6. Fontes utilizadas e limites

Três registros novos: Ayduk/Kross, Iyer e colegas, Breines/Chen; Ryan/Deci já existente foi reconferido e recebeu destino no capítulo 22. Resumos primários e metadados foram consultados; não se alega leitura integral dos artigos. O texto diferencia associação observada, experimento delimitado e aplicação autoral aos casos compostos. DOI, acesso e limites estão em `REFERENCIAS_DE_TRABALHO.md`.

Esta seleção não é revisão sistemática, não valida desidentificação ou luto das identidades como procedimentos clínicos e não revalida automaticamente toda a bibliografia anterior.

## 7. Integridade preparada e conferida na consolidação

- Base: `{EXPECTED['MANUSCRITO_CANONICO.md']}`.
- Manuscrito e snapshot: `{blob}`.
- SHA-256: `{digest}`.
- Snapshot: `{SNAP}`.
- 24 capítulos, seis partes, notas, introdução e um epílogo.
- Oito snapshots/arquivos históricos anteriores preservados byte a byte.
- Histórico e referências anteriores mantidos como prefixos integrais.

O QA verifica extensão, estrutura e hashes; não prova excelência literária ou ausência de toda redundância. A verificação posterior à recuperação do GitHub deve constar de `VERIFICACAO_FINAL_ETAPA_07.md`. A rotina temporária de integração deve ser retirada depois da conferência; o script permanece como registro que recusa bases divergentes e snapshot existente.

## 8. Próxima etapa e pendências

ETAPA 08 — Auditoria Global, Lapidação e Preparação Editorial, conforme prompt já salvo. O corpo de 24 capítulos e epílogo está em primeira redação completa, não em publicação aprovada. Permanecem leitura/aprovação de Sol, lapidação de ritmo e redundâncias, bibliografia final, estado visual das figuras, diagramação e validação dos formatos. Nenhum DOCX, PDF, EPUB ou KPF foi criado ou validado nesta etapa.
'''

old_snapshots = {p: sha256(data) for p,data in original.items() if p.startswith('ETAPAS/')}
qa = dict(etapa='07', data_local='2026-09-11', escopo='notas, introdução, Partes I–VI, capítulos 1–24 e epílogo',
          metodo_contagem=PATTERN+'; lexical Unicode, títulos e chamadas autor-data incluídos; não equivale a páginas',
          palavras_base=words(base), palavras_parte_VI_e_epilogo=new_words, palavras_manuscrito=total_words,
          palavras_por_capitulo=counts, palavras_abertura_parte_VI=opening_words,
          palavras_fechamento_parte_VI=closing_words, palavras_epilogo=epilogue_words,
          bytes_manuscrito=len(manuscript.encode()), git_blob_base=EXPECTED['MANUSCRITO_CANONICO.md'],
          git_blob_manuscrito_e_snapshot=blob, sha256_manuscrito_e_snapshot=digest,
          snapshot=SNAP, snapshot_identico=True, capitulos=list(range(1,25)), partes=['I','II','III','IV','V','VI'],
          snapshots_anteriores_sha256=old_snapshots, prosa_anterior_preservada=True,
          correcoes_prosa_nova=2, correcoes_prosa_anterior=0, alteracoes_cabecalho=1,
          paragrafos_exatamente_duplicados_35_palavras=duplicates,
          blocos_entrada={n: EXPECTED[P+n] for n in names},
          blocos_revisados={n: dict(git_blob_sha=git_blob(texts[P+n].encode()), palavras=words(texts[P+n])) for n in names},
          primeira_redacao_completa=True, aprovacao_autoral=False, publicacao_aprovada=False,
          limites='QA estrutural e revisão editorial; não validação clínica, revisão sistemática, aprovação visual ou prova de publicação.')
outputs = {rel: text for rel,text in texts.items() if rel in original and text.encode()!=original[rel]}
outputs['MANUSCRITO_CANONICO.md'] = manuscript
outputs['PARTE_VI_E_EPILOGO_ETAPA_07.md'] = new
outputs[SNAP] = manuscript
outputs['REGISTRO_EDITORIAL_ETAPA_07.md'] = record
outputs['REVISOES_ETAPA_07.json'] = encode_json(dict(etapa='07', data_local='2026-09-11', substituicoes_e_acrescimos=revisions))
outputs['DIFF_TEXTO_ANTERIOR_ETAPA_07.patch'] = ''.join(difflib.unified_diff(original['MANUSCRITO_CANONICO.md'].decode().splitlines(True), base.splitlines(True), fromfile='ETAPA_06/MANUSCRITO_CANONICO.md', tofile='ETAPA_07/BASE_REVISADA.md'))
outputs['QA_ETAPA_07.json'] = encode_json(qa)
for rel in outputs:
    require(not rel.startswith('/') and '..' not in Path(rel).parts, 'Caminho fora do escopo.')
    if rel not in original:
        require(not (ROOT/rel).exists(), 'Saída já existe; não sobrescrever: '+rel)
for rel,data in original.items():
    require((ROOT/rel).read_bytes()==data, 'Mudança concorrente antes de escrever: '+rel)
for rel,text in outputs.items():
    (ROOT/rel).parent.mkdir(parents=True, exist_ok=True)
    (ROOT/rel).write_bytes(text.encode('utf-8'))
for rel,digest_old in old_snapshots.items():
    require(sha256((ROOT/rel).read_bytes())==digest_old, 'Histórico alterado: '+rel)
require((ROOT/SNAP).read_bytes()==(ROOT/'MANUSCRITO_CANONICO.md').read_bytes(), 'Snapshot não idêntico.')
for rel in ['HISTORICO_ETAPAS.md','REFERENCIAS_DE_TRABALHO.md']:
    require((ROOT/rel).read_bytes().startswith(original[rel]), 'Prefixo perdido: '+rel)
manifest_paths = sorted(set(outputs)|{P+n for n in names}|{P+'REFERENCIAS_ACRESCIMO.md','PROMPT_PROXIMA_ETAPA_08.md'})
manifest = {rel: dict(git_blob=git_blob((ROOT/rel).read_bytes()), sha256=sha256((ROOT/rel).read_bytes()), bytes=len((ROOT/rel).read_bytes())) for rel in manifest_paths}
(ROOT/'ARQUIVOS_INTEGRACAO_ETAPA_07.json').write_text(encode_json(manifest),encoding='utf-8')
print(encode_json(qa))
