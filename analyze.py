import pathlib, json, sys, traceback
issues = []
for py_path in pathlib.Path('.').rglob('*.py'):
    try:
        src = py_path.read_text(encoding='utf-8')
        compile(src, str(py_path), 'exec')
    except Exception as e:
        issues.append({
            "file": str(py_path),
            "error": ''.join(traceback.format_exception_only(type(e), e)).strip()
        })
print(json.dumps(issues, indent=2))
