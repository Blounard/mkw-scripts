from dolphin import event, gui, utils
import configparser
import math
import os

from Modules.mkw_classes.common import SurfaceProperties, eulerAngle
from Modules.mkw_utils import History 

import Modules.settings_utils as setting
import Modules.mkw_utils as mkw_utils
from Modules.mkw_classes import RaceManager, RaceManagerPlayer, RaceState, TimerManager
from Modules.mkw_classes import RaceConfig, RaceConfigScenario, RaceConfigSettings
from Modules.mkw_classes import KartObject, KartMove, KartSettings, KartBody
from Modules.mkw_classes import VehicleDynamics, VehiclePhysics, KartBoost, KartJump
from Modules.mkw_classes import KartState, KartCollide, KartInput, RaceInputState


def make_line_text_speed(left_text_prefix, left_text_suffix, size, speed):
    """Function to generate a line of text
        It has "left_text" as a str on the left,
        enough spaces to make the text on the left exactly size length
        then it has ":" followed by the speed, finished with a \n.
        Param: str left_text
                int size
                float speed
        Return str text"""
    return left_text_prefix+" "*(size - len(left_text_prefix+left_text_suffix))+left_text_suffix + f"{speed:.{c.digits}f}\n"
        
def make_text_speed(speed, speedname, player, boolspd, boolspdoriented, boolspdxyz):
    """Function to generate the text for a certain speed
        Parameters : vec3 speed : the speed to generate the text for.
                    str speedname : the string to write before each line
                    int player : ID of the player (used for oriented speed, 0 if player)
                    bool boolspd : True if we draw the (X, Y, Z) speed
                    bool boolspdoriented : True if we draw (Forward, Sideway, Y)
                    bool boolspdxyz : True if we draw (XZ, XYZ)
        Return str text ready to be displayed"""
    text = ""
    facing_yaw = mkw_utils.get_facing_angle(player).yaw
    offset_size = 13
    if boolspd and boolspdoriented :
        text += make_line_text_speed(speedname,"X: ", offset_size, speed.x)
        text += make_line_text_speed(speedname,"Y: ", offset_size, speed.y)
        text += make_line_text_speed(speedname,"Z: ", offset_size, speed.z)
        text += make_line_text_speed(speedname,"Forward: ", offset_size, speed.forward(facing_yaw))
        text += make_line_text_speed(speedname,"Sideway: ", offset_size, speed.sideway(facing_yaw))
    elif boolspd :
        text += make_line_text_speed(speedname,"X: ", offset_size, speed.x)
        text += make_line_text_speed(speedname,"Y: ", offset_size, speed.y)
        text += make_line_text_speed(speedname,"Z: ", offset_size, speed.z)
    elif boolspdoriented :
        text += make_line_text_speed(speedname,"Forward: ", offset_size, speed.forward(facing_yaw))
        text += make_line_text_speed(speedname,"Sideway: ", offset_size, speed.sideway(facing_yaw))
        text += make_line_text_speed(speedname,"Y: ", offset_size, speed.y)
    if boolspdxyz :
        text += make_line_text_speed(speedname,"XZ: ", offset_size, speed.length_xz())
        text += make_line_text_speed(speedname,"XYZ: ", offset_size, speed.length())
    return text


def make_text_timediff(timediff, prefix_text, prefix_size, timesize):
    timediffms = timediff/59.94
    ms = f"{timediffms:.{c.digits}f}"
    frame = f"{timediff:.{c.digits}f}"
    ms += " "*(timesize - len(ms))
    ms = ms[:timesize]
    frame = frame[:timesize]+"f"
    return prefix_text+":"+" "*(prefix_size - len(prefix_text))+ms+"| "+frame+"\n"


