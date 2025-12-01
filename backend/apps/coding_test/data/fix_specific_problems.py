"""
특정 문제들의 solution_code를 직접 수정
problem_id가 문자열이므로 키도 문자열로
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


# 문제별 올바른 solution_code (키를 문자열로)
FIXED_SOLUTIONS = {
    "1000": """A, B = map(int, input().split())
print(A + B)""",

    "1269": """a_n, b_n = map(int, input().split())
A = set(map(int, input().split()))
B = set(map(int, input().split()))
print(len((A - B) | (B - A)))""",

    "1260": """from collections import deque
import sys
sys.setrecursionlimit(10000)

def dfs(node):
    visited_dfs[node] = True
    dfs_result.append(node)
    for next_node in graph[node]:
        if not visited_dfs[next_node]:
            dfs(next_node)

n, m, v = map(int, input().split())
graph = [[] for _ in range(n + 1)]
for _ in range(m):
    a, b = map(int, input().split())
    graph[a].append(b)
    graph[b].append(a)

for i in range(n + 1):
    graph[i].sort()

dfs_result = []
visited_dfs = [False] * (n + 1)
dfs(v)

bfs_result = []
visited_bfs = [False] * (n + 1)
queue = deque([v])
visited_bfs[v] = True

while queue:
    node = queue.popleft()
    bfs_result.append(node)
    for next_node in graph[node]:
        if not visited_bfs[next_node]:
            visited_bfs[next_node] = True
            queue.append(next_node)

print(' '.join(map(str, dfs_result)))
print(' '.join(map(str, bfs_result)))""",

    "1932": """n = int(input())
triangle = []
for _ in range(n):
    triangle.append(list(map(int, input().split())))

dp = [[0] * (i + 1) for i in range(n)]
dp[0][0] = triangle[0][0]

for i in range(1, n):
    for j in range(i + 1):
        if j == 0:
            dp[i][j] = dp[i-1][j] + triangle[i][j]
        elif j == i:
            dp[i][j] = dp[i-1][j-1] + triangle[i][j]
        else:
            dp[i][j] = max(dp[i-1][j-1], dp[i-1][j]) + triangle[i][j]

print(max(dp[n-1]))""",

    "1934": """import math
