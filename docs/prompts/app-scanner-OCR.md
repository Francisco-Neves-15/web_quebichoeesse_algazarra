# Projeto: Scanner OCR para digitalização das cartas

Você é o agente responsável por desenvolver uma aplicação local para digitalizar cartas físicas de um jogo.

## Objetivo

Preciso transformar aproximadamente **125 cartas físicas** em dados digitais.

Cada carta possui:

* 1 nome de animal;
* 8 dicas sobre o animal;
* portanto, aproximadamente **1.125 campos de texto** no total, considerando nomes + dicas.

A aplicação deverá utilizar uma câmera ou imagens das cartas para:

1. capturar/receber a imagem;
2. localizar a carta;
3. corrigir rotação e perspectiva;
4. melhorar a imagem para OCR;
5. identificar e extrair o nome e as 8 dicas;
6. converter o resultado para dados estruturados;
7. permitir revisão manual dos resultados;
8. salvar os dados em formato apropriado.

## Restrição importante

**Não quero utilizar uma LLM ou serviço de IA generativa como solução principal de OCR.**

A primeira implementação deve utilizar ferramentas tradicionais/localmente executáveis, preferencialmente:

* Python;
* OpenCV;
* Tesseract OCR e/ou outro mecanismo OCR local adequado;
* bibliotecas Python auxiliares quando necessário.

Não utilizar APIs pagas ou serviços externos sem que isso seja previamente justificado.

A prioridade é que o processamento possa funcionar **localmente e offline**.

---

# Primeira tarefa: analisar o projeto antes de implementar

Antes de escrever uma grande quantidade de código, analise toda a pasta do projeto e identifique:

* estrutura existente;
* arquivos;
* imagens de cartas eventualmente existentes;
* exemplos de cartas;
* documentação;
* dependências já instaladas;
* versão do Python;
* ferramentas OCR já disponíveis;
* qualquer código relacionado ao projeto.

Não assuma que todas as cartas possuem exatamente a mesma aparência.

Produza primeiro uma análise técnica curta indicando:

1. o que foi encontrado;
2. quais arquivos/imagens podem ser usados como amostras;
3. quais características visuais das cartas precisam ser consideradas;
4. quais ferramentas existentes podem ser aproveitadas;
5. qual arquitetura inicial você recomenda.

Depois dessa análise, prossiga para a implementação da prova de conceito.

---

# Característica importante das cartas

As cartas possuem estrutura semelhante, mas **o tamanho da fonte das dicas pode variar entre cartas**.

Isso acontece porque algumas dicas possuem textos maiores e, para que caibam na área disponível durante a impressão, determinadas cartas possuem fonte menor.

Portanto:

**NÃO implemente o OCR assumindo que todas as dicas possuem o mesmo tamanho de fonte.**

O sistema deverá ser capaz de trabalhar com:

* fontes maiores;
* fontes menores;
* diferentes densidades de texto;
* diferentes quebras de linha;
* textos mais longos;
* textos mais curtos.

Não use o tamanho da fonte como único critério para identificar uma dica.

---

# Arquitetura desejada

A arquitetura inicial deverá ser aproximadamente:

```text
Imagem / Câmera
       ↓
Detecção da carta
       ↓
Correção de perspectiva
       ↓
Normalização da imagem
       ↓
Detecção/recorte das regiões de texto
       ↓
Pré-processamento específico da região
       ↓
OCR
       ↓
Pós-processamento
       ↓
Identificação:
    - nome
    - dica 1
    - dica 2
    ...
    - dica 8
       ↓
Validação
       ↓
Revisão manual
       ↓
JSON / outro formato estruturado
```

Porém, não considere essa arquitetura definitiva. Se a análise das imagens mostrar uma abordagem melhor, explique a mudança e implemente-a.

---

# Etapa 1 — Prova de conceito OCR

Antes de implementar a câmera ou uma interface complexa, crie uma ferramenta capaz de processar imagens existentes.

A ferramenta deverá aceitar algo como:

```text
input/
    carta_001.jpg
    carta_002.jpg
    carta_003.jpg
```

e gerar:

```text
output/
    carta_001.json
    carta_002.json
    carta_003.json
```

Exemplo:

```json
{
    "id": 1,
    "animal": "Capivara",
    "clues": [
        "Dica 1...",
        "Dica 2...",
        "Dica 3...",
        "Dica 4...",
        "Dica 5...",
        "Dica 6...",
        "Dica 7...",
        "Dica 8..."
    ]
}
```

Também deverá existir uma forma de visualizar o texto bruto retornado pelo OCR para diagnóstico.

---

# Etapa 2 — Não assumir um único pré-processamento

