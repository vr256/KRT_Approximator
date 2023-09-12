import numpy as np
import tensorflow as tf

var = 0.4


class AdditiveModel(tf.keras.Model):
    def __init__(self, name, **kwargs):
        super().__init__(name)
        self.l2_reg = 0.1
        for key in kwargs:
            self.__dict__[key] = kwargs[key]

    def build(self, input_shape):
        # TODO add initializers
        c = [[0 for _ in range(len(self.dims) - 1)] for _ in range(self.dims[0])]
        a = [[0 for _ in range(len(self.dims) - 1)] for _ in range(self.dims[0])]
        lam = [
            [[0 for _ in range(self.dims[q + 1])] for q in range(len(self.dims) - 1)]
            for _ in range(self.dims[0])
        ]
        for y_component in range(self.dims[0]):
            for q in range(len(self.dims) - 1):
                c[y_component][q] = tf.Variable(
                    tf.random.normal(shape=(1,), stddev=var), dtype=tf.float32
                )
                a[y_component][q] = tf.Variable(
                    tf.random.normal(shape=(input_shape[q][0],), stddev=var),
                    dtype=tf.float32,
                )
                for p in range(self.dims[q + 1]):
                    lam[y_component][q][p] = tf.Variable(
                        tf.random.normal(shape=(input_shape[q][1],), stddev=var),
                        dtype=tf.float32,
                    )
        self.lam = lam
        self.a = a
        self.c = c

    def call(self, inputs):
        res = []
        for y_component in range(self.dims[0]):
            y_pred = 0
            for q in range(len(self.dims) - 1):
                for p, a_qp in enumerate(self.a[y_component][q]):
                    y_pred += (
                        self.c[y_component][q]
                        * a_qp
                        * tf.tensordot(
                            self.lam[y_component][q][p],
                            tf.convert_to_tensor(inputs[q][p], dtype=tf.float32),
                            axes=1,
                        )
                    )
            res.append(y_pred)
        return res

    def compile(self, optimizer=tf.optimizers.Adam):
        self.optimizer = optimizer()
        self.optimizer.build(self.trainable_variables)
        self.loss = tf.keras.losses.MeanSquaredError()

    def predict(self, inputs):
        res = []
        for q in range(len(inputs)):
            res.append([i.numpy().item() for i in self.call(inputs[q])])
        return np.array(res)

    # def evaluate(self, x, y, i):
    #     mse_loss = 0
    #     for q in range(len(x)):
    #         y_pred = self.call(x[q], i)
    #         mse_loss += tf.reduce_mean(tf.square(y[i] - y_pred))
    #     return mse_loss

    def fit(self, x, y, epochs=10, batch_size=10, to_print=False):
        # TODO add batch GD
        for epoch in range(epochs):
            epoch_loss = 0.0
            for i in range(len(x)):
                with tf.GradientTape() as tape:
                    y_pred = self.call(x[i])
                    batch_loss = self.loss(y[i], y_pred)  # regularization

                epoch_loss += batch_loss
                grad = tape.gradient(batch_loss, self.trainable_variables)
                self.optimizer.apply_gradients(zip(grad, self.trainable_variables))

            if to_print:
                print(f"Epoch: {epoch + 1}  Loss: {np.round(epoch_loss, 3):.3f}")
