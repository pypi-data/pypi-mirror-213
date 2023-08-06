import cv2
import numpy as np
import os
import win32api, win32con, win32gui
import time
from PIL import ImageGrab
import math
import ctypes
import logging
from PySpeedMacro.PSMMouse import WinMouse
import PySpeedMacro.PSMInterface
import colorsys
import os
import shutil
import subprocess
import sys
import tempfile
from PIL import Image
import mss
import concurrent

platform = sys.platform
is_darwin = platform == "darwin"
is_win32 = platform == "win32"

wm = WinMouse()

speedZeroException = "Value must not be 0. If you are trying to move the mouse instantly, use direct = True"
imageNotFoundException = "Image not found on screen or region."

"""
Just for accurate mouse positioning and movement.
"""


ctypes.windll.user32.SetProcessDPIAware()


class PySpeedMacroException(Exception):
    pass


def accurate_delay(delay):

    """

    A seemingly more accurate time.sleep system.

    """

    _ = time.perf_counter() + delay
    while time.perf_counter() < _:
        pass


def timer(func):

    """

    Description: The 'timer' decorator can be used to returning how long it took for a function to run.

    Usage: @timer

    Note: Not sure if can be used in other scripts.

    """

    def wrapper(*args, **kwargs):

        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Elapsed time for {func.__name__}: {end_time - start_time:.5f} seconds")
        return result

    return wrapper

def capture_screenshot(region=None, grayscale=False):
    if region is None:
        # Capture the whole screen
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
    else:
        # Capture a specific region
        x, y, width, height = region
        with mss.mss() as sct:
            screenshot = sct.grab({'left': x, 'top': y, 'width': width, 'height': height})

    # Convert the screenshot to an OpenCV image
    img = np.array(screenshot)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # Convert to grayscale if required
    if grayscale:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return img

def Screenshot(region=None, grayscale=False, num_threads=16):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)
    with mss.mss() as sct:
        if region is None:
            monitor = sct.monitors[1]
            monitor_info = monitor
            regions = [(monitor_info['left'], monitor_info['top'], monitor_info['width'], monitor_info['height'])]
        else:
            regions = [region]

        # Submit screenshot capture tasks to the thread pool
        futures = []
        for reg in regions:
            future = executor.submit(capture_screenshot, reg, grayscale)
            futures.append(future)

        # Wait for all the tasks to complete and retrieve the results
        screenshots = [future.result() for future in futures]

        # Merge multiple screenshots into a single image
        merged_screenshot = np.concatenate(screenshots, axis=1) if len(screenshots) > 1 else screenshots[0]

        return merged_screenshot

"""

    Description: Quick and easy Screenshot method. 

    Usage: PySpeedMacro.sceenshot(region = (100, 200, 300, 400))

    # This creates a Screenshot from the pixels x = 100, y = 200, with a size of 300 by 400.
    
    Note: If no region is entered, it will Screenshot the whole screen.

    TODO:
    
     - Allow user to save Screenshot as image.
     - Save Screenshot as image type
     - Save Screenshot as title

    """

def lerp(a, b, t):

    """

    I forgot

    """

    return a + (b - a) * t


"""

███╗░░░███╗░█████╗░██╗░░░██╗░██████╗███████╗  ░█████╗░░█████╗░███╗░░██╗████████╗██████╗░░█████╗░██╗░░░░░
████╗░████║██╔══██╗██║░░░██║██╔════╝██╔════╝  ██╔══██╗██╔══██╗████╗░██║╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░
██╔████╔██║██║░░██║██║░░░██║╚█████╗░█████╗░░  ██║░░╚═╝██║░░██║██╔██╗██║░░░██║░░░██████╔╝██║░░██║██║░░░░░
██║╚██╔╝██║██║░░██║██║░░░██║░╚═══██╗██╔══╝░░  ██║░░██╗██║░░██║██║╚████║░░░██║░░░██╔══██╗██║░░██║██║░░░░░
██║░╚═╝░██║╚█████╔╝╚██████╔╝██████╔╝███████╗  ╚█████╔╝╚█████╔╝██║░╚███║░░░██║░░░██║░░██║╚█████╔╝███████╗
╚═╝░░░░░╚═╝░╚════╝░░╚═════╝░╚═════╝░╚══════╝  ░╚════╝░░╚════╝░╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░╚══════╝

"""


def getMousePosition():

    """

    Description: Simple function that returns mouse position, using win32api.

    Usage: PySpeedMacro.getMousePosition()
    
    Alternate Usage: x, y = PySpeedMacro.getMousePosition()

    Note: 

    """

    x, y = win32api.GetCursorPos()

    return x, y

