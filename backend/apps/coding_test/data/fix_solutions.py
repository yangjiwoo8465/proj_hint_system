# -*- coding: utf-8 -*-
import json
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('problems_final_output.json', encoding='utf-8-sig'))

# 수정할 솔루션 코드들
fixes = {}

# 1040: 정수 - K개의 서로 다른 숫자로 이루어진 최소 수
fixes['1040'] = '''def solve():
    line = input().split()
    N = int(line[0])
    K = int(line[1])
    while True:
        digits = set(str(N))
        if len(digits) == K:
            print(N)
            return
        N += 1
solve()
'''

# 1067: 신호 패턴 매칭
fixes['1067'] = '''import sys
input = sys.stdin.readline
n = int(input())
x = list(map(int, input().split()))
y = list(map(int, input().split()))
max_sum = 0
for shift in range(n):
    curr = sum(x[i] * y[(i + shift) % n] for i in range(n))
    max_sum = max(max_sum, curr)
print(max_sum)
'''

# 1069: 집으로
fixes['1069'] = '''import math
x, y, d, t = map(int, input().split())
dist = math.sqrt(x * x + y * y)
ans = dist
n = int(dist // d)
if n > 0:
    ans = min(ans, n * t + (dist - n * d))
ans = min(ans, (n + 1) * t)
if n == 0:
    ans = min(ans, t + (d - dist))
    ans = min(ans, 2 * t)
if ans == int(ans):
    print(f"{int(ans)}.0")
else:
    print(ans)
'''

# 1144: 싼 비용
fixes['1144'] = '''import sys
input = sys.stdin.readline
n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
best = 0
def is_connected(cells):
    if len(cells) <= 1:
        return True
    cells_set = set(cells)
    visited = {cells[0]}
    stack = [cells[0]]
    while stack:
        r, c = stack.pop()
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if (nr, nc) in cells_set and (nr, nc) not in visited:
                visited.add((nr, nc))
                stack.append((nr, nc))
    return len(visited) == len(cells)
if n * m <= 20:
    for mask in range(1, 1 << (n * m)):
        cells = [(i // m, i % m) for i in range(n * m) if mask & (1 << i)]
        if is_connected(cells):
            cost = sum(grid[r][c] for r, c in cells)
            best = min(best, cost)
print(best)
'''

# 1420: 학교 가지마!
fixes['1420'] = '''import sys
from collections import deque
input = sys.stdin.readline
n, m = map(int, input().split())
board = [input().strip() for _ in range(n)]
start = end = None
for i in range(n):
    for j in range(m):
        if board[i][j] == 'K':
            start = (i, j)
        elif board[i][j] == 'H':
            end = (i, j)
dr = [-1, 1, 0, 0]
dc = [0, 0, -1, 1]
for d in range(4):
    ni, nj = start[0] + dr[d], start[1] + dc[d]
    if (ni, nj) == end:
        print(-1)
        sys.exit()
INF = float('inf')
node_in = lambda r, c: r * m + c
node_out = lambda r, c: n * m + r * m + c
total = 2 * n * m
cap = [[0] * total for _ in range(total)]
for i in range(n):
    for j in range(m):
        if board[i][j] == '#':
            continue
        u_in, u_out = node_in(i, j), node_out(i, j)
        if (i, j) == start or (i, j) == end:
            cap[u_in][u_out] = INF
        else:
            cap[u_in][u_out] = 1
        for d in range(4):
            ni, nj = i + dr[d], j + dc[d]
            if 0 <= ni < n and 0 <= nj < m and board[ni][nj] != '#':
                cap[u_out][node_in(ni, nj)] = INF
source = node_out(start[0], start[1])
sink = node_in(end[0], end[1])
def bfs():
    parent = [-1] * total
    parent[source] = source
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in range(total):
            if parent[v] == -1 and cap[u][v] > 0:
                parent[v] = u
                if v == sink:
                    return parent
                queue.append(v)
    return None
max_flow = 0
while True:
    parent = bfs()
    if parent is None:
        break
    flow = INF
    v = sink
    while v != source:
        u = parent[v]
        flow = min(flow, cap[u][v])
        v = u
    v = sink
    while v != source:
        u = parent[v]
        cap[u][v] -= flow
        cap[v][u] += flow
        v = u
    max_flow += flow
print(max_flow)
'''

# 1463: K로 만들기
fixes['1463'] = '''from collections import deque
N, K = map(int, input().split())
if N == K:
    print(0)
else:
    visited = {N}
    queue = deque([(N, 0)])
    while queue:
        curr, steps = queue.popleft()
        nexts = [curr - 1]
        if curr % 2 == 0:
            nexts.append(curr // 2)
        if curr % 3 == 0:
            nexts.append(curr // 3)
        for nxt in nexts:
            if nxt == K:
                print(steps + 1)
                exit()
            if nxt > 0 and nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, steps + 1))
'''

# 1546: 평균 조작
fixes['1546'] = '''n = int(input())
scores = list(map(int, input().split()))
m = max(scores)
new_scores = [s / m * 100 for s in scores]
avg = sum(new_scores) / n
if avg == int(avg):
    print(f"{int(avg)}.0")
else:
    print(avg)
'''

# 1648: 격자판 채우기
fixes['1648'] = '''def solve():
    n, m = map(int, input().split())
    if (n * m) % 2 == 1:
        print(0)
        return
    if n > m:
        n, m = m, n
    dp = [[0] * (1 << n) for _ in range(m + 1)]
    dp[0][0] = 1
    def fill(col, row, mask, next_mask):
        if row == n:
            dp[col + 1][next_mask] += dp[col][mask]
            return
        if mask & (1 << row):
            fill(col, row + 1, mask, next_mask)
        else:
            fill(col, row + 1, mask, next_mask | (1 << row))
            if row + 1 < n and not (mask & (1 << (row + 1))):
                fill(col, row + 2, mask, next_mask)
    for col in range(m):
        for mask in range(1 << n):
            if dp[col][mask]:
                fill(col, 0, mask, 0)
    print(dp[m][0])
solve()
'''

