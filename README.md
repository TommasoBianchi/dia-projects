# dia-projects

This repository contains the code for the projects of the 2019 Data Intelligence Applications course at Politecnico di Milano. The projects aim at understanding how to apply learning algorithms in different online optimization problems.

## Matching - Brief

1. Imagine a matching service on the Internet. Provide a brief description.

2. Imagine several (from 4 to 6) classes of users such that, given every pair of classes C1 and C2 and every pair of individuals x1 of C1 and x2 of C2, the weights on the edges (x1, x2) are the same. The (directed) graph among the individuals/classes can be arbitrary or bipartite. Provide a description of the classes. Suppose that every round corresponds to 120 minutes. For every class, define: the rate with which a new individual of that class enters the problem (described by a distribution probability on the number of users nor the next round that varies during the day according to different phases) and the maximum time to stay in the market (described by a distribution probability on the number of rounds, also here assume to have daily phases). For every pair of classes define: the weight as the product of a known constant and an unknown Bernoulli random variable (also here assume to have daily phases). Typically, the Bernoulli variable describes the failure of the success of the matching. For simplicity, assume that the phases are the same for all the probability distributions (i.e., rate, maximum time to stay in the market, failure probability) and assume that they are four, each at least 4 hours long.

3. Apply to that matching problem the following algorithms (they require the implementation the Edmonds algorithm and of the Postponed Dynamic Deferred Acceptance): combinatorial bandit with UCB1 (in stationary fashion), combinatorial bandit with TS (in stationary fashion).  Plot the regret of the two algorithms along a period of 60 days (where each day is 24 hours long). The regret must be computed w.r.t. the performance of the Postponed Dynamic Deferred Acceptance in the case in which the mean of the probability distribution of the weights is known).

4. Suppose that, the first day of every week, an algorithm to identify contexts is used aiming at distinguishing different daily phases during which the weights are actually drawn from different probability distributions. In this process, you can exploit the information that every round is 120 minutes long and that every phase is at least 2 rounds long. Propose an algorithm that exhaustively enumerate all the possible combinations of features/values. Apply the following algorithms and show, in a plot, how the regret and the reward vary in time (also comparing the regret and the reward of these algorithms with those obtained when the algorithms are applied without context generation): UCB1, TS.

## Advertising - Brief

1. Choose a product to advertise by means of digital tools. Provide a brief description.

2. Imagine 5 advertising sub-campaigns. Imagine an average daily budget/clicks curve (providing, for every value of daily budget, the number of daily clicks) aggregating the curves of three different classes of users. Notice that, in order to define the curves, it is necessary the definition of probability distributions. Provide a description of the three classes of users. Note: the definition of the classes of the users must be done by introducing features and different values for the features (e.g., gender, interests, age).

3. Be given a cumulative daily budget constraint. Be also given a discretisation for the daily budget values. Apply the Combinatorial-GP-TS to the aggregate curve (we are implicitly assuming that the bidding is performed automatically by the advertising platform) and report how the regret varies in time.

4. Focus on a single sub-campaign. Report the the average regression error of the GP as the number of samples increases. The regression error is the maximum error among all the possible arms.

5. Suppose to apply, the first day of every week, an algorithm to identify contexts and, therefore, to disaggregate the curves if doing that is the best we can do. And, if such an algorithm suggests disaggregating the curve at time t, then, from t on, keep such curves disaggregate. In order to disaggregate the curve, it is necessary to reason on the features and the values of the features. Apply the Combinatorial-GP-TS algorithm and show, in a plot, how the regret and the reward vary in time (also comparing the regret and the reward of these algorithms with those obtained when the algorithms are applied to the aggregate curve).

## Contributors

* [Tommaso Bianchi](https://github.com/tommasobianchi)
* [Raffaele Bongo](https://github.com/filus95)
* [Pierpaolo Mancini](https://github.com/PierpaoloM01)
* [Giovanni Probo](https://github.com/GProbo)
