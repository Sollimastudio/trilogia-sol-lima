from build_visuals import *

def tree():
    p=Plate('03_arvore_do_discernimento','A Árvore do Discernimento','Localize a investigação. Uma parte não explica tudo.')
    p.art('arvore_base_cor',102,117,228,276)
    for i,(x,y) in enumerate([(273,182),(163,226),(218,280),(195,359),(269,337),(339,272)],1):
        p.circle(x,y,9);p.text(str(i),x-3,y+3,8,'Bold',GOLD)
    rows=[('1  FRUTOS','Resultados observáveis.'),('2  GALHOS','Áreas da vida e vínculos.'),('3  TRONCO','Valores e limites praticados.'),('4  RAÍZES','Histórias, crenças e hábitos.'),('5  SOLO','Modo de receber e responder.'),('6  AMBIENTE','Condições e influências externas.')]
    for i,(a,b) in enumerate(rows):
        x=30+(i%2)*190;y=416+(i//2)*51
        p.text(a,x,y,10,'Bold',GOLD,180);p.text(b,x,y+17,9,'Body',WHITE,177)
    p.text('Semente é a atitude plantada. Pragas são mecanismos\nque drenam o cultivo; pessoas não são pragas.',30,578,10,'Body',WHITE,372)
    return p.finish('Os números localizam a metáfora; não atribuem uma causa ao fruto.')

def soil():
    p=Plate('04_semente_solo_raizes_ambiente','O que você está investigando?','Quatro conceitos que precisam permanecer distintos.')
    rows=[('SEMENTE · atitude plantada','O que eu efetivamente fiz, decidi ou pratiquei?'),('SOLO · modo operante','Como recebo, interpreto e respondo ao que acontece?'),('RAÍZES · sustentação aprendida','Que crença, hábito ou lealdade sustenta minha resposta?'),('AMBIENTE · condições externas','Que regras, recursos, pressões ou restrições interferem?')]
    for i,(a,b) in enumerate(rows):p.box(30,132+i*89,372,75,a,b)
    p.rect(30,508,372,85,RED,LINE,6);p.text('INVESTIGUE A COMBINAÇÃO',43,530,10.5,'Bold',GOLD)
    p.text('Um mesmo resultado pode envolver prática, modo operante,\naprendizagens e condições externas. Registre o que sabe\ne o que ainda precisa verificar.',43,548,9.4,'Body',WHITE,347)
    return p.finish('A analogia autoral se inspira na Parábola do Semeador.')

def fruits():
    p=Plate('05_avaliacao_dos_frutos','Observe os frutos','O resultado inicia a investigação. Não define seu valor.')
    p.art('frutos_base_cor',30,132,372,148)
    p.text('Estados diferentes pedem perguntas, não sentenças.',30,300,11,'Bold',GOLD,372)
    rows=[('DESCREVA','Qual resultado você observou? Em que área e período?'),('COMPARE','O que melhorou, piorou ou permaneceu? Qual é a referência?'),('INVESTIGUE','O que depende de você, de outra pessoa e do contexto?'),('ESCOLHA','O que preservar? Que prática ou condição precisa mudar?')]
    for i,(a,b) in enumerate(rows):
        y=326+i*64;p.text(a,30,y,10,'Bold',GOLD);p.text(b,30,y+17,9.6,'Body',WHITE,372)
    return p.finish('As imagens simbolizam estados; a aparência não comprova a causa.')

def patterns():
    p=Plate('06_padrao_e_metacognicao','Como um padrão se repete','Encontre um ponto de intervenção na situação concreta.')
    for y,a,b in [(133,'SITUAÇÃO + CONDIÇÕES','O que ocorreu? Que recursos e restrições havia?'),(211,'LEITURA + EMOÇÃO','O que pensei? O que senti? O que pressupus?'),(291,'RESPOSTA HABITUAL','O que fiz, permiti, adiei ou repeti?'),(371,'FRUTO OBSERVADO','O resultado reforçou ou contrariou minha leitura?')]:
        p.box(66,y,300,62,a,b)
        if y<371:p.arrow(216,y+62,216,y+78)
    p.line(66,402,18,402);p.line(18,402,18,241);p.arrow(18,241,66,241);p.arrow(216,433,216,457)
    p.box(30,457,372,74,'SUBA AO MIRANTE','Examine como pensou. Busque evidência e outra leitura.\nEscolha uma resposta possível e reveja o resultado.')
    p.text('Repetição é uma pista para investigar.\nNão prova que a causa esteja sempre dentro de você.',30,568,10,'Body',WHITE,372)
    return p.finish('Metacognição: observar, examinar e ajustar o próprio pensamento.')

def alignment():
    p=Plate('07_alinhamento_em_pratica','Alinhamento em prática','A posição ganha consistência quando chega à conduta.')
    p.box(30,135,176,83,'VALORES + LIMITES','O que você considera importante e precisa sustentar?')
    p.box(226,135,176,83,'FATOS + CONDIÇÕES','Que evidências, deveres, recursos e riscos existem?')
    p.line(118,218,118,239);p.line(314,218,314,239);p.line(118,239,314,239);p.arrow(216,239,216,258)
    for y,a,b in [(258,'FILTRO DA SENSATEZ','Examine a leitura e o movimento pretendido.'),(344,'DECISÃO + PRÁTICA','O que fará? Como comunicará? Que acordo precisa existir?'),(430,'FRUTOS + REVISÃO','A conduta se aproximou dos valores? O que ajustar?')]:
        p.box(66,y,300,65,a,b)
        if y<430:p.arrow(216,y+65,216,y+86)
    p.line(366,464,415,464);p.line(415,464,415,286);p.arrow(415,286,366,286)
    p.text('O Tronco sustenta a prática nos diferentes Galhos.\nRever uma decisão diante de evidência também é coerência.',30,558,10,'Body',WHITE,372)
    return p.finish('O Filtro examina a interpretação; não é apenas outro nome para ela.')

def numbered_page(slug,title,subtitle,rows,start=1,footer=''):
    p=Plate(slug,title,subtitle);gap=444/len(rows)
    for i,(a,b) in enumerate(rows):
        y=131+i*gap;p.rect(30,y,372,gap-8,RED,LINE,5);p.circle(49,y+20,10);n=str(start+i)
        p.text(n,46 if len(n)==1 else 43,y+23,8,'Bold',GOLD)
        yy=p.text(a,68,y+20,10.3,'Bold',GOLD,319,13)
        if b:p.text(b,68,yy+17,9.1,'Body',WHITE,319,12)
    return p.finish(footer or 'Escolha o que se aplica à situação. Registre fatos, não rótulos.')

def filters():
    canon=json.loads((ROOT/'FONTES/canon.json').read_text())
    questions=re.findall(r'^## \d+\. (.+)$',canon['filter'],re.M);assert len(questions)==12
    return [numbered_page('08_filtro_1_a_6','Filtro da Sensatez · 1','Primeiro, examine a leitura da situação.',[(q,'') for q in questions[:6]],1,'Registre o que sabe, o que infere e o que ainda não sabe.'),numbered_page('09_filtro_7_a_12','Filtro da Sensatez · 2','Depois, examine responsabilidades e possibilidades.',[(q,'') for q in questions[6:]],7,'Encerre o exame quando houver base suficiente para um passo possível.')]

def faith():
    p=Plate('10_inspiracao_biblica','Uma orientação para a atenção','Inspiração cristã da autora · Filipenses 4:8')
    for i,t in enumerate(['Verdadeiro','Respeitável','Justo','Puro','Amável','De boa fama','Virtude','Louvor']):
        x=30+(i%2)*190;y=139+(i//2)*73;p.rect(x,y,182,58,RED,LINE,6);p.text(t,x+13,y+34,13,'Title',GOLD,158)
    p.text('Em que você tem colocado sua atenção?',30,478,13,'Bold',GOLD,372)
    p.text('Esta inspiração orienta a reflexão da autora.\nNa aplicação do método, use também as doze perguntas\ndo Filtro: fatos, evidências, responsabilidades e ação.',30,511,10.3,'Body',WHITE,372,15)
    return p.finish('Os oito termos não substituem as doze perguntas do Filtro.')

def laws():
    canon=json.loads((ROOT/'FONTES/canon.json').read_text())
    titles=re.findall(r'^### Lei \d+ — (.+)$',canon['laws'],re.M);assert len(titles)==14
    notes=['Descreva o resultado antes de explicá-lo.','Dê atenção ao que os fatos já mostram.','Crie espaço entre sentir e responder.','Perceba a resposta que se tornou automática.','Examine a história que conta sobre o fato.','Abra espaço para ouvir e examinar.','Reconheça a parte que cabe a você.','Considere compromissos e acordos existentes.','Inclua as consequências que chegam depois.','Examine a mensagem e sua forma de atuação.','Pertencer não exige suspender o discernimento.','Busque evidências e aceite rever a conclusão.','Tolere o custo proporcional de uma prática nova.','Sustente coerência com sensatez e responsabilidade.']
    return [numbered_page('11_leis_1_a_7','14 Leis do Posicionamento','Critérios de conduta · 1 a 7',list(zip(titles[:7],notes[:7])),1),numbered_page('12_leis_8_a_14','14 Leis do Posicionamento','Critérios de conduta · 8 a 14',list(zip(titles[7:],notes[7:])),8)]

def influences():
    p=Plate('13_mapa_de_influencias','Mapa de influências','Observe como a influência atua em uma relação concreta.')
    rows=[('Pensamento','Posso pensar diferente e explicar por quê?'),('Informação','Posso consultar e comparar outras fontes?'),('Emoção','Culpa ou vergonha são usadas para me controlar?'),('Identidade','Posso preservar valores e uma voz própria?'),('Vínculos','Meus outros relacionamentos são restringidos?'),('Medo','Há ameaças ou punições para obter obediência?'),('Questionamento','Posso perguntar e discordar sem intimidação?'),('Saída','Posso me afastar? Quais riscos e dependências existem?')]
    for i,(a,b) in enumerate(rows):p.box(30+(i%2)*190,133+(i//2)*90,182,80,a,b)
    p.text('REGISTRE: observei · não observei · ainda não sei',30,518,10,'Bold',GOLD,372)
    p.text('Anote um fato e uma explicação alternativa.\nConcordar com alguém ou pertencer a um grupo, por si só,\nnão demonstra influência indevida.',30,544,9.7,'Body',WHITE,372,14)
    return p.finish('Roteiro de reflexão do Workbook. Não comprova “lavagem cerebral”.')

def mirrors():
    rows=[('Soberano','Sustenta escolhas e aceita revisão; observe o risco de controlar.'),('Vulcão','A intensidade governa a resposta antes do exame.'),('Névoa','A decisão se prolonga para evitar o custo de escolher.'),('Fantasma','A própria voz diminui para preservar pertencimento.'),('Espelho Partido','O valor próprio oscila conforme a aprovação recebida.'),('Ator','A performance esperada toma o lugar da prática real.'),('Herdeiro','Uma regra herdada é seguida sem exame pessoal.'),('Náufrago','A urgência por segurança transfere a decisão a um resgate.'),('Eco','Uma ideia é repetida antes de ser examinada.'),('Vitrine','A imagem e a plateia governam a escolha.'),('Muro','A defesa impede a entrada de uma informação contrária.'),('Espelho','Preservar a imagem de estar certo bloqueia a revisão.'),('Templo','A linguagem da fé ocupa o lugar da ação responsável.'),('Camaleão','A adaptação cobra o preço dos próprios valores e limites.')]
    return [numbered_page('14_espelhos_1_a_7','14 Espelhos · 1','Observe uma posição numa área e num período.',rows[:7],1,'Espelhos de situações; não são diagnósticos ou identidades fixas.'),numbered_page('15_espelhos_8_a_14','14 Espelhos · 2','Uma pessoa pode ocupar posições diferentes conforme o contexto.',rows[7:],8,'Escolha até dois Espelhos para investigar e levar à prática.')]

def compassion():
    p=Plate('16_autopiedade_e_autocompaixao','A dor e o próximo passo','Reconhecer o sofrimento pode abrir espaço para o cuidado.')
    p.art('autopiedade_base_cor',152,120,128,170)
    p.box(30,314,181,164,'AUTOPIEDADE','A dor ocupa toda a leitura e apaga o movimento possível.\n\nPergunta de exame:\nEstou transformando o que sofri na única explicação para o que posso fazer?')
    p.box(221,314,181,164,'AUTOCOMPAIXÃO','A dor é reconhecida junto das necessidades, dos limites e do cuidado possível.\n\nPergunta de cuidado:\nDo que preciso para dar o próximo passo?')
    p.text('Na experiência de Sol Lima, a autopiedade foi a praga\nmais prejudicial. Essa prioridade nasce da sua história.',30,515,10,'Body',GOLD,372)
    p.text('Precisar de tempo, apoio ou proteção não é autopiedade.\nAcolher a dor e assumir responsabilidade podem coexistir.',30,561,9.6,'Body',WHITE,372)
    return p.finish('A metáfora examina um mecanismo; não diminui a pessoa que sofre.')

def illustrated(slug,title,subtitle,key,lead,body,footer):
    p=Plate(slug,title,subtitle);p.art(key,105,120,222,330)
    yy=p.text(lead,30,481,12,'Bold',GOLD,372,16);p.text(body,30,yy+27,10,'Body',WHITE,372,14)
    return p.finish(footer)

def workbook():
    p=Plate('20_workbook_porta_de_entrada','Do livro ao Workbook','Três instrumentos para registrar e examinar situações.')
    rows=[('TESTE DO POSICIONAMENTO','Observe os 14 Espelhos numa área da vida e escolha até dois para investigar.'),('TESTE DA ÁRVORE','Localize o Fruto, diferencie as partes da Árvore e examine as condições externas.'),('TESTE DE INFLUÊNCIA INDEVIDA','Examine autonomia, formas de pressão e liberdade real numa relação específica.')]
    for i,(a,b) in enumerate(rows):p.box(30,135+i*103,372,85,a,b)
    p.box(30,461,372,73,'FICHA COMPLEMENTAR · AUTOPIEDADE','A ficha F17 aprofunda o exame da autopiedade.\nEla não constitui um quarto teste obrigatório.')
    p.text('Registre um fato, uma hipótese, um passo e uma revisão.\nO livro oferece a travessia; o Workbook organiza o registro.',30,570,9.5,'Body',WHITE,372)
    return p.finish('Instrumentos de reflexão autoral em versão editorial 0.1.')

def branches():
    p=Plate('21_tronco_e_galhos','Um Tronco, vários Galhos','Investigue a área em que a posição aparece.')
    p.box(92,132,248,70,'TRONCO','Valores, limites e acordos que você sustenta na prática.')
    p.line(216,202,216,222);p.line(119,222,309,222)
    for x in [119,309]:p.arrow(x,222,x,241)
    rows=[('Vínculos','Amor, família e convivência.'),('Trabalho','Carreira e marca pessoal.'),('Dinheiro','Compromissos e escolhas.'),('Fé e corpo','Convicções e autocuidado.'),('Vida pública','Participação e política.'),('Redes','Presença e relações digitais.')]
    for i,(a,b) in enumerate(rows):p.box(30+(i%2)*190,241+(i//2)*83,182,71,a,b)
    p.text('UMA ÁREA NÃO É A VIDA INTEIRA',30,522,11,'Bold',GOLD,372)
    p.text('Uma pessoa pode sustentar limites no trabalho e ter\ndificuldade de praticá-los na família. Escolha um Galho,\numa situação e um período para começar.',30,548,10,'Body',WHITE,372,14)
    return p.finish('Áreas exemplificativas. Preserve o que já funciona em cada Galho.')

def commands():
    p=Plate('22_comandos_do_pensamento','Três comandos para pensar','Do automático ao exame consciente.')
    for y,title,body in [(136,'PENSE NISSO','Observe e nomeie fato, emoção e pensamento antes da resposta automática.'),(251,'REPENSE ISSO','Examine interpretação, evidência, contraditório e alternativas.'),(366,'PENSE COMIGO','Acompanhe e teste o raciocínio: razão, emoção, contexto e consequência.')]:
        p.box(30,y,372,90,title,body)
        if y<366:p.arrow(216,y+90,216,y+115)
    p.text('Pensar comigo não exige concordar comigo.',30,508,12,'Bold',GOLD,372)
    p.text('O exercício é examinar como a conclusão foi construída.\nDepois, desça da Árvore: escolha uma ação possível\ne volte para observar os frutos.',30,540,10,'Body',WHITE,372,14)
    return p.finish('Pense nisso: observe. Repense isso: examine. Pense comigo: teste.')

def pest():
    p=Plate('18_pragas_e_ambiencia','Pragas e ambiência','Observe o dano localizado antes de procurar a causa.')
    p.art('pragas_cor',40,122,270,330)
    p.text('GALHO AFETADO',282,153,8.7,'Bold',GOLD,119)
    p.text('Folhas danificadas;\no restante da árvore\nsegue preservado.',290,171,8.4,'Body',WHITE,108,12)
    p.arrow(315,205,260,231)
    p.text('Pessoas não são pragas.',30,481,12,'Bold',GOLD,372)
    p.text('No método, investigue a conduta, a pressão ou o mecanismo\nque drena. Considere o contexto do outro, converse quando\npossível e estabeleça acordos e limites proporcionais.',30,510,9.8,'Body',WHITE,372,14)
    p.text('O desenho ilustra um caso; nem todo problema é externo.',30,583,9.3,'Body',GOLD,372)
    return p.finish('Empatia, proteção e responsabilidade podem caminhar juntas.')

def all_pages():
    return [journey(),cycle(),tree(),soil(),fruits(),patterns(),alignment(),*filters(),faith(),*laws(),influences(),*mirrors(),compassion(),
    illustrated('17_jaula_e_sofa','A Jaula e o Sofá','Uma metáfora da experiência da autora.','jaula_sofa_cor','Que história mantém você no mesmo lugar?','Na história de Sol, a porta estava aberta e o Sofá oferecia\num conforto conhecido. Examine a sua situação concreta:\nqual porta existe e de que condição você precisa para sair?','A porta possível depende também de recursos, apoio e segurança.'),
    pest(),
    illustrated('19_poda_e_nova_semente','Poda e nova Semente','Uma mudança específica que possa chegar à prática.','poda_semente_cor','O que interromper? O que praticar no lugar?','Escolha uma resposta, exposição ou permissão a ajustar.\nPlante uma atitude observável e defina quando avaliar\nos frutos. Preserve o que já funciona.','Poda não é uma ordem para retirar pessoas da sua vida.'),workbook(),branches(),commands()]

if __name__=='__main__':
    pages=all_pages();merged=fitz.open()
    for file in pages:
        with fitz.open(file) as src:merged.insert_pdf(src)
    merged.save(OUT/'Caderno_Visual_Colorido.pdf',deflate=True);merged.close()
    print(json.dumps({'pages':len(pages),'output':str(OUT)},ensure_ascii=False))