def make_text_rotation(rot, rotspd, prefix_text, prefix_size, rotsize):
    rot_text = f"{rot:.{c.digits}f}"
    rotspd_text = f"{rotspd:.{c.digits}f}"
    rot_text += " "*(rotsize - len(rot_text))
    rot_text = rot_text[:rotsize]
    rotspd_text = rotspd_text[:rotsize]
    return prefix_text+":"+" "*(prefix_size - len(prefix_text))+rot_text+"| "+rotspd_text+"\n"
# draw information to the screen

def create_infodisplay():
    text = ""
    
    race_mgr_player = RaceManagerPlayer()
    race_scenario = RaceConfigScenario(addr=RaceConfig.race_scenario())
    race_settings = RaceConfigSettings(race_scenario.settings())
    kart_object = KartObject()
    kart_state = KartState(addr=kart_object.kart_state())
    kart_move = KartMove(addr=kart_object.kart_move())
    kart_body = KartBody(addr=kart_object.kart_body())
    vehicle_dynamics = VehicleDynamics(addr=kart_body.vehicle_dynamics())
    vehicle_physics = VehiclePhysics(addr=vehicle_dynamics.vehicle_physics())
    
    if c.debug :
        value = mkw_utils.delta_position(0) - VehiclePhysics.speed(0)
        text += f"Debug : {value.length()}\n"
    
    if c.frame_count:
        text += f"Frame: {mkw_utils.frame_of_input()}\n\n"
    
    if c.lap_splits:
        # The actual max lap address does not update when crossing the finish line
        # for the final time to finish the race. However, for whatever reason,
        # race completion does. We use the "max" version to prevent lap times
        # from disappearing when crossing the line backwards.
        player_max_lap = math.floor(race_mgr_player.race_completion_max())
        lap_count = race_settings.lap_count()

        if player_max_lap >= 2 and lap_count > 1:
            for lap in range(1, player_max_lap):
                text += "Lap {}: {}\n".format(lap, mkw_utils.update_exact_finish(lap, 0))

        if player_max_lap > lap_count:
            text += "Final: {}\n".format(mkw_utils.get_unrounded_time(lap_count, 0))
        text += "\n"
    
    if c.speed:
        speed = mkw_utils.delta_position(playerIdx=0)
        engine_speed = kart_move.speed()
        cap = kart_move.soft_speed_limit()
        text += make_text_speed(speed, "", 0, False, c.speed_oriented, c.speed)
        text += f"     Engine: {round(engine_speed, c.digits)} / {round(cap, c.digits)}\n"
        text += "\n"
    
    if (c.iv or c.iv_xyz or c.iv_oriented):
        iv = vehicle_physics.internal_velocity()
        text += make_text_speed(iv, "IV ", 0, c.iv, c.iv_oriented, c.iv_xyz)
        text += "\n"
    
    if (c.ev or c.ev_xyz or c.ev_oriented):
        ev = vehicle_physics.external_velocity()
        text += make_text_speed(ev, "EV ", 0, c.ev, c.ev_oriented, c.ev_xyz)
        text += "\n"
    
    if (c.mrv or c.mrv_xyz or c.mrv_oriented):
        mrv = vehicle_physics.moving_road_velocity()
        text += make_text_speed(mrv, "MRV ", 0, c.mrv, c.mrv_oriented, c.mrv_xyz)
        text += "\n"

    if (c.mwv or c.mwv_xyz or c.mwv_oriented):
        mwv = vehicle_physics.moving_water_velocity()
        text += make_text_speed(mwv, "MWV ", 0, c.mwv, c.mwv_oriented, c.mwv_xyz)
        text += "\n"
       
    if c.charges or c.misc:
        kart_settings = KartSettings(addr=kart_object.kart_settings())

    if c.charges:
        kart_boost = KartBoost(addr=kart_move.kart_boost())
        
        mt = kart_move.mt_charge()
        smt = kart_move.smt_charge()
        ssmt = kart_move.ssmt_charge()
        mt_boost = kart_move.mt_boost_timer()
        trick_boost = kart_boost.trick_and_zipper_timer()
        shroom_boost = kart_move.mushroom_timer()
        if kart_settings.is_bike():
            text += f"MT Charge: {mt} | SSMT Charge: {ssmt}\n"
        else:
            text += f"MT Charge: {mt} ({smt}) | SSMT Charge: {ssmt}\n"
            
        text += f"MT: {mt_boost} | Trick: {trick_boost} | Mushroom: {shroom_boost}\n\n"
    
    if c.cps:
        lap_comp = race_mgr_player.lap_completion()
        race_comp = race_mgr_player.race_completion()
        cp = race_mgr_player.checkpoint_id()
        kcp = race_mgr_player.max_kcp()
        rp = race_mgr_player.respawn()
        text += f" Lap%: {round(lap_comp,c.digits)}\n"
        text += f"Race%: {round(race_comp,c.digits)}\n"
        text += f"CP: {cp} | KCP: {kcp} | RP: {rp}\n\n"

    if c.air:
        airtime = kart_move.airtime()
        text += f"Airtime: {airtime}\n\n"

    if c.misc or c.surfaces:
        kart_collide = KartCollide(addr=kart_object.kart_collide())

    if c.misc:
        kart_jump = KartJump(addr=kart_move.kart_jump())
        trick_cd = kart_jump.cooldown()
        hwg_timer = kart_state.hwg_timer()
        oob_timer = kart_collide.solid_oob_timer()
        respawn_timer = kart_collide.time_before_respawn()
        offroad_inv = kart_move.offroad_invincibility()
        if kart_move.is_bike:
            text += f"Wheelie Length: {kart_move.wheelie_frames()}\n"
            text += f"Wheelie CD: {kart_move.wheelie_cooldown()} | "
        text += f"Trick CD: {trick_cd}\n"
        text += f"HWG: {hwg_timer} | OOB: {oob_timer}\n"
        text += f"Respawn: {respawn_timer}\n"
        text += f"Offroad: {offroad_inv}\n\n"

    if c.surfaces:
        surface_properties = kart_collide.surface_properties()
        is_offroad = (surface_properties.value & SurfaceProperties.OFFROAD) > 0
        is_trickable = (surface_properties.value & SurfaceProperties.TRICKABLE) > 0
        kcl_speed_mod = kart_move.kcl_speed_factor()
        text += f"  Offroad: {is_offroad}\n"
        text += f"Trickable: {is_trickable}\n"
        text += f"KCL Speed Modifier: {round(kcl_speed_mod * 100, c.digits)}%\n\n"

    if c.position:
        pos = vehicle_physics.position()
        text += f"X Pos: {pos.x}\n"
        text += f"Y Pos: {pos.y}\n"
        text += f"Z Pos: {pos.z}\n\n"
    
    if c.rotation :
        fac = mkw_utils.get_facing_angle(0)
        mov = mkw_utils.get_moving_angle(0)
        if len(Angle_History) > 1:            
            prevfac = Angle_History[1]['facing']
            prevmov = Angle_History[1]['moving']
        else:
            prevfac = mkw_utils.get_facing_angle(0)
            prevmov = mkw_utils.get_moving_angle(0)
        facdiff = fac - prevfac
        movdiff = mov - prevmov
        prefix_size = 10
        rotsize = c.digits+4
        text += " "*(prefix_size+1)+"Rotation"+" "*(rotsize - 8)+"| Speed\n"
        text += make_text_rotation(fac.pitch, facdiff.pitch, "Pitch", prefix_size, rotsize)
        text += make_text_rotation(fac.yaw, facdiff.yaw, "Yaw", prefix_size, rotsize)
        text += make_text_rotation(mov.yaw, movdiff.yaw, "Moving Y", prefix_size, rotsize)
        text += make_text_rotation(fac.roll, facdiff.roll, "Roll", prefix_size, rotsize)
        text += "\n"
    
    if c.td and not mkw_utils.is_single_player():
        size = 10
        timesize = c.digits+4
        p1, p2 = mkw_utils.get_timediff_settings(c.td_set)
        s = 1 if 1-p1 else -1
        text += "TimeDiff:"+" "*(timesize+size-16)+"Seconds | Frames\n"
        if c.td_absolute:
            absolute = mkw_utils.get_time_difference_absolute(p1,p2)
            text += make_text_timediff(absolute, "Absolute", size, timesize)
        if c.td_relative:
            relative = s*mkw_utils.get_time_difference_relative(p1,p2)
            text += make_text_timediff(relative, "Relative", size, timesize)
        if c.td_projected:
            projected = s*mkw_utils.get_time_difference_projected(p1,p2)
            text += make_text_timediff(projected, "Projected", size, timesize)
        if c.td_crosspath:
            crosspath = s*mkw_utils.get_time_difference_crosspath(p1,p2)
            text += make_text_timediff(crosspath, "CrossPath", size, timesize)
        if c.td_tofinish:
            tofinish = s*mkw_utils.get_time_difference_tofinish(p1,p2)
            text += make_text_timediff(tofinish, "ToFinish", size, timesize)
        if c.td_racecomp:
            racecomp = mkw_utils.get_time_difference_racecompletion(RaceComp_History)
            text += make_text_timediff(racecomp, "RaceComp", size, timesize)  
        text += "\n"
    
    # TODO: figure out why classes.RaceInfoPlayer.stick_x() and 
    #       classes.RaceInfoPlayer.stick_y() do not update
    #       (using these as placeholders until further notice)
    if c.stick:
        kart_input = KartInput(addr=race_mgr_player.kart_input())
        current_input_state = RaceInputState(addr=kart_input.current_input_state())

        stick_x = current_input_state.raw_stick_x() - 7
        stick_y = current_input_state.raw_stick_y() - 7
        text += f"X: {stick_x} | Y: {stick_y}\n\n"
    
    return text


