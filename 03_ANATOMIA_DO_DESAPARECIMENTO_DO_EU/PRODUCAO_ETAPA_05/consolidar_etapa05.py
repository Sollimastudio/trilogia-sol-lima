#!/usr/bin/env python3
"""Integra uma única vez a ETAPA 05. Não acessa rede nem altera outros livros.
Recusa bases divergentes e marcos existentes. Executar a partir de cópia Git limpa.
O sucesso deste script é QA estrutural, não aprovação autoral ou validação clínica.
"""
from __future__ import annotations
import difflib
import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'MANUSCRITO_CANONICO.md': '5bdf895efd012b9b3c6b62d2b322971b264b9e29',
    'STATUS.md': '79a208331981ca920e020dec1e0f6f7b4c9a12e4',
    'HISTORICO_ETAPAS.md': '8f29e274557ce479fe094205df7a85bd80abb4c4',
    'REFERENCIAS_DE_TRABALHO.md': '82bfc363a89ba59c0187a93769b6060b6c55058b',
    'MAPA_MAE.md': 'f9807db2db4764b6116a1ddbc65d0c894f6947ce',
    'PRODUCAO_ETAPA_05/13_ABERTURA_E_NOMES.md': 'd85b49087c18b00cdeac6ffc4ef92ee7b78bcf2a',
    'PRODUCAO_ETAPA_05/14_MOVIMENTO.md': '1c754f6bd5d6f8506a9334afb61b7394f74a1425',
    'PRODUCAO_ETAPA_05/15_EU_AUTOMATICO.md': '0c24b475fd894f089fc9d1c738153ab9a8ef7bc9',
    'PRODUCAO_ETAPA_05/16_SUCESSO_E_FECHAMENTO.md': '65c917b7221a90ad14d3f0b06b4f8145c34646ff',
    'PRODUCAO_ETAPA_05/REFERENCIAS_ACRESCIMO.md': '8ee2eb1043abad938e61b5b6f3f3e26173a1fe59',
    'PROMPT_PROXIMA_ETAPA_06.md': '1e93ed8e9f6cd08ca5b80d8715b507c470ec0da4',
}
BLOCKS = [
    '13_ABERTURA_E_NOMES.md', '14_MOVIMENTO.md',
    '15_EU_AUTOMATICO.md', '16_SUCESSO_E_FECHAMENTO.md',
]
REVISED_COUNTERCASE = '''### Um nome útil que não tomou a mesa de trabalho

Numa outra situação composta, uma tradutora recebia clientes que a chamavam de especialista. Tinha anos de trabalho, livros publicados e experiência em escolhas de linguagem que passavam despercebidas a quem apenas conhecia os idiomas. O nome ajudava a comunicar competência.

Certo dia, recebeu um manual de equipamento cuja terminologia não dominava com segurança. O cliente já falava em valor e prazo. Ela poderia ter aceitado para preservar a imagem de quem sempre sabe. Em vez disso, explicou o que conseguiria fazer e por que o projeto exigiria experiência técnica que não possuía naquele momento. Indicou outra profissional.

Perdeu a encomenda naquela semana. Não perdeu a profissão.

A competência do contracaso não está numa indiferença heroica ao dinheiro. Talvez a recusa pesasse no orçamento. Está em conservar critérios que permitem à especialidade ter uma fronteira. A palavra especialista não recebeu o direito de obrigá-la a simular conhecimento.

A mesma profissional pode estudar aquele campo e, mais tarde, participar de um projeto semelhante. Não precisará negar a cautela anterior para provar evolução. O nome permanece útil porque acompanha o trabalho, em vez de exigir que o trabalho represente onisciência.

Há pessoas que usam nomes desse modo: como referências suficientemente estáveis para orientar e suficientemente delimitadas para continuar aprendendo. Nem toda estabilidade é rigidez. Nem toda alteração é progresso. Uma categoria pode durar muitos anos e ainda ser vivida com autoria.

'''

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def words(text: str) -> int:
    return len(re.findall(r"\b[\wÀ-ÿ]+(?:[-’'][\wÀ-ÿ]+)*\b", text))

