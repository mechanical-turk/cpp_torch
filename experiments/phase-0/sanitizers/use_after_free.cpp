int main() {
  int *value = new int{42};
  delete value;
  return *value;
}