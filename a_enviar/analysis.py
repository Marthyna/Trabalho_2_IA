# analysis.py
# -----------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.


def question2():
    answerDiscount = 0.9
    answerNoise = 0

    # Reduzir o ruído para 0 faz com que as ações sejam determinísticas,
    # ou seja, o agente fica mais estável e não corre o risco de "cair"
    # no abismo ao se mover pela ponte. Aumentá-lo causaria o efeito contrário.

    # Mudar o disconto para 1, apesar de fazer o agente priorizar mais a
    # recompensa futura, não ajuda muito pois seguimos com o problema das
    # ações instáveis, e baixá-lo faria com que o agente focasse ainda menos
    # na recompensa futura, deixando-o menos propenso a cruzar a ponte.

    return answerDiscount, answerNoise


if __name__ == "__main__":
    print("Answers to analysis questions:")
    import analysis

    for q in [q for q in dir(analysis) if q.startswith("question")]:
        response = getattr(analysis, q)()
        print("  Question %s:\t%s" % (q, str(response)))
