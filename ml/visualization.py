import matplotlib.pyplot as plt


def plot_branch_distribution(df):
    """
    Plot the number of students in each branch.
    """

    branch_counts = df["branch"].value_counts()

    plt.figure(figsize=(8, 5))

    branch_counts.plot(kind="bar")

    plt.title("Student Distribution by Branch")
    plt.xlabel("Branch")
    plt.ylabel("Number of Students")

    plt.tight_layout()

    plt.savefig("reports/branch_distribution.png")

    plt.show()

def plot_cgpa_distribution(df):
    """
    Plot the distribution of CGPA.
    """

    plt.figure(figsize=(8, 5))

    plt.hist(df["cgpa"], bins=5)

    plt.title("CGPA Distribution")
    plt.xlabel("CGPA")
    plt.ylabel("Number of Students")

    plt.tight_layout()

    plt.savefig("reports/cgpa_distribution.png")

    plt.show()