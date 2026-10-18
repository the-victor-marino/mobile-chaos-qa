import pytest
from mobile_chaos_qa.scenarios import parse_state, assert_preserved, run_resume_scenario

def test_parse_instrumented_logcat():
    assert parse_state('10-10 I/MobileChaosDemo: GAME_STATE:{"level":12,"coins":500}') == {"level":12,"coins":500}

def test_progression_loss_is_a_failed_assertion():
    result = assert_preserved({"level":12,"coins":500},{"level":12,"coins":0})
    assert not result.passed

def test_resumed_game_preserves_progression():
    assert assert_preserved({"level":12,"coins":500},{"level":12,"coins":500}).passed

def test_missing_evidence_is_not_treated_as_pass(tmp_path):
    def fake_adb(args):
        return "no evidence"
    with pytest.raises(ValueError, match="No GAME_STATE"):
        run_resume_scenario("emulator-5554","pkg",".MainActivity",tmp_path,adb=fake_adb,pause=lambda _: None)

def test_adb_scenario_writes_machine_readable_evidence(tmp_path):
    def fake_adb(args):
        if "logcat" in args and "-d" in args:
            return '\n'.join(['I/MobileChaosDemo: GAME_STATE:{"level":12,"coins":500}', 'I/MobileChaosDemo: GAME_STATE:{"level":12,"coins":500}'])
        return ""
    result = run_resume_scenario("emulator-5554","pkg",".MainActivity",tmp_path,adb=fake_adb,pause=lambda _: None)
    assert result.passed
    assert (tmp_path/"result.json").exists()
    assert (tmp_path/"logcat.txt").exists()

@pytest.mark.parametrize("state", [{}, {"level": 12}, {"level": True, "coins": 500}, {"level": 12, "coins": "500"}])
def test_incomplete_or_invalid_state_cannot_pass(state):
    with pytest.raises(ValueError, match="integer level and coins"):
        assert_preserved(state, state)

def test_initial_launch_logs_cannot_substitute_for_resume_evidence(tmp_path):
    reads = 0
    def fake_adb(args):
        nonlocal reads
        if "-d" in args:
            reads += 1
            return 'GAME_STATE:{"level":12,"coins":500}\n' * 2 if reads == 1 else ""
        return ""
    with pytest.raises(ValueError, match="No GAME_STATE"):
        run_resume_scenario("emulator-5554", "pkg", ".MainActivity", tmp_path, adb=fake_adb, pause=lambda _: None)

def test_screen_lock_compares_state_across_lock_not_a_later_home_cycle(tmp_path):
    from mobile_chaos_qa.interruptions import run_screen_lock_scenario
    commands = []
    locked = False
    def fake_adb(args):
        nonlocal locked
        commands.append(args)
        if "KEYCODE_SLEEP" in args:
            locked = True
        if "-d" in args:
            coins = 0 if locked else 500
            return f'GAME_STATE:{{"level":12,"coins":{coins}}}'
        return ""
    result = run_screen_lock_scenario("emulator-5554", "pkg", ".MainActivity", tmp_path, adb=fake_adb, pause=lambda _: None)
    assert not result.passed
    assert result.name == "screen_lock_preserves_progress"
    assert not any("KEYCODE_HOME" in cmd for cmd in commands)
