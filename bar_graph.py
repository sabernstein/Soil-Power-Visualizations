import matplotlib.pyplot as plt
from matplotlib import font_manager

font_path = './font/linux_libertine/LinLibertine_RB.ttf'  # the location of the font file
my_font = font_manager.FontProperties(fname=font_path, size=21)  # get the font based on the font_path, set font size

font_path2 = './font/linux_libertine/LinLibertine_R.ttf'  # the location of the font file
my_font2 = font_manager.FontProperties(fname=font_path2, size=21)  # get the font based on the font_path, set font size

# Data
configurations = ["v0: Apollo4", "v0: MSP430", "v0: MARS", "v3: Apollo4", "v3: MSP430", "v3: MARS"]
operations_achieved = [3.444036, 53.824715, 46189.237126, 4.469896, 69.829561, 59923.763640]


# Create a bar graph
fig, ax = plt.subplots()
plt.bar(configurations, operations_achieved)



# Set labels and title
plt.xlabel('Configuration', fontproperties=my_font, labelpad=20)
plt.ylabel('Operations Achieved (10^6)', fontproperties=my_font, labelpad=20)

ax.set_yscale('log')


#set font type of tickmarks
for label in ax.get_xticklabels():
    label.set_fontproperties(my_font2)
for label in ax.get_yticklabels():
    label.set_fontproperties(my_font2)

# Show the graph
plt.show()
