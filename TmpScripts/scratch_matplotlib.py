# %%
# bar plot where shorter bar is always in the front
import matplotlib.pyplot as plt
import pandas as pd

df2 = pd.DataFrame(
    {
        "Chapter Name": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "Time Completed": [50, 60, 70, 80, 75, 85, 90, 100, 95, 105],
        "Time Predicted TPW": [40, 65, 70, 75, 80, 85, 90, 95, 100, 105],
        "Goal Time": [72, 80, 55, 80, 80, 82, 85, 105, 75, 100],
    }
)

fig, ax = plt.subplots()
width = 0.35

for i, chapter in enumerate(df2["Chapter Name"]):
    completed = df2.loc[df2["Chapter Name"] == chapter, "Time Completed"].values[0]
    predicted = df2.loc[df2["Chapter Name"] == chapter, "Time Predicted TPW"].values[0]

    if completed < predicted:
        tc_zorder = 2
        tpw_zorder = 1
    else:
        tc_zorder = 1
        tpw_zorder = 2

    ax.bar(i, completed, width, label="Time Completed", color="C0", zorder=tc_zorder)
    ax.bar(
        i, predicted, width, label="Time Predicted TPW", color="C1", zorder=tpw_zorder
    )

ax.set_xticks(range(len(df2)))
ax.set_xticklabels(df2["Chapter Name"])
ax.legend(["Time Completed", "Time Predicted TPW"])
plt.show()


# %%
# scatter plot

# %%
import matplotlib.pyplot as plt

plt.scatter(df["Chapter Name"], df["Time Completed"], label="Time Completed")
plt.scatter(df["Chapter Name"], df["Goal Time"], label="Goal Time")
plt.scatter(df["Chapter Name"], df["Time Predicted TPW"], label="Time Predicted TPW")
plt.legend()
plt.xlabel("Chapter Name")
plt.ylabel("Time (minutes)")
plt.title("Chapter Progress")
plt.show()
