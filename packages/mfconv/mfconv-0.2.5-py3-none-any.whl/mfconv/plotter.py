import os
import numpy as np
import matplotlib.pyplot as plt

## Global dictionaries to look up string matches for MODFLOW version
MF_VERSION_STRING_MATCH = {
        'mf6': 'Model',
        'mf-usg': 'GWF-node number',
        'mf-surfact': 'TODO'
    }
     
MF_VERSION_LINE_MATCH = {
        'mf6': (3, 2, 4),
        'mf-usg': (2, 1, 3),
        'mf-surfact': 'TODO'
    }

def get_convergence_data(mf_version, lst_file_name, mode):
    """
    Parses a MODFLOW list file to return convergence data

    Args:
        mf_version (str): MODFLOW version (default: 'mf6)
        lst_file (str): MODFLOW list file, including directory (default: 'mfsim.lst')
        mode (str): Specifies whether it is a solo or multiple worker run (default: 'solo')

    Return:
        max_heads (list): list of maximum heads at every outer iteration
        max_head_cells (list): a list of tuples containing the maximum head cells for each outer iteration
    """

    ## Lists to append convergence data
    max_heads = []
    max_head_cells = []

    ## Fucntion to read list file  
    def read_lst_file(lst_file):

        ## Temporary lists to allow for multi worker loop
        max_heads_temp = []
        max_head_cells_temp = []

        ## Open the list file with directory
        with open(lst_file) as file:
            
            ## Loop through all the lines
            for line in file:
                
                ## Match the string for the MODFLOW version
                if MF_VERSION_STRING_MATCH.get(mf_version, '') in line.strip():
                    
                    ## Check for convergence in line [MF6]
                    if '*' not in line:

                        ## Strip and split line
                        line_values = line.strip().split()
                        
                        ## Get the max head, inner iteration count and max head cell (node or rcl)
                        max_head = float(line_values[MF_VERSION_LINE_MATCH.get(mf_version, ())[0]])
                        no_inner_iteration = float(line_values[MF_VERSION_LINE_MATCH.get(mf_version, ())[1]])
                        if mf_version == 'mf6':
                            max_head_cell = eval(line_values[MF_VERSION_LINE_MATCH.get(mf_version, ())[2]].split('-')[1])
                        elif mf_version == 'mf-usg':
                            max_head_cell = float(line.strip().split()[MF_VERSION_LINE_MATCH[mf_version][2]])
                        
                        ## Append the data to temp lists
                        max_heads_temp.append(max_head)
                        max_head_cells_temp.append(max_head_cell)

        ## Append back to the main lists
        max_heads.append(max_heads_temp)
        max_head_cells.append(max_head_cells_temp)

    ## Check for list file
    if os.path.exists(lst_file_name):
        
        ## If function in solo run mode, then runs through once
        if mode == 'solo':
            read_lst_file(lst_file_name)
            return max_heads[0], max_head_cells[0]
        
        ## If function in multi worker mode, then runs in a loop
        elif mode == 'multi':
            for dir in os.listdir(os.getcwd()):
                if dir.startswith('agent') and dir[len('agent'):].isdigit():
                    agent_folder = dir
                    agent_folder_lst = os.path.join(agent_folder, lst_file_name)
                    read_lst_file(agent_folder_lst)
            return max_heads, max_head_cells
    
def plot_convergence_data(mf_version, ax, max_heads, max_head_cells):
    """
    Plots the data fetched from MODFLOW list file.

    Args:
        mf_version (str): MODFLOW version (default: 'mf6)
        ax (axis): Matplotlib axis to plot data
        max_heads (list): list of maximum heads at every outer iteration
        max_head_cells (list): a list of tuples containing the maximum head cells for each outer iteration
    """
    ## Pull last maximum head cell number for text inset
    last_max_cell = max_head_cells[-1]

    ## Plot the maximum heads for each outer iteration
    ax.plot(max_heads)
    
    ## Text insets for plot on convergence data
    ax.text(0, 0.90, f'Max Head: {max_heads[-1]:.2f}', transform=ax.transAxes)
    if mf_version == 'mf6':
        ax.text(0, 0.95, f'Max Head Cell: R-{last_max_cell[1]}, C-{last_max_cell[2]}, L-{last_max_cell[0]}',
                transform=ax.transAxes)
    elif mf_version == 'mf-usg':
        ax.text(0, 0.95, f'Max Node: {int(last_max_cell)}', transform=ax.transAxes)
    
    ## Plot formatting details
    ax.grid(True)
    ax.set_xlabel('Outer Iteration')
    ax.set_ylabel('Max Head Change')
    ax.relim()
    ax.autoscale_view()

    ## Draw the figure
    plt.draw()

def run_plotter(root_folder=os.getcwd(), mf_version='mf6', lst_file_name='mfsim.lst', worker_folder_name='agent', mode='solo'):
    """
    Run plotter for MODFLOW run.
    
    Args:
        root_folder (str): Root folder path (default: current working directory)
        mf_version (str): MODFLOW version (default: 'mf6')
        lst_file_name (str): Name of the simulation list file (default: 'mfsim.lst')
        worker_folder_name (str): Name of the worker folders (default: 'agent')
        mode (str): Specifies whether it is a solo or multiple worker run (default: 'solo')
    """
    print('Plotter is running in infinite loop so ctrl+c to exit when done')
    
    lst_file_dir = os.path.join(root_folder, lst_file_name)
    
    ## Infinte loop to run the data fetcher and plotter
    if mode == 'solo':

        ## Create figure and axes outside of infinite loop
        fig, ax = plt.subplots()
        
        ## Infinite loop of data fetching and plotting
        while True:
            max_heads, max_head_cells = get_convergence_data(mf_version, lst_file_dir, mode)
            plot_convergence_data(mf_version, ax, max_heads, max_head_cells)
            plt.pause(5)
            ax.clear()

    ## Infinte loop to run the data fetcher and plotter in looped fashion
    elif mode == 'multi':
        
        # Iterate through folders looking for workers for plotting
        n_subplots = 0
        for dir in os.listdir(root_folder):
            if dir.startswith(worker_folder_name) and dir[len(worker_folder_name):].isdigit():
                n_subplots += 1
        
        # Calculate the number of rows and columns for subplots
        n_rows = int(np.ceil(np.sqrt(n_subplots)))
        n_cols = int(np.ceil(n_subplots / n_rows))

        ## Create figure and axes outside of infinite loop
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(10,10))
        
        ## Infinite loop of data fetching and plotting in multiplots
        while True:
            max_heads, max_head_cells = get_convergence_data(mf_version, lst_file_dir, mode)
            for ax, m_h, m_h_c in zip(axes.ravel(), max_heads, max_head_cells): ## TODO: Delete spare plots
                plot_convergence_data(mf_version, ax, m_h, m_h_c)
            plt.pause(5)
            for ax in axes.ravel():
                ax.clear()