Como o tamanho das fontes varia, desenvolva o OCR de maneira experimental.

Para uma região de texto, considere testar automaticamente diferentes técnicas, por exemplo:

* escala da imagem;
* grayscale;
* aumento de contraste;
* threshold binário;
* adaptive threshold;
* remoção de ruído;
* sharpening;
* diferentes configurações de segmentação do Tesseract;
* diferentes escalas de resolução.

O sistema não precisa executar todas as possibilidades indiscriminadamente em produção.

Primeiro, crie uma ferramenta de teste que permita comparar os resultados.

Por exemplo:

```text
Carta 023
Dica 4

Original OCR:
...

2x + threshold:
...

3x + adaptive threshold:
...

Sharpen + threshold:
...

Melhor resultado:
...
```

O objetivo é descobrir empiricamente qual pipeline funciona melhor para as cartas reais.

---

# Etapa 3 — Aproveitar o layout da carta

Se as imagens demonstrarem que o layout das cartas é suficientemente consistente, utilize isso.

Não faça OCR da imagem inteira se for possível separar as regiões.

Idealmente:

```text
┌────────────────────────────┐
│                            │
│       NOME DO ANIMAL       │
│                            │
├────────────────────────────┤
│  DICA 1                    │
│                            │
│  DICA 2                    │
│                            │
│  DICA 3                    │
│                            │
│  ...                       │
│                            │
│  DICA 8                    │
│                            │
└────────────────────────────┘
```

Entretanto, não assuma que cada dica ocupa exatamente uma altura fixa.

O sistema deverá considerar que uma dica pode ocupar:

```text
1 linha
2 linhas
3 linhas
...
```

dependendo do tamanho do texto e da fonte utilizada.

Se for mais confiável detectar blocos de texto individualmente, implemente detecção de regiões em vez de simplesmente dividir a carta em oito retângulos iguais.

---

# Etapa 4 — Avaliar diferentes mecanismos OCR

Comece testando pelo menos:

* Tesseract;
* uma alternativa OCR local moderna, caso seja viável no ambiente.

Compare os resultados usando as cartas reais.

Não escolha uma ferramenta simplesmente por popularidade.

Avalie:

* acurácia;
* desempenho;
* português;
* textos pequenos;
* textos grandes;
* acentuação;
* pontuação;
* múltiplas linhas;
* facilidade de execução local;
* facilidade de integração com Python.

Registre os resultados.

Se Tesseract for suficiente, mantenha Tesseract.

Se outra solução apresentar resultado significativamente melhor, documente o motivo da escolha.

---

# Etapa 5 — Detecção de erros

O sistema deverá ter uma camada de validação.

Por exemplo:

```python
{
    "animal": "...",
    "clues": [...]
}
```

deve ser considerado inválido se:

```text
animal ausente
menos de 8 dicas
mais de 8 dicas
dica vazia
texto extremamente curto/incomum
OCR com baixa confiança
```

Quando possível, aproveite informações conhecidas.

Por exemplo, se existir uma lista dos 125 animais, ela poderá ser utilizada para validar/corrigir o nome detectado pelo OCR.

Exemplo:

```text
OCR:
TAMANDUA-BANDE1RA

Possível correspondência:
Tamanduá-bandeira
```

Essa correção deve ser determinística, através de comparação textual/dicionário, e não depender de uma LLM.

---

# Etapa 6 — Confiança do OCR

Sempre que o mecanismo OCR fornecer informações de confiança, preserve-as.

O resultado ideal deve poder representar algo como:

```json
{
    "animal": {
        "text": "Capivara",
        "confidence": 0.98
    },
    "clues": [
        {
            "text": "...",
            "confidence": 0.94
        }
    ]
}
```

Se uma região tiver baixa confiança, ela deverá ser marcada para revisão.

Não tente esconder resultados duvidosos.

É preferível:

```text
Carta 037
Dica 5
⚠ baixa confiança
```

do que silenciosamente salvar um texto incorreto.

---

# Etapa 7 — Interface de revisão

Depois que o pipeline básico estiver funcionando, implemente uma interface simples para revisão.

Não precisa ser uma aplicação web inicialmente.

Pode ser uma aplicação desktop/local.

Ela deverá permitir:

```text
┌────────────────────────────────────────────┐
│ CARTA 037                                  │
├────────────────────┬───────────────────────┤
│                    │ Animal                │
│                    │ [ Capivara          ] │
│                    │                       │
│   imagem da carta  │ Dica 1                │
│                    │ [ ...               ] │
│                    │                       │
│                    │ Dica 2                │
│                    │ [ ...               ] │
│                    │                       │
│                    │ ...                   │
│                    │                       │
│                    │ Dica 8                │
│                    │ [ ...               ] │
├────────────────────┴───────────────────────┤
│ [Anterior] [Salvar] [Próxima]              │
└────────────────────────────────────────────┘
```

