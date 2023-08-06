import csv
import datetime
from os.path import expanduser, isfile, join

import numpy
import yaml
from sentry_sdk import capture_exception, capture_message


def config_time(task):
    time = [task["time"]]
    for i in range(len(time)):
        if len(time[i]) != 5:
            raise AssertionError("[OfflineAgent] Time data incorrect length")

    try:
        t = time[0].split(":")
        total_minutes = int(t[0]) * 60 + int(t[1]) * 1

    except BaseException as e:
        capture_exception(e)
        capture_message("[OfflineAgent] Time data incorrect")
        raise BaseException from e

    cron_split = []
    cron = 0

    if task["cron"] != "":
        cron_split.append(task["cron"].split())
        cron_raw = cron_split
        cron_time1 = cron_raw[0][0]
        if len(cron_time1) < 5:
            if len(cron_time1) == 1:
                cron = 0
            elif len(cron_time1) == 4:
                cron_str = cron_time1[2] + cron_time1[3]
                cron = int(cron_str)
            else:
                cron_str = cron_time1[2]
                cron = int(cron_str)

        elif len(cron_time1) > 5:
            if len(cron_time1) == 7:
                cron_str = cron_time1[5] + cron_time1[6]
                cron = int(cron_str)
            elif len(cron_time1) == 6:
                cron_str = cron_time1[5]
                cron = int(cron_str)
        else:
            cron = 0

        new_time = total_minutes

        while cron != 0 and new_time < 1440:
            new_time = new_time + cron
            if new_time > 1440:
                new_time = 1440
            new_time_datetime = "{:02d}:{:02d}".format(*divmod(new_time, 60))
            time.append(new_time_datetime)
    else:
        cron_split.append("")

    return time


