# Direction pass for EP1 (master revision): who is not in the shot yet, who walks in and when, Agnes's peeks,
# the figure in the belfry, camera shakes, zoom-blur transitions and the colour grade. exec'd by anim_ep1.py.
# Times are seconds from the start of the panel's segment unless given as a shot number ("s204").

DIRECT = {
    # convent front: the camera opens wide on the building; Mek walks in, then Daeng runs in, then the Mother walks in
    "59-62":  {"hide": ["daeng", "cat"], "enter": [["mek", .4, "left", False]]},
    "65-68":  {"hide": ["cat"], "enter": [["daeng", .2, "left", True]]},
    "69-74":  {"enter": [["cat", .3, "right", False]]},
    # piano room: Agnes is not there until she appears at the door
    "107-110": {"hide": ["agnes"]},
    "111-116": {"hide": ["agnes"]},
    "117-122": {"peek": {"cid": "agnes", "door": [452, 262, 540, 610], "walk": [474, 640, .64]}, "shake": [[2.0, .5]], "rack": True},
    # kitchen: Agnes only exists from her first look round the door
    "190-193": {"hide": ["agnes"]},
    "194-203": {"hide": ["agnes"]},
    "204-208": {"peek": {"cid": "agnes", "door": [408, 300, 512, 640], "walk": [430, 690, .7]}, "shake": [[2.0, .5]], "rack": True},
    "214-215": {"hide": ["agnes"]},
    # foyer: Mek finds the doll; Agnes peeks round the front door, then walks in toward the stairs
    "185-189": {"peek": {"cid": "agnes", "door": [424, 262, 540, 642], "walk": [360, 720, .74]}, "shake": [[2.0, .45]], "rack": True},
    # the night of the bells, the body, the figure in the belfry
    "235-239": {"shake": [["bell", 1.0]]},
    "247-248": {"shake": [[.3, .8]]},
    "249-253": {"shake": [["s250", 1.0]]},
    "254-255": {"shade": True, "shake": [[1.2, .45]]},
    "282-285": {"shake": [["s284", .9]]},
    # hook: four fast shots before the title
    "302": {"shake": [["bell", .8]]},
    "304": {"shake": [[.5, .7]]},
    "306": {"shade": True},
    "92-96": {"hide": ["rosa", "mek"]},          # Martha's stone alone in the frame (no cut-off legs)
    # who's who when Mek arrives: camera on one person at a time, with their name card (no lines for them yet)
    "311": {"focus": "cat"}, "312": {"focus": "luc"}, "313": {"focus": "mariam"}, "314": {"focus": "rosa"},
    "315": {"focus": "agnes"}, "317": {"focus": "jos"}, "318": {"focus": "daeng"},
}
# segments that open with a fast zoom-blur + whoosh instead of a dip to black
ZOOM_IN = {"304", "306", "31", "33", "49-53", "87", "88-89", "165-171", "217-221", "244-246", "256-262", "277-281"}
GRADE = {}
for st in "tower_fog tower_night chapel_night thana_night rosa_bed rosa_room oldwing veranda call call_mek drain clock evidence_wall rules1 sisters_ext".split(): GRADE[st] = "night"
for st in "flash_dorm dream".split(): GRADE[st] = "flash"

# name card the first time each main character is on screen (user: who is who must be clear)
NAMECARD = {"mek": ("เมฆ", "ช่างภาพ · ผู้เล่าเรื่อง"), "james": ("เจม", "เพื่อนสนิทของเมฆ"), "rosa": ("ซิสเตอร์โรซา", "แม่ชีฝึกหัด"),
            "cat": ("มาเธอร์คาทารีนา", "อธิการิณี"), "daeng": ("ป้าแดง", "แม่ครัว"), "jos": ("คุณพ่อยอแซฟ", "บาทหลวง"),
            "mariam": ("ซิสเตอร์มาเรียม", "แฝดคนที่รอดจากไฟ"), "agnes": ("ซิสเตอร์อักเนส", "ห้องพยาบาล"), "luc": ("มาเธอร์ลูเซีย", "อดีตอธิการิณี"),
            "thana": ("ร.ต.อ.ธนา", "สน.บางกอกน้อย")}
