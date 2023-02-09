import matplotlib.pyplot as plt
import numpy as np
#import custom font
import matplotlib.ticker as mtick
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter

def bar_subplots(data1, data2, data3, data4, data5, data6):
    #import custom font
    font_path = './font/linux_libertine/LinLibertine_RB.ttf'  # the location of the font file
    my_font = font_manager.FontProperties(fname=font_path, size=16)  # get the font based on the font_path, set font size

    font_path2 = './font/linux_libertine/LinLibertine_R.ttf'  # the location of the font file
    my_font2 = font_manager.FontProperties(fname=font_path2, size=20)  # get the font based on the font_path, set font size
    
    
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
    
    axs[0].get_yaxis().get_major_formatter().set_scientific(True)
    axs[1].get_yaxis().get_major_formatter().set_scientific(True)
    axs[2].get_yaxis().get_major_formatter().set_scientific(True)

    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    axs[0].ticklabel_format(style='plain')
    axs[0].yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
    axs[1].ticklabel_format(style='plain')
    axs[1].yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
    axs[2].ticklabel_format(style='plain')
    axs[2].yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
    # Put a legend below current axis
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 3.78),
          fancybox=True, ncol=4, prop=my_font, frameon=False)

    # axs.flat[0].set(ylabel="Ambiq")
    axs.flat[0].set_ylabel("Ambiq", fontproperties=my_font2)
    axs.flat[1].set_ylabel("MSP430", fontproperties=my_font2)
    axs.flat[2].set_ylabel("MARS", fontproperties=my_font2)


    #set font type of tickmarks
    for label in axs[0].get_xticklabels():
        label.set_fontproperties(my_font2)
    for label in axs[0].get_yticklabels():
        label.set_fontproperties(my_font2)

    #set font type of tickmarks
    for label in axs[1].get_xticklabels():
        label.set_fontproperties(my_font2)
    for label in axs[1].get_yticklabels():
        label.set_fontproperties(my_font2)

    #set font type of tickmarks
    for label in axs[2].get_xticklabels():
        label.set_fontproperties(my_font2)
    for label in axs[2].get_yticklabels():
        label.set_fontproperties(my_font2)

    plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.1)
    fig.text(0.03, 0.5, "Number of Sensor Readings", ha='center', va='center', rotation='vertical', fontproperties=my_font, size=22)
    # plt.ylabel("Number of Sensor Readings", fontproperties=my_font, size=22)
    plt.xlabel("Timeline (Days)", fontproperties=my_font, size=22)
    
    # plt.legend()
    plt.show()

#Test data for this function
""" list1 = [139, 1414, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1029, 0, 0, 0, 0, 0, 0, 269, 1412, 1411, 1412, 1412, 1400, 1412, 1411, 1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 740]
list2 = [0, 1109, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414,1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 988, 0, 0, 0, 0, 0, 0, 198, 1412, 1411, 1412, 1412, 1400, 1412, 1411,1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 611]
list3 = [0, 474, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414,1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412,1411, 1412, 1412, 1412, 1411, 1412, 908, 0, 0, 0, 0, 0, 0, 84, 1412, 1411, 1412, 1412, 1400, 1412, 1411, 1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 364]

list4 = [139, 1414, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1029, 0, 0, 0, 0, 0, 0, 269, 1412, 1411, 1412, 1412, 1400, 1412, 1411, 1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 740]
list5 = [0, 1109, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414,1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 988, 0, 0, 0, 0, 0, 0, 198, 1412, 1411, 1412, 1412, 1400, 1412, 1411,1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 611]
list6 = [0, 474, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414,1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412,1411, 1412, 1412, 1412, 1411, 1412, 908, 0, 0, 0, 0, 0, 0, 84, 1412, 1411, 1412, 1412, 1400, 1412, 1411, 1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 364]

print(len(list1), len(list2), len(list3))

bar_subplots(list1, list2, list3, list4, list5, list6) """

def count_vs_cap(cap_list, data1, data2, data3, data4, data5, data6):
    #import custom font
    font_path = './font/linux_libertine/LinLibertine_RB.ttf'  # the location of the font file
    my_font = font_manager.FontProperties(fname=font_path, size=16)  # get the font based on the font_path, set font size

    font_path2 = './font/linux_libertine/LinLibertine_R.ttf'  # the location of the font file
    my_font2 = font_manager.FontProperties(fname=font_path2, size=20)  # get the font based on the font_path, set font size

    fig, axs = plt.subplots(2, 1, figsize=(12, 4), sharex=True)
    #axs[0].set_xscale('log')
    axs[0].plot(cap_list, data1, color="blue", label="Ambiq", alpha=1)
    axs[0].plot(cap_list, data2, color="green", label="MSP430", alpha=1)
    axs[0].plot(cap_list, data3, color="orange", label="MARS", alpha=1)
    axs[0].set_yscale('log')

    #axs[1].set_xscale('log')
    axs[1].plot(cap_list, data4, color="blue", label="Ambiq", alpha=1)
    axs[1].plot(cap_list, data5, color="green", label="MSP430", alpha=1)
    axs[1].plot(cap_list, data6, color="orange", label="MARS", alpha=1)
    axs[1].set_yscale('log')
    
    axs.flat[0].set_ylabel("# of Readings", fontproperties=my_font2)
    axs.flat[0].set_title("v0", fontproperties=my_font2)
    axs.flat[1].set_ylabel("# of Readings", fontproperties=my_font2)
    axs.flat[1].set_title("v3", fontproperties=my_font2)
    plt.xlabel("Capacitance (F)", fontproperties=my_font, size=22)

    #set font type of tickmarks
    for label in axs[0].get_xticklabels():
        label.set_fontproperties(my_font2)
    for label in axs[0].get_yticklabels():
        label.set_fontproperties(my_font2)

    #set font type of tickmarks
    for label in axs[1].get_xticklabels():
        label.set_fontproperties(my_font2)
    for label in axs[1].get_yticklabels():
        label.set_fontproperties(my_font2)

    # Put a legend below current axis
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 2.55),
          fancybox=True, ncol=4, prop=my_font, frameon=False)
    plt.show()

#Test data for this function
'''cap_list = [1, 0.1, 0.01, 0.001, 0.0001, 1e-05, 1e-06, 1e-07, 1e-08, 1e-09, 1e-10, 1e-11, 1e-12, 1e-13, 1e-14, 1e-15,
1e-16, 1e-17, 1e-18, 1e-19]
ambiq0_exec_count = [248439, 1711270, 8138153, 2359716, 224158, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
msp0_exec_count = [4162913, 30319741, 144767449, 42059224, 4196734, 406224, 4058, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
mars0_exec_count = [64204219, 468316692, 2236152915, 649686231, 64913898, 6415356, 561323, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
ambiq3_exec_count = [343012, 2219577, 10556844, 3061778, 296520, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
msp3_exec_count = [5834163, 39439791, 187818639, 54567240, 5449090, 533153, 21069, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
mars3_exec_count = [90061052, 609191678, 2901145740, 842888862, 84217943, 8327399, 732399, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

count_vs_cap(cap_list, ambiq0_exec_count, msp0_exec_count, mars0_exec_count, ambiq3_exec_count, msp3_exec_count, mars3_exec_count)'''