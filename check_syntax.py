import pathlib, json, sys, traceback

def check_file(p):
    try:
        compile(p.read_text(), str(p), 'exec')
    except Exception as e:
        return {"file": str(p), "error": traceback.format_exception_only(type(e), e)[0].strip()}
    return None

issues = []
for p in pathlib.Path('.').rglob('*.py'):
    # skip compiled .pyc etc.
    if p.suffix != '.py':
        continue
    result = check_file(p)
    if result:
        issues.append(result)

print(json.dumps(issues, indent=2))
