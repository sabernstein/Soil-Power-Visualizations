import matplotlib.pyplot as plt
import numpy as np
#import custom font
import matplotlib.ticker as mtick
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter
import models

def bar_subplots(data1, data2, data3, data4, data5, data6):
    #import custom font
    font_path = './font/linux_libertine/LinLibertine_RB.ttf'  # the location of the font file
    my_font = font_manager.FontProperties(fname=font_path, size=16)  # get the font based on the font_path, set font size

    font_path2 = './font/linux_libertine/LinLibertine_R.ttf'  # the location of the font file
    my_font2 = font_manager.FontProperties(fname=font_path2, size=20)  # get the font based on the font_path, set font size
    
    
    fig, axs = plt.subplots(2, 1, figsize=(12, 4), sharex=True)
    barWidth = 0.3
    x = np.arange(len(data1))
    x1 = [item + barWidth for item in x]
    x2 = [item + barWidth for item in x1]
    axs[0].bar(x, data1, color="blue", label="Apollo4", width = barWidth, alpha=1)
    axs[0].bar(x1, data2, color="green", label="MSP430", width = barWidth, alpha=1)
    axs[0].bar(x2, data3, color="orange", label="MARS", width = barWidth, alpha=1)
    axs[0].set_yscale('log')

    axs[1].bar(x, data4, color="blue", label="Apollo4", width = barWidth, alpha=1)
    axs[1].bar(x1, data5, color="green", label="MSP430", width = barWidth, alpha=1)
    axs[1].bar(x2, data6, color="orange", label="MARS", width = barWidth, alpha=1)
    axs[1].set_yscale('log')

    #axs[2].bar(x, data3, color="blue", label="v0", width = barWidth, alpha=1)
    #axs[2].bar(x1, data6, color="green", label="v3", width = barWidth, alpha=0.7)
    
    #axs[0].get_yaxis().get_major_formatter().set_scientific(True)
    #axs[1].get_yaxis().get_major_formatter().set_scientific(True)
    #axs[2].get_yaxis().get_major_formatter().set_scientific(True)

    #plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    #axs[0].ticklabel_format(style='plain')
    #axs[0].yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
    #axs[1].ticklabel_format(style='plain')
    #axs[1].yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
    #axs[2].ticklabel_format(style='plain')
    #axs[2].yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
    # Put a legend below current axis
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 2.4),
          fancybox=True, ncol=4, prop=my_font, frameon=False)

    # axs.flat[0].set(ylabel="Ambiq")
    axs.flat[0].set_ylabel("v0", fontproperties=my_font2)
    axs.flat[1].set_ylabel("v3", fontproperties=my_font2)
    #axs.flat[2].set_ylabel("MARS", fontproperties=my_font2)


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
    # for label in axs[2].get_xticklabels():
    #     label.set_fontproperties(my_font2)
    # for label in axs[2].get_yticklabels():
    #     label.set_fontproperties(my_font2)

    plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.1)
    fig.text(0.07, 0.5, "Number of Operations", ha='center', va='center', rotation='vertical', fontproperties=my_font, size=22)
    # plt.ylabel("Number of Sensor Readings", fontproperties=my_font, size=22)
    plt.xlabel("Timeline (Days)", fontproperties=my_font, size=22)
    
    # plt.legend()
    plt.show()

