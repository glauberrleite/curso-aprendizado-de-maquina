"""
Jogo da velha aprendido por diferencas temporais (secao 08 da aula 01).

E o exemplo da secao 1.5 do Sutton & Barto, em Python: o agente joga de X,
mantem uma tabela V(s) sobre os estados que resultam das suas proprias jogadas
(os afterstates) e ajusta essa tabela com

    V(S_t) <- V(S_t) + alfa [ V(S_{t+1}) - V(S_t) ]

Nao ha modelo do oponente, nem busca em arvore, nem rotulo de jogada certa:
so o resultado das partidas.

Uma escolha de projeto explicita: valor terminal 1 para vitoria, 0.5 para
empate e 0 para derrota. O livro usa 0 tambem para o empate (contra um
adversario fraco, empatar e fracassar). Com 0.5 o agente continua tendo o que
aprender contra um oponente perfeito, com quem empatar e o melhor resultado
possivel. Mude a constante EMPATE e veja o comportamento mudar: e a definicao
do problema que muda, nao o algoritmo.

So precisa da biblioteca padrao (matplotlib apenas para a figura opcional).

Usar:
    python jogo_da_velha_td.py
    python jogo_da_velha_td.py --episodios 50000 --eps 0 --pericia 1.0
    python jogo_da_velha_td.py --figura
"""

import argparse
import random
from functools import lru_cache

LINHAS = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
          (0, 3, 6), (1, 4, 7), (2, 5, 8),
          (0, 4, 8), (2, 4, 6)]

VITORIA, EMPATE, DERROTA = 1.0, 0.5, 0.0

X, O, VAZIO = 1, 2, 0


def vencedor(tab):
    for a, b, c in LINHAS:
        if tab[a] != VAZIO and tab[a] == tab[b] == tab[c]:
            return tab[a]
    return VAZIO


def valor_terminal(tab):
    """Valor do estado do ponto de vista de X, ou None se a partida continua."""
    v = vencedor(tab)
    if v == X:
        return VITORIA
    if v == O:
        return DERROTA
    if VAZIO not in tab:
        return EMPATE
    return None


@lru_cache(maxsize=None)
def minimax(tab):
    """Resultado da partida com jogo perfeito dos dois lados: +1, 0 ou -1 (para X).

    De quem e a vez sai da contagem de pecas, entao o tabuleiro basta como chave.
    """
    v = vencedor(tab)
    if v == X:
        return 1
    if v == O:
        return -1
    if VAZIO not in tab:
        return 0

    vez = X if tab.count(X) == tab.count(O) else O
    resultados = []
    for i in range(9):
        if tab[i] == VAZIO:
            novo = tab[:i] + (vez,) + tab[i + 1:]
            resultados.append(minimax(novo))
    return max(resultados) if vez == X else min(resultados)


def jogada_o(tab, pericia, rng):
    """O oponente: joga otimo com probabilidade `pericia`, senao ao acaso."""
    livres = [i for i in range(9) if tab[i] == VAZIO]

    if rng.random() < pericia:
        melhor, avaliacoes = None, []
        for i in livres:
            avaliacoes.append((minimax(tab[:i] + (O,) + tab[i + 1:]), i))
        pior_para_x = min(v for v, _ in avaliacoes)          # O minimiza
        melhor = rng.choice([i for v, i in avaliacoes if v == pior_para_x])
        return melhor

    return rng.choice(livres)


