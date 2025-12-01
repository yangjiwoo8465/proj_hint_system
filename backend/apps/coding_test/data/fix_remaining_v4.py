"""
남은 문제 수정 - V4
쉬운 문제들 집중 수정
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


FIXED_SOLUTIONS = {
    # 1932: 정수 삼각형 - 역방향 (아래에서 위로 가면서 합 최대)
    # 입력: 위에서 아래로 주어짐, 아래에서 위로 올라가며 합 최대 경로
    "1932": """import sys
input = sys.stdin.readline

n = int(input())
tri = [list(map(int, input().split())) for _ in range(n)]

# 아래에서 위로 DP
for i in range(n - 2, -1, -1):
    for j in range(i + 1):
        tri[i][j] += max(tri[i+1][j], tri[i+1][j+1])

print(tri[0][0])
""",

    # 2169: 로봇 탐사 - 위로 이동 불가 (왼쪽, 오른쪽, 아래만)
    "2169": """import sys
input = sys.stdin.readline

n, m = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(n)]

INF = float('-inf')
dp = [[INF] * m for _ in range(n)]

# 첫 행: 왼쪽에서만 올 수 있음
dp[0][0] = board[0][0]
for j in range(1, m):
    dp[0][j] = dp[0][j-1] + board[0][j]

# 나머지 행: 위에서 오거나 + 같은 행에서 좌우로 이동
for i in range(1, n):
    # 위에서 내려오는 값
    from_top = [dp[i-1][j] + board[i][j] for j in range(m)]

    # 왼쪽에서 오는 경우
    left = [INF] * m
    left[0] = from_top[0]
    for j in range(1, m):
        left[j] = max(from_top[j], left[j-1] + board[i][j])

    # 오른쪽에서 오는 경우
    right = [INF] * m
    right[m-1] = from_top[m-1]
    for j in range(m-2, -1, -1):
        right[j] = max(from_top[j], right[j+1] + board[i][j])

    for j in range(m):
        dp[i][j] = max(left[j], right[j])

print(dp[n-1][m-1])
""",

    # 2206: 벽 부수고 이동하기 - 2개까지 부술 수 있음
    "2206": """import sys
from collections import deque
input = sys.stdin.readline

n, m = map(int, input().split())
board = [input().strip() for _ in range(n)]

if n == 1 and m == 1:
    print(1)
else:
    # BFS with state (x, y, broken_count)
    INF = float('inf')
    MAX_BREAK = 2
    dist = [[[INF] * (MAX_BREAK + 1) for _ in range(m)] for _ in range(n)]
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
                elif board[nx][ny] == '1' and broken < MAX_BREAK and dist[nx][ny][broken + 1] > dist[x][y][broken] + 1:
                    dist[nx][ny][broken + 1] = dist[x][y][broken] + 1
                    queue.append((nx, ny, broken + 1))

    result = min(dist[n-1][m-1])
    print(result if result != INF else -1)
""",

    # 17404: RGB거리 2 - 첫번째와 마지막 집 색이 달라야 함 (순환)
    "17404": """import sys
input = sys.stdin.readline
INF = float('inf')

n = int(input())
cost = [list(map(int, input().split())) for _ in range(n)]

result = INF

# 첫 집의 색을 고정하고 DP
for first_color in range(3):
    dp = [[INF] * 3 for _ in range(n)]
    dp[0][first_color] = cost[0][first_color]

    for i in range(1, n):
        dp[i][0] = min(dp[i-1][1], dp[i-1][2]) + cost[i][0]
        dp[i][1] = min(dp[i-1][0], dp[i-1][2]) + cost[i][1]
        dp[i][2] = min(dp[i-1][0], dp[i-1][1]) + cost[i][2]

    # 마지막 집은 첫 집과 다른 색이어야 함
    for last_color in range(3):
        if last_color != first_color:
            result = min(result, dp[n-1][last_color])

print(result)
""",

    # 11062: 카드 게임 - 게임 이론 DP
    "11062": """import sys
sys.setrecursionlimit(10000)
input = sys.stdin.readline

def solve():
    n = int(input())
    cards = list(map(int, input().split()))

    # dp[l][r] = 현재 턴인 사람이 [l, r] 구간에서 얻을 수 있는 최대 점수
    # 근우 턴: 점수 가져감, 명우 턴: 점수 안 가져감
    dp = {}

    def dfs(l, r, is_geun):
        if l > r:
            return 0
        if (l, r, is_geun) in dp:
            return dp[(l, r, is_geun)]

        if is_geun:
            # 근우는 최대화
            result = max(cards[l] + dfs(l + 1, r, False),
                        cards[r] + dfs(l, r - 1, False))
        else:
            # 명우는 근우 점수 최소화 (자기 점수 최대화하므로)
            result = min(dfs(l + 1, r, True), dfs(l, r - 1, True))

        dp[(l, r, is_geun)] = result
        return result

    return dfs(0, n - 1, True)