A imagem original deve permanecer disponível para comparação.

O usuário deve conseguir corrigir manualmente qualquer campo.

---

# Etapa 8 — Câmera

Somente depois que o processamento de imagens existentes estiver funcionando bem, implemente captura pela câmera.

O fluxo desejado:

```text
abrir aplicação
      ↓
visualizar câmera
      ↓
posicionar carta
      ↓
detectar carta
      ↓
capturar
      ↓
processar
      ↓
mostrar resultado
      ↓
usuário revisa
      ↓
salvar
```

A detecção da carta deve tentar identificar a borda/contorno da carta e corrigir a perspectiva.

Não obrigue o usuário a tirar a fotografia perfeitamente alinhada.

---

# Etapa 9 — Processamento em lote

Depois que uma carta funcionar corretamente, permitir:

```text
input/
    carta_001.jpg
    carta_002.jpg
    ...
    carta_125.jpg
```

e processar todas automaticamente.

O resultado deverá informar:

```text
125 cartas processadas

✓ 118 aprovadas automaticamente
⚠ 7 precisam de revisão
```

A aplicação não deverá considerar uma carta automaticamente correta simplesmente porque o OCR retornou algum texto.

---

# Organização do código

Mantenha as responsabilidades separadas.

Uma estrutura possível:

```text
src/
├── camera/
├── image_processing/
├── detection/
├── ocr/
├── parsing/
├── validation/
├── models/
├── export/
├── ui/
└── main.py
```

Não crie essa estrutura cegamente. Adapte-a ao tamanho real do projeto.

Evite criar abstrações desnecessárias durante a prova de conceito.

Priorize código simples e testável.

---

# Diagnóstico

Crie ferramentas para salvar imagens intermediárias:

```text
debug/
    original/
    detected_card/
    perspective/
    grayscale/
    threshold/
    text_regions/
    ocr/
```

Isso será importante para descobrir por que determinada carta foi mal reconhecida.

Por exemplo:

```text
carta_037_original.png
carta_037_perspective.png
carta_037_threshold.png
carta_037_dica_05.png
```

Deve ser possível abrir essas imagens e entender o que o algoritmo está fazendo.

---

# Métrica de qualidade

Não considere o projeto concluído apenas porque algumas cartas foram reconhecidas.

Crie um pequeno conjunto de referência manualmente conferido.

Por exemplo:

```text
10–20 cartas
```

com os textos corretos conhecidos.

Utilize esse conjunto para medir:

* reconhecimento do nome;
* reconhecimento das dicas;
* caracteres incorretos;
* palavras incorretas;
* erros em textos pequenos;
* erros em textos grandes;
* impacto do pré-processamento.

O objetivo inicial é determinar empiricamente:

```text
Qual é a taxa de acerto real?
```

antes de decidir se é necessário um modelo OCR mais sofisticado.

---

# Regra importante sobre IA

Não introduza LLM, visão generativa ou API externa apenas para corrigir problemas que possam ser resolvidos por:

* melhor fotografia;
* correção de perspectiva;
* aumento de resolução;
* processamento de imagem;
* configuração do OCR;
* segmentação;
* dicionário;
* validação;
* regras determinísticas.

Se, depois dos testes, algum problema continuar sendo difícil para OCR tradicional, documente o problema antes de propor IA.

A prioridade é:

```text
processamento de imagem
        ↓
OCR tradicional/local
        ↓
pós-processamento determinístico
        ↓
validação
        ↓
revisão humana
        ↓
somente então considerar IA
```

---

# Primeira entrega

Não tente implementar todo o sistema de uma vez.

A primeira entrega deverá ser uma **prova de conceito funcional** capaz de:

1. receber algumas imagens reais das cartas;
2. detectar/corrigir a carta quando possível;
3. realizar OCR;
4. separar nome e dicas quando possível;
5. produzir JSON;
6. salvar imagens intermediárias para diagnóstico;
7. apresentar confiança/alertas;
8. permitir comparar diferentes configurações de OCR.

Ao terminar essa primeira etapa, apresente:

* estrutura criada;
* dependências;
* como executar;
* exemplos de entrada;
* exemplos de saída;
* resultados obtidos;
* problemas encontrados;
* taxa de acerto observada;
* próximos problemas técnicos a resolver.

**Não avance para uma implementação complexa de câmera/interface antes de demonstrar que o OCR consegue produzir resultados aceitáveis nas imagens reais das cartas.**
