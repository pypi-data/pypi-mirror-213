import numpy as np
from scipy.spatial.distance import cdist


class CovModel:
    def __init__(
        self,
        bandwidth_len: float,
        bandwidth_step: float,
        k_range: float,
        sill: float = 1,
        nugget: float = 0,
    ):
        self.__bandwidth_len = bandwidth_len
        self.__bandwidth_step = bandwidth_step
        self.__bandwidth = np.arange(0, bandwidth_len, bandwidth_step)
        self.__k_range = k_range
        self.__sill = sill
        self.__nugget = nugget

    @property
    def bandwidth_len(self) -> float:
        return self.__bandwidth_len

    @property
    def bandwidth_step(self) -> float:
        return self.__bandwidth_step

    @property
    def bandwidth(self) -> np.array:
        return self.__bandwidth

    @property
    def k_range(self) -> float:
        return self.__k_range

    @property
    def sill(self) -> float:
        return self.__sill

    @property
    def nugget(self) -> float:
        return self.__nugget

    def cov_compute(self, x: np.array) -> np.array:
        cov = np.empty(len(x))
        for i in range(len(x)):
            cov[i] = self.__sill - self.model(x[i])

        return cov

    def var_compute(self, x: np.array) -> np.array:
        var = np.empty(len(x))
        for i in range(len(x)):
            var[i] = self.model(x[i])

        return var

    def variogram(self, x: np.array) -> np.array:
        dist = cdist(x[:, :1], x[:, :1])
        variogram = []
        # variogram = np.zeros(len(self.__bandwidth))

        for idx, h in enumerate(self.__bandwidth):
            indices = np.where(
                (dist >= h - self.__bandwidth_step) & (dist <= h + self.__bandwidth_step),
            )
            z = np.power(x[indices[0], 1] - x[indices[1], 1], 2)
            z_sum = np.sum(z)
            if z_sum >= 1e-7:
                variogram.append(z_sum / (2 * len(z)))

        return np.array(variogram)
