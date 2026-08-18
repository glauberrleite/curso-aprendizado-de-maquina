# Motivação

Uma criança brincando não precisa de um professor: tem uma conexão sensório-motora com o ambiente.
- A exploração produz informação sobre causa e efeito;
- Consequências dos atos;
- **O que fazer** para **alcançar objetivos**.

Enquanto aprendemos (como humanos) estamos perceptivos a como o ambiente responde ao que fazemos e, com isso, tentamos influenciar o que acontece de acordo com nosso comportamento.

Vamos focar em uma abordagem computacional de aprendizado através da interação. Não há um professor que diz o que é certo ou errado (aprendizado supervisionado) e não há, obrigatoriamente, interesse em descobrimento de padrões (aprendizado não supervisionado).

> (Lapan) RL is the third camp and lies somewhere in between full supervision and a complete lack of predefined labels. On the one hand, it uses many well-established methods of supervised learning, such as deep neural networks for function approximation, stochastic gradient descent, and backpropagation, to learn data representation. On the other hand, it usually applies them in a different way.

A distinção precisa é o **tipo de retorno** que recebemos:
- Aprendizado supervisionado dá um feedback **instrutivo**: diz qual era a ação correta, independentemente da que foi tomada.
- Aprendizado por reforço dá um feedback **avaliativo**: diz apenas quão boa foi a ação tomada, e nada sobre as demais.

É essa diferença que cria o problema de exploração mais adiante.

Vamos extrapolar a modelagem clássica da IA na qual agentes, dotados de sensores e atuadores, interagem com o ambiente.
Nossa abordagem computacional é um aprendizado orientado a objetivo aprendendo da interação. Precisamos de um novo sinal, além das observações.

![agent](./media/agent.png)

# Uma definição formal

> Definição (Sutton): Reinforcement learning is learning what to do so as to maximize a numerical reward signal.

O que fazer: como mapear situações para ações
- situações: estado do mundo modelado, $s \in \mathcal{S}$
- ações: de um conjunto de ações possíveis naquele estado, $a \in \mathcal{A}(s)$
- mapa: pode ser função, tabela, rede neural — uma **política**, que leva de $\mathcal{S}$ para $\mathcal{A}$:

$$ \pi (s) = a $$

Essa é a forma **determinística**. O caso geral é uma política **estocástica**, uma distribuição de probabilidade sobre as ações:

$$ \pi (a \mid s) = \Pr\{A_t = a \mid S_t = s\} $$

💡Em teoria de controle é comum escrever $x \in \mathcal{X}$ para o estado e $u$ para o controle. É a mesma coisa: $x \equiv s$ e $u \equiv a$. Aqui seguimos a notação do Sutton & Barto (2018), que é a do livro-texto.

## O laço, com índices

O tempo é discreto, $t = 0, 1, 2, \dots$ A cada passo, o agente observa o estado, escolhe uma ação, e o ambiente responde com um novo estado e uma recompensa:

$$ S_0, A_0, R_1, S_1, A_1, R_2, S_2, A_2, R_3, \dots $$

⚠️ A recompensa que **resulta** da ação $A_t$ é $R_{t+1}$, e não $R_t$. O índice marca quando o número chegou ao agente, junto com $S_{t+1}$ — os dois vêm do ambiente no mesmo instante. Parte da literatura mais antiga usa $R_t$; nós seguimos o livro-texto.

