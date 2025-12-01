"""
대량 문제 수정 배치 4 - 레벨 1-15 문제
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


def run_solution(code, test_input, timeout=5):
    try:
        test_input = test_input.replace('\r\n', '\n').replace('\r', '\n')
        code = code.replace('\\n', '\n')
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


FIXED_SOLUTIONS = {
    # 1509: 팰린드롬 분할
    "1509": """s = input().strip()
n = len(s)

# is_palindrome[i][j] = s[i:j+1]이 팰린드롬인지
is_pal = [[False] * n for _ in range(n)]
for i in range(n):
    is_pal[i][i] = True
for i in range(n - 1):
    if s[i] == s[i + 1]:
        is_pal[i][i + 1] = True
for length in range(3, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        if s[i] == s[j] and is_pal[i + 1][j - 1]:
            is_pal[i][j] = True

# dp[i] = s[0:i]를 분할하는 최소 개수
dp = [float('inf')] * (n + 1)
dp[0] = 0
for i in range(1, n + 1):
    for j in range(i):
        if is_pal[j][i - 1]:
            dp[i] = min(dp[i], dp[j] + 1)
print(dp[n])""",

    # 1707: 이분 그래프
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
    V, E = map(int, input().split())
    graph = [[] for _ in range(V + 1)]
    for _ in range(E):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
    print("YES" if is_bipartite(V, graph) else "NO")""",

    # 1932: 정수 삼각형
    "1932": """n = int(input())
triangle = []
for _ in range(n):
    triangle.append(list(map(int, input().split())))

for i in range(n - 2, -1, -1):
    for j in range(i + 1):
        triangle[i][j] += max(triangle[i + 1][j], triangle[i + 1][j + 1])

print(triangle[0][0])""",

    # 2042: 구간 합 구하기 (세그먼트 트리)
    "2042": """import sys
input = sys.stdin.readline

def build(arr, tree, node, start, end):
    if start == end:
        tree[node] = arr[start]
    else:
        mid = (start + end) // 2
        build(arr, tree, node * 2, start, mid)
        build(arr, tree, node * 2 + 1, mid + 1, end)
        tree[node] = tree[node * 2] + tree[node * 2 + 1]

def update(tree, node, start, end, idx, val):
    if start == end:
        tree[node] = val
    else:
        mid = (start + end) // 2
        if idx <= mid:
            update(tree, node * 2, start, mid, idx, val)
        else:
            update(tree, node * 2 + 1, mid + 1, end, idx, val)
        tree[node] = tree[node * 2] + tree[node * 2 + 1]

def query(tree, node, start, end, left, right):
    if left > end or right < start:
        return 0
    if left <= start and end <= right:
        return tree[node]
    mid = (start + end) // 2
    return query(tree, node * 2, start, mid, left, right) + query(tree, node * 2 + 1, mid + 1, end, left, right)

N, M, K = map(int, input().split())
arr = [0] + [int(input()) for _ in range(N)]
tree = [0] * (4 * N)
build(arr, tree, 1, 1, N)

for _ in range(M + K):
    a, b, c = map(int, input().split())
    if a == 1:
        update(tree, 1, 1, N, b, c)
    else:
        print(query(tree, 1, 1, N, b, c))""",

    # 2169: 로봇 조종하기
    "2169": """import sys
input = sys.stdin.readline

n, m = map(int, input().split())
grid = []
for _ in range(n):
    grid.append(list(map(int, input().split())))

dp = [[0] * m for _ in range(n)]

# 첫 번째 행
dp[0][0] = grid[0][0]
for j in range(1, m):
    dp[0][j] = dp[0][j - 1] + grid[0][j]

# 나머지 행
for i in range(1, n):
    left = [0] * m
    right = [0] * m

    left[0] = dp[i - 1][0] + grid[i][0]
    for j in range(1, m):
        left[j] = max(dp[i - 1][j], left[j - 1]) + grid[i][j]

    right[m - 1] = dp[i - 1][m - 1] + grid[i][m - 1]
    for j in range(m - 2, -1, -1):
        right[j] = max(dp[i - 1][j], right[j + 1]) + grid[i][j]

    for j in range(m):
        dp[i][j] = max(left[j], right[j])

print(dp[n - 1][m - 1])""",

    # 2206: 벽 부수고 이동하기
    "2206": """from collections import deque
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
grid = [input().strip() for _ in range(n)]

# visited[x][y][k] = (x, y)에 도달, k=벽을 부쉈는지
visited = [[[False] * 2 for _ in range(m)] for _ in range(n)]
queue = deque([(0, 0, 0, 1)])  # x, y, broken, dist
visited[0][0][0] = True

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

result = -1
while queue:
    x, y, broken, dist = queue.popleft()
    if x == n - 1 and y == m - 1:
        result = dist
        break
    for i in range(4):
        nx, ny = x + dx[i], y + dy[i]
        if 0 <= nx < n and 0 <= ny < m:
            if grid[nx][ny] == '0' and not visited[nx][ny][broken]:
                visited[nx][ny][broken] = True
                queue.append((nx, ny, broken, dist + 1))
            elif grid[nx][ny] == '1' and broken == 0 and not visited[nx][ny][1]:
                visited[nx][ny][1] = True
                queue.append((nx, ny, 1, dist + 1))

print(result)""",

    # 2357: 최솟값과 최댓값 (세그먼트 트리)
    "2357": """import sys
input = sys.stdin.readline
INF = float('inf')

def build_min(arr, tree, node, start, end):
    if start == end:
        tree[node] = arr[start]
    else:
        mid = (start + end) // 2
        build_min(arr, tree, node * 2, start, mid)
        build_min(arr, tree, node * 2 + 1, mid + 1, end)
        tree[node] = min(tree[node * 2], tree[node * 2 + 1])

def build_max(arr, tree, node, start, end):
    if start == end:
        tree[node] = arr[start]
    else:
        mid = (start + end) // 2
        build_max(arr, tree, node * 2, start, mid)
        build_max(arr, tree, node * 2 + 1, mid + 1, end)
        tree[node] = max(tree[node * 2], tree[node * 2 + 1])

def query_min(tree, node, start, end, left, right):
    if left > end or right < start:
        return INF
    if left <= start and end <= right:
        return tree[node]
    mid = (start + end) // 2
    return min(query_min(tree, node * 2, start, mid, left, right),
               query_min(tree, node * 2 + 1, mid + 1, end, left, right))

def query_max(tree, node, start, end, left, right):
    if left > end or right < start:
        return -INF
    if left <= start and end <= right:
        return tree[node]
    mid = (start + end) // 2
    return max(query_max(tree, node * 2, start, mid, left, right),
               query_max(tree, node * 2 + 1, mid + 1, end, left, right))

N, M = map(int, input().split())
arr = [0] + [int(input()) for _ in range(N)]
min_tree = [0] * (4 * N)
max_tree = [0] * (4 * N)
build_min(arr, min_tree, 1, 1, N)
build_max(arr, max_tree, 1, 1, N)

for _ in range(M):
    a, b = map(int, input().split())
    print(query_min(min_tree, 1, 1, N, a, b), query_max(max_tree, 1, 1, N, a, b))""",

    # 2533: 사회망 서비스 (SNS)
    "2533": """import sys
sys.setrecursionlimit(300000)
input = sys.stdin.readline

n = int(input())
graph = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

dp = [[0, 0] for _ in range(n + 1)]  # [not_early_adopter, early_adopter]
visited = [False] * (n + 1)

def dfs(node):
    visited[node] = True
    dp[node][0] = 0  # not early adopter
    dp[node][1] = 1  # early adopter

    for child in graph[node]:
        if not visited[child]:
            dfs(child)
            dp[node][0] += dp[child][1]  # if I'm not, child must be
            dp[node][1] += min(dp[child][0], dp[child][1])  # if I am, child can be anything

dfs(1)
print(min(dp[1][0], dp[1][1]))""",

    # 2565: 전깃줄 (LIS)
    "2565": """n = int(input())
wires = []
for _ in range(n):
    a, b = map(int, input().split())
    wires.append((a, b))

wires.sort()
b_values = [w[1] for w in wires]

# LIS
dp = [1] * n
for i in range(1, n):
    for j in range(i):
        if b_values[j] < b_values[i]:
            dp[i] = max(dp[i], dp[j] + 1)

print(n - max(dp))""",

    # 9019: DSLR
    "9019": """from collections import deque
import sys
input = sys.stdin.readline

def solve(a, b):
    visited = [False] * 10000
    queue = deque([(a, "")])
    visited[a] = True

    while queue:
        n, ops = queue.popleft()
        if n == b:
            return ops

        # D: 2n mod 10000
        d = (n * 2) % 10000
        if not visited[d]:
            visited[d] = True
            queue.append((d, ops + "D"))

        # S: n - 1 (mod 10000)
        s = (n - 1) % 10000
        if not visited[s]:
            visited[s] = True
            queue.append((s, ops + "S"))

        # L: rotate left
        l = (n % 1000) * 10 + n // 1000
        if not visited[l]:
            visited[l] = True
            queue.append((l, ops + "L"))

        # R: rotate right
        r = (n % 10) * 1000 + n // 10
        if not visited[r]:
            visited[r] = True
            queue.append((r, ops + "R"))

    return ""

T = int(input())
for _ in range(T):
    a, b = map(int, input().split())
    print(solve(a, b))""",

    # 11049: 행렬 곱셈 순서
    "11049": """import sys
input = sys.stdin.readline
INF = float('inf')

n = int(input())
matrices = []
for _ in range(n):
    r, c = map(int, input().split())
    matrices.append((r, c))

dp = [[0] * n for _ in range(n)]

for length in range(1, n):
    for i in range(n - length):
        j = i + length
        dp[i][j] = INF
        for k in range(i, j):
            cost = dp[i][k] + dp[k + 1][j] + matrices[i][0] * matrices[k][1] * matrices[j][1]
            dp[i][j] = min(dp[i][j], cost)

print(dp[0][n - 1])""",

    # 11404: 플로이드
    "11404": """import sys
input = sys.stdin.readline
INF = float('inf')

n = int(input())
m = int(input())

dist = [[INF] * (n + 1) for _ in range(n + 1)]
for i in range(n + 1):
    dist[i][i] = 0

for _ in range(m):
    a, b, c = map(int, input().split())
    dist[a][b] = min(dist[a][b], c)

for k in range(1, n + 1):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if dist[i][k] + dist[k][j] < dist[i][j]:
                dist[i][j] = dist[i][k] + dist[k][j]

for i in range(1, n + 1):
    row = []
    for j in range(1, n + 1):
        row.append(str(dist[i][j] if dist[i][j] != INF else 0))
    print(' '.join(row))""",

    # 11505: 구간 곱 구하기 (세그먼트 트리)
    "11505": """import sys
input = sys.stdin.readline
MOD = 1000000007

def build(arr, tree, node, start, end):
    if start == end:
        tree[node] = arr[start]
    else:
        mid = (start + end) // 2
        build(arr, tree, node * 2, start, mid)
        build(arr, tree, node * 2 + 1, mid + 1, end)
        tree[node] = (tree[node * 2] * tree[node * 2 + 1]) % MOD

def update(tree, node, start, end, idx, val):
    if start == end:
        tree[node] = val
    else:
        mid = (start + end) // 2
        if idx <= mid:
            update(tree, node * 2, start, mid, idx, val)
        else:
            update(tree, node * 2 + 1, mid + 1, end, idx, val)
        tree[node] = (tree[node * 2] * tree[node * 2 + 1]) % MOD

def query(tree, node, start, end, left, right):
    if left > end or right < start:
        return 1
    if left <= start and end <= right:
        return tree[node]
    mid = (start + end) // 2
    return (query(tree, node * 2, start, mid, left, right) *
            query(tree, node * 2 + 1, mid + 1, end, left, right)) % MOD

N, M, K = map(int, input().split())
arr = [0] + [int(input()) for _ in range(N)]
tree = [0] * (4 * N)
build(arr, tree, 1, 1, N)

for _ in range(M + K):
    a, b, c = map(int, input().split())
    if a == 1:
        update(tree, 1, 1, N, b, c)
    else:
        print(query(tree, 1, 1, N, b, c))""",

    # 11660: 구간 합 구하기 5 (2D prefix sum)
    "11660": """import sys
input = sys.stdin.readline

n, m = map(int, input().split())
arr = [[0] * (n + 1)]
for _ in range(n):
    arr.append([0] + list(map(int, input().split())))

prefix = [[0] * (n + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, n + 1):
        prefix[i][j] = arr[i][j] + prefix[i - 1][j] + prefix[i][j - 1] - prefix[i - 1][j - 1]

for _ in range(m):
    x1, y1, x2, y2 = map(int, input().split())
    result = prefix[x2][y2] - prefix[x1 - 1][y2] - prefix[x2][y1 - 1] + prefix[x1 - 1][y1 - 1]
    print(result)""",

    # 13913: 숨바꼭질 4 (경로 추적)
    "13913": """from collections import deque

n, k = map(int, input().split())

if n == k:
    print(0)
    print(n)
else:
    visited = [-1] * 100001
    parent = [-1] * 100001
    queue = deque([n])
    visited[n] = 0

    while queue:
        pos = queue.popleft()
        if pos == k:
            break
        for next_pos in [pos - 1, pos + 1, pos * 2]:
            if 0 <= next_pos <= 100000 and visited[next_pos] == -1:
                visited[next_pos] = visited[pos] + 1
                parent[next_pos] = pos
                queue.append(next_pos)

    print(visited[k])
    path = []
    cur = k
    while cur != -1:
        path.append(cur)
        cur = parent[cur]
    print(' '.join(map(str, reversed(path))))""",

    # 16928: 뱀과 사다리 게임
    "16928": """from collections import deque

n, m = map(int, input().split())
teleport = {}
for _ in range(n + m):
    x, y = map(int, input().split())
    teleport[x] = y

visited = [-1] * 101
queue = deque([1])
visited[1] = 0

while queue:
    pos = queue.popleft()
    if pos == 100:
        print(visited[100])
        break
    for dice in range(1, 7):
        next_pos = pos + dice
        if next_pos > 100:
            continue
        if next_pos in teleport:
            next_pos = teleport[next_pos]
        if visited[next_pos] == -1:
            visited[next_pos] = visited[pos] + 1
            queue.append(next_pos)""",

    # 17404: RGB거리 2 (원형)
    "17404": """import sys
input = sys.stdin.readline
INF = float('inf')

n = int(input())
cost = []
for _ in range(n):
    cost.append(list(map(int, input().split())))

result = INF

for first in range(3):
    dp = [[INF] * 3 for _ in range(n)]
    dp[0][first] = cost[0][first]

    for i in range(1, n):
        for j in range(3):
            for k in range(3):
                if j != k:
                    dp[i][j] = min(dp[i][j], dp[i - 1][k] + cost[i][j])

    for last in range(3):
        if last != first:
            result = min(result, dp[n - 1][last])

print(result)""",

    # 24480: DFS (내림차순)
    "24480": """import sys
sys.setrecursionlimit(200000)
input = sys.stdin.readline

n, m, r = map(int, input().split())
graph = [[] for _ in range(n + 1)]
for _ in range(m):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

for i in range(n + 1):
    graph[i].sort(reverse=True)

visited = [0] * (n + 1)
order = [0]

def dfs(node):
    order[0] += 1
    visited[node] = order[0]
    for next_node in graph[node]:
        if visited[next_node] == 0:
            dfs(next_node)

dfs(r)

for i in range(1, n + 1):
    print(visited[i])""",

    # 25206: 너의 평점은
    "25206": """grades = {'A+': 4.5, 'A0': 4.0, 'B+': 3.5, 'B0': 3.0,
           'C+': 2.5, 'C0': 2.0, 'D+': 1.5, 'D0': 1.0, 'F': 0.0}

total_credit = 0
total_score = 0

for _ in range(20):
    parts = input().split()
    name = parts[0]
    credit = float(parts[1])
    grade = parts[2]

    if grade == 'P':
        continue

    total_credit += credit
    total_score += credit * grades[grade]

if total_credit == 0:
    print(0)
else:
    print(total_score / total_credit)""",

    # 25501: 재귀의 귀재
    "25501": """def recursion(s, l, r, cnt):
    if l >= r:
        return 1, cnt
    elif s[l] != s[r]:
        return 0, cnt
    else:
        return recursion(s, l + 1, r - 1, cnt + 1)

def is_palindrome(s):
    return recursion(s, 0, len(s) - 1, 1)

t = int(input())
for _ in range(t):
    s = input().strip()
    result, count = is_palindrome(s)
    print(result, count)""",

    # 28065: SW 수열 구하기
    "28065": """n = int(input())
result = list(range(1, n + 1))
if n >= 2:
    result[0], result[1] = result[1], result[0]
print(' '.join(map(str, result)))""",

    # 30618: donstructive
    "30618": """n = int(input())
result = list(range(2, n + 1)) + [1]
print(' '.join(map(str, result)))""",

    # 34068: 이진 탐색
    "34068": """n, target = map(int, input().split())
arr = list(map(int, input().split()))
left, right = 0, n - 1
found = False
while left <= right:
    mid = (left + right) // 2
    if arr[mid] == target:
        found = True
        break
    elif arr[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
print("YES" if found else "NO")""",

    # 34069: 분수 배낭
    "34069": """n, w = map(int, input().split())
items = []
for _ in range(n):
    weight, value = map(int, input().split())
    items.append((value / weight, weight, value))
items.sort(reverse=True)

total_value = 0
remaining = w
for ratio, weight, value in items:
    if remaining >= weight:
        total_value += value
        remaining -= weight
    else:
        total_value += ratio * remaining
        break
print(f'{total_value:.2f}')""",

    # 34098: 조합
    "34098": """def combinations(arr, r, start, current, results):
    if len(current) == r:
        results.append(current[:])
        return
    for i in range(start, len(arr)):
        current.append(arr[i])
        combinations(arr, r, i + 1, current, results)
        current.pop()

n, r = map(int, input().split())
arr = list(map(int, input().split()))
results = []
combinations(arr, r, 0, [], results)
for combo in results:
    print(' '.join(map(str, combo)))""",

    # 34099: 부분집합
    "34099": """def subsets(arr, idx, current, results):
    if idx == len(arr):
        if current:
            results.append(current[:])
        return
    subsets(arr, idx + 1, current, results)
    current.append(arr[idx])
    subsets(arr, idx + 1, current, results)
    current.pop()

n = int(input())
arr = list(map(int, input().split()))
results = []
subsets(arr, 0, [], results)
results.sort(key=lambda x: (len(x), x))
for subset in results:
    print(' '.join(map(str, subset)))""",

    # 34116: 최단 경로 BFS
    "34116": """from collections import deque
import sys
input = sys.stdin.readline

n, m, start = map(int, input().split())
graph = [[] for _ in range(n + 1)]
for _ in range(m):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

dist = [-1] * (n + 1)
dist[start] = 0
queue = deque([start])
while queue:
    node = queue.popleft()
    for next_node in graph[node]:
        if dist[next_node] == -1:
            dist[next_node] = dist[node] + 1
            queue.append(next_node)

result = [str(d if d != -1 else -1) for d in dist[1:]]
print(' '.join(result))""",

    # 34123: 경로 존재 여부
    "34123": """from collections import deque

n, target = map(int, input().split())
arr = [int(input()) for _ in range(n)]

# BFS: 인덱스 0부터 시작
visited = [False] * n
queue = deque([0])
visited[0] = True
count = 0

while queue:
    idx = queue.popleft()
    if arr[idx] == target:
        count += 1
        continue
    for next_idx in [idx - 1, idx + 1]:
        if 0 <= next_idx < n and not visited[next_idx]:
            visited[next_idx] = True
            queue.append(next_idx)

print(count)""",

    # 34175: 유니온 파인드
    "34175": """import sys
input = sys.stdin.readline

def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

def union(parent, rank, x, y):
    px, py = find(parent, x), find(parent, y)
    if px == py:
        return
    if rank[px] < rank[py]:
        parent[px] = py
    elif rank[px] > rank[py]:
        parent[py] = px
    else:
        parent[py] = px
        rank[px] += 1

n, m = map(int, input().split())
parent = list(range(n + 1))
rank_arr = [0] * (n + 1)

for _ in range(m):
    a, b = map(int, input().split())
    union(parent, rank_arr, a, b)

x, y = map(int, input().split())
print("YES" if find(parent, x) == find(parent, y) else "NO")""",

    # 34199: 구간 합 구하기 (업데이트 포함)
    "34199": """import sys
input = sys.stdin.readline

def build(arr, tree, node, start, end):
    if start == end:
        tree[node] = arr[start]
    else:
        mid = (start + end) // 2
        build(arr, tree, node * 2, start, mid)
        build(arr, tree, node * 2 + 1, mid + 1, end)
        tree[node] = tree[node * 2] + tree[node * 2 + 1]

def update(tree, node, start, end, idx, diff):
    if idx < start or idx > end:
        return
    tree[node] += diff
    if start != end:
        mid = (start + end) // 2
        update(tree, node * 2, start, mid, idx, diff)
        update(tree, node * 2 + 1, mid + 1, end, idx, diff)

def query(tree, node, start, end, left, right):
    if left > end or right < start:
        return 0
    if left <= start and end <= right:
        return tree[node]
    mid = (start + end) // 2
    return query(tree, node * 2, start, mid, left, right) + query(tree, node * 2 + 1, mid + 1, end, left, right)

n, q = map(int, input().split())
arr = [0] + list(map(int, input().split()))
tree = [0] * (4 * n)
build(arr, tree, 1, 1, n)

for _ in range(q):
    line = list(map(int, input().split()))
    if line[0] == 1:
        idx, val = line[1], line[2]
        diff = val - arr[idx]
        arr[idx] = val
        update(tree, 1, 1, n, idx, diff)
    else:
        l, r = line[1], line[2]
        print(query(tree, 1, 1, n, l, r))""",

    # 35009: 약수의 합
    "35009": """n = int(input())
nums = list(map(int, input().split()))
total = 0
for num in nums:
    for i in range(1, num + 1):
        if num % i == 0:
            total += i
print(total)""",

    # 36009: 문자 빈도수
    "36009": """s = input().strip()
freq = {}
for c in s:
    freq[c] = freq.get(c, 0) + 1
result = ' '.join(f'{c}:{cnt}' for c, cnt in sorted(freq.items()))
print(result)""",

    # 36022: 값 기준 정렬
    "36022": """n = int(input())
items = []
for _ in range(n):
    parts = input().split()
    items.append((parts[0], int(parts[1])))
items.sort(key=lambda x: x[1])
print(' '.join(item[0] for item in items))""",

    # 34674: 소수판별
    "34674": """def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

n = int(input())
for _ in range(n):
    num = int(input())
    print("YES" if is_prime(num) else "NO")""",

    # 34675: 중첩루프
    "34675": """n = int(input())
total = 0
for i in range(1, n + 1):
    for j in range(1, n + 1):
        total += i * j
print(total)""",

    # 34676: 리스트
    "34676": """n = int(input())
arr = list(map(int, input().split()))
print(sum(arr))
print(max(arr))
print(min(arr))""",

    # 34678: 중복제거
    "34678": """n = int(input())
arr = list(map(int, input().split()))
result = sorted(set(arr))
print(' '.join(map(str, result)))""",

    # 34681: 중복제거2
    "34681": """n = int(input())
arr = list(map(int, input().split()))
seen = set()
result = []
for x in arr:
    if x not in seen:
        seen.add(x)
        result.append(x)
print(' '.join(map(str, result)))""",

    # 34682: 중첩루프2
    "34682": """n, m = map(int, input().split())
for i in range(1, n + 1):
    row = []
    for j in range(1, m + 1):
        row.append(str(i * j))
    print(' '.join(row))""",

    # 34683: 합찾기
    "34683": """n = int(input())
arr = list(map(int, input().split()))
target = int(input())
for i in range(n):
    for j in range(i + 1, n):
        if arr[i] + arr[j] == target:
            print(i, j)
            exit()
print(-1)""",

    # 34684: 큐 시뮬레이션
    "34684": """from collections import deque
n = int(input())
queue = deque()
for _ in range(n):
    line = input().split()
    if line[0] == 'push':
        queue.append(int(line[1]))
    elif line[0] == 'pop':
        if queue:
            print(queue.popleft())
        else:
            print(-1)
    elif line[0] == 'front':
        if queue:
            print(queue[0])
        else:
            print(-1)
    elif line[0] == 'size':
        print(len(queue))
    elif line[0] == 'empty':
        print(0 if queue else 1)""",

    # 31836: 피보나치
    "31836": """n = int(input())
if n <= 2:
    print(1)
else:
    fib = [0, 1, 1]
    for i in range(3, n + 1):
        fib.append(fib[-1] + fib[-2])
    print(fib[n])
print(1)
for i in range(1, n + 1):
    print(i)""",
}


