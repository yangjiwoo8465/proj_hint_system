"""
추가 문제 수정 배치
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
    # 1932: 정수 피라미드 - 역방향 DP
    "1932": """n = int(input())
triangle = []
for _ in range(n):
    triangle.append(list(map(int, input().split())))

for i in range(n-2, -1, -1):
    for j in range(i+1):
        triangle[i][j] += max(triangle[i+1][j], triangle[i+1][j+1])

print(triangle[0][0])""",

    # 5073: 삼각형과 세 변 - 둔각 판별
    "5073": """while True:
    sides = list(map(int, input().split()))
    if sides == [0, 0, 0]:
        break
    sides.sort()
    a, b, c = sides
    if a + b <= c:
        print('Invalid')
    elif a == b == c:
        print('Equilateral')
    elif a*a + b*b == c*c:
        print('Right')
    elif a*a + b*b < c*c:
        print('Obtuse')
    elif a == b or b == c or a == c:
        print('Isosceles')
    else:
        print('Scalene')""",

    # 11047: 동전 0 - 그리디
    "11047": """n, k = map(int, input().split())
coins = [int(input()) for _ in range(n)]
count = 0
for coin in reversed(coins):
    count += k // coin
    k %= coin
print(count)""",

    # 11660: 구간 곱 구하기 5 -> 합 구하기로 수정 (문제 제목이 잘못됨)
    "11660": """import sys
input = sys.stdin.readline
n, m = map(int, input().split())
arr = [[0] * (n + 1)]
for _ in range(n):
    arr.append([0] + list(map(int, input().split())))

# 누적합
prefix = [[0] * (n + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, n + 1):
        prefix[i][j] = arr[i][j] + prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1]

for _ in range(m):
    x1, y1, x2, y2 = map(int, input().split())
    result = prefix[x2][y2] - prefix[x1-1][y2] - prefix[x2][y1-1] + prefix[x1-1][y1-1]
    print(result)""",

    # 11723: 집합 - 비트마스크
    "11723": """import sys
input = sys.stdin.readline
m = int(input())
s = 0
for _ in range(m):
    line = input().split()
    op = line[0]
    if op == 'add':
        x = int(line[1])
        s |= (1 << x)
    elif op == 'remove':
        x = int(line[1])
        s &= ~(1 << x)
    elif op == 'check':
        x = int(line[1])
        print(1 if s & (1 << x) else 0)
    elif op == 'toggle':
        x = int(line[1])
        s ^= (1 << x)
    elif op == 'all':
        s = (1 << 21) - 1
    elif op == 'empty':
        s = 0""",

    # 13305: 주유소
    "13305": """n = int(input())
distances = list(map(int, input().split()))
prices = list(map(int, input().split()))
total = 0
min_price = prices[0]
for i in range(n - 1):
    min_price = min(min_price, prices[i])
    total += min_price * distances[i]
print(total)""",

    # 14425: 문자열 집합 - 트라이
    "14425": """import sys
input = sys.stdin.readline
n, m = map(int, input().split())
s = set()
for _ in range(n):
    s.add(input().strip())
count = 0
for _ in range(m):
    if input().strip() in s:
        count += 1
print(count)""",

    # 14888: 연산자 끼워넣기
    "14888": """from itertools import permutations

n = int(input())
nums = list(map(int, input().split()))
ops = list(map(int, input().split()))  # +, -, *, /

op_list = []
for i, cnt in enumerate(ops):
    op_list.extend([i] * cnt)

max_val = -1e10
min_val = 1e10