# 1932: 정수 피라미드 - 역방향
fixes['1932'] = '''import sys
input = sys.stdin.readline
n = int(input())
tri = []
for _ in range(n):
    tri.append(list(map(int, input().split())))
for i in range(1, n):
    for j in range(i + 1):
        if j == 0:
            tri[i][j] += tri[i-1][j]
        elif j == i:
            tri[i][j] += tri[i-1][j-1]
        else:
            tri[i][j] += max(tri[i-1][j-1], tri[i-1][j])
print(max(tri[n-1]))
'''

# 2108: 통계학
fixes['2108'] = '''from collections import Counter
import sys
input = sys.stdin.readline
n = int(input())
nums = [int(input()) for _ in range(n)]
avg = round(sum(nums) / n)
sorted_nums = sorted(nums)
median = sorted_nums[n // 2]
cnt = Counter(nums)
max_freq = max(cnt.values())
modes = sorted([k for k, v in cnt.items() if v == max_freq])
mode = modes[1] if len(modes) > 1 else modes[0]
range_val = max(nums) - min(nums)
print(avg)
print(median)
print(mode)
print(range_val)
'''

# 2169: 로봇 탐사 - 제약 변형
fixes['2169'] = '''import sys
input = sys.stdin.readline
n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
INF = float('-inf')
dp = [[INF] * m for _ in range(n)]
dp[0][0] = grid[0][0]
for j in range(1, m):
    dp[0][j] = dp[0][j-1] + grid[0][j]
for i in range(1, n):
    left = [INF] * m
    left[0] = dp[i-1][0] + grid[i][0]
    for j in range(1, m):
        left[j] = max(dp[i-1][j], left[j-1]) + grid[i][j]
    right = [INF] * m
    right[m-1] = dp[i-1][m-1] + grid[i][m-1]
    for j in range(m-2, -1, -1):
        right[j] = max(dp[i-1][j], right[j+1]) + grid[i][j]
    for j in range(m):
        dp[i][j] = max(left[j], right[j])
print(dp[n-1][m-1])
'''

# 2252: 줄 세우기 - 위상 정렬
fixes['2252'] = '''import sys
from collections import deque
input = sys.stdin.readline
n, m = map(int, input().split())
adj = [[] for _ in range(n + 1)]
indegree = [0] * (n + 1)
for _ in range(m):
    a, b = map(int, input().split())
    adj[a].append(b)
    indegree[b] += 1
queue = deque()
for i in range(1, n + 1):
    if indegree[i] == 0:
        queue.append(i)
result = []
while queue:
    cur = queue.popleft()
    result.append(cur)
    for nxt in adj[cur]:
        indegree[nxt] -= 1
        if indegree[nxt] == 0:
            queue.append(nxt)
print(' '.join(map(str, result)))
'''

# 2316: 도시 왕복하기 2
fixes['2316'] = '''import sys
from collections import deque
input = sys.stdin.readline
n, p = map(int, input().split())
INF = float('inf')
cap = [[0] * (2 * n + 2) for _ in range(2 * n + 2)]
for v in range(1, n + 1):
    if v == 1 or v == 2:
        cap[v][v + n] = INF
    else:
        cap[v][v + n] = 1
for _ in range(p):
    a, b = map(int, input().split())
    cap[a + n][b] = 1
    cap[b + n][a] = 1
source = 1 + n
sink = 2
def bfs():
    parent = [-1] * (2 * n + 2)
    parent[source] = source
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in range(2 * n + 2):
            if parent[v] == -1 and cap[u][v] > 0:
                parent[v] = u
                if v == sink:
                    return parent
                queue.append(v)
    return None
max_flow = 0
while True:
    parent = bfs()
    if parent is None:
        break
    flow = INF
    v = sink
    while v != source:
        u = parent[v]
        flow = min(flow, cap[u][v])
        v = u
    v = sink
    while v != source:
        u = parent[v]
        cap[u][v] -= flow
        cap[v][u] += flow
        v = u
    max_flow += flow
print(max_flow)
'''

# 2803: 프로젝트 팀 구성
fixes['2803'] = '''import sys
sys.setrecursionlimit(10000)
input = sys.stdin.readline
n, m, k = map(int, input().split())
adj = [[] for _ in range(n + 1)]
for _ in range(k):
    a, b = map(int, input().split())
    adj[a].append(b)
match = [-1] * (m + 1)
def dfs(u, visited):
    for v in adj[u]:
        if visited[v]:
            continue
        visited[v] = True
        if match[v] == -1 or dfs(match[v], visited):
            match[v] = u
            return True
    return False
count = 0
for i in range(1, n + 1):
    visited = [False] * (m + 1)
    if dfs(i, visited):
        count += 1
print(count)
'''

# 4149: 큰 수 소인수분해 - 폴라드 로
fixes['4149'] = '''import random
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    witnesses = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in witnesses:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True
def pollard_rho(n):
    if n % 2 == 0:
        return 2
    x = random.randint(2, n - 1)
    y = x
    c = random.randint(1, n - 1)
    d = 1
    while d == 1:
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
        d = gcd(abs(x - y), n)
    return d
def factorize(n):
    if n == 1:
        return []
    if is_prime(n):
        return [n]
    d = n
    while d == n:
        d = pollard_rho(n)
    return factorize(d) + factorize(n // d)
n = int(input())
factors = sorted(factorize(n))
for f in factors:
    print(f)
'''

