# -*- coding: utf-8 -*-
import json
import subprocess
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('problems_final_output.json', encoding='utf-8-sig'))

# 수정할 솔루션 코드들
fixes = {}

# 1040: 정수 - example 0의 output이 잘못됨 (47 1의 결과는 55가 맞음)
# example output을 수정하거나, 문제 해석을 다시 해야함
# description: "N보다 크거나 같은 수 중에, K개의 서로 다른 숫자로 이루어진 수"
# N=47, K=1 -> 55 (한 숫자로만 이루어진 47 이상의 수)
# 하지만 output이 1이면... K개의 숫자를 사용해서 N보다 크거나 같은 수를 만드는 문제가 아닐 수 있음
# example 0 output=1은 이상함. skip this fix

# 1067: 신호 패턴 매칭 - 순환 이동 정의 재확인
# "순환 이동이란 마지막 값을 제거하고 그 값을 맨 앞으로 삽입하는 것"
# {1,2,3} -> {3,1,2} (마지막 3을 앞으로)
fixes['1067'] = '''import sys
input = sys.stdin.readline
n = int(input())
x = list(map(int, input().split()))
y = list(map(int, input().split()))
max_sum = 0
# X를 순환 이동 (마지막을 앞으로)
for shift in range(n):
    # shift번 순환 이동한 X
    curr = sum(x[(i - shift) % n] * y[i] for i in range(n))
    max_sum = max(max_sum, curr)
# Y를 순환 이동
for shift in range(n):
    curr = sum(x[i] * y[(i - shift) % n] for i in range(n))
    max_sum = max(max_sum, curr)
print(max_sum)
'''

# 1069: 집으로 - 좀 더 정확한 로직
fixes['1069'] = '''import math
x, y, d, t = map(int, input().split())
dist = math.sqrt(x * x + y * y)
ans = dist  # 걷기만
n = int(dist / d)
# n번 점프 + 남은 거리 걷기
if n >= 1:
    ans = min(ans, n * t + (dist - n * d))
# n+1번 점프 (더 가서 돌아오기)
ans = min(ans, (n + 1) * t)
# 거리가 d보다 작을 때
if dist < d:
    # 점프 1번 후 걸어서 돌아오기
    ans = min(ans, t + (d - dist))
    # 점프 2번 (반대방향)
    ans = min(ans, 2 * t)
print(ans)
'''

# 1144: 싼 비용 - 더 정확한 구현
fixes['1144'] = '''import sys
input = sys.stdin.readline
n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
best = 0  # 빈 집합

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

# 모든 부분집합 검사
for mask in range(1, 1 << (n * m)):
    cells = [(i // m, i % m) for i in range(n * m) if mask & (1 << i)]
    if is_connected(cells):
        cost = sum(grid[r][c] for r, c in cells)
        best = min(best, cost)
print(best)
'''

# 1463: K로 만들기 - N에서 K로 가는 BFS (N > K)
fixes['1463'] = '''from collections import deque
N, K = map(int, input().split())
if N == K:
    print(0)
elif N < K:
    print(K - N)  # K가 더 크면 1씩 더하기만 가능? 아니면 역방향?
else:
    # N -> K로 가기 (N을 줄이는 연산)
    dp = {N: 0}
    queue = deque([N])
    while queue:
        curr = queue.popleft()
        if curr == K:
            print(dp[curr])
            break
        for nxt in [curr - 1, curr // 2 if curr % 2 == 0 else None, curr // 3 if curr % 3 == 0 else None]:
            if nxt is not None and nxt >= K and nxt not in dp:
                dp[nxt] = dp[curr] + 1
                queue.append(nxt)
'''

# 1546: 평균 - 출력 형식 맞추기
fixes['1546'] = '''n = int(input())
scores = list(map(int, input().split()))
m = max(scores)
new_scores = [s / m * 100 for s in scores]
avg = sum(new_scores) / n
print(avg)
'''

# 1932: 정수 피라미드 - 역방향 (bottom-up)
# description: "맨 아래층에서 시작하여 맨 위층으로" -> 아래에서 위로 올라감
# 실제로는 bottom-up DP
fixes['1932'] = '''import sys
input = sys.stdin.readline
n = int(input())
tri = []
for _ in range(n):
    tri.append(list(map(int, input().split())))
# bottom-up: 아래에서 위로
for i in range(n - 2, -1, -1):
    for j in range(i + 1):
        tri[i][j] += max(tri[i+1][j], tri[i+1][j+1])
print(tri[0][0])
'''

# 2108: 통계학 - 4개 값 출력
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

