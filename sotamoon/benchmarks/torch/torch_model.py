"""The torch model class."""
import enum
import logging

import torch
import torch.optim as optim
import torch.nn.functional as F
import numpy as np

from ..model import Model, OPTIMISER_OFFSET


MAX_ITER_RANGE = 100.0
MAX_EVAL_RANGE = 125.0
HISTORY_SIZE_RANGE = 200.0
STRONG_WOLFE = "strong_wolfe"


class Optimiser(enum.IntEnum):
    """The optimiser action to perform."""
    Adadelta = 0
    Adagrad = 1
    Adam = 2
    AdamW = 3
    SparseAdam = 4
    Adamax = 5
    ASGD = 6
    LBFGS = 7
    RMSprop = 8
    Rprop = 9
    SGD = 10


class TorchModel(Model):
    """The model class for torch models."""
    def __init__(self, model_path: str):
        super().__init__(model_path)
        self.model = torch.jit.load(model_path)
        self.optimizer = self.generate_optimiser(super().vectorise())

    def generate_optimiser(self, vector: np.array) -> optim.Optimizer:
        """Create an optimiser from a vector."""
        optimiser_type = round(vector[OPTIMISER_OFFSET] * (Optimiser.SGD + 1))
        if optimiser_type == Optimiser.Adadelta:
            rho = vector[OPTIMISER_OFFSET + 1]
            eps = vector[OPTIMISER_OFFSET + 2]
            lr = vector[OPTIMISER_OFFSET + 3]
            weight_decay = vector[OPTIMISER_OFFSET + 4]
            logging.info(f"Mutating torch model optimiser=Adadelta rho={rho} eps={eps} lr={lr} weight_decay={weight_decay}")
            return optim.Adadelta(self.model.parameters(), rho=rho, eps=eps, lr=lr, weight_decay=weight_decay)
        elif optimiser_type == Optimiser.Adagrad:
            lr = vector[OPTIMISER_OFFSET + 1]
            lr_decay = vector[OPTIMISER_OFFSET + 2]
            weight_decay = vector[OPTIMISER_OFFSET + 3]
            eps = vector[OPTIMISER_OFFSET + 4]
            logging.info(f"Mutating torch model optimiser=Adagrad lr={lr} lr_decay={lr_decay} weight_decay={weight_decay} eps={eps}")
            return optim.Adagrad(self.model.parameters(), lr=lr, lr_decay=lr_decay, weight_decay=weight_decay, eps=eps)
        elif optimiser_type == Optimiser.Adam:
            lr = vector[OPTIMISER_OFFSET + 1]
            betas = (vector[OPTIMISER_OFFSET + 2], vector[OPTIMISER_OFFSET + 3])
            eps = vector[OPTIMISER_OFFSET + 4]
            weight_decay = vector[OPTIMISER_OFFSET + 5]
            amsgrad = bool(round(vector[OPTIMISER_OFFSET + 6]))
            logging.info(f"Mutating torch model optimiser=Adam lr={lr} betas=({betas[0]}, {betas[1]}), eps={eps} weight_decay={weight_decay} amsgrad={amsgrad}")
            return optim.Adam(self.model.parameters(), lr=lr, betas=betas, eps=eps, weight_decay=weight_decay, amsgrad=amsgrad)
        elif optimiser_type == Optimiser.AdamW:
            lr = vector[OPTIMISER_OFFSET + 1]
            betas = (vector[OPTIMISER_OFFSET + 2], vector[OPTIMISER_OFFSET + 3])
            eps = vector[OPTIMISER_OFFSET + 4]
            weight_decay = vector[OPTIMISER_OFFSET + 5]
            amsgrad = bool(round(vector[OPTIMISER_OFFSET + 6]))
            logging.info(f"Mutating torch model optimiser=AdamW lr={lr} betas=({betas[0]}, {betas[1]}), eps={eps} weight_decay={weight_decay} amsgrad={amsgrad}")
            return optim.AdamW(self.model.parameters(), lr=lr, betas=betas, eps=eps, weight_decay=weight_decay, amsgrad=amsgrad)
        elif optimiser_type == Optimiser.SparseAdam:
            lr = vector[OPTIMISER_OFFSET + 1]
            betas = (vector[OPTIMISER_OFFSET + 2], vector[OPTIMISER_OFFSET + 3])
            eps = vector[OPTIMISER_OFFSET + 4]
            logging.info(f"Mutating torch model optimiser=SparseAdam lr={lr} betas=({betas[0]}, {betas[1]}), eps={eps}")
            return optim.SparseAdam(self.model.parameters(), lr=lr, betas=betas, eps=eps)
        elif optimiser_type == Optimiser.Adamax:
            lr = vector[OPTIMISER_OFFSET + 1]
            betas = (vector[OPTIMISER_OFFSET + 2], vector[OPTIMISER_OFFSET + 3])
            eps = vector[OPTIMISER_OFFSET + 4]
            weight_decay = vector[OPTIMISER_OFFSET + 5]
            logging.info(f"Mutating torch model optimiser=Adamax lr={lr} betas=({betas[0]}, {betas[1]}), eps={eps} weight_decay={weight_decay}")
            return optim.Adamax(self.model.parameters(), lr=lr, betas=betas, eps=eps, weight_decay=weight_decay)
        elif optimiser_type == Optimiser.ASGD:
            lr = vector[OPTIMISER_OFFSET + 1]
            lambd = vector[OPTIMISER_OFFSET + 2]
            alpha = vector[OPTIMISER_OFFSET + 3]
            t0 = vector[OPTIMISER_OFFSET + 4]
            weight_decay = vector[OPTIMISER_OFFSET + 5]
            logging.info(f"Mutating torch model optimiser=ASGD lr={lr} lambd={lambd} alpha={alpha} t0={t0} weight_decay={weight_decay}")
            return optim.ASGD(self.model.parameters(), lr=lr, lambd=lambd, alpha=alpha, t0=t0, weight_decay=weight_decay)
        elif optimiser_type == Optimiser.LBFGS:
            lr = vector[OPTIMISER_OFFSET + 1]
            max_iter = round(vector[OPTIMISER_OFFSET + 2] * MAX_ITER_RANGE),
            max_eval = round(vector[OPTIMISER_OFFSET + 3] * MAX_EVAL_RANGE)
            tolerance_grad = vector[OPTIMISER_OFFSET + 4]
            tolerance_change = vector[OPTIMISER_OFFSET + 5]
            history_size = round(vector[OPTIMISER_OFFSET + 6] * HISTORY_SIZE_RANGE)
            line_search_fn = STRONG_WOLFE if bool(round(vector[OPTIMISER_OFFSET + 7])) else None
            logging.info(f"Mutating torch model optimiser=LBFGS lr={lr} max_iter={max_iter} max_eval={max_eval} tolerance_grad={tolerance_grad} tolerance_change={tolerance_change} history_size={history_size} line_search_fn={line_search_fn}")
            return optim.LBFGS(self.model.parameters(), lr=lr, max_iter=max_iter, max_eval=max_eval, tolerance_grad=tolerance_grad, tolerance_change=tolerance_change, history_size=history_size, line_search_fn=line_search_fn)
        elif optimiser_type == Optimiser.RMSprop:
            lr = vector[OPTIMISER_OFFSET + 1]
            momentum = vector[OPTIMISER_OFFSET + 2]
            alpha = vector[OPTIMISER_OFFSET + 3]
            eps = vector[OPTIMISER_OFFSET + 4]
            centered = bool(round(vector[OPTIMISER_OFFSET + 5]))
            weight_decay = vector[OPTIMISER_OFFSET + 6]
            logging.info(f"Mutating torch model optimiser=RMSprop lr={lr} momentum={momentum} alpha={alpha} eps={eps} centered={centered} weight_decay={weight_decay}")
            return optim.RMSprop(self.model.parameters(), lr=lr, momentum=momentum, alpha=alpha, eps=eps, centered=centered, weight_decay=weight_decay)
        elif optimiser_type == Optimiser.Rprop:
            lr = vector[OPTIMISER_OFFSET + 1]
            etas = vector[OPTIMISER_OFFSET + 2]
            step_sizes = (vector[OPTIMISER_OFFSET + 3], vector[OPTIMISER_OFFSET + 4])
            logging.info(f"Mutating torch model optimiser=Rprop lr={lr} etas={etas} step_sizes=({step_sizes[0]}, {step_sizes[1]})")
            return optim.Rprop(self.model.parameters(), lr=lr, etas=etas, step_sizes=step_sizes)
        lr = vector[OPTIMISER_OFFSET + 1]
        momentum = vector[OPTIMISER_OFFSET + 2]
        weight_decay = vector[OPTIMISER_OFFSET + 3]
        dampening = vector[OPTIMISER_OFFSET + 4]
        nesterov = bool(round(vector[OPTIMISER_OFFSET + 5]))
        logging.info(f"Mutating torch model optimiser=SGD lr={lr} momentum={momentum} weight_decay={weight_decay} dampening={dampening} nesterov={nesterov}")
        return optim.SGD(self.model.parameters(), lr=lr, momentum=momentum, weight_decay=weight_decay, dampening=dampening, nesterov=nesterov)

    def infer(self, x: np.array) -> np.array:
        """Run inference on a piece of data."""
        with torch.no_grad():
            return self.model(x).numpy()

    def vectorise(self) -> np.array:
        """Vectorise the model."""
        vector = super().vectorise()
        param_groups = self.optimizer.param_groups[0]
        if isinstance(self.optimizer, optim.Adadelta):
            vector[OPTIMISER_OFFSET] = float(Optimiser.Adadelta) / float(Optimiser.SGD + 1)
            vector[OPTIMISER_OFFSET + 1] = param_groups["rho"]
            vector[OPTIMISER_OFFSET + 2] = param_groups["eps"]
            vector[OPTIMISER_OFFSET + 3] = param_groups["lr"]
            vector[OPTIMISER_OFFSET + 4] = param_groups["weight_decay"]
        elif isinstance(self.optimizer, optim.Adagrad):
            vector[OPTIMISER_OFFSET] = float(Optimiser.Adagrad) / float(Optimiser.SGD + 1)
            vector[OPTIMISER_OFFSET + 1] = param_groups["lr"]
            vector[OPTIMISER_OFFSET + 2] = param_groups["lr_decay"]
            vector[OPTIMISER_OFFSET + 3] = param_groups["weight_decay"]
            vector[OPTIMISER_OFFSET + 4] = param_groups["eps"]
        elif isinstance(self.optimizer, optim.Adam):
            vector[OPTIMISER_OFFSET] = float(Optimiser.Adam) / float(Optimiser.SGD + 1)
            vector[OPTIMISER_OFFSET + 1] = param_groups["lr"]
            vector[OPTIMISER_OFFSET + 2] = param_groups["betas"][0]
            vector[OPTIMISER_OFFSET + 3] = param_groups["betas"][1]
            vector[OPTIMISER_OFFSET + 4] = param_groups["eps"]
            vector[OPTIMISER_OFFSET + 5] = param_groups["weight_decay"]
            vector[OPTIMISER_OFFSET + 6] = float(param_groups["amsgrad"])
        elif isinstance(self.optimizer, optim.AdamW):
            vector[OPTIMISER_OFFSET] = float(Optimiser.AdamW) / float(Optimiser.SGD + 1)
            vector[OPTIMISER_OFFSET + 1] = param_groups["lr"]
            vector[OPTIMISER_OFFSET + 2] = param_groups["betas"][0]
            vector[OPTIMISER_OFFSET + 3] = param_groups["betas"][1]
            vector[OPTIMISER_OFFSET + 4] = param_groups["eps"]
            vector[OPTIMISER_OFFSET + 5] = param_groups["weight_decay"]
            vector[OPTIMISER_OFFSET + 6] = float(param_groups["amsgrad"])
        elif isinstance(self.optimizer, optim.SparseAdam):
            vector[OPTIMISER_OFFSET] = float(Optimiser.SparseAdam) / float(Optimiser.SGD + 1)
            vector[OPTIMISER_OFFSET + 1] = param_groups["lr"]
            vector[OPTIMISER_OFFSET + 2] = param_groups["betas"][0]
            vector[OPTIMISER_OFFSET + 3] = param_groups["betas"][1]
            vector[OPTIMISER_OFFSET + 4] = param_groups["eps"]
        elif isinstance(self.optimizer, optim.Adamax):
            vector[OPTIMISER_OFFSET] = float(Optimiser.Adamax) / float(Optimiser.SGD + 1)
            vector[OPTIMISER_OFFSET + 1] = param_groups["lr"]
            vector[OPTIMISER_OFFSET + 2] = param_groups["betas"][0]
            vector[OPTIMISER_OFFSET + 3] = param_groups["betas"][1]
            vector[OPTIMISER_OFFSET + 4] = param_groups["eps"]
            vector[OPTIMISER_OFFSET + 5] = param_groups["weight_decay"]
        elif isinstance(self.optimizer, optim.ASGD):
            vector[OPTIMISER_OFFSET] = float(Optimiser.ASGD) / float(Optimiser.SGD + 1)
            vector[OPTIMISER_OFFSET + 1] = param_groups["lr"]
            vector[OPTIMISER_OFFSET + 2] = param_groups["lambd"]
            vector[OPTIMISER_OFFSET + 3] = param_groups["alpha"]
            vector[OPTIMISER_OFFSET + 4] = param_groups["t0"]
            vector[OPTIMISER_OFFSET + 5] = param_groups["weight_decay"]
        elif isinstance(self.optimizer, optim.LBFGS):
            vector[OPTIMISER_OFFSET] = float(Optimiser.LBFGS) / float(Optimiser.SGD + 1)
            vector[OPTIMISER_OFFSET + 1] = param_groups["lr"]
            vector[OPTIMISER_OFFSET + 2] = float(param_groups["max_iter"]) / MAX_ITER_RANGE
            vector[OPTIMISER_OFFSET + 3] = float(param_groups["max_eval"]) / MAX_EVAL_RANGE
            vector[OPTIMISER_OFFSET + 4] = param_groups["tolerance_grad"]
            vector[OPTIMISER_OFFSET + 5] = param_groups["tolerance_change"]
            vector[OPTIMISER_OFFSET + 6] = param_groups["history_size"] / HISTORY_SIZE_RANGE
            vector[OPTIMISER_OFFSET + 7] = param_groups["line_search_fn"] == STRONG_WOLFE
        elif isinstance(self.optimizer, optim.RMSprop):
            vector[OPTIMISER_OFFSET] = float(Optimiser.RMSprop) / float(Optimiser.SGD + 1)
            vector[OPTIMISER_OFFSET + 1] = param_groups["lr"]
            vector[OPTIMISER_OFFSET + 2] = param_groups["momentum"]
            vector[OPTIMISER_OFFSET + 3] = param_groups["alpha"]
            vector[OPTIMISER_OFFSET + 4] = param_groups["eps"]
            vector[OPTIMISER_OFFSET + 5] = float(param_groups["centered"])
            vector[OPTIMISER_OFFSET + 6] = param_groups["weight_decay"]
        elif isinstance(self.optimizer, optim.Rprop):
            vector[OPTIMISER_OFFSET] = float(Optimiser.Rprop) / float(Optimiser.SGD + 1)
            vector[OPTIMISER_OFFSET + 1] = param_groups["lr"]
            vector[OPTIMISER_OFFSET + 2] = param_groups["etas"]
            vector[OPTIMISER_OFFSET + 3] = param_groups["step_sizes"]
        elif isinstance(self.optimizer, optim.SGD):
            vector[OPTIMISER_OFFSET] = float(Optimiser.SGD) / float(Optimiser.SGD + 1)
            vector[OPTIMISER_OFFSET + 1] = param_groups["lr"]
            vector[OPTIMISER_OFFSET + 2] = param_groups["momentum"]
            vector[OPTIMISER_OFFSET + 3] = param_groups["weight_decay"]
            vector[OPTIMISER_OFFSET + 4] = param_groups["dampening"]
            vector[OPTIMISER_OFFSET + 5] = float(param_groups["nesterov"])
        return vector

    def mutate(self, vector: np.array, example_data: np.array, example_output: np.array):
        """Mutate the model using the new vector."""
        super().mutate(vector, example_data, example_output)
        self.optimizer = self.generate_optimiser(vector)

    def train(self, data: np.array, target: np.array):
        """Train the model."""
        def closure():
            self.optimizer.zero_grad()
            output = self.model(data)
            loss = F.nll_loss(output, target)
            loss.backward()
            self.optimizer.zero_grad()
            return loss
        self.optimizer.step(closure)

    def __str__(self):
        return str(self.model)
