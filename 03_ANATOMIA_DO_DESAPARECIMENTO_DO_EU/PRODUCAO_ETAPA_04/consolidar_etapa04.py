"""Consolidação editorial única: preserva snapshots e recusa base concorrente."""
from __future__ import annotations
import argparse
import collections
import difflib
import hashlib
import json
import re
from pathlib import Path

DATE = '2026-09-10'
INPUT_BLOB = 'a34f0038fd6339846c257c46a88050f55052b7c5'
STATUS_BLOB = '2ab00ead509fe8d6067fc9ad49eb4416fbe09cab'
HISTORY_BLOB = '746f4dd4c99979406306dcad72c583213048e930'
EXPECTED_BLOCKS = {'09_ABERTURA_E_NARRATIVA.md': '6c94e22a376c2149d01bde1930d79057e7650c3d', '10_EXPOSICAO_E_IDENTIFICACAO.md': 'efaf2326f5950cb6f1a9bdf0cb74e2bb472b3ffd', '11_ADOCAO.md': '4714c7c3103c81300b65f9dfb28370e8e5f88b47', '12_REDOMA_FUSAO_DEPENDENCIA.md': 'e9b9190a4e9bb59b1837c92caa655a5233b513ca', '99_FECHAMENTO.md': '52a74f26e0cb88fc32a70954d3c7d5fe7fc580b5'}
BLOCKS = ['09_ABERTURA_E_NARRATIVA.md', '10_EXPOSICAO_E_IDENTIFICACAO.md', '11_ADOCAO.md', '12_REDOMA_FUSAO_DEPENDENCIA.md', '99_FECHAMENTO.md']

def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def words(text: str) -> int:
    return len(re.findall(r"\b[\wÀ-ÿ]+(?:[-’'][\wÀ-ÿ]+)*\b", text))

