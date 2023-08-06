import torch
import torch.nn as nn


class GruNet(nn.Module):
    """Implements a GRU model"""
    def __init__(self, input_size, output_size=256, num_layers=1, activation=nn.ReLU, dropout=0.0):
        """
        Initializes a GRU model.

        Parameters
        ----------
        input_size : int
            Input feature map size.
        output_size : int
            Recurrent hidden state and output size.
        dropout : float
            If non-zero, introduces a Dropout layer on the outputs of each GRU layer except the last layer.
        num_layers : int
            Number of recurrent layers.
        activation : func
            Non-linear activation function.
        """
        super(GruNet, self).__init__()

        self._rnn = nn.GRU(input_size=input_size, num_layers=num_layers, hidden_size=output_size, dropout=dropout)
        self._num_outputs = output_size
        self.activation = activation()

        self.train()

    @property
    def num_outputs(self):
        """Output feature map size (as in np.prod(self.output_shape))."""
        return self._num_outputs

    @property
    def recurrent_hidden_state_size(self):
        """Recurrent hidden state size"""
        return self._num_outputs

    def _forward_gru(self, x, hxs, done):
        """
        Fast forward pass GRU network.
        from Ilya Kostrikov. PyTorch Implementations of Reinforcement Learning Algorithms.
        https://github.com/ikostrikov/pytorch-a2c-ppo-acktr-gail. 2018

        Parameters
        ----------
        x : torch.tensor
            Feature map obtained from environment observation.
        hxs : torch.tensor
            Current recurrent hidden state.
        done : torch.tensor
            Current done tensor, indicating if episode has finished.

        Returns
        -------
        x : torch.tensor
            Feature map obtained after GRU.
        hxs : torch.tensor
            Updated recurrent hidden state.
        """

        masks = 1 - done

        if x.size(0) == hxs.size(0):
            self._rnn.flatten_parameters()
            x, hxs = self._rnn(x.unsqueeze(0), (hxs * masks).unsqueeze(0))
            x = x.squeeze(0)
            hxs = hxs.squeeze(0)
        else:
            # x is a (T, N, -1) tensor that has been flatten to (T * N, -1)
            N = hxs.size(0)
            T = int(x.size(0) / N)

            # unflatten
            x = x.view(T, N, x.size(1))

            # Same deal with masks
            masks = masks.view(T, N)

            # Let's figure out which steps in the sequence have a zero for any agent
            # We will always assume t=0 has a zero in it as that makes the logic cleaner
            has_zeros = torch.nonzero(((masks[1:] == 0.0).any(dim=-1)), as_tuple=False).squeeze().cpu()

            # +1 to correct the masks[1:]
            if has_zeros.dim() == 0:
                # Deal with scalar
                has_zeros = [has_zeros.item() + 1]
            else:
                has_zeros = (has_zeros + 1).numpy().tolist()

            # add t=0 and t=T to the list
            has_zeros = [0] + has_zeros + [T]

            hxs = hxs.unsqueeze(0)
            outputs = []
            for i in range(len(has_zeros) - 1):
                # We can now process steps that don't have any zeros in masks together!
                # This is much faster
                start_idx = has_zeros[i]
                end_idx = has_zeros[i + 1]

                self._rnn.flatten_parameters()
                rnn_scores, hxs = self._rnn(
                    x[start_idx:end_idx],
                    hxs * masks[start_idx].view(1, -1, 1))

                outputs.append(rnn_scores)

            # x is a (T, N, -1) tensor
            x = torch.cat(outputs, dim=0)
            # flatten
            x = x.view(T * N, -1)
            hxs = hxs.squeeze(0)

        return x, hxs

    def forward(self, inputs, rhs, done):
        """
        Forward pass Neural Network

        Parameters
        ----------
        inputs : torch.tensor
            A tensor containing episode observations.
        rhs : torch.tensor
            A tensor representing the recurrent hidden states.
        done : torch.tensor
            A tensor indicating where episodes end.

        Returns
        -------
        x : torch.tensor
            Output feature map.
        rhs : torch.tensor
            Updated recurrent hidden state.
        """

        x = inputs.view(inputs.size(0), -1)
        x, rhs = self._forward_gru(x, rhs, done)
        # x = self.activation(x)
        assert len(x.shape) == 2 and x.shape[1] == self.num_outputs
        return x, rhs

    def get_initial_recurrent_state(self, num_proc):
        """Returns a tensor of zeros with the expected shape of the model's rhs."""
        return torch.zeros(num_proc, self._layer_size)

