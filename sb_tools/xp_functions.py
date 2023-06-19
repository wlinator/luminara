def xp_needed_for_next_level(current_level):
    formula_mapping = {
        (10, 19): lambda level: 12 * level + 27,
        (20, 29): lambda level: 15 * level + 27,
        (30, 39): lambda level: 18 * level + 27,
        (40, 49): lambda level: 21 * level + 27,
        (50, 59): lambda level: 24 * level + 27,
        (60, 69): lambda level: 27 * level + 27,
        (70, 79): lambda level: 30 * level + 27,
        (80, 89): lambda level: 33 * level + 27,
        (90, 99): lambda level: 36 * level + 27,
        (100, 109): lambda level: 39 * level + 27,
    }

    for level_range, formula in formula_mapping.items():
        if level_range[0] <= current_level <= level_range[1]:
            return formula(current_level)

    # For levels below 10 and levels 110 and above
    return 9 * current_level + 27 if current_level < 30 else 42 * current_level + 27