# 5820: 경주
fixes['5820'] = '''import sys
from collections import defaultdict
sys.setrecursionlimit(200000)
input = sys.stdin.readline
n, k = map(int, input().split())
adj = defaultdict(list)
for _ in range(n - 1):
    a, b, w = map(int, input().split())
    adj[a].append((b, w))
    adj[b].append((a, w))
INF = float('inf')
ans = INF
removed = [False] * n
subtree_size = [0] * n
def get_size(v, parent):
    subtree_size[v] = 1
    for u, _ in adj[v]:
        if u != parent and not removed[u]:
            subtree_size[v] += get_size(u, v)
    return subtree_size[v]
def get_centroid(v, parent, tree_size):
    for u, _ in adj[v]:
        if u != parent and not removed[u] and subtree_size[u] > tree_size // 2:
            return get_centroid(u, v, tree_size)
    return v
def solve(v):
    global ans
    tree_size = get_size(v, -1)
    centroid = get_centroid(v, -1, tree_size)
    removed[centroid] = True
    dist_to_edges = {0: 0}
    for u, w in adj[centroid]:
        if removed[u]:
            continue
        paths = []
        stack = [(u, w, 1, centroid)]
        while stack:
            node, dist, edges, par = stack.pop()
            if dist > k:
                continue
            paths.append((dist, edges))
            for next_node, next_w in adj[node]:
                if next_node != par and not removed[next_node]:
                    stack.append((next_node, dist + next_w, edges + 1, node))
        for dist, edges in paths:
            remain = k - dist
            if remain in dist_to_edges:
                ans = min(ans, edges + dist_to_edges[remain])
        for dist, edges in paths:
            if dist not in dist_to_edges or dist_to_edges[dist] > edges:
                dist_to_edges[dist] = edges
    for u, _ in adj[centroid]:
        if not removed[u]:
            solve(u)
if n == 1:
    print(0 if k == 0 else -1)
else:
    solve(0)
    print(ans if ans != INF else -1)
'''

# 9522: 직선 게임
fixes['9522'] = '''n = int(input())
if n % 2 == 1:
    print("Mirko")
else:
    print("Slavko")
'''

# 9662: 돌 게임 8
fixes['9662'] = '''import sys
input = sys.stdin.readline
n = int(input())
k = int(input())
stones = list(map(int, input().split()))
MAX = min(100001, n + 1)
sg = [0] * MAX
for i in range(1, MAX):
    reachable = set()
    for s in stones:
        if i >= s:
            reachable.add(sg[i - s])
    mex = 0
    while mex in reachable:
        mex += 1
    sg[i] = mex
period_start = 1
period_len = 1
for start in range(1, min(1000, MAX)):
    for length in range(1, min(1000, MAX - start)):
        found = True
        for i in range(min(100, MAX - start - length)):
            if sg[start + i] != sg[start + length + i]:
                found = False
                break
        if found:
            period_start = start
            period_len = length
            break
    if found:
        break
count = 0
for i in range(1, min(n + 1, period_start)):
    if sg[i] == 0:
        count += 1
if n >= period_start:
    zeros_in_period = sum(1 for i in range(period_start, min(period_start + period_len, MAX)) if sg[i] == 0)
    remaining = n - period_start + 1
    full_periods = remaining // period_len
    count += full_periods * zeros_in_period
    remainder = remaining % period_len
    for i in range(remainder):
        if period_start + i < MAX and sg[period_start + i] == 0:
            count += 1
print(count)
'''

# 11001: 제품 숙성 최적화
fixes['11001'] = '''import sys
input = sys.stdin.readline
n, d = map(int, input().split())
t = list(map(int, input().split()))
v = list(map(int, input().split()))
ans = 0
for i in range(n):
    left = max(0, i - d)
    max_v = max(v[left:i+1])
    ans = max(ans, max_v * t[i])
print(ans)
'''

# 11191: Xor Maximization
fixes['11191'] = '''import sys
input = sys.stdin.readline
n = int(input())
nums = list(map(int, input().split()))
basis = [0] * 64
for x in nums:
    cur = x
    for i in range(63, -1, -1):
        if not (cur >> i & 1):
            continue
        if basis[i]:
            cur ^= basis[i]
        else:
            basis[i] = cur
            break
ans = 0
for i in range(63, -1, -1):
    ans = max(ans, ans ^ basis[i])
print(ans)
'''

# 11402: 이항 계수 4 - 뤼카의 정리
fixes['11402'] = '''import sys
input = sys.stdin.readline
def lucas(n, k, p):
    def comb_mod_p(n, k, p):
        if k > n:
            return 0
        if k == 0 or k == n:
            return 1
        if n < p:
            num = 1
            den = 1
            for i in range(min(k, n - k)):
                num = num * (n - i) % p
                den = den * (i + 1) % p
            return num * pow(den, p - 2, p) % p
        return 0
    result = 1
    while n > 0 or k > 0:
        ni = n % p
        ki = k % p
        if ki > ni:
            return 0
        result = result * comb_mod_p(ni, ki, p) % p
        n //= p
        k //= p
    return result
n, k, m = map(int, input().split())
print(lucas(n, k, m))
'''

# 11694: 님 게임
fixes['11694'] = '''import sys
input = sys.stdin.readline
n = int(input())
xor = 0
for _ in range(n):
    xor ^= int(input())
if xor == 0:
    print("koosaga")
else:
    print("cubelover")
'''

# 11868: 님 게임 2
fixes['11868'] = '''import sys
input = sys.stdin.readline
n = int(input())
stones = list(map(int, input().split()))
xor = 0
for s in stones:
    xor ^= s
if xor == 0:
    print("cubelover")
else:
    print("koosaga")
'''

# 12015: 가장 긴 증가하는 부분 수열 2
fixes['12015'] = '''import sys
import bisect
input = sys.stdin.readline
n = int(input())
arr = list(map(int, input().split()))
dp = []
for x in arr:
    pos = bisect.bisect_left(dp, x)
    if pos == len(dp):
        dp.append(x)
    else:
        dp[pos] = x
print(len(dp))
'''

# 12852: 1로 만들기 2 - 경로 변형
fixes['12852'] = '''from collections import deque
n = int(input())
if n == 1:
    print(0)
    print(1)
else:
    dist = {1: 0}
    parent = {1: -1}
    queue = deque([1])
    while queue:
        cur = queue.popleft()
        if cur == n:
            break
        nexts = [cur + 1]
        if cur * 2 <= n + 1:
            nexts.append(cur * 2)
        if cur * 3 <= n + 1:
            nexts.append(cur * 3)
        for nxt in nexts:
            if nxt not in dist and nxt <= n:
                dist[nxt] = dist[cur] + 1
                parent[nxt] = cur
                queue.append(nxt)
    path = []
    cur = n
    while cur != -1:
        path.append(cur)
        cur = parent.get(cur, -1)
    print(len(path) - 1)
    print(' '.join(map(str, path)))
'''

