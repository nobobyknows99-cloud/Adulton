# Screens for Adulton: main menu with music, save/load integration

screen main_menu():
    tag menu
    use game_menu("main")

screen game_menu(menu_type):
    # Background
    if renpy.exist("images/title.png"):
        add "images/title.png"
    else:
        add Solid("#101018")

    # Play menu music (loop)
    if not renpy.music.get_playing():
        play music "audio/menu_theme.ogg" loop

    vbox:
        xalign 0.5
        yalign 0.6
        spacing 18

        text "Adulton" size 56 color "#ffffff" bold True xalign 0.5

        textbutton "Start" action Start() xminimum 300 yminimum 60
        textbutton "Load" action ShowMenu("load") xminimum 300 yminimum 60
        textbutton "Preferences" action ShowMenu("preferences") xminimum 300 yminimum 60
        textbutton "Quit" action Quit(confirm=False) xminimum 300 yminimum 60

screen save_slot(slot):
    # This wraps the default save slot so you can add previews or CG thumbnails later.
    default thumb = None
    if renpy.exists("images/cg_preview_" + str(slot) + ".png"):
        add "images/cg_preview_" + str(slot) + ".png" xalign 0.02 yalign 0.02
    use file_slot(slot)
