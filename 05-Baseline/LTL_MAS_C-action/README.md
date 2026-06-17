# LTL_MAS_C-action
A package for the LTL motions and actions planning. The actions contains the Macro-actions.

** REMEMBER to add `path/to/LTL_MAS_C-action/src` to your PYTHONPATH**

updata 2020.6.21
Finished this algorithm.
There are mainly four functions to analysis the LTL planning question.

The first function is 'field' which is used to generate the basic data.

The second function is 'Buchi_poset_builder' which is used to generate a poset from buchi.

The thired function is 'Optimize_method' which contains the function the assigned the poset into the agent swarm.

The last function is 'Agent_swarm' which is used to simulation.
