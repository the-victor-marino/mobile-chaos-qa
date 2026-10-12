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
    with pytest.raises(ValueError, match="Missing before/after"):
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
