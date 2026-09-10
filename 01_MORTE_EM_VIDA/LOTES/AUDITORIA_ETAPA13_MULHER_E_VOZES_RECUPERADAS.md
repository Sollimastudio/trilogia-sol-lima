# AUDITORIA — ETAPA 13
## A Mulher que Quase Não Viveu + recuperação de vozes estruturais

**Data:** 10/09/2026  
**Estado:** arquitetura aprovada para execução antes da prosa.

## 1. Achado principal da auditoria
Ao confrontar o repositório canônico atual com os manuscritos e registros anteriores, foram identificadas três peças literárias importantes que existiam no acervo, mas ainda não haviam sido transplantadas como unidades autônomas para o novo repositório:

1. **Prólogo — O Portão**;
2. **Monólogo de divórcio/pós-divórcio — Agora eu não posso errar**;
3. **A Criança que Não Devia Nada** — reencontro posterior com a criança ingênua/inocente.

Essas peças não serão tratadas como “extras”. Elas passam a integrar a engenharia viva do manuscrito.

---

# 2. PRÓLOGO — O PORTÃO

## Evidência editorial
Diversas arquiteturas anteriores tratam `O Portão` como prólogo fora da cronologia. A função é abrir a ferida central e voltar depois a 1978 para responder: **como uma mãe chegou até aquele portão?**

## Situação no repositório antes desta etapa
A cena do Portão já existia cronologicamente em MV-28/MV-29, mas **não existia como cold open autônomo**.

## Decisão
Criar:
`CAPITULOS/MV-P01_PROLOGO_O_PORTAO.md`

### Função
- abrir depois da Nota Forense;
- começar no ferro/corpo, sem explicação processual;
- mostrar filho inacessível e mãe recebida como risco;
- cortar antes de explicar Caldas, Mãe-Véia, psicóloga, liminar ou processo;
- terminar prometendo retorno à origem.

### Regra anti-repetição
MV-P01 mostra o efeito. MV-28/MV-29 explicam cronologicamente como o Portão foi soldado. Não duplicar a cena inteira.

### Proteções
- portão cinza / cobertura verde conforme referência canônica;
- não usar `Relatório de Judas`, `laudo forjado`, `psicóloga comprada`, `escola cúmplice`, `juiz corrupto`, `sequestro legal` ou `alienação parental` como sentença;
- não inserir número de batimentos não documentado;
- não explicar o processo no prólogo.

---

# 3. MONÓLOGO — AGORA EU NÃO POSSO ERRAR

## Fonte recuperada
Existe versão consolidada de aproximadamente 3 mil palavras: `Morte_em_Vida_Monologo_Agora_Eu_Nao_Posso_Errar_V1`.

## Posição correta
**Depois de MV-22 — A Porta Depois da Saída e antes de MV-I05 — Finalmente?**

É uma ponte II → III: a convivência terminou, mas a mulher não emerge autônoma e esclarecida. Ela entra no pós-divórcio carregando culpa espiritual, medo de errar, confusão sobre corpo, futuro e direção divina.

## Código
`MV-M01 — Agora Eu Não Posso Errar`

## Forma
Pensamento direto no tempo vivido. Não é ensaio retrospectivo.

## Núcleos obrigatórios preservados
- resistência anterior ao divórcio;
- medo de condenação espiritual;
- culpa sentida por pedir o divórcio;
- culpa internalizada pelas traições, embora a responsabilidade permaneça de quem traiu;
- `você faz eu pecar` como fala lembrada;
- sensação de corpo/juventude inadequados;
- pensamento autorizado: `preciso mudar meu corpo`;
- filhos e teto como centro imediato;
- ausência de projeto consciente de “nova mulher”;
- crença de que Deus mostraria o próximo passo;
- mandiocal como lugar de conversa/pedido de perdão;
- mensagem `banho de loja` e confusão entre elogio, crítica, vaidade e pecado;
- memória do batismo precoce / responsabilidade;
- memória breve da queda do tanque e interpretação religiosa da época;
- rego de água distinto do mandiocal; não há entrada na água;
- fecho: `Eu pedi o divórcio, Deus. Mas não queria que o Senhor fosse embora também.`

## Ingenuidade
Aqui `ingenuidade` significa **não possuir ainda as compreensões posteriores**. Não significa pouca inteligência, infantilização ou incapacidade. A personagem é prática, trabalhadora, religiosa, sensível e confusa sobre a própria posição.

