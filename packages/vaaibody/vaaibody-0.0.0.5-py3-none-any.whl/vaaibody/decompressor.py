import torch


class Compressor(torch.nn.Module):
    """Compressor (Auto-dencoder)
    - pose 2 latent
    """

    def __init__(self, input_size, output_size, hidden_size=512):
        super(Compressor, self).__init__()

        self.fc1 = torch.nn.Linear(input_size, hidden_size)
        self.fc2 = torch.nn.Linear(hidden_size, hidden_size)
        self.fc3 = torch.nn.Linear(hidden_size, hidden_size)
        self.fc4 = torch.nn.Linear(hidden_size, output_size)
        self.elu = torch.nn.ELU()

    def forward(self, x):
        n_batch, n_window = x.shape[:2]
        x = x.reshape([n_batch * n_window, -1])
        out1 = self.elu(self.fc1(x))
        out2 = self.elu(self.fc2(out1))
        out3 = self.elu(self.fc3(out2))
        out4 = self.fc4(out3)
        return out4.reshape([n_batch, n_window, -1])


class Decompressor(torch.nn.Module):
    """Decompressor
    - feature+latent to pose
    """

    def __init__(self, input_size, output_size, hidden_size=512):
        super(Decompressor, self).__init__()

        print("input_size", input_size, "output_size", output_size)
        self.fc1 = torch.nn.Linear(input_size, hidden_size)
        self.fc2 = torch.nn.Linear(hidden_size, output_size)

        self.relu = torch.nn.ReLU()

    def forward(self, x):
        n_batch, n_window = x.shape[:2]
        x = x.reshape([n_batch * n_window, -1])

        out1 = self.relu(self.fc1(x))
        out2 = self.fc2(out1)

        return out2.reshape([n_batch, n_window, -1])
