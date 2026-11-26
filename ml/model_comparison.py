"""
Store model comparison results.
"""

comparison_results = []


def add_result(model_name, accuracy):
    comparison_results.append({
        "Model": model_name,
        "Accuracy": accuracy
    })


def show_results():
    print("\n========== MODEL COMPARISON ==========")

    comparison_results.sort(
        key=lambda x: x["Accuracy"],
        reverse=True
    )

    for result in comparison_results:
        print(f"{result['Model']}: {result['Accuracy']:.4f}")