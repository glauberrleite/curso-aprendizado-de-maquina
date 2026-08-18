# Scripts — Aula 01 · Introdução

Quatro scripts independentes. Os três primeiros só precisam de Python; o último
precisa do Manim.

| Script | Para quê | Requisitos |
|---|---|---|
| [`gymnasium_primeiro_contato.py`](./gymnasium_primeiro_contato.py) | Atividade 1: abrir um ambiente e ver o laço rodando | `gymnasium` |
| [`bandit_epsilon.py`](./bandit_epsilon.py) | Exploração × explotação (§ 06), figura 2.2 do Sutton | `numpy`, `matplotlib` |
| [`jogo_da_velha_td.py`](./jogo_da_velha_td.py) | O agente TD do § 08, em Python | biblioteca padrão |
| [`rl_manim.py`](./rl_manim.py) | Animações para projetar | `manim` |

## 1. Primeiro contato com o Gymnasium

```bash
pip install "gymnasium[classic-control]"
python gymnasium_primeiro_contato.py
```

Imprime a ficha do ambiente — espaço de observação, espaço de ação, limite de
passos — e roda uma política aleatória, mostrando os primeiros passos com a
convenção de índices explícita (`A_t` produz `R_{t+1}` e `S_{t+1}`).

```bash
python gymnasium_primeiro_contato.py --env MountainCar-v0 --episodios 20
python gymnasium_primeiro_contato.py --render          # abre a janela
```

O retorno médio da política aleatória é a **linha de base**: qualquer agente que
você escrever na disciplina precisa bater esse número.

## 2. Testbed de 10 braços

```bash
pip install numpy matplotlib
python bandit_epsilon.py
python bandit_epsilon.py --eps 0 0.01 0.1 0.3 --execucoes 2000
python bandit_epsilon.py --sem-figura                   # só os números
```

Dez ações com valores verdadeiros $q_*(a) \sim N(0,1)$ e recompensas ruidosas.
Compara políticas ε-gulosas com estimativa por média amostral e salva
`bandit_epsilon.png` com as duas curvas clássicas (recompensa média e % de ação
ótima).

O que esperar em 1000 passos: ε = 0 estaciona perto de 1,0; ε = 0,1 chega perto
de 1,4; ε = 0,01 ainda está subindo e passa à frente se o experimento continuar.

## 3. Jogo da velha por diferenças temporais

```bash
python jogo_da_velha_td.py
python jogo_da_velha_td.py --episodios 50000 --figura
python jogo_da_velha_td.py --eps 0                      # sem exploração
python jogo_da_velha_td.py --pericia 1.0                # oponente perfeito
```

É a mesma coisa que a demo interativa do § 08 da aula, em Python e sem
dependências. O oponente joga de forma ótima (minimax memorizado) com a
probabilidade dada por `--pericia` e ao acaso no restante das vezes.

Três resultados que vale a pena reproduzir:

| Configuração | Vitórias | Empates | Derrotas |
|---|---:|---:|---:|
| padrão (`--pericia 0.5 --eps 0.1`) | ~74% | ~20% | ~6% |
| sem exploração (`--eps 0`) | ~72% | ~28% | ~0% |
| oponente perfeito (`--pericia 1.0`) | 0% | ~92% | ~8% |

Repare no **tabuleiro de aberturas** que o script imprime no fim: com `--eps 0`,
oito das nove casas continuam em `0.50` — nunca foram experimentadas. É a
exploração que compra esse conhecimento. Com `--pericia 1.0` todas convergem
para `0.50` por outro motivo: contra jogo perfeito, todas empatam.

## 4. Animações (Manim)

```bash
brew install cairo pango pkg-config ffmpeg     # macOS
pip install manim
manim -pqm rl_manim.py LacoAgenteAmbiente
manim -pqm rl_manim.py RecompensaVersusValor
```

- `LacoAgenteAmbiente` — o laço fechado, com a trajetória `S0 A0 R1 S1 …` se
  escrevendo passo a passo. Serve para fixar por que a recompensa da ação
  $A_t$ é indexada $R_{t+1}$.
- `RecompensaVersusValor` — o corredor do § 05 com o desconto γ variando, até a
  troca de preferência em γ = (1/10)^(1/(n−1)).

Não precisa de LaTeX: as cenas usam apenas `Text`.
