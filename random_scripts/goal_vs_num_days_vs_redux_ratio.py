# current_goal_inf = (1 - r) * total / error_margin
# current_goal_non_inf = current_goal_inf / (1-r^(num_days+1))


# %%
from cmath import inf
from typing import Optional

# %%
# TOTAL = 14.88
TOTAL = 25
ERROR_MARGIN = 1


# %%
def current_goal(ratio: float, num_days: Optional[int] = None) -> float:
    inf_goal = (1 - ratio) * TOTAL / ERROR_MARGIN
    if num_days is None:
        return inf_goal
    return inf_goal / (1 - ratio ** (num_days + 1))


# %%
r = [ratio / 1000 for ratio in range(950, 990, 10)]
n = [25, 30]

days_to_print = [1, 5, 10, 15, 20, 25, 30]

# %%
for ratio in r:
    print("")
    print(f"ratio: {ratio:.4f}")
    for num_days in n:
        print(f"num days: {num_days}")
        goal = current_goal(ratio, num_days)
        for d in days_to_print:
            if d <= num_days:
                print(f"    {num_days}-{d:2}: {goal*ratio**(d-1):.4f}")
        print("")


# %%
for num_days in n:
    print("")
    print(f"num days: {num_days}")
    for ratio in r:
        print(f"ratio: {ratio:.4f}")
        goal = current_goal(ratio, num_days)
        for d in days_to_print:
            if d <= num_days:
                print(f"    {num_days}-{d:2}: {goal*ratio**(d-1):.3f}")
        print("")


# %%
for num_days in n:
    print("")
    print(f"num days: {num_days}")
    for ratio in r:
        goal = current_goal(ratio, num_days)
        print(f"ratio: {ratio:.3f}")
        # print(f"    goal:  {goal:.3f}")
        for d in days_to_print:
            if d <= num_days:
                print(f"    {num_days}-{d:2}: {goal*ratio**(d-1):.3f}")
        print("")
        # print(f"    goal for inf: {current_goal(ratio):.3f}")
        # print(
        #     f"    diff:        {current_goal(ratio) - current_goal(ratio, num_days):.3f}"
        # )
        # print(
        #     f"    pct:          {current_goal(ratio) / current_goal(ratio, num_days):.3f}"
        # )

# %%
# for ratio in r:
for ratio in [0.95]:
    print("")
    print(f"ratio: {ratio:.3f}")
    for num_days in n:
        # goal = current_goal(ratio, num_days)
        for d in days_to_print:
            if d <= num_days:
                print(f"    {num_days}-{d}: {goal*ratio**(d-1):.3f}")
        print("")
    # inf_goal = current_goal(ratio)
    # for d in days_to_print:
    #     print(f"    inf-{d}: {inf_goal*ratio**(d-1):.3f}")

# %%
for ratio in r:
    print(f"ratio: {ratio:.3f}")
    print(f"goal:  {current_goal(ratio):.3f}")
    print("")

# %%
