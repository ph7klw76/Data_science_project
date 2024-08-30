import matplotlib.pyplot as plt

def draw_energy_levels(singlet_levels, triplet_levels, offset=0.00, text_offset=0.5):
    fig, ax = plt.subplots()

    # Sort the energy levels
    singlet_levels.sort()
    triplet_levels.sort()

    # Function to add small offset to near-degenerate states
    def add_offset(levels):
        new_levels = []
        offsets = {}
        for level in levels:
            if level not in offsets:
                offsets[level] = 0
            new_levels.append(level + offsets[level])
            offsets[level] += offset
        return new_levels

    singlet_levels = add_offset(singlet_levels)
    triplet_levels = add_offset(triplet_levels)

    # Draw singlet energy levels
    for i, level in enumerate(singlet_levels):
        ax.hlines(level, xmin=0, xmax=1, color='b', linewidth=2, label='Singlet' if i == 0 else "")
        alignment = 'left' if i % 2 == 0 else 'right'
        x_position = 0.25
        
        # Adjust the text position to prevent overlap
        if i > 0 and abs(level - singlet_levels[i-1]) < text_offset:
            x_position += (i % 2) * text_offset
        
        ax.text(x_position, level, f"$S_{{{i+1}}}$", verticalalignment='bottom', horizontalalignment=alignment, fontsize=12, color='b')

    # Draw triplet energy levels
    for ii, level in enumerate(triplet_levels):
        ax.hlines(level, xmin=2, xmax=3, color='r', linewidth=2, label='Triplet' if ii == 0 else "")
        alignment = 'left' if ii % 2 == 0 else 'right'
        x_position = 2.0
        
        # Adjust the text position to prevent overlap
        if ii > 0 and abs(level - triplet_levels[ii-1]) < text_offset:
            x_position += (ii % 2) * text_offset
        
        ax.text(x_position, level, f"$T_{{{ii+1}}}$", verticalalignment='bottom', horizontalalignment=alignment, fontsize=12, color='r')

    # Add labels and title
    ax.set_title('Energy Level Diagram', fontsize=16)
    ax.set_xlabel('Energy Levels', fontsize=16)
    ax.set_ylabel('Energy (eV)', fontsize=16)
    ax.yaxis.set_tick_params(labelsize=16)
    ax.set_ylim([2.60, 3.3])
    
    # Place the legend in the middle
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), fontsize=16)

    # Show the plot
    plt.show()

# Sample singlet and triplet energy levels in eV
singlet_levels = [
    2.75176327,
    3.23288507,
    4.09366319,
    4.40879688,
    4.64652538,
    4.79724668,
    5.131936,
    5.1451659,
    5.39367757
]


triplet_levels = [ 2.61871081, 3.08919253, 3.97894078, 4.25410725, 4.5281552, 4.62266481, 5.05572113, 5.07874281 ]

draw_energy_levels(singlet_levels, triplet_levels)
