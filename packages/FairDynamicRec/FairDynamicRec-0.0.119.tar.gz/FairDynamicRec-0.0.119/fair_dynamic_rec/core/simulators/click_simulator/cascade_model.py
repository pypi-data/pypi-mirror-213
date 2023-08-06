import numpy as np
import math

class CascadeModel():
    name = 'CM'

    def __init__(self, config):
        # super(CascadeModel, self).__init__(*args, **kwargs)
        self.prng = np.random.RandomState(seed=config.seed)
        # assert np.linalg.norm(theta_star) <= 1.00001
        self.config = config
        self.coins = None
        self.coins_ready = False

    def set_coins(self, list_size):
        """
        -- call this, if you want to use the same coins for each positions each round
        -- set coins for each round.
        -- this should be called before get_feedback
        """
        self.coins = self.prng.rand(list_size)
        self.coins_ready = True

    def get_feedback(self, scores):
        # if type(delta) is list:
        #     delta = np.asarray(delta)
        # delta = np.tile(delta, (1, 1))
        # assert delta.shape[1] == self.theta.shape[0]

        # if not self.coins_ready:
        #     self.set_coins(self.config.list_size)
        #     self.del_coins()
        # score = np.dot(delta, self.theta)
        scores[scores > 1] = 1.
        # coins = score >= self.coins
        clicks, rewards = np.zeros((scores.shape)), np.zeros(scores.shape[0])
        n_users = scores.shape[0]
        for i in range(n_users):
            if not self.coins_ready:
                self.set_coins(self.config.list_size)
                self.del_coins()
            clicks[i] = scores[i] >= self.coins
            first_click = np.where(clicks[i])[0]
            if len(first_click) > 0:
                clicks[i][first_click[0]+1:] = False
            rewards[i] = sum(clicks[i])
        return clicks, rewards

    def del_coins(self):
        """
        This should be called by simulator at the end of each round.
        :return:
        """
        self.coins_ready = False

    def ave_feedback(self, delta):
        score = np.dot(delta, self.theta)
        score[score > 1] = 1.
        return 1 - np.prod(1-score)

class EACascadeModel():
    name = 'EACM'

    def __init__(self, config):
        # super(CascadeModel, self).__init__(*args, **kwargs)
        self.prng = np.random.RandomState(seed=config.seed)
        # assert np.linalg.norm(theta_star) <= 1.00001
        self.config = config
        self.coins = None
        self.coins_ready = False
        self.gamma = config.feedback_eacm_gamma

    def set_coins(self, list_size):
        """
        -- call this, if you want to use the same coins for each positions each round
        -- set coins for each round.
        -- this should be called before get_feedback
        """
        self.coins = self.prng.rand(list_size)
        self.coins_ready = True

    def get_feedback(self, scores):
        discount_coef_reward = [1. / math.log(1 + j, 2) for j in range(1, scores.shape[1] + 1)]
        discount_coef_penalization = [self.gamma * 1. / (math.log(1 + j, 2)) for j in range(1, scores.shape[1] + 1)]
        scores[scores > 1] = 1.
        clicks, rewards = np.zeros((scores.shape)), np.zeros(scores.shape[0])
        n_users = scores.shape[0]
        for i in range(n_users):
            if not self.coins_ready:
                self.set_coins(self.config.list_size)
                self.del_coins()
            clicks[i] = scores[i] >= self.coins
            first_click = np.where(clicks[i])[0]
            if len(first_click) > 0:
                clicks[i][first_click[0]+1:] = False
                rewards[i] = discount_coef_reward[first_click[0]] - sum(discount_coef_penalization[:first_click[0]])
            else:
                rewards[i] = -sum(discount_coef_penalization)
        return clicks, rewards

    def del_coins(self):
        """
        This should be called by simulator at the end of each round.
        :return:
        """
        self.coins_ready = False

    def ave_feedback(self, delta):
        score = np.dot(delta, self.theta)
        score[score > 1] = 1.
        return 1 - np.prod(1-score)