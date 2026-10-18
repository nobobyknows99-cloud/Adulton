# Adulton — expanded Ren'Py project
# Title, music, CG placeholders, more characters, and deeper route structure.

init python:
    # Helper to clamp values
    def clamp(v, a=0, b=10):
        return max(a, min(b, v))

# Images (replace with your art files in game/images/)
image bg lounge = "images/bg_lounge.png"
image bg balcony = "images/bg_balcony.png"
image bg street = "images/bg_street.png"
image title = "images/title.png"
image cg_maya_close = "images/cg_maya_close.png"
image cg_noah_close = "images/cg_noah_close.png"

# Characters
define narrator = Character(None)
define p = Character("You")
define maya = Character("Maya", color="#f4b6c2")
define noah = Character("Noah", color="#9cc9ff")
define aria = Character("Aria", color="#ffd166")
define celeste = Character("Celeste", color="#d9b4ff")

default adult_verified = False
default route = "none"
default romance_maya = 0
default romance_noah = 0
default romance_aria = 0
default romance_celeste = 0

default play_music = True

label splashscreen:
    scene black
    with fade
    # Optional: show title image if present
    if renpy.exist("images/title.png"):
        show title
        with dissolve
    pause 1.0
    return

label main_menu:
    # Ren'Py uses screens for the main menu; this label intentionally returns to the launcher
    return

label start:
    call screen age_gate
    if not adult_verified:
        narrator "You chose not to verify your age. The game cannot continue."
        return

    # Play menu music once at start of the story
    if play_music and renpy.music.get_playing() == None:
        play music "audio/menu_theme.ogg" fadein 1.0

    scene bg lounge
    with fade
    narrator "The lounge is alive with low conversation. The lights make the room feel like an island."
    menu:
        "Approach Maya at the booth." :
            $ route = "maya"
            jump maya_route
        "Talk to Noah by the bar." :
            $ route = "noah"
            jump noah_route
        "Find Aria on the balcony." :
            $ route = "aria"
            jump aria_route
        "Speak to Celeste in the corner." :
            $ route = "celeste"
            jump celeste_route

# Maya route expanded with mid-game beats and CG placeholders
label maya_route:
    scene bg lounge
    show cg_maya_close at center
    with dissolve
    maya "I thought you'd show. The night is better with good company."
    menu:
        "Ask about her past." :
            $ romance_maya = clamp(romance_maya + 2)
            maya "There are chapters I keep, and chapters I share. Which would you prefer?"
            jump maya_mid
        "Invite her to walk on the balcony." :
            $ romance_maya = clamp(romance_maya + 3)
            jump maya_balcony

label maya_mid:
    maya "I like honesty. If you're going to be here, be real."
    menu:
        "Be blunt and honest." :
            $ romance_maya = clamp(romance_maya + 3)
            narrator "Her eyes soften. She respects the risk."
            jump maya_balcony
        "Keep it light and teasing." :
            $ romance_maya = clamp(romance_maya + 1)
            narrator "She laughs lightly, amused by the safer conversation."
            jump maya_balcony

label maya_balcony:
    scene bg balcony
    with fade
    maya "The city below looks different from up here. Closer somehow."
    # mature, non-graphic intimate scene placeholder
    if not adult_verified:
        narrator "This moment is reserved for verified adults."
        return

    show cg_maya_close
    narrator "You step closer. The world narrows to the two of you."
    menu:
        "Kiss her gently." :
            $ romance_maya = clamp(romance_maya + 4)
            narrator "The kiss is soft, meaningful — an honest beginning."
            jump maya_epilogue
        "Hold her and say you want to know her more." :
            $ romance_maya = clamp(romance_maya + 3)
            narrator "She leans into the warmth of your words."
            jump maya_epilogue

label maya_epilogue:
    if romance_maya >= 7:
        narrator "Weeks later, you find that night marked the start of something slow and steady."
    else:
        narrator "It becomes a memory that might grow into something else later."
    return

