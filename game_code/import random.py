import numpy as np
from game_simulation import simulation
import matplotlib.pyplot as plt



# Number of samples
N = 100
# Proportion of best samples to select
rho = 0.1
# Number of iterations
iterations = 100
# Number of games to play to compute the learning curve
num_games = 30

# Initialize the parameter vector w to zero
w = np.zeros(21)
# Initialize the covariance matrix Sigma to 100 * I
Sigma = 100 * np.eye(21)

learning_curve = []

for t in range(iterations):
    # Generate samples from the current Gaussian distribution
    samples = np.random.multivariate_normal(w, Sigma, N)
    
    # Evaluate each sample with the score function (game simulation)
    scores = np.array([simulation(sample) for sample in samples])
    
    # Sort samples based on their score and select the best ones
    best_samples_indices = np.argsort(scores)[-int(N * rho):]
    best_samples = samples[best_samples_indices]
    
    # Update w with the empirical mean of the selected best samples
    w = np.mean(best_samples, axis=0)
    
    # Update Sigma with the empirical covariance of the selected best samples
    Sigma = np.cov(best_samples, rowvar=False)

    # Compute the learning curve with the mean weights of the new distribution
    # Play num_games games with these mean weights and record the scores
    game_scores = [simulation(w) for _ in range(num_games)]
    learning_curve.append(np.mean(game_scores))

    # Print the average score of the best samples at each iteration
    print("Iteration {}: Average score of best samples: {}".format(t+1, np.mean(scores[best_samples_indices])))

# Plot the learning curve
plt.plot(range(1, iterations+1), learning_curve, marker='o')
plt.xlabel('Iteration')
plt.ylabel('Average Score')
plt.title('Learning Curve')
plt.grid(True)
plt.show()
