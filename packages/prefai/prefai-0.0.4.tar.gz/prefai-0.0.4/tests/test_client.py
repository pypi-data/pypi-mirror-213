from prefai import prefai_client, PrefaiError
import os

test_user_email = os.getenv("PREFAI_TEST_USER_EMAIL")

def test_add_record_bad_api_key():
    orig_api_key = prefai_client.api_key 
    prefai_client.api_key = "BAD KEY"
    success = False
    try:
        prefai_client.add_record(
            user_email = test_user_email,
            user_action = "Does this recipe have tree nuts? Can you modify if so?",
        )
        success = True
    except PrefaiError as e:
        assert e.code == 401
        assert e.detail == 'Invalid API key'
    assert not success
    prefai_client.api_key = orig_api_key

def test_add_record_none_api_key():
    orig_api_key = prefai_client.api_key 
    prefai_client.api_key = None
    success = False
    try:
        prefai_client.add_record(
            user_email = test_user_email,
            user_action = "Does this recipe have tree nuts? Can you modify if so?",
        )
        success = True
    except PrefaiError as e:
        assert e.code == 401
        assert e.detail == 'Invalid API key'
    assert not success
    prefai_client.api_key = orig_api_key

def test_add_record_missing_user():
    success = False
    try:
        prefai_client.add_record(
            # Missing user_email or user_id
            user_action = "Does this recipe have tree nuts? Can you modify if so?",
        )
        success = True
    except PrefaiError as e:
        assert e.code == 422
        assert e.detail == "Either user_email or user_id must be provided (but not both)"
    assert not success

def test_add_record_missing_source():
    success = False
    try:
        prefai_client.add_record(
            user_email = test_user_email,
            # Missing source
        )
        success = True
    except TypeError as e:
        assert e.args[0] == "add_record() missing 1 required positional argument: 'user_action'"
    assert not success


def test_add():
    res = prefai_client.add_record(
        user_email = test_user_email,
        user_action = "Does this recipe have tree nuts? Can you modify if so?",
    )
    assert res.get('success')
    assert 'record_id' in res

def test_add_with_context():
    res = prefai_client.add_record(
        user_email = test_user_email,
        context = """User: How do I ask someone's name in French?
        
        AI: You would ask: "Comment vous appelez-vous?" """,
        user_action = "Is that a casual way to ask? I don't want to sound too formal.",
    )
    assert res.get('success')
    assert 'record_id' in res

def test_add_record_with_unknown_email():
    user_email = "unknown-email@pref.ai"
    res = prefai_client.add_record(
        user_email = user_email,
        user_action = "Does this recipe have tree nuts? Can you modify if so?",
    )
    assert res.get('success')
    assert 'record_id' in res

def test_retrieve():
    res = prefai_client.retrieve_records(
        user_email = test_user_email,
        context = "User",
        user_action = "How do you say I love you in Spanish?",
        min_similarity = -1.0
    )
    assert res.get('success')
    assert res['records'][0]['user_action'].startswith('Is that a casual way to ask?')
    print(res['records'])

def test_pref_prompt():
    res = prefai_client.pref_prompt(
        user_email = test_user_email,
        context = "User: Hola.\nAI: Hola!",
        user_action = "How do you say I love you in Spanish?",
        min_similarity = -1.0
    )
    assert res.get('success')
    return res
    # assert res['records'][0]['user_action'].startswith('Is that a casual way to ask?')
    # print(res['records'])

if __name__ == "__main__":
    res = test_pref_prompt()
