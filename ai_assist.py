def ai_detect_intent(sentence):
    sentence = sentence.lower()

    ai_map = {
        "CREATE_FOLDER": ["build folder", "generate folder"],
        "CREATE_FILE": ["generate file", "new file"],
        "DELETE_FILE": ["erase file"],
        "DELETE_FOLDER": ["erase folder"],
        "LIST_FILES": ["what files are here"],
        "CURRENT_DIR": ["where am i located"],
        "GO_BACK": ["go previous", "step back"],
        "GO_HOME": ["go to home directory"]
    }

    for intent, examples in ai_map.items():
        for ex in examples:
            if ex in sentence:
                return intent, 0.85

    return "UNKNOWN", 0.0
