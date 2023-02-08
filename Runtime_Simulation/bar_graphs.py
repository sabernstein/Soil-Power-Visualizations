import matplotlib.pyplot as plt

def plot_stacked_bar_graphs(list1, list2, list3):
    fig, axs = plt.subplots(3, 1, figsize=(6, 12))

    index = [0, 1, 2, 3, 4]
    bar_width = 0.25

    axs[0].bar(index, list1, bar_width, label='List 1')
    axs[0].set_xlabel('Index')
    axs[0].set_ylabel('Value')
    axs[0].set_title('List 1')
    axs[0].legend()

    axs[1].bar(index, list2, bar_width, label='List 2')
    axs[1].set_xlabel('Index')
    axs[1].set_ylabel('Value')
    axs[1].set_title('List 2')
    axs[1].legend()

    axs[2].bar(index, list3, bar_width, label='List 3')
    axs[2].set_xlabel('Index')
    axs[2].set_ylabel('Value')
    axs[2].set_title('List 3')
    axs[2].legend()

    plt.tight_layout()
    plt.show()


list1 = [1, 2, 3, 4, 5]
list2 = [2, 4, 6, 8, 10]
list3 = [3, 6, 9, 12, 15]

plot_stacked_bar_graphs(list1, list2, list3)

