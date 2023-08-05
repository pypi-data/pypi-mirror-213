import torch
from pytorchrl.agent.env.vec_envs.vec_env_base import VecEnvWrapper


class VecPyTorch(VecEnvWrapper):
    """
    This wrapper turns obs, reward's and done's from numpy arrays to pytorch
    tensors and places them in the specified device, facilitating interaction
    between the environment and the actor critic function approximators (NNs).

    Parameters
    ----------
    venv : VecEnv
        Original vector environment, previous to applying the wrapper.
    device : torch.device
        CPU or specific GPU where obs, reward's and done's are placed after
        being transformed into pytorch tensors.

    Attributes
    ----------
    device : torch.device
        CPU or specific GPU where obs, reward's and done's are placed after
        being transformed into pytorch tensors.
    num_envs : int
        Size of vector environment.

    """
    def __init__(self, venv, device=torch.device('cpu')):
        super(VecPyTorch, self).__init__(venv)
        self.venv = venv
        self.device = device
        self.num_envs = venv.num_envs

    def reset(self):
        """New vec env reset function"""
        obs = self.venv.reset()
        if isinstance(obs, dict):
            for k in obs:
                obs[k] = torch.from_numpy(obs[k]).float().to(self.device)
        else:
            obs = torch.from_numpy(obs).float().to(self.device)
        return obs

    def reset_single_env(self, env_id):
        """Reset only one environment of the vector."""
        obs = self.venv.reset_single_env(env_id)
        obs = torch.from_numpy(obs).float().to(self.device)
        return obs

    def step_async(self, actions):
        """New vec env step_async function"""

        if isinstance(actions, dict):
            for k in actions:
                if isinstance(actions[k], torch.Tensor):
                    actions[k] = actions[k].squeeze(1).cpu().numpy()
        else:
            if isinstance(actions, torch.Tensor):
                # Squeeze the dimension for discrete actions
                actions = actions.squeeze(1).cpu().numpy()
            actions = actions[None, :]
        self.venv.step_async(actions.squeeze(0))

    def step_wait(self):
        """New vec env step_wait function"""
        obs, reward, done, info = self.venv.step_wait()

        if isinstance(obs, dict):
            for k in obs:
                obs[k] = torch.from_numpy(obs[k]).float().to(self.device)
        else:
            obs = torch.from_numpy(obs).float().to(self.device)

        reward = torch.from_numpy(reward).unsqueeze(dim=1).float().to(self.device)
        done = torch.from_numpy(done).unsqueeze(dim=1).float().to(self.device)

        return obs, reward, done, info
