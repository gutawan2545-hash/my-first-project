# EP1 cut (user: mysterious and twisty but easy to follow; side stories wait for later episodes; when Mek arrives he says
# how many people live in the convent and who they are). Shots listed here are left out; art and voice files stay on disk.
# ORDER: hook (301-306 + twins 31-33), the story, the who's-who roll call (310-318) right after the Mother's rules,
# the clue card (305) before the closing question.
CUT = {3, 4, 8, 10, 12, 15, 17, 18, 19,
       20, 24, 26, 27,
       35, 37, 38, 45, 46, 49, 51, 52, 53, 58,
       60, 61, 67, 71, 72, 73, 74, 76,
       78, 79, 82, 83, 84, 85,                          # Father Joseph: only the welcome and the chapel key stay
       89, 91, 93, 94, 95, 97, 98, 99, 100, 101, 102, 103, 105, 106,   # the nameless grave waits for a later episode
       114, 115, 116, 123,                              # Mariam's name rule waits
       124, 125, 126, 127, 128, 129, 130, 131, 132, 133,   # dinner with the priest: later episode
       134, 137, 138, 140,
       143, 144, 145, 146, 147, 148,                    # counting the sisters: EP5
       149, 150, 151, 152, 153, 154, 155, 156, 157, 158,   # Mother Lucia's words: later episode (she is introduced in the roll call)
       160, 161, 163, 164, 165, 166, 167, 169, 172,
       182,
       190, 193, 194, 195, 198, 199, 210, 211, 212, 213,
       216, 217, 218, 219, 220, 222, 224, 228, 230, 235,
       263, 264, 267, 276,                              # the missing tower key waits
       277, 279}
_story = [n for n in range(1, 288) if n not in CUT and n not in (31, 32, 33)]
_story = _story[:_story.index(70) + 1] + [310, 311, 312, 313, 314, 315, 316, 317, 318] + _story[_story.index(70) + 1:]
_i = _story.index(286)
ORDER = [301, 302, 303, 304, 306, 31, 32, 33] + _story[:_i] + [305] + _story[_i:]
