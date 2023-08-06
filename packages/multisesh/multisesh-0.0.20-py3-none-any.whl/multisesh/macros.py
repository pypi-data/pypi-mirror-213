macro1 = """
rename("active")
run("Duplicate...", "duplicate")
selectWindow("active")
run("Close")
selectWindow("active-1")
run("Re-order Hyperstack ...", "channels=[Slices (z)] slices=[Channels (c)] frames=[Frames (t)]")
"""

macro2 = """
selectWindow("active-1")
run("Close")
selectWindow("Flat-field:active-1")
"""

macro3 = """
selectWindow("Flat-field:active-1")
run("Close")
selectWindow("Dark-field:active-1")
"""

macro4 = """
selectWindow("Dark-field:active-1")
run("Close")
run("Collect Garbage")
"""