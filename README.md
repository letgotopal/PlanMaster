# PlanMaster

**PlanMaster(TM)** is a program designed to help shipping companies optimally solve 2 major issues with handling cargo shipment issues:
- Loading/Unloading Containers from Ships
- Balancing the ships

To make the most out of every order, our program facilitates high-speed results in predicting how to quickly and accurately do the tasks specified above. This would also be our documentation to indicate the aspects of this program as well as talk about functions on our code base.

## Front-end

For the Frontend part of this project, we chose to implement it with Django. When loading the website, it displays a simple UI to the user. We got the idea of how the UI should look like during a meeting on November 3rd. The navigation bar has two buttons, one to navigate home and the other is a menu button. The menu button is a drop-down button that gives you the option to go to the Log file download page. When you press the Log file download button, you are shown the option on another page to download the Log file, clear the Log file, or go back to the homepage. According to the elicitation meeting with Mr Keogh on October 19, we should only deal with one log file at any given time. The second button on the menu, “Tutorial,” takes you to the page where our tutorial video is. On our homepage, we have a button to upload the manifest. After selecting a manifest with the correct format, you press the upload button. It will display “File “filename” uploaded successfully!”. You will have the option to Load/Unload or Balance a ship using the manifest. Under the Load/Unload and Balance button, there is a text box that is used to keep track of signing in and signing out. Pressing the Load/Unload button takes you to the grid with the option to Load container or Unload containers. After selecting the operation that you need to do, you will press the process button that is under the grid. The idea to have a moves page came to us during a meeting on November 10; it will redirect you to a page with the required moves to Load/Unload containers. You have the option to press next to see the next move and back to see the previous move. There is a text box for the user to input comments about the containers. After you are done you press the Download Outbound Manifest button to download the manifest. You then press the Home button to go back to the homepage. Pressing the balance button displays the required moves to balance a ship. The screen has the same options as the Load/Unload moves screen.

