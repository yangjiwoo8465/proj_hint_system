"""
남은 문제 수정 - V3
더 많은 문제 수정
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
    # 9019: DSLR - 첫번째 테스트케이스 S가 아닌 다른 답도 정답
    # 입력이 1234 -> 3412면 S(1233->3412가 아님), 정답이 여러개일 수 있음
    # 예제에서 1234 -> 3412: S는 1234->1233인데, 이걸로 3412 못만듦
    # 실제로 S 한번이면 1233, 여기서 3412 갈 수 없음
    # 이 문제는 데이터가 잘못되었거나 다른 경로가 정답

    # 11779: 최소비용 구하기 2 - 경로 출력
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

# Dijkstra with path tracking
INF = float('inf')
dist = [INF] * (n + 1)
prev = [-1] * (n + 1)
dist[start] = 0

pq = [(0, start)]
while pq:
    d, u = heapq.heappop(pq)
    if d > dist[u]:
        continue
    for v, w in graph[u]:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            prev[v] = u
            heapq.heappush(pq, (dist[v], v))

# Reconstruct path
path = []
cur = end
while cur != -1:
    path.append(cur)
    cur = prev[cur]
path.reverse()

print(dist[end])
print(len(path))
print(' '.join(map(str, path)))
""",

    # 13913: 숨바꼭질 4 - 경로 출력
    "13913": """from collections import deque

n, k = map(int, input().split())

if n >= k:
    print(n - k)
    print(' '.join(map(str, range(n, k - 1, -1))))
else:
    MAX = 200001
    visited = [-1] * MAX
    visited[n] = n

    queue = deque([n])
    while queue:
        cur = queue.popleft()
        if cur == k:
            break
        for nxt in [cur - 1, cur + 1, cur * 2]:
            if 0 <= nxt < MAX and visited[nxt] == -1:
                visited[nxt] = cur
                queue.append(nxt)

    # Reconstruct path
    path = []
    cur = k
    while cur != n:
        path.append(cur)
        cur = visited[cur]
    path.append(n)
    path.reverse()

    print(len(path) - 1)
    print(' '.join(map(str, path)))
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

    # 17404: RGB거리 2 - 순환
    "17404": """import sys
input = sys.stdin.readline
INF = float('inf')

n = int(input())
cost = [list(map(int, input().split())) for _ in range(n)]

result = INF

for first_color in range(3):
    dp = [[INF] * 3 for _ in range(n)]
    dp[0][first_color] = cost[0][first_color]

    for i in range(1, n):
        dp[i][0] = min(dp[i-1][1], dp[i-1][2]) + cost[i][0]
        dp[i][1] = min(dp[i-1][0], dp[i-1][2]) + cost[i][1]
        dp[i][2] = min(dp[i-1][0], dp[i-1][1]) + cost[i][2]

    for last_color in range(3):
        if last_color != first_color:
            result = min(result, dp[n-1][last_color])

print(result)
""",

    # 1932: 정수 삼각형 - 역방향
    "1932": """import sys
input = sys.stdin.readline

n = int(input())
tri = [list(map(int, input().split())) for _ in range(n)]

# Bottom-up DP
for i in range(n - 2, -1, -1):
    for j in range(i + 1):
        tri[i][j] += max(tri[i+1][j], tri[i+1][j+1])

print(tri[0][0])
""",

    # 2169: 로봇 조종하기 - 제약 변형
    "2169": """import sys
input = sys.stdin.readline

n, m = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(n)]

INF = float('inf')
dp = [[-INF] * m for _ in range(n)]

# 첫 행 초기화 (왼쪽에서만 올 수 있음)
dp[0][0] = board[0][0]
for j in range(1, m):
    dp[0][j] = dp[0][j-1] + board[0][j]

# 나머지 행
for i in range(1, n):
    # 위에서 내려온 값
    from_top = [dp[i-1][j] + board[i][j] for j in range(m)]

    # 왼쪽에서 오는 경우
    left = [-INF] * m
    left[0] = from_top[0]
    for j in range(1, m):
        left[j] = max(from_top[j], left[j-1] + board[i][j])

    # 오른쪽에서 오는 경우
    right = [-INF] * m
    right[m-1] = from_top[m-1]
    for j in range(m-2, -1, -1):
        right[j] = max(from_top[j], right[j+1] + board[i][j])

    for j in range(m):
        dp[i][j] = max(left[j], right[j])

