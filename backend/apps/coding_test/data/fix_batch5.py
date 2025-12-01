"""
대량 문제 수정 배치 5 - 추가 문제들
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
    # 33919: 1부터 16까지 합
    "33919": """print(136)""",

    # 33923: 1부터 93까지 합
    "33923": """print(4371)""",

    # 25206: 너의 평점은 (소수점 6자리)
    "25206": """grades = {'A+': 4.5, 'A0': 4.0, 'B+': 3.5, 'B0': 3.0,
           'C+': 2.5, 'C0': 2.0, 'D+': 1.5, 'D0': 1.0, 'F': 0.0}

total_credit = 0
total_score = 0

for _ in range(20):
    parts = input().split()
    credit = float(parts[1])
    grade = parts[2]

    if grade == 'P':
        continue

    total_credit += credit
    total_score += credit * grades[grade]

if total_credit == 0:
    print('0.000000')
else:
    print(f'{total_score / total_credit:.6f}')""",

    # 1311: 할 일 정하기 1 (비트마스크 DP)
    "1311": """import sys
input = sys.stdin.readline
INF = float('inf')

n = int(input())
cost = []
for _ in range(n):
    cost.append(list(map(int, input().split())))

dp = [INF] * (1 << n)
dp[0] = 0

for mask in range(1 << n):
    person = bin(mask).count('1')
    if person >= n:
        continue
    for job in range(n):
        if mask & (1 << job):
            continue
        new_mask = mask | (1 << job)
        dp[new_mask] = min(dp[new_mask], dp[mask] + cost[person][job])

print(dp[(1 << n) - 1])""",

    # 1167: 트리의 지름 (DFS 2번)
    "1167": """import sys
from collections import defaultdict
sys.setrecursionlimit(100001)
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

def dfs(start):
    visited = [-1] * (n + 1)
    visited[start] = 0
    stack = [start]
    max_dist = 0
    farthest = start

    while stack:
        node = stack.pop()
        for neighbor, weight in graph[node]:
            if visited[neighbor] == -1:
                visited[neighbor] = visited[node] + weight
                stack.append(neighbor)
                if visited[neighbor] > max_dist:
                    max_dist = visited[neighbor]
                    farthest = neighbor

    return farthest, max_dist

# 첫 번째 DFS: 임의의 노드에서 가장 먼 노드 찾기
node1, _ = dfs(1)
# 두 번째 DFS: 찾은 노드에서 가장 먼 거리 찾기
_, diameter = dfs(node1)
print(diameter)""",

    # 17472: 다리 만들기 2 (BFS + MST)
    "17472": """from collections import deque
import sys
input = sys.stdin.readline

def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

def union(parent, rank, a, b):
    pa, pb = find(parent, a), find(parent, b)
    if pa == pb:
        return False
    if rank[pa] < rank[pb]:
        parent[pa] = pb
    elif rank[pa] > rank[pb]:
        parent[pb] = pa
    else:
        parent[pb] = pa
        rank[pa] += 1
    return True

n, m = map(int, input().split())
grid = []
for _ in range(n):
    grid.append(list(map(int, input().split())))

# 섬 번호 매기기
island_num = 0
island = [[0] * m for _ in range(n)]
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

for i in range(n):
    for j in range(m):
        if grid[i][j] == 1 and island[i][j] == 0:
            island_num += 1
            queue = deque([(i, j)])
            island[i][j] = island_num
            while queue:
                x, y = queue.popleft()
                for d in range(4):
                    nx, ny = x + dx[d], y + dy[d]
                    if 0 <= nx < n and 0 <= ny < m and grid[nx][ny] == 1 and island[nx][ny] == 0:
                        island[nx][ny] = island_num
                        queue.append((nx, ny))

# 다리 찾기
edges = []
for i in range(n):
    for j in range(m):
        if island[i][j] == 0:
            continue
        start_island = island[i][j]
        for d in range(4):
            length = 0
            ni, nj = i + dx[d], j + dy[d]
            while 0 <= ni < n and 0 <= nj < m:
                if island[ni][nj] != 0:
                    if island[ni][nj] != start_island and length >= 2:
                        edges.append((length, start_island, island[ni][nj]))
                    break
                length += 1
                ni += dx[d]
                nj += dy[d]

