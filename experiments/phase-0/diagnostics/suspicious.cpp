int evaluate(int count) {
  int result = 0;
  int unused = 7;

  if (count = 0) {
    result = 1;
  }

  unsigned limit = 10;
  if (count < limit) {
    result += 2;
  }

  double ratio = 0.5;
  int truncated = ratio;

  {
    int count = 3;
    result += count;
  }

  return result + truncated;
}

int main() {
  return evaluate(4);
}
