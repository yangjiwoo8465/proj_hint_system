# -*- coding: utf-8 -*-
"""
1039개 문제에 20개 대분류(category) 추가
"""
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

INPUT_FILE = r'C:\Users\playdata2\Desktop\playdata\Workspace\팀프로젝트5\5th-project_mvp\backend\apps\coding_test\data\problems_final_output.json'
OUTPUT_FILE = INPUT_FILE

data = json.load(open(INPUT_FILE, encoding='utf-8-sig'))

# 20개 대분류 매핑 (태그 기반)
CATEGORY_MAPPING = {
    "입출력/기초": [
        "구현", "기초", "사칙연산", "반복문", "조건문", "입출력", "1차원 배열", "2차원 배열",
        "반복", "입출력과 사칙연산", "시간 복잡도"
    ],
    "수학": [
        "수학", "정수론", "소수 판정", "에라토스테네스의 체", "유클리드 호제법", "조합론",
        "약수, 배수와 소수", "중국인의 나머지 정리", "뫼비우스", "페르마의 소정리", "확장 유클리드",
        "포함배제", "카운팅", "수학 1", "수학 2", "수학 3", "Berlekamp", "kitamasa", "Kitamasa",
        "선형점화", "점화식", "라그랑주", "보간", "거듭제곱", "약수"
    ],
    "문자열": [
        "문자열", "KMP", "트라이", "아호 코라식", "라빈 카프", "매내처", "Z", "접미사 배열",
        "접미사트리", "회문", "문자열 알고리즘", "해시"
    ],
    "정렬": [
        "정렬", "카운팅 정렬", "버블정렬", "병합정렬", "정렬/선택"
    ],
    "탐색": [
        "이분 탐색", "매개변수 탐색", "삼분 탐색", "탐색", "binary_search"
    ],
    "자료구조 (기본)": [
        "스택", "큐", "덱", "리스트", "힙", "우선순위 큐", "스택, 큐, 덱",
        "연결 리스트", "배열", "list_operation", "stack_queue"
    ],
    "자료구조 (고급)": [
        "세그먼트 트리", "펜윅 트리", "분리 집합", "유니온 파인드", "세그먼트트리",
        "느리게 갱신되는 세그먼트 트리", "머지 소트 트리", "Splay 트리", "레이지 프로파게이션",
        "구간쿼리", "구간 업데이트", "RMQ", "Heavy-Light 분해", "평방분할", "sqrt_decomposition"
    ],
    "해시/맵": [
        "집합과 맵", "해시", "해시맵", "해시를 사용한 집합과 맵", "트리를 사용한 집합과 맵",
        "hash_map", "딕셔너리"
    ],
    "DP (동적계획법)": [
        "다이나믹 프로그래밍", "DP", "동적 계획법", "배낭 문제", "LCS", "LIS",
        "비트필드를 이용한 다이나믹 프로그래밍", "트리에서의 다이나믹 프로그래밍",
        "동적 계획법 최적화", "분할 정복을 이용한 거듭제곱", "볼록 껍질을 이용한 최적화",
        "dp_basic", "dp_1d", "dp_optimization", "선형계획", "심플렉스"
    ],
    "그래프 (기본)": [
        "그래프 이론", "너비 우선 탐색", "깊이 우선 탐색", "그래프 탐색", "BFS", "DFS",
        "bfs", "dfs", "연결성", "인접리스트"
    ],
    "그래프 (고급)": [
        "최단 경로", "다익스트라", "벨만 포드", "플로이드 워셜", "최소 신장 트리",
        "프림", "크루스칼", "위상 정렬", "강한 연결 요소", "단절점과 단절선",
        "이중 연결 요소", "dijkstra", "bellman_ford", "floyd_warshall", "MST", "최단경로"
    ],
    "트리": [
        "트리", "최소 공통 조상", "트리와 쿼리", "오일러 경로", "센트로이드 분할",
        "Heavy-Light Decomposition", "트리 동형 사상", "서브트리", "centroid_decomp"
    ],
    "그리디": [
        "그리디 알고리즘", "그리디", "greedy_basic"
    ],
    "분할정복": [
        "분할 정복", "분할정복", "분할 정복을 이용한 거듭제곱"
    ],
    "브루트포스/백트래킹": [
        "브루트포스 알고리즘", "백트래킹", "비트마스킹", "비트마스크", "완전 탐색",
        "backtracking_basic", "재귀"
    ],
    "기하학": [
        "기하학", "볼록 껍질", "선분 교차 판정", "회전하는 캘리퍼스", "반평면 교집합",
        "들로네 삼각분할", "보로노이 다이어그램", "기하 1", "기하 2", "기하 3"
    ],
    "네트워크 플로우": [
        "최대 유량", "이분 매칭", "최소 컷", "최소 비용 최대 유량", "네트워크 플로우",
        "최대 유량 최소 컷 정리", "홀정리", "매칭", "이분매칭", "네트워크플로우", "최대유량",
        "hall_theorem"
    ],
    "게임 이론": [
        "게임 이론", "님 게임", "스프라그–그런디 정리", "님게임", "게임이론"
    ],
    "고급 알고리즘": [
        "고속 푸리에 변환", "FFT", "다항식곱셈", "Mo", "mo_algorithm",
        "번사이드", "대칭", "온라인", "페이징", "랜덤화", "매트로이드", "matroid"
    ],
    "기타/특수": [
        "시뮬레이션", "파싱", "애드 혹", "해 구성하기", "역추적", "투 포인터",
        "슬라이딩 윈도우", "누적 합", "스위핑", "좌표 압축", "오프라인 쿼리",
        "two_pointer", "sliding_window", "string_pattern", "string_manip"
    ]
}

