# VADER-UMPT
Vader-UMPT é uma ferramenta para análise de sentimento em português do Brasil. Utiliza o [LeIA](https://github.com/rafjaa/LeIA) que, por sua vez, se baseia na ferramenta [VADER](https://github.com/brunneis/vader-multi).

## Desenvolvimento
O código por trás deste projeto foi inicialmente baseado na biblioteca [LeIA](https://github.com/rafjaa/LeIA), uma adaptação do VADER para português do Brasil. Foram desenvolvidas duas ferramentas que permitem explorar a utilização desta biblioteca, sendo elas um ambiente web (desenvolvido com o Streamlit) e uma interface de linha de comandos.

Sendo que o objetivo da ferramenta é permitir explorar o funcionamento interno do algoritmo VADER, o código da biblioteca foi modificado para devolver, para além das pontuações, uma explicação passo-a-passo de como foi obtido o resultado final. No entanto, ao explorar melhor os resultados, foram descobertos alguns problemas na biblioteca, que tentámos resolver:

1. **O algoritmo ignora qualquer conjunção disjuntiva para além de "mas"** - Foi resolvido iterando por várias conjunções para confirmar se uma foi usada
2. **Adjetivos no sexo feminino são ignorados** - O dicionário original apenas inclui adjetivos no sexo masculino. Isto foi resolvido lematizando as palavras com o spaCy antes de as processar mais, uniformizando-as todas de uma forma que funciona com os dicionários existentes.
3. **Emojis são ignorados** - Apesar de conter código especial para converter emojis numa descrição textual, o código que removia acentos antes da análise estava simplesmente a remover todos os caracteres não ASCII, removendo também os emojis antes de estes terem uma oportunidade para serem processados. Isto foi resolvido alterando o código para filtrar apenas acentos.

Algumas destas soluções foram contribuídas de volta ao projeto original.

### Funcionamento do algoritmo
Com o explorador completo, podemos então ver em mais detalhe como funciona o algoritmo. Vamos utilizar a frase "Gosto do filme! ❤️".

1. **Lematizar o texto**: "Gosto de o filme ! ❤️"
2. **Remover acentos**: "Gosto de o filme ! ❤️"
3. **Emojis para texto**: "Gosto de o filme ! coração vermelho"
4. **Análise de sentimento por palavra**: "Gosto (1.7) de (0) o (0) filme (0) ! (0) coração (0) vermelho (0)"
5. **Somar pontuações**: 1.7
6. **Amplificar pontuação**: +0.292 pontos por conter um ponto de exclamação
7. **Normalizar soma**: 0.4574

O resultado final dá-nos uma pontuação composta de 0.4574, uma positiva de 0.333, uma neutra de 0.667 e uma negativa de 0.

### Melhorias
Como podemos ver, o algoritmo não é perfeito. No entanto, este explorador permite-nos mais facilmente descobrir o porquê.

Neste caso, seria provavelmente ideal arranjar uma forma melhor de lidar com emojis, provavelmente adicionando-os diretamente ao dicionário em vez de o converter em palavras (que muitas vezes não conseguem traduzir verdadeiramente o sentimento por trás do emoji). No entanto, tendo em conta o número elevado de emojis, tal está fora do alcance deste projeto.

Para além disso, é desejável criar também um dicionário para português de portugal, mas novamente tendo em conta o número elevado de palavras a ter em conta, e a metodologia utilizada para as pontuar (uma sondagem extensa envolvendo várias pessoas), também estava fora do alcance deste projeto.

## Instalação
```sh
$ pip install --user vader_umpt
```

### Ambiente de desenvolvimento
Para desenvolvimento, utilizamos o `poetry`. Depois de clonado o repositório, podemos ativar o _virtual environment_:

```sh
$ poetry install # instala todos os pacotes
$ poetry shell
```

Alternativamente, podemos utilizar o _venv_:

```sh
$ python -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Utilização

Abaixo são apresentadas todas as possíveis utilizações deste programa, obtidas através de `vader-umpt --help`.

```
usage: VADER-UMPT [-h] [--export-dicts] [-l LEXICON] [--emoji-lexicon EMOJI_LEXICON] [-e] [-w]

options:
  -h, --help            show this help message and exit
  --export-dicts        Exporta os dicionários
  -l LEXICON, --lexicon LEXICON
                        Ficheiro com o dicionário a ser utilizado
  --emoji-lexicon EMOJI_LEXICON
                        Ficheiro com o dicionário de emojis a ser utilizado
  -e, --explain         Imprimir explicação detalhada sobre como a pontuação foi calculada
  -w, --web             Executar um playground web para testar o analisador
```
### Playground Web
```sh
vader-umpt -w
```
Este comando irá executar o *playground web*, isto é, uma interface a partir do qual poderá fornecer texto e obter uma análise de sentimento detalhada. Este comando devolve um IP que pode ser utilizado para aceder à página através do *browser*.
Seguem-se alguns exemplos de utilização da *interface*, sendo apenas mostrada a parte inicial da página:

![Exemplo Playground](pics/muito_feio.png)
![Exemplo Playground](pics/gostei_muito.png)

### Explicação de Resultados
Uma outra utilização do programa passa por ler do *standard input* e devolver uma explicação detalhada da análise de sentimento.
```sh
./vader-umpt -e
Esta visita foi extremamente desagradável
{"neg": 0.438, "neu": 0.562, "pos": 0.0, "compound": -0.5984, "explanation": [["Lemmatize text", "este visita ser extremamente desagradável ."], ["Remove accents", "este visita ser extremamente desagradavel ."], ["Emojis to text", "este visita ser extremamente desagradavel ."], ["Sentiments", [["este", 0]]], ["Sentiments", [["este", 0], ["visita", 0]]], ["Sentiments", [["este", 0], ["visita", 0], ["ser", 0]]], ["Sentiments", [["este", 0], ["visita", 0], ["ser", 0], ["extremamente", 0], ["desagradavel", -2.8930000000000002]]], ["Sentiments", [["este", 0], ["visita", 0], ["ser", 0], ["extremamente", 0], ["desagradavel", -2.8930000000000002], [".", 0]]], ["Sentiments", [["este", 0], ["visita", 0], ["ser", 0], ["extremamente", 0], ["desagradavel", -2.8930000000000002], [".", 0]]], ["Sentiments after but check", [["este", 0], ["visita", 0], ["ser", 0], ["extremamente", 0], ["desagradavel", -2.8930000000000002], [".", 0]]], ["Sum", -2.8930000000000002], ["Punctuation amplifier", "Exclamation: 0.0, Question: 0, Total: 0.0"], ["Normalized sum", -0.5984449372171403]]}
A comida estava horrível
{"neg": 0.552, "neu": 0.448, "pos": 0.0, "compound": -0.5719, "explanation": [["Lemmatize text", "o comida estar horrível"], ["Remove accents", "o comida estar horrivel"], ["Emojis to text", "o comida estar horrivel"], ["Sentiments", [["o", 0]]], ["Sentiments", [["o", 0], ["comida", 0]]], ["Sentiments", [["o", 0], ["comida", 0], ["estar", 0]]], ["Sentiments", [["o", 0], ["comida", 0], ["estar", 0], ["horrivel", -2.7]]], ["Sentiments", [["o", 0], ["comida", 0], ["estar", 0], ["horrivel", -2.7]]], ["Sentiments after but check", [["o", 0], ["comida", 0], ["estar", 0], ["horrivel", -2.7]]], ["Sum", -2.7], ["Punctuation amplifier", "Exclamation: 0.0, Question: 0, Total: 0.0"], ["Normalized sum", -0.5718850320700721]]}
```

### Exportação de Dicionários
É possível imprimir os dicionários em formato *JSON* no *standard output* e, consequentemente, redirecioná-los para um ficheiro.
```sh
vader-umpt --export-dicts > dicionario.json
```

### Especificação de Dicionários
Especificação de dicionário a ser utilizado
```sh
vader-umpt --lexicon lexicon.json
```
Especificação de dicionário de *emojis* a ser utilizado
```sh
vader-umpt --emoji-lexicon emojis.json
```

## Autores
Trabalho realizado por Alexandre Flores, Matilde Bravo e Pedro Alves.
