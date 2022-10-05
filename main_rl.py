import random

import torch
import wandb

from env.maze_env import maze_env
from rl.q_agent_loc import QAgent
from utils.arguments import maze_args


# from tqdm import tqdm


def main(args, rand=False, exp_name='temp'):
    # wandb.init(project='IoT', entity='heemang')
    # wandb.init(project="etri", entity="curie_ahn", config=args)
    agent = QAgent(in_dim=2)
    agent.to(agent.device)
    env = maze_env(args)

    n_ep = 100000
    for e in range(n_ep):
        if rand:
            env.size = random.choice([5, 10, 15, 20])

        g, mask = env.reset()
        R, ep_len = 0, 0
        while True:
            ep_len += 1
            action = agent.step(g, mask)
            # assert mask.squeeze()[action].item() is False, "{}: maze={}, ag_loc={}, init_loc={}, mask={}".format(
            #     ep_len, env.maze, env.ag_loc, env.start_loc, mask)
            ng, r, n_mask, t = env.step(action)
            agent.push(g, action, mask, r, ng, n_mask, t)

            g, mask = ng, n_mask
            R += r
            if t:
                ret_dict = agent.fit()
                exp_dict = {"reward": R, 'ep_len': ep_len, 'epsilon': agent.epsilon, 'episode': e}
                # wandb.log({**exp_dict, **ret_dict})
                print({**exp_dict, **ret_dict})
                break

        if e % 1000 == 0 and e > 0:
            torch.save(agent.state_dict(), './saved/grid_{}_{}.th'.format(exp_name, e))


if __name__ == '__main__':
    exp_name = 'rand'
    main(maze_args, rand=True, exp_name=exp_name)