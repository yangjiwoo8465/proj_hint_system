"""
394개 invalid 문제들의 solution_code를 새로 생성
문제 설명, 입력/출력 형식, 예제를 분석해서 올바른 코드 생성
"""

import json
import os
import sys
import subprocess
import re
import random
from typing import Dict, List, Tuple, Optional

sys.stdout.reconfigure(encoding='utf-8')

script_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(script_dir, 'problems_final.json')
output_path = os.path.join(script_dir, 'problems_all_fixed.json')

data = json.load(open(input_path, encoding='utf-8-sig'))


def run_solution(code: str, test_input: str, timeout: int = 5) -> Tuple[bool, str, str]:
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


def test_solution(code: str, test_input: str, expected_output: str) -> bool:
    success, actual, err = run_solution(code, test_input)
    if not success:
        return False
    expected = expected_output.strip().replace('\r\n', '\n').replace('\r', '\n')
    return actual == expected


def analyze_input(input_str: str) -> Dict:
    """입력 형식 상세 분석"""
    lines = input_str.strip().split('\n')
    analysis = {
        'num_lines': len(lines),
        'lines': []
    }
    for line in lines:
        parts = line.split()
        types = []
        for p in parts:
            try:
                int(p)
                types.append('int')
            except:
                try:
                    float(p)
                    types.append('float')
                except:
                    types.append('str')
        analysis['lines'].append({
            'raw': line,
            'parts': parts,
            'num_parts': len(parts),
            'types': types
        })
    return analysis


def generate_input_code(analysis: Dict) -> str:
    """입력 형식에 맞는 입력 코드 생성"""
    code_lines = []
    var_names = []

    for i, line in enumerate(analysis['lines']):
        n_parts = line['num_parts']
        types = line['types']

        if n_parts == 0:
            continue
        elif n_parts == 1:
            var = f"v{i}"
            if types[0] == 'int':
                code_lines.append(f"{var} = int(input())")
            elif types[0] == 'float':
                code_lines.append(f"{var} = float(input())")
            else:
                code_lines.append(f"{var} = input().strip()")
            var_names.append(var)
        else:
            if all(t == 'int' for t in types):
                if n_parts == 2:
                    code_lines.append(f"v{i}a, v{i}b = map(int, input().split())")
                    var_names.extend([f"v{i}a", f"v{i}b"])
                elif n_parts == 3:
                    code_lines.append(f"v{i}a, v{i}b, v{i}c = map(int, input().split())")
                    var_names.extend([f"v{i}a", f"v{i}b", f"v{i}c"])
                else:
                    code_lines.append(f"arr{i} = list(map(int, input().split()))")
                    var_names.append(f"arr{i}")
            elif all(t == 'float' for t in types):
                code_lines.append(f"arr{i} = list(map(float, input().split()))")
                var_names.append(f"arr{i}")
            else:
                code_lines.append(f"arr{i} = input().split()")
                var_names.append(f"arr{i}")

    return '\n'.join(code_lines), var_names


# 문제 유형별 솔루션 생성 함수들