# 13018: 작업 배정 최적화
fixes['13018'] = '''import sys
import heapq
input = sys.stdin.readline
n = int(input())
tasks = []
for i in range(n):
    d, t = map(int, input().split())
    tasks.append((d, t, i))
tasks.sort()
total_time = 0
pq = []
for d, t, i in tasks:
    heapq.heappush(pq, -t)
    total_time += t
    while total_time > d and pq:
        removed = -heapq.heappop(pq)
        total_time -= removed
if len(pq) == n:
    print("YES")
else:
    print("NO")
'''

# 13034: 다각형 게임
fixes['13034'] = '''import sys
input = sys.stdin.readline
n = int(input())
sg = [0] * (n + 1)
for i in range(2, n + 1):
    reachable = set()
    for j in range(2, i - 1):
        reachable.add(sg[j] ^ sg[i - j])
    mex = 0
    while mex in reachable:
        mex += 1
    sg[i] = mex
if sg[n] == 0:
    print(2)
else:
    print(1)
'''

# 13332: Project Team
fixes['13332'] = '''import sys
sys.setrecursionlimit(10000)
input = sys.stdin.readline
n, m, k = map(int, input().split())
if k == 0:
    print(-1 if m > 0 else 0)
else:
    adj = [[] for _ in range(n + 1)]
    for _ in range(k):
        a, b = map(int, input().split())
        adj[a].append(b)
    match = [-1] * (m + 1)
    def dfs(u, visited):
        for v in adj[u]:
            if visited[v]:
                continue
            visited[v] = True
            if match[v] == -1 or dfs(match[v], visited):
                match[v] = u
                return True
        return False
    count = 0
    for i in range(1, n + 1):
        visited = [False] * (m + 1)
        if dfs(i, visited):
            count += 1
    if count == m:
        print(count)
    else:
        print(-1)
'''

# 13448: SW 역량 테스트
fixes['13448'] = '''import sys
input = sys.stdin.readline
n, k = map(int, input().split())
problems = []
for _ in range(n):
    line = input().split()
    t = int(line[0])
    p = int(line[1])
    problems.append((t, p))
dp = [0] * (k + 1)
for t, p in problems:
    for j in range(k, t - 1, -1):
        dp[j] = max(dp[j], dp[j - t] + p)
print(dp[k])
'''

# 13976: 타일 채우기 2 - 큰 N
fixes['13976'] = '''import sys
input = sys.stdin.readline
MOD = 1000000007
def mat_mult(A, B, mod):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C
def mat_pow(M, p, mod):
    n = len(M)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    while p:
        if p & 1:
            result = mat_mult(result, M, mod)
        M = mat_mult(M, M, mod)
        p >>= 1
    return result
n = int(input())
if n % 2 == 1:
    print(0)
elif n == 0:
    print(1)
elif n == 2:
    print(3)
else:
    M = [[4, -1], [1, 0]]
    result = mat_pow(M, n // 2 - 1, MOD)
    ans = (result[0][0] * 3 + result[0][1]) % MOD
    print(ans)
'''

# 14636: Money 반복문 Nothing
fixes['14636'] = '''import sys
input = sys.stdin.readline
n = int(input())
count = 0
for _ in range(n):
    line = input().strip()
    if line == "pocket":
        count = 0
    elif line == "check":
        print(count)
    else:
        count += int(line)
'''

# 14750: Jerry and Tom
fixes['14750'] = '''import sys
sys.setrecursionlimit(10000)
input = sys.stdin.readline
def ccw(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
def can_see(hole, mouse, walls):
    hx, hy = hole
    mx, my = mouse
    for wall in walls:
        x1, y1, x2, y2 = wall
        d1 = ccw((hx, hy), (mx, my), (x1, y1))
        d2 = ccw((hx, hy), (mx, my), (x2, y2))
        d3 = ccw((x1, y1), (x2, y2), (hx, hy))
        d4 = ccw((x1, y1), (x2, y2), (mx, my))
        if d1 * d2 < 0 and d3 * d4 < 0:
            return False
    return True
n, m, h = map(int, input().split())
walls = []
for _ in range(n):
    x1, y1, x2, y2 = map(int, input().split())
    walls.append((x1, y1, x2, y2))
holes = []
for _ in range(h):
    x, y = map(int, input().split())
    holes.append((x, y))
mice = []
for _ in range(m):
    x, y = map(int, input().split())
    mice.append((x, y))
adj = [[] for _ in range(m)]
for i, mouse in enumerate(mice):
    for j, hole in enumerate(holes):
        if can_see(hole, mouse, walls):
            adj[i].append(j)
match = [-1] * h
def dfs(u, visited):
    for v in adj[u]:
        if visited[v]:
            continue
        visited[v] = True
        if match[v] == -1 or dfs(match[v], visited):
            match[v] = u
            return True
    return False
count = 0
for i in range(m):
    visited = [False] * h
    if dfs(i, visited):
        count += 1
if count == m:
    print("Possible")
else:
    print("Impossible")
'''

# 15439: 베라의 패션 - 조합 변형
fixes['15439'] = '''n = int(input())
print(n * n - n)
'''

# 16229: 반복 패턴
fixes['16229'] = '''import sys
input = sys.stdin.readline
n, k = map(int, input().split())
s = input().strip()
if n == 0:
    print(0)
else:
    ans = 0
    for period in range(1, n + 1):
        mismatch = 0
        valid = True
        for i in range(n):
            if s[i] != s[i % period]:
                mismatch += 1
                if mismatch > k:
                    valid = False
                    break
        if valid:
            ans = period
            break
    print(ans)
'''

# 16883: 대각 게임
fixes['16883'] = '''n, m = map(int, input().split())
xor = 0
for i in range(n):
    row = list(map(int, input().split()))
    for j, x in enumerate(row):
        if x == 1:
            xor ^= (i + 1) ^ (j + 1)
if xor == 0:
    print("cubelover")
else:
    print("koosaga")
'''

