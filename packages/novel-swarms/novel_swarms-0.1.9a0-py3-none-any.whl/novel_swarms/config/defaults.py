from ..behavior.AngularMomentum import AngularMomentumBehavior
from ..behavior.AverageSpeed import AverageSpeedBehavior
from ..behavior.GroupRotationBehavior import GroupRotationBehavior
from ..behavior.RadialVariance import RadialVarianceBehavior
from ..behavior.ScatterBehavior import ScatterBehavior
from .AgentConfig import DiffDriveAgentConfig
from .ResultsConfig import ResultsConfig
from .WorldConfig import RectangularWorldConfig
from ..sensors.BinaryFOVSensor import BinaryFOVSensor
from ..sensors.BinaryLOSSensor import BinaryLOSSensor
from ..sensors.SensorSet import SensorSet


class ConfigurationDefaults:

    SIMPLE_SENSOR = SensorSet([
        BinaryLOSSensor(angle=0),
    ])

    FOV_LOS_SENSOR = SensorSet([
        BinaryFOVSensor(theta=14 / 2, distance=200, degrees=True)
    ])

    DIFF_DRIVE_AGENT = DiffDriveAgentConfig(
        sensors=SIMPLE_SENSOR,
    )

    FOV_DIFF_DRIVE_AGENT = DiffDriveAgentConfig(
        sensors=FOV_LOS_SENSOR,
    )

    BEHAVIOR_VECTOR = [
        AverageSpeedBehavior(),
        AngularMomentumBehavior(),
        RadialVarianceBehavior(),
        ScatterBehavior(),
        GroupRotationBehavior(),
    ]

    RECTANGULAR_WORLD = RectangularWorldConfig(
        size=(500, 500),
        n_agents=30,
        behavior=BEHAVIOR_VECTOR,
        padding=15
    )

    RESULTS = ResultsConfig(
        k_clusters=10,
        display_trends=False
    )

    FLOCKBOT_SENSOR_SET = SensorSet([
        BinaryFOVSensor(
            theta=14 / 2,
            distance=(15.1 * 13.25),
            bias=4,
            degrees=True,
            false_positive=0.1,
            false_negative=0.05,
            # Rectangle Representing Environment Boundaries
            walls=None,
            wall_sensing_range=(15.1 * 4),
            time_step_between_sensing=1,
            goal_sensing_range=(15.1 * 29.13),
            detect_goal_with_added_state=True,
        )
    ],
        custom_state_decision="Linear")