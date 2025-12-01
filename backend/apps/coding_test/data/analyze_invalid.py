import json
import subprocess

# Load all problems
with open('problems_all_fixed.json', 'r', encoding='utf-8-sig') as f:
    all_problems = json.load(f)

# Load valid problems
with open('problems_final_output.json', 'r', encoding='utf-8-sig') as f:
    valid_problems = json.load(f)

valid_ids = {p['problem_id'] for p in valid_problems}
invalid_problems = [p for p in all_problems if p['problem_id'] not in valid_ids]

print(f'Invalid problems: {len(invalid_problems)}')
print()

# Analyze errors
errors = {'ValueError': [], 'IndexError': [], 'EOFError': [], 'Wrong Answer': [], 'Timeout': [], 'Other': [], 'Placeholder': []}

for p in invalid_problems:
    code = p.get('solution_code', '')
    examples = p.get('examples', [])

    if not examples or not examples[0].get('input') or examples[0].get('output') in ['출력 예제', '', None]:
        errors['Placeholder'].append(p)
        continue

    test_input = examples[0]['input'].replace('\r\n', '\n').replace('\r', '\n')
    expected = examples[0]['output'].strip()

    try:
        result = subprocess.run(
            ['python', '-c', code],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=3
        )
        actual = result.stdout.strip()
        if result.returncode != 0:
            err = result.stderr
            if 'ValueError' in err:
                errors['ValueError'].append((p, err[:200]))
            elif 'IndexError' in err:
                errors['IndexError'].append((p, err[:200]))
            elif 'EOFError' in err:
                errors['EOFError'].append((p, err[:200]))
            else:
                errors['Other'].append((p, err[:200]))
        elif actual != expected:
            errors['Wrong Answer'].append((p, actual[:80], expected[:80]))
    except subprocess.TimeoutExpired:
        errors['Timeout'].append(p)
    except Exception as e:
        errors['Other'].append((p, str(e)[:200]))

print('Error distribution:')
for k, v in errors.items():
    print(f'  {k}: {len(v)}')

print()
print('=== Placeholder problems ===')
for p in errors['Placeholder'][:5]:
    print(f"  [{p['problem_id']}] {p['title']}")

print()
print('=== ValueError problems ===')
for item in errors['ValueError'][:15]:
    p = item[0]
    err = item[1] if len(item) > 1 else ''
    ex = p.get('examples', [{}])[0]
    inp = ex.get('input', '')[:80].replace('\n', '|')
    print(f"  [{p['problem_id']}] {p['title']}")
    print(f"    input: {inp}")

print()
print('=== IndexError problems ===')
for item in errors['IndexError'][:10]:
    p = item[0]
    ex = p.get('examples', [{}])[0]
    inp = ex.get('input', '')[:80].replace('\n', '|')
    print(f"  [{p['problem_id']}] {p['title']}")
    print(f"    input: {inp}")

print()
print('=== Wrong Answer problems ===')
for item in errors['Wrong Answer'][:20]:
    p, actual, expected = item
    print(f"  [{p['problem_id']}] {p['title']}")
    print(f"    exp: {expected[:50]}")
    print(f"    got: {actual[:50]}")