# 17131: 여우가 점보섬에 올라온 이유
fixes['17131'] = '''import sys
from collections import defaultdict
input = sys.stdin.readline
MOD = 1000000007
n = int(input())
points = []
for _ in range(n):
    x, y = map(int, input().split())
    points.append((x, y))
by_y = defaultdict(list)
for x, y in points:
    by_y[y].append(x)
ys = sorted(by_y.keys(), reverse=True)
all_x = sorted(set(x for x, y in points))
x_to_idx = {x: i for i, x in enumerate(all_x)}
size = len(all_x)
left_tree = [0] * (2 * size)
right_tree = [0] * (2 * size)
def update(tree, idx, delta):
    idx += size
    tree[idx] += delta
    while idx > 1:
        idx //= 2
        tree[idx] = tree[2 * idx] + tree[2 * idx + 1]
def query(tree, l, r):
    res = 0
    l += size
    r += size
    while l < r:
        if l & 1:
            res += tree[l]
            l += 1
        if r & 1:
            r -= 1
            res += tree[r]
        l //= 2
        r //= 2
    return res
ans = 0
for y in ys:
    xs = by_y[y]
    for x in xs:
        idx = x_to_idx[x]
        left = query(left_tree, 0, idx)
        right = query(right_tree, idx + 1, size)
        ans = (ans + left * right) % MOD
    for x in xs:
        idx = x_to_idx[x]
        update(left_tree, idx, 1)
        update(right_tree, idx, 1)
print(ans)
'''

# 17409: 성과 트렌드 분석
fixes['17409'] = '''import sys
input = sys.stdin.readline
MOD = 1000000007
n = int(input())
arr = list(map(int, input().split()))
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    def update(self, i, delta):
        while i <= self.n:
            self.tree[i] = (self.tree[i] + delta) % MOD
            i += i & (-i)
    def query(self, i):
        s = 0
        while i > 0:
            s = (s + self.tree[i]) % MOD
            i -= i & (-i)
        return s
sorted_arr = sorted(set(arr))
compress = {v: i + 1 for i, v in enumerate(sorted_arr)}
size = len(sorted_arr)
bit = BIT(size)
ans = 0
for x in arr:
    idx = compress[x]
    cnt = bit.query(idx - 1)
    bit.update(idx, cnt + 1)
    ans = (ans + cnt + 1) % MOD
print(ans)
'''

# 17435: 합성함수와 쿼리
fixes['17435'] = '''import sys
input = sys.stdin.readline
LOG = 20
m = int(input())
f = [0] + list(map(int, input().split()))
sparse = [[0] * (m + 1) for _ in range(LOG)]
sparse[0] = f[:]
for j in range(1, LOG):
    for i in range(1, m + 1):
        sparse[j][i] = sparse[j-1][sparse[j-1][i]]
q = int(input())
for _ in range(q):
    n, x = map(int, input().split())
    for j in range(LOG):
        if n & (1 << j):
            x = sparse[j][x]
    print(x)
'''

# 20149: 케이블 교차점 찾기
fixes['20149'] = '''import sys
input = sys.stdin.readline
def ccw(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
def intersects(p1, p2, p3, p4):
    d1 = ccw(p1, p2, p3)
    d2 = ccw(p1, p2, p4)
    d3 = ccw(p3, p4, p1)
    d4 = ccw(p3, p4, p2)
    if d1 * d2 < 0 and d3 * d4 < 0:
        return True
    if d1 == 0 and min(p1[0], p2[0]) <= p3[0] <= max(p1[0], p2[0]) and min(p1[1], p2[1]) <= p3[1] <= max(p1[1], p2[1]):
        return True
    if d2 == 0 and min(p1[0], p2[0]) <= p4[0] <= max(p1[0], p2[0]) and min(p1[1], p2[1]) <= p4[1] <= max(p1[1], p2[1]):
        return True
    if d3 == 0 and min(p3[0], p4[0]) <= p1[0] <= max(p3[0], p4[0]) and min(p3[1], p4[1]) <= p1[1] <= max(p3[1], p4[1]):
        return True
    if d4 == 0 and min(p3[0], p4[0]) <= p2[0] <= max(p3[0], p4[0]) and min(p3[1], p4[1]) <= p2[1] <= max(p3[1], p4[1]):
        return True
    return False
def get_intersection(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
    ix = x1 + t * (x2 - x1)
    iy = y1 + t * (y2 - y1)
    if ix == int(ix) and iy == int(iy):
        return (int(ix), int(iy))
    return (ix, iy)
x1, y1, x2, y2 = map(int, input().split())
x3, y3, x4, y4 = map(int, input().split())
p1, p2 = (x1, y1), (x2, y2)
p3, p4 = (x3, y3), (x4, y4)
if intersects(p1, p2, p3, p4):
    print(1)
    pt = get_intersection(p1, p2, p3, p4)
    if pt:
        print(pt[0], pt[1])
else:
    print(0)
'''

# 20176: Needle
fixes['20176'] = '''import sys
from collections import defaultdict
from math import gcd
input = sys.stdin.readline
n = int(input())
points = []
for _ in range(n):
    x, y = map(int, input().split())
    points.append((x, y))
count = 0
for i in range(n):
    slopes = defaultdict(int)
    for j in range(n):
        if i == j:
            continue
        dx = points[j][0] - points[i][0]
        dy = points[j][1] - points[i][1]
        g = gcd(abs(dx), abs(dy))
        dx //= g
        dy //= g
        if dx < 0 or (dx == 0 and dy < 0):
            dx, dy = -dx, -dy
        slopes[(dx, dy)] += 1
    for cnt in slopes.values():
        count += cnt * (cnt - 1) // 2
print(count)
'''

# 20412: 추첨상 사수 대작전!
fixes['20412'] = '''import sys
input = sys.stdin.readline
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = extended_gcd(b, a % b)
    return g, y, x - (a // b) * y
def mod_inverse(a, m):
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        return None
    return x % m
m, seed, x1, x2 = map(int, input().split())
diff1 = (x1 - seed) % m
diff2 = (x2 - x1) % m
if diff1 == 0:
    print(0, x1)
else:
    inv = mod_inverse(diff1, m)
    if inv is None:
        print(0, 0)
    else:
        a = (diff2 * inv) % m
        c = (x1 - a * seed) % m
        print(a, c)
'''