# 2169: 로봇 탐사 - 왼/오/아래 이동
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
    right = [INF] * m
    # 위에서 내려온 후 왼쪽으로 이동
    left[0] = dp[i-1][0] + grid[i][0]
    for j in range(1, m):
        left[j] = max(dp[i-1][j], left[j-1]) + grid[i][j]
    # 위에서 내려온 후 오른쪽으로 이동
    right[m-1] = dp[i-1][m-1] + grid[i][m-1]
    for j in range(m-2, -1, -1):
        right[j] = max(dp[i-1][j], right[j+1]) + grid[i][j]
    for j in range(m):
        dp[i][j] = max(left[j], right[j])
print(dp[n-1][m-1])
'''

# 2252: 줄 세우기 - 위상 정렬 (여러 답 가능)
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

# 2803: 프로젝트 팀 구성
fixes['2803'] = '''import sys
sys.setrecursionlimit(10000)
input = sys.stdin.readline
line = input().split()
n, m, k = int(line[0]), int(line[1]), int(line[2])
adj = [[] for _ in range(n + 1)]
for _ in range(k):
    line = input().split()
    a, b = int(line[0]), int(line[1])
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

# 9662: 돌 게임 8 - 재확인 필요
fixes['9662'] = '''import sys
input = sys.stdin.readline
n = int(input())
k = int(input())
stones = list(map(int, input().split()))
# SG 함수로 후공 승리 횟수 계산
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
# 주기 찾기
period = 0
for p in range(1, MAX):
    valid = True
    for i in range(p, min(p + 100, MAX)):
        if i + p < MAX and sg[i] != sg[i + p]:
            valid = False
            break
    if valid:
        period = p
        break
# 카운트
count = 0
if period == 0 or n < MAX:
    for i in range(1, min(n + 1, MAX)):
        if sg[i] == 0:
            count += 1
else:
    # 주기 이전
    prefix = min(period, n)
    for i in range(1, prefix + 1):
        if sg[i] == 0:
            count += 1
    # 주기 부분
    if n > period:
        zeros_in_period = sum(1 for i in range(1, period + 1) if sg[i] == 0)
        remaining = n - period
        full = remaining // period
        count += full * zeros_in_period
        partial = remaining % period
        for i in range(1, partial + 1):
            if sg[i] == 0:
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
    for j in range(max(0, i - d), i + 1):
        ans = max(ans, v[j] * t[i])
print(ans)
'''

# 11191: Xor Maximization - 선형 기저
fixes['11191'] = '''import sys
input = sys.stdin.readline
n = int(input())
nums = list(map(int, input().split()))
basis = []
for x in nums:
    cur = x
    for b in basis:
        cur = min(cur, cur ^ b)
    if cur > 0:
        basis.append(cur)
        basis.sort(reverse=True)
ans = 0
for b in basis:
    if ans ^ b > ans:
        ans ^= b
print(ans)
'''

# 11694: 님 게임 - 출력 형식 확인 (koosaga/cubelover vs 민수/?)
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