t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    print(a * b // math.gcd(a, b))""",

    "2178": """from collections import deque

n, m = map(int, input().split())
maze = [input().strip() for _ in range(n)]

dist = [[-1] * m for _ in range(n)]
dist[0][0] = 1
queue = deque([(0, 0)])

dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]

while queue:
    x, y = queue.popleft()
    for i in range(4):
        nx, ny = x + dx[i], y + dy[i]
        if 0 <= nx < n and 0 <= ny < m:
            if maze[nx][ny] == '1' and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                queue.append((nx, ny))

print(dist[n-1][m-1])""",

    "2581": """def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

M = int(input())
N = int(input())
primes = [i for i in range(M, N+1) if is_prime(i)]

if primes:
    print(sum(primes))
    print(min(primes))
else:
    print(-1)""",

    "2630": """import sys
sys.setrecursionlimit(10000)

def count_paper(x, y, n):
    global blue, white

    color = paper[x][y]
    same = True

    for i in range(x, x + n):
        for j in range(y, y + n):
            if paper[i][j] != color:
                same = False
                break
        if not same:
            break

    if same:
        if color == 1:
            blue += 1
        else:
            white += 1
    else:
        half = n // 2
        count_paper(x, y, half)
        count_paper(x, y + half, half)
        count_paper(x + half, y, half)
        count_paper(x + half, y + half, half)

n = int(input())
paper = []
for _ in range(n):
    paper.append(list(map(int, input().split())))

blue = 0
white = 0
count_paper(0, 0, n)
print(white)
print(blue)""",

    "2675": """T = int(input())
for _ in range(T):
    parts = input().split()
    R = int(parts[0])
    S = parts[1]
    result = ''.join(char * R for char in S)
    print(result)""",

    "2720": """T = int(input())
coins = [25, 10, 5, 1]
for _ in range(T):
    C = int(input())
    counts = []
    for coin in coins:
        counts.append(C // coin)
        C %= coin
    print(' '.join(map(str, counts)))""",

    "2740": """n, m = map(int, input().split())
A = []
for _ in range(n):
    A.append(list(map(int, input().split())))

m2, k = map(int, input().split())
B = []
for _ in range(m2):
    B.append(list(map(int, input().split())))

C = [[0] * k for _ in range(n)]
for i in range(n):
    for j in range(k):
        for l in range(m):
            C[i][j] += A[i][l] * B[l][j]

for row in C:
    print(' '.join(map(str, row)))""",

    "3273": """n = int(input())
nums = list(map(int, input().split()))
x = int(input())

count = 0
seen = set()
for num in nums:
    if x - num in seen:
        count += 1
    seen.add(num)

print(count)""",

    "4779": """import sys

def cantor(n):
    if n == 0:
        return '-'
    prev = cantor(n - 1)
    space = ' ' * (3 ** (n - 1))
    return prev + space + prev

for line in sys.stdin:
    n = int(line.strip())
    print(cantor(n))""",

    "5073": """while True:
    a, b, c = map(int, input().split())
    if a == 0 and b == 0 and c == 0:
        break

    sides = sorted([a, b, c])
    if sides[0] + sides[1] <= sides[2]:
        print('Invalid')
    elif a == b == c:
        print('Equilateral')
    elif a == b or b == c or a == c:
        print('Isosceles')
    else:
        print('Scalene')""",

    "5086": """while True:
    a, b = map(int, input().split())
    if a == 0 and b == 0:
        break

    if b % a == 0:
        print('factor')
    elif a % b == 0:
        print('multiple')
    else:
        print('neither')""",

    "10250": """T = int(input())
for _ in range(T):
    H, W, N = map(int, input().split())
    floor = N % H
    room = N // H + 1
    if floor == 0:
        floor = H
        room -= 1
    print(floor * 100 + room)""",

    "10818": """n = int(input())
nums = list(map(int, input().split()))
print(min(nums), max(nums))""",

    "10871": """n, x = map(int, input().split())
nums = list(map(int, input().split()))
result = [num for num in nums if num < x]
print(' '.join(map(str, result)))""",

    "10951": """import sys
for line in sys.stdin:
    a, b = map(int, line.split())
    print(a + b)""",

    "10952": """while True:
    a, b = map(int, input().split())
    if a == 0 and b == 0:
        break
    print(a + b)""",

    "11654": """c = input()
print(ord(c))""",

    "11720": """n = int(input())
s = input()
print(sum(int(c) for c in s))""",

    "15552": """import sys
input = sys.stdin.readline
T = int(input())
for _ in range(T):
    a, b = map(int, input().split())
    print(a + b)""",

    "1110": """n = int(input())
original = n
count = 0

while True:
    tens = n // 10
    ones = n % 10
    new_ones = (tens + ones) % 10
    n = ones * 10 + new_ones
    count += 1
    if n == original:
        break

print(count)""",

    "2438": """n = int(input())
for i in range(1, n + 1):
    print('*' * i)""",

    "2439": """n = int(input())
for i in range(1, n + 1):
    print(' ' * (n - i) + '*' * i)""",

    "2562": """nums = [int(input()) for _ in range(9)]
print(max(nums))
print(nums.index(max(nums)) + 1)""",

    "2577": """a = int(input())
b = int(input())
c = int(input())
result = str(a * b * c)
for i in range(10):
    print(result.count(str(i)))""",

    "2884": """h, m = map(int, input().split())
total = h * 60 + m - 45
if total < 0:
    total += 24 * 60
print(total // 60, total % 60)""",

    "2908": """a, b = input().split()
a = int(a[::-1])
b = int(b[::-1])
print(max(a, b))""",

    "8958": """T = int(input())
for _ in range(T):
    s = input()
    score = 0
    combo = 0
    for c in s:
        if c == 'O':
            combo += 1
            score += combo
        else:
            combo = 0
    print(score)""",

    "1152": """s = input().strip()
if s:
    print(len(s.split()))
else:
    print(0)""",

    "1157": """s = input().upper()
count = {}
for c in s:
    count[c] = count.get(c, 0) + 1

max_count = max(count.values())
max_chars = [c for c, cnt in count.items() if cnt == max_count]

if len(max_chars) == 1:
    print(max_chars[0])
else:
    print('?')""",

    "1546": """n = int(input())
scores = list(map(int, input().split()))
m = max(scores)
new_scores = [s / m * 100 for s in scores]
print(sum(new_scores) / n)""",

    "2475": """nums = list(map(int, input().split()))
s = sum(n * n for n in nums)
print(s % 10)""",

    "2480": """a, b, c = map(int, input().split())
if a == b == c:
    print(10000 + a * 1000)
elif a == b:
    print(1000 + a * 100)
elif b == c:
    print(1000 + b * 100)
elif a == c:
    print(1000 + a * 100)
else:
    print(max(a, b, c) * 100)""",

    "2525": """h, m = map(int, input().split())
t = int(input())
total = h * 60 + m + t
print(total // 60 % 24, total % 60)""",

    "2739": """n = int(input())
for i in range(1, 10):
    print(f'{n} * {i} = {n * i}')""",

    "2741": """n = int(input())
for i in range(1, n + 1):
    print(i)""",

    "2742": """n = int(input())
for i in range(n, 0, -1):
    print(i)""",

    "2753": """year = int(input())
if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
    print(1)
else:
    print(0)""",

    "9498": """score = int(input())
if score >= 90:
    print('A')
elif score >= 80:
    print('B')
elif score >= 70:
    print('C')
elif score >= 60:
    print('D')
else:
    print('F')""",

    "10809": """s = input()
for c in 'abcdefghijklmnopqrstuvwxyz':
    print(s.find(c), end=' ')""",

    "10872": """n = int(input())
result = 1
for i in range(1, n + 1):
    result *= i
print(result)""",

    "10998": """a, b = map(int, input().split())
print(a * b)""",

    "1008": """a, b = map(int, input().split())
print(a / b)""",

    "1001": """a, b = map(int, input().split())
print(a - b)""",

    "2558": """a = int(input())
b = int(input())
print(a + b)""",
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
    for f in failed_list[:10]:
        print(f"\n[{f['pid']}] {f['title']}")
        print(f"  Expected: {f['expected']}")
        print(f"  Actual: {f['actual']}")
        print(f"  Error: {f['error']}")

# 저장
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved to: {output_path}")