t = int(input())
for _ in range(t):
    print(solve())
""",

    # 4803: 트리 - 사이클 판별
    "4803": """import sys
input = sys.stdin.readline
sys.setrecursionlimit(1000000)

def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

def union(parent, a, b):
    pa, pb = find(parent, a), find(parent, b)
    if pa == pb:
        return False  # 사이클 발생
    parent[pb] = pa
    return True

case_num = 0
while True:
    line = input().split()
    n, m = int(line[0]), int(line[1])
    if n == 0 and m == 0:
        break

    case_num += 1
    parent = list(range(n + 1))
    has_cycle = [False] * (n + 1)  # 각 컴포넌트에 사이클이 있는지

    for _ in range(m):
        a, b = map(int, input().split())
        pa, pb = find(parent, a), find(parent, b)
        if pa == pb:
            has_cycle[pa] = True
        else:
            # 합치기
            if has_cycle[pa] or has_cycle[pb]:
                has_cycle[pa] = True
            parent[pb] = pa

    # 트리 개수 세기 (사이클이 없는 컴포넌트)
    tree_count = 0
    counted = set()
    for i in range(1, n + 1):
        root = find(parent, i)
        if root not in counted:
            counted.add(root)
            if not has_cycle[root]:
                tree_count += 1

    if tree_count == 0:
        print(f"Case {case_num}: No trees.")
    elif tree_count == 1:
        print(f"Case {case_num}: There is one tree.")
    else:
        print(f"Case {case_num}: A forest of {tree_count} trees.")
""",

    # 11779: 최소비용 구하기 2 - 경로 복원
    "11779": """import heapq
import sys
input = sys.stdin.readline

n = int(input())
m = int(input())

graph = [[] for _ in range(n + 1)]
for _ in range(m):
    u, v, w = map(int, input().split())
    graph[u].append((v, w))

start, end = map(int, input().split())

INF = float('inf')
dist = [INF] * (n + 1)
prev_node = [-1] * (n + 1)
dist[start] = 0

pq = [(0, start)]
while pq:
    d, u = heapq.heappop(pq)
    if d > dist[u]:
        continue
    for v, w in graph[u]:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            prev_node[v] = u
            heapq.heappush(pq, (dist[v], v))

# 경로 복원
path = []
cur = end
while cur != -1:
    path.append(cur)
    cur = prev_node[cur]
path.reverse()

print(dist[end])
print(len(path))
print(' '.join(map(str, path)))
""",

    # 13913: 숨바꼭질 4 - 경로 복원
    "13913": """from collections import deque

n, k = map(int, input().split())

if n >= k:
    print(n - k)
    print(' '.join(map(str, range(n, k - 1, -1))))
else:
    MAX = 200001
    prev_pos = [-1] * MAX
    prev_pos[n] = -2  # 시작점 표시

    queue = deque([n])
    while queue:
        cur = queue.popleft()
        if cur == k:
            break
        for nxt in [cur - 1, cur + 1, cur * 2]:
            if 0 <= nxt < MAX and prev_pos[nxt] == -1:
                prev_pos[nxt] = cur
                queue.append(nxt)

    # 경로 복원
    path = []
    cur = k
    while cur != -2:
        path.append(cur)
        cur = prev_pos[cur]
    path.reverse()

    print(len(path) - 1)
    print(' '.join(map(str, path)))
""",

    # 9019: DSLR
    "9019": """from collections import deque
import sys
input = sys.stdin.readline

def solve(a, b):
    if a == b:
        return ""

    visited = [False] * 10000
    visited[a] = True
    prev = [(-1, '')] * 10000  # (이전 숫자, 연산)

    queue = deque([a])
    while queue:
        cur = queue.popleft()

        # D
        d = (cur * 2) % 10000
        if not visited[d]:
            visited[d] = True
            prev[d] = (cur, 'D')
            if d == b:
                break
            queue.append(d)

        # S
        s = (cur - 1) % 10000
        if not visited[s]:
            visited[s] = True
            prev[s] = (cur, 'S')
            if s == b:
                break
            queue.append(s)

        # L
        l = (cur % 1000) * 10 + cur // 1000
        if not visited[l]:
            visited[l] = True
            prev[l] = (cur, 'L')
            if l == b:
                break
            queue.append(l)

        # R
        r = (cur % 10) * 1000 + cur // 10
        if not visited[r]:
            visited[r] = True
            prev[r] = (cur, 'R')
            if r == b:
                break
            queue.append(r)

    # 경로 복원
    path = []
    cur = b
    while prev[cur][0] != -1:
        path.append(prev[cur][1])
        cur = prev[cur][0]
    return ''.join(reversed(path))

