import moviepy
import numpy as np
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys
import os
import time
import subprocess
import math

import configparser


def create_config(filename):
    config = configparser.ConfigParser(allow_no_value=True)
    config.optionxform = str
    config.add_section('README')
    config.set('README', 'Visit : https://docs.google.com/document/d/e/2PACX-1vTXoEveB_1MZ3WizOpEWvZ-oyJMgg-3pRLGiNu-5vo853BMcrr8RY69REcTsheurI9qS2kfqrx1BZkT/pub\n\n' )
    
    config.add_section('Encoding options')
    config.set('Encoding options', '\n#Valid options are "normal", "discord", "youtube"')
    '''
    config.set('Encoding options', '#"normal" is no particular encoding settings, for people who want to do more video editing afterward')
    config.set('Encoding options', '#"discord" is for size based encoding, allowing for a specific filesize output')
    config.set('Encoding options', '#"youtube" is for directly uploading on YT. uses encode settings from https://gist.github.com/wuziq/b86f8551902fa1d477980a8125970877')
    '''
    config.set('Encoding options', '#You can also set an integer, to only render the .png of the corresponding frame (useful for trying different display options quickly)')
    config.set('Encoding options', 'encode_style', 'discord')#
    config.set('Encoding options', '\n#Video output size in mb. only used with discord encoding style')
    config.set('Encoding options', 'output_file_size', '9.5')#in MB
    config.set('Encoding options', '\n#range from 0 to 51. Only used with normal encoding style')
    config.set('Encoding options', 'crf_value', '0')#
    config.set('Encoding options', '\n#Choice "ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"')
    config.set('Encoding options', '#it affect the size of the output file, and the performances. it also affect quality when using discord encoding style')
    config.set('Encoding options', 'preset', 'slow')#
    config.set('Encoding options', '\n#Threads amount to use for ffmpeg')
    config.set('Encoding options', 'threads', '4')#
    config.set('Encoding options', '\n#Height of the output video in pixel')
    config.set('Encoding options', 'resize_resolution', '1080')#
    config.set('Encoding options', '\n#Choice "stretch", "crop", "fill", "none"')
    config.set('Encoding options', 'resize_style', 'none') #stretch, crop, fill, none
    config.set('Encoding options', '\n#Choice "nearest", "box", "bilinear", "hamming", "bicubic", "lanczos"')
    config.set('Encoding options', '#visit https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-filters')
    config.set('Encoding options', 'scaling_option', 'lanczos') #https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-filters
    config.set('Encoding options', '\n#filename for the output file. .mp4 extension required')
    config.set('Encoding options', 'output_filename', 'output.mp4')#
    config.set('Encoding options', '\n#time in seconds for the video fade in')
    config.set('Encoding options', 'video_fade_in', '0')#
    config.set('Encoding options', '\n#time in seconds for the video fade out')
    config.set('Encoding options', 'video_fade_out', '0')#
    config.set('Encoding options', '\n#Choice "blur", "contour", "detail", "edge_enhance", "edge_enhance_more", "emboss", "find_edges", "sharpen", "smooth", "smooth_more"')
    config.set('Encoding options', '#You can use several effects by separating them with a ",". DO NOT USE SPACES')
    config.set('Encoding options', 'special_effects', 'none') #https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html#module-PIL.ImageFilter
    
    config.set('Encoding options', '\n\n##############################################################################\n')

    config.add_section('Audio options')
    config.set('Audio options', '\n#Choice "dsp", "dtk", "none"')
    config.set('Audio options', 'audiodump_target', 'none') #dsp, dtk, none
    config.set('Audio options', '\n#multiplicator on the in game volume')
    config.set('Audio options', 'audiodump_volume', '1.0')#
    config.set('Audio options', '\n#Must be a file in the same folder as this config file')
    config.set('Audio options', 'bgm_filename', '')#
    config.set('Audio options', '\n#multiplicator on the bgm volume')
    config.set('Audio options', 'bgm_volume', '1')#
    config.set('Audio options', '\n#Time in second the BGM should start at in the output video. You can use negative values to skip the beginning of the BGM')
    config.set('Audio options', 'bgm_offset', '0')#
    config.set('Audio options', '\n#time in second for the audio fade in')
    config.set('Audio options', 'fade_in', '0')#
    config.set('Audio options', '\n#time in second for the audio fade out')
    config.set('Audio options', 'fade_out', '0')#

    config.set('Audio options', '\n\n##############################################################################\n')
    
    config.add_section('Infodisplay')
    config.set('Infodisplay', '\n#draw the infodisplay')
    config.set('Infodisplay', 'show_infodisplay', 'True')#
    config.set('Infodisplay', '\n#Font filename. You must put the font in the Fonts folder.')
    config.set('Infodisplay', 'font', 'MKW_Font')#
    config.set('Infodisplay', '\n#font size in pixel on the final output resolution for fonts other than the mkw font.')
    config.set('Infodisplay', 'font_size', '48')#
    config.set('Infodisplay', '\n#Scaling factor for MKW Font if used')
    config.set('Infodisplay', 'mkw_font_scaling', '3')#
    config.set('Infodisplay', '\n#vertical spacing in pixel between lines')
    config.set('Infodisplay', 'spacing', '4')#
    config.set('Infodisplay', '\n#frame OF INPUT this section will appear on')
    config.set('Infodisplay', 'start_frame', '0')#
    config.set('Infodisplay', '\n#frame OF INPUT this section will disappear on. Leave empty for race end')
    config.set('Infodisplay', 'end_frame', '' )#
    config.set('Infodisplay', '\n#put a fade in and fade out animation to the infodisplay')
    config.set('Infodisplay', 'fade_animation', 'True')#
    config.set('Infodisplay', '\n#duration of the fade in animation in the infodisplay')
    config.set('Infodisplay', 'fade_in_duration', '20')#
    config.set('Infodisplay', '\n#duration of the fade out animation in the infodisplay')
    config.set('Infodisplay', 'fade_out_duration', '120')#
    config.set('Infodisplay', '\n#put a fly in and fly out animation to the infodisplay')
    config.set('Infodisplay', 'fly_animation', 'False')#
    config.set('Infodisplay', '\n#Choose to have the Info Display fly in from the top or bottom. (when fly_animation is enabled)')
    config.set('Infodisplay', 'fly_in_direction', 'bottom')#
    config.set('Infodisplay', '\n#Anchor for infodisplay text. 0,0 is top left, 1,1 is bottom right, 0.5,0.5 is middle of the screen')
    config.set('Infodisplay', 'anchor', '0.2,0.1')#
    config.set('Infodisplay', '\n#Choice "left", "middle", "right"')
    config.set('Infodisplay', 'anchor_style', 'middle')#
    config.set('Infodisplay', '\n# True for having the value, then the text, False for having the text, then the value')
    config.set('Infodisplay', 'invert_text', 'True')#
    config.set('Infodisplay', '\n#size of the outline of the font in pixel')
    config.set('Infodisplay', 'outline_width', '3')#
    config.set('Infodisplay', '\n#color of the outline of the font')
    config.set('Infodisplay', 'outline_color', '000000FF')#
    
    config.set('Infodisplay', '\n#reimplements pretty speedometer using fade/fly in animations. set it to "xyz", "xz","iv"; or "off" to disable it.')
    config.set('Infodisplay', 'pretty_speedometer_type', 'off')#Might be deleted later, since we can have several infodisplay, which gives more options
    config.set('Infodisplay', 'pretty_speedometer_color', 'F2E622FF')#

    config.set('Infodisplay', '\n#parameters for the XYZ speed (delta position)')
    config.set('Infodisplay', 'show_speed_xyz', 'True')
    config.set('Infodisplay', 'text_speed_xyz', '. Speed')
    config.set('Infodisplay', 'color_speed_xyz', 'FF0000FF')

    config.set('Infodisplay', '\n#parameters for the XZ speed (delta position)')   
    config.set('Infodisplay', 'show_speed_xz', 'False')
    config.set('Infodisplay', 'text_speed_xz', '. Speed XZ')
    config.set('Infodisplay', 'color_speed_xz', 'FF0000FF')

    config.set('Infodisplay', '\n#parameters for the Y speed (delta position)')
    config.set('Infodisplay', 'show_speed_y', 'False')
    config.set('Infodisplay', 'text_speed_y', '. Speed Y')
    config.set('Infodisplay', 'color_speed_y', 'FF0000FF')

    config.set('Infodisplay', '\n#parameters for the XYZ internal velocity')
    config.set('Infodisplay', 'show_iv_xyz', 'True')
    config.set('Infodisplay', 'text_iv_xyz', '. IV')
    config.set('Infodisplay', 'color_iv_xyz', '00FF00FF')

    config.set('Infodisplay', '\n#parameters for the XZ internal velocity')
    config.set('Infodisplay', 'show_iv_xz', 'False')
    config.set('Infodisplay', 'text_iv_xz', '. IV XZ')
    config.set('Infodisplay', 'color_iv_xz', '00FF00FF')

    config.set('Infodisplay', '\n#parameters for the Y internal velocity')
    config.set('Infodisplay', 'show_iv_y', 'False')
    config.set('Infodisplay', 'text_iv_y', '. IV Y')
    config.set('Infodisplay', 'color_iv_y', '00FF00FF')

    config.set('Infodisplay', '\n#parameters for the XYZ external velocity')
    config.set('Infodisplay', 'show_ev_xyz', 'True')
    config.set('Infodisplay', 'text_ev_xyz', '. EV')
    config.set('Infodisplay', 'color_ev_xyz', '0000FFFF')

    config.set('Infodisplay', '\n#parameters for the XZ external velocity')
    config.set('Infodisplay', 'show_ev_xz', 'False')
    config.set('Infodisplay', 'text_ev_xz', '. EV XZ ')
    config.set('Infodisplay', 'color_ev_xz', '0000FFFF')

    config.set('Infodisplay', '\n#parameters for the Y external velocity')
    config.set('Infodisplay', 'show_ev_y', 'False')
    config.set('Infodisplay', 'text_ev_y', '. EV Y')
    config.set('Infodisplay', 'color_ev_y', '0000FFFF')

    config.set('Infodisplay', '\n#display custom text using the mkw font. the anchors x axis will be the center of the text, the y axis will be the top')
    config.set('Infodisplay', 'enable_custom_text', 'False')

    config.set('Infodisplay', '\n#to add multiple texts, copy these lines below and increment the number at the end of the parameters')
    config.set('Infodisplay', 'custom_text_anchor_1', '0.2.01')
    config.set('Infodisplay', 'custom_text_scaling_1', '2.5')
    config.set('Infodisplay', 'custom_text_1', 'your text here')
    config.set('Infodisplay', 'custom_text_color_1', 'F2E622FF')
    
    config.set('Infodisplay', '\n\n##############################################################################\n')

    config.add_section('Speed display')
    config.set('Speed display', '\n#draw the speed display')
    config.set('Speed display', 'show_speed_display', 'True')
    config.set('Speed display', '\n#frame OF INPUT this section will appear on')
    config.set('Speed display', 'start_frame', '0')#
    config.set('Speed display', '\n#frame OF INPUT this section will disappear on. Leave empty for race end')
    config.set('Speed display', 'end_frame', '')#
    config.set('Speed display', '\n#put a fade in and fade out animation to the Speed display')
    config.set('Speed display', 'fade_animation', 'True')#
    config.set('Speed display', '\n#duration of the fade in animation in the Speed display')
    config.set('Speed display', 'fade_in_duration', '20')#
    config.set('Speed display', '\n#duration of the fade out animation in the Speed display')
    config.set('Speed display', 'fade_out_duration', '120')#
    config.set('Speed display', '\n#put a fly in and fly out animation to the speed display')
    config.set('Speed display', 'fly_animation', 'False')#
    config.set('Speed display', '\n#Choose to have the Speed Display fly in from the top or bottom. (when fly_animation is enabled)')
    config.set('Speed display', 'fly_in_direction', 'bottom')#
    config.set('Speed display', '\n#Top left anchor for speed display text. 0,0 is top left, 1,1 is bottom right, 0.5,0.5 is middle of the screen')
    config.set('Speed display', 'top_left', '0.7, 0.5')#
    config.set('Speed display', '\n#Activating this will make the circle rotate with your facing yaw, so it always face up')
    config.set('Speed display', 'rotate_with_yaw', 'True')#
    config.set('Speed display', '\n#Radius of the circle in pixel on the final output resolution')
    config.set('Speed display', 'circle_radius', '200')#
    config.set('Speed display', '\n#Color of the interior of the circle')
    config.set('Speed display', 'circle_color', 'FFFFFF80')#
    config.set('Speed display', '\n#color of the border of the circle')
    config.set('Speed display', 'circle_outline_color', '000000FF')#
    config.set('Speed display', '\n#size of the border of the circle')
    config.set('Speed display', 'circle_outline_width', '4')#
    config.set('Speed display', '\n#draw the XZ axis when rotating with yaw. Draw the sideways and forward axis when not rotating with yaw')
    config.set('Speed display', 'draw_axis', 'True')#
    config.set('Speed display', '\n#color of the axis')
    config.set('Speed display', 'axis_color', '000000FF')#
    config.set('Speed display', '\n#width of the axis in pixel on the final output resolution')
    config.set('Speed display', 'axis_width', '2')#
    config.set('Speed display', '\n#Draw a pieslice corresponding to the facing yaw') 
    config.set('Speed display', 'draw_pieslice', 'False')#
    config.set('Speed display', '\n#color of that pieslice')
    config.set('Speed display', 'pieslice_color', 'FFFF00FF')
    config.set('Speed display', '\n#width of the arrows')
    config.set('Speed display', 'arrow_width', '6')#
    config.set('Speed display', '\n#size of the border of the arrows')
    config.set('Speed display', 'arrow_outline_width', '1')#
    config.set('Speed display', '\n#color of the border of the arrows')
    config.set('Speed display', 'arrow_outline_color', '000000FF')#
    config.set('Speed display', '\n#maximum speed corresponding to a full arrow. this parameter also scale the length of the arrow')
    config.set('Speed display', 'cap_speed', '125')#
    config.set('Speed display', '\n#arrow corresponding to speed (delta position)')
    config.set('Speed display', 'show_speed', 'True')
    config.set('Speed display', 'color_speed', 'FF0000FF')
    config.set('Speed display', '\n#arrow corresponding to internal velocity')
    config.set('Speed display', 'show_iv', 'True')
    config.set('Speed display', 'color_iv', '00FF00FF')
    config.set('Speed display', '\n#arrow corresponding to external velocity')
    config.set('Speed display', 'show_ev', 'True')
    config.set('Speed display', 'color_ev', '0000FFFF')

    config.set('Speed display', '\n\n##############################################################################\n')
    
    config.add_section('Input display')
    config.set('Input display', '\n#draw the input display')
    config.set('Input display', 'show_input_display', 'True')
    config.set('Input display', '\n#frame OF INPUT this section will appear on')
    config.set('Input display', 'start_frame', '0')#
    config.set('Input display', '\n#frame OF INPUT this section will disappear on. Leave empty for race end')
    config.set('Input display', 'end_frame', '')#
    config.set('Input display', '\n#put a fade in and fade out animation to the Input display')
    config.set('Input display', 'fade_animation', 'True')#
    config.set('Input display', '\n#duration of the fade in animation in the Input display')
    config.set('Input display', 'fade_in_duration', '20')#
    config.set('Input display', '\n#duration of the fade out animation in the Input display')
    config.set('Input display', 'fade_out_duration', '120')#
    config.set('Input display', '\n#put a fly in and fly out animation to the input display')
    config.set('Input display', 'fly_animation', 'False')#
    config.set('Input display', '\n#Choose to have the Input Display fly in from the top or bottom. (when fly_animation is enabled)')
    config.set('Input display', 'fly_in_direction', 'bottom')#
    config.set('Input display', '\n#Top left anchor for input display text. 0,0 is top left, 1,1 is bottom right, 0.5,0.5 is middle of the screen')
    config.set('Input display', 'top_left', '0.03,0.7')#
    config.set('Input display', '\n#width options equivalent to pyrkg and other input display tools. image quality has also been improved')
    config.set('Input display', '#all pairs of widths 3-7 and outline widths 2-4 are possible, except (7,4)')
    config.set('Input display', 'width', '3')#
    config.set('Input display', 'outline_width', '3')#
    config.set('Input display', '\n#coloring options for the input display parts. alpha channel has no effect but must use RGBA format')
    config.set('Input display', 'color_shoulder_left', 'FFFFFFFF')
    config.set('Input display', 'color_shoulder_right', 'FFFFFFFF')
    config.set('Input display', 'color_dpad', 'FFFFFFFF')
    config.set('Input display', 'color_analog', 'FFFFFFFF')
    config.set('Input display', 'color_a_button', 'FFFFFFFF')
    config.set('Input display', 'color_stick_text', 'FFFFFFFF')
    config.set('Input display', '\n#multiplier on the size of input display. Default size is 250x400 in pixel on the output resolution')
    config.set('Input display', 'scaling', '1')#
    config.set('Input display', '\n#Choice "nearest", "box", "bilinear", "hamming", "bicubic", "lanczos"')
    config.set('Input display', '#visit #https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-filters')
    config.set('Input display', 'scaling_option', 'lanczos') #https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-filters
    config.set('Input display', '\n#draw the bounding box. The file itself can be modified in the Input_display folder')
    config.set('Input display', 'draw_box', 'True')#
    config.set('Input display', '\n#Draw the +7,-7 text corresponding to the stick input')
    config.set('Input display', 'draw_stick_text', 'True')#
    config.set('Input display', '\n#size of stick text. the default size is 36')
    config.set('Input display', 'stick_text_size', '36')#
    config.set('Input display', '\n#Choice "blur", "contour", "detail", "edge_enhance", "edge_enhance_more", "emboss", "find_edges", "sharpen", "smooth", "smooth_more"')
    config.set('Input display', '#You can use several effects by separating them with a ",". DO NOT USE SPACES')
    config.set('Input display', 'special_effects', 'none')#
    config.set('Input display', '\n\n##############################################################################\n')

    config.add_section('Author display')
    config.set('Author display', '\n#draw the author display')
    config.set('Author display', 'show_author_display', 'False')
    config.set('Author display', '\n#frame OF INPUT this section will appear on')
    config.set('Author display', 'start_frame', '0')#
    config.set('Author display', '\n#frame OF INPUT this section will disappear on. Leave empty for race end')
    config.set('Author display', 'end_frame', '')#
    config.set('Author display', '\n#put a fade in and fade out animation to the Author display')
    config.set('Author display', 'fade_animation', 'True')#
    config.set('Author display', '\n#duration of the fade in animation in the Author display')
    config.set('Author display', 'fade_in_duration', '20')#
    config.set('Author display', '\n#duration of the fade out animation in the Author display')
    config.set('Author display', 'fade_out_duration', '120')#
    config.set('Author display', '\n#put a fly in and fly out animation to the author display')
    config.set('Author display', 'fly_animation', 'False')#
    config.set('Author display', '\n#Choose to have the Author Display fly in from the top or bottom. (when fly_animation is enabled)')
    config.set('Author display', 'fly_in_direction', 'top')#
    config.set('Author display', '\n#Top left anchor for author display text. 0,0 is top left, 1,1 is bottom right, 0.5,0.5 is middle of the screen')
    config.set('Author display', 'top_left', '0.1,0.4')#   
    config.set('Author display', '\n#Must be a file in the same folder as this config file. Mandatory for the author display to work')
    config.set('Author display', 'author_list_filename', 'authors.txt')#
    config.set('Author display', '\n#Font filename. You must put the font in the Font folder.')
    config.set('Author display', 'font', 'FOT-Rodin Pro EB.otf')#
    config.set('Author display', '\n#font size in pixel on the final output resolution')
    config.set('Author display', 'font_size', '48')#
    config.set('Author display', '\n#color used for the text when the author has input on this frame')
    config.set('Author display', 'active_text_color', 'FFFFFFFF')#
    config.set('Author display', '\n#color used for the text when the author does not have input on this frame')
    config.set('Author display', 'inactive_text_color', 'FFFFFF55')#
    config.set('Author display', '\n#outline width for the font used')
    config.set('Author display', 'outline_width', '3')#
    config.set('Author display', '\n#color of the outline when the author has input on this frame')
    config.set('Author display', 'active_outline_color', '000000FF')#
    config.set('Author display', '\n#color of the outline when the author has input on this frame')
    config.set('Author display', 'inactive_outline_color', '00000055')#
    config.set('Author display', '\n\n##############################################################################\n')

    config.add_section('Extra display')
    config.set('Extra display', '\n#this is a debug feature, ignore it\n')
    config.set('Extra display', '\n#draw the Extra display')
    config.set('Extra display', 'show_extra_display', 'True')#
    config.set('Extra display', '\n#Font filename. You must put the font in the Fonts folder.')
    config.set('Extra display', 'font', 'CONSOLA.TTF')#
    config.set('Extra display', '\n#font size in pixel on the final output resolution for fonts other than the mkw font.')
    config.set('Extra display', 'font_size', '48')#
    config.set('Extra display', '\n#Scaling factor for MKW Font if used')
    config.set('Extra display', 'mkw_font_scaling', '3')#
    config.set('Extra display', '\n#vertical spacing in pixel between lines')
    config.set('Extra display', 'spacing', '4')#
    config.set('Extra display', '\n#Anchor for Extra display text. 0,0 is top left, 1,1 is bottom right, 0.5,0.5 is middle of the screen')
    config.set('Extra display', 'anchor', '0.05,0.05')#
    config.set('Extra display', '\n#Choice "left", "middle", "right"')
    config.set('Extra display', 'anchor_style', 'middle')#
    config.set('Extra display', '\n#size of the outline of the font in pixel')
    config.set('Extra display', 'outline_width', '3')#
    config.set('Extra display', '\n#color of the outline of the font')
    config.set('Extra display', 'outline_color', '000000FF')#
    
    with open(filename, 'w') as f:
        config.write(f)

def get_config(config_filename):
    config = configparser.ConfigParser()
    config.read(config_filename)
    return config