# 크루스칼
edges.sort()
parent = list(range(island_num + 1))
rank_arr = [0] * (island_num + 1)
total = 0
count = 0

for length, a, b in edges:
    if union(parent, rank_arr, a, b):
        total += length
        count += 1
        if count == island_num - 1:
            break

if count == island_num - 1:
    print(total)
else:
    print(-1)""",

    # 11779: 최소비용 구하기 2 (다익스트라 + 경로 추적)
    "11779": """import heapq
import sys
input = sys.stdin.readline
INF = float('inf')

n = int(input())
m = int(input())
graph = [[] for _ in range(n + 1)]
for _ in range(m):
    a, b, c = map(int, input().split())
    graph[a].append((b, c))

start, end = map(int, input().split())

dist = [INF] * (n + 1)
parent = [-1] * (n + 1)
dist[start] = 0
pq = [(0, start)]

while pq:
    d, node = heapq.heappop(pq)
    if d > dist[node]:
        continue
    for next_node, cost in graph[node]:
        if dist[node] + cost < dist[next_node]:
            dist[next_node] = dist[node] + cost
            parent[next_node] = node
            heapq.heappush(pq, (dist[next_node], next_node))

print(dist[end])

path = []
cur = end
while cur != -1:
    path.append(cur)
    cur = parent[cur]
path.reverse()

print(len(path))
print(' '.join(map(str, path)))""",

    # 2150: 강한 연결 요소 (SCC)
    "2150": """import sys
sys.setrecursionlimit(100001)
input = sys.stdin.readline

def dfs(node):
    visited[node] = True
    for next_node in graph[node]:
        if not visited[next_node]:
            dfs(next_node)
    stack.append(node)

def reverse_dfs(node, scc_id):
    visited[node] = True
    scc[scc_id].append(node)
    for next_node in reverse_graph[node]:
        if not visited[next_node]:
            reverse_dfs(next_node, scc_id)

V, E = map(int, input().split())
graph = [[] for _ in range(V + 1)]
reverse_graph = [[] for _ in range(V + 1)]

for _ in range(E):
    a, b = map(int, input().split())
    graph[a].append(b)
    reverse_graph[b].append(a)

# 첫 번째 DFS
visited = [False] * (V + 1)
stack = []
for i in range(1, V + 1):
    if not visited[i]:
        dfs(i)

# 역방향 DFS
visited = [False] * (V + 1)
scc = []
while stack:
    node = stack.pop()
    if not visited[node]:
        scc.append([])
        reverse_dfs(node, len(scc) - 1)

# 결과 출력
print(len(scc))
for component in sorted([sorted(s) for s in scc]):
    print(' '.join(map(str, component)) + ' -1')""",

    # 2162: 선분 그룹
    "2162": """import sys
input = sys.stdin.readline

def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

def union(parent, rank, size, a, b):
    pa, pb = find(parent, a), find(parent, b)
    if pa == pb:
        return
    if rank[pa] < rank[pb]:
        parent[pa] = pb
        size[pb] += size[pa]
    else:
        parent[pb] = pa
        size[pa] += size[pb]
        if rank[pa] == rank[pb]:
            rank[pa] += 1

def ccw(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def on_segment(p, q, r):
    return min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1])

def intersect(s1, s2):
    p1, p2 = s1
    p3, p4 = s2
    d1 = ccw(p3, p4, p1)
    d2 = ccw(p3, p4, p2)
    d3 = ccw(p1, p2, p3)
    d4 = ccw(p1, p2, p4)

    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True

    if d1 == 0 and on_segment(p3, p1, p4):
        return True
    if d2 == 0 and on_segment(p3, p2, p4):
        return True
    if d3 == 0 and on_segment(p1, p3, p2):
        return True
    if d4 == 0 and on_segment(p1, p4, p2):
        return True

    return False

n = int(input())
segments = []
for _ in range(n):
    x1, y1, x2, y2 = map(int, input().split())
    segments.append(((x1, y1), (x2, y2)))

parent = list(range(n))
rank_arr = [0] * n
size = [1] * n

