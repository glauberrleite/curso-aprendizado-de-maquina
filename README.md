# PPGI071 - Aprendizado por Reforço
Repositório de conteúdos para a disciplina de Aprendizado por Reforço, oferecida no Instituto de Computação da Universidade Federal de Alagoas.

🌐 **Página da disciplina:** https://glauberrleite.github.io/curso-aprendizado-por-reforco/

👨‍🏫 Professor [Glauber Rodrigues Leite](https://glauberrleite.com/)

## 🎯 Objetivo da disciplina
Compreender a base formal e prática de algoritmos de aprendizado de máquina baseados na interação explícita com o ambiente.

## 📋 Ementa
- Introdução ao Aprendizado por Reforço
- Problema Multi-armed Bandits
- Processos de decisão de Markov
- Métodos de Monte Carlo
- Aprendizado por Diferenças Temporais
- Bootstrapping n-passos
- Planejamento e Aprendizado com Métodos Tabulares 
- Predição e Controle on-policy com Aproximação
- Métodos Off-Policy com Aproximação
- Traços de Elegibilidade
- Métodos de Gradiente de Política
- Aprendizado por Reforço Profundo

## 📚 Bibliografia
- **SUTTON, R. S.; BARTO, A. G.** _Reinforcement Learning: An Introduction_. 2 ed. MIT Press. 2018.  [Link](https://www.amazon.com.br/Reinforcement-Learning-Introduction-Richard-Sutton/dp/0262039249)
- **LAPAN, M.** _Deep Reinforcement Learning Hands-on: A Practical and Easy-to-follow Guide to RL from Q-learning and DQNs to PPO and RLHF_. Packt Publishing Ltd, 2024. [Link](https://www.amazon.com.br/Reinforcement-Learning-Hands-easy-follow/dp/1835882706)
- (Complementar) Reinforcement Learning Toolbox - MATLAB. [Link](https://www.mathworks.com/products/reinforcement-learning.html)

## 📝 Avaliação
- $P_1$ - Projeto 1: 0 a 10
- $P_2$ - Projeto 2: 0 a 10

$$AV = \frac{P_1 + P_2}{2}$$

## Abreviações

- ML: Machine Learning (Aprendizado de máquina)
- RL: Reinforcement Learning (Aprendizado por reforço)

## 🔤 Glossário e notação

Notação do Sutton & Barto (2018), usada na disciplina inteira. Em teoria de controle é comum $x \equiv s$ (estado) e $u \equiv a$ (ação).

| Símbolo | Nome | Quem produz | O que é |
|---|---|---|---|
| $t$ | passo de tempo | — | o tempo é discreto: $t = 0, 1, 2, \dots$ |
| $S_t \in \mathcal{S}$ | estado | ambiente | o que o agente sabe no instante $t$ |
| $A_t \in \mathcal{A}(s)$ | ação | **agente** | a única coisa que o agente controla |
| $R_{t+1} \in \mathbb{R}$ | recompensa | ambiente | avaliação imediata, escalar |
| $G_t$ | retorno | — | soma descontada das recompensas futuras |
| $\pi(a \mid s)$ | política | agente | como escolher a ação |
| $v_\pi(s)$ | valor do estado | agente (estima) | retorno esperado a partir de $s$ |
| $q_\pi(s,a)$ | valor da ação | agente (estima) | retorno esperado fixando a primeira ação |
| $\gamma \in [0,1]$ | desconto | projetista | quanto o futuro pesa |

⚠️ A recompensa que resulta da ação $A_t$ é $R_{t+1}$, e não $R_t$: o índice marca quando o número chegou ao agente, junto com $S_{t+1}$.

### Termos

- **Agente** — o processo de decisão. Controla apenas as ações.
- **Ambiente** — tudo o que o agente não controla arbitrariamente (inclusive os motores e o corpo de um robô).
- **Trajetória** — a sequência $S_0, A_0, R_1, S_1, A_1, R_2, \dots$
- **Feedback avaliativo** — diz quão boa foi a ação tomada, e nada sobre as demais (RL). Oposto de **feedback instrutivo**, que diz qual era a ação correta (aprendizado supervisionado).
- **Explotação** (_exploitation_) — escolher a ação de maior valor estimado. **Exploração** (_exploration_) — escolher outra, para melhorar as estimativas. O conflito entre as duas é permanente.
- **Consequência atrasada** (_delayed reward_) — uma ação afeta não só a recompensa imediata, mas os estados e as recompensas seguintes.
- **Recompensa ≠ valor** — a recompensa vem do ambiente e é imediata; o valor é uma previsão do agente sobre o futuro. Decidimos sobre o valor.
- **Tarefa episódica × contínua** — se a interação se quebra em episódios, $\gamma = 1$ é permitido; se nunca termina, é preciso $\gamma < 1$ para o retorno convergir.

## 📖 Aulas
| # | Aula | Material |
|---|------|----------|
| 01 | Introdução ao aprendizado por reforço | [notas](./01-introducao/README.md) · [slides](https://glauberrleite.github.io/curso-aprendizado-de-maquina/01-introducao/aula.html) · [guia](./01-introducao/guia-aula.md) · [scripts](./01-introducao/scripts/) |
