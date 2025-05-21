The HackAtari Environments
==============================

HackAtari is an object-centric extension of the Atari Learning Environment (ALE), built on top of OCAtari. It enables custom environment modifications and dynamic reward functions for Atari games in research and experimentation.

.. module:: hackatari.core
.. autoclass:: HackAtari
    :show-inheritance:
    
Example
~~~~~~~~~~

    .. code-block:: python
        :caption: Create an HackAtari env and play random moves
        :linenos:

        # Create an HackAtari environment with ram-based object detection and DQN-like observation
        env = HackAtari(env_name="ALE/Pong-v5", mode="ram", obs_mode="dqn")

        # Interact with the environment
        obs = env.reset()
        done = False
        while not done:
            action = env.action_space.sample()  # Sample a random action
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated

            # Render the environment with object overlays
            env.render()

HackAtari (Methods)
~~~~~~~~~~

.. automethod:: hackatari.core.HackAtari.__init__
.. automethod:: hackatari.core.HackAtari.reset
.. automethod:: hackatari.core.HackAtari.step
.. autoattribute:: hackatari.core.HackAtari.available_modifications

HackAtari (HumanPlayable)
~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: hackatari.core.HumanPlayable.__init__
.. automethod:: hackatari.core.HumanPlayable.run
