from smartcab.agent import LearningAgent
from smartcab.environment import Environment
from smartcab.simulator import Simulator
import itertools

class DummyPlanner:
    NextDirection = None

    def next_waypoint(self):
        return self.NextDirection

def choose_optimal_action(state, waypoint):
    """ The choose_action function is called when the agent is asked to choose
        which action to take, based on the 'state' the smartcab is in. """

    # Set the agent state and default action
    action = None

    if state[1] == 'red':
        if waypoint == 'right':
            # turning on red light is allowed
            if state[3] != 'forward':
                action = waypoint
    else:
        if waypoint == 'forward':
            action = waypoint
        if waypoint == 'left':
            if (state[2] == None or state[2] == 'left'):
                action = waypoint
            else:
                action = 'forward'
        elif waypoint == 'right':
            action = waypoint

    return action

env = Environment()

##############
# Create the driving agent
# Flags:
#   learning   - set to True to force the driving agent to use Q-learning
#    * epsilon - continuous value for the exploration factor, default is 1
#    * alpha   - continuous value for the learning rate, default is 0.5
agent = env.create_agent(LearningAgent, completeStates=True, strategy=None, learning=True, alpha=0.5)

##############
# Follow the driving agent
# Flags:
#   enforce_deadline - set to True to enforce a deadline metric
env.set_primary_agent(agent, enforce_deadline=True)

##############
# Create the simulation
# Flags:
#   update_delay - continuous time (in seconds) between actions, default is 2.0 seconds
#   display      - set to False to disable the GUI if PyGame is enabled
#   log_metrics  - set to True to log trial and simulation results to /logs
#   optimized    - set to True to change the default log file name
sim = Simulator(env, update_delay=0, log_metrics=True, display=False, optimized=True)

##############
# Run the simulator
# Flags:
#   tolerance  - epsilon tolerance before beginning testing, default is 0.05
#   n_test     - discrete number of testing trials to perform, default is 0
sim.run(n_test=20)

Dummy = DummyPlanner

validWaypoints = ['left', 'right', 'forward']
lights = ['red', 'green']
otherTraffic = ['left', 'right', 'forward', None]

numBadActions = 0
numBadActionsNotFinished = 0
numUnknownStates = 0
for state in itertools.product( validWaypoints, lights, otherTraffic, otherTraffic, otherTraffic ):
    if state not in agent.Q:
        numUnknownStates += 1
    else:
        Dummy.NextDirection = state[0]
        agent.planer = Dummy
        chosenAction = agent.choose_action(state)

        optimalAction = choose_optimal_action(state, state[0])

        if chosenAction != optimalAction:
            print "Not Optimal!"
            print state
            print chosenAction
            print optimalAction
            numBadActions += 1

            if optimalAction not in agent.Q[state]:
                numBadActionsNotFinished += 1


print "Number of bad actions: ", numBadActions
print numBadActionsNotFinished, " of them couldn't have been chosen"
print "Number of unknown States: ", numUnknownStates