def episodio(V, alfa, eps, pericia, rng, aprender_exploratorias=False):
    """Joga uma partida inteira e atualiza V. Devolve +1 vitoria, 0 empate, -1 derrota."""
    tab = (VAZIO,) * 9
    anterior = None

    while True:
        # ---- jogada do agente (X): escolhe entre os estados resultantes ----
        livres = [i for i in range(9) if tab[i] == VAZIO]
        explorou = rng.random() < eps

        if explorou:
            escolha = rng.choice(livres)
        else:
            melhor_valor, candidatos = -1.0, []
            for i in livres:
                depois = tab[:i] + (X,) + tab[i + 1:]
                terminal = valor_terminal(depois)
                valor = terminal if terminal is not None else V.setdefault(depois, 0.5)
                if valor > melhor_valor:
                    melhor_valor, candidatos = valor, [i]
                elif valor == melhor_valor:
                    candidatos.append(i)
            escolha = rng.choice(candidatos)

        tab = tab[:escolha] + (X,) + tab[escolha + 1:]
        V.setdefault(tab, 0.5)

        terminal = valor_terminal(tab)
        if terminal is not None:                      # X venceu ou empatou
            if anterior is not None:
                V[anterior] += alfa * (terminal - V[anterior])
            return 1 if terminal == VITORIA else 0

        # ---- a atualizacao temporal: puxa a estimativa anterior para a atual ----
        # So aprendemos com jogadas gulosas: uma jogada exploratoria nao diz nada
        # sobre o valor da politica que pretendemos seguir.
        if anterior is not None and (not explorou or aprender_exploratorias):
            V[anterior] += alfa * (V[tab] - V[anterior])
        anterior = tab

        # ---- jogada do oponente (O) ----
        i = jogada_o(tab, pericia, rng)
        tab = tab[:i] + (O,) + tab[i + 1:]

        terminal = valor_terminal(tab)
        if terminal is not None:                      # derrota ou empate
            V[anterior] += alfa * (terminal - V[anterior])
            return -1 if terminal == DERROTA else 0


def tabuleiro_de_aberturas(V):
    """V do tabuleiro que resulta de colocar o primeiro X em cada casa."""
    linhas = []
    for l in range(3):
        celulas = []
        for c in range(3):
            i = 3 * l + c
            tab = tuple(X if j == i else VAZIO for j in range(9))
            celulas.append(f"{V.get(tab, 0.5):.2f}")
        linhas.append("  ".join(celulas))
    return "\n".join("    " + s for s in linhas)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--episodios", type=int, default=30000)
    ap.add_argument("--alfa", type=float, default=0.1)
    ap.add_argument("--eps", type=float, default=0.1)
    ap.add_argument("--pericia", type=float, default=0.5,
                    help="probabilidade de o oponente jogar de forma otima")
    ap.add_argument("--aprender-exploratorias", action="store_true")
    ap.add_argument("--semente", type=int, default=20250817)
    ap.add_argument("--figura", action="store_true")
    args = ap.parse_args()

    rng = random.Random(args.semente)
    V = {}
    historico, janela = [], []

    for ep in range(1, args.episodios + 1):
        r = episodio(V, args.alfa, args.eps, args.pericia, rng,
                     args.aprender_exploratorias)
        janela.append(r)
        if len(janela) > 500:
            janela.pop(0)
        if ep % 100 == 0:
            vit = 100 * sum(1 for x in janela if x == 1) / len(janela)
            der = 100 * sum(1 for x in janela if x == -1) / len(janela)
            historico.append((ep, vit, der))

    ep, vit, der = historico[-1]
    print(f"episodios          : {ep}")
    print(f"pericia do oponente: {args.pericia:.0%}   alfa={args.alfa}  eps={args.eps}")
    print(f"ultimas 500 partidas: {vit:.1f}% vitorias, "
          f"{100 - vit - der:.1f}% empates, {der:.1f}% derrotas")
    print(f"estados na tabela  : {len(V)}")
    print("\nvalor de cada abertura (casas em 0.50 nunca foram experimentadas):")
    print(tabuleiro_de_aberturas(V))

    if args.figura:
        import matplotlib.pyplot as plt

        eps_x = [h[0] for h in historico]
        fig, ax = plt.subplots(figsize=(9, 4))
        ax.plot(eps_x, [h[1] for h in historico], lw=1.3, label="vitorias")
        ax.plot(eps_x, [h[2] for h in historico], lw=1.3, label="derrotas")
        ax.set_xlabel("partidas")
        ax.set_ylabel("% das ultimas 500")
        ax.set_ylim(0, 100)
        ax.legend(frameon=False)
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        fig.savefig("jogo_da_velha_td.png", dpi=150)
        print("\nfigura salva em jogo_da_velha_td.png")


if __name__ == "__main__":
    main()
