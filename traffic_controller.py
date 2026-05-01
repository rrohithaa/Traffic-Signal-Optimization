# =============================================================================
# ai_optimizer.py – Q-Learning traffic signal optimizer
# =============================================================================
# The agent observes a discretised density state for the active phase and
# chooses how many seconds of green to grant.  It learns off-policy using
# the standard Bellman update so it gradually minimises vehicle wait time.
#
# State  : tuple(density_primary, density_secondary)
#           where each density is bucketed into 0-4  (5 levels)
# Action : index into ACTIONS list (green-time duration in seconds)
# Reward : negative mean waiting time for vehicles that cleared the junction
#           this cycle  (higher throughput = less negative = better)
# =============================================================================

import os
import random
import numpy as np
from config import (
    ALPHA, GAMMA, EPSILON_START, EPSILON_MIN, EPSILON_DECAY,
    ACTIONS, Q_TABLE_PATH, MAX_DENSITY
)

# Number of density buckets per lane direction
N_BUCKETS = 5    # 0-1, 2-3, 4-5, 6-7, 8-10  (for MAX_DENSITY=10)


def _discretise(density: int) -> int:
    """Map a raw vehicle count to a bucket index [0, N_BUCKETS-1]."""
    step = max(1, MAX_DENSITY // N_BUCKETS)
    return min(N_BUCKETS - 1, density // step)


class QLearningAgent:
    """
    Tabular Q-Learning agent that decides green-signal durations.

    The Q-table is a numpy array of shape
        (N_BUCKETS, N_BUCKETS, len(ACTIONS))
    indexed as  Q[primary_bucket, secondary_bucket, action_index].
    """

    def __init__(self):
        self.n_actions = len(ACTIONS)
        self.epsilon   = EPSILON_START
        self._q        = self._load_or_init()
        self._prev_state  = None
        self._prev_action = None
        self.total_reward = 0.0
        self.step_count   = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def choose_action(self, primary_density: int, secondary_density: int) -> int:
        """
        ε-greedy policy: choose a green-time action index.

        Parameters
        ----------
        primary_density   : vehicle count on the lane ABOUT TO get green
        secondary_density : vehicle count on the opposing (waiting) lane

        Returns
        -------
        int  – index into ACTIONS list
        """
        state = self._state(primary_density, secondary_density)

        if random.random() < self.epsilon:
            action = random.randrange(self.n_actions)   # explore
        else:
            action = int(np.argmax(self._q[state]))      # exploit

        self._prev_state  = state
        self._prev_action = action
        return action

    def get_green_time(self, primary_density: int, secondary_density: int) -> int:
        """Return the actual green-time in seconds for this decision."""
        idx = self.choose_action(primary_density, secondary_density)
        return ACTIONS[idx]

    def learn(self, reward: float,
              next_primary: int, next_secondary: int):
        """
        Apply the Bellman update after observing a reward.

        Parameters
        ----------
        reward          : scalar reward signal (negative wait time)
        next_primary    : density on next primary lane
        next_secondary  : density on next secondary lane
        """
        if self._prev_state is None:
            return

        next_state  = self._state(next_primary, next_secondary)
        best_next   = float(np.max(self._q[next_state]))
        old_value   = self._q[self._prev_state][self._prev_action]

        # Q(s,a) ← Q(s,a) + α [ r + γ·max Q(s',·) − Q(s,a) ]
        self._q[self._prev_state][self._prev_action] = (
            old_value + ALPHA * (reward + GAMMA * best_next - old_value)
        )

        self.total_reward += reward
        self.step_count   += 1

        # Decay exploration rate
        self.epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)

    def save(self):
        """Persist the Q-table to disk."""
        os.makedirs(os.path.dirname(Q_TABLE_PATH), exist_ok=True)
        np.save(Q_TABLE_PATH, self._q)

    def load(self):
        """Reload Q-table from disk (if it exists)."""
        self._q = self._load_or_init()

    @property
    def average_reward(self) -> float:
        if self.step_count == 0:
            return 0.0
        return self.total_reward / self.step_count

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _state(self, primary: int, secondary: int) -> tuple:
        return (_discretise(primary), _discretise(secondary))

    def _load_or_init(self) -> np.ndarray:
        """Load an existing Q-table or create a zeroed one."""
        if os.path.exists(Q_TABLE_PATH):
            try:
                q = np.load(Q_TABLE_PATH)
                if q.shape == (N_BUCKETS, N_BUCKETS, len(ACTIONS)):
                    return q
            except Exception:
                pass
        # Initialise with small random values to break symmetry
        return np.random.uniform(low=-0.01, high=0.01,
                                  size=(N_BUCKETS, N_BUCKETS, len(ACTIONS)))
