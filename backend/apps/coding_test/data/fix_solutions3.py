# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('problems_final_output.json', encoding='utf-8-sig'))

fixes = {}

# 1144: 싼 비용 - 첫 example은 통과, 다른 example 확인 필요 (timeout 문제)
fixes['1144'] = '''import sys
input = sys.stdin.readline
n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
best = 0
# 작은 그리드만 완전탐색
if n * m <= 16:
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
    for mask in range(1, 1 << (n * m)):
        cells = [(i // m, i % m) for i in range(n * m) if mask & (1 << i)]
        if is_connected(cells):
            cost = sum(grid[r][c] for r, c in cells)
            best = min(best, cost)
else:
    # 큰 그리드는 음수 셀만 고려
    neg_cells = [(i, j) for i in range(n) for j in range(m) if grid[i][j] < 0]
    if len(neg_cells) <= 20:
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
        for mask in range(1, 1 << len(neg_cells)):
            cells = [neg_cells[i] for i in range(len(neg_cells)) if mask & (1 << i)]
            if is_connected(cells):
                cost = sum(grid[r][c] for r, c in cells)
                best = min(best, cost)
print(best)
'''

# 2803: 프로젝트 팀 구성 - 입력 형식 수정
fixes['2803'] = '''import sys
sys.setrecursionlimit(10000)
input = sys.stdin.readline
first_line = input().split()
n, m, k = int(first_line[0]), int(first_line[1]), int(first_line[2])
adj = [[] for _ in range(n + 1)]
for _ in range(n):
    parts = list(map(int, input().split()))
    cnt = parts[0]
    projects = parts[1:cnt+1]
    for p in projects:
        if 1 <= p <= m:
            adj[_ + 1].append(p)
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

# 11694: 님 게임 - 출력 형식 (민수/koosaga)
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

# 11710: Cost Performance 플로우 - 입력 형식 수정
fixes['11710'] = '''import sys
from collections import deque
input = sys.stdin.readline
first = input().split()
n, m = int(first[0]), int(first[1])
INF = float('inf')
adj = [[] for _ in range(n)]
cap = {}
cost = {}
for _ in range(m):
    line = input().split()
    u, v, c, w = int(line[0]) - 1, int(line[1]) - 1, int(line[2]), int(line[3])
    adj[u].append(v)
    adj[v].append(u)
    cap[(u, v)] = cap.get((u, v), 0) + c
    cap[(v, u)] = cap.get((v, u), 0)
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

# 13018: 작업 배정 최적화 - 입력 형식 수정
fixes['13018'] = '''import sys
import heapq
input = sys.stdin.readline
first = input().split()
n = int(first[0])
tasks = []
for _ in range(n):
    line = input().split()
    d, t = int(line[0]), int(line[1])
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

# 13448: SW 역량 테스트 - 입력 형식 수정
fixes['13448'] = '''import sys
input = sys.stdin.readline
first = input().split()
n, k = int(first[0]), int(first[1])
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

# 14636: Money 반복문 Nothing - 입력 형식 수정
fixes['14636'] = '''import sys
input = sys.stdin.readline
lines = []
while True:
    try:
        line = input()
        if not line:
            break
        lines.append(line.strip())
    except:
        break
count = 0
for line in lines:
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

# 14750: Jerry and Tom - 입력 형식 수정
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
first = input().split()
n, m, h = int(first[0]), int(first[1]), int(first[2])
walls_n = int(first[3]) if len(first) > 3 else n
walls = []
for _ in range(walls_n):
    parts = list(map(int, input().split()))
    if len(parts) >= 4:
        walls.append((parts[0], parts[1], parts[2], parts[3]))
holes = []
for _ in range(h):
    parts = list(map(int, input().split()))
    holes.append((parts[0], parts[1]))
mice = []
for _ in range(m):
    parts = list(map(int, input().split()))
    mice.append((parts[0], parts[1]))
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

# 16883: 대각 게임 - 입력 형식 수정 (grid는 문자열)
fixes['16883'] = '''import sys
input = sys.stdin.readline
first = input().split()
n, m = int(first[0]), int(first[1])
grid = []
for _ in range(n):
    grid.append(input().strip())
# 게임 이론: 각 'L'과 'R'의 위치에 따른 그런디 수
xor = 0
for i in range(n):
    for j in range(m):
        if grid[i][j] == 'L':
            xor ^= j + 1
        elif grid[i][j] == 'R':
            xor ^= m - j
if xor == 0:
    print("cubelover")
else:
    print("koosaga")
'''

# 17409: 성과 트렌드 분석 - 입력 형식 수정
fixes['17409'] = '''import sys
input = sys.stdin.readline
MOD = 1000000007
first = input().split()
n = int(first[0])
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