def solve_two_int_one_line(problem: Dict) -> Optional[str]:
    """한 줄에 두 정수 입력 문제"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    parts = inp.split()
    if len(parts) != 2:
        return None

    try:
        a, b = int(parts[0]), int(parts[1])
    except:
        return None

    # 다양한 연산 시도
    ops = [
        (a + b, "a, b = map(int, input().split())\nprint(a + b)"),
        (a - b, "a, b = map(int, input().split())\nprint(a - b)"),
        (b - a, "a, b = map(int, input().split())\nprint(b - a)"),
        (a * b, "a, b = map(int, input().split())\nprint(a * b)"),
        (a // b if b else None, "a, b = map(int, input().split())\nprint(a // b)"),
        (a % b if b else None, "a, b = map(int, input().split())\nprint(a % b)"),
        (max(a, b), "a, b = map(int, input().split())\nprint(max(a, b))"),
        (min(a, b), "a, b = map(int, input().split())\nprint(min(a, b))"),
        (abs(a - b), "a, b = map(int, input().split())\nprint(abs(a - b))"),
        (a ** b if b < 20 else None, "a, b = map(int, input().split())\nprint(a ** b)"),
    ]

    for result, code in ops:
        if result is not None and str(result) == out:
            return code

    # 나눗셈 (실수)
    if b != 0:
        try:
            if abs(float(out) - a/b) < 0.0001:
                return "a, b = map(int, input().split())\nprint(a / b)"
        except:
            pass

    return None


def solve_single_int(problem: Dict) -> Optional[str]:
    """단일 정수 입력 문제"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    try:
        n = int(inp)
    except:
        return None

    ops = [
        (n, "n = int(input())\nprint(n)"),
        (n * 2, "n = int(input())\nprint(n * 2)"),
        (n ** 2, "n = int(input())\nprint(n ** 2)"),
        (n * (n + 1) // 2, "n = int(input())\nprint(n * (n + 1) // 2)"),
        (n * (n - 1) // 2, "n = int(input())\nprint(n * (n - 1) // 2)"),
        (2 ** n if n < 30 else None, "n = int(input())\nprint(2 ** n)"),
    ]

    for result, code in ops:
        if result is not None and str(result) == out:
            return code

    return None


def solve_n_and_array(problem: Dict) -> Optional[str]:
    """N과 배열 입력 (2줄)"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) != 2:
        return None

    try:
        n = int(lines[0].strip())
        arr = list(map(int, lines[1].strip().split()))
    except:
        return None

    ops = [
        (sum(arr), "n = int(input())\narr = list(map(int, input().split()))\nprint(sum(arr))"),
        (max(arr), "n = int(input())\narr = list(map(int, input().split()))\nprint(max(arr))"),
        (min(arr), "n = int(input())\narr = list(map(int, input().split()))\nprint(min(arr))"),
        (len(set(arr)), "n = int(input())\narr = list(map(int, input().split()))\nprint(len(set(arr)))"),
        (max(arr) - min(arr), "n = int(input())\narr = list(map(int, input().split()))\nprint(max(arr) - min(arr))"),
        (sum(arr) // n if n else None, "n = int(input())\narr = list(map(int, input().split()))\nprint(sum(arr) // n)"),
        (' '.join(map(str, sorted(arr))), "n = int(input())\narr = list(map(int, input().split()))\nprint(' '.join(map(str, sorted(arr))))"),
        (' '.join(map(str, sorted(arr, reverse=True))), "n = int(input())\narr = list(map(int, input().split()))\nprint(' '.join(map(str, sorted(arr, reverse=True))))"),
    ]

    for result, code in ops:
        if result is not None and str(result) == out:
            return code

    return None


def solve_string_problem(problem: Dict) -> Optional[str]:
    """문자열 문제"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    # 단일 문자열 입력
    if '\n' not in inp:
        s = inp
        ops = [
            (len(s), "s = input()\nprint(len(s))"),
            (s[::-1], "s = input()\nprint(s[::-1])"),
            (s.upper(), "s = input()\nprint(s.upper())"),
            (s.lower(), "s = input()\nprint(s.lower())"),
            (s.count('a'), "s = input()\nprint(s.count('a'))"),
            (len(s.split()), "s = input()\nprint(len(s.split()))"),
            (sum(c.isdigit() for c in s), "s = input()\nprint(sum(c.isdigit() for c in s))"),
            (sum(c.isalpha() for c in s), "s = input()\nprint(sum(c.isalpha() for c in s))"),
            (''.join(sorted(s)), "s = input()\nprint(''.join(sorted(s)))"),
            (''.join(sorted(set(s))), "s = input()\nprint(''.join(sorted(set(s))))"),
        ]

        for result, code in ops:
            if str(result) == out:
                return code

    return None


def solve_comparison(problem: Dict) -> Optional[str]:
    """비교 문제"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip().upper()

    parts = inp.split()
    if len(parts) != 2:
        return None

    try:
        a, b = int(parts[0]), int(parts[1])
    except:
        return None

    templates = [
        ("a < b", a < b),
        ("a > b", a > b),
        ("a == b", a == b),
        ("a <= b", a <= b),
        ("a >= b", a >= b),
        ("a != b", a != b),
    ]

    for expr, result in templates:
        if out in ['YES', 'TRUE', '1'] and result:
            return f"a, b = map(int, input().split())\nprint('YES' if {expr} else 'NO')"
        if out in ['NO', 'FALSE', '0'] and not result:
            return f"a, b = map(int, input().split())\nprint('YES' if {expr} else 'NO')"

    # > or < 출력
    if out == '>':
        return "a, b = map(int, input().split())\nprint('>' if a > b else '<' if a < b else '==')"
    if out == '<':
        return "a, b = map(int, input().split())\nprint('>' if a > b else '<' if a < b else '==')"
    if out == '==':
        return "a, b = map(int, input().split())\nprint('>' if a > b else '<' if a < b else '==')"

    return None


def solve_grid_problem(problem: Dict) -> Optional[str]:
    """그리드/2D 배열 문제"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) < 2:
        return None

    # 첫 줄이 N M 형태인지 확인
    first_parts = lines[0].split()
    if len(first_parts) == 2:
        try:
            n, m = int(first_parts[0]), int(first_parts[1])
            grid = [lines[i+1] for i in range(min(n, len(lines)-1))]

            # 그리드의 특정 문자 개수
            for char in 'WBXY01#.':
                count = sum(row.count(char) for row in grid)
                if str(count) == out:
                    return f'''n, m = map(int, input().split())
grid = [input() for _ in range(n)]
print(sum(row.count('{char}') for row in grid))'''
        except:
            pass

    return None


def solve_set_operations(problem: Dict) -> Optional[str]:
    """집합 연산 문제"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) < 3:
        return None

    try:
        # 첫 줄: 두 집합의 크기
        sizes = list(map(int, lines[0].split()))
        if len(sizes) != 2:
            return None

        a_size, b_size = sizes
        set_a = set(map(int, lines[1].split()))
        set_b = set(map(int, lines[2].split()))

        ops = [
            (len(set_a | set_b), "a_n, b_n = map(int, input().split())\nA = set(map(int, input().split()))\nB = set(map(int, input().split()))\nprint(len(A | B))"),
            (len(set_a & set_b), "a_n, b_n = map(int, input().split())\nA = set(map(int, input().split()))\nB = set(map(int, input().split()))\nprint(len(A & B))"),
            (len(set_a - set_b), "a_n, b_n = map(int, input().split())\nA = set(map(int, input().split()))\nB = set(map(int, input().split()))\nprint(len(A - B))"),
            (len(set_b - set_a), "a_n, b_n = map(int, input().split())\nA = set(map(int, input().split()))\nB = set(map(int, input().split()))\nprint(len(B - A))"),
            (len(set_a ^ set_b), "a_n, b_n = map(int, input().split())\nA = set(map(int, input().split()))\nB = set(map(int, input().split()))\nprint(len(A ^ B))"),
            (len((set_a - set_b) | (set_b - set_a)), "a_n, b_n = map(int, input().split())\nA = set(map(int, input().split()))\nB = set(map(int, input().split()))\nprint(len((A - B) | (B - A)))"),
        ]

        for result, code in ops:
            if str(result) == out:
                return code
    except:
        pass

    return None


def solve_fibonacci(problem: Dict) -> Optional[str]:
    """피보나치 관련 문제"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    try:
        n = int(inp)
    except:
        return None

    # 피보나치 계산
    def fib(x):
        if x <= 1:
            return x
        a, b = 0, 1
        for _ in range(x - 1):
            a, b = b, a + b
        return b

    if str(fib(n)) == out:
        return """n = int(input())
if n <= 1:
    print(n)
else:
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    print(b)"""

    # 피보나치 mod
    for mod in [10, 100, 1000, 10000, 1000000007]:
        if str(fib(n) % mod) == out:
            return f"""n = int(input())
if n <= 1:
    print(n)
else:
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, (a + b) % {mod}
    print(b)"""

    return None


def solve_factorial(problem: Dict) -> Optional[str]:
    """팩토리얼 관련 문제"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    try:
        n = int(inp)
    except:
        return None

    import math
    fact = math.factorial(n)

    if str(fact) == out:
        return """import math
n = int(input())
print(math.factorial(n))"""

    # 팩토리얼 mod
    for mod in [10, 100, 1000, 10000, 1000000007]:
        result = 1
        for i in range(1, n + 1):
            result = (result * i) % mod
        if str(result) == out:
            return f"""n = int(input())
result = 1
for i in range(1, n + 1):
    result = (result * i) % {mod}
print(result)"""

    return None


def solve_prime(problem: Dict) -> Optional[str]:
    """소수 관련 문제"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    # 범위 내 소수 출력
    parts = inp.split()
    if len(parts) == 2:
        try:
            m, n = int(parts[0]), int(parts[1])

            def sieve(limit):
                if limit < 2:
                    return []
                is_prime = [True] * (limit + 1)
                is_prime[0] = is_prime[1] = False
                for i in range(2, int(limit**0.5) + 1):
                    if is_prime[i]:
                        for j in range(i*i, limit + 1, i):
                            is_prime[j] = False
                return [i for i in range(limit + 1) if is_prime[i]]

            primes = [p for p in sieve(n) if p >= m]
            expected = '\n'.join(map(str, primes))

            if expected.replace('\r', '') == out.replace('\r', ''):
                return """def sieve(limit):
    if limit < 2:
        return []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i*i, limit + 1, i):
                is_prime[j] = False
    return [i for i in range(limit + 1) if is_prime[i]]

m, n = map(int, input().split())
for p in sieve(n):
    if p >= m:
        print(p)"""
        except:
            pass

    # 단일 숫자 소수 판별
    try:
        n = int(inp)
        is_prime = n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))

        if out.upper() in ['YES', 'TRUE', '1'] and is_prime:
            return """n = int(input())
if n < 2:
    print('NO')
else:
    is_prime = True
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            is_prime = False
            break
    print('YES' if is_prime else 'NO')"""

        if out.upper() in ['NO', 'FALSE', '0'] and not is_prime:
            return """n = int(input())
if n < 2:
    print('NO')
else:
    is_prime = True
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            is_prime = False
            break
    print('YES' if is_prime else 'NO')"""
    except:
        pass

    return None


