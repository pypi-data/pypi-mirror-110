"""This is one general script. For different data, you should re-write this and tune."""
from __future__ import print_function, division

import torch.nn.functional as F
from torch.nn import Module, Linear, ModuleList
from torch_geometric.nn import CGConv

from featurebox.models.models_geo.basemodel import BaseCrystalModel


class _Interactions(Module):
    """Auto attention."""

    def __init__(self, hidden_channels=64, num_gaussians=5, num_filters=64, n_conv=2,
                 ):
        super(_Interactions, self).__init__()
        self.lin0 = Linear(hidden_channels, num_filters)
        short_len = 5
        self.short = Linear(num_gaussians, short_len)

        self.conv = ModuleList()

        for _ in range(n_conv):
            nn = CGConv(channels=num_filters, dim=short_len,
                        aggr='add', batch_norm=False,
                        bias=True, )
            self.conv.append(nn)

        self.n_conv = n_conv

    def forward(self, h, edge_index, edge_weight, edge_attr, data):
        out = F.relu(self.lin0(h))
        edge_attr = F.relu(self.short(edge_attr))

        for convi in self.conv:
            out = F.relu(convi(x=out, edge_index=edge_index, edge_attr=edge_attr))

        return out


class CrystalGraphConvNet(BaseCrystalModel):
    """
    CrystalGraph with GAT.
    """

    def __init__(self, *args, num_gaussians=5, num_filters=64, hidden_channels=64, **kwargs):
        super(CrystalGraphConvNet, self).__init__(*args, num_gaussians=num_gaussians, num_filters=num_filters,
                                                  hidden_channels=hidden_channels, **kwargs)
        self.num_state_features = None  # not used for this network.

    def get_interactions_layer(self):
        self.interactions = _Interactions(self.hidden_channels, self.num_gaussians, self.num_filters,
                                          n_conv=self.num_interactions, )