### Proibido
Não colocar dentro da cabeça dela, naquele período:
- `estou me apagando`;
- `preciso assumir as rédeas`;
- `quem sou além de mãe?`;
- teoria de autoestima, posicionamento, trauma ou identidade que só veio depois.

---

# 4. A CRIANÇA QUE NÃO DEVIA NADA

## Fonte recuperada
Versões antigas possuem uma peça chamada `A Criança que Não Devia Nada`, posicionada depois do Sepultamento Simbólico.

## Função correta
É o pagamento da **criança ingênua/inocente** depois que a dívida com Oripe foi separada da vida da narradora.

Não é a criança falando com vocabulário adulto. É a narradora adulta conseguindo, finalmente, olhar a criança sem colocá-la no banco dos réus.

## Posição
**Depois de MV-39 — O Sepultamento Simbólico e antes de MV-40 — A Investigadora Ganha Linguagem.**

## Código
`MV-I06 — A Criança que Não Devia Nada`

## Núcleos
- olhar para a criança com ternura, não cobrança;
- reconhecer a disciplina autopunitiva do `mais`: mais boa, menor, silenciosa, útil, santa etc.;
- devolver à criança corpo, fome, xixi, cocô, cabelo, medo, raiva, alegria e desejo sem culpa automática;
- `a criança que eu fui não devia nada`;
- `inocente` no sentido específico de não ter causado a morte de Oripe nem ser responsável por dores adultas;
- não transformar essa inocência específica em santificação geral;
- abrir possibilidade de retorno à voz/corpo/vida;
- não ensinar Reposicione-se.

---

# 5. VI-L5-001–012 — A MULHER QUE QUASE NÃO VIVEU

## Fatos e camadas
### Confirmado no núcleo autobiográfico/autoral
- Sol reconhece que viveu por muito tempo principalmente como filha, esposa, mãe, crente/pastora, cuidadora, trabalhadora, sobrevivente e investigadora;
- percebe ausência de experiências escolhidas apenas por gosto/presença;
- participa do programa `Mulher Magnética`, atribuído a Vanessa de Oliveira;
- essa experiência entra como formação/experiência pessoal, não terapia ou validação científica;
- existe um TCC no qual Sol viveu/aplicou um processo posteriormente associado à origem vivida do Magnetus;
- Magnetus evolui de investigação pessoal de atração/presença para protocolo posterior;
- nasce a direção autoral de autorrelacionamento que amadurece em Relacione-se.

### Lacunas preservadas
Não foram localizados com segurança suficiente para publicação:
- data do Mulher Magnética;
- curso do TCC;
- instituição do TCC;
- título exato do TCC;
- data do TCC;
- ordem fina entre Mulher Magnética, DISC, Master Love e TCC;
- data em que o nome `Magnetus` foi adotado;
- data formal de nascimento do Relacione-se.

Nenhuma dessas lacunas será preenchida por acabamento literário.

## Decisão de arquitetura
Um capítulo principal basta:

### MV-41 — A Mulher que Quase Não Viveu
**Movimento:**
`sei explicar → ainda não sei viver → estranhamento diante da própria preferência → Mulher Magnética como experiência → corpo sem tribunal → gosto → desejo → limite → presença → TCC como laboratório ainda documentalmente incompleto → experiência é observada → Magnetus nasce depois como organização → Relacione-se surge como direção de autorrelacionamento`.

### Função
Mostrar que a mulher não precisava ser fabricada. Precisava receber experiência, escolha e presença.

### Fronteira
- Magnetus entra como fruto biográfico, não produto;
- Relacione-se entra como consequência, não marca em campanha;
- Reposicione-se não é ensinado;
- Fuga Identitária não é desenvolvida.

---

# 6. CONTAGEM DA ETAPA
Antes da ETAPA 13: **46 unidades V1/V1.1**.

Serão acrescentadas quatro unidades canônicas:
- MV-P01 — Prólogo — O Portão;
- MV-M01 — Agora Eu Não Posso Errar;
- MV-I06 — A Criança que Não Devia Nada;
- MV-41 — A Mulher que Quase Não Viveu.

**Total projetado após a etapa: 50 unidades em primeira escrita.**

## Observação de versionamento
MV-P01, MV-M01 e MV-I06 são **cirurgias retroativas controladas**. Elas não alteram snapshots históricos das Etapas 04–12. Os mapas vivos serão atualizados e a renumeração final ocorrerá no Manuscrito Alfa.