# 태그 -> 카테고리 역매핑 생성
tag_to_category = {}
for category, tags in CATEGORY_MAPPING.items():
    for tag in tags:
        tag_to_category[tag.lower()] = category

# step_title 기반 매핑 (태그가 없는 경우 대비)
STEP_TO_CATEGORY = {
    "basic_math": "수학",
    "입출력과 사칙연산": "입출력/기초",
    "조건문": "입출력/기초",
    "반복문": "입출력/기초",
    "1차원 배열": "입출력/기초",
    "2차원 배열": "입출력/기초",
    "정렬": "정렬",
    "문자열": "문자열",
    "재귀": "브루트포스/백트래킹",
    "백트래킹": "브루트포스/백트래킹",
    "브루트 포스": "브루트포스/백트래킹",
    "집합과 맵": "해시/맵",
    "스택, 큐, 덱 1": "자료구조 (기본)",
    "스택, 큐, 덱 2": "자료구조 (기본)",
    "우선순위 큐": "자료구조 (기본)",
    "힙": "자료구조 (기본)",
    "동적 계획법 1": "DP (동적계획법)",
    "동적 계획법 2": "DP (동적계획법)",
    "동적 계획법 3": "DP (동적계획법)",
    "동적 계획법 4": "DP (동적계획법)",
    "동적 계획법 5": "DP (동적계획법)",
    "동적 계획법 최적화 1": "DP (동적계획법)",
    "동적 계획법 최적화 2": "DP (동적계획법)",
    "그래프와 순회": "그래프 (기본)",
    "최단 경로": "그래프 (고급)",
    "최소 신장 트리": "그래프 (고급)",
    "트리": "트리",
    "트리와 쿼리": "트리",
    "최소 공통 조상": "트리",
    "세그먼트 트리 1": "자료구조 (고급)",
    "세그먼트 트리 2": "자료구조 (고급)",
    "세그먼트 트리 3": "자료구조 (고급)",
    "이분 탐색": "탐색",
    "분할 정복": "분할정복",
    "그리디 알고리즘 1": "그리디",
    "그리디 알고리즘 2": "그리디",
    "문자열 알고리즘 1": "문자열",
    "문자열 알고리즘 2": "문자열",
    "기하 1": "기하학",
    "기하 2": "기하학",
    "기하 3": "기하학",
    "네트워크 플로우 1": "네트워크 플로우",
    "네트워크 플로우 2": "네트워크 플로우",
    "네트워크 플로우 3": "네트워크 플로우",
    "네트워크 플로우 4": "네트워크 플로우",
    "이분 매칭": "네트워크 플로우",
    "스프라그 그런디 정리": "게임 이론",
    "고속 푸리에 변환": "고급 알고리즘",
    "평방 분할": "자료구조 (고급)",
    "유니온 파인드 1": "자료구조 (고급)",
    "유니온 파인드 2": "자료구조 (고급)",
    "강한 연결 요소": "그래프 (고급)",
    "위상 정렬": "그래프 (고급)",
}


