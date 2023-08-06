from os import environ
from meili_ros_lib.sentry import agent_sentry
from numpy.distutils.fcompiler import str2bool


class Setup:
    def __init__(self):
        # Variables initialization
        self.aws_access_key_id = None
        self.aws_secret_access_key = None
        self.path_planning = None
        self.traffic_control = None
        self.battery_present = False
        self.lipo_battery = None
        self.outdoor = False
        self.topic_streaming_mode = None
        self.publish_frequency = None
        self.offline_flag = None

        # Logging
        self.log_info = None
        self.log_error = None

    def init_parameters_setup(self):
        try:

            if (
                    environ.get("AWS_ACCESS_KEY_ID") is not None
                    and environ.get("AWS_SECRET_ACCESS_KEY") is not None
            ):
                self.aws_access_key_id = environ.get("AWS_ACCESS_KEY_ID")
                self.aws_secret_access_key = environ.get("AWS_SECRET_ACCESS_KEY")
            else:
                self.aws_access_key_id = None
                self.aws_secret_access_key = None

            # get ROS distro
            ros_distro = environ["ROS_DISTRO"]
            ros_version = environ["ROS_VERSION"]

            self.log_info("[SetUp] Reading initialization parameters")
            self.log_info(f"[SetUp] Ros distro is : {ros_distro}")
            self.log_info(f"[SetUp] Ros version is :{ros_version}")

        except KeyError:
            self.log_error(f"[SetUp] Parameter {KeyError} does not exist. ")
            agent_sentry(KeyError)
            self.log_error("[SetUp] Roscore is not running, check your ros config")
            raise

        self.log_info(
            "[SetUp] COMPLETED Initial ROS Parameter configuration"
        )

        # get initial ros parameters
    def battery_parameter(self, battery):
        battery = str2bool(battery)
        if battery == "lipo":
            self.battery_present = True
            self.lipo_battery = True
            self.log_info("[SetUp] The Lipo battery is present")

        elif battery:
            self.battery_present = True
            self.log_info("[SetUp] The Battery is present")

