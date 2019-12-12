import STATE
import monte_carlo_tree_searchV2
import monte_carlo_tree_searchV1
import collections
import time
import pickle


import marshal
def pickle_text_heur(file1, file2, file3, file4, file1P, file2P, file3P, file4P):
    """
    file order: children, numvisited, rewards, heur, alternate files for pickle same order
    """
    children_out = file1
    num_visited_out = file2
    rewards_out = file3
    heur_out = file4

    Children = dict()
    VisitCount = collections.defaultdict(int)
    Rewards = collections.defaultdict(float)
    Heur = collections.defaultdict(float)

    start_time = time.time()

    child_file = open(children_out, 'r')
    child_line = child_file.readline()
    i = 0
    while child_line:
        if i%100 == 0:
            print(i)
            print(time.time() - start_time)
        i += 1
        child_line = child_line.split("   ")
        parent = STATE.State(tupleKey=eval(child_line[0]))
        children = child_line[1].split("  ")
        children.pop(len(children) - 1)
        set_children = set()
        for child in children:
            set_children.add(STATE.State(tupleKey=eval(child)))
        Children[parent] = set_children
        child_line = child_file.readline()
    child_file.close()

    reward_file = open(rewards_out, 'r')
    reward_line = reward_file.readline()
    while reward_line:
        reward_line = reward_line.split("  ")
        state_of_being = STATE.State(tupleKey=eval(reward_line[0]))
        reward = eval(reward_line[1])
        Rewards[state_of_being] = reward
        reward_line = reward_file.readline()
    reward_file.close()
    vis_file = open(num_visited_out, 'r')
    vis_line = vis_file.readline()
    while vis_line:
        vis_line = vis_line.split("  ")
        state_of_being = STATE.State(tupleKey=eval(vis_line[0]))
        num_vis = eval(vis_line[1])
        VisitCount[state_of_being] = num_vis
        vis_line = vis_file.readline()
    vis_file.close()
    heur_file = open(heur_out, 'r')
    heur_line = heur_file.readline()
    while heur_line:
        heur_line = heur_line.split("  ")
        state_of_being = STATE.State(tupleKey=eval(heur_line[0]))
        num_heur = eval(heur_line[1])
        Heur[state_of_being] = num_heur
        heur_line = heur_file.readline()
    vis_file.close()
    with open(file1P, 'wb') as children_dump:
        pickle.dump(Children, children_dump)
    with open(file2P, 'wb') as reward_dump:
        pickle.dump(Rewards, reward_dump)
    with open(file3P, 'wb') as vis_dump:
        pickle.dump(VisitCount, vis_dump)
    with open(file4P, 'wb') as heur_dump:
        pickle.dump(Heur, heur_dump)

    return


if __name__ == "__main__":
    pickle_text_heur('v2_sim50_heur1_children.txt', 'v2_sim50_heur1_rewards.txt', 'v2_sim50_heur1_num_visit.txt', 'v2_sim50_heur1_heur.txt',
                     'pkl_sim50_heur1_children.marshal', 'pkl_sim50_heur1_rewards.marshal', 'pkl_sim50_heur1_num_visit.marshal', 'pkl_sim50_heur1_heur.marshal')