def fmt(n: int) -> str:
    return format(n, ',').replace(',', '.')

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--book-dir', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--preview', action='store_true')
    args = parser.parse_args()
    root = args.book_dir.resolve()
    master = root / 'MANUSCRITO_CANONICO.md'
    snapshot = root / 'ETAPAS' / f'04_PARTE_III_ANATOMIA_OCUPACAO_{DATE}.md'
    old_bytes = master.read_bytes()
    if blob(old_bytes) != INPUT_BLOB:
        raise RuntimeError('Manuscrito mudou: reler e reconciliar; nenhuma sobrescrita automática.')
    if snapshot.exists():
        raise RuntimeError('Snapshot da ETAPA 04 já existe; não sobrescrever marco histórico.')
    if blob((root/'STATUS.md').read_bytes()) != STATUS_BLOB:
        raise RuntimeError('STATUS mudou: revisar concorrência.')
    if blob((root/'HISTORICO_ETAPAS.md').read_bytes()) != HISTORY_BLOB:
        raise RuntimeError('Histórico mudou: revisar concorrência.')
    frozen = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'ETAPAS').glob('*.md')}
    old = old_bytes.decode('utf-8')
    revisions: list[dict] = []

    def replace(text: str, before: str, after: str, file: str, reason: str, count: int = 1) -> str:
        actual = text.count(before)
        if actual != count:
            raise RuntimeError(f'Alvo inesperado ({actual}, esperado {count}): {file}: {before[:80]}')
        revisions.append({'arquivo': file, 'antes': before, 'depois': after, 'ocorrencias': count, 'motivo': reason})
        return text.replace(before, after)

    def prior(before: str, after: str, reason: str) -> None:
        nonlocal old
        old = replace(old, before, after, 'MANUSCRITO_CANONICO.md: texto preexistente', reason)

    prior('manuscrito canônico vivo — ETAPA 03', 'manuscrito canônico vivo — ETAPA 04', 'Atualizar marco, sem alterar identidade da obra.')
    prior('Estamos testando dependência.', 'Estamos observando nossa relação com esses papéis, não medindo dependência. O desconforto deste exercício, sozinho, não prova desaparecimento identitário.', 'Evitar impressão de teste clínico validado no capítulo 1.')
    prior('Toda performance persistente recebe alguma recompensa.', 'Algumas performances persistem porque recebem recompensa; outras são mantidas por hábito, obrigação ou coerção.', 'Retirar universalização não sustentada do capítulo 4.')
    prior('Slogans são deliciosos porque poupam metabolismo.', 'Slogans são deliciosos porque parecem poupar o trabalho de examinar.', 'Preservar ironia sem sugerir alegação metabólica não demonstrada.')
    prior('Mas ninguém aprende a desaparecer sozinho.', 'Muitos desses aprendizados acontecem nas relações.', 'Reduzir generalização causal e eco imediato do final da Parte I.')
    prior('Na fusão, a fronteira entre vínculo e identidade enfraquece a ponto de discordar parecer traição de existência.', 'Na fusão restritiva que esta metáfora investiga, discordar pode parecer traição de existência. Esse uso autoral não equivale ao construto científico de fusão de identidade, distinguido no capítulo 12.', 'Distinguir metáfora de construto científico desde o capítulo 6.')
    prior('Riêm das mesmas piadas.', 'Riem das mesmas piadas.', 'Correção ortográfica.')
    prior('A opinião fica mais extrema porque a nuance reduz alcance.', 'A opinião pode ficar mais extrema quando o criador interpreta a reação do público como recompensa por eliminar nuances.', 'Evitar lei geral sem evidência sobre nuance e alcance.')
    prior('enquanto comparações laterais eram mais comuns e não apresentavam o mesmo padrão consistente (Burnell et al., 2024).', 'enquanto comparações laterais eram mais comuns e não apresentavam o mesmo padrão consistente (Burnell et al., 2024). Nesse estudo, a associação com menor autoestima foi observada para comparações ascendentes em relação às descendentes; não é uma medida do efeito de toda comparação sobre toda pessoa.', 'Explicitar o contraste observado no estudo, sem inferência universal.')
    prior('Uma meta-análise publicada em 2026 encontrou associação positiva modesta entre uso problemático de redes sociais e comparação social,', 'Uma meta-análise de Demir e colegas (2026) encontrou associação positiva modesta entre uso problemático de redes sociais e comparação social,', 'Adicionar atribuição autor-data já verificada.')
    prior('Uma meta-análise publicada em 2026 sobre engajamento parassocial com influenciadores encontrou associações', 'Uma meta-análise de Li, Liu e Liu (2026) sobre engajamento parassocial com influenciadores encontrou associações', 'Adicionar atribuição autor-data e evitar referência anônima.')
    prefix, chapter8 = old.split('# CAPÍTULO 8\n', 1)
    n_marina = chapter8.count('Marina')
    chapter8 = replace(chapter8, 'Marina', 'Lívia', 'MANUSCRITO_CANONICO.md: apenas capítulo 8', 'Diferenciar criadora da Marina funcionária do capítulo 3.', n_marina)
    old = prefix + '# CAPÍTULO 8\n' + chapter8
    prior('Ele oferece uma lente.\n\nLentes não sentenciam pessoas.', 'Os casos e contracasos apresentados são ficcionais ou compostos para ilustrar possibilidades, sem corresponder a pessoas identificáveis. Não são relatos clínicos nem provas empíricas do mecanismo.\n\nEle oferece uma lente.\n\nLentes não sentenciam pessoas.', 'Unificar transparência sobre os exemplos do conjunto na Nota Conceitual.')

    loaded: dict[str, str] = {}
    input_blocks = {}
    for filename in BLOCKS:
        p = root/'PRODUCAO_ETAPA_04'/filename
        data = p.read_bytes()
        if blob(data) != EXPECTED_BLOCKS[filename]:
            raise RuntimeError(f'Bloco mudou após revisão: {filename}')
        input_blocks[filename] = blob(data)
        text = data.decode('utf-8')
        targets = {
            '09_ABERTURA_E_NARRATIVA.md': [
                ('O legado deste livro organizou uma distinção útil:', 'Uma distinção útil para essa leitura separa', 'Retirar comentário de produção do corpo literário.'),
                ('Elisa é uma personagem composta adaptada do legado desta obra.', 'Elisa é uma personagem composta.', 'Manter procedência de migração no registro editorial, não na narrativa.')],
            '11_ADOCAO.md': [
                ('Este caso é composto e retoma, sob outra forma, uma situação do legado desta obra: alguém encontra uma linguagem útil e depois precisa descobrir até onde ela alcança.', 'Neste caso composto, alguém encontra uma linguagem útil e depois precisa descobrir até onde ela alcança.', 'Eliminar referência a bastidores de produção.')],
            '12_REDOMA_FUSAO_DEPENDENCIA.md': [
                ('O caso é composto, adaptado do legado desta obra.', 'O caso é composto.', 'Separar ficção ilustrativa de comentários de migração.'),
                ('A frase do legado continua útil quando perde o tom de sentença universal:', 'Essa possibilidade pode ser resumida sem transformá-la em sentença universal:', 'Preservar formulação autoral sem referência a versões técnicas.'),
                ('Vera é uma personagem composta. Sua história foi adaptada de um caso do legado, sem corresponder a Sol nem à Helena apresentada na Parte I. Essa distinção importa: não vamos inventar violência numa trajetória anterior só para facilitar uma explicação.', 'Vera é uma personagem composta. Sua história permite observar restrições concretas à liberdade, sem reduzir a permanência numa relação ao que a pessoa acredita sobre si.', 'Retirar comentário técnico e preservar identificação independente de Vera.')]
        }
        for before, after, why in targets.get(filename, []):
            text = replace(text, before, after, f'PRODUCAO_ETAPA_04/{filename}', why)
        loaded[filename] = text
    new_part = '\n\n'.join(loaded[f].strip() for f in BLOCKS) + '\n'
    combined = old.rstrip() + '\n\n---\n\n' + new_part
    content = combined.encode('utf-8')
    chapters = [int(x) for x in re.findall(r'^# CAPÍTULO (\d+)\s*$', combined, re.M)]
    assert chapters == list(range(1,13)), chapters
    assert re.findall(r'^# PARTE ([IVX]+) —', combined, re.M) == ['I','II','III']
    for title in ['# NOTA DA AUTORA', '# NOTA CONCEITUAL', '# INTRODUÇÃO']:
        assert combined.count(title) == 1
    assert '# CAPÍTULO 13' not in combined
    assert 12000 <= words(new_part) <= 16000, words(new_part)
    assert 'Na anatomia da ocupação.' in combined[:combined.index('# PARTE III')]
    assert 'Esta vida funciona. Eu também estou nela?' in combined
    assert 'Marina' in prefix and 'Marina' not in chapter8
    assert 'Lívia' in chapter8 and 'Lívia' in loaded['11_ADOCAO.md']
    for bad in ['[TODO]', '[INSERIR', 'PLACEHOLDER', 'cite', 'filecite']:
        assert bad not in combined, bad
    assert 'legado' not in new_part.lower(), 'Bastidor editorial no novo corpo.'

    def section_counts(text: str) -> dict[str,int]:
        matches = list(re.finditer(r'^# CAPÍTULO (\d+)\s*$', text, re.M))
        result = {}
        for i, m in enumerate(matches):
            end = matches[i+1].start() if i+1 < len(matches) else len(text)
            section = text[m.start():end]
            for stopper in ['# FECHAMENTO DA PARTE', '# PARTE ']:
                if stopper in section:
                    section = section.split(stopper, 1)[0]
            result[m.group(1)] = words(section)
        return result

    digest = hashlib.sha256(content).hexdigest()
    output_blob = blob(content)
    blocks_final = {k: {'git_blob_sha':blob(v.encode()), 'palavras':words(v), 'bytes':len(v.encode())} for k,v in loaded.items()}
    counts = section_counts(combined)
    para_counts = collections.Counter(x.strip() for x in combined.split('\n\n') if words(x)>=35)
    duplicates = [{'ocorrencias':n,'inicio':p[:120]} for p,n in para_counts.items() if n>1]
    qa = {
        'etapa':'04', 'data_local':DATE, 'escopo':'abertura e Partes I–III; capítulos 1–12',
        'metodo_contagem':"regex lexical Unicode; inclui títulos e chamadas autor-data; não equivale a páginas",
        'palavras_base':words(old_bytes.decode()), 'palavras_base_apos_revisao':words(old),
        'palavras_parte_III':words(new_part), 'palavras_manuscrito':words(combined),
        'palavras_por_capitulo':counts, 'bytes_manuscrito':len(content),
        'git_blob_base':INPUT_BLOB, 'git_blob_manuscrito_e_snapshot':output_blob,
        'sha256_manuscrito_e_snapshot':digest, 'snapshot':snapshot.relative_to(root).as_posix(),
        'capitulos':chapters, 'snapshot_identico':True, 'snapshots_anteriores_sha256':frozen,
        'blocos_de_entrada':input_blocks, 'blocos_revisados':blocks_final,
        'alteracoes_documentadas':len(revisions), 'paragrafos_exatamente_duplicados_35_palavras':duplicates,
        'aprovacao_autoral':False, 'publicacao_aprovada':False,
        'limites':'QA estrutural e revisão editorial; não validação clínica, revisão sistemática ou prova de publicação.'
    }
    if args.preview:
        print(json.dumps(qa,ensure_ascii=False,indent=2))
        (root/'PREVIEW_ETAPA_04.md').write_bytes(content)
        (root/'PREVIEW_PARTE_III.md').write_text(new_part,encoding='utf-8')
        (root/'PREVIEW_REVISOES.json').write_text(json.dumps(revisions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        return

    assert (root/'PROMPT_PROXIMA_ETAPA_05.md').is_file()
    refs_path = root/'REFERENCIAS_DE_TRABALHO.md'
    refs = refs_path.read_text(encoding='utf-8')
    refs = replace(refs,
        '**Uso herdado:** capítulo 8, personalização por interesses e engajamento. A consulta direta nesta rodada não expôs texto completo estável; a redação específica herdada deve ser novamente conferida na revisão técnica final das plataformas. Não acrescentada afirmação técnica nova sobre TikTok na Parte III. Essa limitação não foi ocultada como verificação integral.',
        '**Uso herdado:** capítulo 8, personalização por interesses e engajamento. A rota original não expôs texto completo estável nesta consulta. A afirmação foi reconferida na página oficial alternativa https://support.tiktok.com/en/getting-started/for-you/test-for-you e no texto institucional https://newsroom.tiktok.com/en-us/how-tiktok-recommends-videos-for-you. O relato histórico não foi tratado como prova de implementação atual. Antes da publicação, reconferir interfaces e funções que podem mudar.',
        'REFERENCIAS_DE_TRABALHO.md', 'Registrar resolução da limitação de acesso mediante fontes oficiais alternativas.')
    qa['alteracoes_documentadas'] = len(revisions)

    status = (root/'STATUS.md').read_text(encoding='utf-8')
    status = status.replace('abertura + Partes I e II, capítulos 1–8.', 'abertura + Partes I, II e III, capítulos 1–12.')
    status = status.replace('| Parte III — A Anatomia da Ocupação | ◐ | Próxima frente: Caps. 9–12. Forte legado em narrativa/exposição/identificação/adoção/redoma/fusão; precisa condensação para não duplicar `Reposicione-se`. |', '| Parte III — A Anatomia da Ocupação | ◉ | Caps. 9–12 completos, revisados e integrados; snapshot integral da ETAPA 04 verificado; leitura autoral pendente. |')
    status = status.replace('| Parte IV — O Eu Emprestado em Funcionamento | ◐ | Legado relevante + novos eixos Eu automático/sucesso. |', '| Parte IV — O Eu Emprestado em Funcionamento | ◐ | Próxima frente: ETAPA 05, Caps. 13–16, conforme prompt específico. |')
    status = status.replace('**ETAPA 03 — Parte II: Os Espelhos que Respondem por Nós:** ✓ execução editorial concluída; texto em revisão autoral.', '**ETAPA 03 — Parte II: Os Espelhos que Respondem por Nós:** ✓ execução editorial concluída; texto em revisão autoral.  \n**ETAPA 04 — Parte III: A Anatomia da Ocupação:** ✓ escrita, revisão, integração e integridade verificadas; leitura autoral pendente.')
    status = status.replace('compartilham o blob `a34f0038fd6339846c257c46a88050f55052b7c5`', 'compartilhavam o blob `a34f0038fd6339846c257c46a88050f55052b7c5`')
    status = status.split('## ETAPA ATIVA / PRÓXIMA')[0] + f'''### Marco atual — ETAPA 04

- Capítulos 1–12; {fmt(words(combined))} palavras no manuscrito (contagem lexical incluindo títulos).
- Parte III: {fmt(words(new_part))} palavras.
- `REGISTRO_EDITORIAL_ETAPA_04.md`, `REFERENCIAS_DE_TRABALHO.md`, `REVISOES_ETAPA_04.json` e `QA_ETAPA_04.json` documentam trabalho e limites.
- Manuscrito e snapshot integral: blob `{output_blob}`; SHA-256 `{digest}`.
- Snapshots anteriores preservados, não sobrescritos.
- A criadora do capítulo 8 passa a chamar-se Lívia; Marina continua sendo a funcionária do capítulo 3.
- Fusão científica não é sinônimo de apagamento do Eu; distinção no capítulo 12 e remissão no capítulo 6.

## ETAPA ATIVA / PRÓXIMA

**ETAPA 05 — PARTE IV: O EU EMPRESTADO EM FUNCIONAMENTO**

Executar `PROMPT_PROXIMA_ETAPA_05.md`, escrevendo abertura, capítulos 13–16 e fechamento. Preservar capítulos anteriores, conferir o estado vivo e os hashes antes de atualizar, revisar o conjunto, registrar fontes e alterações, atualizar histórico/status, congelar snapshot integral e preparar a ETAPA 06.

Capítulos: 13 — Nomes que acolhem, rótulos que aprisionam; 14 — Quando o movimento começa a usar a pessoa; 15 — O Eu automático; 16 — O desaparecimento dentro do sucesso.

**Execução editorial não equivale a aprovação autoral, validação clínica ou autorização de publicação.**
'''

    history = (root/'HISTORICO_ETAPAS.md').read_text(encoding='utf-8')
    history_before = history
    history += f'''\n---

## ETAPA 04 — PARTE III: A ANATOMIA DA OCUPAÇÃO
**Data local:** {DATE}.  
**Entrada:** abertura + Partes I–II, capítulos 1–8; blob `{INPUT_BLOB}`.

### Execução
- Escritos integralmente abertura, capítulos 9–12, fechamento e ponte para a Parte IV.
- Parte III com {fmt(words(new_part))} palavras; manuscrito acumulado com {fmt(words(combined))} palavras.
- Reuso seletivo dos antigos capítulos 4–7 e 13–17; material legado não foi apagado.
- Matriz NARRATIVA condensada; método de Reposicione-se não reconstruído.
- Fontes verificadas e limites registrados em `REFERENCIAS_DE_TRABALHO.md`.
- Corrigida distinção entre fusão científica e metáfora de restrição identitária.
- Corrigida colisão de nomes: Marina funcionária preservada; criadora passa a Lívia. Novos casos Davi e Vera não substituem Rafael e Helena da primeira parte.
- Correções anteriores delimitadas, preservadas em `REVISOES_ETAPA_04.json` e `DIFF_TEXTO_ANTERIOR_ETAPA_04.patch`.
- Retirados comentários de migração de dentro da nova prosa; procedência preservada no registro editorial.
- Atualizados estado e mapa-mãe apenas quanto ao avanço de produção, sem alterar arquitetura.

### Integridade
Snapshot integral: `{snapshot.relative_to(root).as_posix()}`.  
Manuscrito/snapshot: blob `{output_blob}`, SHA-256 `{digest}`, {fmt(len(content))} bytes.  
Capítulos numerados uma vez, de 1 a 12; Partes I–III; snapshots anteriores mantidos byte a byte.

### Pendências
Leitura e aprovação autoral; escrita das Partes IV–VI e epílogo; lapidação global de ritmo e diagramação; figuras legadas não inspecionadas visualmente nesta etapa; revisão factual/técnica final antes de publicar.

### Próxima etapa
ETAPA 05 — Parte IV, capítulos 13–16. Comando integral em `PROMPT_PROXIMA_ETAPA_05.md`.

**Estado:** execução editorial concluída; obra ainda não aprovada para publicação.
'''

    map_path = root/'MAPA_MAE.md'
    map_text = map_path.read_text(encoding='utf-8')
    assert blob(map_path.read_bytes()) == '696224a9dce4366c1a4046e69f0e37ebbe9a23ae'
    map_text = map_text.replace('**Estado vivo após ETAPA 01 — Auditoria e Consolidação do Legado**', '**Arquitetura consolidada na ETAPA 01; produção atualizada até a ETAPA 04**')
    map_text = map_text.split('# 10. ESTADO')[0] + '''# 10. ESTADO

ETAPAS 00 e 01 preservadas; ETAPAS 02, 03 e 04 com escrita e revisão executadas. O manuscrito vivo contém abertura e Partes I–III, capítulos 1–12. Aprovação autoral e publicação continuam pendentes.

A arquitetura deste mapa não foi alterada na ETAPA 04. Correções conceituais e de continuidade estão documentadas no registro editorial, especialmente a distinção entre fusão científica e metáfora autoral.

Próxima frente: **ETAPA 05 — Parte IV: O Eu Emprestado em Funcionamento**, capítulos 13–16. Seguir `PROMPT_PROXIMA_ETAPA_05.md` e `STATUS.md`.
'''

    report = f'''# REGISTRO EDITORIAL — ETAPA 04

**Livro:** Anatomia do Desaparecimento do Eu / Fuga Identitária.  
**Autora:** Sol Lima.  
**Data local:** {DATE}.  
**Estado:** execução da etapa concluída; texto em revisão autoral, não publicado.

## 1. Entrega concreta

Abertura da Parte III, capítulos 9–12 completos, fechamento e ponte para Parte IV integrados ao manuscrito. Não foram entregues outlines no lugar de capítulos.

| Bloco | Palavras lexicais |
|---|---:|
| Abertura + Partes I–II antes da revisão | {words(old_bytes.decode())} |
| Abertura + Partes I–II depois das correções | {words(old)} |
| Parte III nova, incluindo abertura e fechamento | {words(new_part)} |
| Manuscrito acumulado | {words(combined)} |
| Capítulo 9 | {counts['9']} |
| Capítulo 10 | {counts['10']} |
| Capítulo 11 | {counts['11']} |
| Capítulo 12 | {counts['12']} |

Método: regex lexical Unicode; títulos e chamadas autor-data incluídos. Não usar bytes como substituto de palavras ou inventar paginação. O manuscrito tem {fmt(len(content))} bytes, mas esse não é seu indicador editorial de extensão.

## 2. O que cada capítulo acrescenta

**9 — Narrativa:** liga fato, interpretação, identidade atribuída e comando. Rafael retorna com acontecimento novo; Elisa mostra um auxílio útil que extrapola autoridade. Matriz NARRATIVA aparece condensada, em nove componentes, aplicada à identidade. O título universalizante é explicitamente delimitado como lente autoral, não lei empírica.

**10 — Exposição e identificação:** distingue contato, familiaridade, agrado, julgamento de verdade e correspondência pessoal. Samuel recebe ajuda real e precisa preservar nuances; Davi é introduzido pelo aprendizado, não como pessoa sem pensamento. Repetição não equivale a evidência independente. O contracaso mostra aprendizagem que aceita correção externa.

**11 — Adoção:** Luiza aprende linguagem de limites, aplica-a de modo amplo demais e recupera precisão sem regressar à submissão. Lívia reaparece fora da câmera. Conhecimento recebido, confiança em especialista e hábitos úteis não são confundidos com ocupação. Fluência verbal não é usada como prova de autoria.

**12 — Redoma, fusão e dependência:** Davi percebe humilhação e o impulso de racionalizá-la. Vera demonstra restrições concretas, sem culpa transferida à vítima. Distinguidas correção, proteção legítima, dependência material, pertença e coerção. Fusão científica não significa sumiço da identidade pessoal. O fechamento prepara a vida organizada pelo Eu emprestado, sem antecipar a reconstrução da Parte VI.

## 3. Migração do patrimônio anterior

| Origem legada | Operação nesta etapa |
|---|---|
| Caps. 4–5, narrativa e matriz | Condensação e adaptação no cap. 9; Elisa e camadas preservadas por função. |
| Caps. 6–7, valores, lógica e eixo | Recursos incorporados ao exame; não foi recriado o método inteiro. |
| Caps. 13–14, exposição e identificação | Integração no cap. 10, com pesquisa e distinção de efeitos. |
| Cap. 15, adoção | Adaptação no cap. 11, cenas novas e proteção da aprendizagem legítima. |
| Caps. 16–17, redoma, fusão, dependência | Adaptação no cap. 12; segurança, benefício real, custo de saída e contraditório. |
| Rafael mentorado e Helena sob controle no legado | Renomeados Davi e Vera para não alterar biografias compostas já estabelecidas no manuscrito novo. |

O repositório legado foi consultado por função. Não se alegou nova auditoria integral de todas as suas palavras, figuras ou referências. Nenhum arquivo de origem foi apagado.

## 4. Auditoria da abertura e Partes I–III

**Progressão:** pessoa e papéis → espelhos e validação → mecanismo de interpretação, adoção e fechamento. A passagem do capítulo 8 para o 9 continua necessária. O encerramento da Parte III abre nomes, movimentos, Eu automático e sucesso, sem escrever antecipadamente esses capítulos.

**Fronteiras:** não foram recontadas cenas biográficas de Morte em Vida, nem reconstruídos Árvore, Jaula, Leis, Frutos, Poda e Nova Semente. Não foi deslocado o Livro 3 para antes de Reposicione-se. O método herdado é aplicado, não apresentado como uma segunda obra didática.

**Storytelling:** cenas compostas articulam contribuições reais, custos e possibilidade de correção. Não se afirma que um caso imaginado demonstra causalidade. A Parte III usa parágrafos mais desenvolvidos e menos listas fragmentadas; mantém linhas breves quando acrescentam ênfase.

**Repetição:** foi removido um eco imediato de caráter universal na abertura da Parte II. Retornos de personagens cumprem função nova. Persistem, no texto anterior, formulações e parágrafos muito curtos cuja cadência merece lapidação global após a conclusão da obra. Não foram substituídas grandes passagens só por preferência estilística.

**Precisão:** corrigidos universalizadores sobre recompensa e alcance, um contraste de comparação social e chamadas autor-data ausentes. A metáfora de fusão recebeu uma fronteira científica explícita. Não há estatística de prevalência de Fuga Identitária nem alegação de instrumento validado.

**Segurança:** não se usa demora de saída como prova de consentimento; dependência pode existir sem aceitação da narrativa; não se exige confronto, reconciliação ou exposição de plano. Canais brasileiros têm função distinta e foram conferidos.

## 5. Correções registradas

O arquivo `REVISOES_ETAPA_04.json` preserva cada substituição com texto anterior, texto posterior, contagem e motivo. O diff do texto preexistente permite revisão humana sem misturar a adição de 14 mil palavras às pequenas correções.

Marina funcionária permanece Marina; somente a criadora passa a Lívia. Rafael continua funcionário; Davi é o profissional do grupo de formação. Helena continua personagem da rotina admirável; Vera é outro caso, de controle relacional. Não há novo fato biográfico atribuído a Sol.

## 6. Fontes e seus limites

As fontes utilizadas e reconferidas estão em `REFERENCIAS_DE_TRABALHO.md`, com identificação bibliográfica, destino, condição de acesso e limites. Parte III: Fazio; Montoya; Ryan/Deci; Swann e colegas; Kunda; Hartgerink e colegas; Home Office; Ministério das Mulheres. Partes anteriores: rechecadas referências de desenvolvimento, autonomia, comparação, relações parassociais e documentação de plataformas.

Não se declara validação científica da lente autoral. A consulta a resumo primário é distinguida de acesso integral. Documentação estrangeira não é tratada como legislação brasileira. Uma indisponibilidade da rota original do TikTok foi resolvida por fonte oficial alternativa e registrada, não escondida.

## 7. Integridade verificável

- Base: `{INPUT_BLOB}`.
- Manuscrito e snapshot: `{output_blob}`.
- SHA-256: `{digest}`.
- Snapshot: `{snapshot.relative_to(root).as_posix()}`.
- 12 capítulos em sequência, três partes, notas e introdução preservadas.
- Snapshots anteriores comparados por SHA-256 e mantidos byte a byte.
- `QA_ETAPA_04.json` contém contagens, hashes e limites do teste.

Foi utilizada rotina temporária de GitHub Actions para exportação, consolidação e conferência. Ela não governa decisões editoriais e deve ser retirada depois da verificação, para não deixar uma tarefa futura capaz de duplicar texto. Nenhuma automação permanente é parte desta entrega.

## 8. Pendências reais

Leitura e aprovação de Sol; conclusão das Partes IV–VI e epílogo; lapidação final de ritmo, terminologia, referências e diagramação; conferência visual das figuras legadas; revisão técnica de serviços e plataformas antes de publicar. Não foram gerados nem validados Kindle Create, KPF, EPUB ou PDF nesta etapa.

## 9. Próxima execução

ETAPA 05 — Parte IV: O Eu Emprestado em Funcionamento, capítulos 13–16. Seguir `PROMPT_PROXIMA_ETAPA_05.md`. Preservar as distinções científicas, os nomes e os snapshots; criar corpo de livro, não outra arquitetura.
'''
    report = report.replace('adição de 14 mil palavras', f'adição de {fmt(words(new_part))} palavras')
    writes = {master:content, snapshot:content, root/'PARTE_III_ETAPA_04.md':new_part.encode(),
              root/'STATUS.md':status.encode(), root/'HISTORICO_ETAPAS.md':history.encode(),
              map_path:map_text.encode(), refs_path:refs.encode(),
              root/'REGISTRO_EDITORIAL_ETAPA_04.md':report.encode(),
              root/'QA_ETAPA_04.json':(json.dumps(qa,ensure_ascii=False,indent=2)+'\n').encode(),
              root/'REVISOES_ETAPA_04.json':(json.dumps(revisions,ensure_ascii=False,indent=2)+'\n').encode(),
              root/'DIFF_TEXTO_ANTERIOR_ETAPA_04.patch':''.join(difflib.unified_diff(old_bytes.decode().splitlines(True),old.splitlines(True),fromfile='ETAPA_03',tofile='ETAPA_04_texto_preexistente_revisado')).encode()}
    for k,v in loaded.items(): writes[root/'PRODUCAO_ETAPA_04'/k]=v.encode()
    for p,data in writes.items():
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(data)
    assert master.read_bytes() == snapshot.read_bytes()
    for name,d in frozen.items():
        assert hashlib.sha256((root/name).read_bytes()).hexdigest()==d, name
    assert history.startswith(history_before), 'Histórico anterior precisa continuar integral.'
    print(json.dumps(qa,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
