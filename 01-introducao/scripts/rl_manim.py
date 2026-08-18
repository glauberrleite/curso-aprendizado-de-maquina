"""
Animacoes da aula 01 — aprendizado por reforco, com Manim (Community Edition).

Duas cenas, pensadas para projetar em aula:

  LacoAgenteAmbiente  o laco fechado agente -> acao -> ambiente -> (estado,
                      recompensa) -> agente, com a trajetoria S0 A0 R1 S1 ...
                      se escrevendo embaixo. Serve para fixar a convencao de
                      indices: a recompensa da acao A_t chega como R_{t+1}.

  RecompensaVersusValor  o corredor da secao 05: um passo a esquerda paga +1
                      agora; n passos a direita pagam +10 depois. Varre o
                      desconto gama e mostra a troca de preferencia no ponto
                      gama = (1/10)^(1/(n-1)).

Instalar o manim (uma vez):
    pip install manim
    # dependencias de sistema (macOS/Homebrew): brew install cairo pango pkg-config ffmpeg
    # Este script usa apenas Text (sem MathTex), entao NAO precisa de LaTeX.

Renderizar (-p abre o video ao final; qm = qualidade media):
    manim -pqm rl_manim.py LacoAgenteAmbiente
    manim -pqm rl_manim.py RecompensaVersusValor
"""

from manim import (
    ORIGIN, UP, DOWN, LEFT, RIGHT, PI,
    BLUE, TEAL, YELLOW, GREY, WHITE, RED,
    Scene, VGroup, Rectangle, Square, Text, Dot, CurvedArrow, Line,
    ValueTracker, DecimalNumber, always_redraw,
    Create, Write, FadeIn, MoveAlongPath,
)

COR_AGENTE = BLUE          # agente, acao, politica
COR_AMBIENTE = TEAL        # ambiente, estado
COR_RECOMPENSA = YELLOW    # recompensa, retorno, valor


def caixa(rotulo, cor, largura=3.0, altura=1.2):
    ret = Rectangle(width=largura, height=altura, color=cor, stroke_width=2.5)
    txt = Text(rotulo, font_size=30, color=cor)
    return VGroup(ret, txt)


class LacoAgenteAmbiente(Scene):
    """O laco fechado, um passo de tempo por vez."""

    N_PASSOS = 4

    def construct(self):
        agente = caixa("agente", COR_AGENTE).shift(4.2 * LEFT + 1.2 * UP)
        ambiente = caixa("ambiente", COR_AMBIENTE).shift(4.2 * RIGHT + 1.2 * UP)

        ida = CurvedArrow(
            agente[0].get_right() + 0.05 * RIGHT,
            ambiente[0].get_left() + 0.05 * LEFT,
            angle=-PI / 3, color=COR_AGENTE, stroke_width=3,
        )
        volta = CurvedArrow(
            ambiente[0].get_left() + 0.05 * LEFT,
            agente[0].get_right() + 0.05 * RIGHT,
            angle=-PI / 3, color=COR_AMBIENTE, stroke_width=3,
        )

        rot_ida = Text("ação  A t", font_size=24, color=COR_AGENTE)
        rot_ida.next_to(ida, UP, buff=0.15)
        rot_volta = Text("estado  S t+1     recompensa  R t+1", font_size=24, color=COR_AMBIENTE)
        rot_volta.next_to(volta, DOWN, buff=0.15)

        self.play(Create(agente), Create(ambiente))
        self.play(Create(ida), Write(rot_ida))
        self.play(Create(volta), Write(rot_volta))
        self.wait(0.5)

        # a fita da trajetoria vai crescendo embaixo
        fita = VGroup(Text("S 0", font_size=30, color=COR_AMBIENTE)).arrange(RIGHT, buff=0.3)
        fita.to_edge(DOWN, buff=1.0)
        self.play(FadeIn(fita))

        for t in range(self.N_PASSOS):
            pulso = Dot(color=COR_AGENTE, radius=0.11).move_to(ida.get_start())
            self.add(pulso)
            self.play(MoveAlongPath(pulso, ida), run_time=1.0)

            novo_a = Text(f"A {t}", font_size=30, color=COR_AGENTE)
            self._acrescentar(fita, novo_a)
            self.remove(pulso)

            pulso = Dot(color=COR_RECOMPENSA, radius=0.11).move_to(volta.get_start())
            self.add(pulso)
            self.play(MoveAlongPath(pulso, volta), run_time=1.0)
            self.remove(pulso)

            novo_r = Text(f"R {t + 1}", font_size=30, color=COR_RECOMPENSA)
            self._acrescentar(fita, novo_r)
            novo_s = Text(f"S {t + 1}", font_size=30, color=COR_AMBIENTE)
            self._acrescentar(fita, novo_s)

        aviso = Text(
            "a recompensa da ação A t chega como R t+1",
            font_size=26, color=COR_RECOMPENSA,
        ).next_to(fita, UP, buff=0.5)
        self.play(Write(aviso))
        self.wait(2)

    def _acrescentar(self, fita, novo):
        """Coloca um simbolo no fim da fita e recentra o conjunto."""
        novo.next_to(fita[-1], RIGHT, buff=0.3)
        fita.add(novo)
        self.play(FadeIn(novo), run_time=0.35)
        self.play(fita.animate.move_to(ORIGIN + 2.6 * DOWN), run_time=0.25)


