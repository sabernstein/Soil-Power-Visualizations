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
    axs[0].set_xscale('log')
    axs[0].plot(cap_list, data1, color="blue", label="Ambiq", alpha=1)
    axs[0].plot(cap_list, data2, color="green", label="MSP430", alpha=1)
    axs[0].plot(cap_list, data3, color="orange", label="MARS", alpha=1)
    #axs[0].set_yscale('log')

    axs[1].set_xscale('log')
    axs[1].plot(cap_list, data4, color="blue", label="Ambiq", alpha=1)
    axs[1].plot(cap_list, data5, color="green", label="MSP430", alpha=1)
    axs[1].plot(cap_list, data6, color="orange", label="MARS", alpha=1)
    #axs[1].set_yscale('log')
    
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
'''

cap_list = [0.2, 0.196, 0.192, 0.188, 0.184, 0.18000000000000002, 0.17600000000000002, 0.17200000000000001, 0.168, 0.164, 0.16, 0.15600000000000003, 0.15200000000000002, 0.14800000000000002, 0.14400000000000002, 0.14, 0.136, 0.132, 0.128, 0.12400000000000001, 0.12000000000000001, 0.116, 0.11200000000000002, 0.10800000000000001, 0.10400000000000001, 0.1, 0.096, 0.09200000000000001, 0.08800000000000001, 0.084, 0.08000000000000002, 0.07600000000000001, 0.07200000000000001,0.068, 0.064, 0.06, 0.055999999999999994, 0.05200000000000002, 0.048000000000000015, 0.04400000000000001, 0.04000000000000001, 0.036000000000000004, 0.032, 0.027999999999999997, 0.02400000000000002, 0.020000000000000018, 0.016000000000000014, 0.01200000000000001, 0.008000000000000007, 0.0040000000000000036]
ambiq0_exec_count = [911231, 927165, 947040, 963925, 984096, 1003558, 1024601, 1046033, 1068366, 1094158, 1115862, 1143329, 1170475, 1200267, 1229429, 1260906, 1295102, 1330556, 1369125, 1408638, 1449873, 1496208, 1544643, 1594621, 1651199, 1711270, 1774536, 1842545, 1919437, 1998220, 2085964, 2182562, 2288628, 2403175, 2532634, 2674810, 2835953, 3017025, 3222312, 3455189, 3727974, 4043184, 4414032, 4856943, 5389974, 6036079, 6815939, 7707218, 8454007, 7491406]
msp0_exec_count = [16072500, 16374733, 16689149, 17016949, 17358067, 17713740, 18084413, 18472341, 18877544, 19301261, 19745282, 20210890, 20699646, 21213608, 21753942, 22324221, 22925149, 23560489, 24232889, 24946494, 25703203, 26508530, 27367217, 28284756, 29266410, 30319741, 31453091, 32675797, 33999005, 35435142, 36998191, 38706206, 40581514, 42647909, 44936646, 47485256, 50339030, 53555404, 57206006, 61382813, 66203420, 71821378, 78438900, 86320549, 95808643, 107314135, 121190772, 137063897, 150410898, 133330090]
mars0_exec_count = [248222242, 252896405, 257757684, 262817124, 268087520, 273581963, 279314901, 285302077, 291560967, 298109842, 304969853, 312163193, 319714837, 327651812, 336004528, 344806275, 354093833, 363908885, 374296638, 385309173, 397003867,409445615, 422708442, 436875513, 452041991, 468316692, 485824935, 504711294, 525143628, 547318039, 571465665, 597858849, 626822135, 658745707, 694101188, 733464160, 777544350, 827224159, 883615416, 948132774, 1022597696, 1109381560,1211597447, 1333339323, 1479897296, 1657619903, 1871966534, 2117159431, 2323325121, 2059493343]
ambiq3_exec_count = [1185216, 1207834, 1230552, 1254802, 1280528, 1303883, 1330575, 1358416, 1388729, 1419950, 1453929, 1487165, 1521726, 1558669, 1596632, 1636826, 1684046, 1730228, 1777386, 1830975, 1886428, 1944512, 2005533, 2071034, 2143975, 2219577, 2303310, 2391621, 2488028, 2593178, 2706419, 2830658, 2968944, 3116258, 3282985, 3471396, 3679756, 3912138, 4179457, 4482692, 4834124, 5242459, 5725061, 6299974, 6991641, 7827716, 8840617, 9996377, 10968335, 9721376]
msp3_exec_count = [20996661, 21387651, 21794733, 22217962, 22659305, 23118726, 23598685, 24099747, 24624413, 25172928, 25746840, 26349979, 26982422, 27647523, 28346761, 29085213, 29863699, 30685872, 31556852, 32479776, 33459916, 34503189, 35615050, 36803310, 38075222, 39439791, 40907886, 42492239, 44205787, 46065919, 48092208, 50306152, 52736416, 55414365, 58380880, 61683433, 65382819, 69551231, 74283744, 79698206, 85948071, 93231286, 101811063, 112029513, 124331406, 139250278,157244345, 177828992, 195136844, 172976128]
mars3_exec_count = [324302140, 330343651, 336627629, 343168566, 349982907, 357087634, 364501682, 372245464, 380341240, 388813375, 397688775, 406996447, 416768447, 427040449, 437851206, 449243913, 461266807, 473973362, 487422723, 501682046, 516825518,532938153, 550114954, 568464440, 588109530, 609191678, 631873078, 656341334, 682814101, 711546183, 742835899, 777037602, 814572086, 855944574, 901766926, 952785738, 1009920661, 1074316618, 1147415197, 1231050260, 1327584231, 1440092637, 1572613264, 1730454987, 1920480082, 2150924197, 2428871323, 2746833501, 3014186320, 2671882531]


count_vs_cap(cap_list, ambiq0_exec_count, msp0_exec_count, mars0_exec_count, ambiq3_exec_count, msp3_exec_count, mars3_exec_count)