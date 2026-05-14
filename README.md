# The Torchbearer

**Student Name:** Zakaria Abdullahi
**Student ID:** 820007650
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  A single shortest-path from S gives the cheapest path to each individual node, but the problem requires
  visiting all relics/nodes and then reaching the exit, meaning we need a full route.

- **What decision remains after all inter-location costs are known:**
  Deciding in which order to visist the relics/nodes. Traversing in different orders produce different results 
  and we want the minimum overall cost.

- **Why this requires a search over orders (one sentence):**
  Because the total cost depends on the sequence of relic/node visits, we must explore different possible orders
  to determine the minimum overall cost.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|---|---|
| _S_ | _The route begins at S, so we need the shortest path from S to all relavent nodes_ |
| _relic chambers_| _After visiting each relic, the next step starts at that relic to others and the exit_ | 

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer |
|---|---|
| Data structure name | Nested dictionary |
| What the keys represent | Outer key represents source node u, inner key represents destination node v |
| What the values represent | Shortest-path distance from u to v|
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Dictionaries use hashing, allowing for constant time key access|

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** _k+1_
- **Cost per run:** _O((V + E) log V)_
- **Total complexity:** _O((k + 1)(V + E) log V)_
- **Justification (one line):** _Run Dijkstra once from each source (spawn + each relic), and each costs O((V + E) log V)_

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  _For nodes already finalized, their stored distance is the true cheapest distance from the source._

- **For nodes not yet finalized (not in S):**
  _For nodes not yet finalized, their stored distance is the current best known distance using paths that go through finalized nodes first._

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  _The source starts with distance 0 becuase it costs nothing to reach itself. All other nodes start at infinity because no path has been found yet._

- **Maintenance : why finalizing the min-dist node is always correct:**
  _Dijkstra chooses the unfinished node with the smallest known distance. Since all edge weights are nonnegative, any alternate path through another unfinished node cannot be cheaper later._

- **Termination : what the invariant guarantees when the algorithm ends:**
  _When the algorithm finishes, every reachable finalized node has it's true shortest-path distance from the source. Unreachable nodes remain at infinity._

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

_Correct Dijkstra distances make the route planner compare relic orders using true minimum travel costs, so it's final route decision is based on those correct numbers._

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** _Greedy can pick the nearest next relic, but the local choice may force a more expensive path later._
- **Counter-example setup:** _Consider our graph example with source node S, exit node T, and relic nodes B,C, D. S->B=1, S->C=2, S->D=2, B->D=1, D->C=1, C->T=1, C->B=1, D->T=100._
- **What greedy picks:** _Greedy starts at S and picks B first because S->B has a cost of 1 which is cheaper than our other options, S->C and S->D, which both have a cost of 2. It can then go from B->D->C->T for a total cost of 4._
- **What optimal picks:** _The optimal route may opt to choose an order based on the whole remaining route, not just the nearest next relic._
- **Why greedy loses:** _Greedy only minimizes the next step, while the problem needs the minimum total route across all relics and our exit._

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- _The algorithm must explore each possible order of relic vists because the total fuel cost depends on the routes order._

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_node | node | Node where the route is currently at. |
| Relics already collected | collected_relics | set[node] | The relic nodes already visited on the route. |
| Fuel cost so far | fuel_cost | float | Total distance/fuel used so far |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | set |
| Operation: check if relic already collected | Time complexity: O(1) |
| Operation: mark a relic as collected | Time complexity: O(1) |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) |
| Why this structure fits | A set lets us quickly if a relic is already in the set, add relics, and remove relics while exploring other routes. |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _k!_
- **Why:** _In the worst case, the algorithm may need to try every possible ordering of k relics._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Backtracking refrence: https://medium.com/@albertoarrigoni/the-choose-explore-unchoose-pattern-for-backtracking-c0a519a3c2e8_
