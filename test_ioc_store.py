from iocstore import IOCStore

def test_known_bad_url():
    store = IOCStore()
    store.add("http://evil.example/malware.exe")
    assert store.is_bad("http://evil.example/malware.exe") == True

def test_clean_url():
    store = IOCStore()
    store.add("http://evil.example/malware.exe")
    assert store.is_bad("http://google.com") == False

def test_missing_url():
    store = IOCStore()
    store.load("missing.csv")
    store.is_bad("http://evil.example/malware.exe") == False