#   Copyright (C) 2021  Davide De Tommaso
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>

import yarp
yarp.Network.init()

from pyicub.controllers.GazeController import GazeController
from pyicub.controllers.PositionController import PositionController
from pyicub.modules.emotions import emotionsPyCtrl
from pyicub.modules.speech import speechPyCtrl
from pyicub.modules.face import facePyCtrl
from pyicub.modules.faceLandmarks import faceLandmarksPyCtrl
from pyicub.core.BufferedPort import BufferedReadPort
from pyicub.core.Logger import YarpLogger

import threading
import yaml
import os
from collections import deque
import concurrent.futures

class ICUB_PARTS:
    HEAD       = 'head'
    FACE       = 'face'
    TORSO      = 'torso'
    LEFT_ARM   = 'left_arm'
    RIGHT_ARM  = 'right_arm'
    LEFT_LEG   = 'left_leg'
    RIGHT_LEG  = 'right_leg'

class iCubPart:
    def __init__(self, name, joints_n):
        self.name = name
        self.joints_n = joints_n
        self.joints_list = range(0, joints_n)

class JointAction:
    def __init__(self, part_name, target_position, req_time, joints_list=None):
        self.part_name = part_name
        self.target_position = target_position
        self.req_time = req_time
        self.joints_list = joints_list

class PortMonitor:
    def __init__(self, yarp_src_port, activate_function, callback, period=0.01, autostart=False):
        self._port = BufferedReadPort(yarp_src_port + "_reader_" + str(id(self)), yarp_src_port,)
        self._activate = activate_function
        self._callback = callback
        self._period = period
        self._values = deque( int(1000/(period*1000))*[None], maxlen=int(1000/(period*1000))) #Values of the last second
        self._stop_thread = False
        if autostart:
            self.start()

    def start(self):
        if self._stop_thread:
           self.stop()
        self._worker_thread = threading.Thread(target=self.worker)
        self._worker_thread.start()

    def stop(self):
        if not self._stop_thread:
            self._stop_thread = True
        self._worker_thread.join()
        self._stop_thread = False

    def worker(self):
        while not self._stop_thread:
            res = self._port.read(shouldWait=False)
            if not res is None:
                self._values.append(res.toString())
                if self._activate(self._values):
                    self._callback()
            yarp.delay(self._period)

    def __del__(self):
        self.stop()
        del self._port

class iCubRequest:

    TIMEOUT_REQUEST = 30.0

    def __init__(self, timeout, target, *args, **kwargs):
        self.start_time = time.perf_counter()
        self.timeout = timeout
        self.duration = None
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.future = self.executor.submit(target,*args,**kwargs)

    def wait_for_completed(self):
        res = None
        try:
            res = self.future.result(self.timeout)
        except Exception:
            pass
        finally:
            self.duration = time.perf_counter() - self.start_time
            self.executor.shutdown(wait=False)
        return res


class iCubTask:

    @staticmethod
    def request(timeout=iCubRequest.TIMEOUT_REQUEST):
        def wrapper(target):
                def f(*args, **kwargs):
                    return iCubRequest(timeout, target, *args, **kwargs)
                return f
        return wrapper

    @staticmethod
    def join(requests):
        for req in requests:
            req.wait_for_completed()

