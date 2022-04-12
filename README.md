# Trajectory Estimation

This add-on calculates the direction of movement of trackable objects based on their past and present coordinates in the frame.

### Config

The class `TrajectoryProcessor` is initialized with the following config parameters:

```python
DEFAULT = {
    "centroid_index": 2,
    "temporal_length": 10
}
```

where:
- `centroid_index` (int): -nth centroid to compare with the current centroid. This comparison occurs when we don't have enough centroid datapoint as the `temporal_length` requires 
- `temporal_length` (int): The amount of centroid points to compare against the present centroid position.

### Input

The `post_process` gets as input the `AddonObject` and relies on the results of the `tracking` add-on set in:

- `AddonObject.shared['trackable_objects']` (format: `OrderedDict`)
- `AddonObject.shared['trackable_objects_history']` (format: `OrderedDict`)

**Direct dependency with the `tracking` add-on.**

### Process

After object detection and object tracking, the trajectory estimator receives the full history of `trackable_objects` from the `tracking` add-on. For every `trackable_object` we check its previous centroid positions from the past frames and estimate the object's direction of movement on the current frame.

We support the following directions format: 

```
'up', 'down', 'left', 'right', 'downleft', 'downright', 'upleft', 'upright' or '' if direction can't be set.
```

### Output

The add-on's output is shared on the `AddonObject.inference.extra` for each object that was actively tracked by the `tracking` add-on on the current frame:

- `AddonObject.inference.extra['movement_directions']` - (format: `dict` where `{'obj_id': direction}`)