def get_category(problem):
    """문제의 태그와 step_title을 기반으로 카테고리 결정"""
    tags = problem.get('tags', [])
    step_title = problem.get('step_title', '')

    # 1. 태그 기반 매칭 (우선순위 순서로)
    priority_order = [
        "네트워크 플로우", "게임 이론", "기하학", "고급 알고리즘",
        "자료구조 (고급)", "그래프 (고급)", "트리", "DP (동적계획법)",
        "그래프 (기본)", "문자열", "분할정복", "브루트포스/백트래킹",
        "그리디", "탐색", "자료구조 (기본)", "해시/맵", "정렬", "수학", "입출력/기초"
    ]

    tag_matches = set()
    for tag in tags:
        cat = tag_to_category.get(tag.lower())
        if cat:
            tag_matches.add(cat)

    # 우선순위 순서로 매칭
    for cat in priority_order:
        if cat in tag_matches:
            return cat

    # 2. step_title 기반 매칭
    if step_title in STEP_TO_CATEGORY:
        return STEP_TO_CATEGORY[step_title]

    # 3. step_title 부분 매칭
    step_lower = step_title.lower()
    if 'dp' in step_lower or '동적' in step_lower:
        return "DP (동적계획법)"
    if '그래프' in step_lower:
        return "그래프 (기본)"
    if '트리' in step_lower:
        return "트리"
    if '세그먼트' in step_lower or '펜윅' in step_lower:
        return "자료구조 (고급)"
    if '문자열' in step_lower or 'string' in step_lower:
        return "문자열"
    if '정렬' in step_lower:
        return "정렬"
    if '수학' in step_lower or 'math' in step_lower:
        return "수학"
    if '기하' in step_lower:
        return "기하학"
    if '플로우' in step_lower or '매칭' in step_lower:
        return "네트워크 플로우"
    if '탐색' in step_lower or 'search' in step_lower:
        return "탐색"
    if '그리디' in step_lower or 'greedy' in step_lower:
        return "그리디"
    if '백트래킹' in step_lower or 'backtrack' in step_lower:
        return "브루트포스/백트래킹"
    if '스택' in step_lower or '큐' in step_lower or '힙' in step_lower:
        return "자료구조 (기본)"
    if '해시' in step_lower or 'hash' in step_lower or '맵' in step_lower:
        return "해시/맵"

    # 4. 레벨 기반 기본 분류
    level = problem.get('level', 1)
    if level <= 5:
        return "입출력/기초"
    elif level <= 10:
        return "수학"
    else:
        return "기타/특수"


print("=" * 60)
print("         1039개 문제에 20개 대분류 추가")
print("=" * 60)

# 카테고리 추가
category_count = {}
for p in data:
    cat = get_category(p)
    p['category'] = cat
    category_count[cat] = category_count.get(cat, 0) + 1

# 결과 출력
print("\n카테고리별 문제 분포:")
print("-" * 60)
for cat in [
    "입출력/기초", "수학", "문자열", "정렬", "탐색",
    "자료구조 (기본)", "자료구조 (고급)", "해시/맵",
    "DP (동적계획법)", "그래프 (기본)", "그래프 (고급)", "트리",
    "그리디", "분할정복", "브루트포스/백트래킹", "기하학",
    "네트워크 플로우", "게임 이론", "고급 알고리즘", "기타/특수"
]:
    cnt = category_count.get(cat, 0)
    bar = "█" * (cnt // 10) + "░" * ((100 - cnt) // 10)
    print(f"  {cat:20s}: {cnt:4d}개  {bar}")

print("-" * 60)
print(f"총 카테고리 수: {len(category_count)}개")
print(f"총 문제 수: {len(data)}개")

# 저장
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n저장 완료: {OUTPUT_FILE}")
