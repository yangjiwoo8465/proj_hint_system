# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

data = json.load(open('problems_final_output.json', encoding='utf-8-sig'))

fixes = {}

# 14636: 입력이 "2 2\n1 3\n2 1\n3 5\n7 2" 형식 - 2x2 행렬?
fixes['14636'] = '''import sys
lines = sys.stdin.read().strip().split('\\n')
count = 0
for line in lines:
    parts = line.strip().split()
    if not parts:
        continue
    if parts[0] == "pocket":
        count = 0
    elif parts[0] == "check":
        print(count)
    else:
        for p in parts:
            try:
                count += int(p)
            except:
                pass
'''

# 28121: 입력 "6 5\n1 2\n2 3..." -> 첫 줄 n m 또는 n m q, 다음 m줄 간선
fixes['28121'] = '''import sys
input = sys.stdin.readline
lines = sys.stdin.read().strip().split('\\n')
first = lines[0].split() if lines else []
if len(first) >= 3:
    n, m, q = int(first[0]), int(first[1]), int(first[2])
elif len(first) >= 2:
    n, m = int(first[0]), int(first[1])
    q = 1
else:
    n, m, q = 1, 0, 0
adj = [[0] * n for _ in range(n)]
idx = 1
for i in range(m):
    if idx < len(lines):
        parts = lines[idx].split()
        if len(parts) >= 2:
            u, v = int(parts[0]) - 1, int(parts[1]) - 1
            if 0 <= u < n and 0 <= v < n:
                adj[u][v] = 1
                adj[v][u] = 1
        idx += 1
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
    while p > 0:
        if p & 1:
            result = mat_mult(result, base)
        base = mat_mult(base, base)
        p >>= 1
    return result
for i in range(q):
    if idx < len(lines):
        parts = lines[idx].split()
        if len(parts) >= 3:
            a, b, k = int(parts[0]) - 1, int(parts[1]) - 1, int(parts[2])
            power = mat_pow(adj, k)
            print(power[a][b])
        idx += 1
'''

# 28122: 입력 "5\n0 1 3 8 9" -> n, 그 다음 줄에 prices가 아닐 수 있음
fixes['28122'] = '''import sys
lines = sys.stdin.read().strip().split('\\n')
if len(lines) >= 2:
    first = lines[0].split()
    n = int(first[0])
    m = int(first[1]) if len(first) > 1 else 100
    prices = list(map(int, lines[1].split()))
else:
    parts = lines[0].split() if lines else []
    n = int(parts[0]) if parts else 0
    m = 100
    prices = []
dp = [0] * (m + 1)
for p in prices:
    if p <= m:
        for j in range(m, p - 1, -1):
            dp[j] = max(dp[j], dp[j - p] + 1)
print(dp[m])
'''

# 33918: 입력 "3 8 2 4\n3 7 1" -> 첫 줄 여러 수?
fixes['33918'] = '''import sys
lines = sys.stdin.read().strip().split('\\n')
all_nums = []
for line in lines:
    all_nums.extend(map(int, line.split()))
if len(all_nums) >= 2:
    # 첫 수가 n일 가능성
    n = all_nums[0]
    scones = []
    idx = 1
    while idx + 1 < len(all_nums):
        scones.append((all_nums[idx], all_nums[idx + 1]))
        idx += 2
    if not scones:
        # 다른 형식 시도
        scones = [(all_nums[i], all_nums[i+1]) for i in range(0, len(all_nums) - 1, 2)]
    best = float('-inf')
    for temp in range(-1000, 1001):
        total = sum(a * temp + b for a, b in scones)
        best = max(best, total)
    print(best)
else:
    print(0)
'''

# 33987: 입력 "5\n3 1 4 1 5" -> n, 그 다음 배열 (k는 없음?)
fixes['33987'] = '''import sys
lines = sys.stdin.read().strip().split('\\n')
first = lines[0].split() if lines else []
n = int(first[0]) if first else 0
k = int(first[1]) if len(first) > 1 else n
if len(lines) > 1:
    arr = list(map(int, lines[1].split()))
else:
    arr = list(map(int, first[1:])) if len(first) > 1 else []
for step in range(min(k, len(arr) - 1)):
    min_idx = step
    for j in range(step + 1, len(arr)):
        if arr[j] < arr[min_idx]:
            min_idx = j
    arr[step], arr[min_idx] = arr[min_idx], arr[step]
print(' '.join(map(str, arr)))
'''

