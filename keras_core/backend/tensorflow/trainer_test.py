import numpy as np

from keras_core import testing
from keras_core import layers
from keras_core import optimizers
from keras_core import losses
from keras_core.backend.tensorflow.trainer import TensorFlowTrainer


# A model is just a layer mixed in with a Trainer.
class TFModel(layers.Dense, TensorFlowTrainer):
    def __init__(self, units):
        layers.Dense.__init__(self, units=units)
        TensorFlowTrainer.__init__(self)


class TestTFTrainer(testing.TestCase):
    def _test_basic_flow(self, run_eagerly, jit_compile):
        model = TFModel(units=3)
        x = np.random.random((100, 4))
        y = np.random.random((100, 3))
        batch_size = 16
        epochs = 3

        model.compile(optimizer=optimizers.SGD(), loss=losses.MeanSquaredError(), run_eagerly=run_eagerly, jit_compile=jit_compile)
        model.fit(x, y, batch_size=batch_size, epochs=epochs)

    def test_basic_flow_eager(self):
        self._test_basic_flow(run_eagerly=True, jit_compile=False)

    def test_basic_flow_graph_fn(self):
        self._test_basic_flow(run_eagerly=False, jit_compile=False)

    def test_basic_flow_jit(self):
        self._test_basic_flow(run_eagerly=False, jit_compile=True)