# 20670: 미스테리 싸인
fixes['20670'] = '''import sys
input = sys.stdin.readline
def ccw(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
def point_in_convex(poly, p):
    n = len(poly)
    if n < 3:
        return False
    sign = None
    for i in range(n):
        d = ccw(poly[i], poly[(i + 1) % n], p)
        if d == 0:
            continue
        if sign is None:
            sign = d > 0
        elif (d > 0) != sign:
            return False
    return True
n, m, k = map(int, input().split())
outer = []
for _ in range(n):
    x, y = map(int, input().split())
    outer.append((x, y))
inner = []
for _ in range(m):
    x, y = map(int, input().split())
    inner.append((x, y))
signatures = []
for _ in range(k):
    x, y = map(int, input().split())
    signatures.append((x, y))
valid_count = 0
for sig in signatures:
    in_inner = point_in_convex(inner, sig)
    if in_inner:
        valid_count += 1
print(valid_count)
'''

# 20944: 팰린드롬 척화비
fixes['20944'] = '''n = int(input())
print('a' * n)
'''

# 22029: 철도
fixes['22029'] = '''import sys
from collections import defaultdict
input = sys.stdin.readline
n, m = map(int, input().split())
adj = defaultdict(list)
degree = [0] * (n + 1)
for _ in range(m):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)
    degree[a] += 1
    degree[b] += 1
odd = [i for i in range(1, n + 1) if degree[i] % 2 == 1]
if len(odd) == 0:
    print(0)
elif len(odd) == 2:
    print(1)
    print(odd[0], odd[1])
else:
    k = len(odd) // 2
    print(k)
    for i in range(k):
        print(odd[2 * i], odd[2 * i + 1])
'''

# 23381: Gyrating Glyphs (인터랙티브)
fixes['23381'] = '''import sys
n = int(input())
sys.stdout.write("? " + " ".join(["1"] * n) + "\\n")
sys.stdout.flush()
first = input().strip()
sys.stdout.write("? " + " ".join([str(i) for i in range(n)]) + "\\n")
sys.stdout.flush()
second = input().strip()
result = []
for i in range(n):
    if first == second:
        result.append('+')
    else:
        result.append('x')
sys.stdout.write("! " + "".join(result) + "\\n")
sys.stdout.flush()
'''

# 23656: Jack and Jill
fixes['23656'] = '''import sys
input = sys.stdin.readline
t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    jack_pos = 0
    jill_pos = 0
    for i in range(n):
        jack_pos += a[i]
        jill_pos += b[i]
        if jack_pos > jill_pos:
            print(">")
        elif jack_pos < jill_pos:
            print("<")
        else:
            print("=")
'''

# 25051: 천체 관측
fixes['25051'] = '''import sys
input = sys.stdin.readline
n, k = map(int, input().split())
stars = []
for _ in range(n):
    x, y = map(int, input().split())
    stars.append((x, y))
xs = sorted(set(x for x, y in stars))
ys = sorted(set(y for x, y in stars))
count = 0
for i1, x1 in enumerate(xs):
    for i2, x2 in enumerate(xs[i1:], i1):
        for j1, y1 in enumerate(ys):
            for j2, y2 in enumerate(ys[j1:], j1):
                cnt = sum(1 for sx, sy in stars if x1 <= sx <= x2 and y1 <= sy <= y2)
                if cnt <= k:
                    count += 1
print(count)
'''

# 25184: 동가수열 구하기
fixes['25184'] = '''import sys
input = sys.stdin.readline
n = int(input())
b = list(map(int, input().split()))
for a0 in range(1, n + 1):
    a = [a0]
    valid = True
    used = {a0}
    for i in range(n - 1):
        next_a = b[i] - a[-1]
        if next_a < 1 or next_a > n or next_a in used:
            valid = False
            break
        a.append(next_a)
        used.add(next_a)
    if valid:
        print(' '.join(map(str, a)))
        break
'''

# 25672: 짝수와 홀수 조합
fixes['25672'] = '''import sys
input = sys.stdin.readline
n = int(input())
arr = list(map(int, input().split()))
evens = [x for x in arr if x % 2 == 0]
odds = [x for x in arr if x % 2 == 1]
print(len(evens), len(odds))
'''

# 27312: 운영진에게 설정 짜기는 어려워 (인터랙티브)
fixes['27312'] = '''import sys
n, m = map(int, input().split())
difficulties = []
for i in range(1, n + 1):
    sys.stdout.write(f"? 1 {i}\\n")
    sys.stdout.flush()
    d = int(input())
    difficulties.append(d)
sys.stdout.write("! " + " ".join(map(str, difficulties)) + "\\n")
sys.stdout.flush()
'''

# 28065: SW 수열 구하기
fixes['28065'] = '''import sys
input = sys.stdin.readline
n = int(input())
b = list(map(int, input().split()))
for a0 in range(1, n + 1):
    a = [a0]
    valid = True
    used = {a0}
    for i in range(n - 1):
        next_a = b[i] - a[-1]
        if next_a < 1 or next_a > n or next_a in used:
            valid = False
            break
        a.append(next_a)
        used.add(next_a)
    if valid:
        print(' '.join(map(str, a)))
        break
'''

# 28121: 산책과 쿼리
fixes['28121'] = '''import sys
input = sys.stdin.readline
n, m, q = map(int, input().split())
adj = [[0] * n for _ in range(n)]
for _ in range(m):
    u, v = map(int, input().split())
    adj[u - 1][v - 1] = 1
    adj[v - 1][u - 1] = 1
def mat_mult(A, B):
    n = len(A)
    m = len(B[0])
    k = len(B)
    C = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for p in range(k):
                C[i][j] += A[i][p] * B[p][j]
    return C
def mat_pow(M, p):
    n = len(M)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    while p:
        if p & 1:
            result = mat_mult(result, M)
        M = mat_mult(M, M)
        p >>= 1
    return result
for _ in range(q):
    a, b, k = map(int, input().split())
    power = mat_pow(adj, k)
    print(power[a - 1][b - 1])
'''

