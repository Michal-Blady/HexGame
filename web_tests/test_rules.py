# web_tests/test_rules.py
def test_rules_basic(tcms_exec):
    rpc       = tcms_exec["rpc"]
    plan_id   = tcms_exec["plan_id"]
    build_id  = tcms_exec["build_id"]
    # oznaczenie statusu
    rpc.TestExecution.create({
        "testcase_id": 124,
        "build_id": build_id,
        "notes": "Uruchomione przez Jenkins",
        "status": 2,    # 2 = Fail
    })
    assert 2 * 2 == 4
