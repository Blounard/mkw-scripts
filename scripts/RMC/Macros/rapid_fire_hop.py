"""
Usage: Hold B to rapid fire hop.
"""
from dolphin import controller, event # type: ignore
import Modules.mkw_classes as mkw
from Modules.macro_utils import MKWiiGCController


@event.on_frameadvance
def on_frame_advance():
    if mkw.RaceManager().state() != mkw.RaceState.RACE:
        return

    ctrl = MKWiiGCController(controller)
    user_inputs = ctrl.user_inputs()

    if user_inputs["B"]:
        hop_pressed = mkw.KartState.bitfield() & 0x80 > 0
        ctrl.set_inputs({
            "B": not hop_pressed,
        })
