"""
추가 문제 수정 배치 3
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
    # 25288: 영어 시험 - 문자열 매칭
    "25288": """n = int(input())
words = [input().strip() for _ in range(n)]
m = int(input())
for _ in range(m):
    sentence = input().strip()
    count = sum(1 for w in words if w in sentence)
    print(count)""",

    # 34063: 이진 탐색 - 처음과 끝
    "34063": """def binary_search_first(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            right = mid - 1
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result

def binary_search_last(arr, target):
    left, right = 0, len(arr) - 1
    result = -1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            result = mid
            left = mid + 1
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result

n, target = map(int, input().split())
arr = list(map(int, input().split()))
first = binary_search_first(arr, target)
last = binary_search_last(arr, target)
print(first, last)""",

    # 34067: 이진 탐색 - 회전
    "34067": """def search_rotated(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        if arr[left] <= arr[mid]:
            if arr[left] <= target < arr[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if arr[mid] < target <= arr[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1

n, target = map(int, input().split())
arr = list(map(int, input().split()))
print(search_rotated(arr, target))""",

    # 34084: 해시맵 - 두 합
    "34084": """n, target = map(int, input().split())
arr = list(map(int, input().split()))
seen = {}
for i, num in enumerate(arr):
    if target - num in seen:
        print(seen[target - num], i)
        break
    seen[num] = i""",

    # 30917: 두 수 빼기 - 유니코드 문제
    "30917": """a, b = map(int, input().split())
print(a - b)""",

    # 30924: 두 수 빼기 - 유니코드 문제
    "30924": """a, b = map(int, input().split())
print(a - b)""",

    # 2839: 설탕 배달
    "2839": """n = int(input())
result = -1
for i in range(n // 5 + 1):
    remaining = n - 5 * i
    if remaining >= 0 and remaining % 3 == 0:
        result = i + remaining // 3
        break
if result == -1:
    for i in range(n // 3 + 1):
        remaining = n - 3 * i
        if remaining >= 0 and remaining % 5 == 0:
            result = i + remaining // 5
            break
print(result)""",

    # 1074: Z
    "1074": """def solve(n, r, c):
    if n == 0:
        return 0
    half = 2 ** (n - 1)
    area_size = half * half
    if r < half and c < half:
        return solve(n - 1, r, c)
    elif r < half and c >= half:
        return area_size + solve(n - 1, r, c - half)
    elif r >= half and c < half:
        return 2 * area_size + solve(n - 1, r - half, c)
    else:
        return 3 * area_size + solve(n - 1, r - half, c - half)

n, r, c = map(int, input().split())
print(solve(n, r, c))""",

    # 11399: ATM
    "11399": """n = int(input())
times = sorted(list(map(int, input().split())))
total = 0
current = 0
for t in times:
    current += t
    total += current
print(total)""",

    # 1931: 회의실 배정
    "1931": """n = int(input())
meetings = []
for _ in range(n):
    s, e = map(int, input().split())
    meetings.append((e, s))
meetings.sort()
count = 0
last_end = 0
for end, start in meetings:
    if start >= last_end:
        count += 1
        last_end = end
print(count)""",

    # 11053: 가장 긴 증가하는 부분 수열
    "11053": """n = int(input())
arr = list(map(int, input().split()))
dp = [1] * n
for i in range(1, n):
    for j in range(i):
        if arr[j] < arr[i]:
            dp[i] = max(dp[i], dp[j] + 1)
print(max(dp))""",

    # 11054: 가장 긴 바이토닉 부분 수열
    "11054": """n = int(input())
arr = list(map(int, input().split()))

# LIS
lis = [1] * n
for i in range(1, n):
    for j in range(i):
        if arr[j] < arr[i]:
            lis[i] = max(lis[i], lis[j] + 1)

# LDS (역방향 LIS)
lds = [1] * n
for i in range(n - 2, -1, -1):
    for j in range(i + 1, n):
        if arr[j] < arr[i]:
            lds[i] = max(lds[i], lds[j] + 1)

max_len = 0
for i in range(n):
    max_len = max(max_len, lis[i] + lds[i] - 1)
print(max_len)""",

    # 9251: LCS
    "9251": """s1 = input().strip()
s2 = input().strip()
n, m = len(s1), len(s2)
dp = [[0] * (m + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, m + 1):
        if s1[i-1] == s2[j-1]:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])
print(dp[n][m])""",

    # 9012: 괄호
    "9012": """t = int(input())
for _ in range(t):
    s = input().strip()
    count = 0
    valid = True
    for c in s:
        if c == '(':
            count += 1
        else:
            count -= 1
            if count < 0:
                valid = False
                break
    if count != 0:
        valid = False
    print('YES' if valid else 'NO')""",

    # 10773: 제로
    "10773": """k = int(input())
stack = []
for _ in range(k):
    n = int(input())
    if n == 0:
        stack.pop()
    else:
        stack.append(n)
print(sum(stack))""",

    # 4949: 균형잡힌 세상
    "4949": """while True:
    line = input()
    if line == '.':
        break
    stack = []
    valid = True
    for c in line:
        if c in '([':
            stack.append(c)
        elif c == ')':
            if not stack or stack[-1] != '(':
                valid = False
                break
            stack.pop()
        elif c == ']':
            if not stack or stack[-1] != '[':
                valid = False
                break
            stack.pop()
    if stack:
        valid = False
    print('yes' if valid else 'no')""",

    # 1654: 랜선 자르기
    "1654": """k, n = map(int, input().split())
lans = [int(input()) for _ in range(k)]

left, right = 1, max(lans)
result = 0
while left <= right:
    mid = (left + right) // 2
    count = sum(lan // mid for lan in lans)
    if count >= n:
        result = mid
        left = mid + 1
    else:
        right = mid - 1
print(result)""",

    # 2805: 나무 자르기
    "2805": """n, m = map(int, input().split())
trees = list(map(int, input().split()))

left, right = 0, max(trees)
result = 0
while left <= right:
    mid = (left + right) // 2
    total = sum(max(0, t - mid) for t in trees)
    if total >= m:
        result = mid
        left = mid + 1
    else:
        right = mid - 1
print(result)""",

    # 1629: 곱셈
    "1629": """a, b, c = map(int, input().split())

def power(a, b, c):
    if b == 0:
        return 1
    if b == 1:
        return a % c
    half = power(a, b // 2, c)
    if b % 2 == 0:
        return (half * half) % c
    else:
        return (half * half * a) % c

print(power(a, b, c))""",

    # 11051: 이항 계수 2
    "11051": """n, k = map(int, input().split())
MOD = 10007
dp = [[0] * (n + 1) for _ in range(n + 1)]
for i in range(n + 1):
    dp[i][0] = 1
    dp[i][i] = 1
for i in range(2, n + 1):
    for j in range(1, i):
        dp[i][j] = (dp[i-1][j-1] + dp[i-1][j]) % MOD
print(dp[n][k])""",

    # 2004: 조합 0의 개수
    "2004": """def count_factor(n, p):
    count = 0
    pk = p
    while pk <= n:
        count += n // pk
        pk *= p
    return count

n, m = map(int, input().split())
twos = count_factor(n, 2) - count_factor(m, 2) - count_factor(n - m, 2)
fives = count_factor(n, 5) - count_factor(m, 5) - count_factor(n - m, 5)
print(min(twos, fives))""",

    # 9375: 패션왕 신해빈
    "9375": """t = int(input())
for _ in range(t):
    n = int(input())
    clothes = {}
    for _ in range(n):
        _, kind = input().split()
        clothes[kind] = clothes.get(kind, 0) + 1
    result = 1
    for cnt in clothes.values():
        result *= (cnt + 1)
    print(result - 1)""",

    # 1966: 프린터 큐
    "1966": """from collections import deque
t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    priorities = list(map(int, input().split()))
    queue = deque([(p, i) for i, p in enumerate(priorities)])
    count = 0
    while queue:
        current = queue.popleft()
        if any(p > current[0] for p, _ in queue):
            queue.append(current)
        else:
            count += 1
            if current[1] == m:
                print(count)
                break""",

    # 11866: 요세푸스 문제 0
    "11866": """from collections import deque
n, k = map(int, input().split())
queue = deque(range(1, n + 1))
result = []
while queue:
    for _ in range(k - 1):
        queue.append(queue.popleft())
    result.append(str(queue.popleft()))
print('<' + ', '.join(result) + '>')""",

    # 1978: 소수 찾기
    "1978": """def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

n = int(input())
nums = list(map(int, input().split()))
print(sum(1 for x in nums if is_prime(x)))""",

    # 2609: 최대공약수와 최소공배수
    "2609": """import math
a, b = map(int, input().split())
g = math.gcd(a, b)
l = a * b // g
print(g)
print(l)""",

    # 1929: 소수 구하기
    "1929": """m, n = map(int, input().split())
sieve = [True] * (n + 1)
sieve[0] = sieve[1] = False
for i in range(2, int(n**0.5) + 1):
    if sieve[i]:
        for j in range(i*i, n + 1, i):
            sieve[j] = False
for i in range(m, n + 1):
    if sieve[i]:
        print(i)""",

    # 4153: 직각삼각형
    "4153": """while True:
    a, b, c = map(int, input().split())
    if a == 0 and b == 0 and c == 0:
        break
    sides = sorted([a, b, c])
    if sides[0]**2 + sides[1]**2 == sides[2]**2:
        print('right')
    else:
        print('wrong')""",

    # 9184: 신나는 함수 실행
    "9184": """import sys
sys.setrecursionlimit(10000)

memo = {}

def w(a, b, c):
    if (a, b, c) in memo:
        return memo[(a, b, c)]

    if a <= 0 or b <= 0 or c <= 0:
        return 1
    if a > 20 or b > 20 or c > 20:
        return w(20, 20, 20)
    if a < b < c:
        result = w(a, b, c-1) + w(a, b-1, c-1) - w(a, b-1, c)
    else:
        result = w(a-1, b, c) + w(a-1, b-1, c) + w(a-1, b, c-1) - w(a-1, b-1, c-1)

    memo[(a, b, c)] = result
    return result

while True:
    a, b, c = map(int, input().split())
    if a == -1 and b == -1 and c == -1:
        break
    print(f'w({a}, {b}, {c}) = {w(a, b, c)}')""",

    # 17626: Four Squares
    "17626": """n = int(input())
dp = [0] * (n + 1)
for i in range(1, n + 1):
    dp[i] = i
    j = 1
    while j * j <= i:
        dp[i] = min(dp[i], dp[i - j*j] + 1)
        j += 1
print(dp[n])""",

    # 1436: 영화감독 숌
    "1436": """n = int(input())
count = 0
num = 666
while count < n:
    if '666' in str(num):
        count += 1
        if count == n:
            print(num)
            break
    num += 1""",

    # 1018: 체스판 다시 칠하기
    "1018": """n, m = map(int, input().split())
board = [input().strip() for _ in range(n)]

# 패턴 생성
patterns = []
for start in ['W', 'B']:
    pattern = []
    for i in range(8):
        row = ''
        for j in range(8):
            if (i + j) % 2 == 0:
                row += start
            else:
                row += 'B' if start == 'W' else 'W'
        pattern.append(row)
    patterns.append(pattern)

min_paint = float('inf')
for si in range(n - 7):
    for sj in range(m - 7):
        for pattern in patterns:
            count = 0
            for i in range(8):
                for j in range(8):
                    if board[si + i][sj + j] != pattern[i][j]:
                        count += 1
            min_paint = min(min_paint, count)

print(min_paint)""",

    # 7568: 덩치
    "7568": """n = int(input())
people = [tuple(map(int, input().split())) for _ in range(n)]
ranks = []
for i in range(n):
    rank = 1
    for j in range(n):
        if i != j:
            if people[j][0] > people[i][0] and people[j][1] > people[i][1]:
                rank += 1
    ranks.append(str(rank))
print(' '.join(ranks))""",
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
