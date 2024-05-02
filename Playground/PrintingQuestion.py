import matplotlib.pyplot as plt

class Vertex:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

def find_top_peaks(vertices):
    n = len(vertices)
    top_threshold = sum(vertex.y for vertex in vertices) / n  # Average Y-coordinate

    peaks = []

    # Loop through each vertex
    for i in range(n):
        current = vertices[i]
        prev = vertices[i - 1]  # Previous vertex wraps automatically due to negative indexing
        next = vertices[(i + 1) % n]  # Next vertex wraps around using modulus

        # Check if current vertex is a peak and above the average
        if current.y > prev.y and current.y > next.y and current.y > top_threshold:
            peaks.append(current.id)

    peaks.sort()
    return peaks[:-1] # Return all peaks except the last one (one that is connected to the plate)



def plot_graph(vertices, edges):
    fig, ax = plt.subplots()

    # Plot vertices
    for vertex in vertices:
        ax.plot(vertex.x, vertex.y, 'bo')  
        ax.text(vertex.x, vertex.y + 0.1, f'V{vertex.id}', color='blue', ha='center')

    # Draw edges
    for v1, v2 in edges:
        ax.plot([vertices[v1 - 1].x, vertices[v2 - 1].x],
                [vertices[v1 - 1].y, vertices[v2 - 1].y], 'k-') 

    ax.set_aspect('equal', adjustable='datalim')
    plt.grid(True)
    plt.show()


# example test

vertices = [
    Vertex(1, 0, 0), Vertex(2, 2, -1), Vertex(3, 4, 1),
    Vertex(4, 6, 0.5), Vertex(5, 8, 1.5), Vertex(6, 9, -1.5),
    Vertex(7, 7, -3), Vertex(8, 5, -4), Vertex(9, 3, -3),
    Vertex(10, 1, -2), Vertex(11, -1, 0), Vertex(12, -2, 2)
]
edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 1)]

plot_graph(vertices, edges)
print(find_top_peaks(vertices))
plot_graph(vertices, edges)