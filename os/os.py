import time
import shutil
import subprocess
import os
import socket
from periphery import GPIO
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont

# Set to "rock2f" or "rpi"
BOARD = "rock2f"

if BOARD == "rock2f":
    I2C_PORT = 0
    GPIOCHIP = "/dev/gpiochip4"
    BUZZER = 19
    BTN_UP = 15
    BTN_SELECT = 16
    BTN_DOWN = 22
elif BOARD == "rpi":
    I2C_PORT = 1
    GPIOCHIP = "/dev/gpiochip4"
    BUZZER = 12
    BTN_UP = 22
    BTN_SELECT = 27
    BTN_DOWN = 17
else:
    raise ValueError(f"Unknown BOARD: {BOARD}")


class RecorderState:
    def __init__(self, output_dir=None):
        if output_dir is None:
            output_dir = os.path.expanduser("~/captures")
        self.mode = "idle"
        self.start_time = None
        self.process = None
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    @property
    def camera_connected(self):
        # Check if a FireWire camera is connected (fw1 exists when camera plugged in)
        return os.path.exists("/dev/fw1")

    def toggle(self):
        if self.mode == "idle":
            if not self.camera_connected:
                return
            self.mode = "recording"
            self.start_time = time.time()
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            self.process = subprocess.Popen(
                ["dvgrab", "-buffers", "20",
                 f"{self.output_dir}/capture_{timestamp}-"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        else:
            self.mode = "idle"
            if self.process:
                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.process.kill()
                self.process = None
            self.start_time = None

    @property
    def is_recording(self):
        return self.mode == "recording"

    @property
    def elapsed_text(self):
        if not self.is_recording or self.start_time is None:
            return "00:00:00"
        elapsed = time.time() - self.start_time
        hh, rem = divmod(int(elapsed), 3600)
        mm, ss = divmod(rem, 60)
        return f"{hh:02}:{mm:02}:{ss:02}"

    @property
    def recording_minutes_left(self):
        _, _, free = shutil.disk_usage(self.output_dir)
        # DV video around 3.6 MB/s = 216 MB/min
        # How could we know bitrate of different cameras?
        minutes = free / (216 * 1024 * 1024)
        return f"{int(minutes)}m"


class Display:
    def __init__(self):
        serial = i2c(port=I2C_PORT, address=0x3C)
        self.device = sh1106(serial)
        self.font_medium = ImageFont.truetype(
            "fonts/Px437_DOS-V_re_JPN12.ttf", 12
        )
        self.font_big = ImageFont.truetype(
            "fonts/Px437_Paradise132_7x16.ttf", 34
        )

    def clear(self):
        img = Image.new("1", self.device.size)
        self.device.display(img)

    def render(self, draw_func):
        img = Image.new("1", self.device.size)
        draw = ImageDraw.Draw(img)
        draw_func(draw, self.device.width, self.device.height)
        self.device.display(img)


class Screen:    
    def __init__(self, app):
        self.app = app
    
    def on_select(self):
        pass
    
    def can_navigate(self):
        return True
    
    def render(self, draw, width, height):
        pass


class RecordingScreen(Screen):
    def on_select(self):
        self.app.recorder.toggle()
    
    def can_navigate(self):
        return not self.app.recorder.is_recording
    
    def render(self, draw, width, height):
        recorder = self.app.recorder
        font_medium = self.app.display.font_medium
        font_big = self.app.display.font_big
        
        # No camera connected
        if not recorder.camera_connected and not recorder.is_recording:
            draw.text((0, 0), "RECORD", font=font_medium, fill=255)
            no_cam = "NO CAM"
            bbox = draw.textbbox((0, 0), no_cam, font=font_big)
            x = (width - (bbox[2] - bbox[0])) // 2
            draw.text((x, 28), no_cam, font=font_big, fill=255)
            return
        
        # Recording indicator
        if recorder.is_recording:
            if int(time.time() * 2) % 2:
                draw.ellipse((0, 2, 10, 12), fill=255)
            draw.text((14, 0), "REC", font=font_medium, fill=255)
        else:
            draw.text((0, 0), "RECORD", font=font_medium, fill=255)
        
        # Minutes left (top right)
        mins_left = recorder.recording_minutes_left
        bbox = draw.textbbox((0, 0), mins_left, font=font_medium)
        draw.text((width - (bbox[2] - bbox[0]), 0), mins_left, font=font_medium, fill=255)
        
        # Timer (center)
        timer = recorder.elapsed_text
        bbox = draw.textbbox((0, 0), timer, font=font_big)
        x = (width - (bbox[2] - bbox[0])) // 2
        draw.text((x, 28), timer, font=font_big, fill=255)


class StorageScreen(Screen):
    def render(self, draw, width, height):
        font_medium = self.app.display.font_medium
        
        draw.text((0, 0), "STORAGE", font=font_medium, fill=255)
        
        total, used, free = shutil.disk_usage(self.app.recorder.output_dir)
        total_gb = total / (1024**3)
        used_gb = used / (1024**3)
        free_gb = free / (1024**3)
        percent = (used / total) * 100
        
        draw.text((0, 16), f"Total: {total_gb:.1f} GB", font=font_medium, fill=255)
        draw.text((0, 30), f"Used:  {used_gb:.1f} GB ({percent:.0f}%)", font=font_medium, fill=255)
        draw.text((0, 44), f"Free:  {free_gb:.1f} GB", font=font_medium, fill=255)


class NetworkScreen(Screen):
    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "No connection"
    
    def render(self, draw, width, height):
        font_medium = self.app.display.font_medium
        
        draw.text((0, 0), "NETWORK", font=font_medium, fill=255)
        
        ip = self.get_ip()
        draw.text((0, 20), "IP Address:", font=font_medium, fill=255)
        draw.text((0, 34), ip, font=font_medium, fill=255)


class USBGadgetScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.enabled = False
    
    def on_select(self):
        self.enabled = not self.enabled
        if self.enabled:
            subprocess.run(["modprobe", "g_mass_storage", 
                          f"file={self.app.recorder.output_dir}", "removable=1"],
                          capture_output=True)
        else:
            subprocess.run(["modprobe", "-r", "g_mass_storage"], capture_output=True)
    
    def render(self, draw, width, height):
        font_medium = self.app.display.font_medium
        
        draw.text((0, 0), "USB GADGET", font=font_medium, fill=255)
        
        status = "ENABLED" if self.enabled else "DISABLED"
        draw.text((0, 20), "Mass Storage Mode:", font=font_medium, fill=255)
        draw.text((0, 34), status, font=font_medium, fill=255)
        draw.text((0, 50), "Press to toggle", font=font_medium, fill=255)


class PowerScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        self.options = ["Shutdown", "Reboot", "Cancel"]
        self.selected = 0
        self.confirm_mode = False
    
    def on_select(self):
        if not self.confirm_mode:
            self.confirm_mode = True
        else:
            if self.options[self.selected] == "Shutdown":
                subprocess.run(["sudo", "shutdown", "-h", "now"])
            elif self.options[self.selected] == "Reboot":
                subprocess.run(["sudo", "reboot"])
            else:
                self.confirm_mode = False
                self.selected = 0
    
    def on_up(self):
        if self.confirm_mode:
            self.selected = (self.selected - 1) % len(self.options)
            return True
        return False
    
    def on_down(self):
        if self.confirm_mode:
            self.selected = (self.selected + 1) % len(self.options)
            return True
        return False
    
    def render(self, draw, width, height):
        font_medium = self.app.display.font_medium
        
        draw.text((0, 0), "POWER", font=font_medium, fill=255)
        
        if not self.confirm_mode:
            draw.text((0, 20), "Press to select:", font=font_medium, fill=255)
            draw.text((0, 34), "Shutdown / Reboot", font=font_medium, fill=255)
        else:
            for i, opt in enumerate(self.options):
                y = 16 + i * 16
                prefix = "> " if i == self.selected else "  "
                draw.text((0, y), prefix + opt, font=font_medium, fill=255)


class TestScreen(Screen):
    def render(self, draw, width, height):
        draw.rectangle((0, 0, width, height), fill=255)



class Buzzer:
    def __init__(self, chip=GPIOCHIP, line=BUZZER):
        self.gpio = GPIO(chip, line, "out")
    
    def beep(self, duration=0.08, freq=2048):
        cycles = int(duration * freq)
        half_period = 1.0 / freq / 2
        for _ in range(cycles):
            self.gpio.write(True)
            time.sleep(half_period)
            self.gpio.write(False)
            time.sleep(half_period)
    
    def close(self):
        self.gpio.close()


class Button:
    def __init__(self, chip, line):
        self.gpio = GPIO(chip, line, "in")
        self.last_state = True
        self.last_press = 0

    def pressed(self):
        current = self.gpio.read()
        now = time.time()

        if self.last_state and not current and (now - self.last_press) > 0.3:
            self.last_press = now
            self.last_state = current
            return True

        self.last_state = current
        return False

    def close(self):
        self.gpio.close()


class Buttons:
    def __init__(self):
        self.up = Button(GPIOCHIP, BTN_UP)
        self.select = Button(GPIOCHIP, BTN_SELECT)
        self.down = Button(GPIOCHIP, BTN_DOWN)
 
    def close(self):
        self.up.close()
        self.select.close()
        self.down.close()


class App:
    def __init__(self):
        self.recorder = RecorderState()
        self.display = Display()
        self.buttons = Buttons()
        self.buzzer = Buzzer()
        
        self.screens = [
            #TestScreen(self),
            RecordingScreen(self),
            StorageScreen(self),
            NetworkScreen(self),
            #USBGadgetScreen(self),
            PowerScreen(self),
        ]
        self.current_screen_idx = 0
    
    @property
    def current_screen(self):
        return self.screens[self.current_screen_idx]
    
    def navigate_up(self):
        if hasattr(self.current_screen, 'on_up') and self.current_screen.on_up():
            return
        
        if self.current_screen.can_navigate():
            self.current_screen_idx = (self.current_screen_idx - 1) % len(self.screens)
    
    def navigate_down(self):
        if hasattr(self.current_screen, 'on_down') and self.current_screen.on_down():
            return
        
        if self.current_screen.can_navigate():
            self.current_screen_idx = (self.current_screen_idx + 1) % len(self.screens)
    
    def run(self):
        try:
            while True:
                if self.buttons.up.pressed():
                    self.buzzer.beep()
                    self.navigate_up()
                
                if self.buttons.down.pressed():
                    self.buzzer.beep()
                    self.navigate_down()
                
                if self.buttons.select.pressed():
                    self.buzzer.beep()
                    self.current_screen.on_select()
                
                self.display.render(self.current_screen.render)
                time.sleep(0.05)
        
        except KeyboardInterrupt:
            pass
        finally:
            if self.recorder.is_recording:
                self.recorder.toggle()
            self.buttons.close()
            self.buzzer.close()


def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()