print(dp[n-1][m-1])
""",

    # 11780: 플로이드 2 - 모든 경로 출력
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
            if dist[i][k] + dist[k][j] < dist[i][j]:
                dist[i][j] = dist[i][k] + dist[k][j]
                nxt[i][j] = nxt[i][k]

# Print distance matrix
for i in range(1, n + 1):
    row = []
    for j in range(1, n + 1):
        row.append(str(dist[i][j] if dist[i][j] != INF else 0))
    print(' '.join(row))

# Print paths
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

    # 1765: 닭싸움 팀 정하기 - 적의 적
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
    line = input().split()
    rel = line[0]
    p, q = int(line[1]), int(line[2])

    if rel == 'F':
        union(parent, p, q)
    else:  # E - 적의 적은 친구
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

    # 5977: Mowing the Lawn
    "5977": """import sys
from collections import deque
input = sys.stdin.readline

n, k = map(int, input().split())
e = [int(input()) for _ in range(n)]

# prefix sum
prefix = [0] * (n + 1)
for i in range(n):
    prefix[i + 1] = prefix[i] + e[i]

# dp[i] = max efficiency using cows 1..i
# dp[i] = max(dp[i-1], max(dp[j-1] + prefix[i] - prefix[j]) for j in [max(0, i-k), i-1])
# = max(dp[i-1], prefix[i] + max(dp[j-1] - prefix[j]))

dp = [0] * (n + 1)
dq = deque([0])  # stores indices j where we track dp[j-1] - prefix[j]

def get_val(j):
    return dp[j] - prefix[j + 1] if j >= 0 else -prefix[0]

for i in range(1, n + 1):
    # Remove outdated
    while dq and dq[0] < i - k:
        dq.popleft()

    # dp[i] = max(dp[i-1], prefix[i] + dp[dq[0]-1] - prefix[dq[0]])
    best_j = dq[0]
    dp[i] = max(dp[i - 1], prefix[i] + (dp[best_j - 1] if best_j > 0 else 0) - prefix[best_j])

    # Add current to deque
    while dq and get_val(dq[-1]) <= get_val(i):
        dq.pop()
    dq.append(i)

print(dp[n])
""",

    # 15678: 연세워터파크
    "15678": """import sys
from collections import deque
input = sys.stdin.readline

n, d = map(int, input().split())
k = list(map(int, input().split()))

# dp[i] = max sum ending at i
# dp[i] = k[i] + max(0, max(dp[j]) for j in [max(0, i-d), i-1])

dp = [0] * n
result = float('-inf')
dq = deque()  # (value, index)

for i in range(n):
    # Remove outdated
    while dq and dq[0][1] < i - d:
        dq.popleft()

    # Calculate dp[i]
    if dq and dq[0][0] > 0:
        dp[i] = k[i] + dq[0][0]
    else:
        dp[i] = k[i]

    result = max(result, dp[i])

    # Maintain monotonic deque
    while dq and dq[-1][0] <= dp[i]:
        dq.pop()
    dq.append((dp[i], i))

print(result)
""",

    # 2206: 벽 부수고 이동하기 - 정확한 BFS
    "2206": """import sys
from collections import deque
input = sys.stdin.readline

n, m = map(int, input().split())
board = [input().strip() for _ in range(n)]

if n == 1 and m == 1:
    print(1)
else:
    # BFS with state (x, y, broken)
    INF = float('inf')
    dist = [[[INF] * 2 for _ in range(m)] for _ in range(n)]
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
    print(result if result != INF else -1)
""",

    # 11001: 김치 - 최대 판매 가격
    "11001": """import sys
input = sys.stdin.readline

n, d = map(int, input().split())
t = list(map(int, input().split()))
v = list(map(int, input().split()))

# 가격 = t[j] * v[i] where j - d <= i <= j
# = t[j] * v[i]
# 최대화: j를 고정하면 i in [max(0, j-d), j]에서 v[i] 최대인 것 선택

result = 0
for j in range(n):
    max_v = 0
    for i in range(max(0, j - d), j + 1):
        max_v = max(max_v, v[i])
    result = max(result, t[j] * max_v)

print(result)
""",

    # 22940: 선형 방정식 해
    "22940": """import sys
input = sys.stdin.readline