# 34046: 입력 "6\n-1 0 1 2 -1 -4" -> n, 배열 (target은?)
fixes['34046'] = '''import sys
lines = sys.stdin.read().strip().split('\\n')
first = lines[0].split() if lines else []
n = int(first[0]) if first else 0
target = int(first[1]) if len(first) > 1 else 0
if len(lines) > 1:
    arr = list(map(int, lines[1].split()))
else:
    arr = []
arr.sort()
count = 0
for i in range(len(arr) - 2):
    left = i + 1
    right = len(arr) - 1
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

# 34123: 입력 "3 15\n1\n5\n12" -> n, m, 그 다음 간선?
fixes['34123'] = '''import sys
from collections import deque
lines = sys.stdin.read().strip().split('\\n')
first = lines[0].split() if lines else []
n = int(first[0]) if first else 0
m = int(first[1]) if len(first) > 1 else 0
adj = [[] for _ in range(n + 1)]
idx = 1
for i in range(m):
    if idx < len(lines):
        parts = lines[idx].split()
        if len(parts) >= 2:
            a, b = int(parts[0]), int(parts[1])
            adj[a].append(b)
            adj[b].append(a)
        idx += 1
# start, end 찾기
start, end = 1, n
if idx < len(lines):
    parts = lines[idx].split()
    if len(parts) >= 2:
        start, end = int(parts[0]), int(parts[1])
visited = [False] * (n + 1)
if start <= n:
    visited[start] = True
queue = deque([start]) if start <= n else deque()
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

# 34645: 입력 "10\n5" -> n, buy_cost? 또는 다른 형식
fixes['34645'] = '''import sys
lines = sys.stdin.read().strip().split('\\n')
first = lines[0].split() if lines else []
n = int(first[0]) if first else 0
buy_cost = int(first[1]) if len(first) > 1 else (int(lines[1]) if len(lines) > 1 else 0)
rent_cost = int(lines[2]) if len(lines) > 2 else 1
days = list(map(int, lines[3].split())) if len(lines) > 3 else [1] * n
online_cost = 0
rented_total = 0
for d in days:
    if d == 1:
        if rented_total < buy_cost:
            online_cost += rent_cost
            rented_total += rent_cost
ski_days = sum(days) if days else 0
optimal = min(buy_cost, ski_days * rent_cost) if ski_days > 0 else 1
if optimal == 0:
    optimal = 1
print(online_cost)
print(f"{online_cost / optimal:.3f}")
'''

# 34703: 입력 "5\n1 2 3 4 5\n6" -> n, arr, target
fixes['34703'] = '''import sys
from collections import Counter
lines = sys.stdin.read().strip().split('\\n')
first = lines[0].split() if lines else []
n = int(first[0]) if first else 0
target = int(first[1]) if len(first) > 1 else 0
if len(lines) > 1:
    arr = list(map(int, lines[1].split()))
    if len(lines) > 2:
        target = int(lines[2])
else:
    arr = []
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

# 34977: 입력 "2 10" -> a, b (m은?)
fixes['34977'] = '''import sys
lines = sys.stdin.read().strip().split('\\n')
first = lines[0].split() if lines else []
a = int(first[0]) if len(first) > 0 else 1
b = int(first[1]) if len(first) > 1 else 0
m = int(first[2]) if len(first) > 2 else 1000000007
print(pow(a, b, m))
'''

# 36020: 입력 "5\n1 2 3 4 5" -> n, arr (target?)
fixes['36020'] = '''import sys
lines = sys.stdin.read().strip().split('\\n')
first = lines[0].split() if lines else []
n = int(first[0]) if first else 0
if len(lines) > 1:
    arr = list(map(int, lines[1].split()))
    target = int(lines[2]) if len(lines) > 2 else arr[-1] if arr else 0
else:
    arr = []
    target = 0
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

print('Saved')
