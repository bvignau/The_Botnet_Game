# The_Botnet_Game 1.1

This tool is develop in order to help researchers to determine the most efficients features of botnets. It's a simulating tool and actually only the random and sequential scan are implemented. More behaviors will be implemented in the future.

## install python3 package

matplotlib
pandas
pyfastcopy


## Usage
To use this tool, just clone the repository, create a conf file and use the two bash scripts. 

### Configuration file
Before starting simulation, you need to set your parameters in the Simulation.conf file. The first section contains general parameters about the simulation : Time is the total number of turn, Steps correspond to the frequency of the measurement of the population size. The Thread parameter define how many thread will use one process of the simulation, number is the number of simulation each thread will do. The Total parameter define the total population of the simulation. The ensemble parameter defined how many different set of IoT will be simulated. This can be usefull to simulate the differents set of IoT architectures etc. Here the parameter is equal to 1, so all botnets will target the same population. 

The population section defined the proportion of potential victims for each botnets. The section botnet defined with how much bots each botnet starts.
### Start simulations
First use the script multiple.sh :

``./multiple.sh 5`` this commande will create five differents process. With our parameters Treads equal to 5 and number equal to 4 we will have a total of 5x5x4 = 100 simulations. The total number of process, threads and number are to adpat with your machine and desired number of simulation. Here, we let one example conf file, corresponding to our exeperience 1B

### Collect results

To collect the results, 1st use the collect.sh script, it will create a csv file with the result of all the simulations. Then use the python scrupt multiplot.py to create figures.
To use the collect script : ``collect.sh mirai00 5`` you need to run this command for each botnet population. In our example you need to run it two times :  
``collect.sh mirai00 5`` and ``collect.sh mirai10 5``.
It will create one CSV file with all the result of all simulation for each population. The script collect and produce one CSV for each call. 

## Results of our experiences

Our results for our experiences are detailed in the res/ directory.