# Noah route with a deeper scene and optional CG
label noah_route:
    scene bg lounge
    with dissolve
    noah "The bar tells stories if you listen. Will you listen?"
    menu:
        "Share a secret to test the silence." :
            $ romance_noah = clamp(romance_noah + 2)
            jump noah_mid
        "Order a quiet drink and watch." :
            $ romance_noah = clamp(romance_noah + 1)
            jump noah_mid

label noah_mid:
    noah "I don't ask for much, but I do ask for truth."
    menu:
        "Give him the truth." :
            $ romance_noah = clamp(romance_noah + 3)
            jump noah_street
        "Tell a small white lie to keep things smooth." :
            $ romance_noah = clamp(romance_noah + 1)
            jump noah_street

label noah_street:
    scene bg street
    with fade
    noah "It's quieter out here. Conversations can breathe."
    if not adult_verified:
        narrator "This passage contains adult themes and is restricted."
        return
    narrator "The night allows you to be closer. But the scene keeps its dignity — there's warmth, consent, and no graphic detail."
    menu:
        "Take his hand and walk." :
            $ romance_noah = clamp(romance_noah + 4)
            narrator "You walk beneath the streetlights, an honest beginning forming."
            jump noah_epilogue
        "Ask for a promise of honesty." :
            $ romance_noah = clamp(romance_noah + 2)
            narrator "He nods. The promise feels heavier than words."
            jump noah_epilogue

label noah_epilogue:
    if romance_noah >= 7:
        narrator "The two of you keep meeting, building trust one night at a time."
    else:
        narrator "The moment stays as an elegy of choices not yet made."
    return

# Aria route
label aria_route:
    scene bg balcony
    with dissolve
    aria "Most people mistake flash for connection. I'm not most people."
    menu:
        "Tell her you want depth." :
            $ romance_aria = clamp(romance_aria + 3)
            jump aria_mid
        "Joke and keep things light." :
            $ romance_aria = clamp(romance_aria + 1)
            jump aria_mid

label aria_mid:
    aria "Depth isn't easy, but it's worth the risk."
    if not adult_verified:
        narrator "Adult material is restricted."
        return
    narrator "You talk for hours. The night becomes a quiet corridor where two people share truths without spectacle."
    menu:
        "Promise to see her again." :
            $ romance_aria = clamp(romance_aria + 4)
            jump aria_epilogue
        "Ask for something slower." :
            $ romance_aria = clamp(romance_aria + 2)
            jump aria_epilogue

label aria_epilogue:
    if romance_aria >= 6:
        narrator "The relationship grows with patience and careful attention."
    else:
        narrator "It becomes a treasured memory, small but real."
    return

# Celeste route
label celeste_route:
    scene bg lounge
    with dissolve
    celeste "I like when people show up with intention. It changes everything."
    menu:
        "Ask her what she wants." :
            $ romance_celeste = clamp(romance_celeste + 2)
            jump celeste_mid
        "Tell her you're curious about her." :
            $ romance_celeste = clamp(romance_celeste + 1)
            jump celeste_mid

label celeste_mid:
    celeste "I want truth. Not always easy, but always cleaner."
    if not adult_verified:
        narrator "Adult scenes are locked until verification."
        return
    narrator "The two of you step into a small, dim room. The scene remains sensual and adult — focused on consent and connection rather than needless detail."
    menu:
        "Be honest about what you want." :
            $ romance_celeste = clamp(romance_celeste + 4)
            jump celeste_epilogue
        "Ask for a slow beginning." :
            $ romance_celeste = clamp(romance_celeste + 2)
            jump celeste_epilogue

label celeste_epilogue:
    if romance_celeste >= 7:
        narrator "Slow beginnings become stories you tell yourself later with a fondness that never fades."
    else:
        narrator "The night keeps its secret; you keep your curiosity."
    return

# Optional: quick jump menu for testing
label developer_menu:
    menu:
        "Start Maya route" : jump maya_route
        "Start Noah route" : jump noah_route
        "Start Aria route" : jump aria_route
        "Start Celeste route" : jump celeste_route
        "Quit" : return
