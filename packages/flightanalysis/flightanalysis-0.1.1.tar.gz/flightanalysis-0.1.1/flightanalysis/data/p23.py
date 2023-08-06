"""This file defines a P23 sequence using the ManDef Classes and helper functions."""
from flightanalysis.schedule.definition import *
from flightanalysis.schedule.elements import *
from flightanalysis.criteria import *
import numpy as np

c45 = np.cos(np.radians(45))


p23_def = SchedDef([
    f3amb.create(ManInfo(
            "Top Hat", "tHat", k=4, position=Position.CENTRE, 
            start=BoxLocation(Height.BTM, Direction.UPWIND, Orientation.UPRIGHT),
            end=BoxLocation(Height.BTM)
        ),[
            f3amb.loop(np.pi/2),
            f3amb.roll("2x4"),
            f3amb.loop(np.pi/2), 
            f3amb.roll("1/2",line_length=100),
            f3amb.loop(-np.pi/2),
            f3amb.roll("2x4"),
            f3amb.loop(-np.pi/2)
        ]),
    f3amb.create(ManInfo("Half Square Loop", "hSqL", 2, Position.END,
            BoxLocation(Height.BTM, Direction.UPWIND, Orientation.INVERTED),
            BoxLocation(Height.TOP)
        ),[
            f3amb.loop(-np.pi/2),
            f3amb.roll("1/2"),
            f3amb.loop(np.pi/2)
        ]),
    f3amb.create(ManInfo("Humpty Bump", "hB", 4, Position.CENTRE,
            BoxLocation(Height.TOP, Direction.DOWNWIND, Orientation.INVERTED),
            BoxLocation(Height.TOP)
        ),[
            f3amb.loop(np.pi/2),
            f3amb.roll("1/1"), # TODO this should change to 1 sometime
            f3amb.loop(np.pi),
            f3amb.roll("1/2"),
            f3amb.loop(-np.pi/2)
        ]),
    f3amb.create(ManInfo("Half Square on Corner", "hSqLC", 3, Position.END,
            BoxLocation(Height.TOP, Direction.DOWNWIND, Orientation.UPRIGHT),
            BoxLocation(Height.BTM)
        ),[
            f3amb.loop(-np.pi/4),
            f3amb.roll("1/2"),
            f3amb.loop(np.pi/2),
            f3amb.roll("1/2"),
            f3amb.loop(-np.pi/4)
        ], line_length=130*c45),
    f3amb.create(ManInfo("45 Upline Snaps", "upL", 5, Position.CENTRE,
            BoxLocation(Height.BTM, Direction.UPWIND, Orientation.INVERTED),
            BoxLocation(Height.TOP)
        ),[
            f3amb.loop(-np.pi/4),
            f3amb.snap(1.5),
            f3amb.loop(-np.pi/4) 
        ], line_length=110 + 130/c45),
    f3amb.create(ManInfo("Half 8 Sided Loop", "h8L", 3, Position.END,
            BoxLocation(Height.TOP, Direction.UPWIND, Orientation.UPRIGHT),
            BoxLocation(Height.BTM)
        ),[
            f3amb.loop(-np.pi/4),
            f3amb.line(),
            f3amb.loop(-np.pi/4),
            f3amb.line(),
            f3amb.loop(-np.pi/4),
            f3amb.line(),
            f3amb.loop(-np.pi/4)            
        ], line_length=50),
    f3amb.create(ManInfo("Roll Combo", "rollC", 4, Position.CENTRE,
            BoxLocation(Height.BTM, Direction.DOWNWIND, Orientation.INVERTED),
            BoxLocation(Height.BTM)
        ),[
            f3amb.roll([np.pi, np.pi, -np.pi, -np.pi], padded=False)
        ]),
    f3amb.create(ManInfo("Immelman Turn", "pImm", 2, Position.END,
            BoxLocation(Height.BTM, Direction.DOWNWIND, Orientation.INVERTED),
            BoxLocation(Height.TOP)
        ),[
            f3amb.loop(-np.pi),
            f3amb.roll("1/2", padded=False)
        ],loop_radius=100),
    f3amb.create(ManInfo("Inverted Spin",  "iSp",  4, Position.CENTRE,
            BoxLocation(Height.TOP, Direction.UPWIND, Orientation.INVERTED),
            BoxLocation(Height.BTM)
        ),[
            0,
            f3amb.spin(2.5),
            f3amb.line(),
            f3amb.loop(np.pi/2)
        ]),
    f3amb.create(
        ManInfo("Humpty Bump",  "hB2",  3, Position.END,
            BoxLocation(Height.BTM, Direction.UPWIND, Orientation.UPRIGHT),
            BoxLocation(Height.BTM)
        ),
        [
            f3amb.loop(np.pi/2),
            f3amb.roll("roll_option[0]"),
            f3amb.loop(np.pi),
            f3amb.roll("roll_option[1]"),
            f3amb.loop(-np.pi/2)   
        ], 
        roll_option=ManParm(
            "roll_option", 
            Combination([
                [np.pi, np.pi],
                [np.pi, -np.pi],
                [-np.pi, np.pi],
                [-np.pi, -np.pi],
                [np.pi*1.5, -np.pi/2], 
                [-np.pi*1.5, np.pi/2]
            ]),
            0
        )
    ),
    f3amb.create(ManInfo("Reverese Figure Et",  "rEt",  4, Position.CENTRE,
            BoxLocation(Height.BTM, Direction.DOWNWIND, Orientation.INVERTED),
            BoxLocation(Height.TOP)
        ),[
            f3amb.loop(-np.pi/4),
            f3amb.roll([np.pi, -np.pi], line_length=str(2*f3amb.mps.loop_radius)),
            f3amb.loop(7*np.pi/4),
            f3amb.roll("2x4", line_length=100),
            f3amb.loop(-np.pi/2)
        ], 
        loop_radius=70
    ),
    f3amb.create(ManInfo("Half Square Loop", "sqL", 2,Position.END,
            BoxLocation(Height.TOP, Direction.DOWNWIND, Orientation.UPRIGHT),
            BoxLocation(Height.BTM)
        ),[
            f3amb.loop(-np.pi/2),
            f3amb.roll("1/2"),
            f3amb.loop(np.pi/2)
        ]),
    f3amb.create(ManInfo("Figure M", "M", 5,Position.CENTRE,
            BoxLocation(Height.BTM, Direction.UPWIND, Orientation.UPRIGHT),
            BoxLocation(Height.BTM)
        ),[
            f3amb.loop(np.pi/2),
            f3amb.roll("roll_option[0]"),
            f3amb.stallturn(),
            f3amb.line(),
            f3amb.loop(-np.pi),
            f3amb.line(),
            f3amb.stallturn(),
            f3amb.roll("roll_option[1]"),
            f3amb.loop(np.pi/2)
        ],
        roll_option=ManParm(
            "roll_option", 
            Combination([
                [np.pi*3/2, np.pi*3/2],
                [-np.pi*3/2, -np.pi*3/2],
            ]),
            1
        ),
        line_length=150.0,
        speed=ManParm("speed", inter_free, 30.0)
    ),
    f3amb.create(ManInfo("Fighter Turn", "fTrn", 4,Position.END,
            BoxLocation(Height.BTM, Direction.UPWIND, Orientation.UPRIGHT),
            BoxLocation(Height.BTM)
        ),[
            f3amb.loop(np.pi/4),
            f3amb.roll("roll_option[0]"),
            f3amb.loop(-np.pi),
            f3amb.roll("roll_option[1]"),
            f3amb.loop(np.pi/4)
        ],
        roll_option=ManParm("roll_option", Combination(
            [
                [-np.pi/2, np.pi/2],
                [np.pi/2, -np.pi/2]
            ]
        ),0)),
    f3amb.create(ManInfo("Triangular Loop", "trgle", 3,Position.CENTRE,
            BoxLocation(Height.BTM, Direction.DOWNWIND, Orientation.UPRIGHT),
            BoxLocation(Height.BTM)
        ),[
            f3amb.roll("1/2", padded=False),
            f3amb.line(length=str(f3amb.mps.line_length*c45-0.5*np.pi*f3amb.mps.speed/f3amb.mps.partial_roll_rate)),
            f3amb.loop(-np.pi*3/4),
            f3amb.roll("2x4"),
            f3amb.loop(np.pi/2),
            f3amb.roll("2x4"),
            f3amb.loop(-np.pi*3/4),
            f3amb.line(length=str(f3amb.mps.line_length*c45-0.5*np.pi*f3amb.mps.speed/f3amb.mps.partial_roll_rate)),
            f3amb.roll("1/2", padded=False)
        ]),
    f3amb.create(ManInfo("Shark Fin", "sFin", 3,Position.END,
            BoxLocation(Height.BTM, Direction.DOWNWIND, Orientation.UPRIGHT),
            BoxLocation(Height.BTM)
        ),[
            f3amb.loop(np.pi/2),
            f3amb.roll("1/2", line_length=80),
            f3amb.loop(-np.pi*3/4),
            f3amb.roll("2X4", line_length=80/c45 + 60),
            f3amb.loop(-np.pi/4),
        ],loop_radius=30),
    f3amb.create(ManInfo("Loop", "loop", 3,Position.CENTRE,
            BoxLocation(Height.BTM, Direction.UPWIND, Orientation.INVERTED),
            BoxLocation(Height.BTM)
        ),[
            f3amb.loop(-np.pi*3/4),
            f3amb.loop(-np.pi/2,roll="roll_option"),
            f3amb.loop(np.pi*3/4)    
        ],
        loop_radius=80,
        roll_option=ManParm(
            "roll_option", 
            Combination([[np.pi], [-np.pi]]), 0
        ))
])

if __name__ == "__main__":
    
    p23_def.to_json("flightanalysis/data/p23.json")
    #from flightplotting import plotsec

    #p23, template = p23_def.create_template(170, 1)
    #from flightplotting import plotsec
    
    #plotsec(template).show()