@event.on_savestateload
def on_state_load(fromSlot: bool, slot: int):
    global c
    race_mgr = RaceManager()
    c = setting.get_infodisplay_config()
    
    '''if race_mgr.state().value >= RaceState.COUNTDOWN.value:
        text = create_infodisplay()
        gui.draw_text((10, 10), c.color, text)'''
    

 # Something in that commented code causes dolphin to crash when loading a savestate from boot to in race
 # It's the create_infodisplay, but I can't figure out a line that makes the crash.
 # I think it's when there is too much instructions

    

def main():
    global c
    c = setting.get_infodisplay_config()
    
    #Those 2 variables are used to store some parameters from previous frames
    global Frame_of_input
    Frame_of_input = 0

    def prc():
        return RaceManagerPlayer(0).race_completion()
    def grc():
        return RaceManagerPlayer(1).race_completion()
    def fa():
        return mkw_utils.get_facing_angle(0)
    def ma():
        return mkw_utils.get_moving_angle(0)
    
    global RaceComp_History
    RaceComp_History = History({'prc':prc, 'grc':grc}, c.history_size)

    global Angle_History
    Angle_History = History({'facing' : fa, 'moving' : ma}, 2)


if __name__ == '__main__':
    main()


@event.on_frameadvance
def on_frame_advance():
    global Frame_of_input
    global Angle_History
    global RaceComp_History
    global c

    if not (Frame_of_input == mkw_utils.frame_of_input() or Frame_of_input == mkw_utils.frame_of_input()-1):
        c = setting.get_infodisplay_config()
    
    race_mgr = RaceManager()
    newframe = Frame_of_input != mkw_utils.frame_of_input()
    draw = race_mgr.state().value >= RaceState.COUNTDOWN.value
    if newframe and draw:
        Frame_of_input = mkw_utils.frame_of_input()
        try:
            Angle_History.update()
            RaceComp_History.update()
        except AssertionError:
            pass

    if draw:
        gui.draw_text((10, 10), c.color, create_infodisplay())

