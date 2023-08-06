import scipy.stats as stats

from popsynth.auxiliary_sampler import AuxiliarySampler, AuxiliaryParameter


class NormalAuxSampler(AuxiliarySampler):
    _auxiliary_sampler_name = "NormalAuxSampler"

    mu = AuxiliaryParameter(default=0)
    tau = AuxiliaryParameter(default=1, vmin=0)
    sigma = AuxiliaryParameter(default=1, vmin=0)

    def __init__(self, name: str, observed: bool = True):
        """
        A normal distribution sampler

        :param name: 
        :type name: str
        :param observed: 
        :type observed: bool
        :returns: 

        """
    
        super(NormalAuxSampler, self).__init__(name=name, observed=observed)

    def true_sampler(self, size: int):

        self._true_values = stats.norm.rvs(loc=self.mu,
                                           scale=self.tau,
                                           size=size)

    def observation_sampler(self, size: int):

        if self._is_observed:

            self._obs_values = stats.norm.rvs(loc=self._true_values,
                                              scale=self.sigma,
                                              size=size)

        else:

            self._obs_values = self._true_values
