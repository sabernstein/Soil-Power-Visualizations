import matplotlib.pyplot as plt
import numpy as np

def bar_subplots(data1, data2, data3, data4, data5, data6):
    #import custom font
    from matplotlib import font_manager
    font_path = './font/linux_libertine/LinLibertine_RB.ttf'  # the location of the font file
    my_font = font_manager.FontProperties(fname=font_path, size=16)  # get the font based on the font_path, set font size

    font_path2 = './font/linux_libertine/LinLibertine_R.ttf'  # the location of the font file
    my_font2 = font_manager.FontProperties(fname=font_path2, size=22)  # get the font based on the font_path, set font size
    
    
    fig, axs = plt.subplots(3, 1, figsize=(12, 4), sharex=True)
    barWidth = 0.5
    x = np.arange(len(data1))
    x1 = [item + barWidth for item in x]
    axs[0].bar(x, data1, color="blue", label="v0", width = barWidth, alpha=1)
    axs[0].bar(x1, data4, color="green", label="v3", width = barWidth, alpha=0.7)

    axs[1].bar(x, data2, color="blue", label="v0", width = barWidth, alpha=1)
    axs[1].bar(x1, data5, color="green", label="v3", width = barWidth, alpha=0.7)

    axs[2].bar(x, data3, color="blue", label="v0", width = barWidth, alpha=1)
    axs[2].bar(x1, data6, color="green", label="v3", width = barWidth, alpha=0.7)
    
    # Put a legend below current axis
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.18),
          fancybox=True, ncol=4, prop=my_font, frameon=False)

    axs.flat[0].set(ylabel="Ambiq")
    axs.flat[1].set(ylabel="MSP430")
    axs.flat[2].set(ylabel="MARS")

    plt.xlabel("Timeline (Days)", fontproperties=my_font, size=22)
    
    plt.legend()
    plt.show()
'''
list1 = [139, 1414, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1029, 0, 0, 0, 0, 0, 0, 269, 1412, 1411, 1412, 1412, 1400, 1412, 1411, 1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 740]
list2 = [0, 1109, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414,1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 988, 0, 0, 0, 0, 0, 0, 198, 1412, 1411, 1412, 1412, 1400, 1412, 1411,1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 611]
list3 = [0, 474, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414,1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412,1411, 1412, 1412, 1412, 1411, 1412, 908, 0, 0, 0, 0, 0, 0, 84, 1412, 1411, 1412, 1412, 1400, 1412, 1411, 1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 364]

list4 = [139, 1414, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1029, 0, 0, 0, 0, 0, 0, 269, 1412, 1411, 1412, 1412, 1400, 1412, 1411, 1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 740]
list5 = [0, 1109, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414,1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 988, 0, 0, 0, 0, 0, 0, 198, 1412, 1411, 1412, 1412, 1400, 1412, 1411,1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 611]
list6 = [0, 474, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414,1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412,1411, 1412, 1412, 1412, 1411, 1412, 908, 0, 0, 0, 0, 0, 0, 84, 1412, 1411, 1412, 1412, 1400, 1412, 1411, 1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 364]

print(len(list1), len(list2), len(list3))

bar_subplots(list1, list2, list3, list4, list5, list6)'''
