# web_tests/test_ai.py
def test_ai_simple(tcms_exec):
    # tu sprawdzasz logikę AI, a po teście rejestrujesz wynik w Kiwi
    rpc       = tcms_exec["rpc"]
    plan_id   = tcms_exec["plan_id"]
    build_id  = tcms_exec["build_id"]
    # przykład: dodajemy wykonanie testu o "testcase_id = 123"
    rpc.TestExecution.create({
        "testcase_id": 123,
        "build_id": build_id,
        "notes": "Uruchomione przez Jenkins",
        "status": 1,   # 1 = Pass, 2 = Fail, 4 = Blocked itp.
    })
    assert 1 + 1 == 2
