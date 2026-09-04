from __future__ import annotations


def metrics_table(rows):
    headers = ["Domain", "Scenario", "Precision", "Recall", "F1", "FPR", "Recon RMSE"]
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        lines.append(
            "| {domain} | {scenario} | {precision:.3f} | {recall:.3f} | {f1:.3f} | "
            "{false_positive_rate:.3f} | {reconstruction_rmse:.3f} |".format(**r)
        )
    return "\n".join(lines)