class iCub:

    def __init__(self, configuration_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'robot_configuration.yaml'), disable_logs=False):
        self.__icub_controllers__ = {}
        self.__position_controllers__ = {}
        self.__drivers__ = {}
        self.__encoders__ = {}
        self.__gazectrl__ = None
        self.__emo__ = None
        self.__speech__ = None
        self.__face__ = None
        self.__facelandmarks__ = None
        self.__monitors__ = []
        self.__logger__ = YarpLogger.getLogger()

        if disable_logs:
            self.__logger__.disable_logs()

        self.__icub_parts__ = {}
        self.__icub_parts__[ICUB_PARTS.HEAD] = iCubPart(ICUB_PARTS.HEAD, 6)
        self.__icub_parts__[ICUB_PARTS.FACE] = iCubPart(ICUB_PARTS.FACE, 1)
        self.__icub_parts__[ICUB_PARTS.LEFT_ARM] = iCubPart(ICUB_PARTS.LEFT_ARM, 16)
        self.__icub_parts__[ICUB_PARTS.RIGHT_ARM] = iCubPart(ICUB_PARTS.RIGHT_ARM, 16)
        self.__icub_parts__[ICUB_PARTS.TORSO] = iCubPart(ICUB_PARTS.TORSO, 3)
        self.__icub_parts__[ICUB_PARTS.LEFT_LEG] = iCubPart(ICUB_PARTS.LEFT_LEG, 6)
        self.__icub_parts__[ICUB_PARTS.RIGHT_LEG] = iCubPart(ICUB_PARTS.RIGHT_LEG, 6)

        with open(configuration_file) as f:
            self.__robot_conf__ = yaml.load(f, Loader=yaml.FullLoader)

        self.__robot__ = self.__robot_conf__['robot_name']

        if 'gaze_controller' in self.__robot_conf__.keys():
            if self.__robot_conf__['gaze_controller'] is True:
                self.__gazectrl__ = GazeController(self.__robot__)

        if 'position_controllers' in self.__robot_conf__.keys():
            for part_name in self.__robot_conf__['position_controllers']:
                self.__icub_controllers__[part_name] = self.getPositionController(self.__icub_parts__[part_name])

    def __getDriver__(self, robot_part):
        if not robot_part.name in self.__drivers__.keys():
            props = self.__getRobotPartProperties__(robot_part)
            self.__drivers__[robot_part.name] = yarp.PolyDriver(props)
        return self.__drivers__[robot_part.name]

    def __getIEncoders__(self, robot_part):
        if not robot_part.name in self.__encoders__.keys():
            driver = self.__getDriver__(robot_part)
            self.__encoders__[robot_part.name] = driver.viewIEncoders()
        return self.__encoders__[robot_part.name]

    def __getRobotPartProperties__(self, robot_part):
        props = yarp.Property()
        props.put("device","remote_controlboard")
        props.put("local","/client/" + self.__robot__ + "/" + robot_part.name)
        props.put("remote","/" + self.__robot__ + "/" + robot_part.name)
        return props

    def close(self):
        if len(self.__monitors__) > 0:
            for v in self.__monitors__:
                v.stop()
        for driver in self.__drivers__.values():
            driver.close()
        yarp.Network.fini()

    @property
    def face(self):
        if self.__face__ is None:
            self.__face__ = facePyCtrl(self.__robot__)
        return self.__face__

    @property
    def facelandmarks(self):
        if self.__facelandmarks__ is None:
           self.__facelandmarks__ = faceLandmarksPyCtrl()
        return self.__facelandmarks__

    @property
    def gaze(self):
        return self.__gazectrl__

    @property
    def emo(self):
        if self.__emo__ is None:
            self.__emo__ = emotionsPyCtrl(self.__robot__)
        return self.__emo__

    @property
    def speech(self):
        if self.__speech__ is None:
            self.__speech__ = speechPyCtrl(self.__robot__)
        return self.__speech__

    def portmonitor(self, yarp_src_port, activate_function, callback):
        self.__monitors__.append(PortMonitor(yarp_src_port, activate_function, callback, period=0.01, autostart=True))

    def getPositionController(self, robot_part, joints_list=None):
        if not robot_part in self.__position_controllers__.keys():
            driver = self.__getDriver__(robot_part)
            iencoders = self.__getIEncoders__(robot_part)
            if joints_list is None:
                joints_list = robot_part.joints_list
            self.__position_controllers__[robot_part.name] = PositionController(driver, joints_list, iencoders)
        return self.__position_controllers__[robot_part.name]

    def move(self, action):
        ctrl = self.__icub_controllers__[action.part_name]
        return ctrl.move(target_joints=action.target_position, req_time=action.req_time, joints_list=action.joints_list)