for i in range(n):
    for j in range(i + 1, n):
        if intersect(segments[i], segments[j]):
            union(parent, rank_arr, size, i, j)

groups = set()
max_size = 0
for i in range(n):
    p = find(parent, i)
    groups.add(p)
    max_size = max(max_size, size[p])

print(len(groups))
print(max_size)""",

    # 1069: 집으로 (수학)
    "1069": """import math

x, y, d, t = map(int, input().split())
dist = math.sqrt(x * x + y * y)

# 걷기
walk = dist

# 점프 n번 + 걷기
jump1 = (dist // d) * t + (dist % d)  # 점프 n번 + 남은 거리 걷기
jump2 = (dist // d + 1) * t  # 점프 n+1번

# 거리가 d보다 작을 때
if dist < d:
    # 점프 1번 후 돌아오기
    jump3 = t + (d - dist)
    # 점프 2번 (한 번 건너뛰고 돌아오기)
    jump4 = 2 * t
    result = min(walk, jump3, jump4)
else:
    result = min(walk, jump1, jump2)

print(result)""",

    # 1086: 박성원 (비트마스크 DP)
    "1086": """import sys
from math import gcd
input = sys.stdin.readline

n = int(input())
nums = [input().strip() for _ in range(n)]
k = int(input())

# 각 숫자를 k로 나눈 나머지
mods = [int(num) % k for num in nums]

# 10^len을 k로 나눈 나머지
powers = [pow(10, len(num), k) for num in nums]

# dp[mask][remainder] = mask에 해당하는 숫자들을 사용해서 나머지가 remainder인 경우의 수
dp = [[0] * k for _ in range(1 << n)]
dp[0][0] = 1

for mask in range(1 << n):
    for remainder in range(k):
        if dp[mask][remainder] == 0:
            continue
        for i in range(n):
            if mask & (1 << i):
                continue
            new_mask = mask | (1 << i)
            new_remainder = (remainder * powers[i] + mods[i]) % k
            dp[new_mask][new_remainder] += dp[mask][remainder]

# 전체 경우의 수 (n!)
factorial = 1
for i in range(1, n + 1):
    factorial *= i

# 결과
divisible = dp[(1 << n) - 1][0]
g = gcd(divisible, factorial)
print(f'{divisible // g}/{factorial // g}')""",

    # 1017: 소수 쌍
    "1017": """import sys
input = sys.stdin.readline

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def dfs(node, match, visited, adj):
    for next_node in adj[node]:
        if visited[next_node]:
            continue
        visited[next_node] = True
        if match[next_node] == -1 or dfs(match[next_node], match, visited, adj):
            match[next_node] = node
            return True
    return False

n = int(input())
nums = list(map(int, input().split()))

first = nums[0]
odd = [x for x in nums if x % 2 == 1]
even = [x for x in nums if x % 2 == 0]

# 첫 번째 수가 홀수면 짝수와 매칭, 짝수면 홀수와 매칭
if first % 2 == 1:
    left, right = odd, even
else:
    left, right = even, odd

result = []

for candidate in right:
    if not is_prime(first + candidate):
        continue

    # 이분 매칭
    adj = [[] for _ in range(len(left))]
    for i, l in enumerate(left):
        if l == first:
            if is_prime(l + candidate):
                adj[i].append(right.index(candidate))
        else:
            for j, r in enumerate(right):
                if is_prime(l + r):
                    adj[i].append(j)

    match = [-1] * len(right)
    match[right.index(candidate)] = left.index(first)

    matched = 1
    for i, l in enumerate(left):
        if l == first:
            continue
        visited = [False] * len(right)
        visited[right.index(candidate)] = True
        if dfs(i, match, visited, adj):
            matched += 1

    if matched == len(left):
        result.append(candidate)

if result:
    print(' '.join(map(str, sorted(result))))
else:
    print(-1)""",
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
    for f in failed_list[:15]:
        print(f"\n[{f['pid']}] {f['title']}")
        print(f"  Expected: {f['expected']}")
        print(f"  Actual: {f['actual']}")
        print(f"  Error: {f['error']}")

# 저장
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved to: {output_path}")