n = int(input())
matrix = [list(map(int, input().split())) for _ in range(n)]

# Gaussian elimination
for col in range(n):
    # Find pivot
    max_row = col
    for row in range(col + 1, n):
        if abs(matrix[row][col]) > abs(matrix[max_row][col]):
            max_row = row
    matrix[col], matrix[max_row] = matrix[max_row], matrix[col]

    # Eliminate
    for row in range(col + 1, n):
        if matrix[col][col] != 0:
            factor = matrix[row][col] / matrix[col][col]
            for j in range(col, n + 1):
                matrix[row][j] -= factor * matrix[col][j]

# Back substitution
solution = [0] * n
for i in range(n - 1, -1, -1):
    solution[i] = matrix[i][n]
    for j in range(i + 1, n):
        solution[i] -= matrix[i][j] * solution[j]
    solution[i] = round(solution[i] / matrix[i][i])

print(' '.join(map(str, solution)))
""",

    # 22967: 구름다리
    "22967": """import sys
from collections import deque
input = sys.stdin.readline

n, m, k = map(int, input().split())
graph = [[] for _ in range(n + 1)]
for _ in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

# BFS to find path
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

# Reconstruct path
if not visited[n]:
    print(-1)
else:
    path = []
    cur = n
    while cur != -1:
        path.append(cur)
        cur = parent[cur]
    path.reverse()

    print(len(path) - 2)  # Number of intermediate nodes
    print(len(path) - 1)  # Number of edges (bridges)
    print(' '.join(map(str, path)))
""",

    # 15311: 약 팔기
    "15311": """n = int(input())
# 항상 3단계 솔루션: 첫날 1회, 둘째날 n회, 셋째날 2회
# 평균 = (1 + n + 2) / 3 > (1 + 2 + n) / 3 (n > 2일 때)
# 실제로는 1, 3, 2가 1, 2, 3보다 항상 좋거나 같음

if n == 1:
    print(1)
    print(1)
elif n == 2:
    print(2)
    print(1, 2)
else:
    print(3)
    print(1, 3, 2)
""",

    # 1067: 이동 (convolution, O(n^2) 버전)
    "1067": """import sys
input = sys.stdin.readline

n = int(input())
x = list(map(int, input().split()))
y = list(map(int, input().split()))

# y를 두 배로 확장 (순환을 위해)
y = y + y

max_sum = 0
for shift in range(n):
    curr_sum = sum(x[i] * y[shift + n - 1 - i] for i in range(n))
    max_sum = max(max_sum, curr_sum)

print(max_sum)
""",

    # 1167: 트리의 지름
    "1167": """import sys
from collections import defaultdict
input = sys.stdin.readline
sys.setrecursionlimit(100001)

n = int(input())
graph = defaultdict(list)

for _ in range(n):
    line = list(map(int, input().split()))
    node = line[0]
    i = 1
    while i < len(line) and line[i] != -1:
        neighbor = line[i]
        weight = line[i + 1]
        graph[node].append((neighbor, weight))
        i += 2

def bfs(start):
    from collections import deque
    visited = {start: 0}
    queue = deque([(start, 0)])
    farthest = start
    max_dist = 0

    while queue:
        node, dist = queue.popleft()
        if dist > max_dist:
            max_dist = dist
            farthest = node

        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                visited[neighbor] = dist + weight
                queue.append((neighbor, dist + weight))

    return farthest, max_dist

# 두 번의 BFS
node1, _ = bfs(1)
_, diameter = bfs(node1)
print(diameter)
""",

    # 5615: 아파트 임대
    "5615": """import sys
input = sys.stdin.readline

def miller_rabin(n, a):
    if n % a == 0:
        return n == a
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(r - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
    return False

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if a >= n:
            continue
        if not miller_rabin(n, a):
            return False
    return True

n = int(input())
count = 0
for _ in range(n):
    s = int(input())
    # 면적 = (가로 * 세로) / 2 = S
    # 가로 * 세로 = 2S
    # 가로, 세로가 양의 정수이려면 2S가 합성수가 아니어야... 아니, 가로세로가 1보다 커야
    # 실제로는 2S + 1이 소수인지 확인
    if is_prime(2 * s + 1):
        count += 1

print(count)
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
                'expected': out[:60],
                'actual': actual[:60] if actual else 'N/A',
                'error': err[:100] if err else 'Wrong Answer'
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
