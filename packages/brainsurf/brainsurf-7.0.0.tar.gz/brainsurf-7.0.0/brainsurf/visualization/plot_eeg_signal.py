import matplotlib.pyplot as plt

def plot_data(x, y, x_label, y_label, title):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.show()


def plot_comparison(x, y1, y2, x_label, y_label, title):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y1, label='Pre-Meditation')
    plt.plot(x, y2, label='Post-Meditation')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()