The grid page contains the grid mechanism, which is visible after the user pushes the Load/Unload button on the home page. The grid displays the layout of the ship bay imported from the previously uploaded manifest. It shows each possible space as a cell in the grid, with labels depending on the status of the space. If the space is occupied, it shows the first 5 characters of the description extracted from the manifest. If the space is unoccupied, it shows the label “Empty”. If the cell does not have space for a container, then it is labeled “N/A”. In any case, each cell is labeled with its coordinates in the form of [row #, column #]. “Empty” cells are a light shade of gray, occupied cells are a medium shade of gray, and “N/A” cells are a dark shade of gray for clear visual differentiation. The grid mechanism also allows the user to select the containers that they want to unload by clicking on the corresponding cell. When selected, the cell will change to a distinctly different bright orange color for ease of visibility. This is also to match the accent color of our logo for theme consistency. Furthermore, there is a “Load” button at the top above the grid which when clicked, prompts the user to enter the description and weight of the container that they wish to load onto the ship. With all the inputs from the user, the user can click the button labeled “Process”. Our group decided the layout of this user interface, from the grid design to the cell display methods to the position of the buttons, during our meeting on November 3rd around 2:30 pm. The program then passes the data along to the backend loading and unloading algorithms and stores the data in our database for access further down the pipeline. While the algorithm is running, the “Process” button will change its label to “Working…” so that the user is aware that the computations are running. In the background, the program also generates the list of instructions for the user to follow. Once all of this is done, the grid page redirects automatically to the load/unload moves page mentioned before, where the instructions are displayed to the user.

## Back-end

### Ship Design

The design of the ship class was the fundamental basis of this project. The core elements for designing this user-defined class were first decided upon by all 4 members of the team on Nov 10, 2023. This was then subsequently expanded to fit specific needs which are briefly described in the functions below:

- `__init__()`: Is the base of the underlying ship class that makes up the object’s contents
  - Storing the rows and columns: ints
  - Setting up the bay: A 2D list storing tuples of weights and ship descriptions
  - ColHeights: A List tuples of type ints that store the top and bottom of the stack of containers
  - Gn: An int value of the score
  - craneLocation: A single tuple of ints that store the current position of the crane corresponding to the ship’s state
  - Parent: A ship type variable that traces back to its own parent
  - lastMove: A tuple of tuples of ints that store the initial and final position of the last container moved on the ship.

This brings us to the supporting functions within ship with a brief description for each one of them:

- `self_value(self, i, j, value)`: Changes the value of a ship based on its ith and jth location.
- `get_value(self, i, j)`: Gets the current value at an i, j index location on the ship.
- `calculateColHeight(self)`: Calculates the height of container stacks on each column every time it’s called
- `__eq__(self, other)`: Overloaded equality operator for Ship object comparisons
- `balanceTimeFunction(self, initCol,finalCol)`: Calculates the time taken to balance a given container based on the crane movement and its initial as well as final location.
- `balanceHeuristic(self)`: Calculates the heuristic value based on the ship’s current progress towards being balanced
- `unloadHeuristic(self, unloadList)`: Produces a heuristic value based on the progress achieved towards finishing all the unloads
- `craneTimeFunction(self, finalColumn)`: Calculates the time taken to move the crane to move from its current position to a new destination.
- `unloadTimeFunction(self, row, column)`: Calculates the time taken to unload a container.
- `siftHeuristic(self, goal)`: Calculates a probable heuristic value while trying to achieve in-place sifting.

### Algorithm Design Breakdown

Here, we are going to be presenting a brief overview of all the algorithm files that are used to achieve balancing, loading, unloading and shifting.

# Balancing Algorithm

Starting off with the balancing algorithm, we began with a simple UCS algorithm and designed our now-transformed `balanceOperations` functions following the final class in Week 8. This pointed us to the slide deck sent out on Nov 21, 2023, at 9:35 am. Following up on this at a meeting on Nov 27 at 4:50 pm, we used the idea of generating different ship states that place the current container in the most feasible position for every column. This would then prompt it to calculate the balancing value. During this move, we also accumulate the g(n) values taken to perform those actions. This was later expanded to adding the heuristic h(n) on Dec 1, 2023, at 2:30 pm. This value made the whole algorithm off the calculated F(n) value which also improved on the time taken to achieve the ideal balance state.

For the balancing heuristic, we based it off of the example provided in the same slide deck mentioned previously. We add up the total weight of all of the containers on the ship, and then the weights of each side (left, right) of the ship. With this, we can calculate the weight that each side should have to be properly balanced. Then we calculate the weight deficit of the lighter side, and search for a container on the surplus side that is less than or equal to that deficit. We know that in order to balance a ship, containers will have to be moved from the surplus side to the deficit side, so once we find the container, we figure out how many moves (horizontally) it would take to get it to the first available spot on the opposite side. This runs in a loop, updating the deficit side, until we are out of surplus-side containers that are less than or equal to the deficit. This gives us an estimate on the amount of moves it would take to balance a ship from its current state. We add the number of moves calculated (since they can directly be converted to minutes), to the original cost function and run the full algorithm with this.

# Unloading Algorithm

For the unloading algorithm, we also started out with a basic UCS algorithm. With this algorithm, we had to supply it with the starting state, a goal state, the list of containers to unload (from the transfer list), and a cost function. This is relatively straightforward for unloading. The starting state is the initial ship that comes into the port (which is detailed in the manifest). The goal state is a little more complicated, because we are looking for a ship that no longer contains the containers we wanted to remove. After meeting with Dr. Keogh in his office, we came to the conclusion that a good way to keep track of whether the ship is at a goal state or not would be to see if all of the items on the transfer list (that were to be unloaded) have been addressed by the program. Finally, for the cost function, we are just calculating the Manhattan distance it takes to move the crane to the container, and then move the container off of the ship to a truck, or to a different location on the ship (in cases where we need to move a container out of the way).

At a basic level, we look at a ship, then determine if any containers can be immediately removed. If so, we try to remove those. If there are containers in the way, we call a similar function to the balancing operations to get ship states where those containers are no longer in the way so we can unload from under them.

We also have a heuristic that checks how many containers are blocking containers that we want to remove. This is a decent heuristic because it gives an idea of how many additional moves we will have to make to unload all of the containers. Since it is in moves it can be converted to minutes.

# Load Algorithm

The load algorithm followed a simple looping function where we find the cheapest possible location to place each container onto. We started the discussion and implementation later onto the project around Dec 5, 2023, at 3:30 pm. This meant that for a given ship and a list of container/s, we loop through each container, place it in the best possible spot, update the ship, and follow the same pattern until all the containers have been placed on the bay. We also handle cases if we encounter any errors in terms of loading the containers which was covered on testing during Dec 12, 2023, around 3:12 pm, the function exits and returns the message on why it fails (ex. Failed for trying to load onto a full ship).


## Database
Our group decided to use the SQ-Lite database for the layout of this user interface, from the grid design to the cell display methods to the position of the buttons, during our meeting on November 3rd around 2:30 pm. The program then passes the data along to the backend loading and unloading algorithms and stores the data in this database for access further down the pipeline. This database facilitates the communications between the program’s frontend and backend.