#Test data for this function
'''list1 = [139, 1414, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1029, 0, 0, 0, 0, 0, 0, 269, 1412, 1411, 1412, 1412, 1400, 1412, 1411, 1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 740]
list2 = [0, 1109, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414,1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 988, 0, 0, 0, 0, 0, 0, 198, 1412, 1411, 1412, 1412, 1400, 1412, 1411,1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 611]
list3 = [0, 474, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414,1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412,1411, 1412, 1412, 1412, 1411, 1412, 908, 0, 0, 0, 0, 0, 0, 84, 1412, 1411, 1412, 1412, 1400, 1412, 1411, 1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 364]

list4 = [139, 1414, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1029, 0, 0, 0, 0, 0, 0, 269, 1412, 1411, 1412, 1412, 1400, 1412, 1411, 1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 740]
list5 = [0, 1109, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414,1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 988, 0, 0, 0, 0, 0, 0, 198, 1412, 1411, 1412, 1412, 1400, 1412, 1411,1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 611]
list6 = [0, 474, 1413, 1414, 1412, 1414, 1414, 1413, 1414, 1413, 1414, 1414, 1413, 1414, 372, 1406, 1414, 1414,1413, 1414, 1413, 1414, 1414, 1413, 1414, 1413, 1362, 1412, 1411, 1412, 1412, 1412, 1411, 1412, 1412, 1412,1411, 1412, 1412, 1412, 1411, 1412, 908, 0, 0, 0, 0, 0, 0, 84, 1412, 1411, 1412, 1412, 1400, 1412, 1411, 1412, 1412, 1411, 1412, 1411, 1412, 1411, 1412, 1412, 1313, 1412, 1412, 1411, 364]

print(len(list1), len(list2), len(list3))

bar_subplots(list1, list2, list3, list4, list5, list6)'''

