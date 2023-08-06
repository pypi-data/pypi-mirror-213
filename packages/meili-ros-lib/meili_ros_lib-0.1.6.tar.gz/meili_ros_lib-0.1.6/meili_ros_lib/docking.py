from geometry_msgs.msg import PoseStamped


class DockingActionServer:
    def __init__(self, name):
        self.plan = None
        self.recording = None
        self.action_name = name

    def callback_pose(self, msg):

        if self.recording:
            pose = PoseStamped()
            pose.header = msg.header
            x_coord = round(msg.pose.pose.position.x, 2)
            y_coord = round(msg.pose.pose.position.y, 2)

            try:
                if len(self.plan.poses) != 0:
                    x_coord_prev = self.plan.poses[-1].pose.position.x
                    y_coord_prev = self.plan.poses[-1].pose.position.y
                else:
                    x_coord_prev = 0.0
                    y_coord_prev = 0.0

                if x_coord != x_coord_prev and y_coord != y_coord_prev:
                    pose.pose.position.x = x_coord
                    pose.pose.position.y = y_coord
                    pose.pose.orientation.x = msg.pose.pose.orientation.x
                    pose.pose.orientation.y = msg.pose.pose.orientation.y
                    pose.pose.orientation.z = msg.pose.pose.orientation.z
                    pose.pose.orientation.w = msg.pose.pose.orientation.w

                    self.plan.poses.append(pose)

            except Exception as e:
                self.log_info(f"[DockingServer] Error in callback pose: {e}")

    def callback_recording(self, msg):
        self.recording = msg.data