# 수정 적용
fixed_count = 0
failed_list = []

for problem in data:
    pid = str(problem['problem_id'])
    if pid in FIXED_SOLUTIONS:
        new_code = FIXED_SOLUTIONS[pid]

        # 테스트
        ex = problem.get('examples', [{}])[0]
        success, actual, err = test_solution(new_code, ex.get('input', ''), ex.get('output', ''))

        if success:
            problem['solutions'][0]['solution_code'] = new_code
            fixed_count += 1
            print(f"✓ Fixed [{pid}] {problem['title']}")
        else:
            failed_list.append({
                'pid': pid,
                'title': problem['title'],
                'expected': ex.get('output', '')[:80],
                'actual': actual[:80] if actual else 'N/A',
                'error': err[:100] if err else 'Wrong Answer'
            })
            print(f"✗ Failed [{pid}] {problem['title']}")

print(f"\nFixed: {fixed_count}")
print(f"Failed: {len(failed_list)}")

if failed_list:
    print("\n=== Failed details ===")
    for f in failed_list[:20]:
        print(f"\n[{f['pid']}] {f['title']}")
        print(f"  Expected: {f['expected']}")
        print(f"  Actual: {f['actual']}")
        print(f"  Error: {f['error']}")

# 저장
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved to: {output_path}")
