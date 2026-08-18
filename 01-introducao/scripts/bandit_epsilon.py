"""
Testbed de 10 bracos — exploracao x explotacao (secao 06 da aula 01).

Reproduz o experimento classico do Sutton & Barto (figura 2.2): 10 acoes,
cada uma com valor verdadeiro q*(a) ~ N(0, 1); a recompensa de escolher a e
sorteada de N(q*(a), 1). Compara politicas epsilon-gulosas com estimativa por
media amostral.

O ponto da figura: quem nunca explora (eps = 0) trava numa acao que pareceu boa
cedo; quem explora demais paga pedagio para sempre.

Requer numpy e matplotlib.

Usar:
    python bandit_epsilon.py
    python bandit_epsilon.py --execucoes 2000 --passos 1000
    python bandit_epsilon.py --eps 0 0.01 0.1 0.3 --sem-figura
"""

import argparse

import numpy as np


def experimento(eps, execucoes, passos, k, rng):
    """Devolve (recompensa media por passo, fracao de acoes otimas por passo)."""
    soma_rec = np.zeros(passos)
    soma_opt = np.zeros(passos)

    for _ in range(execucoes):
        q_estrela = rng.normal(0.0, 1.0, k)      # o problema desta execucao
        melhor = int(np.argmax(q_estrela))

        Q = np.zeros(k)                          # estimativas do agente
        N = np.zeros(k)                          # quantas vezes cada acao foi tentada

        for t in range(passos):
            if rng.random() < eps:
                a = rng.integers(k)              # explora
            else:
                # desempate aleatorio: sem isso o guloso puro fica preso na acao 0
                melhores = np.flatnonzero(Q == Q.max())
                a = int(rng.choice(melhores))

            r = rng.normal(q_estrela[a], 1.0)

            N[a] += 1
            Q[a] += (r - Q[a]) / N[a]            # media amostral incremental

            soma_rec[t] += r
            soma_opt[t] += (a == melhor)

    return soma_rec / execucoes, 100.0 * soma_opt / execucoes


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--eps", type=float, nargs="+", default=[0.0, 0.01, 0.1])
    ap.add_argument("--execucoes", type=int, default=1000)
    ap.add_argument("--passos", type=int, default=1000)
    ap.add_argument("--bracos", type=int, default=10)
    ap.add_argument("--semente", type=int, default=20250817)
    ap.add_argument("--sem-figura", action="store_true")
    args = ap.parse_args()

    print(f"{args.bracos} bracos · {args.execucoes} execucoes · {args.passos} passos")
    print()
    print(f"{'eps':>6} {'rec. media (ult. 100)':>24} {'% otima (ult. 100)':>20}")

    resultados = []
    for eps in args.eps:
        # mesma semente para todos: as politicas enfrentam os mesmos problemas
        rng = np.random.default_rng(args.semente)
        rec, opt = experimento(eps, args.execucoes, args.passos, args.bracos, rng)
        resultados.append((eps, rec, opt))
        print(f"{eps:>6.2f} {rec[-100:].mean():>24.3f} {opt[-100:].mean():>19.1f}%")

    if args.sem_figura:
        return

    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
    for eps, rec, opt in resultados:
        rotulo = f"eps = {eps:g}" + (" (guloso)" if eps == 0 else "")
        ax1.plot(rec, lw=1.2, label=rotulo)
        ax2.plot(opt, lw=1.2, label=rotulo)

    ax1.set_ylabel("recompensa media")
    ax1.legend(frameon=False)
    ax2.set_ylabel("% de acoes otimas")
    ax2.set_xlabel("passos")
    ax2.set_ylim(0, 100)
    for ax in (ax1, ax2):
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Testbed de 10 bracos — epsilon-guloso com media amostral")
    fig.tight_layout()
    fig.savefig("bandit_epsilon.png", dpi=150)
    print("\nfigura salva em bandit_epsilon.png")


if __name__ == "__main__":
    main()
