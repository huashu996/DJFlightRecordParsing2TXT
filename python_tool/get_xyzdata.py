from pyproj import Proj
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as mplot3d
def read_coordinates_from_txt(file_path):
    coordinates = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            latitude = float(parts[0].split(':')[1].strip())
            longitude = float(parts[1].split(':')[1].strip())
            altitude = float(parts[2].split(':')[1].strip())
            coordinates.append((latitude, longitude, altitude))
    return coordinates

def calculate_avg_coordinates(coordinates):
    num_points = len(coordinates)
    avg_latitude = sum(coord[0] for coord in coordinates) / num_points
    avg_longitude = sum(coord[1] for coord in coordinates) / num_points
    return avg_latitude, avg_longitude


def project_coordinates_to_xyz(coordinates, avg_latitude, avg_longitude, origin_x, origin_y):
    # Define the projection coordinate system (UTM zone 10, WGS84 ellipsoid)
    p = Proj(proj='utm', zone=20, ellps='WGS84', preserve_units=False)

    # Project all points in the coordinates list to xy coordinate system
    projected_coordinates = [p(longitude, latitude) for latitude, longitude, _ in coordinates]

    # Calculate the relative xyz values for each point with respect to the origin
    relative_xyz_coordinates = []
    for (x, y), (_, _, altitude) in zip(projected_coordinates, coordinates):
        relative_x = x - origin_x
        relative_y = y - origin_y
        relative_xyz_coordinates.append((relative_x, relative_y, altitude))
    return relative_xyz_coordinates
    
def three_plot_coordinates(coordinates):
    # Separate the x, y, z coordinates for plotting
    x_values, y_values, z_values = zip(*coordinates)

    # Create a new figure for the 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot points as a 3D scatter plot
    ax.scatter(x_values, y_values, z_values, c='blue', label='Points')

    # Connect points with lines
    for i in range(1, len(x_values)):
        ax.plot([x_values[i - 1], x_values[i]], [y_values[i - 1], y_values[i]], [z_values[i - 1], z_values[i]], 'k-', linewidth=0.5)

    # Add labels and title
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_zlabel('Z (meters)')
    ax.set_title('Projected Coordinates - 3D')

    # Display the 3D plot in a separate window
    plt.show()

def two_plot_coordinates(coordinates):
    # Separate the x, y, z coordinates for plotting
    x_values, y_values, z_values = zip(*coordinates)

    # Create a new figure for the 2D plot
    fig = plt.figure()

    # Plot points
    plt.scatter(x_values, y_values, c='blue', label='Points')

    # Connect points with lines
    for i in range(1, len(x_values)):
        plt.plot([x_values[i - 1], x_values[i]], [y_values[i - 1], y_values[i]], 'k-', linewidth=0.5)

    # Add labels and title
    plt.xlabel('X (meters)')
    plt.ylabel('Y (meters)')
    plt.title('Projected Coordinates - 2D')
    plt.legend()

    # Display the 2D plot in a separate window
    plt.show()
    
if __name__ == "__main__":
    input_file_path = "lalo_output.txt"  # Replace with the actual input file path

    coordinates = read_coordinates_from_txt(input_file_path)

    # Use the first 10 points to define the projection coordinate system
    num_points_for_avg = 20
    avg_coordinates = coordinates[:num_points_for_avg]
    avg_latitude, avg_longitude = calculate_avg_coordinates(avg_coordinates)

    # Project the average latitude and longitude to xy coordinate system
    p = Proj(proj='utm', zone=20, ellps='WGS84', preserve_units=False)
    origin_x, origin_y = p(avg_longitude, avg_latitude)

    print(f"Average Latitude: {avg_latitude}, Average Longitude: {avg_longitude}")
    print(f"Projected Coordinates (x, y): {origin_x}, {origin_y}")

    # Project all points in the coordinates list to xy coordinate system
    first_coordinates = [(0, 0, 0)] * min(len(coordinates), num_points_for_avg)
    projected_coordinates2 = project_coordinates_to_xyz(coordinates[num_points_for_avg:], avg_latitude, avg_longitude, origin_x, origin_y)
    projected_coordinates = first_coordinates+projected_coordinates2
    # Save projected coordinates to a new text file
    output_file_path = "projected_coordinates.txt"
    with open(output_file_path, 'w') as output_file:
        for x, y, z in projected_coordinates:
            output_file.write(f"x: {x}, y: {y}, z: {z}\n")
    three_plot_coordinates(projected_coordinates)
    two_plot_coordinates(projected_coordinates)