def dump(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'

def fmt(number: int) -> str:
    return f'{number:,}'.replace(',', '.')

def check(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def main() -> None:
    today = datetime.now(ZoneInfo('America/Sao_Paulo')).date()
    iso, br = today.isoformat(), today.strftime('%d/%m/%Y')
    snapshot = f'ETAPAS/05_PARTE_IV_EU_EMPRESTADO_{iso}.md'
    new_names = [snapshot, 'PARTE_IV_ETAPA_05.md', 'REGISTRO_EDITORIAL_ETAPA_05.md',
                 'REVISOES_ETAPA_05.json', 'QA_ETAPA_05.json',
                 'DIFF_TEXTO_ANTERIOR_ETAPA_05.patch', 'ARQUIVOS_INTEGRACAO_ETAPA_05.json']
    for name in new_names:
        check(not (ROOT/name).exists(), f'Marco já existe: {name}; não será sobrescrito.')
    for name, expected in EXPECTED.items():
        check((ROOT/name).is_file(), f'Entrada ausente: {name}')
        check(blob((ROOT/name).read_bytes()) == expected, f'Base divergente: {name}. Reconciliar antes de prosseguir.')
    originals = {name: (ROOT/name).read_text(encoding='utf-8') for name in EXPECTED}
    old_snapshots = {str(f.relative_to(ROOT)): sha256(f.read_bytes()) for f in (ROOT/'ETAPAS').glob('*.md')}
    qa4 = json.loads((ROOT/'QA_ETAPA_04.json').read_text())
    for name, digest in qa4['snapshots_anteriores_sha256'].items():
        check(old_snapshots.get(name) == digest, f'Snapshot antigo divergente: {name}')
    check(old_snapshots.get('ETAPAS/04_PARTE_III_ANATOMIA_OCUPACAO_2026-09-10.md') ==
          '656b75851e4caf005713d2abf610b7758e40eb687e43315df86baac43a854e86', 'Marco 04 divergente.')
    revisions: list[dict] = []
    def replace(text: str, before: str, after: str, file: str, reason: str) -> str:
        check(text.count(before) == 1, f'Substituição ambígua/ausente em {file}: {before[:80]}')
        if before != after:
            revisions.append({'arquivo': file, 'antes': before, 'depois': after, 'ocorrencias': 1, 'motivo': reason})
        return text.replace(before, after, 1)

    old = originals['MANUSCRITO_CANONICO.md']
    revised = replace(old, 'manuscrito canônico vivo — ETAPA 04', 'manuscrito canônico vivo — ETAPA 05',
                      'MANUSCRITO_CANONICO.md', 'Atualização do marco editorial, sem alteração da arquitetura.')
    if br != '10/09/2026':
        revised = replace(revised, '**Data de consolidação desta etapa:** 10/09/2026',
                          f'**Data de consolidação desta etapa:** {br}', 'MANUSCRITO_CANONICO.md', 'Data local real da integração.')
    revised = replace(revised, 'Lívia, a criadora apresentada no capítulo anterior,',
                      'Lívia, a criadora apresentada na Parte II,', 'MANUSCRITO_CANONICO.md',
                      'Correção da remissão no capítulo 11: Lívia foi apresentada no capítulo 8, não no 10.')
    loaded = {name: originals['PRODUCAO_ETAPA_05/'+name] for name in BLOCKS}
    name = '13_ABERTURA_E_NOMES.md'
    text = loaded[name]
    start = text.index('### Um nome útil que não tomou a oficina')
    end = text.index('### A encomenda sobre a bancada', start)
    loaded[name] = replace(text, text[start:end], REVISED_COUNTERCASE, 'PRODUCAO_ETAPA_05/'+name,
        'Varia o contracaso de competência delimitada: a restauração já ilustrava revisão e limite técnico no capítulo 10. Mantém função identitária com tradução.')
    name = '16_SUCESSO_E_FECHAMENTO.md'
    loaded[name] = replace(loaded[name],
        'Sônia não precisou negar a causa para reconhecer uma tarde que não lhe pertencia.',
        'Sônia não precisou negar a causa para reconhecer uma tarde que não pertencia à associação.',
        'PRODUCAO_ETAPA_05/'+name, 'Esclarece o referente: a tarde não pertencia à associação, não se nega a autonomia de Sônia.')
    part = '\n\n---\n\n'.join(loaded[name].strip() for name in BLOCKS) + '\n'
    combined = revised.rstrip() + '\n\n---\n\n' + part
    data = combined.encode('utf-8')
    digest, git_blob = sha256(data), blob(data)
    chapters = [int(n) for n in re.findall(r'^# CAPÍTULO (\d+)\s*$', combined, re.M)]
    check(chapters == list(range(1,17)), 'Capítulos fora de sequência ou duplicados.')
    check(re.findall(r'^# PARTE ([IVX]+) —', combined, re.M) == ['I','II','III','IV'], 'Partes divergentes.')
    for heading in ['# NOTA DA AUTORA', '# NOTA CONCEITUAL', '# INTRODUÇÃO', '# FECHAMENTO DA PARTE IV']:
        check(combined.count(heading) == 1, f'Moldura ausente ou duplicada: {heading}')
    check(not re.search(r'\[(?:TODO|INSERIR|A DESENVOLVER)\]|\bLorem ipsum\b', combined, re.I), 'Marcador editorial no corpo.')
    delimiters = re.compile(r'^# (?:CAPÍTULO \d+|PARTE [IVX]+ —.*|FECHAMENTO DA PARTE [IVX]+)\s*$', re.M)
    counts = {}
    for n in chapters:
        match = re.search(r'^# CAPÍTULO '+str(n)+r'\s*$', combined, re.M)
        stop = delimiters.search(combined, match.end())
        counts[str(n)] = words(combined[match.start():stop.start() if stop else len(combined)])
    check(all(counts[str(n)] >= 2400 for n in range(13,17)), 'Capítulo novo abaixo da dimensão verificada.')
    paragraphs = [' '.join(p.split()) for p in re.split(r'\n\s*\n', combined) if words(p) >= 35]
    duplicates = [p for p,c in Counter(paragraphs).items() if c > 1]
    check(not duplicates, 'Parágrafos extensos exatamente duplicados: revisar antes de integrar.')
    diff = ''.join(difflib.unified_diff(old.splitlines(True), revised.splitlines(True),
        fromfile='MANUSCRITO_ETAPA_04', tofile='TEXTO_ANTERIOR_REVISADO_NA_ETAPA_05'))

    refs = replace(originals['REFERENCIAS_DE_TRABALHO.md'],
        '**Escopo:** referências efetivamente utilizadas nas Partes II e III e verificações feitas na ETAPA 04.',
        '**Escopo:** referências utilizadas nas Partes II–IV; verificações da ETAPA 04 preservadas e cinco fontes consultadas na ETAPA 05.',
        'REFERENCIAS_DE_TRABALHO.md', 'Atualiza o escopo sem declarar nova reconferência integral das fontes anteriores.')
    if br != '10/09/2026':
        refs = replace(refs, '**Atualização:** 10/09/2026, data local de São Paulo.',
            f'**Atualização:** {br}, data local de São Paulo.', 'REFERENCIAS_DE_TRABALHO.md', 'Data do registro acumulado.')
    refs += '\n---\n\n' + originals['PRODUCAO_ETAPA_05/REFERENCIAS_ACRESCIMO.md'].rstrip() + '\n'
    for citation, reference in [
        ('NIMH, 2024', '24-MH-3573'),
        ('van Zomeren; Postmes; Spears, 2008', '10.1037/0033-2909.134.4.504'),
        ('Neal et al., 2011', '10.1177/0146167211419863'),
        ('Wood; Tam; Guerrero Witt, 2005', '10.1037/0022-3514.88.6.918'),
        ('Crocker et al., 2003', '10.1037/0022-3514.85.3.507')]:
        check(citation in part and reference in refs, f'Pareamento bibliográfico ausente: {citation}')

    status = originals['STATUS.md']
    pairs = [
        ('| Migração dos 24 capítulos | ✓ | Matriz de reaproveitamento criada. |',
         '| Matriz de migração dos 24 capítulos | ✓ | Planejamento de reaproveitamento criado; integração textual continua por etapa. |',
         'Distingue matriz concluída de migração integral ainda não concluída.'),
        ('`MANUSCRITO_CANONICO.md` contém abertura + Partes I, II e III, capítulos 1–12.',
         '`MANUSCRITO_CANONICO.md` contém abertura + Partes I–IV, capítulos 1–16.', 'Atualiza extensão efetivamente integrada.'),
        ('| Parte IV — O Eu Emprestado em Funcionamento | ◐ | Próxima frente: ETAPA 05, Caps. 13–16, conforme prompt específico. |',
         '| Parte IV — O Eu Emprestado em Funcionamento | ◉ | Caps. 13–16 completos, revisados e integrados; snapshot integral da ETAPA 05 conferido; leitura autoral pendente. |', 'Registra a execução sem antecipar aprovação autoral.'),
        ('| Parte V — Quando Fugir de Si Parece Liberdade | ◐ | Material legado forte; hierarquia revisada. |',
         '| Parte V — Quando Fugir de Si Parece Liberdade | ◐ | Próxima frente: ETAPA 06, Caps. 17–20, conforme prompt específico. |', 'Atualiza a próxima frente.'),
        ('### Marco atual — ETAPA 04', '### Marco histórico — ETAPA 04', 'Preserva os dados do marco anterior com rótulo histórico.'),
        ('| Pesquisa e referências | ◑ | Parte II recebeu atualização de fontes sobre desenvolvimento identitário, autonomia/controle parental, recomendação, comparação social e relações parassociais; migração continua por capítulo. |',
         '| Pesquisa e referências | ◑ | Registros das Partes II–III preservados; cinco fontes da Parte IV verificadas e registradas com limites; não se trata de revisão sistemática. |', 'Distingue verificação desta etapa de fontes herdadas.'),
    ]
    for before, after, reason in pairs:
        status = replace(status, before, after, 'STATUS.md', reason)
    if br != '10/09/2026':
        status = replace(status, '**Atualizado:** 10/09/2026', f'**Atualizado:** {br}', 'STATUS.md', 'Data real da atualização.')
    old_end = status[status.index('## ETAPA ATIVA / PRÓXIMA'):]
    new_end = f'''### Marco atual — ETAPA 05

**ETAPA 05 — Parte IV: O Eu Emprestado em Funcionamento:** escrita e revisão executadas; integração e integridade conferidas; leitura autoral pendente.

- Manuscrito: {fmt(words(combined))} palavras, capítulos 1–16.
- Parte IV: {fmt(words(part))} palavras, incluindo abertura e fechamento.
- Snapshot: `{snapshot}`.
- Git blob de manuscrito e snapshot: `{git_blob}`.
- SHA-256: `{digest}`.
- Registros: `REGISTRO_EDITORIAL_ETAPA_05.md`, `REVISOES_ETAPA_05.json`, `QA_ETAPA_05.json` e referências de trabalho.
- Os seis arquivos históricos anteriores de ETAPAS permanecem intactos.

## ETAPA ATIVA / PRÓXIMA

**ETAPA 06 — PARTE V: QUANDO FUGIR DE SI PARECE LIBERDADE**

Executar `PROMPT_PROXIMA_ETAPA_06.md`: abertura, capítulos 17–20, fechamento e ponte para Parte VI. Os capítulos são Fuga cognitiva; Propósito emprestado; Quando o outro vira função; Autenticidade sem responsabilidade. Preservar versões, personagens e limites conceituais; revisar o conjunto, registrar fontes, salvar snapshot integral e preparar a ETAPA 07.

**Execução editorial não equivale a aprovação autoral, validação clínica, conclusão dos 24 capítulos ou liberação para publicação.**
'''
    status = replace(status, old_end, new_end, 'STATUS.md', 'Registra o marco atual e a próxima execução com hashes verificados.')
    book_map = replace(originals['MAPA_MAE.md'],
        '**Arquitetura consolidada na ETAPA 01; produção atualizada até a ETAPA 04**',
        '**Arquitetura consolidada na ETAPA 01; produção atualizada até a ETAPA 05**',
        'MAPA_MAE.md', 'Atualiza progresso, não arquitetura.')
    book_map = replace(book_map, '**Snapshot anterior:** `ETAPAS/00_ESTRUTURA_BASE_2026-09-10.md`',
        '**Snapshot estrutural inicial:** `ETAPAS/00_ESTRUTURA_BASE_2026-09-10.md`', 'MAPA_MAE.md', 'Evita confundir marco inicial com o snapshot mais recente.')
    old_state = book_map[book_map.index('# 10. ESTADO'):]
    book_map = replace(book_map, old_state, '''# 10. ESTADO

ETAPAS 00 e 01 preservadas; ETAPAS 02–05 com escrita e revisão executadas. O manuscrito vivo contém abertura e Partes I–IV, capítulos 1–16. Aprovação autoral e publicação continuam pendentes.

A arquitetura de seis partes e 24 capítulos não foi alterada. As correções da ETAPA 04, especialmente a distinção entre fusão científica e metáfora autoral, foram preservadas. A ETAPA 05 acrescentou nomes, causas, automatismo e sucesso com funções próprias; atualizou uma remissão a Lívia e registrou ajustes no novo texto.

Próxima frente: **ETAPA 06 — Parte V: Quando Fugir de Si Parece Liberdade**, capítulos 17–20. Seguir `PROMPT_PROXIMA_ETAPA_06.md`, `STATUS.md` e `QA_ETAPA_05.json`.
''', 'MAPA_MAE.md', 'Sincroniza estado com a escrita efetiva e a próxima parte.')

    history_entry = f'''## ETAPA 05 — PARTE IV: O EU EMPRESTADO EM FUNCIONAMENTO

**Data local:** {br}.  
**Entrada:** abertura e Partes I–III, capítulos 1–12, blob `{EXPECTED['MANUSCRITO_CANONICO.md']}`.  
**Estado:** execução editorial concluída; leitura e aprovação autoral permanecem pendentes.

### Escrita e integração

Abertura e fechamento da Parte IV; capítulo 13 — Nomes que acolhem, rótulos que aprisionam; 14 — Quando o movimento começa a usar a pessoa; 15 — O Eu automático; 16 — O desaparecimento dentro do sucesso. Parte nova com {fmt(words(part))} palavras; acumulado com {fmt(words(combined))}. Contagem lexical Unicode, títulos e chamadas autor-data incluídos.

### Revisão e migração

Consultados por função os antigos capítulos 11 e 12 da Camada 11 do legado; preservados nomes como recursos, causa legítima, critério consistente e pertencimento sem posse. Não foi importado um catálogo de guerras culturais. Fontes externas específicas verificadas; referências herdadas preservadas sem alegar nova revisão sistemática.

Lívia permanece criadora; Marina permanece funcionária e retorna no capítulo 15. Cecília, Sônia e Augusto são novos casos compostos. Corrigida uma remissão de Lívia no capítulo 11. No texto novo, variado o contracaso técnico para não repetir a restauração do capítulo 10 e esclarecido o referente de uma frase sobre a tarde de Sônia. Cabeçalho e arquivos de controle foram atualizados; cada substituição está documentada.

### Integridade

Snapshot `{snapshot}` idêntico ao manuscrito. Git blob `{git_blob}`; SHA-256 `{digest}`. Capítulos 1–16 em sequência, quatro partes, notas e introdução. Os seis snapshots/arquivos históricos anteriores de ETAPAS foram mantidos byte a byte. Histórico anterior preservado por acréscimo.

### Pendências e próxima etapa

Leitura autoral; Partes V–VI e epílogo; lapidação global, bibliografia final, figuras e diagramação. Não há validação clínica ou autorização de publicação. Próxima execução: ETAPA 06, Parte V, capítulos 17–20, conforme `PROMPT_PROXIMA_ETAPA_06.md`.
'''
    history = originals['HISTORICO_ETAPAS.md'] + '\n---\n\n' + history_entry
    check(history.startswith(originals['HISTORICO_ETAPAS.md']), 'Histórico anterior não preservado.')
    prose_revisions = [r for r in revisions if r['arquivo'] == 'MANUSCRITO_CANONICO.md' or r['arquivo'].startswith('PRODUCAO_ETAPA_05/')]
    qa = {
        'etapa':'05', 'data_local':iso, 'escopo':'abertura e Partes I–IV; capítulos 1–16',
        'metodo_contagem':r"regex lexical Unicode \b[\wÀ-ÿ]+(?:[-’'][\wÀ-ÿ]+)*\b; inclui títulos e chamadas autor-data; não equivale a páginas",
        'palavras_base':words(old), 'palavras_base_apos_revisao':words(revised),
        'palavras_parte_IV':words(part), 'palavras_manuscrito':words(combined),
        'palavras_por_capitulo':counts,
        'palavras_abertura_parte_IV':words(part[:part.index('# CAPÍTULO 13')]),
        'palavras_fechamento_parte_IV':words(part[part.index('# FECHAMENTO DA PARTE IV'):]),
        'bytes_manuscrito':len(data), 'git_blob_base':EXPECTED['MANUSCRITO_CANONICO.md'],
        'git_blob_manuscrito_e_snapshot':git_blob, 'sha256_manuscrito_e_snapshot':digest,
        'snapshot':snapshot, 'snapshot_identico':True, 'capitulos':chapters, 'partes':['I','II','III','IV'],
        'bases_verificadas':EXPECTED, 'snapshots_anteriores_sha256':old_snapshots,
        'blocos_revisados':{name:{'palavras':words(t),'git_blob_sha':blob(t.encode())} for name,t in loaded.items()},
        'alteracoes_documentadas_total':len(revisions), 'alteracoes_manuscrito_blocos_e_cabecalho':len(prose_revisions),
        'paragrafos_exatamente_duplicados_35_palavras':duplicates,
        'chamadas_novas_pareadas_com_referencias':5,
        'historico_anterior_preservado_integralmente':True,
        'aprovacao_autoral':False, 'publicacao_aprovada':False,
        'limites':'QA estrutural e revisão editorial. Ausência de duplicatas exatas não prova ausência de toda repetição semântica. Não valida conceitos clínicos nem constitui revisão sistemática.'
    }
    report = f'''# REGISTRO EDITORIAL — ETAPA 05

**Livro:** Anatomia do Desaparecimento do Eu / Fuga Identitária.  
**Autora:** Sol Lima.  
**Data local:** {br}.  
**Estado:** escrita, revisão e integração executadas; texto em revisão autoral, não publicado.

## 1. Entrega concreta

| Bloco | Palavras lexicais |
|---|---:|
| Abertura e Partes I–III herdadas | {words(old)} |
| Texto herdado após correção | {words(revised)} |
| Abertura da Parte IV | {qa['palavras_abertura_parte_IV']} |
| Capítulo 13 | {counts['13']} |
| Capítulo 14 | {counts['14']} |
| Capítulo 15 | {counts['15']} |
| Capítulo 16 | {counts['16']} |
| Fechamento da Parte IV | {qa['palavras_fechamento_parte_IV']} |
| Parte IV integral | {words(part)} |
| Manuscrito acumulado | {words(combined)} |

Método lexical igual ao da ETAPA 04; inclui títulos e chamadas autor-data. Não se atribui paginação a bytes. Os capítulos são prosa completa, não sinopses ou amostras.

## 2. Função própria de cada capítulo

**13 — Nomes:** Cecília recebe espaço na palavra artista e passa a perguntar ao nome se pode aceitar uma encomenda. O capítulo distingue descrição, pertença, hipótese, categoria clínica e obrigação de representar uma identidade. O contracaso final é uma tradutora: competência que suporta reconhecer uma fronteira. Um diagnóstico útil não foi declarado inimigo nem reduzido a rótulo moral.

**14 — Movimento:** Sônia encontra recursos numa mobilização de moradores, mas passa a julgar o tempo e os vínculos pelo serviço à causa. A imagem de uma moradora não é convertida automaticamente em material de campanha. O contracaso de uma associação cultural tem custo real: reduzir um evento e distribuir tarefas, em vez de elogiar limites sem respeitá-los. Não foi reencenada a humilhação de Davi.

**15 — Automático:** Marina retorna em episódio novo: lê no domingo um arquivo para quinta-feira, intervém sem tarefa atribuída e descobre retrabalho. Depois responde a uma urgência verdadeira de sua responsabilidade. A diferença impede tanto eliminar hábitos úteis quanto tratar risco atual como passado encerrado. Eu automático é uma formulação autoral, não diagnóstico.

**16 — Sucesso:** Augusto é homenageado como o homem que nunca para enquanto tenta reduzir viagens e delegar. A conquista é real; a revisão envolve custo material e identitário. Lívia reaparece numa negociação comercial que exagera sua história, não numa reprise da gravação. A professora que divide a coordenação oferece contraponto de excelência sem onisciência ou posse.

## 3. Migração do legado

Fonte: Camada 11 de `Sollimastudio/fuga-identit-ria-`, blob `d7f0b2dda2e1c07e870d5365bca59e32b385312a`. Consultados por função os antigos capítulos 11 e 12.

Do capítulo 12: funções dos nomes, diferença entre acolher e exigir performance, pessoa maior que categoria, contracasos. Do capítulo 11: contribuição real de causas, alcance da autoridade, critérios consistentes sem falsa equivalência e vida fora do pertencimento. Os mecanismos já desenvolvidos nos capítulos 9–12 não foram apresentados de novo como um manual.

Capítulos 15 e 16 recebem escrita nova substancial. As aplicações antigas a comunidades específicas continuam disponíveis no repositório legado; não foram apagadas nem transportadas como catálogo de identidades suspeitas. Não se alegou nova auditoria integral de todas as palavras ou figuras do legado.

## 4. Revisão acumulada — Abertura e Partes I–IV

O conjunto foi examinado quanto a progressão, chamadas internas, função de casos, coerência conceitual, repetição e fronteiras. As notas preservam a condição não diagnóstica da tese. A Parte I identifica papéis e versões; a II fornece espelhos; a III examina incorporação e redução do contraditório; a IV mostra nomes, agendas, temporalidade e custo de sucesso operando na vida.

**Correção concreta no texto herdado:** no capítulo 11, Lívia era descrita como apresentada no capítulo anterior; a referência correta é a Parte II. Não foram atribuídos acontecimentos novos à biografia de Sol nem alteradas as histórias de Marina, Rafael, Helena, Davi ou Vera.

**Repetição:** o contracaso inicialmente escrito com restauração se aproximava do capítulo 10; passou a usar tradução, mantendo sua função sobre identidade de especialista. Persistem refrões conceituais e, sobretudo nas primeiras partes, uma cadência fragmentada a lapidar globalmente. O teste não encontrou parágrafos exatamente repetidos de pelo menos 35 palavras; isso não é prova de ausência de ecos semânticos.

**Fronteiras:** Morte em Vida não foi recontado; a Árvore, a Jaula e o método de Reposicione-se não foram reensinados. A Parte IV reconhece funcionamento e escolhas limitadas; não resolve antecipadamente desidentificação, luto e sustentação profunda reservados à Parte VI.

**Precisão e segurança:** mantida a distinção entre fusão científica e metáfora autoral; não se infere diagnóstico por hábitos, imagens ou categorias; sair não prova que cessou o perigo. Dependência material, cuidado, trabalho e compromisso não foram reduzidos a problemas de vontade. Nenhuma cena manda uma vítima confrontar ou anunciar saída.

## 5. Alterações rastreáveis

`REVISOES_ETAPA_05.json` registra antes, depois, ocorrência e motivo de {len(revisions)} substituições, incluindo {len(prose_revisions)} no manuscrito, nos blocos novos ou no cabeçalho. O diff separado mostra somente a revisão do texto herdado, sem esconder a adição da Parte IV.

Além da remissão de Lívia e do contracaso variado, foi esclarecida uma frase do fechamento: a tarde de Sônia não pertencia à associação. Os controles foram sincronizados. No STATUS, matriz de migração concluída foi distinguida da integração de todos os 24 capítulos, que ainda não terminou.

## 6. Fontes efetivamente usadas

Cinco novas referências foram conferidas para alegações delimitadas: NIMH sobre avaliação e cuidado; van Zomeren, Postmes e Spears sobre ação coletiva; Neal e colegas e Wood, Tam e Guerrero Witt sobre hábitos em contextos específicos; Crocker e colegas sobre desempenho acadêmico e autoavaliação. Identificação, DOI, acesso e limites estão em `REFERENCIAS_DE_TRABALHO.md`, códigos R05-01 a R05-05.

Nos quatro artigos, consultou-se o resumo dos autores e metadados; não se afirma leitura integral. No NIMH, consultou-se o texto institucional em HTML. As inferências sobre os casos compostos foram separadas do que foi efetivamente pesquisado. Esta etapa não revalidou externamente toda a bibliografia anterior nem constitui revisão sistemática.

## 7. Integridade do marco

- Base: `{EXPECTED['MANUSCRITO_CANONICO.md']}`.
- Manuscrito e snapshot: `{git_blob}`.
- SHA-256: `{digest}`.
- Snapshot integral: `{snapshot}`.
- Dezesseis capítulos em sequência, quatro partes e molduras iniciais preservadas.
- Seis arquivos históricos anteriores de ETAPAS mantidos byte a byte.
- Histórico anterior preservado integralmente, com novo registro por acréscimo.
- QA, revisões e diff acompanham a entrega; a verificação posterior ao salvamento deve ser registrada separadamente.

Foi necessária uma rotina temporária de GitHub Actions para exportar leitura e integrar arquivos sem retranscrever o manuscrito inteiro. Ela deve ser removida após conferência final; não integra a automação permanente do projeto.

## 8. Pendências e próxima execução

Leitura e aprovação de Sol; Partes V–VI e epílogo; revisão final de ritmo, repetição, bibliografia e termos; figuras legadas ainda sem conferência visual nesta etapa; diagramação e validação de formatos de publicação. Nenhum EPUB, PDF, DOCX ou KPF foi criado ou validado nesta execução.

Próxima etapa: **ETAPA 06 — Parte V: Quando Fugir de Si Parece Liberdade**, capítulos 17–20, conforme `PROMPT_PROXIMA_ETAPA_06.md`. O comando mantém as fronteiras e exige nova revisão acumulada e snapshot verificado.
'''
    outputs = {
        'MANUSCRITO_CANONICO.md':combined, snapshot:combined, 'PARTE_IV_ETAPA_05.md':part,
        'REFERENCIAS_DE_TRABALHO.md':refs, 'STATUS.md':status,
        'HISTORICO_ETAPAS.md':history, 'MAPA_MAE.md':book_map,
        'REGISTRO_EDITORIAL_ETAPA_05.md':report,
        'REVISOES_ETAPA_05.json':dump(revisions), 'QA_ETAPA_05.json':dump(qa),
        'DIFF_TEXTO_ANTERIOR_ETAPA_05.patch':diff,
    }
    for name in BLOCKS:
        if loaded[name] != originals['PRODUCAO_ETAPA_05/'+name]:
            outputs['PRODUCAO_ETAPA_05/'+name] = loaded[name]
    outputs['ARQUIVOS_INTEGRACAO_ETAPA_05.json'] = dump(sorted(list(outputs) + ['ARQUIVOS_INTEGRACAO_ETAPA_05.json']))
    # Tudo foi calculado e validado antes da primeira escrita.
    for name, text in outputs.items():
        destination = ROOT/name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(text.encode('utf-8'))
    check((ROOT/snapshot).read_bytes() == (ROOT/'MANUSCRITO_CANONICO.md').read_bytes(), 'Snapshot não idêntico após a escrita.')
    for name, digest_before in old_snapshots.items():
        check(sha256((ROOT/name).read_bytes()) == digest_before, f'Marco histórico alterado: {name}')
    check((ROOT/'HISTORICO_ETAPAS.md').read_bytes().startswith(originals['HISTORICO_ETAPAS.md'].encode()), 'Histórico não preservado.')
    print(dump({'palavras_parte_IV':words(part), 'palavras_manuscrito':words(combined),
                'git_blob':git_blob, 'snapshot':snapshot, 'sha256':digest,
                'alteracoes_documentadas':len(revisions), 'arquivos':len(outputs)}))

if __name__ == '__main__':
    main()
