def head_bytes(path, n=262144):
    with open(path, "rb") as f:
        return f.read(n)

def read_text(path, limit=20000):
    with open(path, "rb") as f:
        return f.read(limit).decode("utf-8", errors="replace")