def click(button = "left", separation = 0.1):

    wm.click(button, separation)


def multiClick(button = "left", count = 2, separation = 0.1):

    """

    Description: Click multiple times.

    Parameters: 

     - button | Type of button to click: "left", "right", or "middle"
     - count | How many clicks to simulate
     - separation | How long each click will take before starting a new click.

    Usage: PySpeedMacro.multiClick(count = 15, separation = 0.05)

    Note: Delay may be a little inaccurate with different operating systems.

    TODO: 

    """

    for i in range(count):

        wm.click(button, separation)
        #print("ok")


def spinMouse(center_x = None, center_y = None, radius = 100, speed = 1, count = 1):

    """

    Description: Move the mouse in a circular motion.

    Parameters: 

     - center_x, center_y | Center coordinates of the circle that the mouse will go around.
     - radius | Circle radius in pixels.
     - speed | Time in seconds to complete motion.
     - count | Amount of times mouse will spin in a circle.

    Usage: PySpeedMacro.spinMouse(100, 100, radius = 250, speed = 0.1, count = 2)

    Note: 

    TODO: 

    """

    if center_x or center_y or radius <= 0:
        print("center_x, center_y, or radius is 0. You may run into errors!")

    #try:

    if center_x or center_y == None:
        center_x, center_y = getMousePosition()

    if count < 1:
        raise ValueError("Count must be greater than or equal to 1")

    for i in range(count):
        start_time = time.time()
        angle = 0
        while time.time() - start_time < speed:
            angle = (time.time() - start_time) * 2 * math.pi / speed
            x = round(center_x + math.cos(angle) * radius)
            y = round(center_y + math.sin(angle) * radius)
            moveMouse(x, y, direct = True)

    #except:
    #    print("Could not complete operation.")


def moveMouse(x, y, direct = False, speed=0.1):
    
    """

    Description: Run a given function, then return mouse to starting position. 

    Parameters: 

     - x, y | x and y coordinates to move the mouse to.
     - direct | boolean expression for whether mouse should blink back to original spot, or glide smoothly.
     - speed | total time it should take for mouse to glide to original starting point in seconds.

    Usage: PySpeedMacro.moveMouse(100, 100, direct = False, speed = 1)

    Note: 

    TODO: Allow mouse to move freely while mouse is moving??

    """

    if speed == 0:

        raise PySpeedMacroException(speedZeroException)

    if direct:
        print(x)
        print(y)
        win32api.SetCursorPos((x, y))
    else:

        startx, starty = getMousePosition()
        distance = (x - startx, y - starty)
        steps = int(speed * 100)
        step_x = distance[0] / steps
        step_y = distance[1] / steps

        #print(f"step_x, step_y: {step_x}, {step_y}")
        #print(f"Distance: {distance}")

        for i in range(steps):
            new_x = int(startx + step_x * i)
            new_y = int(starty + step_y * i)
            win32api.SetCursorPos((new_x, new_y))
            accurate_delay(speed / steps)

        win32api.SetCursorPos((x, y))


def returnMouse(function=None, direct = False, speed = 0.1):

    """

    Description: Run a given function, then return mouse to starting position. 

    Parameters: 

     - function | run given function.
     - direct | boolean expression for whether mouse should blink back to original spot, or glide smoothly.
     - speed | total time it should take for mouse to glide to original starting point in seconds.

    Usage: PySpeedMacro.returnMouse(function=test, direct = False, speed = 0.1)

    Note: 

    TODO: 

    """

    if function is not None:

        startx, starty = getMousePosition()
        function()
        moveMouse(startx, starty, direct, speed)

    else:

        print("WARNING: No given function to run!")


"""

██╗███╗░░░███╗░█████╗░░██████╗░███████╗░██████╗███████╗░█████╗░██████╗░░█████╗░██╗░░██╗
██║████╗░████║██╔══██╗██╔════╝░██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██║░░██║
██║██╔████╔██║███████║██║░░██╗░█████╗░░╚█████╗░█████╗░░███████║██████╔╝██║░░╚═╝███████║
██║██║╚██╔╝██║██╔══██║██║░░╚██╗██╔══╝░░░╚═══██╗██╔══╝░░██╔══██║██╔══██╗██║░░██╗██╔══██║
██║██║░╚═╝░██║██║░░██║╚██████╔╝███████╗██████╔╝███████╗██║░░██║██║░░██║╚█████╔╝██║░░██║
╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝░╚═════╝░╚══════╝╚═════╝░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝

"""

