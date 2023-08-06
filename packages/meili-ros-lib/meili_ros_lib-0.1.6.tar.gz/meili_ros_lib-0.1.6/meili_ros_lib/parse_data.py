from geometry_msgs.msg import PoseStamped, Twist
from meili_ros_lib.maths import quaternion_to_euler, euler_to_quaternion

import math


def rotation_setup(rotation):
    rotation_float = float(rotation)

    if float(rotation) > 180:
        rotation_float = -360 + float(rotation)
    elif float(rotation) == 180:
        rotation_float = -180

    # rotation_quaternion = {"qx": 0, "qy": 0, "qw": 0, "qz": 0}
    rotation_quaternion = euler_to_quaternion(0, 0, math.radians(rotation_float))

    return rotation_quaternion


def goal_setup(data):
    """Set up the goal with rotation, x and y"""
    x_meters = data["location"]["metric"]["x"]
    y_meters = data["location"]["metric"]["y"]
    try:
        rotation = data["location"]["rotation"]
    except KeyError:
        rotation = 0
    rotation_quaternion = rotation_setup(rotation)

    return x_meters, y_meters, rotation_quaternion


def parse_waypoints(data):
    pose = []
    rotation_angle = data["rotation_angles"]
    waypoints = data["metric_waypoints"]

    for index, waypoint in enumerate(waypoints):
        x = waypoint[0]
        y = waypoint[1]
        rotation = rotation_angle[index]
        pose.append([x, y, rotation])

    return pose


def parse_battery_data(msg):
    # creating dictionary for storing battery data
    battery_data = {}

    if hasattr(msg, "capacity"):
        battery_data["value"] = round(msg.capacity, 2)
        battery_data["power_supply_status"] = msg.power_supply_status
    elif hasattr(msg, "level"):
        battery_data["value"] = round(msg.level, 2)
        if msg.is_charging:
            battery_data["power_supply_status"] = 1
        else:
            battery_data["power_supply_status"] = 3
    elif hasattr(msg, "data"):
        battery_data["value"] = msg.data
        battery_data["power_supply_status"] = 3

    elif hasattr(msg, "rsoc"):
        battery_data["value"] = msg.rsoc
        battery_data["power_supply_status"] = 3

    return battery_data


def parse_vel(max_vel_x):
    # TO DO: get the current parameters and just change the linear.x
    vel = Twist()

    vel.linear.x = 0.0  # float(max_vel_x)
    vel.linear.y = 0.0
    vel.linear.z = 0.0

    vel.angular.x = 0.0
    vel.angular.y = 0.0
    vel.angular.z = 0.0

    return vel


def parse_docking_routine(result):
    path = [[pose.pose.position.x, pose.pose.position.y] for pose in result.poses]
    rotation_angles = [[round(quaternion_to_euler(
        pose.pose.orientation.x, pose.pose.orientation.y, pose.pose.orientation.z, pose.pose.orientation.w
    ), 3)] for pose in result.poses]

    return path, rotation_angles
