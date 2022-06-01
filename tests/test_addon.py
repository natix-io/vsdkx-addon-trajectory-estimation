import numpy as np
import unittest

from vsdkx.core.structs import AddonObject, Inference
from vsdkx.addon.trajectory_estimation.processor import TrajectoryProcessor
from vsdkx.addon.tracking.trackableobject import TrackableObject


class TestAddon(unittest.TestCase):
    addon_config = {
        "centroid_index": 2,
        "temporal_length": 10
    }

    model_config = {
        "filter_class_ids": [0]
    }

    def test_get_current_direction(self):
        addon_processor = TrajectoryProcessor(self.addon_config, {}, self.model_config, {})

        bb_1 = np.array([120, 150, 170, 200])
        c_1 = (145, 175)

        # ""
        trackable_object_1 = TrackableObject(0, c_1, bb_1)

        # up
        c_2 = (145, 170)
        up = TrackableObject(1, c_1, bb_1)
        up.centroids.extend([c_1, c_2])

        # down
        c_2 = (145, 180)
        down = TrackableObject(2, c_1, bb_1)
        down.centroids.extend([c_1, c_2])

        # left
        c_2 = (150, 175)
        left = TrackableObject(2, c_1, bb_1)
        left.centroids.extend([c_1, c_2])

        # right
        c_2 = (140, 175)
        right = TrackableObject(2, c_1, bb_1)
        right.centroids.extend([c_1, c_2])

        # downleft
        c_2 = (150, 180)
        downleft = TrackableObject(1, c_1, bb_1)
        downleft.centroids.extend([c_1, c_2])

        # downright
        c_2 = (140, 180)
        downright = TrackableObject(1, c_1, bb_1)
        downright.centroids.extend([c_1, c_2])

        # upleft
        c_2 = (150, 170)
        upleft = TrackableObject(1, c_1, bb_1)
        upleft.centroids.extend([c_1, c_2])

        # upright
        c_2 = (140, 170)
        upright = TrackableObject(1, c_1, bb_1)
        upright.centroids.extend([c_1, c_2])

        trackable_objects = {
            "0": trackable_object_1,
            "1": up,
            "2": down,
            "3": left,
            "4": right,
            "5": downleft,
            "6": downright,
            "7": upleft,
            "8": upright
        }

        addon_processor._get_current_direction(trackable_objects)

        self.assertEqual(trackable_object_1.direction, "")
        self.assertEqual(up.direction, "up")
        self.assertEqual(down.direction, "down")
        self.assertEqual(left.direction, "left")
        self.assertEqual(right.direction, "right")
        self.assertEqual(downleft.direction, "downleft")
        self.assertEqual(downright.direction, "downright")
        self.assertEqual(upleft.direction, "upleft")
        self.assertEqual(upright.direction, "upright")

    def test_post_process(self):
        addon_processor = TrajectoryProcessor(self.addon_config, {}, self.model_config, {})

        frame = (np.random.rand(640, 640, 3) * 100).astype('uint8')
        inference = Inference()

        bb_1 = np.array([120, 150, 170, 200])
        c_1 = (145, 175)

        trackable_object_1 = TrackableObject(0, c_1, bb_1)
        trackable_object_1.centroids.extend([c_1, c_1])

        shared = {
            "trackable_objects": {
                "0": trackable_object_1,
            },
            "trackable_objects_history": {
                "0": trackable_object_1,
            }
        }

        test_object = AddonObject(frame=frame, inference=inference, shared=shared)
        result = addon_processor.post_process(test_object)

        self.assertIn('movement_directions', result.inference.extra)
        self.assertIn('0', result.inference.extra['movement_directions'])


if __name__ == '__main__':
    unittest.main()
