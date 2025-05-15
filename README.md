**Code Description: Interactive Neural Grid Simulation**

This Python script simulates and visualizes a 2D grid of simple "integrate-and-fire" neurons using the Pygame library for graphics and event handling, and the NumPy library for efficient numerical calculations. It creates a dynamic, evolving visual pattern based on the interactions between neighboring neurons.

**Core Functionality:**

1.  **Neuron Grid:** A 2D grid (defined by `MATRIX_WIDTH` and `MATRIX_HEIGHT`) represents the neurons. Each neuron's state is stored as a floating-point "potential" value in a NumPy array (`neuron_potential`).
2.  **Potential Accumulation:** In each simulation step, every neuron's potential increases slightly due to a small, random `FLUCTUATION_AMOUNT`.
3.  **Firing Mechanism:** If a neuron's potential reaches or exceeds a defined `THRESHOLD`, it is marked as "fired" for the current step.
4.  **Neighbor Interaction (8 Neighbors):** When a neuron fires, it releases a certain amount of `RELEASE_ENERGY`. A portion of this energy (`NEIGHBOR_COUPLING`) is distributed equally among its 8 immediate neighbors (including diagonals). This increases the potential of the neighboring neurons, potentially causing them to fire in subsequent steps. The simulation uses NumPy's array padding (`np.pad` with `mode='wrap'`) and slicing for efficient calculation of neighbor influences across the entire grid, handling edges with wrap-around (toroidal) boundary conditions.
5.  **Reset:** Neurons that fire have their potential reset to a low random value (between `RESET_POTENTIAL_LOW` and `RESET_POTENTIAL_HIGH`) in the same simulation step.
6.  **Visualization:** The state of the neuron grid is visualized in real-time in a fullscreen Pygame window. Each neuron's potential (from 0 up to the `THRESHOLD`) is mapped to a grayscale color (black for low potential, white for high/near-threshold potential). The NumPy array data is efficiently converted to a Pygame surface using `pygame.surfarray.make_surface` (after transposing the array dimensions) and scaled to fit the screen.
7.  **User Interaction:**
    *   **Left Mouse Click:** Clicking the left mouse button instantly sets the potential of neurons within a square area (defined by `CLICK_RADIUS`) around the cursor to the `THRESHOLD`, causing them to fire and potentially initiating waves of activity.
    *   **'X' Key Press:** Pressing the 'x' key instantly sets the potential of neurons within a square area (`CLICK_RADIUS`) around the current mouse cursor position to the minimum (`RESET_POTENTIAL_LOW`), effectively suppressing activity in that region.
    *   **Escape Key:** Pressing the Escape key quits the simulation.
8.  **Configurable Parameters:** Key aspects of the simulation (grid size, threshold, energy levels, fluctuation rate, interaction strength, click radius) are defined as constants at the beginning of the script, allowing for easy experimentation with different behaviors.

[Screenshot showing neural automaton running with 3 stages of an erased circle](image.png)

**Dependencies:**

*   `pygame`: For graphics, window management, and event handling.
*   `numpy`: For efficient array operations crucial to the simulation's performance.
*   `sys`: For exiting the program cleanly.

In essence, the code creates a visually engaging cellular automaton where simple rules governing local interactions lead to complex emergent patterns like spreading waves and interference phenomena, which the user can interact with directly.
