import matplotlib.pyplot as plt
from matplotlib import font_manager
import matplotlib.ticker as mtick

font_path = './font/linux_libertine/LinLibertine_RB.ttf'  # the location of the font file
my_font = font_manager.FontProperties(fname=font_path, size=21)  # get the font based on the font_path, set font size

font_path2 = './font/linux_libertine/LinLibertine_R.ttf'  # the location of the font file
my_font2 = font_manager.FontProperties(fname=font_path2, size=21)  # get the font based on the font_path, set font size

# Data
configurations = ["Apollo4", "Apollo4 ",  "MSP430", "MSP430 ", "MARS", "MARS "]
operations_achieved = [3.444036, 4.469896, 53.824715, 69.829561, 46189.237126, 59923.763640]
index = 0
for o in operations_achieved:
    operations_achieved[index] = o * (10**6)
    index += 1
# Define colors for each bar
# Define colors for each bar
colors = ['tab:green', 'tab:blue'] * 3

# Create a bar graph with custom colors
fig, ax = plt.subplots()
bars = plt.bar(configurations, operations_achieved, color=[colors[i % 2] for i in range(len(configurations))])




# Set labels and title
plt.xlabel('Configuration', fontproperties=my_font, labelpad=20)
plt.ylabel('Operations Achieved', fontproperties=my_font, labelpad=20)
ax.yaxis.set_major_locator(mtick.MaxNLocator(4))
ax.set_yscale('symlog',linthresh=1e1)
# plt.yscale('sqrt')

#set font type of tickmarks
for label in ax.get_xticklabels():
    label.set_fontproperties(my_font2)
for label in ax.get_yticklabels():
    label.set_fontproperties(my_font2)

# Create a legend
green_patch = plt.Rectangle((0, 0), 1, 1, color='tab:green')
blue_patch = plt.Rectangle((0, 0), 1, 1, color='tab:blue')
plt.legend([green_patch, blue_patch], ['v0', 'v3'],loc='upper center', bbox_to_anchor=(0.5, 1.25),
          fancybox=True, ncol=4, prop=my_font, frameon=False)

# Show the graph
plt.show()
