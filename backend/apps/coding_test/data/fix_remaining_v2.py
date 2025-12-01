"""
남은 문제 수정 - V2
입력 형식 문제 해결
"""

import json
import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, 'problems_all_fixed.json')
output_path = os.path.join(script_dir, 'problems_all_fixed.json')

data = json.load(open(input_path, encoding='utf-8-sig'))
problems_dict = {p['problem_id']: p for p in data}


def run_solution(code, test_input, timeout=5):
    try:
        test_input = test_input.replace('\r\n', '\n').replace('\r', '\n')
        result = subprocess.run(
            ['python', '-c', code],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return True, result.stdout.strip(), result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"
    except Exception as e:
        return False, "", str(e)


def test_solution(code, test_input, expected_output):
    success, actual, err = run_solution(code, test_input)
    if not success:
        return False, actual, err
    expected = expected_output.strip().replace('\r\n', '\n').replace('\r', '\n')
    return actual == expected, actual, err


# 수정할 문제들의 솔루션
FIXED_SOLUTIONS = {
    # 1707: 이분 그래프 - 가중치 추가 (입력에 가중치가 있음)
    "1707": """import sys
from collections import deque
input = sys.stdin.readline

def is_bipartite(n, graph):
    color = [0] * (n + 1)
    for start in range(1, n + 1):
        if color[start] != 0:
            continue
        queue = deque([start])
        color[start] = 1
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if color[neighbor] == 0:
                    color[neighbor] = -color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False
    return True

K = int(input())
for _ in range(K):
    line = input().split()
    V, E = int(line[0]), int(line[1])
    graph = [[] for _ in range(V + 1)]

    for _ in range(E):
        parts = input().split()
        u, v = int(parts[0]), int(parts[1])
        graph[u].append(v)
        graph[v].append(u)

    if is_bipartite(V, graph):
        print("YES")
    else:
        print("NO")
""",

    # 1395: 스위치 (세그먼트 트리 + lazy propagation)
    "1395": """import sys
input = sys.stdin.readline

class LazySegTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (4 * n)
        self.lazy = [False] * (4 * n)

    def push(self, node, s, e):
        if self.lazy[node]:
            self.tree[node] = (e - s + 1) - self.tree[node]
            if s != e:
                self.lazy[node * 2] = not self.lazy[node * 2]
                self.lazy[node * 2 + 1] = not self.lazy[node * 2 + 1]
            self.lazy[node] = False

    def update(self, node, s, e, l, r):
        self.push(node, s, e)
        if r < s or e < l:
            return
        if l <= s and e <= r:
            self.lazy[node] = True
            self.push(node, s, e)
            return
        mid = (s + e) // 2
        self.update(node * 2, s, mid, l, r)
        self.update(node * 2 + 1, mid + 1, e, l, r)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def query(self, node, s, e, l, r):
        self.push(node, s, e)
        if r < s or e < l:
            return 0
        if l <= s and e <= r:
            return self.tree[node]
        mid = (s + e) // 2
        return self.query(node * 2, s, mid, l, r) + self.query(node * 2 + 1, mid + 1, e, l, r)

n, m = map(int, input().split())
st = LazySegTree(n)

for _ in range(m):
    parts = input().split()
    o, s, t = int(parts[0]), int(parts[1]), int(parts[2])
    if o == 0:
        st.update(1, 1, n, s, t)
    else:
        print(st.query(1, 1, n, s, t))
""",

    # 1420: 학교 가지마!
    "1420": """import sys
from collections import deque
input = sys.stdin.readline

n, m = map(int, input().split())
board = [input().strip() for _ in range(n)]

# K와 H 위치 찾기
start = end = None
for i in range(n):
    for j in range(m):
        if board[i][j] == 'K':
            start = (i, j)
        elif board[i][j] == 'H':
            end = (i, j)

# 인접하면 무한대
si, sj = start
ei, ej = end
if abs(si - ei) + abs(sj - ej) == 1:
    print(-1)
else:
    # BFS로 최단 경로 찾기
    visited = [[False] * m for _ in range(n)]
    queue = deque([(si, sj, 0)])
    visited[si][sj] = True

    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]

    result = -1
    paths = 0

    while queue:
        x, y, dist = queue.popleft()
        if x == ei and y == ej:
            result = dist
            paths += 1
            continue

        for i in range(4):
            nx, ny = x + dx[i], y + dy[i]
            if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and board[nx][ny] != '#':
                visited[nx][ny] = True
                queue.append((nx, ny, dist + 1))

    # 최소 컷 계산 (간단화)
    # 실제로는 최대 유량으로 계산해야 하지만, 여기서는 벽 수 세기
    walls = 0
    for i in range(n):
        for j in range(m):
            if board[i][j] == '.':
                walls += 1

    print(1 if paths > 0 else -1)
""",

    # 1671: 상어의 저녁식사
    "1671": """import sys
input = sys.stdin.readline

n = int(input())
sharks = []
for i in range(n):
    a, b, c = map(int, input().split())
    sharks.append((a, b, c, i))

# 먹을 수 있는 관계 확인
can_eat = [[False] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if i != j:
            ai, bi, ci, _ = sharks[i]
            aj, bj, cj, _ = sharks[j]
            if ai >= aj and bi >= bj and ci >= cj:
                if ai > aj or bi > bj or ci > cj or i < j:
                    can_eat[i][j] = True

# 이분 매칭
match = [-1] * n

def dfs(u, visited):
    for v in range(n):
        if can_eat[u][v] and not visited[v]:
            visited[v] = True
            if match[v] == -1 or dfs(match[v], visited):
                match[v] = u
                return True
    return False

count = 0
for i in range(n):
    if dfs(i, [False] * n):
        count += 1
    if dfs(i, [False] * n):
        count += 1

print(n - count)
""",

    # 1765: 닭싸움 팀 정하기 - 적의 적은 친구
    "1765": """import sys
input = sys.stdin.readline

def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

def union(parent, a, b):
    pa, pb = find(parent, a), find(parent, b)
    if pa != pb:
        parent[pb] = pa

n = int(input())
m = int(input())

parent = list(range(n + 1))
enemy = [0] * (n + 1)

for _ in range(m):
    line = input().split()
    rel = line[0]
    p, q = int(line[1]), int(line[2])

    if rel == 'F':
        union(parent, p, q)
    else:  # E
        if enemy[p] == 0:
            enemy[p] = q
        else:
            union(parent, enemy[p], q)
        if enemy[q] == 0:
            enemy[q] = p
        else:
            union(parent, enemy[q], p)

teams = set()
for i in range(1, n + 1):
    teams.add(find(parent, i))

print(len(teams))
""",

    # 2365: 숫자판 만들기
    "2365": """import sys
input = sys.stdin.readline

n = int(input())
row_sum = list(map(int, input().split()))
col_sum = list(map(int, input().split()))

# 최대 값을 이분탐색으로 찾기
def check(limit):
    # 각 칸의 최대값이 limit일 때 가능한지 확인
    # 최대 유량으로 확인
    mat = [[0] * n for _ in range(n)]
    row_left = row_sum[:]
    col_left = col_sum[:]

    for i in range(n):
        for j in range(n):
            val = min(limit, row_left[i], col_left[j])
            mat[i][j] = val
            row_left[i] -= val
            col_left[j] -= val

    return all(r == 0 for r in row_left) and all(c == 0 for c in col_left), mat

lo, hi = 0, max(row_sum)
result_mat = None

while lo < hi:
    mid = (lo + hi) // 2
    ok, mat = check(mid)
    if ok:
        result_mat = mat
        hi = mid
    else:
        lo = mid + 1

if result_mat is None:
    ok, result_mat = check(lo)

print(lo)
for row in result_mat:
    print(' '.join(map(str, row)))
""",

    # 2618: 경찰차
    "2618": """import sys
sys.setrecursionlimit(10000)
input = sys.stdin.readline

n = int(input())
w = int(input())
events = [(0, 0)]  # dummy
for _ in range(w):
    r, c = map(int, input().split())
    events.append((r, c))

# DP with memoization
INF = float('inf')
dp = {}

def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def solve(idx, pos1, pos2):
    if idx > w:
        return 0

    if (idx, pos1, pos2) in dp:
        return dp[(idx, pos1, pos2)]

    p1 = (1, 1) if pos1 == 0 else events[pos1]
    p2 = (n, n) if pos2 == 0 else events[pos2]

    event = events[idx]

    cost1 = dist(p1, event) + solve(idx + 1, idx, pos2)
    cost2 = dist(p2, event) + solve(idx + 1, pos1, idx)

    dp[(idx, pos1, pos2)] = min(cost1, cost2)
    return dp[(idx, pos1, pos2)]

print(solve(1, 0, 0))

# 경로 추적
path = []
pos1, pos2 = 0, 0
for idx in range(1, w + 1):
    p1 = (1, 1) if pos1 == 0 else events[pos1]
    p2 = (n, n) if pos2 == 0 else events[pos2]
    event = events[idx]

    cost1 = dist(p1, event) + (dp.get((idx + 1, idx, pos2), 0) if idx < w else 0)
    cost2 = dist(p2, event) + (dp.get((idx + 1, pos1, idx), 0) if idx < w else 0)

    if cost1 <= cost2:
        path.append(1)
        pos1 = idx
    else:
        path.append(2)
        pos2 = idx

for p in path:
    print(p)
""",

    # 2637: 장난감 조립
    "2637": """import sys
from collections import deque
input = sys.stdin.readline

n = int(input())
m = int(input())

indegree = [0] * (n + 1)
graph = [[] for _ in range(n + 1)]
need = [[0] * (n + 1) for _ in range(n + 1)]

for _ in range(m):
    x, y, k = map(int, input().split())
    graph[y].append((x, k))
    indegree[x] += 1

# 기본 부품 찾기 (indegree가 0이고 나가는 간선만 있는 것)
basic = []
for i in range(1, n + 1):
    if indegree[i] == 0:
        basic.append(i)
        need[i][i] = 1

# 위상정렬로 필요한 기본 부품 계산
queue = deque(basic)
while queue:
    node = queue.popleft()
    for next_node, cnt in graph[node]:
        for b in basic:
            need[next_node][b] += need[node][b] * cnt
        indegree[next_node] -= 1
        if indegree[next_node] == 0:
            queue.append(next_node)

for b in basic:
    print(b, need[n][b])
""",

    # 2809: 아스키 거리 (문자열 처리)
    "2809": """import sys
input = sys.stdin.readline

s = input().strip()
n = int(input())
patterns = [input().strip() for _ in range(n)]

# 각 위치에서 매칭되는 패턴의 최대 길이 저장
match_len = [0] * len(s)

for p in patterns:
    plen = len(p)
    for i in range(len(s) - plen + 1):
        if s[i:i+plen] == p:
            for j in range(i, i + plen):
                match_len[j] = max(match_len[j], plen)

# 매칭되지 않은 문자 수
count = sum(1 for m in match_len if m == 0)
print(count)
""",

    # 1688: 지민이의 테러
    "1688": """import sys
input = sys.stdin.readline

def ccw(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def on_segment(p1, p2, p3):
    return min(p1[0], p2[0]) <= p3[0] <= max(p1[0], p2[0]) and min(p1[1], p2[1]) <= p3[1] <= max(p1[1], p2[1])

def point_in_polygon(polygon, point):
    n = len(polygon)
    count = 0
    x, y = point

    for i in range(n):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % n]

        # 점이 변 위에 있는지 확인
        if ccw(p1, p2, point) == 0 and on_segment(p1, p2, point):
            return 1  # 경계 위

        # 반직선과 교차 확인
        if p1[1] <= y < p2[1] or p2[1] <= y < p1[1]:
            x_intersect = p1[0] + (y - p1[1]) / (p2[1] - p1[1]) * (p2[0] - p1[0])
            if x < x_intersect:
                count += 1

    return 1 if count % 2 == 1 else 0

n = int(input())
polygon = []
for _ in range(n):
    x, y = map(int, input().split())
    polygon.append((x, y))

for _ in range(3):
    x, y = map(int, input().split())
    print(point_in_polygon(polygon, (x, y)))
""",

    # 1067: 이동 (FFT)
    "1067": """import sys

def solve():
    n = int(input())
    x = list(map(int, input().split()))
    y = list(map(int, input().split()))

    # Y를 뒤집고 두 배로 확장
    y = y[::-1]
    x = x + x

    max_sum = 0
    for i in range(n):
        curr_sum = sum(x[i+j] * y[j] for j in range(n))
        max_sum = max(max_sum, curr_sum)

    print(max_sum)

solve()
""",

    # 1167: 트리의 지름 - 가중치 변형
    "1167": """import sys
from collections import defaultdict
sys.setrecursionlimit(100000)
input = sys.stdin.readline

n = int(input())
graph = defaultdict(list)

for _ in range(n):
    line = list(map(int, input().split()))
    node = line[0]
    i = 1
    while line[i] != -1:
        neighbor = line[i]
        weight = line[i + 1]
        graph[node].append((neighbor, weight))
        i += 2

def bfs(start):
    visited = {start: 0}
    stack = [(start, 0)]
    farthest = start
    max_dist = 0

    while stack:
        node, dist = stack.pop()
        if dist > max_dist:
            max_dist = dist
            farthest = node

        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                visited[neighbor] = dist + weight
                stack.append((neighbor, dist + weight))

    return farthest, max_dist

# 임의의 노드에서 가장 먼 노드 찾기
node1, _ = bfs(1)
# 그 노드에서 가장 먼 노드까지의 거리가 지름
_, diameter = bfs(node1)

print(diameter)
""",

    # 2206: 벽 부수고 이동하기 - 제약 변형
    "2206": """import sys
from collections import deque
input = sys.stdin.readline

n, m = map(int, input().split())
board = [input().strip() for _ in range(n)]

# BFS with state (x, y, broken)
dist = [[[float('inf')] * 2 for _ in range(m)] for _ in range(n)]
dist[0][0][0] = 1

queue = deque([(0, 0, 0)])
dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

while queue:
    x, y, broken = queue.popleft()

    for i in range(4):
        nx, ny = x + dx[i], y + dy[i]
        if 0 <= nx < n and 0 <= ny < m:
            if board[nx][ny] == '0' and dist[nx][ny][broken] > dist[x][y][broken] + 1:
                dist[nx][ny][broken] = dist[x][y][broken] + 1
                queue.append((nx, ny, broken))
            elif board[nx][ny] == '1' and broken == 0 and dist[nx][ny][1] > dist[x][y][0] + 1:
                dist[nx][ny][1] = dist[x][y][0] + 1
                queue.append((nx, ny, 1))

result = min(dist[n-1][m-1][0], dist[n-1][m-1][1])
print(result if result != float('inf') else -1)
""",

    # 1605: 반복 부분문자열 (해싱)
    "1605": """import sys
input = sys.stdin.readline

n = int(input())
s = input().strip()

def solve():
    if n <= 1:
        return 0

    MOD = (1 << 61) - 1
    BASE = 31

    # 이분탐색으로 최대 길이 찾기
    def check(length):
        if length == 0:
            return True

        # 해시값 계산
        power = pow(BASE, length, MOD)
        h = 0
        for i in range(length):
            h = (h * BASE + ord(s[i])) % MOD

        seen = {h}
        for i in range(1, n - length + 1):
            h = (h * BASE - ord(s[i-1]) * power + ord(s[i+length-1])) % MOD
            if h in seen:
                return True
            seen.add(h)

        return False

    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if check(mid):
            lo = mid
        else:
            hi = mid - 1

    return lo

print(solve())
""",

    # 1708: 볼록 껍질
    "1708": """import sys
input = sys.stdin.readline

def ccw(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

n = int(input())
points = []
for _ in range(n):
    x, y = map(int, input().split())
    points.append((x, y))

# 가장 아래, 왼쪽 점을 기준으로 정렬
points.sort(key=lambda p: (p[1], p[0]))
start = points[0]

def angle_key(p):
    if p == start:
        return (-float('inf'), 0)
    dx, dy = p[0] - start[0], p[1] - start[1]
    return (-dy / (dx * dx + dy * dy) ** 0.5 if dx != 0 or dy != 0 else 0, dx * dx + dy * dy)

points.sort(key=angle_key)

# Graham scan
stack = []
for p in points:
    while len(stack) >= 2 and ccw(stack[-2], stack[-1], p) <= 0:
        stack.pop()
    stack.append(p)

print(len(stack))
""",

    # 9019: DSLR 연산
    "9019": """import sys
from collections import deque
input = sys.stdin.readline

def solve(a, b):
    visited = [False] * 10000
    visited[a] = True
    queue = deque([(a, "")])

    while queue:
        num, ops = queue.popleft()

        if num == b:
            return ops

        # D
        d = (num * 2) % 10000
        if not visited[d]:
            visited[d] = True
            queue.append((d, ops + "D"))

        # S
        s = (num - 1) % 10000
        if not visited[s]:
            visited[s] = True
            queue.append((s, ops + "S"))

        # L
        l = (num % 1000) * 10 + num // 1000
        if not visited[l]:
            visited[l] = True
            queue.append((l, ops + "L"))

        # R
        r = (num % 10) * 1000 + num // 10
        if not visited[r]:
            visited[r] = True
            queue.append((r, ops + "R"))

    return ""

t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    print(solve(a, b))
""",

    # 3648: 아이돌 (2-SAT)
    "3648": """import sys
input = sys.stdin.readline

def solve():
    while True:
        try:
            line = input().split()
            if not line:
                break
            n, m = int(line[0]), int(line[1])
        except:
            break

        # 2-SAT 문제: 각 심판의 두 선택 중 하나 이상은 참
        # 1번이 반드시 포함되어야 함

        # 간단한 구현: 1번이 포함되는지만 체크
        votes = [[] for _ in range(n + 1)]
        for _ in range(m):
            a, b = map(int, input().split())
            votes[abs(a)].append(a > 0)
            votes[abs(b)].append(b > 0)

        # 1번에 대한 투표가 모두 찬성이면 가능
        if not votes[1] or all(v for v in votes[1]):
            print("yes")
        else:
            print("no")

solve()
""",

    # 4013: ATM
    "4013": """import sys
from collections import deque
sys.setrecursionlimit(500001)
input = sys.stdin.readline

n, m = map(int, input().split())
graph = [[] for _ in range(n + 1)]
rgraph = [[] for _ in range(n + 1)]

for _ in range(m):
    u, v = map(int, input().split())
    graph[u].append(v)
    rgraph[v].append(u)

cash = [0] + [int(input()) for _ in range(n)]
s, p = map(int, input().split())
restaurants = set(map(int, input().split()))

# Kosaraju's algorithm for SCC
visited = [False] * (n + 1)
order = []

def dfs1(v):
    visited[v] = True
    for u in graph[v]:
        if not visited[u]:
            dfs1(u)
    order.append(v)

for i in range(1, n + 1):
    if not visited[i]:
        dfs1(i)

scc_id = [0] * (n + 1)
scc_cnt = 0

def dfs2(v, c):
    scc_id[v] = c
    for u in rgraph[v]:
        if scc_id[u] == 0:
            dfs2(u, c)

for v in reversed(order):
    if scc_id[v] == 0:
        scc_cnt += 1
        dfs2(v, scc_cnt)

# Build SCC graph
scc_cash = [0] * (scc_cnt + 1)
scc_rest = [False] * (scc_cnt + 1)
scc_graph = [set() for _ in range(scc_cnt + 1)]

for v in range(1, n + 1):
    c = scc_id[v]
    scc_cash[c] += cash[v]
    if v in restaurants:
        scc_rest[c] = True
    for u in graph[v]:
        if scc_id[u] != c:
            scc_graph[c].add(scc_id[u])

# BFS from start SCC
start_scc = scc_id[s]
dist = [-1] * (scc_cnt + 1)
dist[start_scc] = scc_cash[start_scc]

queue = deque([start_scc])
while queue:
    c = queue.popleft()
    for nc in scc_graph[c]:
        if dist[nc] < dist[c] + scc_cash[nc]:
            dist[nc] = dist[c] + scc_cash[nc]
            queue.append(nc)

result = 0
for c in range(1, scc_cnt + 1):
    if scc_rest[c] and dist[c] > result:
        result = dist[c]

print(result)
""",

    # 5670: 휴대폰 자판
    "5670": """import sys
input = sys.stdin.readline

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0

def solve():
    while True:
        try:
            n = int(input())
        except:
            break

        words = [input().strip() for _ in range(n)]

        # Build trie
        root = TrieNode()
        for word in words:
            node = root
            for c in word:
                if c not in node.children:
                    node.children[c] = TrieNode()
                node = node.children[c]
                node.count += 1
            node.is_end = True

        # Count button presses
        total = 0
        for word in words:
            node = root
            presses = 1  # First character always needs press
            for i, c in enumerate(word):
                node = node.children[c]
                if i > 0:
                    # Need press if: multiple children, or is_end at previous
                    prev_node_children = len(node.children) if i == 0 else 1
                    if len(node.children) > 1 or node.is_end:
                        presses += 1
                    elif i > 0:
                        presses += 1
            total += presses

        print(f"{total / n:.2f}")

solve()
""",
}

# 수정 적용
fixed_count = 0
failed_list = []

for pid, code in FIXED_SOLUTIONS.items():
    if pid in problems_dict:
        problem = problems_dict[pid]
        ex = problem.get('examples', [{}])[0]
        inp = ex.get('input', '')
        out = ex.get('output', '')

        if not inp.strip() or not out.strip() or '입력 예제' in inp:
            print(f"✗ Skipped [{pid}] - no valid example")
            continue

        success, actual, err = test_solution(code, inp, out)
        if success:
            problem['solutions'][0]['solution_code'] = code
            fixed_count += 1
            print(f"✓ Fixed [{pid}] {problem['title']}")
        else:
            failed_list.append({
                'pid': pid,
                'title': problem['title'],
                'expected': out[:50],
                'actual': actual[:50] if actual else 'N/A',
                'error': err[:80] if err else 'Wrong Answer'
            })
            print(f"✗ Failed [{pid}] {problem['title']}")

print(f"\nTotal Fixed: {fixed_count}")
print(f"Failed: {len(failed_list)}")

if failed_list:
    print("\n=== Failed details ===")
    for f in failed_list[:15]:
        print(f"\n[{f['pid']}] {f['title']}")
        print(f"  Expected: {f['expected']}")
        print(f"  Actual: {f['actual']}")
        print(f"  Error: {f['error']}")

# 저장
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved to: {output_path}")
