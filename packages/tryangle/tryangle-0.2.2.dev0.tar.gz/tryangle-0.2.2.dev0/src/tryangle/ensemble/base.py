# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import numpy as np
from chainladder.workflow.voting import _BaseTriangleEnsemble
from sklearn.base import clone
from sklearn.ensemble._base import _fit_single_estimator
from sklearn.utils.validation import _deprecate_positional_args
from tryangle.ensemble.optimizers import Adam
from tryangle.metrics.base import get_expected
from tryangle.ensemble.losses import LOSS_FUNCTIONS


class AutoEnsemble(_BaseTriangleEnsemble):
    """Automated ensembling of chainladder methods

    `AutoEnsemble` uses a neural network to find optimal weights
    to ensemble multiple chainladder methods.

    Read more in the :ref:`User Guide <autoensemble>`

    .. versionadded:: 0.1.0

    Parameters
    ----------
    estimators : list of (str, estimator) tuples
        Invoking the ``fit`` method on the ``AutoEnsemble`` will fit clones
        of those original estimators across the cv folds of the triangle and
        store the expected incremental claims for the next diagonal for each
        of the folds.

    cv : `TriangleSplit` cross-validation generator
        Determines the number of cross-validation folds
        over which to fit. Must be an instance of `TriangleSplit`

        Refer :ref:`User Guide <cross_validation>`

    max_iter : int, default=1000
        Maximum number of iterations (or epochs) used to train the neural
        network. Currently the optimizers use all iterations.

    optimizer : optimizer object, default=Adam()
        The optimization method to find optimal weights and biases.

    initial_weight : ndarray of shape (1, num_estimators), default=None
        Force the initial weights instead of using a random initialization

    initial_bias : ndarray of shape (1, num_estimators), default=None
        Force the initial biases instead of using a random initialization

    weight_function : 'linear', 'poly(n)', or None, default='linear'
        Specify a function to constrain the voting weights.
        ``poly(n)`` will fit an n-term polynomial:
        t^n * w + t^(n-1) * w + ... + t^(2) * w + t * w + b
        where t is the origin period, w is the weight, and b is the bias
        ``linear`` is equivalent to ``poly(1)``
        ``None`` will not constrain the weights meaning each origin period
        will have its own vector of weights.

    random_state : int or None, default=None
        Specify the seed for random weight and bias initialization.

    n_jobs : int, default=None
        Number of jobs to run in parallel
        ``None`` means 1.
        ``-1`` means using all processors.
        Currently only the compilation step is run in parallel. Optimization
        is not.

    verbose : int, default=False
        Controls the verbosity: the higher, the more messages.

    dropout : float, default=False
        Randomly sets incremental claim amounts equal to 0 equivalently for
        actual and expected. That is, the same incremental claims set to
        zero for actual are set to zero for expected. Parameter is given as
        a proportion of number of incremental claims data points.

    broad_dropout : float, default=False
        Randomly sets entire folds to zero equivalently for actual and expected.
        Parameter is given as a proportion of the number of folds and rounded to
        the nearest integer.

    Attributes
    ----------

    actual_ : ndarray
        The actual incremental claims for each fold.

    expected_ : ndarray
        The expected incremental claims for each estimator for each fold.

    weights_ : ndarray
        The optimal weights found to ensemble the estimators.

    Notes
    -----

    ``AutoEnsemble`` is still experimental and may change with future versions.
    """

    @_deprecate_positional_args
    def __init__(
        self,
        estimators,
        cv,
        max_iter=1000,
        optimizer=Adam(),
        initial_weight=None,
        initial_bias=None,
        weight_function="linear",
        loss="mse",
        random_state=None,
        n_jobs=None,
        verbose=False,
        dropout=False,
        broad_dropout=False,
    ):
        self.estimators = estimators
        self.cv = cv
        self.max_iter = max_iter
        self.optimizer = optimizer
        self.initial_weight = initial_weight
        self.initial_bias = initial_bias
        self.weight_function = weight_function
        self.loss = loss
        self.random_state = random_state
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.dropout = dropout
        self.broad_dropout = broad_dropout

    def _log_message(self, name, idx, total):
        if self.verbose < 2:
            return None
        return "(%d of %d) Processing %s" % (idx, total, name)

    def initialize_weights(self):
        if self.weight_function is None:
            weight_dim = self.origin_dim
        elif self.weight_function == "linear":
            weight_dim = 1
        elif "poly" in self.weight_function:
            self.weight_polynomial = int(
                self.weight_function[
                    self.weight_function.find("(") + 1 : self.weight_function.find(")")
                ]
            )
            weight_dim = 1
        else:
            raise Exception(
                "Unknown weight function provided. Options are None, linear, or poly(n)."
            )

        if self.initial_weight is None:
            np.random.seed(self.random_state)
            self.weights = np.random.normal(
                0,
                np.sqrt(2 / (2 * len(self.estimators))),
                size=(weight_dim, len(self.estimators)),
            )
        else:
            self.weights = self.initial_weight
        if self.initial_bias is None:
            np.random.seed(self.random_state)
            self.biases = np.zeros((weight_dim, len(self.estimators)))
        else:
            self.biases = self.initial_bias

    def preprocess(self, X, y=None, sample_weight=None):
        """
        In order to find optimal weights, the actual incremental claims
        and expected incremental claims for each estimator is required.
        This method also returns the `t` array.
        """

        names, clfs = self._validate_estimators()

        actual = X.latest_diagonal.to_frame().fillna(0).to_numpy()[:-1]
        actual = actual[np.newaxis, ...]
        expected = np.array(
            [
                get_expected(
                    _fit_single_estimator(
                        clone(clf),
                        X,
                        X,
                        sample_weight=None,
                        message_clsname=f"Preprocessing - {names[idx]}_expected",
                        message=self._log_message(names[idx], idx + 1, len(clfs)),
                    ),
                    X,
                )
                for idx, clf in enumerate(clfs)
            ]
        )

        t = (
            np.arange(1, actual.shape[1] + 1).reshape(-1, 1)[np.newaxis, ...]
            / actual.shape[1]
        )

        return actual, expected, t

    def compile(self, X, y=None, sample_weight=None):
        """
        Obtain the actual, expected, and t, arrays for each estimator
        for each fold and reshape for input to the neural network.
        """
        # Fit individual estimators
        if self.verbose > 1:
            print("\n[Compiling]\n")

        names, clfs = self._validate_estimators()

        self.actual_ = []
        self.expected_ = []

        # Preprocessing for each fold
        for fold, (train, _) in enumerate(self.cv.split(X)):

            zeros_to_pad = self.cv.n_splits - fold

            fold_actual, fold_expected, _ = self.preprocess(X[train])

            # Pad actuals to have same shape
            fold_actual = np.pad(
                fold_actual,
                [
                    [0, 0],
                    [zeros_to_pad, 0],
                    [0, 0],
                ],
            )

            self.actual_.append(fold_actual)

            # Pad expecteds to have same shape
            fold_expected = np.pad(
                fold_expected,
                [
                    [0, 0],
                    [zeros_to_pad, 0],
                    [0, 0],
                ],
            )

            self.expected_.append(fold_expected)

        self.actual_ = np.concatenate(self.actual_, axis=0)
        self.expected_ = np.concatenate(self.expected_, axis=2).T
        self.t_ = (
            np.repeat(
                np.arange(1, self.actual_.shape[1] + 1).reshape(-1, 1)[np.newaxis, ...],
                self.cv.n_splits,
                axis=0,
            )
            / self.actual_.shape[1]
        )
        self._output = np.zeros(self.actual_.shape)
        self.origin_dim = self.actual_.shape[1]

        if self.verbose:
            print()

        return self

    def _softmax(self, x):
        return np.exp(x) / np.exp(x).sum(axis=2, keepdims=True)

    def _softmax_gradient(self, x):
        identity = np.repeat(
            np.repeat(np.eye(x.shape[2])[np.newaxis, ...], x.shape[1], axis=0)[
                np.newaxis, ...
            ],
            x.shape[0],
            axis=0,
        )
        lhs_jacobian = identity * self._softmax(x)[..., np.newaxis]
        rhs_jacobian = np.einsum("fij,kif->fijk", self._softmax(x), self._softmax(x).T)
        return lhs_jacobian - rhs_jacobian

    def dense(self, t):
        if self.weight_function is None:
            return t * self.weights + self.biases
        elif self.weight_function == "linear":
            return np.matmul(t, self.weights) + self.biases
        elif self.weight_function[:4] == "poly":
            return (
                sum(
                    [t ** (n + 1) * self.weights for n in range(self.weight_polynomial)]
                )
                + self.biases
            )
        else:
            raise Exception(
                "Unknown weight function provided. Options are None, linear, or poly(n)."
            )

    def _dense_gradient(self, t):
        if self.weight_function is None:
            return t
        elif self.weight_function == "linear":
            return t
        elif self.weight_function[:4] == "poly":
            return sum([(n + 1) * t ** (n) for n in range(self.weight_polynomial)])
        else:
            raise Exception(
                "Unknown weight function provided. Options are None, linear, or poly(n)."
            )

    def activation(self, x):
        return self._softmax(x)

    def output(self, expected, activation):
        return (expected * activation).sum(axis=2, keepdims=True)

    def compute_loss(self, output, actual):
        return self.Loss()._loss(output, actual)

    def forward_pass(self, actual, expected, t, text_file=None):
        if self.verbose > 2:
            print("Starting weights: ", self.weights, " ", self.biases, file=text_file)
        self._dense = self.dense(t)
        self._activation = self.activation(self._dense)
        self._output = self.output(expected, self._activation)
        self._compute_loss = self.compute_loss(self._output, actual)
        if self.verbose > 2:
            print("Loss: ", self._compute_loss, file=text_file)

        return self

    def backward_pass(self, actual, expected, t, epoch, text_file):
        dLdy = self.Loss()._loss_gradient(self._output, actual)
        dyds = expected
        dsdd = self._softmax_gradient(self._dense)
        dddw = self._dense_gradient(t)
        dddb = np.ones(t.shape)

        dLdd = np.einsum("fkij,fkj->fki", dsdd, dLdy * dyds)

        self._w_grad = (dLdd * dddw).mean(axis=(0, 1))
        self._b_grad = (dLdd * dddb).mean(axis=(0, 1))

        self.optimizer.pre_update_params(epoch)
        self.optimizer.update_params(self, epoch)

        if self.verbose > 2:
            print(
                "[EPOCH: ",
                epoch,
                "]: cust_w_grad: ",
                self._w_grad,
                ", cust_b_grad: ",
                self._b_grad,
                file=text_file,
            )

        return self

    def _log_epoch(self, epoch):
        if not epoch % 10:
            print(
                f"[Epoch {epoch}/{self.max_iter}] "
                + f"loss: {self._loss:.4f} "
                + f"lr: {self.optimizer._learning_rate:.8f}"
            )

    def fit(self, X, y=None, sample_weight=None, loss="mse", text_file=None):

        self.compile(X, y, sample_weight)
        self.Loss = LOSS_FUNCTIONS[self.loss]

        if self.verbose:
            print("[Training]\n")

        num_folds = self.actual_.shape[0]

        weights = []
        biases = []
        eval_losses = []

        for p in range(num_folds):

            actual_train = np.delete(self.actual_, p, axis=0)
            expected_train = np.delete(self.expected_, p, axis=0)
            t_train = np.delete(self.t_, p, axis=0)

            actual_test = self.actual_[np.newaxis, p, :, :]
            expected_test = self.expected_[np.newaxis, p, :, :]
            t_test = self.t_[np.newaxis, p, :, :]

            self.initialize_weights()
            self.optimizer.reset(self)

            for epoch in range(self.max_iter + 1):
                _actual_train = actual_train
                _expected_train = expected_train
                _t_train = t_train

                if self.dropout:
                    drop_mask = np.ones_like(
                        _actual_train.reshape(-1, _actual_train.shape[-1])
                    )
                    choices = list(range(drop_mask.shape[0]))
                    drop_idx = np.random.choice(
                        choices, int(len(choices) * self.dropout)
                    )
                    drop_mask[drop_idx] = 0
                    drop_mask = drop_mask.reshape(_actual_train.shape)

                    _actual_train = _actual_train * drop_mask
                    _expected_train = _expected_train * drop_mask

                if self.broad_dropout:
                    choices = list(range(_actual_train.shape[0]))
                    drop_idx = np.random.choice(
                        choices, int(len(choices) * self.broad_dropout)
                    )
                    drop_mask = np.ones_like(_actual_train)
                    drop_mask[drop_idx, :, :] = 0

                    _actual_train = _actual_train * drop_mask
                    _expected_train = _expected_train * drop_mask

                self.forward_pass(_actual_train, _expected_train, _t_train, text_file)
                self.backward_pass(
                    _actual_train, _expected_train, _t_train, epoch, text_file
                )

                if self.verbose:
                    self._log_epoch(epoch)

            weights.append(self.weights)
            biases.append(self.biases)

            eval_loss = self.compute_loss(
                self._predict(expected_test, t_test), actual_test
            )
            eval_loss = eval_loss / actual_test.mean()
            eval_losses.append(eval_loss)

        self.weights = np.average(np.stack(weights, axis=1), axis=1)
        self.biases = np.average(np.stack(biases, axis=1), axis=1)

        self.weights_ = self._activation[-1]

        print()
        if self.verbose:
            print("\n")

        return self

    def _predict(self, expected, t):
        dense = self.dense(t)
        activation = self.activation(dense)
        output = self.output(expected, activation)
        return output

    def predict(self, X, y=None, sample_weight=None):
        _, expected, t = self.preprocess(X, y, sample_weight)
        return self._predict(expected, t)

    def evaluate(self, X, y=None, sample_weight=None):
        actual, expected, t = self.preprocess(X, y, sample_weight)
        output = self._predict(expected, t)
        return self.compute_loss(output, actual)
