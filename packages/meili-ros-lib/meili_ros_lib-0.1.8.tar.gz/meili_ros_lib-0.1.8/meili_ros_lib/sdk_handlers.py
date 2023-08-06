from meili_sdk.websockets.client import MeiliWebsocketClient
from sentry_sdk import capture_exception, capture_message
from meili_ros_lib.parse_data import parse_waypoints, parse_docking_routine
from meili_ros_lib.sentry import agent_sentry

from std_msgs.msg import Bool

import time


class Handlers:

    def __init__(self, agent):

        self.agent = agent
        self.client = []  # docking routine

        for i in range(0, self.agent.number_of_vehicles):
            self.client.append(0)  # docking routine

        self.rate = None

    def sdk_setup(self):
        """sdk_setup"""
        try:
            self.agent.client = MeiliWebsocketClient(
                self.agent.token,
                override_host=self.agent.server_instance.replace("http", "ws"),
                fleet=self.agent.fleet,
                open_handler=self.open_handler,
                close_handler=self.close_handler,
                error_handler=self.error_handler,
                task_handler=self.task_handler,
                task_cancellation_handler=self.task_cancellation_handler,
                move_action_handler=self.move_action_handler,
                slow_down_handler=self.slow_down_handler,
                topic_list_initializer_handler=self.topic_handler,
                path_rerouting_handler=self.path_rerouting_handler,
                docking_routine_request_handler=self.docking_routine_request_handler,
                docking_routine_finalize_handler=self.docking_routine_finalize_handler,
                collision_clearance_handler=self.collision_clearance_handler,
            )
        except KeyError as error:
            self.agent.log_info(f"[ROSHandler] No handler named {error}")
            capture_exception(error)
        return self.agent.client

    def check_fleet_get_vehicle_position(self, vehicle):
        if self.agent.fleet:
            return self.agent.return_vehicle_position(vehicle)
        return 0

    def move_action_handler(self, _, data: dict, vehicle: str):
        """When a task is received, goal is generated and sent to the specific robot"""
        try:
            vehicle_position = self.check_fleet_get_vehicle_position(vehicle)
            self.send_goal(data, vehicle_position)
            self.rate.sleep()

            # If the robot is moving the task will be automatically cancelled to go to the
            # charging station.
            self.agent.log_info(
                f"[ROSHandler] Sending vehicle {self.agent.vehicle_list[vehicle_position]}: "
                f"{self.agent.vehicle_names[vehicle_position]} to CHARGING STATION"
            )

        except Exception as error:
            self.agent.log_error(
                "[ROSHandler] Error move_action_handler: %s" % (error,)
            )
            agent_sentry(error, "[ROSHandler] Error move_action_handler")

    def task_handler(self, _, data: dict, vehicle: str):
        """When a task is received, goal is generated and sent to the specific robot"""
        try:
            vehicle_position = self.check_fleet_get_vehicle_position(vehicle)
            current_task_uuid = data["uuid"]

            self.agent.number_of_tasks = self.agent.number_of_tasks + 1

            self.agent.log_info(
                f"[ROSHandler] Number of received task is: {self.agent.number_of_tasks}"
            )
            self.agent.log_info(
                f"[ROSHandler] Received task assigned to vehicle: {self.agent.vehicle_names[vehicle_position]}"
            )
            if not data["metric_waypoints"]:
                # Case when only one task is sent
                self.send_goal(data, vehicle_position)
            else:
                # This is batch-task vehicle
                if self.agent.node.path_planning:
                    pose = parse_waypoints(data)
                    # self.agent.total_waypoints = len(x_meters)
                    self.waypoints_handler(
                        vehicle_position=vehicle_position,
                        pose=pose,
                        current_task_uuid=current_task_uuid,
                    )
                else:
                    self.send_goal(data, vehicle_position)

            self.rate.sleep()

        except KeyError as error:
            self.agent.log_error(
                f"[ROSHandler] Error task_handler: {error}"
            )
            agent_sentry(error, "[ROSHandler] Error task_handler")

    def task_cancellation_handler(self, goal_id, vehicle):
        """Handles task cancellation info to specific robot"""
        vehicle_position = self.check_fleet_get_vehicle_position(vehicle)
        self.agent.log_info(
            f"[ROSHandler] Cancelling task with of vehicle: {self.agent.vehicle_names[vehicle_position]} goal id: {goal_id}")

        # if cancellation is received cancel goal
        # Refresh variables (it has to be before the cancel_goal so the path stops being sent and there is no delay
        # for the traffic control)
        if self.agent.waypoints[vehicle_position]:
            # This line should be first to cancel the waypoints thread in ROS1
            self.agent.waypoints[vehicle_position] = False
            self.cancel_goal_waypoints(goal_id, vehicle_position)
        else:
            self.cancel_goal(goal_id, vehicle_position)

    def waypoints_handler(
            self, vehicle_position, pose, current_task_uuid
    ):
        """Handles offline waypoints and sends to specific robot"""
        # ROS2
        try:
            self.agent.waypoints[vehicle_position] = True
            self.send_waypoints(pose, vehicle_position)
        except KeyError as error:
            self.agent.log_error(
                f"[ROSHandler] Error waypoints_handler:{error}"
            )

            agent_sentry(error, "[ROSHandler] Error waypoints_handler")

    # def get_list_of_topic():
    #    """Getting the list of topics available with specified namespace"""
    #    # getting  topics available
    #    topic_list = rospy.get_published_topics(namespace="/robot1")
    #    return topic_list

    def topic_request_handler(self, _):
        """logging information"""
        self.agent.log_info("[ROSHandler] Received topic request")
        # get_list_of_topic()

    def close_handler(self, *_):
        """Close the websocket"""
        self.agent.log_info("[ROSHandler] WS close for Agent")
        self.agent.ws_open = False
        capture_message("[ROSHandler] WS close for Agent")

    def error_handler(self, _, err):
        """verifies websocket connection"""
        if not self.agent.connection.offline_agent.offline:
            self.agent.log_error(f"[ROSHandler] WS error {err}")
            capture_message("[ROSHandler] WS error")

    def open_handler(self, *_, **__):
        """Opens the websocket connection"""
        self.agent.log_info("[ROSHandler] WS open")
        self.agent.ws_open = True

    def path_rerouting_handler(self, _, data: dict, vehicle: str):
        vehicle_position = self.check_fleet_get_vehicle_position(vehicle)
        
        if data["path"] is not None:
            self.agent.pause_paths[vehicle_position] = True
            self.agent.log_info(f"[ROSHandler] Path Rerouting vehicle: {self.agent.vehicle_names[vehicle_position]}")
            self.agent.goal_id_rerouted[vehicle_position] = self.agent.goal_id[vehicle_position]
            self.task_cancellation_handler(goal_id=self.agent.goal_id_rerouted[vehicle_position], vehicle=vehicle)

            data_new_path = {"rotation_angles": data["rotation_angles"], "metric_waypoints": data["path"]}
            current_task_uuid = "Rerouted_task"

            pose = parse_waypoints(data_new_path)
            self.agent.waypoints[vehicle_position] = True # To Test
            self.waypoints_handler(
                vehicle_position=vehicle_position,
                pose=pose,
                current_task_uuid=current_task_uuid,
            )
        else:
            self.agent.log_error("[ROSHandler] Received empty path from path rerouting message.No action is done.")

    def docking_routine_finalize_handler(self, data: dict, vehicle: str):
        self.agent.log_info("[ROSHandler] Docking Routine FINALIZING request")
        vehicle_position = self.check_fleet_get_vehicle_position(vehicle)

        try:
            vehicle = self.agent.vehicles[vehicle_position]
            vehicle_prefix = str(vehicle["prefix"])
            if vehicle_prefix == "None":
                vehicle_prefix = ""

            pub = self.end_recording_publisher(vehicle_prefix)

            for i in range(10):
                variable = Bool()
                variable.data = False
                pub.publish(variable)
                time.sleep(1)
            self.agent.log_info("[ROSHandler] Published end of recording")

            self.client[vehicle_position].wait_for_result()
            result = self.client[vehicle_position].get_result()

            if result is not None:
                # rospy.loginfo(f"[ROSHandler] Result {result}")
                path, rotation_angles = parse_docking_routine(result.plan)
                self.agent.ping_docking_routine(vehicle["uuid"], path, rotation_angles)
            else:
                self.agent.log_error(f"[ROSHandler] Docking output is None. Try again.")
        except Exception as e:
            self.agent.log_error(f"[ROSHandler] Error on Docking Routine Finalize: {e}")

    def slow_down_handler(self, _, data: dict, vehicle: str):
        # Method should be written in the particular ROS Handler
        pass

    def docking_routine_request_handler(self, data: dict, vehicle: str):
        # Method should be written in the particular ROS Handler
        pass

    def collision_clearance_handler(self, data: dict, vehicle: str):
        # Method should be written in the particular ROS Handler
        pass