# 28122: 아이템
fixes['28122'] = '''import sys
input = sys.stdin.readline
n, m = map(int, input().split())
prices = list(map(int, input().split()))
dp = [0] * (m + 1)
for p in prices:
    for j in range(m, p - 1, -1):
        dp[j] = max(dp[j], dp[j - p] + 1)
print(dp[m])
'''

# 31836: 피보나치 기념품
fixes['31836'] = '''import sys
input = sys.stdin.readline
n = int(input())
fib = [1, 1]
while fib[-1] < n:
    fib.append(fib[-1] + fib[-2])
result = []
remaining = n
for f in reversed(fib):
    if f <= remaining:
        result.append(f)
        remaining -= f
    if remaining == 0:
        break
print(len(result))
print(' '.join(map(str, result)))
'''

# 32395: 네트워크 사각형 패턴
fixes['32395'] = '''import sys
from collections import defaultdict
input = sys.stdin.readline
n, m = map(int, input().split())
adj = defaultdict(set)
for _ in range(m):
    a, b = map(int, input().split())
    adj[a].add(b)
    adj[b].add(a)
count = 0
nodes = list(adj.keys())
for i, u in enumerate(nodes):
    for j, v in enumerate(nodes):
        if i >= j:
            continue
        common = len(adj[u] & adj[v])
        count += common * (common - 1) // 2
print(count)
'''

# 33918: 맛있는 스콘 만들기
fixes['33918'] = '''import sys
input = sys.stdin.readline
n = int(input())
scones = []
for _ in range(n):
    a, b = map(int, input().split())
    scones.append((a, b))
best = float('-inf')
for temp in range(-10000, 10001):
    total = sum(a * temp + b for a, b in scones)
    best = max(best, total)
print(best)
'''

# 33983: 리스트 탐색 - 선형
fixes['33983'] = '''import sys
input = sys.stdin.readline
n, target = map(int, input().split())
arr = list(map(int, input().split()))
result = -1
for i in range(n):
    if arr[i] == target:
        result = i
        break
print(result)
'''

# 33987: 선택 정렬
fixes['33987'] = '''import sys
input = sys.stdin.readline
n, k = map(int, input().split())
arr = list(map(int, input().split()))
for step in range(min(k, n - 1)):
    min_idx = step
    for j in range(step + 1, n):
        if arr[j] < arr[min_idx]:
            min_idx = j
    arr[step], arr[min_idx] = arr[min_idx], arr[step]
print(' '.join(map(str, arr)))
'''

# 33994: 회문 판별
fixes['33994'] = '''s = input().strip()
if s == s[::-1]:
    print("YES")
else:
    print("NO")
'''

# 34027: 재귀 - 하노이
fixes['34027'] = '''n = int(input())
print(2 ** n - 1)
'''

# 34046: 투포인터 - 세 수의 합
fixes['34046'] = '''import sys
input = sys.stdin.readline
n, target = map(int, input().split())
arr = list(map(int, input().split()))
arr.sort()
count = 0
for i in range(n - 2):
    left = i + 1
    right = n - 1
    while left < right:
        s = arr[i] + arr[left] + arr[right]
        if s == target:
            count += 1
            left += 1
            right -= 1
        elif s < target:
            left += 1
        else:
            right -= 1
print(count)
'''

# 34066: 그리디 기본 - 동전 교환
fixes['34066'] = '''import sys
input = sys.stdin.readline
n, amount = map(int, input().split())
coins = list(map(int, input().split()))
coins.sort(reverse=True)
count = 0
for coin in coins:
    count += amount // coin
    amount %= coin
print(count)
'''

# 34069: 그리디 기본 - 분수 배낭
fixes['34069'] = '''import sys
input = sys.stdin.readline
n, capacity = map(int, input().split())
items = []
for _ in range(n):
    w, v = map(int, input().split())
    items.append((v / w, w, v))
items.sort(reverse=True)
total = 0
for ratio, w, v in items:
    if capacity >= w:
        total += v
        capacity -= w
    else:
        total += ratio * capacity
        break
print(f"{total:.2f}")
'''

# 34084: 해시맵 - 두 합
fixes['34084'] = '''import sys
input = sys.stdin.readline
n, target = map(int, input().split())
arr = list(map(int, input().split()))
seen = {}
for i, x in enumerate(arr):
    if target - x in seen:
        print(seen[target - x], i)
        exit()
    seen[x] = i
print(-1, -1)
'''

# 34093: 계단 오르기 1
fixes['34093'] = '''import sys
input = sys.stdin.readline
n = int(input())
stairs = [0] + [int(input()) for _ in range(n)]
if n == 1:
    print(stairs[1])
elif n == 2:
    print(stairs[1] + stairs[2])
else:
    dp = [[0] * 3 for _ in range(n + 1)]
    dp[1][1] = stairs[1]
    dp[2][1] = stairs[2]
    dp[2][2] = stairs[1] + stairs[2]
    for i in range(3, n + 1):
        dp[i][1] = max(dp[i-2][1], dp[i-2][2]) + stairs[i]
        dp[i][2] = dp[i-1][1] + stairs[i]
    print(max(dp[n][1], dp[n][2]))
'''

# 34123: 경로 존재 여부
fixes['34123'] = '''import sys
from collections import deque
input = sys.stdin.readline
n, m = map(int, input().split())
adj = [[] for _ in range(n + 1)]
for _ in range(m):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)
start, end = map(int, input().split())
visited = [False] * (n + 1)
visited[start] = True
queue = deque([start])
while queue:
    cur = queue.popleft()
    if cur == end:
        print(1)
        exit()
    for nxt in adj[cur]:
        if not visited[nxt]:
            visited[nxt] = True
            queue.append(nxt)
print(-1)
'''

