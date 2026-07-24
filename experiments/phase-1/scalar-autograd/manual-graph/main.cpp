#include <cassert>
#include <iostream>
#include <unordered_set>
#include <vector>

enum class Operation {
  leaf,
  multiply,
  add,
  subtract,
  square,
};

struct Node {
  double data;
  double grad = 0.0;
  Operation operation = Operation::leaf;
  Node *left = nullptr;
  Node *right = nullptr;
};

void build_topology(
    Node *node,
    std::unordered_set<Node *>& visited,
    std::vector<Node *>& topology
) {
  if (!node || visited.contains(node))
    return;
  visited.insert(node);
  build_topology(node->left, visited, topology);
  build_topology(node->right, visited, topology);
  topology.push_back(node);
}

void backward_local(
    Node& node
) {
  switch (node.operation) {
  case Operation::leaf:
    break;
  case Operation::multiply: {
    assert(node.left != nullptr);
    assert(node.right != nullptr);
    node.left->grad += node.grad * node.right->data;
    node.right->grad += node.grad * node.left->data;
    break;
  }
  case Operation::add: {
    assert(node.left != nullptr);
    assert(node.right != nullptr);
    node.left->grad += node.grad;
    node.right->grad += node.grad;
    break;
  }
  case Operation::subtract: {
    assert(node.left != nullptr);
    assert(node.right != nullptr);
    node.left->grad += node.grad;
    node.right->grad -= node.grad;
    break;
  }
  case Operation::square: {
    assert(node.left != nullptr);
    node.left->grad += node.grad * 2 * node.left->data;
    break;
  }
  }
}

int main() {

  Node x(3.0);
  Node y(4.0);

  Node m {
    .data = x.data * y.data,
    .operation = Operation::multiply,
    .left = &x,
    .right = &y,
  };

  Node loss {
    .data = m.data + m.data,
    .operation = Operation::add,
    .left = &m,
    .right = &m
  };

  std::cout << "loss: " << loss.data << '\n';

  loss.grad = 1.0;

  std::unordered_set<Node *> visited;
  std::vector<Node *> topology;
  build_topology(&loss, visited, topology);

  for (auto it = topology.rbegin(); it != topology.rend(); ++it) {
    backward_local(**it);
  }

  std::cout << "m.grad: " << m.grad << '\n';
  std::cout << "x.grad: " << x.grad << '\n';
  std::cout << "y.grad: " << y.grad << '\n';
}
