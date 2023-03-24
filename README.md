## Brownian Motion Simulator
This program simulates (simplified) Brownian motion of particles moving in 2D space. Each particle is initiated with a random position and velocity. When a particle collides with the boundary of the arena, its angle changes randomly and speed remains the same. Collision between two particles are modeled as elastic collision.

Required packages: `numpy`, `matplotlib`
Usage:
```
example.py -f <GIF_FILENAME>
# e.g. example.py -f brownian.gif
``` 

[example of generated gif](example.gif)
