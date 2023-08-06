import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import numpy as np
import colorcet as cc
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image

fig_width_pixels = 800
fig_height_pixels = 800
dpi = 100

def get_colors(N):
    colors = []
    step = 256 / N
    for i in range(N):
        index = int(i * step)
        colors.append(cc.rainbow[index])
    return colors

def plot_routes(routes, node_coords, save_path, draw_lines=True, draw_linehauls=True):
    """
    Plot the routes on a 2D plane.

    Args:
        routes (list): A list of routes, where each route is a list of node IDs.
        node_coords (dict): A dictionary of node coordinates, where the key is
            the node ID and the value is a tuple of the x and y coordinates.
        save_path (str): The path to save the plot to.
        draw_lines (bool): Whether to draw lines between the nodes in each route.
        draw_linehauls (bool): Whether to draw the linehauls in each route.

    Returns:
        save_path (str): The path to the saved plot.
    """
    fig = plt.figure(figsize=(fig_width_pixels / dpi, fig_height_pixels / dpi), dpi=dpi)

    # Create a list of unique colors for each route
    colors = get_colors(len(routes))

    # Plot each route with a different color
    for i, route in enumerate(routes):
        if not draw_linehauls:
            route = route[1: -1]
        x = [node_coords[node][0] for node in route]
        y = [node_coords[node][1] for node in route]
        if draw_lines:
            plt.plot(x, y, 'o-', color=colors[i])
        else:
            plt.plot(x, y, 'o', color=colors[i])

    # Plot the depot node with an X
    depot_x, depot_y = node_coords[0]
    plt.plot(depot_x, depot_y, 'kx', markersize=10, label='Depot')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Routes')
    plt.savefig(save_path)
    plt.close()
    return save_path

def plot_embeddings(routes, embeddings, save_path="test.png"):
    """
    Plot the embeddings in 2D space.
    
    Args:
        routes (list): A list of routes, where each route is a list of node IDs.
        embeddings (np.ndarray): A 2D array of embeddings, where each row is an
            embedding vector.

    Returns:
        save_path (str): The path to the saved plot.
    """
    fig = plt.figure(figsize=(fig_width_pixels / dpi, fig_height_pixels / dpi), dpi=dpi)

    # Colors
    colors = get_colors(len(routes))

    # Perform t-SNE dimensionality reduction
    tsne = TSNE(n_components=2, random_state=42)
    embeddings_2d = tsne.fit_transform(embeddings)

    # Initialize lists to store x and y coordinates for each class
    x_coords_list = []
    y_coords_list = []

    # Split the 2D embeddings based on the number of samples in each class
    for route in routes:
        # Extract x and y coordinates for the current class
        x_coords = embeddings_2d[route, 0]
        y_coords = embeddings_2d[route, 1]

        # Append the coordinates to the lists
        x_coords_list.append(x_coords)
        y_coords_list.append(y_coords)

    # Plot the embeddings for each class
    for idx, (x_coords, y_coords) in enumerate(zip(x_coords_list, y_coords_list)):
        plt.scatter(x_coords, y_coords, marker='.', color=colors[idx])
    x_coords = embeddings_2d[0, 0]
    y_coords = embeddings_2d[0, 1]
    plt.scatter(x_coords, y_coords, marker='x', color='black', label='Depot')

    plt.xlabel('Dimension 1')
    plt.ylabel('Dimension 2')
    plt.title('Embeddings in 2D Space')
    # plt.legend()

    # Save the plot as "test.png"
    plt.savefig(save_path)
    plt.close()
    return save_path

def concatenate_images(image_paths, grid_size, save_path="test.png"):
    """
    Concatenate a list of images into a grid.

    Args:
        image_paths (list): A list of image paths.
        grid_size (tuple): A tuple of the number of rows and columns in the grid.
        save_path (str): The path to save the concatenated image to.

    Returns:
        save_path (str): The path to the saved image.
    """
    num_images = len(image_paths)
    grid_rows, grid_cols = grid_size

    # Open and load all images
    images = [Image.open(path) for path in image_paths]

    # Determine the size of each image
    image_width, image_height = images[0].size

    # Create an empty grid canvas
    grid_width = image_width * grid_cols
    grid_height = image_height * grid_rows
    grid = Image.new('RGB', (grid_width, grid_height))

    # Paste each image onto the grid
    for i, image in enumerate(images):
        row = i // grid_cols
        col = i % grid_cols
        x = col * image_width
        y = row * image_height
        grid.paste(image, (x, y))

    # Display the concatenated image
    grid.show()

    # Save the concatenated image
    grid.save(save_path)

