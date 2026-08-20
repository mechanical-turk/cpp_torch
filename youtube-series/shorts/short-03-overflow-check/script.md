# Short 3: This Check Can Never Catch an Overflow

## Script

### 00:00-00:04

Start with:

```cpp
#include <iostream>
using std::cout;

int main() {
  unsigned char x = 20;
  unsigned char y = 20;

  x *= y;

  if (x < 20) {
    // overflow?
  }
}
```

> This check can never catch an overflow.

### 00:04-00:09

> An `unsigned char` can only hold zero through two fifty-five. But here, we're multiplying twenty by twenty.

Show:

```text
20 × 20 = 400
```

> That's four hundred. It doesn't fit.

### 00:09-00:14

> So when we store the result back in `x`, it wraps around to one forty-four.

Show:

```text
400 → 144
```

### 00:14-00:18

Add the `cout` statements:

```cpp
if (x < 20) {
  cout << "overflow\n";
} else {
  cout << "no overflow\n";
}
```

> Let's print what the check actually tells us.

### 00:18-00:21

Compile and run:

```bash
g++ overflow.cpp -o overflow
./overflow
```

Output:

```text
no overflow
```

> No overflow. Because one forty-four is still bigger than twenty.

### 00:21-00:25

> The problem is that we're checking after the multiplication. By then, four hundred is already gone.

Show:

```text
x = 144
```

### 00:25-00:31

> So we need to check whether the multiplication will overflow before we actually do it.

Change the code to:

```cpp
#include <iostream>
using std::cout;

int main() {
  unsigned char x = 20;
  unsigned char y = 20;

  if (x > 255 / y) {
    cout << "overflow\n";
  } else {
    x *= y;
    cout << "no overflow\n";
  }
}
```

### 00:31-00:34

Compile and run again:

```bash
g++ overflow.cpp -o overflow
./overflow
```

Output:

```text
overflow
```

> And now we catch it before it happens.