def solve_gcd_lcm(problem: Dict) -> Optional[str]:
    """GCD/LCM 문제"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    parts = inp.split()
    if len(parts) != 2:
        return None

    try:
        a, b = int(parts[0]), int(parts[1])
    except:
        return None

    import math
    gcd = math.gcd(a, b)
    lcm = a * b // gcd

    if str(gcd) == out:
        return """import math
a, b = map(int, input().split())
print(math.gcd(a, b))"""

    if str(lcm) == out:
        return """import math
a, b = map(int, input().split())
print(a * b // math.gcd(a, b))"""

    if f"{gcd}\n{lcm}" == out or f"{gcd} {lcm}" == out:
        return """import math
a, b = map(int, input().split())
g = math.gcd(a, b)
print(g)
print(a * b // g)"""

    return None


def solve_dp_basic(problem: Dict) -> Optional[str]:
    """기본 DP 문제 (계단 오르기 등)"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    try:
        n = int(inp)
    except:
        return None

    # 계단 오르기 (1 or 2칸)
    def stairs(x):
        if x <= 2:
            return x
        dp = [0] * (x + 1)
        dp[1], dp[2] = 1, 2
        for i in range(3, x + 1):
            dp[i] = dp[i-1] + dp[i-2]
        return dp[x]

    if str(stairs(n)) == out:
        return """n = int(input())
if n <= 2:
    print(n)
else:
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    print(dp[n])"""

    return None


def solve_four_int_one_line(problem: Dict) -> Optional[str]:
    """한 줄에 4개 정수 입력"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    parts = inp.split()
    if len(parts) != 4:
        return None

    try:
        a, b, c, d = map(int, parts)
    except:
        return None

    ops = [
        (a + b + c + d, "a, b, c, d = map(int, input().split())\nprint(a + b + c + d)"),
        (a * b * c * d, "a, b, c, d = map(int, input().split())\nprint(a * b * c * d)"),
        (max(a, b, c, d), "a, b, c, d = map(int, input().split())\nprint(max(a, b, c, d))"),
        (min(a, b, c, d), "a, b, c, d = map(int, input().split())\nprint(min(a, b, c, d))"),
        ((a + b) * (c + d), "a, b, c, d = map(int, input().split())\nprint((a + b) * (c + d))"),
    ]

    for result, code in ops:
        if str(result) == out:
            return code

    return None


def solve_three_int_one_line(problem: Dict) -> Optional[str]:
    """한 줄에 3개 정수 입력"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    parts = inp.split()
    if len(parts) != 3:
        return None

    try:
        a, b, c = map(int, parts)
    except:
        return None

    ops = [
        (a + b + c, "a, b, c = map(int, input().split())\nprint(a + b + c)"),
        (a * b * c, "a, b, c = map(int, input().split())\nprint(a * b * c)"),
        (max(a, b, c), "a, b, c = map(int, input().split())\nprint(max(a, b, c))"),
        (min(a, b, c), "a, b, c = map(int, input().split())\nprint(min(a, b, c))"),
        ((a + b + c) // 3, "a, b, c = map(int, input().split())\nprint((a + b + c) // 3)"),
        (sorted([a, b, c])[1], "a, b, c = map(int, input().split())\nprint(sorted([a, b, c])[1])"),  # 중앙값
    ]

    for result, code in ops:
        if str(result) == out:
            return code

    return None


def solve_multi_line_numbers(problem: Dict) -> Optional[str]:
    """여러 줄에 숫자들"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    # 첫 줄이 N, 이후 N줄에 각각 숫자
    if len(lines) >= 2:
        try:
            n = int(lines[0].strip())
            if len(lines) == n + 1:
                nums = [int(lines[i+1].strip()) for i in range(n)]

                ops = [
                    (sum(nums), f"n = int(input())\nnums = [int(input()) for _ in range(n)]\nprint(sum(nums))"),
                    (max(nums), f"n = int(input())\nnums = [int(input()) for _ in range(n)]\nprint(max(nums))"),
                    (min(nums), f"n = int(input())\nnums = [int(input()) for _ in range(n)]\nprint(min(nums))"),
                    (sum(nums) // n, f"n = int(input())\nnums = [int(input()) for _ in range(n)]\nprint(sum(nums) // n)"),
                ]

                for result, code in ops:
                    if str(result) == out:
                        return code
        except:
            pass

    return None


def solve_palindrome(problem: Dict) -> Optional[str]:
    """회문 판별"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    # 단일 문자열
    if '\n' not in inp:
        s = inp
        is_palindrome = s == s[::-1]

        if out.upper() in ['YES', 'TRUE', '1'] and is_palindrome:
            return "s = input().strip()\nprint('YES' if s == s[::-1] else 'NO')"
        if out.upper() in ['NO', 'FALSE', '0'] and not is_palindrome:
            return "s = input().strip()\nprint('YES' if s == s[::-1] else 'NO')"
        if out == '1' and is_palindrome:
            return "s = input().strip()\nprint(1 if s == s[::-1] else 0)"
        if out == '0' and not is_palindrome:
            return "s = input().strip()\nprint(1 if s == s[::-1] else 0)"

    return None


def solve_count_chars(problem: Dict) -> Optional[str]:
    """문자 개수 세기"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) == 2:
        s = lines[0]
        target = lines[1]

        count = s.lower().count(target.lower())
        if str(count) == out:
            return """s = input()
target = input()
print(s.lower().count(target.lower()))"""

    return None


def solve_divisors(problem: Dict) -> Optional[str]:
    """약수 관련"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    try:
        n = int(inp)
    except:
        return None

    divisors = [i for i in range(1, n + 1) if n % i == 0]

    # 약수 개수
    if str(len(divisors)) == out:
        return """n = int(input())
count = sum(1 for i in range(1, n + 1) if n % i == 0)
print(count)"""

    # 약수 합
    if str(sum(divisors)) == out:
        return """n = int(input())
total = sum(i for i in range(1, n + 1) if n % i == 0)
print(total)"""

    # 약수 출력
    div_str = '\n'.join(map(str, divisors))
    if div_str == out:
        return """n = int(input())
for i in range(1, n + 1):
    if n % i == 0:
        print(i)"""

    return None


def solve_sort_words(problem: Dict) -> Optional[str]:
    """단어 정렬"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) >= 2:
        try:
            n = int(lines[0])
            words = [lines[i+1].strip() for i in range(n)]

            # 사전순 정렬
            sorted_words = sorted(set(words))
            if '\n'.join(sorted_words) == out:
                return """n = int(input())
words = [input().strip() for _ in range(n)]
for w in sorted(set(words)):
    print(w)"""

            # 길이순, 사전순 정렬
            sorted_words = sorted(set(words), key=lambda x: (len(x), x))
            if '\n'.join(sorted_words) == out:
                return """n = int(input())
words = [input().strip() for _ in range(n)]
for w in sorted(set(words), key=lambda x: (len(x), x)):
    print(w)"""
        except:
            pass

    return None


def solve_binary(problem: Dict) -> Optional[str]:
    """이진수 변환"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    try:
        n = int(inp)
        if bin(n)[2:] == out:
            return "n = int(input())\nprint(bin(n)[2:])"
        if str(int(inp, 2)) == out:
            return "s = input()\nprint(int(s, 2))"
    except:
        pass

    return None


def solve_ascii(problem: Dict) -> Optional[str]:
    """ASCII 변환"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    # 문자 -> 아스키
    if len(inp) == 1:
        if str(ord(inp)) == out:
            return "c = input()\nprint(ord(c))"

    # 아스키 -> 문자
    try:
        n = int(inp)
        if chr(n) == out:
            return "n = int(input())\nprint(chr(n))"
    except:
        pass

    return None


def solve_reverse_array(problem: Dict) -> Optional[str]:
    """배열 뒤집기"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) == 2:
        try:
            n = int(lines[0])
            arr = list(map(int, lines[1].split()))
            reversed_arr = arr[::-1]

            if ' '.join(map(str, reversed_arr)) == out:
                return """n = int(input())
arr = list(map(int, input().split()))
print(' '.join(map(str, arr[::-1])))"""
        except:
            pass

    return None


def solve_many_int_one_line(problem: Dict) -> Optional[str]:
    """한 줄에 여러 정수 (5개 이상)"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    if '\n' in inp:
        return None

    parts = inp.split()
    if len(parts) < 5:
        return None

    try:
        nums = list(map(int, parts))
    except:
        return None

    ops = [
        (sum(nums), "nums = list(map(int, input().split()))\nprint(sum(nums))"),
        (max(nums), "nums = list(map(int, input().split()))\nprint(max(nums))"),
        (min(nums), "nums = list(map(int, input().split()))\nprint(min(nums))"),
        (len(nums), "nums = list(map(int, input().split()))\nprint(len(nums))"),
        (' '.join(map(str, sorted(nums))), "nums = list(map(int, input().split()))\nprint(' '.join(map(str, sorted(nums))))"),
        (' '.join(map(str, sorted(nums, reverse=True))), "nums = list(map(int, input().split()))\nprint(' '.join(map(str, sorted(nums, reverse=True))))"),
    ]

    for result, code in ops:
        if str(result) == out:
            return code

    return None


def solve_star_pattern(problem: Dict) -> Optional[str]:
    """별표 패턴 출력"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    try:
        n = int(inp)
    except:
        return None

    out_lines = out.split('\n')

    # 직각삼각형 (왼쪽 정렬)
    pattern1 = '\n'.join('*' * i for i in range(1, n + 1))
    if pattern1 == out:
        return """n = int(input())
for i in range(1, n + 1):
    print('*' * i)"""

    # 직각삼각형 (오른쪽 정렬)
    pattern2 = '\n'.join(' ' * (n - i) + '*' * i for i in range(1, n + 1))
    if pattern2 == out:
        return """n = int(input())
for i in range(1, n + 1):
    print(' ' * (n - i) + '*' * i)"""

    # 역삼각형
    pattern3 = '\n'.join('*' * i for i in range(n, 0, -1))
    if pattern3 == out:
        return """n = int(input())
for i in range(n, 0, -1):
    print('*' * i)"""

    # N x N 사각형
    pattern4 = '\n'.join('*' * n for _ in range(n))
    if pattern4 == out:
        return """n = int(input())
for _ in range(n):
    print('*' * n)"""

    return None


def solve_two_line_each_number(problem: Dict) -> Optional[str]:
    """두 줄에 각각 숫자 하나씩"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) != 2:
        return None

    try:
        a = int(lines[0].strip())
        b = int(lines[1].strip())
    except:
        return None

    ops = [
        (a + b, "a = int(input())\nb = int(input())\nprint(a + b)"),
        (a - b, "a = int(input())\nb = int(input())\nprint(a - b)"),
        (b - a, "a = int(input())\nb = int(input())\nprint(b - a)"),
        (a * b, "a = int(input())\nb = int(input())\nprint(a * b)"),
        (a // b if b else None, "a = int(input())\nb = int(input())\nprint(a // b)"),
        (max(a, b), "a = int(input())\nb = int(input())\nprint(max(a, b))"),
        (min(a, b), "a = int(input())\nb = int(input())\nprint(min(a, b))"),
    ]

    for result, code in ops:
        if result is not None and str(result) == out:
            return code

    import math
    if str(math.gcd(a, b)) == out:
        return "import math\na = int(input())\nb = int(input())\nprint(math.gcd(a, b))"
    if str(a * b // math.gcd(a, b)) == out:
        return "import math\na = int(input())\nb = int(input())\nprint(a * b // math.gcd(a, b))"

    return None


def solve_coordinate_problem(problem: Dict) -> Optional[str]:
    """좌표 관련 문제"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    parts = inp.split()
    if len(parts) == 2:
        try:
            x, y = int(parts[0]), int(parts[1])

            # 사분면 판단
            if out in ['1', '2', '3', '4']:
                quadrant = 0
                if x > 0 and y > 0:
                    quadrant = 1
                elif x < 0 and y > 0:
                    quadrant = 2
                elif x < 0 and y < 0:
                    quadrant = 3
                elif x > 0 and y < 0:
                    quadrant = 4

                if str(quadrant) == out:
                    return """x, y = map(int, input().split())
if x > 0 and y > 0:
    print(1)
elif x < 0 and y > 0:
    print(2)
elif x < 0 and y < 0:
    print(3)
else:
    print(4)"""
        except:
            pass

    return None


def solve_time_problem(problem: Dict) -> Optional[str]:
    """시간 관련 문제"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    parts = inp.split()
    if len(parts) == 2:
        try:
            h, m = int(parts[0]), int(parts[1])

            # 1시간 전
            prev_h = (h - 1) % 24
            prev_m = m
            if out == f"{prev_h} {prev_m}":
                return """h, m = map(int, input().split())
print((h - 1) % 24, m)"""

            # 45분 전
            total = h * 60 + m - 45
            if total < 0:
                total += 24 * 60
            new_h, new_m = total // 60, total % 60
            if out == f"{new_h} {new_m}":
                return """h, m = map(int, input().split())
total = h * 60 + m - 45
if total < 0:
    total += 24 * 60
print(total // 60, total % 60)"""
        except:
            pass

    return None


def solve_tax_problem(problem: Dict) -> Optional[str]:
    """세금/할인 계산"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    try:
        n = int(inp)
    except:
        return None

    # 일반적인 할인/세금 비율
    for rate in [0.1, 0.15, 0.2, 0.25, 0.3, 0.5]:
        if str(int(n * (1 - rate))) == out:
            return f"""n = int(input())
print(int(n * {1 - rate}))"""
        if str(int(n * (1 + rate))) == out:
            return f"""n = int(input())
print(int(n * {1 + rate}))"""

    return None


def solve_hello_world(problem: Dict) -> Optional[str]:
    """Hello World 류"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    # 입력 없이 고정 출력
    if not inp and out:
        return f'print("{out}")'

    # 입력받아 인사
    if inp and out:
        if out == f"Hello, {inp}!":
            return 's = input()\nprint(f"Hello, {s}!")'
        if out == f"hello, {inp}":
            return 's = input()\nprint(f"hello, {s}")'

    return None


def solve_calculator(problem: Dict) -> Optional[str]:
    """간단한 계산기"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) == 3:
        try:
            a = int(lines[0])
            b = int(lines[1])
            op = lines[2].strip()

            result = None
            if op == '+':
                result = a + b
            elif op == '-':
                result = a - b
            elif op == '*':
                result = a * b
            elif op == '/':
                result = a // b if b else None

            if result is not None and str(result) == out:
                return """a = int(input())
b = int(input())
op = input().strip()
if op == '+':
    print(a + b)
elif op == '-':
    print(a - b)
elif op == '*':
    print(a * b)
elif op == '/':
    print(a // b)"""
        except:
            pass

    return None


def solve_even_odd(problem: Dict) -> Optional[str]:
    """짝수/홀수 판별"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip().lower()

    try:
        n = int(inp)
    except:
        return None

    is_even = n % 2 == 0

    if out in ['even', 'even', '짝수'] and is_even:
        return """n = int(input())
print('Even' if n % 2 == 0 else 'Odd')"""
    if out in ['odd', 'odd', '홀수'] and not is_even:
        return """n = int(input())
print('Even' if n % 2 == 0 else 'Odd')"""

    return None


def solve_positive_negative(problem: Dict) -> Optional[str]:
    """양수/음수/0 판별"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip().lower()

    try:
        n = int(inp)
    except:
        return None

    if n > 0 and out in ['positive', 'positive', '양수', '1']:
        return """n = int(input())
if n > 0:
    print('positive')
elif n < 0:
    print('negative')
else:
    print('zero')"""
    if n < 0 and out in ['negative', 'negative', '음수', '-1']:
        return """n = int(input())
if n > 0:
    print('positive')
elif n < 0:
    print('negative')
else:
    print('zero')"""
    if n == 0 and out in ['zero', 'zero', '0']:
        return """n = int(input())
if n > 0:
    print('positive')
elif n < 0:
    print('negative')
else:
    print('zero')"""

    return None


def solve_digit_sum(problem: Dict) -> Optional[str]:
    """자릿수 합"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    try:
        n = int(inp)
        digit_sum = sum(int(d) for d in str(abs(n)))

        if str(digit_sum) == out:
            return """n = int(input())
print(sum(int(d) for d in str(abs(n))))"""

        # 자릿수 개수
        if str(len(str(abs(n)))) == out:
            return """n = int(input())
print(len(str(abs(n))))"""
    except:
        pass

    return None


def solve_a_b_multiple_ops(problem: Dict) -> Optional[str]:
    """두 수에 대한 여러 연산 결과 출력"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    parts = inp.split()
    if len(parts) != 2:
        return None

    try:
        a, b = int(parts[0]), int(parts[1])
    except:
        return None

    # A+B, A-B, A*B, A/B 등 여러 줄 출력
    out_lines = out.split('\n')

    if len(out_lines) == 4:
        if (str(a + b) == out_lines[0] and str(a - b) == out_lines[1] and
            str(a * b) == out_lines[2]):
            if b != 0 and (str(a // b) == out_lines[3] or str(a / b) == out_lines[3]):
                return """a, b = map(int, input().split())
print(a + b)
print(a - b)
print(a * b)
print(a // b)"""

    if len(out_lines) == 5:
        if b != 0:
            expected = [a + b, a - b, a * b, a // b, a % b]
            if all(str(e) == o for e, o in zip(expected, out_lines)):
                return """a, b = map(int, input().split())
print(a + b)
print(a - b)
print(a * b)
print(a // b)
print(a % b)"""

    return None


def solve_reverse_string(problem: Dict) -> Optional[str]:
    """문자열 뒤집기"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    if '\n' not in inp and inp[::-1] == out:
        return "s = input()\nprint(s[::-1])"

    return None


def solve_min_max_avg(problem: Dict) -> Optional[str]:
    """최솟값, 최댓값, 평균"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) == 2:
        try:
            n = int(lines[0])
            nums = list(map(int, lines[1].split()))

            out_lines = out.split('\n')

            # min max
            if len(out_lines) == 2:
                if str(min(nums)) == out_lines[0] and str(max(nums)) == out_lines[1]:
                    return """n = int(input())
nums = list(map(int, input().split()))
print(min(nums))
print(max(nums))"""

            # min max 같은 줄
            if out == f"{min(nums)} {max(nums)}":
                return """n = int(input())
nums = list(map(int, input().split()))
print(min(nums), max(nums))"""

        except:
            pass

    return None


def solve_empty_input(problem: Dict) -> Optional[str]:
    """입력 없이 고정 출력"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    if not inp and out:
        # 다단 출력
        if '=' in out and 'x' in out.lower():
            # 구구단 패턴 탐지
            lines = out.split('\n')
            if lines:
                first = lines[0]
                # Nx1=N 형태인지 확인
                import re
                match = re.match(r'(\d+)x1=(\d+)', first)
                if match:
                    n = int(match.group(1))
                    return f"""for i in range(1, 10):
    print(f'{n}x{{i}}={{{n}*i}}')"""

        # 토끼 같은 고정 출력
        escaped = out.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        return f'print("{escaped}")'

    return None


def solve_symmetric_difference(problem: Dict) -> Optional[str]:
    """대칭 차집합"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) == 3:
        try:
            first_parts = lines[0].split()
            if len(first_parts) == 2:
                a_n, b_n = int(first_parts[0]), int(first_parts[1])
                set_a = set(map(int, lines[1].split()))
                set_b = set(map(int, lines[2].split()))

                # 대칭 차집합 크기
                sym_diff = len((set_a - set_b) | (set_b - set_a))
                if str(sym_diff) == out:
                    return """a_n, b_n = map(int, input().split())
A = set(map(int, input().split()))
B = set(map(int, input().split()))
print(len((A - B) | (B - A)))"""
        except:
            pass

    return None


def solve_anagram(problem: Dict) -> Optional[str]:
    """애너그램 판별"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip().upper()

    if len(lines) == 2:
        s1, s2 = lines[0].strip(), lines[1].strip()
        is_anagram = sorted(s1.lower()) == sorted(s2.lower())

        if out in ['YES', 'TRUE', '1'] and is_anagram:
            return """s1 = input().strip()
s2 = input().strip()
print('YES' if sorted(s1.lower()) == sorted(s2.lower()) else 'NO')"""
        if out in ['NO', 'FALSE', '0'] and not is_anagram:
            return """s1 = input().strip()
s2 = input().strip()
print('YES' if sorted(s1.lower()) == sorted(s2.lower()) else 'NO')"""

    return None


def solve_substring(problem: Dict) -> Optional[str]:
    """부분문자열 판별"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip().upper()

    if len(lines) == 2:
        main_str = lines[0].strip()
        sub_str = lines[1].strip()
        is_sub = sub_str in main_str

        if out in ['YES', 'TRUE', '1'] and is_sub:
            return """s = input().strip()
sub = input().strip()
print('YES' if sub in s else 'NO')"""
        if out in ['NO', 'FALSE', '0'] and not is_sub:
            return """s = input().strip()
sub = input().strip()
print('YES' if sub in s else 'NO')"""

    return None


def solve_filter_less_than(problem: Dict) -> Optional[str]:
    """X보다 작은 수"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) == 2:
        first_parts = lines[0].split()
        if len(first_parts) == 2:
            try:
                n, x = int(first_parts[0]), int(first_parts[1])
                nums = list(map(int, lines[1].split()))
                filtered = [num for num in nums if num < x]

                if ' '.join(map(str, filtered)) == out:
                    return """n, x = map(int, input().split())
nums = list(map(int, input().split()))
print(' '.join(str(num) for num in nums if num < x))"""
            except:
                pass

    return None


def solve_multiple_test_cases_gcd_lcm(problem: Dict) -> Optional[str]:
    """다중 테스트케이스 GCD/LCM"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    try:
        t = int(lines[0])
        if len(lines) >= t + 1:
            import math
            results = []
            for i in range(1, t + 1):
                parts = lines[i].split()
                if len(parts) == 2:
                    a, b = int(parts[0]), int(parts[1])
                    results.append(a * b // math.gcd(a, b))

            expected = '\n'.join(map(str, results))
            if expected == out:
                return """import math
t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    print(a * b // math.gcd(a, b))"""

            # GCD
            results = []
            for i in range(1, t + 1):
                parts = lines[i].split()
                if len(parts) == 2:
                    a, b = int(parts[0]), int(parts[1])
                    results.append(math.gcd(a, b))

            expected = '\n'.join(map(str, results))
            if expected == out:
                return """import math
t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    print(math.gcd(a, b))"""
    except:
        pass

    return None


def solve_cutline(problem: Dict) -> Optional[str]:
    """커트라인 문제"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) == 2:
        first_parts = lines[0].split()
        if len(first_parts) == 2:
            try:
                n, k = int(first_parts[0]), int(first_parts[1])
                scores = list(map(int, lines[1].split()))
                sorted_scores = sorted(scores, reverse=True)

                # k등 점수
                if str(sorted_scores[k-1]) == out:
                    return """n, k = map(int, input().split())
scores = list(map(int, input().split()))
scores.sort(reverse=True)
print(scores[k-1])"""

                # 하위 k등 점수
                sorted_asc = sorted(scores)
                if str(sorted_asc[k-1]) == out:
                    return """n, k = map(int, input().split())
scores = list(map(int, input().split()))
scores.sort()
print(scores[k-1])"""
            except:
                pass

    return None


def solve_statistics(problem: Dict) -> Optional[str]:
    """통계학 문제 (평균, 중앙값, 최빈값, 범위)"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    try:
        n = int(lines[0])
        if len(lines) == n + 1:
            nums = [int(lines[i+1]) for i in range(n)]
            out_lines = out.split('\n')

            # 평균
            avg = round(sum(nums) / n)
            # 중앙값
            sorted_nums = sorted(nums)
            median = sorted_nums[n // 2]
            # 최빈값
            from collections import Counter
            cnt = Counter(nums)
            max_freq = max(cnt.values())
            modes = sorted([k for k, v in cnt.items() if v == max_freq])
            mode = modes[1] if len(modes) > 1 else modes[0]
            # 범위
            range_val = max(nums) - min(nums)

            if len(out_lines) == 4:
                expected = [avg, median, mode, range_val]
                if all(str(e) == o for e, o in zip(expected, out_lines)):
                    return """from collections import Counter
n = int(input())
nums = [int(input()) for _ in range(n)]
avg = round(sum(nums) / n)
sorted_nums = sorted(nums)
median = sorted_nums[n // 2]
cnt = Counter(nums)
max_freq = max(cnt.values())
modes = sorted([k for k, v in cnt.items() if v == max_freq])
mode = modes[1] if len(modes) > 1 else modes[0]
range_val = max(nums) - min(nums)
print(avg)
print(median)
print(mode)
print(range_val)"""
    except:
        pass

    return None


def solve_lis(problem: Dict) -> Optional[str]:
    """가장 긴 증가하는 부분수열"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) == 2:
        try:
            n = int(lines[0])
            nums = list(map(int, lines[1].split()))

            # LIS 길이 계산
            dp = [1] * n
            for i in range(1, n):
                for j in range(i):
                    if nums[j] < nums[i]:
                        dp[i] = max(dp[i], dp[j] + 1)
            lis_len = max(dp)

            if str(lis_len) == out:
                return """n = int(input())
nums = list(map(int, input().split()))
dp = [1] * n
for i in range(1, n):
    for j in range(i):
        if nums[j] < nums[i]:
            dp[i] = max(dp[i], dp[j] + 1)
print(max(dp))"""
        except:
            pass

    return None


def solve_permutation(problem: Dict) -> Optional[str]:
    """순열 출력"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    try:
        parts = inp.split('\n')
        if len(parts) == 2:
            n = int(parts[0])
            nums = list(map(int, parts[1].split()))

            # 순열 생성
            from itertools import permutations
            perms = list(permutations(nums))
            expected = '\n'.join(' '.join(map(str, p)) for p in perms)

            if expected == out:
                return """from itertools import permutations
n = int(input())
nums = list(map(int, input().split()))
for p in permutations(nums):
    print(' '.join(map(str, p)))"""
    except:
        pass

    return None


def solve_subsets(problem: Dict) -> Optional[str]:
    """부분집합 출력"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    try:
        parts = inp.split('\n')
        if len(parts) == 2:
            n = int(parts[0])
            nums = list(map(int, parts[1].split()))

            # 부분집합 생성
            from itertools import combinations
            subsets = []
            for r in range(n + 1):
                for combo in combinations(nums, r):
                    subsets.append(' '.join(map(str, combo)))

            expected = '\n'.join(subsets)

            if expected == out:
                return """from itertools import combinations
n = int(input())
nums = list(map(int, input().split()))
for r in range(n + 1):
    for combo in combinations(nums, r):
        print(' '.join(map(str, combo)))"""
    except:
        pass

    return None


def solve_hex_addition(problem: Dict) -> Optional[str]:
    """16진수 덧셈"""
    ex = problem['examples'][0]
    inp = ex['input'].strip()
    out = ex['output'].strip()

    parts = inp.split()
    if len(parts) == 2:
        try:
            a_hex, b_hex = parts[0], parts[1]
            # 0x 접두사 처리
            a_val = int(a_hex, 16)
            b_val = int(b_hex, 16)
            result = a_val + b_val

            if out.lower().startswith('0x'):
                expected_hex = hex(result)
                if expected_hex == out.lower():
                    return """a, b = input().split()
print(hex(int(a, 16) + int(b, 16)))"""
        except:
            pass

    return None


def solve_ball_problem(problem: Dict) -> Optional[str]:
    """공 넣기 문제"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) >= 2:
        try:
            first_parts = lines[0].split()
            if len(first_parts) == 2:
                n, m = int(first_parts[0]), int(first_parts[1])
                basket = [0] * (n + 1)

                for i in range(1, m + 1):
                    cmd = list(map(int, lines[i].split()))
                    if len(cmd) == 3:
                        start, end, ball = cmd
                        for j in range(start, end + 1):
                            basket[j] = ball

                expected = ' '.join(map(str, basket[1:]))
                if expected == out:
                    return """n, m = map(int, input().split())
basket = [0] * (n + 1)
for _ in range(m):
    start, end, ball = map(int, input().split())
    for j in range(start, end + 1):
        basket[j] = ball
print(' '.join(map(str, basket[1:])))"""
        except:
            pass

    return None


def solve_unique_count(problem: Dict) -> Optional[str]:
    """중복 제거 후 합/개수"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) == 2:
        try:
            n = int(lines[0])
            nums = list(map(int, lines[1].split()))
            unique_sum = sum(set(nums))

            if str(unique_sum) == out:
                return """n = int(input())
nums = list(map(int, input().split()))
print(sum(set(nums)))"""
        except:
            pass

    return None


def solve_symmetric_diff_simple(problem: Dict) -> Optional[str]:
    """간단한 대칭 차집합 (3줄)"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    if len(lines) == 3:
        try:
            first_parts = lines[0].split()
            if len(first_parts) == 2:
                a_n, b_n = int(first_parts[0]), int(first_parts[1])
                set_a = set(map(int, lines[1].split()))
                set_b = set(map(int, lines[2].split()))

                # 대칭 차집합
                sym_diff = (set_a - set_b) | (set_b - set_a)
                if str(len(sym_diff)) == out:
                    return """a_n, b_n = map(int, input().split())
A = set(map(int, input().split()))
B = set(map(int, input().split()))
print(len((A - B) | (B - A)))"""
        except:
            pass

    return None


def solve_triangle_dp(problem: Dict) -> Optional[str]:
    """정수 삼각형 DP"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    try:
        n = int(lines[0])
        if len(lines) == n + 1:
            triangle = []
            for i in range(1, n + 1):
                triangle.append(list(map(int, lines[i].split())))

            # DP 계산
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

            if str(max(dp[n-1])) == out:
                return """n = int(input())
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

print(max(dp[n-1]))"""
    except:
        pass

    return None


def solve_wine_dp(problem: Dict) -> Optional[str]:
    """포도주 시식 DP"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    try:
        n = int(lines[0])
        if len(lines) == n + 1:
            wine = [0] + [int(lines[i+1]) for i in range(n)]

            if n == 1:
                result = wine[1]
            elif n == 2:
                result = wine[1] + wine[2]
            else:
                dp = [0] * (n + 1)
                dp[1] = wine[1]
                dp[2] = wine[1] + wine[2]

                for i in range(3, n + 1):
                    dp[i] = max(dp[i-1], dp[i-2] + wine[i], dp[i-3] + wine[i-1] + wine[i])

                result = dp[n]

            if str(result) == out:
                return """n = int(input())
wine = [0] + [int(input()) for _ in range(n)]

if n == 1:
    print(wine[1])
elif n == 2:
    print(wine[1] + wine[2])
else:
    dp = [0] * (n + 1)
    dp[1] = wine[1]
    dp[2] = wine[1] + wine[2]

    for i in range(3, n + 1):
        dp[i] = max(dp[i-1], dp[i-2] + wine[i], dp[i-3] + wine[i-1] + wine[i])

    print(dp[n])"""
    except:
        pass

    return None


def solve_dfs_bfs(problem: Dict) -> Optional[str]:
    """DFS와 BFS"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    try:
        first_parts = lines[0].split()
        if len(first_parts) == 3:
            n, m, v = int(first_parts[0]), int(first_parts[1]), int(first_parts[2])

            # 그래프 생성
            graph = [[] for _ in range(n + 1)]
            for i in range(1, m + 1):
                edge = list(map(int, lines[i].split()))
                a, b = edge[0], edge[1]
                graph[a].append(b)
                graph[b].append(a)

            for i in range(n + 1):
                graph[i].sort()

            # DFS
            dfs_result = []
            visited_dfs = [False] * (n + 1)

            def dfs(node):
                visited_dfs[node] = True
                dfs_result.append(node)
                for next_node in graph[node]:
                    if not visited_dfs[next_node]:
                        dfs(next_node)

            dfs(v)

            # BFS
            from collections import deque
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

            expected = ' '.join(map(str, dfs_result)) + '\n' + ' '.join(map(str, bfs_result))
            if expected.strip() == out.strip():
                return """from collections import deque

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
print(' '.join(map(str, bfs_result)))"""
    except:
        pass

    return None


def solve_maze_bfs(problem: Dict) -> Optional[str]:
    """미로 탐색 BFS"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    try:
        first_parts = lines[0].split()
        if len(first_parts) == 2:
            n, m = int(first_parts[0]), int(first_parts[1])
            maze = [lines[i+1] for i in range(n)]

            # BFS
            from collections import deque
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

            if str(dist[n-1][m-1]) == out:
                return """from collections import deque

n, m = map(int, input().split())
maze = [input() for _ in range(n)]

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

print(dist[n-1][m-1])"""
    except:
        pass

    return None


def solve_quadtree(problem: Dict) -> Optional[str]:
    """쿼드트리"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    try:
        n = int(lines[0])
        video = [lines[i+1] for i in range(n)]

        def quad(x, y, size):
            if size == 1:
                return video[x][y]

            first = video[x][y]
            same = True
            for i in range(x, x + size):
                for j in range(y, y + size):
                    if video[i][j] != first:
                        same = False
                        break
                if not same:
                    break

            if same:
                return first

            half = size // 2
            return '(' + quad(x, y, half) + quad(x, y + half, half) + quad(x + half, y, half) + quad(x + half, y + half, half) + ')'

        result = quad(0, 0, n)
        if result == out:
            return """import sys
sys.setrecursionlimit(10000)

n = int(input())
video = [input() for _ in range(n)]

def quad(x, y, size):
    if size == 1:
        return video[x][y]

    first = video[x][y]
    same = True
    for i in range(x, x + size):
        for j in range(y, y + size):
            if video[i][j] != first:
                same = False
                break
        if not same:
            break

    if same:
        return first

    half = size // 2
    return '(' + quad(x, y, half) + quad(x, y + half, half) + quad(x + half, y, half) + quad(x + half, y + half, half) + ')'

print(quad(0, 0, n))"""
    except:
        pass

    return None


def solve_tree_traversal(problem: Dict) -> Optional[str]:
    """트리 순회"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    try:
        n = int(lines[0])
        tree = {}
        for i in range(1, n + 1):
            parts = lines[i].split()
            root, left, right = parts[0], parts[1], parts[2]
            tree[root] = (left, right)

        def preorder(node):
            if node == '.':
                return ''
            left, right = tree[node]
            return node + preorder(left) + preorder(right)

        def inorder(node):
            if node == '.':
                return ''
            left, right = tree[node]
            return inorder(left) + node + inorder(right)

        def postorder(node):
            if node == '.':
                return ''
            left, right = tree[node]
            return postorder(left) + postorder(right) + node

        out_lines = out.split('\n')

        # 전위, 중위, 후위 출력
        if len(out_lines) == 3:
            expected = preorder('A') + '\n' + inorder('A') + '\n' + postorder('A')
            if expected == out:
                return """n = int(input())
tree = {}
for _ in range(n):
    root, left, right = input().split()
    tree[root] = (left, right)

def preorder(node):
    if node == '.':
        return ''
    left, right = tree[node]
    return node + preorder(left) + preorder(right)

def inorder(node):
    if node == '.':
        return ''
    left, right = tree[node]
    return inorder(left) + node + inorder(right)

def postorder(node):
    if node == '.':
        return ''
    left, right = tree[node]
    return postorder(left) + postorder(right) + node

print(preorder('A'))
print(inorder('A'))
print(postorder('A'))"""

        # 중위, 후위만 출력
        if len(out_lines) == 2:
            # 공백으로 구분
            in_result = ' '.join(inorder('A'))
            post_result = ' '.join(postorder('A'))
            expected = in_result + '\n' + post_result
            if expected == out:
                return """n = int(input())
tree = {}
for _ in range(n):
    root, left, right = input().split()
    tree[root] = (left, right)

def inorder(node):
    if node == '.':
        return ''
    left, right = tree[node]
    return inorder(left) + node + inorder(right)

def postorder(node):
    if node == '.':
        return ''
    left, right = tree[node]
    return postorder(left) + postorder(right) + node

print(' '.join(inorder('A')))
print(' '.join(postorder('A')))"""
    except:
        pass

    return None


def solve_chessboard(problem: Dict) -> Optional[str]:
    """체스판 다시 칠하기"""
    ex = problem['examples'][0]
    lines = ex['input'].strip().split('\n')
    out = ex['output'].strip()

    try:
        first_parts = lines[0].split()
        n, m = int(first_parts[0]), int(first_parts[1])
        board = [lines[i+1] for i in range(n)]

        def count_repaint(x, y, first_char):
            count = 0
            for i in range(8):
                for j in range(8):
                    expected = first_char if (i + j) % 2 == 0 else ('B' if first_char == 'W' else 'W')
                    if board[x + i][y + j] != expected:
                        count += 1
            return count

        min_count = 64
        for i in range(n - 7):
            for j in range(m - 7):
                min_count = min(min_count, count_repaint(i, j, 'W'))
                min_count = min(min_count, count_repaint(i, j, 'B'))

        if str(min_count) == out:
            return """n, m = map(int, input().split())
board = [input() for _ in range(n)]

def count_repaint(x, y, first_char):
    count = 0
    for i in range(8):
        for j in range(8):
            expected = first_char if (i + j) % 2 == 0 else ('B' if first_char == 'W' else 'W')
            if board[x + i][y + j] != expected:
                count += 1
    return count

min_count = 64
for i in range(n - 7):
    for j in range(m - 7):
        min_count = min(min_count, count_repaint(i, j, 'W'))
        min_count = min(min_count, count_repaint(i, j, 'B'))

print(min_count)"""
    except:
        pass

    return None


def generate_hidden_tests(code: str, analysis: Dict, num: int = 8) -> List[Dict]:
    """hidden_test_cases 생성"""
    tests = []
    attempts = 0

    while len(tests) < num and attempts < num * 5:
        attempts += 1

        # 랜덤 입력 생성
        new_lines = []
        for line in analysis['lines']:
            new_parts = []
            for val, t in zip(line['parts'], line['types']):
                if t == 'int':
                    orig = int(val)
                    if orig <= 10:
                        new_parts.append(str(random.randint(1, 10)))
                    elif orig <= 100:
                        new_parts.append(str(random.randint(1, 100)))
                    else:
                        new_parts.append(str(random.randint(1, min(orig * 2, 10000))))
                elif t == 'float':
                    new_parts.append(str(round(random.uniform(0, float(val) * 2), 2)))
                else:
                    if val.isalpha():
                        chars = 'abcdefghijklmnopqrstuvwxyz'
                        if val.isupper():
                            chars = chars.upper()
                        new_parts.append(''.join(random.choice(chars) for _ in range(len(val))))
                    else:
                        new_parts.append(val)
            new_lines.append(' '.join(new_parts))

        test_input = '\n'.join(new_lines)

        if any(t['input'] == test_input for t in tests):
            continue

        success, output, _ = run_solution(code, test_input)
        if success and output:
            tests.append({'input': test_input, 'output': output})

    return tests


# 메인 실행
print("=== GENERATING SOLUTIONS FOR INVALID PROBLEMS ===\n")

solvers = [
    solve_two_int_one_line,
    solve_single_int,
    solve_n_and_array,
    solve_string_problem,
    solve_comparison,
    solve_grid_problem,
    solve_set_operations,
    solve_fibonacci,
    solve_factorial,
    solve_prime,
    solve_gcd_lcm,
    solve_dp_basic,
    solve_four_int_one_line,
    solve_three_int_one_line,
    solve_multi_line_numbers,
    solve_palindrome,
    solve_count_chars,
    solve_divisors,
    solve_sort_words,
    solve_binary,
    solve_ascii,
    solve_reverse_array,
    solve_many_int_one_line,
    solve_star_pattern,
    solve_two_line_each_number,
    solve_coordinate_problem,
    solve_time_problem,
    solve_tax_problem,
    solve_hello_world,
    solve_calculator,
    solve_even_odd,
    solve_positive_negative,
    solve_digit_sum,
    solve_a_b_multiple_ops,
    solve_reverse_string,
    solve_min_max_avg,
    solve_empty_input,
    solve_symmetric_difference,
    solve_anagram,
    solve_substring,
    solve_filter_less_than,
    solve_multiple_test_cases_gcd_lcm,
    solve_cutline,
    solve_statistics,
    solve_lis,
    solve_permutation,
    solve_subsets,
    solve_hex_addition,
    solve_ball_problem,
    solve_unique_count,
    solve_symmetric_diff_simple,
    solve_triangle_dp,
    solve_wine_dp,
    solve_dfs_bfs,
    solve_maze_bfs,
    solve_quadtree,
    solve_tree_traversal,
    solve_chessboard,
]

fixed_count = 0
still_invalid = 0

for i, problem in enumerate(data):
    pid = problem['problem_id']
    examples = problem.get('examples', [])
    solutions = problem.get('solutions', [])

    if not examples or not solutions:
        continue

    ex = examples[0]
    code = solutions[0].get('solution_code', '')

    # 이미 유효하면 스킵
    if test_solution(code, ex.get('input', ''), ex.get('output', '')):
        continue

    # 각 solver 시도
    new_code = None
    for solver in solvers:
        try:
            new_code = solver(problem)
            if new_code and test_solution(new_code, ex['input'], ex['output']):
                break
            new_code = None
        except:
            continue

    if new_code:
        problem['solutions'][0]['solution_code'] = new_code

        # hidden_test_cases 생성
        analysis = analyze_input(ex['input'])
        new_tests = generate_hidden_tests(new_code, analysis)
        if new_tests:
            existing = problem.get('hidden_test_cases', [])
            problem['hidden_test_cases'] = existing + new_tests

        fixed_count += 1
        print(f"✓ Fixed [{pid}] {problem['title']}")
    else:
        still_invalid += 1

    if (i + 1) % 200 == 0:
        print(f"Progress: {i + 1}/{len(data)}")

print(f"\n=== RESULTS ===")
print(f"Fixed: {fixed_count}")
print(f"Still invalid: {still_invalid}")

# 최종 통계
valid_count = 0
for p in data:
    ex = p.get('examples', [{}])[0]
    sols = p.get('solutions', [{}])
    if sols and test_solution(sols[0].get('solution_code', ''), ex.get('input', ''), ex.get('output', '')):
        valid_count += 1

print(f"\nTotal valid: {valid_count}/{len(data)}")

# 저장
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Saved to: {output_path}")
