# Short 4: Big O Matters So Much Less Than You Think

Target runtime: 26 to 30 seconds

## Script

### 00:00-00:05

Start on `assets/opening-question.png`, filling the complete code region.

> Which is faster: scanning this matrix row by row, or column by column? 

>Both  are big O of n squared, but in my benchmark, one took waaaaaay longer than the other.

### 00:05-00:09

Cut to both functions. Keep the outer loops visible together.

> Both loops visit the same 16 million integers and perform the same number of
> additions.

### 00:09-00:13

Highlight `vector<int>& arr`, then the flat index expression.

> But this matrix is stored row by row inside one flat vector.

### 00:13-00:16

Highlight `sum_rows()` and its index expression.

> So rows first reads neighboring integers.

### 00:16-00:21

Highlight `sum_cols()` and its index expression.

> Columns first jumps 4,096 integers on each step, creating a much less
> cache-friendly access pattern.

### 00:21-00:27

Reveal `assets/hook-comparison.png`, filling the complete code region.

> On my machine, rows first took 1.7 milliseconds. Columns first took 71.1,
> about 41 times as long.

### 00:27-00:30

Keep the result visible.

> Big O describes how the work grows, not how that work interacts with the
> hardware.