# 11710: Cost Performance 플로우 - 수정
fixes['11710'] = '''import sys
from collections import deque
input = sys.stdin.readline
n, m = map(int, input().split())
INF = float('inf')
adj = [[] for _ in range(n)]
cap = {}
cost = {}
for _ in range(m):
    parts = input().split()
    u, v, c, w = int(parts[0]) - 1, int(parts[1]) - 1, int(parts[2]), int(parts[3])
    adj[u].append(v)
    adj[v].append(u)
    cap[(u, v)] = c
    cap[(v, u)] = 0
    cost[(u, v)] = w
    cost[(v, u)] = -w
source, sink = 0, n - 1
total_flow = 0
total_cost = 0
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
            if cap.get((u, v), 0) > 0 and dist[u] + cost.get((u, v), 0) < dist[v]:
                dist[v] = dist[u] + cost[(u, v)]
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
        flow = min(flow, cap[(u, v)])
        v = u
    v = sink
    while v != source:
        u = parent[v]
        cap[(u, v)] -= flow
        cap[(v, u)] = cap.get((v, u), 0) + flow
        v = u
    total_flow += flow
    total_cost += flow * dist[sink]
if total_flow > 0:
    print(f"{total_cost}/{total_flow}")
else:
    print("0/1")
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
sg = 0
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
            sg ^= size
if sg == 0:
    print("Second")
else:
    print("First")
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

# 12015: LIS 길이
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

# 12852: 1로 만들기 2 - N에서 1로
fixes['12852'] = '''from collections import deque
n = int(input())
dist = {n: 0}
parent = {n: -1}
queue = deque([n])
while queue:
    cur = queue.popleft()
    if cur == 1:
        break
    nexts = []
    if cur % 3 == 0:
        nexts.append(cur // 3)
    if cur % 2 == 0:
        nexts.append(cur // 2)
    nexts.append(cur - 1)
    for nxt in nexts:
        if nxt > 0 and nxt not in dist:
            dist[nxt] = dist[cur] + 1
            parent[nxt] = cur
            queue.append(nxt)
path = []
cur = 1
while cur != -1:
    path.append(cur)
    cur = parent.get(cur, -1)
path.reverse()
print(dist[1])
print(' '.join(map(str, path)))
'''

# 13018: 작업 배정 최적화
fixes['13018'] = '''import sys
import heapq
input = sys.stdin.readline
n = int(input())
tasks = []
for i in range(n):
    parts = input().split()
    d, t = int(parts[0]), int(parts[1])
    tasks.append((d, t))
tasks.sort()
total_time = 0
pq = []
count = 0
for d, t in tasks:
    heapq.heappush(pq, -t)
    total_time += t
    count += 1
    while total_time > d and pq:
        removed = -heapq.heappop(pq)
        total_time -= removed
        count -= 1
print(count)
'''

# 13034: 다각형 게임
fixes['13034'] = '''n = int(input())
sg = [0] * (n + 1)
for i in range(2, n + 1):
    reachable = set()
    for j in range(0, i + 1):
        k = i - j - 2
        if k >= 0:
            reachable.add(sg[j] ^ sg[k])
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
parts = input().split()
n, m, k = int(parts[0]), int(parts[1]), int(parts[2])
if k == 0:
    if m == 0:
        print(0)
    else:
        print(-1)
else:
    adj = [[] for _ in range(n + 1)]
    for _ in range(k):
        parts = input().split()
        a, b = int(parts[0]), int(parts[1])
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

# 13448: SW 역량 테스트 - 0-1 배낭
fixes['13448'] = '''import sys
input = sys.stdin.readline
parts = input().split()
n, k = int(parts[0]), int(parts[1])
problems = []
for _ in range(n):
    parts = input().split()
    t = int(parts[0])
    p = int(parts[1])
    problems.append((t, p))
dp = [0] * (k + 1)
for t, p in problems:
    for j in range(k, t - 1, -1):
        dp[j] = max(dp[j], dp[j - t] + p)
print(dp[k])
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
        try:
            count += int(line)
        except:
            pass
'''

# 14750: Jerry and Tom
fixes['14750'] = '''import sys
sys.setrecursionlimit(10000)
input = sys.stdin.readline
def ccw(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
def can_see(hole, mouse, walls):
    for wall in walls:
        x1, y1, x2, y2 = wall
        d1 = ccw(hole, mouse, (x1, y1))
        d2 = ccw(hole, mouse, (x2, y2))
        d3 = ccw((x1, y1), (x2, y2), hole)
        d4 = ccw((x1, y1), (x2, y2), mouse)
        if d1 * d2 < 0 and d3 * d4 < 0:
            return False
    return True
parts = input().split()
n, m, h = int(parts[0]), int(parts[1]), int(parts[2])
walls = []
for _ in range(n):
    parts = input().split()
    walls.append((int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])))
holes = []
for _ in range(h):
    parts = input().split()
    holes.append((int(parts[0]), int(parts[1])))
mice = []
for _ in range(m):
    parts = input().split()
    mice.append((int(parts[0]), int(parts[1])))
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

# 16229: 반복 패턴 - KMP 기반
fixes['16229'] = '''import sys
input = sys.stdin.readline
parts = input().split()
n, k = int(parts[0]), int(parts[1])
s = input().strip()
if n == 0:
    print(0)
else:
    # KMP failure function
    fail = [0] * n
    j = 0
    for i in range(1, n):
        while j > 0 and s[i] != s[j]:
            j = fail[j - 1]
        if s[i] == s[j]:
            j += 1
            fail[i] = j
        else:
            fail[i] = 0
    # 가능한 주기 찾기
    ans = n  # 최악의 경우 전체가 주기
    for period in range(1, n + 1):
        mismatch = 0
        for i in range(n):
            if s[i] != s[i % period]:
                mismatch += 1
        if mismatch <= k:
            ans = period
            break
    print(ans)
'''

# 16883: 대각 게임
fixes['16883'] = '''import sys
input = sys.stdin.readline
parts = input().split()
n, m = int(parts[0]), int(parts[1])
xor = 0
for i in range(n):
    row = list(map(int, input().split()))
    for j in range(m):
        if row[j] == 1:
            xor ^= min(i + 1, j + 1, n - i, m - j)
if xor == 0:
    print("cubelover")
else:
    print("koosaga")
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
sz = len(sorted_arr)
bit = BIT(sz)
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
LOG = 19
m = int(input())
f = [0] + list(map(int, input().split()))
sparse = [[0] * (m + 1) for _ in range(LOG)]
for i in range(1, m + 1):
    sparse[0][i] = f[i]
for j in range(1, LOG):
    for i in range(1, m + 1):
        sparse[j][i] = sparse[j-1][sparse[j-1][i]]
q = int(input())
for _ in range(q):
    parts = input().split()
    n, x = int(parts[0]), int(parts[1])
    for j in range(LOG):
        if n & (1 << j):
            x = sparse[j][x]
    print(x)
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