def count_vs_cap(cap_list, data1, data2, data3, data4, data5, data6):
    #import custom font
    font_path = './font/linux_libertine/LinLibertine_RB.ttf'  # the location of the font file
    my_font = font_manager.FontProperties(fname=font_path, size=16)  # get the font based on the font_path, set font size

    font_path2 = './font/linux_libertine/LinLibertine_R.ttf'  # the location of the font file
    my_font2 = font_manager.FontProperties(fname=font_path2, size=20)  # get the font based on the font_path, set font size

    fig, axs = plt.subplots(2, 1, figsize=(12, 4), sharex=True)
    axs[0].set_xscale('log')
    axs[0].plot(cap_list, data1, color="blue", label="Ambiq", alpha=1)
    axs[0].plot(cap_list, data2, color="green", label="MSP430", alpha=1)
    axs[0].plot(cap_list, data3, color="orange", label="MARS", alpha=1)
    axs[0].set_yscale('log')

    axs[1].set_xscale('log')
    axs[1].plot(cap_list, data4, color="blue", label="Ambiq", alpha=1)
    axs[1].plot(cap_list, data5, color="green", label="MSP430", alpha=1)
    axs[1].plot(cap_list, data6, color="orange", label="MARS", alpha=1)
    axs[1].set_yscale('log')
    
    axs.flat[0].set_ylabel("# of Operations", fontproperties=my_font2)
    axs.flat[0].set_title("v0", fontproperties=my_font2)
    axs.flat[1].set_ylabel("# of Operations", fontproperties=my_font2)
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
mars3_exec_count = [90061052, 609191678, 2901145740, 842888862, 84217943, 8327399, 732399, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]'''

'''
cap_list = [0.015, 0.0147, 0.0144, 0.0141, 0.0138, 0.0135, 0.0132, 0.0129, 0.0126, 0.0123, 0.012, 0.0117, 0.0114, 0.011099999999999999, 0.0108, 0.010499999999999999, 0.0102, 0.009899999999999999, 0.009600000000000001, 0.0093, 0.009000000000000001, 0.0087, 0.008400000000000001, 0.0081, 0.0078, 0.0075, 0.0072, 0.0069, 0.0066, 0.0063, 0.006, 0.0057, 0.0054, 0.0051, 0.0048000000000000004, 0.0045000000000000005, 0.004200000000000001, 0.0039000000000000007, 0.0036000000000000008, 0.003300000000000001, 0.003000000000000001, 0.002700000000000001, 0.002400000000000001, 0.002100000000000001, 0.0018000000000000013, 0.0015000000000000013, 0.0012000000000000014, 0.0009000000000000015, 0.0005999999999999998, 0.0002999999999999999]
ambiq0_exec_count = [2885520, 2912608, 2941229, 2968561, 2995178, 3022220, 3051678, 3079059, 3106432, 3133340, 3162585, 3189746, 3216139, 3243567, 3269777, 3296861, 3320810, 3346168, 3368266, 3389972, 3411244, 3428617, 3447050, 3460480, 3471033, 3480298, 3484579, 3484481, 3479596, 3467561, 3451000, 3423950, 3390643, 3345267, 3289907, 3218545, 3133912, 3032443, 2910894, 2769265, 2606177, 2417412, 2206810, 1969352, 1712845, 1440378, 1155571, 867510, 574366, 280608]
msp0_exec_count = [63634363, 64232672, 64835717, 65443051, 66054862, 66669497, 67286847, 67905742, 68525389, 69144283, 69761013, 70374444, 70982478, 71583573, 72174739, 72753138, 73316492, 73860900, 74382296, 74876017, 75337242, 75759473, 76136067, 76459219, 76720424, 76908357, 77012315, 77017912, 76911192, 76673276, 76285253, 75723877, 74964484, 73977454, 72731086, 71189770, 69315347, 67065874, 64399404, 61274794, 57654482, 53511227, 48834101, 43638037, 37976579, 31942465, 25662659, 19267740, 12844366, 6417658]
mars0_exec_count = [30899520824, 31189924549, 31482761034, 31777792234, 32074740217, 32373280959, 32673040259, 32973584725, 33274414813, 33574955950, 33874548152, 34172433579, 34467744797, 34759487729, 35046524257, 35327553556, 35601087016, 35865422833, 36118615491, 36358440031, 36582352857, 36787444406, 36970387770, 37127376853, 37254058019, 37345452057, 37395864661, 37398787685, 37346788092, 37231387737, 37042933800, 36770465312, 36401583568, 35922337878, 35317147345, 34568792136, 33658524246, 32566369234, 31271729866, 29754438303, 27996450994, 25984399818, 23713170902, 21190426729, 18441319847, 15511204669, 12461992241, 9357069399, 6238292742, 3118499309]
ambiq3_exec_count = [3742005, 3776879, 3812833, 3847929, 3882678, 3919306, 3955203, 3991580, 4027922, 4064044, 4101074, 4135695, 4171747, 4206781, 4241119, 4275656, 4308446, 4340759, 4370183, 4398241, 4425826, 4450136, 4472631, 4490168, 4506232, 4516503, 4523240, 4523385, 4516165, 4502165, 4479327, 4446180, 4400922, 4342988, 4270383, 4179104, 4069316, 3936912, 3781204, 3596589, 3384082, 3140012, 2864865, 2559093, 2227730, 1871478, 1504425, 1128047, 752310, 369486]
msp3_exec_count = [82564106, 83339694, 84121519, 84909490, 85702511, 86499887, 87300709, 88103071, 88906254, 89709147, 90509118, 91304537, 92092822, 92872296, 93638850, 94389356, 95119761, 95825894, 96501862, 97142251, 97740192, 98287641, 98776116, 99195484, 99533604, 99777482, 99912303, 99919797, 99780429, 99472192, 98968515, 98240570, 97254926, 95974482, 94357680, 92358109, 89926405, 87008498, 83549832, 79495747, 74799107, 69423688, 63355609, 56615642, 49270861, 41442049, 33295205, 24999572, 16665668, 8330519]
mars3_exec_count = [40091347835, 40467934854, 40847678282, 41230268739, 41615346097, 42002490701, 42391216662, 42780961937, 43171078582, 43560821837, 43949335144, 44335636316, 44718599379, 45096934944, 45469167989, 45833610078, 46188330927, 46531122874, 46859462547, 47170463674, 47460826996, 47726778627, 47964002079, 48167561503, 48331808645, 48450284765, 48515603345, 48519321325, 48451796875, 48302031464, 48057502684, 47703992058, 47225414278, 46603670905, 45818548377, 44847706258, 43666821741, 42249978985, 40570453716, 38602078106, 36321436966, 33711181045, 30764666282, 27491825407, 23925279878, 20123867284, 16167909789, 12139654765, 8093419145, 4045863699]

print(models.getMax(cap_list, ambiq0_exec_count))
print(models.getMax(cap_list, msp0_exec_count))
print(models.getMax(cap_list, mars0_exec_count))
print(models.getMax(cap_list, ambiq3_exec_count))
print(models.getMax(cap_list, msp3_exec_count))
print(models.getMax(cap_list, mars3_exec_count))

count_vs_cap(cap_list, ambiq0_exec_count, msp0_exec_count, mars0_exec_count, ambiq3_exec_count, msp3_exec_count, mars3_exec_count)'''