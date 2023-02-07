import matplotlib.pyplot as plt

def plot_bar_graph(list1, list2, list3):
    fig, ax = plt.subplots()

    index = [0, 1, 2, 3, 4]
    bar_width = 0.25

    bar1 = ax.bar(index, list1, bar_width, label='List 1')
    bar2 = ax.bar([i + bar_width for i in index], list2, bar_width, label='List 2')
    bar3 = ax.bar([i + 2*bar_width for i in index], list3, bar_width, label='List 3')

    ax.set_xlabel('Index')
    ax.set_ylabel('Value')
    ax.set_title('Bar Graph of 3 Lists')
    ax.set_xticks([i + bar_width for i in index])
    ax.set_xticklabels(index)
    ax.legend()

    plt.tight_layout()
    plt.show()


list1 = [1, 2, 3, 4, 5]
list2 = [2, 4, 6, 8, 10]
list3 = [3, 6, 9, 12, 15]

plot_bar_graph(list1, list2, list3)
