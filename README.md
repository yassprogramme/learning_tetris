
# Learning Tetris with Cross-Entropy Method and Simulated Annealing

### Project Overview
This project explores the application of optimization algorithms to learn Tetris Game .
We focus on two variations of the Cross-Entropy Method (CEM)—one with constant noise and another with decreasing noise—to understand how different noise strategies affect learning and optimization. Additionally, Simulated Annealing (SA) is implemented as a comparative method to gauge its effectiveness against the CEM strategies.

### Cross-Entropy Method Explained
The Cross-Entropy Method is an optimization algorithm that iteratively refines a probability model based on the performance of sample solutions. In this project, two distinct CEM strategies are used:
- **CEM with Constant Noise**: Maintains a fixed level of noise throughout the training process to encourage exploration.
- **CEM with Decreasing Noise**: Gradually reduces the noise level, aiming to stabilize the solution as it converges towards the optimum.
==> These noise variations are designed to prevent the algorithm from prematurely converging to suboptimal solutions, commonly known as local optima.

### Simulated Annealing
Simulated Annealing is inspired by the annealing process in metallurgy. This technique varies the probability of accepting worse solutions as it explores the solution space, which decreases over time in a manner similar to the cooling of metal.


### Performance Tracking
Our approach to assessing the effectiveness of each optimization method includes comprehensive performance metrics. We track the average score, the highest score achieved, and the computational efficiency . Additionally, we have implemented parallelization on the CPU to enhance the computational efficiency. This allows for simultaneous processing of multiple training instances, significantly speeding up the learning process. 


### References 

 **Szita, I., & Lőrincz, A. (2006). Learning Tetris Using the Noisy Cross-Entropy Method.**


