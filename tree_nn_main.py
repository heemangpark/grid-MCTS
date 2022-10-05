import networkx as nx
import numpy as np
import torch

from env.maze_env import maze_env
from mcts_nn.tree import Tree
from rl.q_agent_loc import QAgent
from utils.arguments import maze_args
from utils.visualize import vis_route

if __name__ == "__main__":
    for id in range(10):
        env = maze_env(maze_args)
        env.size = 5

        agent = QAgent(in_dim=2, embedding_dim=64)
        agent.load_state_dict(torch.load('./saved/grid_random2_22000.th', 'cuda'))

        g, mask = env.reset()
        tree = Tree(env, agent)
        tree.grow()
        vis_route(env.maze, tree.state_seq, env.start_loc, env.goal_loc, 'tree_{}'.format(id + 1))

    # nx.write_gpickle(tree, './tree/tree.nx')
    # np.save('./tree/route', np.array(tree.act_seq))
