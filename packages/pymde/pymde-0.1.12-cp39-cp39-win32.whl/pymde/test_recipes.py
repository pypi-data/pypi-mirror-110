import numpy as np
import torch

from pymde import constraints
from pymde import preprocess
from pymde import recipes
from pymde import util
from pymde.functions import penalties
import pymde.testing as testing


def test_k_nearest_neighbors():
    data_matrix = np.array([[0.0], [1.0], [1.5], [1.75]])
    graph = preprocess.data_matrix.k_nearest_neighbors(data_matrix, k=2)
    edges = set(tuple(e) for e in graph.edges.cpu().numpy().tolist())
    # [2, 1], [3, 2], [3, 1], omitted because they are duplicates
    expected = set(
        tuple(e)
        for e in np.array([[0, 1], [0, 2], [1, 2], [1, 3], [2, 3]]).tolist()
    )
    assert edges == expected

    edges = graph.edges.cpu().numpy()
    # 2 if i and j are neighbors of each other,
    # 1 if i is neighbor of j but not vice versa
    testing.assert_allclose(np.array([1.0, 1.0, 2.0, 2.0, 2.0]), graph.weights)


@testing.cpu_and_cuda
def test_laplacian_embedding(device):
    np.random.seed(0)
    torch.manual_seed(0)
    data_matrix = torch.randn(100, 10)

    np.random.seed(0)
    torch.manual_seed(0)
    laplacian_emb = recipes.laplacian_embedding(
        data_matrix, device=device
    ).embed()

    np.random.seed(0)
    torch.manual_seed(0)
    also_laplacian = recipes.preserve_neighbors(
        data_matrix,
        attractive_penalty=penalties.Quadratic,
        repulsive_penalty=None,
        device=device,
    ).embed()

    also_laplacian = util.align(source=also_laplacian, target=laplacian_emb)

    testing.assert_allclose(
        laplacian_emb.cpu().numpy(), also_laplacian.cpu().numpy()
    )


@testing.cpu_and_cuda
def test_anchor_initialization(device):
    n_items = 10

    np.random.seed(0)
    torch.manual_seed(0)
    data_matrix = torch.randn(n_items, 5)

    anchors = torch.tensor([0, 1, 3])
    values = torch.tensor([2.0, 1.0, 3.0]).reshape(3, 1)
    constraint = constraints.Anchored(anchors, values)

    # preserve neighbors
    mde = recipes.preserve_neighbors(
        data_matrix, embedding_dim=1, constraint=constraint, init="random"
    )
    testing.assert_allclose(mde._X_init[anchors], values)

    mde = recipes.preserve_neighbors(
        data_matrix, embedding_dim=1, constraint=constraint, init="quadratic"
    )
    testing.assert_allclose(mde._X_init[anchors], values)


@testing.cpu_and_cuda
def test_no_anchor_anchor_edges(device):
    np.random.seed(0)
    torch.manual_seed(0)
    data_matrix = torch.randn(3, 2)

    anchors = torch.tensor([0, 1])
    values = torch.tensor([2.0, 3.0]).reshape(2, 1)
    constraint = constraints.Anchored(anchors, values)

    mde = recipes.preserve_distances(
        data_matrix, embedding_dim=1, constraint=constraint
    )
    expected_edges = torch.tensor([[0, 2], [1, 2]])
    testing.assert_all_equal(expected_edges, mde.edges)

    mde = recipes.preserve_neighbors(
        data_matrix, embedding_dim=1, constraint=constraint
    )
    testing.assert_all_equal(expected_edges, mde.edges)
