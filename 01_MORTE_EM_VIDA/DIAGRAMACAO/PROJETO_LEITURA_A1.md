# PROJETO DE LEITURA — A1

## Finalidade

Reunir a abertura, as quatro Partes e o encerramento em uma prova de desenvolvimento que possa ser lida sem comentários de produção no meio do texto. O acabamento não equivale a aprovação factual, literária, jurídica ou autoral.

## Fonte e ordem

Usar `ORDEM_LEITURA_A1.json` com 55 códigos únicos. Cada código deve corresponder exatamente a um arquivo em `CAPITULOS/`. Extrair somente o corpo posterior ao marcador de texto literário; nas notas forenses, usar seu marcador específico. Não cortar o monólogo pós-divórcio para ajustar extensão. Não ordenar arquivos alfabeticamente.

## Projeto tipográfico da prova

- Formato de página: 6 × 9 polegadas (15,24 × 22,86 cm).
- Miolo preto sobre branco, orientado à leitura, não reprodução da capa comercial definitiva.
- Corpo serifado, aproximadamente 10,6 pontos e entrelinha de 14,2 pontos nesta configuração; tamanhos da edição final serão revistos com o texto estabilizado.
- Títulos com hierarquia consistente; divisões de Partes e identificação de prólogo, interlúdios, monólogo e epílogo.
- Sumário do PDF composto a partir da paginação efetiva, com marcadores para as unidades.
- Cabeçalho discreto e rodapé identificando a prova A1, sem ISBN ou ficha catalográfica inventados.
- O DOCX editável tem navegação pelos títulos; sua repaginação não é obrigatoriamente igual à do PDF.
- A versão HTML é fluida, funciona sem recursos externos e não deve exigir uma instalação para leitura.

## Verificações exigidas em cada exportação

1. Conferir a integridade dos arquivos-fonte contra o manifesto da exportação disponível.
2. Confirmar a quantidade de códigos, correspondência única por arquivo e ausência de reservas contadas como prosa pronta.
3. Registrar palavras, hashes e página inicial de cada unidade.
4. Detectar páginas vazias e conferir a presença do encerramento.
5. Conferir visualmente sumário, títulos, divisões, margens e páginas representativas, separando essa conferência dos testes automáticos.
6. Manter os relatórios de pendências fora do miolo de leitura.

Nenhum contador de páginas indica percentual de conclusão do livro. A prova pode crescer ou diminuir com a revisão de repetições, parágrafos e cenas.

## Imagens

Esta configuração é tipográfica. Ilustrações e fotografias definitivas dependem de seleção, fontes, direitos, pertinência e posição editorial. Não usar imagem gerada como evidência documental. Não inserir imagem apenas para ocupar página ou representar uma ocorrência ainda não recuperada.

Não distribuir arquivos de fontes tipográficas no pacote. A exportação do repositório é uma cópia dos arquivos rastreados selecionados, não do histórico Git completo.

## Continuidade

As novas versões da prova devem indicar seu commit de origem e manifestar quais textos foram alterados. A prosa e os mapas ficam versionados no GitHub; anexos PDF/DOCX só devem ser descritos como armazenados no repositório se houver gravação específica desses binários.