# PySpeedMacro is designed to 
#
#
#
#

def locateOnScreen(path, confidence=1, directory='.', region=None, grayscale=False):

    """

    Description: Locates an image and returns the location variables for the first found image.

    Parameters: 

     - path | Image name in string form.
     - confidence | 0.0 to 1.0 scale of accuracy in matching the image. Example: 0.5 means 50% accuracy. 0.95 means 95% accuracy.
     - directory | If left empty, it will use the current directory to access the image file.
     - region | If no region is entered, it will Screenshot the whole screen.
     - grayscale | Boolean expression for converting the image to gray or not. Increase in performance if True! May lower accuracy! 

    Usage: PySpeedMacro.LocateOnScreen("image.png", confidence = 0.7, region = (100, 100, 200, 200), grayscale = True)

    Explanation: The function searches for "image.png", in a 200 by 200 region starting at 100, 100. The image matching threshold is 70% accuracy and the image is set to grayscale.

    TODO: 

    """
    try:


        fullPath = os.path.join(directory, path)
        screen = Screenshot(region, grayscale=grayscale)
        image = cv2.imread(fullPath)

        if grayscale:

            """
            If grayscale is True, then convert image to grayscale.
            """

            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        else:

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        result = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= confidence:

            x, y = max_loc[0], max_loc[1]
            w, h = image.shape[1], image.shape[0]

            if region is not None:

                x += region[0]
                y += region[1]

            return (x, y, w, h)

        else:

            return None


    except cv2.error as e:

        print(e)
        return None


