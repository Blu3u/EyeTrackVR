import PySimpleGUI as sg
from config import EyeTrackSettingsConfig
from threading import Event, Thread
from eye_processor import EyeProcessor, InformationOrigin
from enum import Enum
from queue import Queue, Empty
from camera import Camera, CameraState
import cv2
from osc import EyeId

class SettingsWidget:
    def __init__(self, widget_id: EyeId, main_config: EyeTrackSettingsConfig, osc_queue: Queue):

        self.gui_flip_x_axis_left = f"-FLIPXAXISLEFT{widget_id}-"
        self.gui_flip_x_axis_right = f"-FLIPXAXISRIGHT{widget_id}-"
        self.gui_flip_y_axis = f"-FLIPYAXIS{widget_id}-"
        self.gui_general_settings_layout = f"-GENERALSETTINGSLAYOUT{widget_id}-"
        self.gui_osc_address = f"-OSCADDRESS{widget_id}-"
        self.gui_osc_port = f"-OSCPORT{widget_id}-"
        self.gui_osc_receiver_port = f"OSCRECEIVERPORT{widget_id}-"
        self.gui_osc_recenter_address = f"OSCRECENTERADDRESS{widget_id}-"
        self.gui_osc_recalibrate_address = f"OSCRECALIBRATEADDRESS{widget_id}-"
        self.gui_BLOB = f"-BLOBFALLBACK{widget_id}-"
        self.gui_HSF = f"-HSF{widget_id}-"
        self.gui_RANSAC3D = f"-RANSAC3D{widget_id}-"
        self.gui_BLINK = f"-BLINK{widget_id}-"
        self.gui_HSRAC = f"-HSRAC{widget_id}-"
        self.gui_HSF_radius = f"-HSFRADIUS{widget_id}-"
        self.gui_blob_maxsize = f"-BLOBMAXSIZE{widget_id}-"
        self.gui_blob_minsize = f"-BLOBMINSIZE{widget_id}-"
        self.gui_speed_coefficient = f"-SPEEDCOEFFICIENT{widget_id}-"
        self.gui_min_cutoff = f"-MINCUTOFF{widget_id}-"
        self.gui_eye_falloff = f"-EYEFALLOFF{widget_id}-"
        self.gui_blink_sync = f"-BLINKSYNC{widget_id}-"

        self.gui_HSRACP = f"-HSRACP{widget_id}-"
        self.gui_RANSAC3DP = f"-RANSAC3DP{widget_id}-"
        self.gui_HSFP = f"-HSFP{widget_id}-"
        self.gui_BLOBP = f"-BLOBP{widget_id}-"


        self.gui_threshold_slider = f"-BLOBTHRESHOLD{widget_id}-"
        self.main_config = main_config
        self.config = main_config.settings
        self.osc_queue = osc_queue

        # Define the window's contents
        self.general_settings_layout = [
           
            [
                sg.Checkbox(
                    "Flip Left Eye X Axis",
                    default=self.config.gui_flip_x_axis_left,
                    key=self.gui_flip_x_axis_left,
                    background_color='#424042',
                    tooltip = "Flips the left eye's X axis.",
                ),
                sg.Checkbox(
                    "Flip Right Eye X Axis",
                    default=self.config.gui_flip_x_axis_right,
                    key=self.gui_flip_x_axis_right,
                    background_color='#424042',
                    tooltip = "Flips the right eye's X axis.",
                ),

            ],
            [sg.Checkbox(
                    "Flip Y Axis",
                    default=self.config.gui_flip_y_axis,
                    key=self.gui_flip_y_axis,
                    background_color='#424042',
                    tooltip = "Flips the eye's Y axis.",
                ),
            ],
            [sg.Checkbox(
                    "Dual Eye Falloff",
                    default=self.config.gui_eye_falloff,
                    key=self.gui_eye_falloff,
                    background_color='#424042',
                    tooltip = "If one eye stops tracking, we send tracking data from your other eye.",
                ),
            ],
            [sg.Checkbox(
                    "Sync Blinks (disables winking)",
                    default=self.config.gui_blink_sync,
                    key=self.gui_blink_sync,
                    background_color='#424042',
                    tooltip = "Only send a blink to VRC if both eyes are closed.",
                ),
            ],

            [
                sg.Text("Tracking Algorithim Settings:", background_color='#242224'),
            ],

            [sg.Checkbox(
                    "",
                    default=self.config.gui_HSRAC,
                    key=self.gui_HSRAC,
                    background_color='#424042',
                    tooltip = "Our newest algoritim, utilizing both HSF and RANSAC for best tracking quality and lighting resistance.",
                ),
                sg.Combo(['1','2','3','4'],
                default_value=self.config.gui_HSRAC,
                key=self.gui_HSRACP,
                background_color='#424042',
                text_color='white',
                button_arrow_color= "black",
                button_background_color = "#6f4ca1",
                tooltip = "Select the priority of eyetracking algorithims.",
                ),
                sg.Text("HSRAC", background_color='#424042'),
            ],
            [
                sg.Checkbox(
                    "",
                    default=self.config.gui_RANSAC3D,
                    key=self.gui_RANSAC3D,
                    background_color='#424042',
                    tooltip = "RANSAC3D provides good tracking quality, however does not do well in bad lighting conditions.",
                ),
                sg.Combo(['1','2','3','4'],
                default_value=self.config.gui_RANSAC3DP,
                key=self.gui_RANSAC3DP,
                background_color='#424042',
                text_color='white',
                button_arrow_color= "black",
                button_background_color = "#6f4ca1",
                tooltip = "Select the priority of eyetracking algorithims.",
                ),
                sg.Text("RANSAC 3D", background_color='#424042'),
            ],
            [
                sg.Checkbox(
                    "",
                    default=self.config.gui_HSF,
                    key=self.gui_HSF,
                    background_color='#424042',
                    tooltip = "HSF Is a new, lower resolution tracking algorithim that provides excelent resilancy to lighting conditions and great speed.",
                ),
                sg.Combo(['1','2','3','4'],
                default_value=self.config.gui_HSFP,
                key=self.gui_HSFP,
                background_color='#424042',
                text_color='white',
                button_arrow_color= "black",
                button_background_color = "#6f4ca1",
                tooltip = "Select the priority of eyetracking algorithims.",
                ),
                sg.Text("Haar Surround Feature", background_color='#424042'),
            ],
            [
                sg.Checkbox(
                    "",
                    default=self.config.gui_BLOB,
                    key=self.gui_BLOB,
                    background_color='#424042',
                    tooltip = "Blob tracking is the oldest and worst tracking algorithm, it provides fast, though sometimes innaccurate tracking.",
                ),
                sg.Combo(['1','2','3','4'],
                default_value=self.config.gui_BLOBP,
                key=self.gui_BLOBP,
                background_color='#424042',
                text_color='white',
                button_arrow_color= "black",
                button_background_color = "#6f4ca1",
                tooltip = "Select the priority of eyetracking algorithims.",
                ),
                sg.Text("Blob", background_color='#424042'),
            ],
            [
                sg.Checkbox(
                    "Blink Algo",
                    default=self.config.gui_BLINK,
                    key=self.gui_BLINK,
                    background_color='#424042',
                ),
            ],
        
            [sg.Text("HSF Radius:", background_color='#424042'),
                sg.Slider(
                    range=(1, 50),
                    default_value=self.config.gui_HSF_radius,
                    orientation="h",
                    key=self.gui_HSF_radius,
                    background_color='#424042',
                    tooltip = "Adjusts the radius paramater for HSF. Only adjust if you are having tracking issues.",
                ),
            ],
            [
                sg.Text("Blob Threshold", background_color='#424042'), #TODO make this for right and left eyes? I dont know how vital that is..
                sg.Slider(
                    range=(0, 110),
                    default_value=self.config.gui_threshold,
                    orientation="h",
                    key=self.gui_threshold_slider,
                    background_color='#424042',
                    tooltip = "Adjusts the threshold for blob tracking.",
                ),
            ],
            [sg.Text("Min Blob Size:", background_color='#424042'),
                sg.Slider(
                    range=(1, 50),
                    default_value=self.config.gui_blob_minsize,
                    orientation="h",
                    key=self.gui_blob_minsize,
                    background_color='#424042',
                    tooltip = "Minimun size a blob has to be for blob tracking.",
                ),
                
                sg.Text("Max Blob Size:", background_color='#424042'),
                sg.Slider(
                    range=(1, 50),
                    default_value=self.config.gui_blob_maxsize,
                    orientation="h",
                    key=self.gui_blob_maxsize,
                    background_color='#424042',
                    tooltip = "Maximum size a blob can be for blob tracking.",
                ),

   
            ],
            [
                sg.Text("One Euro Filter Paramaters:", background_color='#242224'),
            ],
            [
                
                sg.Text("Min Frequency Cutoff", background_color='#424042'),
                sg.InputText(
                    self.config.gui_min_cutoff,
                    key=self.gui_min_cutoff,
                ),
            ],
            [
                sg.Text("Speed Coefficient", background_color='#424042'),
                sg.InputText(
                    self.config.gui_speed_coefficient, 
                    key=self.gui_speed_coefficient,
                ),
            ],
             [
                sg.Text("OSC Settings:", background_color='#242224'),
            ],
            [
                sg.Text("OSC Address:", background_color='#424042'),
                sg.InputText(
                    self.config.gui_osc_address, 
                    key=self.gui_osc_address,
                    tooltip = "IP address we send OSC data to.",
                ),
                
            ],
            [
                sg.Text("OSC Port:", background_color='#424042'),
                sg.InputText(
                    self.config.gui_osc_port, 
                    key=self.gui_osc_port,
                    tooltip = "OSC port we send data to.",
                ),
            ],
            [
                sg.Text("OSC Receiver Port:", background_color='#424042'),
                sg.InputText(
                    self.config.gui_osc_receiver_port, 
                    key=self.gui_osc_receiver_port,
                    tooltip = "Port we receive OSC data from (used to recalibrate or recenter app from within VRChat.",
                ),
            ],
            [
                sg.Text("OSC Recenter Address:", background_color='#424042'),
                sg.InputText(
                    self.config.gui_osc_recenter_address, 
                    key=self.gui_osc_recenter_address,
                    tooltip = "OSC Address used for recentering your eye.",
                    ),
            ],
            [
                sg.Text("OSC Recalibrate Address:", background_color='#424042'),
                sg.InputText(
                    self.config.gui_osc_recalibrate_address, 
                    key=self.gui_osc_recalibrate_address,
                    tooltip = "OSC address we use for recalibrating your eye",
                    ),
            ]

        ]

        
        self.widget_layout = [
            [   
                sg.Text("General Settings:", background_color='#242224'),
            ],
            [
                sg.Column(self.general_settings_layout, key=self.gui_general_settings_layout, background_color='#424042' ),
            ],
           # [
            #    sg.Button(
             #       "Save Settings", key=self.gui_save_button, button_color = '#6f4ca1'
              #  ),
            #],
        ]

        self.cancellation_event = Event() # Set the event until start is called, otherwise we can block if shutdown is called.
        self.cancellation_event.set()
        self.image_queue = Queue()


    def started(self):
        return not self.cancellation_event.is_set()

    def start(self):
        # If we're already running, bail
        if not self.cancellation_event.is_set():
            return
        self.cancellation_event.clear()

    def stop(self):
        # If we're not running yet, bail
        if self.cancellation_event.is_set():
            return
        self.cancellation_event.set()

    def render(self, window, event, values):
        # If anything has changed in our configuration settings, change/update those.
        changed = False

        if self.config.gui_osc_port != values[self.gui_osc_port]:
            try: 
                int(values[self.gui_osc_port])
                if len(values[self.gui_osc_port]) <= 5:
                    self.config.gui_osc_port = int(values[self.gui_osc_port])
                    changed = True
                else:
                    print("[ERROR] OSC port value must be an integer 0-65535")
            except:
                print("[ERROR] OSC port value must be an integer 0-65535")

        if self.config.gui_osc_receiver_port != values[self.gui_osc_receiver_port]:
            try: 
                int(values[self.gui_osc_receiver_port])
                if len(values[self.gui_osc_receiver_port]) <= 5:
                    self.config.gui_osc_receiver_port = int(values[self.gui_osc_receiver_port])
                    changed = True
                else:
                    print("[ERROR] OSC receive port value must be an integer 0-65535")
            except:
                print("[ERROR] OSC receive port value must be an integer 0-65535")

        if self.config.gui_osc_address != values[self.gui_osc_address]:
            self.config.gui_osc_address = values[self.gui_osc_address]
            changed = True

        if self.config.gui_osc_recenter_address != values[self.gui_osc_recenter_address]:
            self.config.gui_osc_recenter_address = values[self.gui_osc_recenter_address]
            changed = True

        if self.config.gui_osc_recalibrate_address != values[self.gui_osc_recalibrate_address]:
            self.config.gui_osc_recalibrate_address = values[self.gui_osc_recalibrate_address]
            changed = True

        if self.config.gui_min_cutoff != values[self.gui_min_cutoff]:
            self.config.gui_min_cutoff = values[self.gui_min_cutoff]
            changed = True
            
        if self.config.gui_speed_coefficient != values[self.gui_speed_coefficient]:
            self.config.gui_speed_coefficient = values[self.gui_speed_coefficient]
            changed = True

        if self.config.gui_flip_x_axis_right != values[self.gui_flip_x_axis_right]:
            self.config.gui_flip_x_axis_right = values[self.gui_flip_x_axis_right]
            changed = True

        if self.config.gui_flip_x_axis_left != values[self.gui_flip_x_axis_left]:
            self.config.gui_flip_x_axis_left = values[self.gui_flip_x_axis_left]
            changed = True

        if self.config.gui_HSFP != int(values[self.gui_HSFP]):
            self.config.gui_HSFP = int(values[self.gui_HSFP])
            changed = True

        if self.config.gui_HSF != values[self.gui_HSF]:
            self.config.gui_HSF = values[self.gui_HSF]
            changed = True
        
        if self.config.gui_RANSAC3DP != int(values[self.gui_RANSAC3DP]): #TODO check that priority order is unique/auto fix it.
            self.config.gui_RANSAC3DP = int(values[self.gui_RANSAC3DP])
            changed = True

        if self.config.gui_RANSAC3D != values[self.gui_RANSAC3D]:
            self.config.gui_RANSAC3D = values[self.gui_RANSAC3D]
            changed = True

        if self.config.gui_HSRACP != int(values[self.gui_HSRACP]):
            self.config.gui_HSRACP = int(values[self.gui_HSRACP])
            changed = True

        if self.config.gui_HSRAC != values[self.gui_HSRAC]:
            self.config.gui_HSRAC = values[self.gui_HSRAC]
            changed = True

        if self.config.gui_BLINK != values[self.gui_BLINK]:
            self.config.gui_BLINK = values[self.gui_BLINK]
            changed = True

        if self.config.gui_HSF_radius != values[self.gui_HSF_radius]:
            self.config.gui_HSF_radius = values[self.gui_HSF_radius]
            changed = True

        if self.config.gui_flip_y_axis != values[self.gui_flip_y_axis]:
            self.config.gui_flip_y_axis = values[self.gui_flip_y_axis]
            changed = True

        if self.config.gui_BLOB != values[self.gui_BLOB]:
            self.config.gui_BLOB = values[self.gui_BLOB]
            changed = True

        if self.config.gui_BLOBP != int(values[self.gui_BLOBP]):
            self.config.gui_BLOBP = int(values[self.gui_BLOBP])
            changed = True

        if self.config.gui_threshold != values[self.gui_threshold_slider]:
            self.config.gui_threshold = int(values[self.gui_threshold_slider])
            changed = True

        if self.config.gui_eye_falloff != values[self.gui_eye_falloff]:
            self.config.gui_eye_falloff = values[self.gui_eye_falloff]
            changed = True

        if self.config.gui_blink_sync != values[self.gui_blink_sync]:
            self.config.gui_blink_sync = values[self.gui_blink_sync]
            changed = True

        if self.config.gui_blob_maxsize != values[self.gui_blob_maxsize]:
            self.config.gui_blob_maxsize = values[self.gui_blob_maxsize]
            changed = True

        if changed:
            self.main_config.save()
            
        self.osc_queue.put((EyeId.SETTINGS))