class RecompensaVersusValor(Scene):
    """Guloso pela recompensa x guloso pelo valor, varrendo o desconto gama."""

    N = 3            # passos ate o premio grande
    GRANDE = 10.0    # tamanho do premio grande
    PEQUENO = 1.0    # recompensa imediata a esquerda

    def construct(self):
        total = self.N + 2
        celulas = VGroup(*[
            Square(side_length=1.0, stroke_width=2,
                   color=COR_RECOMPENSA if i in (0, total - 1) else GREY)
            for i in range(total)
        ]).arrange(RIGHT, buff=0.18).shift(1.8 * UP)

        rotulos = VGroup(
            Text(f"+{self.PEQUENO:g}", font_size=26, color=COR_RECOMPENSA).move_to(celulas[0]),
            Text(f"+{self.GRANDE:g}", font_size=26, color=COR_RECOMPENSA).move_to(celulas[-1]),
        )
        zeros = VGroup(*[
            Text("0", font_size=22, color=GREY).move_to(celulas[i])
            for i in range(2, total - 1)
        ])
        agente = Dot(color=COR_AGENTE, radius=0.18).move_to(celulas[1])

        self.play(Create(celulas), FadeIn(rotulos), FadeIn(zeros), FadeIn(agente))

        gama = ValueTracker(0.15)

        def retorno_direita():
            return self.GRANDE * gama.get_value() ** (self.N - 1)

        # --- barras: esquerda fixa, direita acompanha gama ---
        escala = 0.42
        base_x, base_y = -3.0, -0.6

        barra_esq = Rectangle(
            width=self.PEQUENO * escala, height=0.45,
            color=COR_RECOMPENSA, fill_opacity=0.5, stroke_width=1,
        )
        barra_esq.move_to([base_x + self.PEQUENO * escala / 2, base_y, 0])

        barra_dir = always_redraw(lambda: Rectangle(
            width=max(retorno_direita() * escala, 0.001), height=0.45,
            color=COR_RECOMPENSA, fill_opacity=0.85, stroke_width=1,
        ).move_to([base_x + retorno_direita() * escala / 2, base_y - 0.7, 0]))

        txt_esq = Text("ir para a esquerda:  G = 1,00", font_size=26, color=WHITE)
        txt_esq.next_to(barra_esq, UP, buff=0.18).align_to(barra_esq, LEFT)

        rot_dir = Text("ir para a direita:  G =", font_size=26, color=WHITE)
        val_dir = DecimalNumber(0, num_decimal_places=2, font_size=26, color=COR_RECOMPENSA)
        val_dir.add_updater(lambda m: m.set_value(retorno_direita()))
        grupo_dir = VGroup(rot_dir, val_dir).arrange(RIGHT, buff=0.18)
        grupo_dir.next_to(barra_dir, DOWN, buff=0.18).align_to(barra_esq, LEFT)

        leitura_gama = VGroup(
            Text("gama =", font_size=30, color=COR_AGENTE),
            DecimalNumber(0.15, num_decimal_places=2, font_size=30, color=COR_AGENTE),
        ).arrange(RIGHT, buff=0.15).to_edge(DOWN, buff=0.7)
        leitura_gama[1].add_updater(lambda m: m.set_value(gama.get_value()))

        self.play(FadeIn(barra_esq), FadeIn(txt_esq))
        self.add(barra_dir)
        self.play(FadeIn(grupo_dir), FadeIn(leitura_gama))
        self.wait(0.8)

        critico = (self.PEQUENO / self.GRANDE) ** (1.0 / (self.N - 1))
        linha = Line(
            [base_x + self.PEQUENO * escala, base_y + 0.35, 0],
            [base_x + self.PEQUENO * escala, base_y - 1.05, 0],
            color=RED, stroke_width=2,
        )
        self.play(Create(linha))

        # varre gama devagar ate o ponto de virada e depois ate quase 1
        self.play(gama.animate.set_value(critico), run_time=3.5)
        aviso = Text(
            f"empate em gama = {critico:.3f}",
            font_size=26, color=RED,
        ).next_to(linha, UP, buff=0.2)
        self.play(Write(aviso))
        self.wait(1.2)

        self.play(gama.animate.set_value(0.95), run_time=3.5)
        fecho = Text(
            "a recompensa imediata não mudou; o valor, sim",
            font_size=28, color=COR_RECOMPENSA,
        ).to_edge(DOWN, buff=1.6)
        self.play(Write(fecho))
        self.wait(2)

        val_dir.clear_updaters()
        leitura_gama[1].clear_updaters()