def locateCenter(path, confidence=1, directory='.', region=None, grayscale=False, method = cv2.TM_CCOEFF_NORMED):

    """

    Description: Locates an image and returns the center coordinates for the first found image.

    Parameters: 

     - path | Image name in string form.
     - confidence | 0.0 to 1.0 scale of accuracy in matching the image. Example: 0.5 means 50% accuracy. 0.95 means 95% accuracy.
     - directory | If left empty, it will use the current directory to access the image file.
     - region | If no region is entered, it will Screenshot the whole screen.
     - grayscale | Boolean expression for converting the image to gray or not. Increase in performance if True! May lower accuracy! 

    Usage: PySpeedMacro.LocateCenter("image.png", confidence = 0.7, region = (100, 100, 200, 200), grayscale = True)

    Explanation: The function searches for "image.png", in a 200 by 200 region starting at 100, 100. The image matching threshold is 70% accuracy and the image is set to grayscale.

    TODO: 

    """

    try:


        fullPath = os.path.join(directory, path)
        screen = Screenshot(region, grayscale=grayscale)
        image = cv2.imread(fullPath)

        if grayscale:

            """
            If grayscale is True, then convert image to grayscale.
            """
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        else:

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        result = cv2.matchTemplate(screen, image, method)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= confidence:

            x, y = max_loc[0], max_loc[1]
            w, h = image.shape[1], image.shape[0]

            if region is not None:

                x += region[0]
                y += region[1]

            return (x+w//2, y+h//2)

        else:

            return None

    except Exception as e:
        print(e)
        return None


def locateAndMove(path, confidence=1, directory='.', region=None, grayscale=False, direct=True, speed=1):

    """
    Description: By far the most handy Image Search function! Locates an image and moves the mouse to the center of the first found image.

    Parameters:
     - path | Image name in string form.
     - confidence | 0.0 to 1.0 scale of accuracy in matching the image. Example: 0.5 means 50% accuracy. 0.95 means 95% accuracy.
     - directory | If left empty, it will use the current directory to access the image file.
     - region | If no region is entered, it will Screenshot the whole screen.
     - grayscale | Boolean expression for converting the image to gray or not. Increase in performance if True! May lower accuracy!
     - direct | boolean expression for whether mouse should blink back to original spot, or glide smoothly.
     - speed | total time it should take for mouse to glide to original starting point in seconds.

    Usage: PySpeedMacro.LocateAndMove("image.png", confidence = 0.7, region = (100, 100, 200, 200), grayscale = True, direct = False, speed = 0.2)

    Explanation: The function searches for "image.png", in a 200 by 200 region starting at 100, 100. The image matching threshold is 70% accuracy and the image is set to grayscale. Once the image is located the mouse will glide to that location in 0.2 seconds.

    """

    try:

        fullPath = os.path.join(directory, path)

        if region is not None and region[2] <= 0:

            raise ValueError("Width of the screenshot region must be a positive number.")

        if region is not None and region[3] <= 0:

            raise ValueError("Height of the screenshot region must be a positive number.")

        screen = Screenshot(region, grayscale=grayscale)
        image = cv2.imread(fullPath)

        if grayscale:

            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        else:

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        result = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= confidence:

            x, y = max_loc[0], max_loc[1]
            w, h = image.shape[1], image.shape[0]

            if region is not None:

                x += region[0]
                y += region[1]

            moveMouse(x + w // 2, y + h // 2, direct, speed)

            return (x, y, w, h)

        else:

            print("Image not found")
            return None

    except cv2.error as e:

        print(e)
        return None

    except ValueError as e:

        print(e)
        return None

def getPixelRGB(x, y):

    screen = np.array(ImageGrab.grab())

    r, g, b = screen[y, x, :]

    return (r, g, b)

def getPixelHSV(x, y):

    screen = np.array(ImageGrab.grab())
    hsv_image = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2HSV)

    hsv = hsv_image[y, x]
    return (hsv[0], hsv[1], hsv[2])


def grab(bbox=None, include_layered_windows=False, all_screens=False, xdisplay=None):
    if xdisplay is None:
        if is_darwin:
            fh, filepath = tempfile.mkstemp(".png")
            os.close(fh)
            args = ["screencapture"]
            if bbox:
                left, top, right, bottom = bbox
                args += ["-R", f"{left},{top},{right - left},{bottom - top}"]
            subprocess.call(args + ["-x", filepath])
            im = Image.open(filepath)
            im.load()
            os.unlink(filepath)
            if bbox:
                im_resized = im.resize((right - left, bottom - top))
                im.close()
                return im_resized
            return im
        elif is_win32:
            offset, size, data = Image.core.grabscreen_win32(include_layered_windows, all_screens)
            im = Image.frombytes(
                "RGB",
                size,
                data,
                "raw",
                "BGR",
                (size[0] * 3 + 3) & -4,
                -1,
            )
            if bbox:
                x0, y0 = offset
                left, top, right, bottom = bbox
                im = im.crop((left - x0, top - y0, right - x0, bottom - y0))
            return im
    try:
        if not Image.core.HAVE_XCB:
            raise OSError("Pillow was built without XCB support")
        size, data = Image.core.grabscreen_x11(xdisplay)
    except OSError:
        if xdisplay is None and platform not in ("darwin", "win32") and shutil.which("gnome-screenshot"):
            fh, filepath = tempfile.mkstemp(".png")
            os.close(fh)
            subprocess.call(["gnome-screenshot", "-f", filepath])
            im = Image.open(filepath)
            im.load()
            os.unlink(filepath)
            if bbox:
                im_cropped = im.crop(bbox)
                im.close()
                return im_cropped
            return im
        else:
            raise
    else:
        im = Image.frombytes("RGB", size, data, "raw", "BGRX", size[0] * 4, 1)
        if bbox:
            im = im.crop(bbox)
        return im








@timer
def getHue(region):

    screen = Screenshot(region)

    pixels = np.array(screen)
    total_r, total_g, total_b = 0, 0, 0
    for y in range(pixels.shape[0]):
        for x in range(pixels.shape[1]):
            pixel = pixels[y, x]
            total_r += pixel[0]
            total_g += pixel[1]
            total_b += pixel[2]
    pixel_count = pixels.shape[0] * pixels.shape[1]
    avg_r = total_r // pixel_count
    avg_g = total_g // pixel_count
    avg_b = total_b // pixel_count
    # Calculate the difference between the average color and the grayscale value
    gray = (avg_r + avg_g + avg_b) // 3
    delta_gray = abs(avg_r - gray) + abs(avg_g - gray) + abs(avg_b - gray)
    # Return the "hue" value as a percentage of the maximum possible value (255*3)
    return delta_gray / (255 * 3)


def setWindow(name):
    """
    Name = Window name : Type = String
    """
    # Get the window handle for the specified window name
    handle = win32gui.FindWindow(None, name)

    # Check if a window handle was found
    if handle == 0:
        print(f"No window found with name '{name}'")
        return

    # Check if the window is currently hidden
    if win32gui.IsIconic(handle):
        # Window is hidden, so restore it
        win32gui.ShowWindow(handle, win32con.SW_RESTORE)
    else:
        # Window is already active, so just focus on it
        ctypes.windll.user32.SetForegroundWindow(handle)

    print(f"Window '{name}' activated")
