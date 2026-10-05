from __future__ import annotations

from typing import List

from src.models import CarPose, Cone, Path2D


class PathPlanning:
    """Student-implemented path planner.

    You are given the car pose and an array of detected cones, each cone with (x, y, color)
    where color is 0 for yellow (right side) and 1 for blue (left side). The goal is to
    generate a sequence of path points that the car should follow.

    Implement ONLY the generatePath function.
    """

    def __init__(self, car_pose: CarPose, cones: List[Cone]):
        self.car_pose = car_pose
        self.cones = cones

    def generatePath(self) -> Path2D:
        """Return a list of path points (x, y) in world frame.

        Requirements and notes:
        - Cones: color==0 (yellow) are on the RIGHT of the track; color==1 (blue) are on the LEFT.
        - You may be given 2, 1, or 0 cones on each side.
        - Use the car pose (x, y, yaw) to seed your path direction if needed.
        - Return a drivable path that stays between left (blue) and right (yellow) cones.
        - The returned path will be visualized by PathTester.

        The path can contain as many points as you like, but it should be between 5-10 meters,
        with a step size <= 0.5. Units are meters.

        Replace the placeholder implementation below with your algorithm.
        """

        
         
     
       
        
        import math

        path: Path2D = []

        
        yellow_cones = [c for c in self.cones if c.color == 0]
        blue_cones = [c for c in self.cones if c.color == 1]

        
        if not yellow_cones and not blue_cones:
            num_points = 20
            step = 0.5
            cx, cy = self.car_pose.x, self.car_pose.y
            for i in range(1, num_points + 1):
                dx = math.cos(self.car_pose.yaw) * step * i
                dy = math.sin(self.car_pose.yaw) * step * i
                path.append((cx + dx, cy + dy))
            return path

       
        track_width = 2.0

        if len(yellow_cones) == 0 and len(blue_cones) > 0:
            for b in blue_cones:
                vx = b.x + track_width * math.sin(self.car_pose.yaw)
                vy = b.y - track_width * math.cos(self.car_pose.yaw)
                yellow_cones.append(Cone(x=vx, y=vy, color=0))

        elif len(blue_cones) == 0 and len(yellow_cones) > 0:
            for y in yellow_cones:
                vx = y.x - track_width * math.sin(self.car_pose.yaw)
                vy = y.y + track_width * math.cos(self.car_pose.yaw)
                blue_cones.append(Cone(x=vx, y=vy, color=1))

       
        mid_points = []
        for b in blue_cones:
            closest_y = min(yellow_cones, key=lambda y: math.hypot(b.x - y.x, b.y - y.y))
            mid_x = (b.x + closest_y.x) / 2.0
            mid_y = (b.y + closest_y.y) / 2.0
            mid_points.append((mid_x, mid_y))

      
        mid_points.sort(key=lambda p: math.hypot(p[0] - self.car_pose.x, p[1] - self.car_pose.y))

        
        waypoints = [(self.car_pose.x, self.car_pose.y)] + mid_points

        for k in range(len(waypoints) - 1):
            p1 = waypoints[k]
            p2 = waypoints[k + 1]
            dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
            steps = max(int(dist / 0.3), 5)
            for i in range(steps):
                t = i / steps
                px = p1[0] + t * (p2[0] - p1[0])
                py = p1[1] + t * (p2[1] - p1[1])
                path.append((px, py))

        
        path.append(mid_points[-1])

       
        if len(waypoints) >= 2:
            last_p = waypoints[-1]
            prev_p = waypoints[-2]
            dx = last_p[0] - prev_p[0]
            dy = last_p[1] - prev_p[1]
            norm = math.hypot(dx, dy) or 1.0
            step_x, step_y = (dx / norm) * 0.3, (dy / norm) * 0.3
            for i in range(1, 10):
                path.append((last_p[0] + step_x * i, last_p[1] + step_y * i))

        return path

 """الكود هيبدأ بانه يشوف مثلا هل فيه اصلا اقماع او لاء ؟ لو لاء لو مفيش هيكمل قدام عادى
   طب لو لقى اقماع عنده مش كامله (هبدا بالسيناريو بتاع بارت 2 عشان بارت 1 اسهل فى الحل)
   فى العاده لما يكون فيه كيرف بيبقى فيه عدد اقماع الى من القوس من بره اكتر من الى من جوه او حتى لو مفيش كيرف فيه
   missions عدد الاقماع بتبقى مش متساويه اصلا او ناقصه
   فهو هيعمل اقماع وهميه قصاد القمع الى موجود بعرض = الطريق الى شايفه
   حاجه زى ال mirroring y3ni 
   و بعدين بيرجع لفكره بارت 1 انه يحسب المنتصف عن طريق القانون العادى بتاع نقطه المنتصف """
       