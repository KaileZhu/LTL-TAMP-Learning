import matplotlib.pyplot as plt

# Set the size of the main figure
fig = plt.figure(figsize=(10, 6))

# Create subplots within the main figure
nrows, ncols = 2, 2
subfig1 = plt.subplot(nrows, ncols, 1)
subfig2 = plt.subplot(nrows, ncols, 2)
subfig3 = plt.subplot(nrows, ncols, 3)
subfig4 = plt.subplot(nrows, ncols, 4)

# Do your plotting for each subfigure
subfig1.plot([1, 2, 3], [4, 5, 6])
subfig2.plot([1, 2, 3], [6, 5, 4])
subfig3.plot([1, 2, 3], [2, 4, 6])
subfig4.plot([1, 2, 3], [3, 1, 2])

# Set titles or labels for each subfigure and position them at the bottom
title_size = 14  # Adjust the title size as needed
subfig1.set_title("Subfigure 1", fontsize=title_size, y=-0.2)
subfig2.set_title("Subfigure 2", fontsize=title_size, y=-0.2)
subfig3.set_title("Subfigure 3", fontsize=title_size, y=-0.2)
subfig4.set_title("Subfigure 4", fontsize=title_size, y=-0.2)

# Adjust the layout to prevent overlap of subfigure titles and axis labels
plt.tight_layout()

# Show the plot
plt.show()