A aplicação da ação $a$ altera o estado do ambiente e, com isso, produz um sinal de recompensa $r \in \mathbb{R}$. No caso geral tanto a recompensa quanto o próximo estado são **aleatórios**: o ambiente sorteia $(S_{t+1}, R_{t+1})$ a partir de $(S_t, A_t)$. Formalizamos isso como $p(s', r \mid s, a)$ na aula sobre processos de decisão de Markov.

## Onde fica a fronteira entre agente e ambiente

Não é a fronteira física. A regra é: **tudo o que o agente não controla arbitrariamente faz parte do ambiente**. Motores, bateria e o próprio corpo de um robô costumam ficar do lado do ambiente; o agente é o processo de decisão.

💡O agente pode conhecer o ambiente por completo e ainda ter uma tarefa difícil — conhecer as regras do cubo mágico não é saber resolvê-lo.

# Recompensa não é valor

Este é o ponto que mais gera confusão, e vale separar com cuidado.

**Hipótese da recompensa**: tudo o que entendemos por objetivo pode ser bem representado como a maximização do valor esperado da soma acumulada de um sinal escalar de recompensa. É uma hipótese, não um teorema — e aceitá-la é o que define o campo.

O que se maximiza não é a recompensa imediata, é o **retorno**:

$$ G_t = R_{t+1} + \gamma R_{t+2} + \gamma^2 R_{t+3} + \cdots = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1} $$

com a taxa de desconto $0 \le \gamma \le 1$:
- $\gamma = 0$: agente míope, só enxerga o próximo passo;
- $\gamma \to 1$: agente previdente;
- $\gamma < 1$ é também o que garante que a soma converge em tarefas que nunca terminam (**contínuas**). Em tarefas **episódicas**, que terminam sozinhas, $\gamma = 1$ é permitido.

As **funções de valor** são esperanças do retorno:

$$ v_\pi(s) = \mathbb{E}_\pi[G_t \mid S_t = s] \qquad q_\pi(s,a) = \mathbb{E}_\pi[G_t \mid S_t = s, A_t = a] $$

E é de $q$ que sai a política gulosa:

$$ \pi(s) = \arg \max_{a \in \mathcal{A}(s)} q(s,a) $$

⚠️ Recompensa e valor são coisas diferentes:

| | vem de | horizonte | precisa ser aprendido? |
|---|---|---|---|
| recompensa $r$, $R_t$ | **ambiente** | imediato | não |
| valor $v$, $q$ | **agente** (estima) | futuro esperado | **sim** |

O valor é que é uma estimativa, porque não conhecemos o futuro. A recompensa não é estimada: ela chega pronta.

⚠️ Também não confunda os dois valores: $v$ é função só do estado, $q$ é função do par estado–ação. Escrever $v(s,a)$ é sintoma de que algo se embaralhou.

💡Ações podem não afetar apenas a recompensa imediata, mas também a próxima situação (e as recompensas subsequentes) ou apresentar um atraso na recompensa (_delayed reward_). É exatamente por isso que precisamos de valor, e não só de recompensa.

# A natureza do aprendizado por reforço

💡A dimensão $t$ às vezes não é considerada explicitamente em outros problemas de aprendizado de máquina. No aprendizado por reforço ela faz parte da própria natureza do problema.

- Em comparação a aprendizado supervisionado: deve trabalhar em torno da própria experiência — e a distribuição dos dados **muda** quando a política muda.
- Em comparação a aprendizado não supervisionado: maximizar uma recompensa pode não ser necessariamente encontrar uma estrutura desconhecida.

- **Explotação** (_exploitation_): preferir ações **passadas** efetivas, em cima da recompensa estimada.
- **Exploração** (_exploration_): descobrir novas ações.

O conflito entre os dois é permanente e não existe solução universal. Como o ambiente costuma ser estocástico, uma única tentativa não estabelece o valor de uma ação: cada ação precisa ser tentada várias vezes para que a estimativa fique confiável.

# Explorando melhor os elementos de RL

- **Política**: A **policy** defines the learning agent’s way of behaving at a given time. Roughly speaking, a policy is a mapping from perceived states of the environment to actions to be taken when in those states.
- **Sinal de recompensa**: A **reward signal** defines the goal in a reinforcement learning problem. On each time step, the environment sends to the reinforcement learning agent a single number, a reward.
- **Função valor**: a value function specifies what is good in the long run. Roughly speaking, the value of a state is the total amount of reward an agent can expect to accumulate over the future, starting from that state.
- **Modelo do ambiente** (opcional): A **model of the environment** is something that mimics the behavior of the environment, or more generally, that allows inferences to be made about how the environment will behave.
  - Modelo muito limitado vs modelo muito detalhado
  - Conceito _cheap simulation_
  - Com modelo dá para **planejar** (_model-based_: programação dinâmica, Dyna, MCTS); sem modelo, resta aprender por tentativa e erro (_model-free_: Q-learning, SARSA, DQN, PPO).

