# Tighter cut of EP1 (user: 15-20 min, hook first, less confusing). Shots listed here are left out of the episode;
# their art and voice files stay on disk. ORDER is the running order: the hook (301-304 + the twins frame 31-33 and the
# title) first, then the story, with the clue card (305) right before the closing question.
CUT = {3, 4, 8, 10, 12, 15, 17, 18, 19,
       20, 24, 26, 27,
       35, 37, 38, 45, 46, 49, 51, 52, 53, 58,
       60, 61, 67, 71, 72, 73, 74, 76,
       79, 85,
       89, 91, 97, 98, 99, 100, 101, 102, 103, 105, 106,
       123,
       125, 126, 128, 129, 130, 132,
       134, 137, 138, 140,
       143, 144, 150, 151, 153, 158,
       160, 161, 163, 165, 166, 167, 169, 172,
       182,
       190, 193, 198, 199, 210, 212,
       216, 217, 218, 219, 220, 222, 224, 228, 230, 235,
       263, 264, 267,
       277, 279}
_story = [n for n in range(1, 288) if n not in CUT and n not in (31, 32, 33)]
_i = _story.index(286)
ORDER = [301, 302, 303, 304, 31, 32, 33] + _story[:_i] + [305] + _story[_i:]
