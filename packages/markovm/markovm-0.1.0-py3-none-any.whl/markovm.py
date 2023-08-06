"""MarkovM: Python library for Markov Models."""

from dataclasses import dataclass
from typing import Any, Generator, Iterable, Optional

from numpy import float64, newaxis
from numpy.random import default_rng
from numpy.typing import NDArray

__version__: str = "0.1.0"


@dataclass(eq=False, frozen=True)
class MarkovModel:
    """Markov Model

    A stochastic model describing a sequence of possible events in which
    the probability of each event depends only on the state attained in
    the previous event.

    Attributes
    ----------
    state_space : tuple
        The collection of states in the Markov model.
    transition_matrix : NDArray
        The matrix describes the probabilities of transitions.
    """

    __slots__ = ["state_space", "transition_matrix"]

    state_space: tuple
    transition_matrix: NDArray[float64]


def create_markov_model(states: Iterable, transitions: NDArray) -> MarkovModel:
    """Create a Markov model.

    Provides an easy way to create a new Markov model and ensure the
    the transition matrix is valid by normalizing the transition argument
    automatically.

    Parameters
    ----------
    states : Iterable
        The collection of states in the Markov model.
    transitions : NDArray
        The matrix is to be normalized and serve as the transition matrix.

    Returns
    -------
    MarkovModel
        A newly created Markov model.

    Raises
    ------
    ValueError
        The shape of the transitions didn't match the total number of
        states. Given n states, the transitions matrix should be n-by-n.
    """
    # iterate through states and store as a tuple
    state_space = tuple(states)

    # verify if the transition shape matches with state size
    num_of_states = len(state_space)
    if transitions.shape != (num_of_states, num_of_states):
        raise ValueError("shape misatch between states and transitions")

    # normalize transitions
    transition_matrix = transitions / transitions.sum(axis=1)[:, newaxis]

    # create a new Markov model and return
    return MarkovModel(state_space, transition_matrix)


def random_walk(
    model: MarkovModel, index: int = 0, seed: Optional[int] = None
) -> Generator[Any, None, None]:
    """Randomly walk through the Markov model.

    Parameters
    ----------
    model : MarkovModel
        The Markov model contains states and transition probabilities.
    index : int, optional
        The index of the initial state, by default 0.
    seed : int, optional
        The seed is to be used to generate random moves, by default None.

    Yields
    ------
    state : Any
        The state after taking a random move.
    """
    idxes = tuple(i for i, _ in enumerate(model.state_space))
    rng = default_rng(seed=seed)

    while True:
        yield model.state_space[index]
        index = rng.choice(idxes, p=model.transition_matrix[index])
