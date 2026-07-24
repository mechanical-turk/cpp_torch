#include "value.hpp"
#include <memory>
#include <unordered_set>
#include <utility>
#include <vector>

namespace cpp_torch::autograd::detail {
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
  std::shared_ptr<Node> left = nullptr;
  std::shared_ptr<Node> right = nullptr;

  void backward_local() {
    switch (operation) {
    case Operation::leaf:
      break;
    case Operation::multiply: {
      left->grad += grad * right->data;
      right->grad += grad * left->data;
      break;
    }
    case Operation::add: {
      left->grad += grad;
      right->grad += grad;
      break;
    }
    case Operation::subtract: {
      left->grad += grad;
      right->grad -= grad;
      break;
    }
    case Operation::square: {
      left->grad += grad * 2 * left->data;
      break;
    }
    }
  }
};

void build_topology(
    Node *node,
    std::unordered_set<Node *>& visited,
    std::vector<Node *>& topology
) {
  if (!node || visited.contains(node))
    return;
  visited.insert(node);
  build_topology(node->left.get(), visited, topology);
  build_topology(node->right.get(), visited, topology);
  topology.push_back(node);
}

std::vector<Node *> make_topology(
    Node *node
) {
  std::unordered_set<Node *> visited;
  std::vector<Node *> topology;
  build_topology(node, visited, topology);
  return topology;
}

} // namespace cpp_torch::autograd::detail

namespace cpp_torch::autograd {
using cpp_torch::autograd::detail::Node;
using cpp_torch::autograd::detail::Operation;

Value::Value(
    double data
)
    : node_(std::make_shared<Node>(Node {.data = data})) {
}

double Value::data() const {
  return node_->data;
}

double Value::grad() const {
  return node_->grad;
}

Value Value::operator*(
    const Value& other
) const {
  std::shared_ptr<Node> node = std::make_shared<Node>(Node {
    .data = node_->data * other.data(),
    .operation = Operation::multiply,
    .left = node_,
    .right = other.node_,
  });
  return Value(std::move(node));
}

Value Value::operator+(
    const Value& other
) const {
  std::shared_ptr<Node> node = std::make_shared<Node>(Node {
    .data = node_->data + other.data(),
    .operation = Operation::add,
    .left = node_,
    .right = other.node_,
  });
  return Value(std::move(node));
}

Value Value::operator-(
    const Value& other
) const {
  std::shared_ptr<Node> node = std::make_shared<Node>(Node {
    .data = node_->data - other.data(),
    .operation = Operation::subtract,
    .left = node_,
    .right = other.node_,
  });
  return Value(std::move(node));
}

Value Value::square() const {
  std::shared_ptr<Node> node = std::make_shared<Node>(Node {
    .data = node_->data * node_->data,
    .operation = Operation::square,
    .left = node_,
  });
  return Value(std::move(node));
}

void Value::backward() {
  std::vector<Node *> topology = make_topology(node_.get());

  node_->grad = 1.0;

  for (auto it = topology.rbegin(); it != topology.rend(); ++it) {
    (*it)->backward_local();
  }
}

void Value::zero_grad() {
  for (Node *node : make_topology(node_.get())) {
    node->grad = 0.0;
  }
}

Value::Value(
    std::shared_ptr<Node> node
)
    : node_(std::move(node)) {
}

} // namespace cpp_torch::autograd
