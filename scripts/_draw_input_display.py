from dolphin import gui, event
from Modules import input_display as display
from Modules import mkw_classes as classes

stick_dict = {-7: 0, -6: 60, -5: 70, -4: 80, -3: 90, -2: 100, -1: 110,
              0: 128, 1: 155, 2: 165, 3: 175, 4: 185, 5: 195, 6: 200, 7: 255}


@event.on_frameadvance
def on_frame_advance():
    if classes.RaceInfo.stage() >= 1:

        # TODO: use masks instead of the values for buttons

        ablr = classes.RaceInfoPlayer.ablr_buttons()
        dpad = classes.RaceInfoPlayer.dpad()
        xstick = classes.RaceInfoPlayer.stick_x() - 7
        ystick = classes.RaceInfoPlayer.stick_y() - 7

        # A Button
        display.create_unpressed_button([330, gui.get_display_size()[1] - 95],
                                        35, 0xFFFFFFFF)
        if ablr == 1 or ablr == 3 or ablr == 5 or ablr == 11 or ablr == 15:
            display.fill_pressed_button([330, gui.get_display_size()[1] - 95],
                                        35, 0xFFFFFFFF)

        # L Button
        display.create_unpressed_bumper(
            [30, gui.get_display_size()[1] - 200], 100, 50, 0xFFFFFFFF)
        if ablr == 4 or ablr == 5 or ablr == 6 or ablr == 7 or ablr == 15:
            display.create_unpressed_bumper(
                [30, gui.get_display_size()[1] - 200], 100, 50, 0xFFFFFFFF)

        # R Button
        display.create_unpressed_bumper(
            [280, gui.get_display_size()[1] - 200], 100, 50, 0xFFFFFFFF)
        if ablr == 2 or ablr == 3 or ablr == 6 or ablr == 11 or ablr == 15:
            display.fill_pressed_bumper(
                [280, gui.get_display_size()[1] - 200], 100, 50, 0xFFFFFFFF)

        # D-Pad
        # TODO: fix the module so that -35 does not have to be used here
        display.create_dpad(
            [30, gui.get_display_size()[1] - 32.5], 30, -35, 0xFFFFFFFF)

        if dpad == 1:
            display.fill_dpad([30, gui.get_display_size()[1] - 32.5],
                              30, -35, 0xFFFFFFFF, ["Up"])
        elif dpad == 2:
            display.fill_dpad([30, gui.get_display_size()[1] - 32.5],
                              30, -35, 0xFFFFFFFF, ["Down"])
        elif dpad == 3:
            display.fill_dpad([30, gui.get_display_size()[1] - 32.5],
                              30, -35, 0xFFFFFFFF, ["Left"])
        elif dpad == 4:
            display.fill_dpad([30, gui.get_display_size()[1] - 32.5],
                              30, -35, 0xFFFFFFFF, ["Right"])

        # Control Stick
        display.create_control_stick([210, gui.get_display_size()[1] - 100], 50, 30, 50,
            stick_dict.get(xstick, 0), stick_dict.get(ystick, 0), 0xFFFFFFFF)