class OfflineAgent:
    def __init__(
            self, vehicle_list, handlers, log_info, log_error

    ):

        self.log_info = log_info
        self.log_error = log_error
        self.vehicle_list = vehicle_list
        self.number_of_vehicles = len(vehicle_list)
        self.handlers = handlers

        self.current_task_uuid = None
        self.task_offline_started = False
        self.last_executed_time = None

        self.offline = None
        self.offline_tasks = None

    def activate_offline_agent(self):
        #self.log_info("[OfflineAgent] Offline Agent Activated")

        self.task_offline_started= self.offline_task_executer(
            self.offline_tasks,
            self.vehicle_list,
            self.task_offline_started,
        )
        self.offline = True

    def config_weekdays(self, task):
        week_days = numpy.zeros(7, dtype=int)
        weeks_days = []

        for day in task["week_days"]:
            if not isinstance(day, int):
                raise TypeError("[OfflineAgent] Day is not integer")

            if int(day) < 0 or int(day) > 7:
                raise TypeError("[OfflineAgent] Day must be between 0 to 6")

            week_days[int(day)] = 1
            weeks_days.append(int(day))

        # If no days are specified it is done for all the days
        if len(weeks_days) == 0:
            self.log_info(
                "[OfflineAgent] Offline task where no weekdays where specified"
            )
            for day in range(7):
                week_days[int(day)] = 1
                weeks_days.append(int(day))

        return weeks_days

    def config_goal(self, task):
        goals = []
        for goal in task["task_preset"]["subtasks"]:
            point = goal[list(goal.keys())[1]]
            point_type = point["point_type"]

            if not isinstance(point_type, str):
                raise TypeError("[OfflineAgent] Point Type is not string")
            # self.check_empty(point_type, "Offline Task, point_type")
            x = point["x_coordinate"]
            y = point["y_coordinate"]
            self.check_empty(x, "Offline Task, x")
            self.check_empty(y, "Offline Task, y")
            rotation = point["rotation"]
            self.check_empty(rotation, "Offline Task, rotation")
            if not isinstance(rotation, int) or (rotation > 361 or rotation < 0):
                raise TypeError("[OfflineAgent] Rotation is an invalid data")

            goals.append([x, y, rotation])

        return goals

    def config_loc_uuid(self, task):
        location_uuid = []

        for goal in task["task_preset"]["subtasks"]:

            point = goal[list(goal.keys())[1]]

            if not isinstance(point["uuid"], str):
                raise TypeError("[OfflineAgent] Uuid is not string")

            self.check_empty(point["uuid"], "Offline Task, point_uuid")

            location_uuid.append(point["uuid"])

        return location_uuid

    def open_yaml(self, filename):
        try:
            with open(filename, "r") as config:
                return yaml.safe_load(config)
        except OSError:
            capture_exception(OSError)

            self.log_info(
                "[OfflineAgent] %s does not exist" % (filename,)
            )

    def config_offlinetasks(self):
        offline_tasks = []
        self.log_info("[OfflineAgent] Configuring Offline Tasks")

        if self.offline:
            try:
                tasks_file_path = join(expanduser("~"), ".meili/tasks.yaml")
                data = self.open_yaml(tasks_file_path)
                self.check_empty(data, "Offline Tasks file")

                self.last_executed_time = [0 for _ in range(self.number_of_vehicles)]

                for task in data:
                    uuid = task["uuid"]
                    vehicle = task["vehicle"]["uuid"]

                    if not isinstance(uuid, str):
                        raise TypeError("[OfflineAgent] Offline Task file, task uuid")
                    if not isinstance(vehicle, str):
                        raise TypeError(
                            "[OfflineAgent] Offline Task file, vehicle uuid"
                        )
                    self.check_empty(uuid, "Offline Task file, uuid")
                    self.check_empty(vehicle, "Offline Task file, vehicle uuid")

                    goals = []
                    weeks_days = []
                    time = []
                    location_uuid = []
                    try:
                        weeks_days = self.config_weekdays(task)
                        goals = self.config_goal(task)
                        location_uuid = self.config_loc_uuid(task)
                        time = config_time(task)
                    except Exception as e:
                        self.log_error(
                            "[OfflineAgent] Configuration Error: %s" % e,
                        )

                    if len(vehicle) != 0 and len(goals) != 0:
                        offline_tasks.append(
                            [uuid, weeks_days, time, vehicle, goals, location_uuid]
                        )

                self.log_info("[OfflineAgent] Offline Tasks Configured")
            except AssertionError:
                capture_exception(AssertionError)
                capture_message("[OfflineAgent] Error Configuring Offline Tasks")
                self.log_error(
                    "[OfflineAgent] Error Configuring Offline Tasks"
                )
                exit()

        return offline_tasks

    def get_vehicle_position(self, vehicle_list, vehicle_uuid):
        try:
            position = vehicle_list.index(vehicle_uuid)
        except ValueError:
            capture_exception(ValueError)
            self.log_info(
                "[OfflineAgent] Vehicle %s is not in the list of vehicle, task will be sent to the first one in the "
                "list "
                % (vehicle_uuid,)
            )
            position = 0

        return position

    def offline_task_handler(self, pose, location, vehicle_position):
        if len(pose) == 1:
            x = pose[0][1]
            y = pose[0][2]
            xm = x
            ym = y
            rotation = pose[0][3]
            vehicle = self.offline_tasks[0][3]

            task = {
                "location": location,
                "number": location,
                "uuid": location,
            }
            data = {
                "uuid": location,
                "number": location,
                "location": {
                    "uuid": location,
                    "x": x,
                    "y": y,
                    "metric": {"x": xm, "y": ym},
                    "rotation": rotation,
                },
                "metric_waypoints": None,
            }

            self.handlers.task_handler(
                task=task,
                data=data,
                vehicle=vehicle,
            )
        else:
            self.handlers.waypoints_handler(vehicle_position=vehicle_position, pose=pose, current_task_uuid=location)

    def offline_task_executer(
            self,
            offline_tasks,
            vehicle_list,
            task_offline_started,
    ):
        today = datetime.date.today().weekday()
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")

        self.offline_tasks = offline_tasks

        for task in offline_tasks:
            task_execution_time = task[2]
            task_execution_day = task[1]

            pose = task[4]
            vehicle_uuid = task[3]
            location = task[5]

            position = self.get_vehicle_position(vehicle_list, vehicle_uuid)

            for day in task_execution_day:
                if today == day:
                    for execution_time in task_execution_time:
                        if (
                                current_time == execution_time
                                and task_offline_started is False
                                and current_time != self.last_executed_time[position]
                        ):
                            task_offline_started = True
                            self.last_executed_time[position] = execution_time
                            self.current_task_uuid = task[0]
                            self.offline_task_handler(pose, location, position)

        return task_offline_started

    def logging_offlinetasks(
            self, offline_task, number_of_tasks, vehicle_list, start_time, success
    ):

        task_number = number_of_tasks
        uuid = offline_task[0]

        # TO DO: add time+date
        vehicle = offline_task[3]
        location_uuid = offline_task[5]
        time = self.last_executed_time[vehicle_list.index(vehicle)]
        now = datetime.datetime.now()
        end_time = now.strftime("%d/%m/%Y %H:%M:%S")

        tasks_log_file_path = join(expanduser("~"), ".meili/log_tasks.csv")
        file_exists = isfile(tasks_log_file_path)

        with open(tasks_log_file_path, "a+", newline="") as file:
            fieldnames = [
                "no",
                "time",
                "uuid",
                "vehicle",
                "success",
                "location",
                "start_time",
                "end_time",
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            data = {
                "no": task_number,
                "time": time,
                "uuid": uuid,
                "vehicle": vehicle,
                "success": success,
                "location": location_uuid,
                "start_time": start_time,
                "end_time": end_time,
            }

            writer.writerow(data)
        self.log_info(
            "[ROSAgent] Task %s Logged in %s"
            % (
                task_number,
                tasks_log_file_path,
            )
        )

    def check_empty(self, variable, name):
        if not variable and variable != 0:
            self.log_error("[OfflineAgent] %s is empty" % (name,))
            raise AssertionError("[OfflineAgent] Empty", name)
