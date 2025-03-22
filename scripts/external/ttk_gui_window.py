import time
import tkinter as tk
from tkinter import ttk  # lol
import os
import struct
import external_utils as ex

# This constant determines how the buttons are arranged.
# Ex: BUTTON_LAYOUT[section_index][row_index][column_index]
BUTTON_LAYOUT = [
    [
        ["Load from Player", "Load from Ghost"],
        ["Save to RKG", "Load from RKG"],
    ],
    [
        ["Load from Player", "Load from Ghost"],
        ["Save to RKG", "Load from RKG"],
    ],
]

def main():
    try:
        shm_activate = ex.SharedMemoryBlock.connect(name="ttk_gui_activate")
        shm_buttons = ex.SharedMemoryBlock.connect(name="ttk_gui_buttons")
        shm_player_csv = ex.SharedMemoryReader(name="ttk_gui_player_csv")
        shm_ghost_csv = ex.SharedMemoryReader(name="ttk_gui_ghost_csv")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Shared memory buffer '{e.filename}' not found. Make sure the `TTK_GUI` script is enabled.")

    # Button presses get stored in a queue and then written to shared memory one at a time
    button_command_queue = []

    window = tk.Tk()
    window.title("TAS Toolkit GUI")
    window.geometry("500x250")
    
    root_frame = ttk.Frame(window)
    root_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    activate_state = [tk.BooleanVar(), tk.BooleanVar()]
    def on_checkbox_change():
        shm_activate.write(struct.pack('>??', *[var.get() for var in activate_state]))
    
    player_csv = tk.StringVar(value=shm_player_csv.read_text())
    ghost_csv = tk.StringVar(value=shm_ghost_csv.read_text())

    for section_index, section_title in enumerate(["Player Inputs", "Ghost Inputs"]):
        section_frame = ttk.LabelFrame(root_frame, text=section_title)
        section_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    
        ttk.Checkbutton(section_frame, text="Activate", variable=activate_state[section_index], command=on_checkbox_change) \
            .pack(pady=5)
        
        ttk.Label(section_frame, text=f"File: {os.path.basename([player_csv, ghost_csv][section_index].get())}") \
            .pack(pady=5)

        for row_index, row in enumerate(BUTTON_LAYOUT[section_index]):
            btn_row_frame = ttk.Frame(section_frame)
            btn_row_frame.pack(pady=5)

            for col_index, btn_text in enumerate(row):
                button_data = struct.pack('>?BBB', True, section_index, row_index, col_index)
                def on_click(data=button_data):
                    button_command_queue.append(data)
                ttk.Button(btn_row_frame, text=btn_text, command=on_click, width=15) \
                    .pack(side=tk.LEFT, padx=5)

    while True:
        # Wait to send next button command until shared memory is cleared
        if button_command_queue and shm_buttons.read()[0] == 0:
            shm_buttons.write(button_command_queue.pop(0))

        new_text = shm_player_csv.read_text()
        if new_text and new_text != player_csv.get():
            player_csv.set(new_text)
        
        new_text = shm_ghost_csv.read_text()
        if new_text and new_text != ghost_csv.get():
            ghost_csv.set(new_text)

        window.update_idletasks()
        window.update()
        time.sleep(0.01)  # Prevents CPU hogging


if __name__ == '__main__':
    main()