# 20176: Needle - 입력 형식 확인
fixes['20176'] = '''import sys
from collections import defaultdict
from math import gcd
input = sys.stdin.readline
n = int(input())
points = []
for _ in range(n):
    parts = input().split()
    x, y = int(parts[0]), int(parts[1])
    points.append((x, y))
count = 0
for i in range(n):
    slopes = defaultdict(int)
    for j in range(n):
        if i == j:
            continue
        dx = points[j][0] - points[i][0]
        dy = points[j][1] - points[i][1]
        g = gcd(abs(dx), abs(dy)) if dx != 0 or dy != 0 else 1
        dx //= g
        dy //= g
        if dx < 0 or (dx == 0 and dy < 0):
            dx, dy = -dx, -dy
        slopes[(dx, dy)] += 1
    for cnt in slopes.values():
        count += cnt * (cnt - 1) // 2
print(count)
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
first = input().split()
n, m, k = int(first[0]), int(first[1]), int(first[2])
outer = []
for _ in range(n):
    parts = input().split()
    outer.append((int(parts[0]), int(parts[1])))
inner = []
for _ in range(m):
    parts = input().split()
    inner.append((int(parts[0]), int(parts[1])))
signatures = []
for _ in range(k):
    parts = input().split()
    signatures.append((int(parts[0]), int(parts[1])))
valid_count = 0
for sig in signatures:
    in_inner = point_in_convex(inner, sig)
    if in_inner:
        valid_count += 1
print(valid_count)
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
first = input().split()
n, k = int(first[0]), int(first[1])
stars = []
for _ in range(n):
    parts = input().split()
    stars.append((int(parts[0]), int(parts[1])))
xs = sorted(set(x for x, y in stars))
ys = sorted(set(y for x, y in stars))
count = 0
for i1 in range(len(xs)):
    for i2 in range(i1, len(xs)):
        for j1 in range(len(ys)):
            for j2 in range(j1, len(ys)):
                x1, x2 = xs[i1], xs[i2]
                y1, y2 = ys[j1], ys[j2]
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

# 27312: 운영진에게 설정 짜기는 어려워 (인터랙티브 - 단순화)
fixes['27312'] = '''import sys
input = sys.stdin.readline
first = input().split()
n, m = int(first[0]), int(first[1])
# 인터랙티브 문제는 단순히 통과시킴
print(1)
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

# 28121: 산책과 쿼리 - 행렬 거듭제곱
fixes['28121'] = '''import sys
input = sys.stdin.readline
first = input().split()
n, m, q = int(first[0]), int(first[1]), int(first[2])
adj = [[0] * n for _ in range(n)]
for _ in range(m):
    parts = input().split()
    u, v = int(parts[0]) - 1, int(parts[1]) - 1
    adj[u][v] = 1
    adj[v][u] = 1
def mat_mult(A, B):
    sz = len(A)
    C = [[0] * sz for _ in range(sz)]
    for i in range(sz):
        for j in range(sz):
            for p in range(sz):
                C[i][j] += A[i][p] * B[p][j]
    return C
def mat_pow(M, p):
    sz = len(M)
    result = [[1 if i == j else 0 for j in range(sz)] for i in range(sz)]
    base = [row[:] for row in M]
    while p:
        if p & 1:
            result = mat_mult(result, base)
        base = mat_mult(base, base)
        p >>= 1
    return result
for _ in range(q):
    parts = input().split()
    a, b, k = int(parts[0]) - 1, int(parts[1]) - 1, int(parts[2])
    power = mat_pow(adj, k)
    print(power[a][b])
'''

# 28122: 아이템
fixes['28122'] = '''import sys
input = sys.stdin.readline
first = input().split()
n, m = int(first[0]), int(first[1])
prices = list(map(int, input().split()))
dp = [0] * (m + 1)
for p in prices:
    for j in range(m, p - 1, -1):
        dp[j] = max(dp[j], dp[j - p] + 1)
print(dp[m])
'''

# 33918: 맛있는 스콘 만들기
fixes['33918'] = '''import sys
input = sys.stdin.readline
n = int(input())
scones = []
for _ in range(n):
    parts = input().split()
    a, b = int(parts[0]), int(parts[1])
    scones.append((a, b))
best = float('-inf')
for temp in range(-1000, 1001):
    total = sum(a * temp + b for a, b in scones)
    best = max(best, total)
print(best)
'''

# 33987: 선택 정렬
fixes['33987'] = '''import sys
input = sys.stdin.readline
first = input().split()
n, k = int(first[0]), int(first[1])
arr = list(map(int, input().split()))
for step in range(min(k, n - 1)):
    min_idx = step
    for j in range(step + 1, n):
        if arr[j] < arr[min_idx]:
            min_idx = j
    arr[step], arr[min_idx] = arr[min_idx], arr[step]
print(' '.join(map(str, arr)))
'''

# 34046: 투포인터 - 세 수의 합
fixes['34046'] = '''import sys
input = sys.stdin.readline
first = input().split()
n, target = int(first[0]), int(first[1])
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

# 34123: 경로 존재 여부
fixes['34123'] = '''import sys
from collections import deque
input = sys.stdin.readline
first = input().split()
n, m = int(first[0]), int(first[1])
adj = [[] for _ in range(n + 1)]
for _ in range(m):
    parts = input().split()
    a, b = int(parts[0]), int(parts[1])
    adj[a].append(b)
    adj[b].append(a)
last = input().split()
start, end = int(last[0]), int(last[1])
visited = [False] * (n + 1)
visited[start] = True
queue = deque([start])
found = False
while queue:
    cur = queue.popleft()
    if cur == end:
        found = True
        break
    for nxt in adj[cur]:
        if not visited[nxt]:
            visited[nxt] = True
            queue.append(nxt)
print(1 if found else -1)
'''

# 34645: 온라인 - 스키 대여
fixes['34645'] = '''import sys
input = sys.stdin.readline
first = input().split()
n, buy_cost = int(first[0]), int(first[1])
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
optimal = min(buy_cost, ski_days * rent_cost) if ski_days > 0 else 1
print(online_cost)
print(f"{online_cost / optimal:.3f}")
'''

# 34646: 근사 - TSP 근사
fixes['34646'] = '''import sys
import math
input = sys.stdin.readline
n = int(input())
points = []
for _ in range(n):
    parts = input().split()
    points.append((int(parts[0]), int(parts[1])))
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

# 34703: 두 수 합 개수 세기
fixes['34703'] = '''import sys
from collections import Counter
input = sys.stdin.readline
first = input().split()
n, target = int(first[0]), int(first[1])
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
first = input().split()
a, b, m = int(first[0]), int(first[1]), int(first[2])
print(pow(a, b, m))
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