⚠️ Métodos **evolutivos** (algoritmos genéticos, _simulated annealing_) também maximizam recompensa, mas não são aprendizado por reforço no sentido desta disciplina: eles avaliam políticas inteiras e ignoram quais estados foram visitados e quais ações foram tomadas dentro de cada episódio — justamente a informação que as funções de valor aproveitam.

# Exemplo: jogo da velha

O exemplo da seção 1.5 do Sutton & Barto, contra um oponente **imperfeito** (não queremos empatar sempre, queremos explorar as falhas dele):

- **Estado**: o tabuleiro depois da nossa jogada (o _afterstate_).
- **Tabela de valores**: $V(s)$ estimando a probabilidade de vencer a partir dali.
- **Valores terminais**: 1 na vitória, 0 na derrota. Para o empate, o livro usa 0 (contra um adversário fraco, empatar é fracassar); nas demos desta aula usamos 0,5, para que o agente ainda tenha o que aprender contra um oponente perfeito. Todos os demais estados começam em 0,5.
- **Política**: quase sempre gulosa; de vez em quando, uma jogada exploratória.
- **Aprendizado** por diferenças temporais:

$$ V(S_t) \leftarrow V(S_t) + \alpha \left[ V(S_{t+1}) - V(S_t) \right] $$

Note que não esperamos o fim da partida para aprender: cada jogada corrige a estimativa da anterior. Minimax não serviria (assume adversário perfeito e joga para o empate) e programação dinâmica exigiria conhecer o modelo do oponente, que não temos.

O exemplo já contém quase tudo: interação, objetivo claro, consequências atrasadas, ausência de modelo do adversário e melhora contínua durante o uso. O que ele esconde é a escala: são $3^9 = 19\,683$ configurações, que cabem numa tabela. O gamão tem $10^{20}$ e o Go, $10^{170}$ — daí a necessidade de aproximação de função na segunda metade do curso.

# Limites e dificuldades

- **Estado ≠ observação**: a teoria supõe que $S_t$ resume tudo o que importa do passado (propriedade de Markov). Na prática recebemos observações parciais.
- **Atribuição de crédito**: a recompensa chega tarde e não diz qual ação foi a responsável.
- **Fome de dados**: milhões de interações para tarefas que um humano entende em minutos.
- **Dimensionalidade**: tabelas acabam; com aproximação perdemos as garantias de convergência do caso tabular.
- **Especificar a recompensa**: o agente otimiza exatamente o que foi escrito, inclusive atalhos não previstos (_reward hacking_).

# Atividade - Preparação de ambiente

Originalmente, muitas APIs eram baseadas na *OpenAI Gym library*, que não é mais mantida. A lib [Gymnasium](https://gymnasium.farama.org/index.html) é um _fork_ mantido pela Farama Foundation.
- Rode em seu computador (e tente entender a ideia) a parte "Basic Usage" e "Training an Agent".
- O livro do Lapan (2º capítulo) fornece uma instrução direcionada.
- Há um roteiro pronto em [`scripts/gymnasium_primeiro_contato.py`](./scripts/gymnasium_primeiro_contato.py).
- Para entregar: para o ambiente escolhido, identifique $\mathcal{S}$, $\mathcal{A}$, o sinal de recompensa, o que encerra um episódio, e se a tarefa é episódica ou contínua.
- Procure outras opções de tecnologias que auxiliem RL como [Reinforcement Learning Toolbox (MATLAB)](https://www.mathworks.com/products/reinforcement-learning.html), [Genesis AI](https://genesis-world.readthedocs.io/en/latest/) e [NVidia Isaac Lab](https://developer.nvidia.com/isaac/lab).

---

Material de apoio desta aula: [slides interativos](./aula.html) · [guia de condução](./guia-aula.md) · [scripts](./scripts/)