t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    print(solve(a, b))
""",

    # 24480: DFS - 내림차순 방문 순서
    "24480": """import sys
sys.setrecursionlimit(200000)
input = sys.stdin.readline

n, m, r = map(int, input().split())
graph = [[] for _ in range(n + 1)]
for _ in range(m):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

# 내림차순 정렬
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
    print(visited[i])
""",

    # 25501: 재귀의 귀재 - 호출 횟수
    "25501": """def recursion(s, l, r, cnt):
    cnt[0] += 1
    if l >= r:
        return 1
    elif s[l] != s[r]:
        return 0
    else:
        return recursion(s, l + 1, r - 1, cnt)

def is_palindrome(s):
    cnt = [0]
    result = recursion(s, 0, len(s) - 1, cnt)
    return result, cnt[0]

t = int(input())
for _ in range(t):
    s = input().strip()
    result, cnt = is_palindrome(s)
    print(result, cnt)
""",

    # 11780: 플로이드 2 - 경로 복원
    "11780": """import sys
input = sys.stdin.readline
INF = float('inf')

n = int(input())
m = int(input())

dist = [[INF] * (n + 1) for _ in range(n + 1)]
nxt = [[0] * (n + 1) for _ in range(n + 1)]

for i in range(n + 1):
    dist[i][i] = 0

for _ in range(m):
    a, b, c = map(int, input().split())
    if c < dist[a][b]:
        dist[a][b] = c
        nxt[a][b] = b

# Floyd-Warshall
for k in range(1, n + 1):
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if dist[i][k] != INF and dist[k][j] != INF:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]

# 거리 행렬 출력
for i in range(1, n + 1):
    row = []
    for j in range(1, n + 1):
        row.append(str(0 if dist[i][j] == INF else dist[i][j]))
    print(' '.join(row))

# 경로 출력
for i in range(1, n + 1):
    for j in range(1, n + 1):
        if i == j or dist[i][j] == INF:
            print(0)
        else:
            path = [i]
            cur = i
            while cur != j:
                cur = nxt[cur][j]
                path.append(cur)
            print(len(path), ' '.join(map(str, path)))
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
enemy = [[] for _ in range(n + 1)]

for _ in range(m):
    parts = input().split()
    rel = parts[0]
    p, q = int(parts[1]), int(parts[2])

    if rel == 'F':
        union(parent, p, q)
    else:  # E
        enemy[p].append(q)
        enemy[q].append(p)

# 적의 적은 친구
for i in range(1, n + 1):
    for j in range(len(enemy[i])):
        for k in range(j + 1, len(enemy[i])):
            union(parent, enemy[i][j], enemy[i][k])

teams = set()
for i in range(1, n + 1):
    teams.add(find(parent, i))

print(len(teams))
""",

    # 22967: 구름다리 (입력 형식 확인 필요)
    "22967": """import sys
from collections import deque
input = sys.stdin.readline

line = input().split()
n, m = int(line[0]), int(line[1])
k = int(line[2]) if len(line) > 2 else int(input())

graph = [[] for _ in range(n + 1)]
for _ in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

# BFS
parent = [-1] * (n + 1)
visited = [False] * (n + 1)
queue = deque([1])
visited[1] = True

while queue:
    node = queue.popleft()
    if node == n:
        break
    for nxt in graph[node]:
        if not visited[nxt]:
            visited[nxt] = True
            parent[nxt] = node
            queue.append(nxt)

if not visited[n]:
    print(-1)
else:
    path = []
    cur = n
    while cur != -1:
        path.append(cur)
        cur = parent[cur]
    path.reverse()

    # 중간 노드 수 (첫 노드와 마지막 노드 제외)
    print(len(path) - 2)
    # 다리 수 (간선 수)
    print(len(path) - 1)
    print(' '.join(map(str, path)))
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
                'expected': out[:80],
                'actual': actual[:80] if actual else 'N/A',
                'error': err[:120] if err else 'Wrong Answer'
            })
            print(f"✗ Failed [{pid}] {problem['title']}")

print(f"\nTotal Fixed: {fixed_count}")
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