# 34645: 온라인 - 스키 대여
fixes['34645'] = '''import sys
input = sys.stdin.readline
n, buy_cost = map(int, input().split())
rent_cost = int(input())
days = list(map(int, input().split()))
online_cost = 0
rented_total = 0
for d in days:
    if d == 1:
        if rented_total < buy_cost:
            online_cost += rent_cost
            rented_total += rent_cost
ski_days = sum(days)
optimal = min(buy_cost, ski_days * rent_cost)
print(online_cost)
print(f"{online_cost / optimal:.3f}")
'''

# 34646: 근사 - TSP 근사
fixes['34646'] = '''import sys
import math
input = sys.stdin.readline
n = int(input())
points = []
for i in range(n):
    x, y = map(int, input().split())
    points.append((x, y))
def dist(i, j):
    dx = points[i][0] - points[j][0]
    dy = points[i][1] - points[j][1]
    return math.sqrt(dx * dx + dy * dy)
visited = [False] * n
path = [0]
visited[0] = True
total = 0
for _ in range(n - 1):
    cur = path[-1]
    nearest = -1
    nearest_dist = float('inf')
    for j in range(n):
        if not visited[j]:
            d = dist(cur, j)
            if d < nearest_dist:
                nearest_dist = d
                nearest = j
    path.append(nearest)
    visited[nearest] = True
    total += nearest_dist
total += dist(path[-1], 0)
path.append(0)
print(int(total))
print(' '.join(map(str, path)))
'''

# 34647: 온라인 - 페이징
fixes['34647'] = '''import sys
from collections import OrderedDict
input = sys.stdin.readline
k, n = map(int, input().split())
requests = list(map(int, input().split()))
cache = OrderedDict()
faults = 0
for page in requests:
    if page in cache:
        cache.move_to_end(page)
    else:
        faults += 1
        if len(cache) >= k:
            cache.popitem(last=False)
        cache[page] = True
print(faults)
'''

# 34654: 근사 - 정점 덮개
fixes['34654'] = '''import sys
input = sys.stdin.readline
n, m = map(int, input().split())
edges = []
for _ in range(m):
    a, b = map(int, input().split())
    edges.append((a, b))
covered = set()
vertex_cover = set()
for a, b in edges:
    if a not in covered and b not in covered:
        vertex_cover.add(a)
        vertex_cover.add(b)
        covered.add(a)
        covered.add(b)
result = sorted(vertex_cover)
print(len(result))
print(' '.join(map(str, result)))
'''

# 34703: 두 수 합 개수 세기
fixes['34703'] = '''import sys
from collections import Counter
input = sys.stdin.readline
n, target = map(int, input().split())
arr = list(map(int, input().split()))
cnt = Counter(arr)
count = 0
for x in arr:
    y = target - x
    if y in cnt:
        count += cnt[y]
        if x == y:
            count -= 1
print(count // 2)
'''

# 34977: 거듭제곱 빠르게 계산하기
fixes['34977'] = '''import sys
input = sys.stdin.readline
a, b, m = map(int, input().split())
print(pow(a, b, m))
'''

# 36016: 알파벳/숫자만 남기기
fixes['36016'] = '''s = input().strip()
result = ''.join(c for c in s if c.isalnum())
print(len(result))
'''

# 36020: 배열 요소 존재 확인
fixes['36020'] = '''import sys
input = sys.stdin.readline
n = int(input())
arr = list(map(int, input().split()))
target = int(input())
if target in arr:
    print("YES")
else:
    print("NO")
'''

# 11710: Cost Performance 플로우
fixes['11710'] = '''import sys
from collections import deque
input = sys.stdin.readline
def mcmf(n, source, sink, adj, cap, cost):
    INF = float('inf')
    result_flow = 0
    result_cost = 0
    while True:
        dist = [INF] * n
        parent = [-1] * n
        in_queue = [False] * n
        dist[source] = 0
        queue = deque([source])
        in_queue[source] = True
        while queue:
            u = queue.popleft()
            in_queue[u] = False
            for v in adj[u]:
                if cap[u][v] > 0 and dist[u] + cost[u][v] < dist[v]:
                    dist[v] = dist[u] + cost[u][v]
                    parent[v] = u
                    if not in_queue[v]:
                        queue.append(v)
                        in_queue[v] = True
        if dist[sink] == INF:
            break
        flow = INF
        v = sink
        while v != source:
            u = parent[v]
            flow = min(flow, cap[u][v])
            v = u
        v = sink
        while v != source:
            u = parent[v]
            cap[u][v] -= flow
            cap[v][u] += flow
            v = u
        result_flow += flow
        result_cost += flow * dist[sink]
    return result_flow, result_cost
n, m = map(int, input().split())
source = 0
sink = n - 1
adj = [[] for _ in range(n)]
cap = [[0] * n for _ in range(n)]
cost = [[0] * n for _ in range(n)]
for _ in range(m):
    u, v, c, w = map(int, input().split())
    u -= 1
    v -= 1
    adj[u].append(v)
    adj[v].append(u)
    cap[u][v] = c
    cost[u][v] = w
    cost[v][u] = -w
flow, total_cost = mcmf(n, source, sink, adj, cap, cost)
print(f"{total_cost}/{flow}" if flow > 0 else "0/0")
'''

# 11717: Wall Making Game
fixes['11717'] = '''import sys
from collections import deque
input = sys.stdin.readline
n, m = map(int, input().split())
grid = []
for _ in range(n):
    grid.append(input().strip())
visited = [[False] * m for _ in range(n)]
xor = 0
for i in range(n):
    for j in range(m):
        if grid[i][j] == '.' and not visited[i][j]:
            queue = deque([(i, j)])
            visited[i][j] = True
            size = 0
            while queue:
                x, y = queue.popleft()
                size += 1
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] == '.' and not visited[nx][ny]:
                        visited[nx][ny] = True
                        queue.append((nx, ny))
            xor ^= size
if xor == 0:
    print("Second")
else:
    print("First")
'''

# 데이터 수정
fixed_count = 0
for p in data:
    pid = p.get('problem_id', '')
    if pid in fixes:
        p['solutions'][0]['solution_code'] = fixes[pid]
        fixed_count += 1
        print(f'Fixed: {pid}')

print(f'\nTotal fixed: {fixed_count}')

# 저장
with open('problems_final_output.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Saved to problems_final_output.json')
