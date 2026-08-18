"""
Primeiro contato com o Gymnasium — Atividade 1 da aula 01.

Abre um ambiente, imprime a estrutura do problema (o que e o estado, o que sao
as acoes, quando o episodio acaba) e roda uma politica aleatoria por alguns
episodios para servir de linha de base.

Nao ha aprendizado nenhum aqui: o objetivo e enxergar o laco
    estado -> acao -> (recompensa, proximo estado)
com as suas proprias maos antes de escrever qualquer algoritmo.

Instalar (uma vez):
    pip install "gymnasium[classic-control]"

Usar:
    python gymnasium_primeiro_contato.py
    python gymnasium_primeiro_contato.py --env MountainCar-v0 --episodios 20
    python gymnasium_primeiro_contato.py --render          # abre a janela
"""

import argparse
import statistics

import gymnasium as gym


def descrever(env, nome):
    """Imprime a ficha do ambiente: S, A e o significado da recompensa."""
    print("=" * 68)
    print(f"Ambiente: {nome}")
    print("=" * 68)
    print(f"  espaco de observacao (S) : {env.observation_space}")
    print(f"  espaco de acao (A)       : {env.action_space}")

    # Discrete tem .n; Box tem .shape, .low e .high
    if hasattr(env.action_space, "n"):
        print(f"  |A| = {env.action_space.n} acoes discretas")
    else:
        print(f"  acoes continuas com forma {env.action_space.shape}")

    limite = env.spec.max_episode_steps if env.spec else None
    print(f"  limite de passos por episodio: {limite}")
    print()


def rodar(env, episodios, semente):
    """Politica aleatoria. Devolve os retornos (soma das recompensas) por episodio."""
    retornos, duracoes = [], []

    for ep in range(episodios):
        estado, info = env.reset(seed=semente + ep)
        G = 0.0
        t = 0

        while True:
            acao = env.action_space.sample()          # a politica: sortear
            estado, recompensa, terminou, truncou, info = env.step(acao)

            # ATENCAO a convencao: a recompensa que volta aqui e R_{t+1},
            # a consequencia da acao A_t que acabamos de enviar.
            G += recompensa
            t += 1

            if ep == 0 and t <= 5:
                print(f"    t={t - 1:>2}  A_t={acao}  ->  R_{t}={recompensa:+.1f}  S_{t}={estado}")

            # terminou: o episodio acabou pelas regras do ambiente (estado terminal)
            # truncou : acabou por limite de tempo, o que NAO e a mesma coisa
            if terminou or truncou:
                break

        retornos.append(G)
        duracoes.append(t)

    return retornos, duracoes


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--env", default="CartPole-v1", help="id do ambiente Gymnasium")
    ap.add_argument("--episodios", type=int, default=30)
    ap.add_argument("--semente", type=int, default=0)
    ap.add_argument("--render", action="store_true", help="abre a janela do ambiente")
    args = ap.parse_args()

    env = gym.make(args.env, render_mode="human" if args.render else None)
    descrever(env, args.env)

    print("  primeiros passos do episodio 1:")
    retornos, duracoes = rodar(env, args.episodios, args.semente)
    env.close()

    print()
    print(f"  {args.episodios} episodios com politica aleatoria")
    print(f"    retorno medio  : {statistics.mean(retornos):8.2f}")
    if len(retornos) > 1:
        print(f"    desvio padrao  : {statistics.stdev(retornos):8.2f}")
    print(f"    melhor / pior  : {max(retornos):8.2f} / {min(retornos):8.2f}")
    print(f"    duracao media  : {statistics.mean(duracoes):8.2f} passos")
    print()
    print("  Para entregar, responda: o que e S? o que e A? qual e o sinal de")
    print("  recompensa? o que encerra um episodio? a tarefa e episodica ou continua?")


if __name__ == "__main__":
    main()