for perm in set(permutations(op_list)):
    result = nums[0]
    for i, op in enumerate(perm):
        if op == 0:
            result += nums[i + 1]
        elif op == 1:
            result -= nums[i + 1]
        elif op == 2:
            result *= nums[i + 1]
        else:
            if result < 0:
                result = -(-result // nums[i + 1])
            else:
                result //= nums[i + 1]
    max_val = max(max_val, result)
    min_val = min(min_val, result)

print(int(max_val))
print(int(min_val))""",

    # 14889: 스타트와 링크
    "14889": """from itertools import combinations

n = int(input())
s = []
for _ in range(n):
    s.append(list(map(int, input().split())))

min_diff = float('inf')
all_players = set(range(n))

for team1 in combinations(range(n), n // 2):
    team1 = set(team1)
    team2 = all_players - team1

    score1 = sum(s[i][j] for i in team1 for j in team1)
    score2 = sum(s[i][j] for i in team2 for j in team2)

    min_diff = min(min_diff, abs(score1 - score2))

print(min_diff)""",

    # 24444: BFS - 방문 순서 (오름차순)
    "24444": """from collections import deque
import sys
input = sys.stdin.readline

n, m, r = map(int, input().split())
graph = [[] for _ in range(n + 1)]
for _ in range(m):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

for i in range(n + 1):
    graph[i].sort()

visited = [0] * (n + 1)
order = 1
queue = deque([r])
visited[r] = order

while queue:
    node = queue.popleft()
    for next_node in graph[node]:
        if visited[next_node] == 0:
            order += 1
            visited[next_node] = order
            queue.append(next_node)

for i in range(1, n + 1):
    print(visited[i])""",

    # 24480: DFS - 방문 순서 (내림차순)
    "24480": """import sys
sys.setrecursionlimit(100000)
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

    # 25184: 동가수열 구하기
    "25184": """n = int(input())
result = list(range(1, n + 1))
print(' '.join(map(str, result)))""",

    # 2164: 카드2 - 큐
    "2164": """from collections import deque
n = int(input())
cards = deque(range(1, n + 1))
while len(cards) > 1:
    cards.popleft()
    cards.append(cards.popleft())
print(cards[0])""",

    # 1874: 스택 수열
    "1874": """n = int(input())
seq = [int(input()) for _ in range(n)]
stack = []
result = []
current = 1
possible = True

for num in seq:
    while current <= num:
        stack.append(current)
        result.append('+')
        current += 1
    if stack[-1] == num:
        stack.pop()
        result.append('-')
    else:
        possible = False
        break

if possible:
    print('\\n'.join(result))
else:
    print('NO')""",

    # 10828: 스택
    "10828": """import sys
input = sys.stdin.readline
n = int(input())
stack = []
result = []
for _ in range(n):
    cmd = input().split()
    if cmd[0] == 'push':
        stack.append(int(cmd[1]))
    elif cmd[0] == 'pop':
        result.append(str(stack.pop() if stack else -1))
    elif cmd[0] == 'size':
        result.append(str(len(stack)))
    elif cmd[0] == 'empty':
        result.append('1' if not stack else '0')
    elif cmd[0] == 'top':
        result.append(str(stack[-1] if stack else -1))
print('\\n'.join(result))""",

    # 10845: 큐
    "10845": """import sys
from collections import deque
input = sys.stdin.readline
n = int(input())
queue = deque()
result = []
for _ in range(n):
    cmd = input().split()
    if cmd[0] == 'push':
        queue.append(int(cmd[1]))
    elif cmd[0] == 'pop':
        result.append(str(queue.popleft() if queue else -1))
    elif cmd[0] == 'size':
        result.append(str(len(queue)))
    elif cmd[0] == 'empty':
        result.append('1' if not queue else '0')
    elif cmd[0] == 'front':
        result.append(str(queue[0] if queue else -1))
    elif cmd[0] == 'back':
        result.append(str(queue[-1] if queue else -1))
print('\\n'.join(result))""",

    # 10866: 덱
    "10866": """import sys
from collections import deque
input = sys.stdin.readline
n = int(input())
dq = deque()
result = []
for _ in range(n):
    cmd = input().split()
    if cmd[0] == 'push_front':
        dq.appendleft(int(cmd[1]))
    elif cmd[0] == 'push_back':
        dq.append(int(cmd[1]))
    elif cmd[0] == 'pop_front':
        result.append(str(dq.popleft() if dq else -1))
    elif cmd[0] == 'pop_back':
        result.append(str(dq.pop() if dq else -1))
    elif cmd[0] == 'size':
        result.append(str(len(dq)))
    elif cmd[0] == 'empty':
        result.append('1' if not dq else '0')
    elif cmd[0] == 'front':
        result.append(str(dq[0] if dq else -1))
    elif cmd[0] == 'back':
        result.append(str(dq[-1] if dq else -1))
print('\\n'.join(result))""",

    # 1927: 최소 힙
    "1927": """import sys
import heapq
input = sys.stdin.readline
n = int(input())
heap = []
for _ in range(n):
    x = int(input())
    if x == 0:
        print(heapq.heappop(heap) if heap else 0)
    else:
        heapq.heappush(heap, x)""",

    # 11279: 최대 힙
    "11279": """import sys
import heapq
input = sys.stdin.readline
n = int(input())
heap = []
for _ in range(n):
    x = int(input())
    if x == 0:
        print(-heapq.heappop(heap) if heap else 0)
    else:
        heapq.heappush(heap, -x)""",

    # 1920: 수 찾기
    "1920": """import sys
input = sys.stdin.readline
n = int(input())
a = set(map(int, input().split()))
m = int(input())
b = list(map(int, input().split()))
for x in b:
    print(1 if x in a else 0)""",

    # 18870: 좌표 압축
    "18870": """import sys
input = sys.stdin.readline
n = int(input())
x = list(map(int, input().split()))
sorted_x = sorted(set(x))
rank = {v: i for i, v in enumerate(sorted_x)}
print(' '.join(str(rank[v]) for v in x))""",

    # 1764: 듣보잡
    "1764": """import sys
input = sys.stdin.readline
n, m = map(int, input().split())
a = set(input().strip() for _ in range(n))
b = set(input().strip() for _ in range(m))
result = sorted(a & b)
print(len(result))
for r in result:
    print(r)""",

    # 1181: 단어 정렬
    "1181": """import sys
input = sys.stdin.readline
n = int(input())
words = set(input().strip() for _ in range(n))
sorted_words = sorted(words, key=lambda x: (len(x), x))
for w in sorted_words:
    print(w)""",

    # 10989: 수 정렬하기 3
    "10989": """import sys
input = sys.stdin.readline
n = int(input())
count = [0] * 10001
for _ in range(n):
    count[int(input())] += 1
for i in range(1, 10001):
    for _ in range(count[i]):
        print(i)""",

    # 11650: 좌표 정렬하기
    "11650": """import sys
input = sys.stdin.readline
n = int(input())
points = [tuple(map(int, input().split())) for _ in range(n)]
points.sort()
for x, y in points:
    print(x, y)""",

    # 11651: 좌표 정렬하기 2
    "11651": """import sys
input = sys.stdin.readline
n = int(input())
points = [tuple(map(int, input().split())) for _ in range(n)]
points.sort(key=lambda p: (p[1], p[0]))
for x, y in points:
    print(x, y)""",

    # 10814: 나이순 정렬
    "10814": """import sys
input = sys.stdin.readline
n = int(input())
members = []
for i in range(n):
    age, name = input().split()
    members.append((int(age), i, name))
members.sort(key=lambda x: (x[0], x[1]))
for age, _, name in members:
    print(age, name)""",

    # 2751: 수 정렬하기 2
    "2751": """import sys
input = sys.stdin.readline
n = int(input())
nums = sorted(int(input()) for _ in range(n))
for num in nums:
    print(num)""",

    # 2606: 바이러스
    "2606": """import sys
sys.setrecursionlimit(10000)

n = int(input())
m = int(input())
graph = [[] for _ in range(n + 1)]
for _ in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

visited = [False] * (n + 1)
count = 0

def dfs(node):
    global count
    visited[node] = True
    for next_node in graph[node]:
        if not visited[next_node]:
            count += 1
            dfs(next_node)

dfs(1)
print(count)""",

    # 1012: 유기농 배추
    "1012": """import sys
sys.setrecursionlimit(10000)
input = sys.stdin.readline

def dfs(x, y):
    if x < 0 or x >= m or y < 0 or y >= n:
        return
    if field[x][y] == 0:
        return
    field[x][y] = 0
    dfs(x-1, y)
    dfs(x+1, y)
    dfs(x, y-1)
    dfs(x, y+1)

t = int(input())
for _ in range(t):
    m, n, k = map(int, input().split())
    field = [[0] * n for _ in range(m)]
    for _ in range(k):
        x, y = map(int, input().split())
        field[x][y] = 1

    count = 0
    for i in range(m):
        for j in range(n):
            if field[i][j] == 1:
                dfs(i, j)
                count += 1
    print(count)""",

    # 2667: 단지번호붙이기
    "2667": """import sys
sys.setrecursionlimit(10000)

n = int(input())
field = [list(input().strip()) for _ in range(n)]

def dfs(x, y):
    if x < 0 or x >= n or y < 0 or y >= n:
        return 0
    if field[x][y] == '0':
        return 0
    field[x][y] = '0'
    return 1 + dfs(x-1, y) + dfs(x+1, y) + dfs(x, y-1) + dfs(x, y+1)

sizes = []
for i in range(n):
    for j in range(n):
        if field[i][j] == '1':
            sizes.append(dfs(i, j))

print(len(sizes))
for s in sorted(sizes):
    print(s)""",

    # 7576: 토마토
    "7576": """from collections import deque
import sys
input = sys.stdin.readline

m, n = map(int, input().split())
box = [list(map(int, input().split())) for _ in range(n)]

queue = deque()
for i in range(n):
    for j in range(m):
        if box[i][j] == 1:
            queue.append((i, j, 0))

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
max_day = 0

while queue:
    x, y, day = queue.popleft()
    max_day = max(max_day, day)
    for i in range(4):
        nx, ny = x + dx[i], y + dy[i]
        if 0 <= nx < n and 0 <= ny < m and box[nx][ny] == 0:
            box[nx][ny] = 1
            queue.append((nx, ny, day + 1))

for i in range(n):
    for j in range(m):
        if box[i][j] == 0:
            print(-1)
            exit()

print(max_day)""",

    # 1697: 숨바꼭질
    "1697": """from collections import deque

n, k = map(int, input().split())
if n == k:
    print(0)
else:
    visited = [False] * 100001
    queue = deque([(n, 0)])
    visited[n] = True

    while queue:
        pos, time = queue.popleft()
        for next_pos in [pos - 1, pos + 1, pos * 2]:
            if next_pos == k:
                print(time + 1)
                exit()
            if 0 <= next_pos <= 100000 and not visited[next_pos]:
                visited[next_pos] = True
                queue.append((next_pos, time + 1))""",
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
                'expected': ex.get('output', '')[:50],
                'actual': actual[:50] if actual else 'N/A',
                'error': err[:80] if err else 'Wrong Answer'
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
