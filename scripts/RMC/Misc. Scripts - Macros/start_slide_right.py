from dolphin import event, gui, utils
from Modules import ttk_lib
from Modules.mkw_utils import frame_of_input
from Modules import mkw_translations as translate
from Modules.mkw_classes import RaceManager, RaceState, KartSettings
from Modules.framesequence import FrameSequence
import os

flame_slide_bikes = ("Flame Runner"),
mach_slide_bikes = ("Mach Bike", "Sugarscoot", "Zip Zip")
spear_slide_bikes = ("Jet Bubble", "Phantom", "Spear", "Sneakster")
wario_slide_bikes = ("Wario Bike")
wiggle_slide_bikes  = ("Bit Bike", "Bullet Bike", "Dolphin Dasher", "Magikruiser",
                     "Quacker", "Shooting Star", "Standard Bike L", "Standard Bike M",
                     "Standard Bike S")

@event.on_savestateload
def on_state_load(is_slot, slot):
    global player_inputs
    player_inputs = FrameSequence(check_vehicle(translate.vehicle_id()))
    player_inputs.read_from_file()

@event.on_frameadvance
def on_frame_advance():
    frame = frame_of_input()
    stage = RaceManager.state()
    
    player_input = player_inputs[frame]
    if (player_input and stage.value == RaceState.COUNTDOWN.value):
        ttk_lib.write_player_inputs(player_input, mirror = True)

def main() -> None:
    global player_inputs
    player_inputs = FrameSequence(check_vehicle(translate.vehicle_id()))
    
    gui.add_osd_message("Startslide: {} ".format(len(player_inputs) > 0))

    
def check_vehicle(vehicle):
    path = utils.get_script_dir()

    if vehicle in flame_slide_bikes:
        return os.path.join(path, "MKW_Inputs", "Startslides", "flame_left.csv")

    elif vehicle in spear_slide_bikes:
        return os.path.join(path, "MKW_Inputs", "Startslides", "spear_left.csv")

    elif vehicle in wiggle_slide_bikes:
        return os.path.join(path, "MKW_Inputs", "Startslides", "wiggle_left.csv")

    elif vehicle in mach_slide_bikes:
        return os.path.join(path, "MKW_Inputs", "Startslides", "mach_left.csv")

    else: #Karts fall here
        return os.path.join(path, "MKW_Inputs", "Startslides", "wario_left.csv")

if __name__ == '__main__':
    main()
