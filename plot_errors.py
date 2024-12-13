import argparse
import matplotlib.pyplot as plt
from utilities import FileReader

# Made changes in this file to reflect code used in lab 4. Optimized it to make it 
# easier to store results

def plot_errors(filename):
    headers, values = FileReader(filename).read_file()

    time_list = []

    first_stamp = values[0][-1]

    for val in values:
        time_list.append(val[-1] - first_stamp)

    fig, axes = plt.subplots(2, 1, figsize=(12, 6))
    fig.subplots_adjust(hspace=0.6)

    # PLOT THE STATE SPACE

    # EKF x and y positions
    axes[0].plot([lin[len(headers) - 3] for lin in values], [lin[len(headers) - 2] for lin in values])

    # Odom x and y positions
    axes[0].plot([lin[0] for lin in values], [lin[1] for lin in values])

    # x,y=map(list, zip(*planner.trajectory_planner()))
    # axes[0].plot(x,y, marker='.')

    axes[0].set_title("State Space")
    axes[0].set_xlabel("x Position (m)")
    axes[0].set_ylabel("y Position (m)")
    axes[0].legend(["EKF", "Odom"])
    axes[0].grid()


    # PLOT THE INDIVIDUAL STATES

    axes[1].set_title("Each Individual State")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("State Value")
    axes[1].grid()
    lines = []
    for i in range(0, len(headers) - 1):
        lines.append(axes[1].plot([time/1e9 for time in time_list], [lin[i] for lin in values], label=headers[i]))

    # FOLLOWING CODE IS USED TO TOGGLE ON AND OFF SPECIFIC LINES USING THE LEGEND
    # USED EXAMPLE FROM OFFICIAL MATPLOTLIB WEBSITE
    # LINK: https://matplotlib.org/stable/gallery/event_handling/legend_picking.html
    leg = axes[1].legend()
    lined = {}
    for legend_line, original_line in zip(leg.get_lines(), lines):
        legend_line.set_picker(4)  # 4 pts tolerance
        lined[legend_line] = original_line[0]

    def on_select(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle the visibility
        legend_line = event.artist
        original_line = lined[legend_line]
        visable = not original_line.get_visible()
        original_line.set_visible(visable)
        # Change the alpha on the line in the legend so we can see what lines have been toggled
        if visable:
            legend_line.set_alpha(1.0)
        else:
            legend_line.set_alpha(0.2)
        fig.canvas.draw()
    fig.canvas.mpl_connect('pick_event', on_select)
    plt.show()

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process these files')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')

    args = parser.parse_args()

    print("Plotting the files", args.files)

    filenames = args.files
    for filename in filenames:
        plot_errors(filename)