import matplotlib.pyplot as plt

plt.ion()

def plot(scores, mean_scores):
    plt.clf()
    plt.title('Entraînement...')
    plt.xlabel('Nombre de Jeux')
    plt.ylabel('Score')
    plt.plot(scores, label='Score')
    plt.plot(mean_scores, label='Score Moyen')
    plt.ylim(ymin=0)
    if len(scores) > 0:
        plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    if len(mean_scores) > 0:
        plt.text(len(mean_scores)-1, mean_scores[-1], f'{mean_scores[-1]:.1f}')
    plt.legend()
    plt.show(block=False)
    plt.pause(.1) 