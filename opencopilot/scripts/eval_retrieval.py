"""
Search evaluation script.

Currently, the script expects that Weaviate vector store is running at http://0.0.0.0:8080/ and is
already filled with data.

If nothing is retrieved and nothing should be retrieved, then the result is perfect -
100% precision and 100% recall. But mostly, something should be retrieved. In that case:
If document retrieval returns nothing, the precision is 100%, and recall is 0%.
If document retrieval return everything, the precision is near 0%, and the recall is 100%.

Usage: see python eval_retrieval.py --help

"""
import argparse
import json
from typing import Callable
from typing import List


import matplotlib.pyplot as plt
from pathlib import Path
from langchain.schema import Document
from tqdm import tqdm

from opencopilot.utils.scripting import set_default_settings

set_default_settings("eval_retrieval")

from opencopilot.repository.documents import document_store
from opencopilot.eval.retrieval import evaluate_retrieval_dataset
from opencopilot.eval.entities import (
    RetrievalDataset,
    RetrievalResult,
    RetrievalSummaryEvaluation,
)


def parse_uri(s: str):
    """Turn into a (relatively) canonical URI."""
    s = s.strip()

    if "://" in s:
        return s[s.index("://") + 3 :]

    return s


def dataset_from_file(dataset_path: Path, limit: int = None) -> RetrievalDataset:
    with open(dataset_path) as f:
        examples_dict = json.load(f)
        if limit:
            examples_dict["examples"] = examples_dict["examples"][:limit]

        # Fix URLs - todo this is a bit hacky but best place to canonicalize URLs
        for example in examples_dict["examples"]:
            example["documents"] = [parse_uri(d) for d in example["documents"]]

    return RetrievalDataset.from_dict(examples_dict)


def print_metrics(metrics: RetrievalSummaryEvaluation):
    print("  Metrics")
    print(f"    average precision:", metrics.average_precision)
    print(f"       average recall:", metrics.average_recall)


def evaluate_retriever(
    search_function: Callable, dataset: RetrievalDataset, **search_kwargs
) -> RetrievalSummaryEvaluation:
    """Evaluate a retriever function on a dataset."""

    predictions = []
    for example in tqdm(dataset.examples):
        predicted_raw: List[Document] = search_function(example.query, **search_kwargs)
        retrieved_urls = [parse_uri(p.metadata["source"]) for p in predicted_raw]
        predictions.append(RetrievalResult(documents=retrieved_urls))

    return evaluate_retrieval_dataset(dataset, predictions)


def _draw_curve(dataset_path: str, limit=None):
    final_metrics = []
    for k in range(0, 11):
        document_retriever = document_store.get_document_store()
        search_type = f"similarity_search"
        metrics = evaluate_retriever(
            document_retriever.find,
            dataset=dataset_from_file(dataset_path, limit=limit),
            search_type=search_type,
            k=k + 1,
        )
        final_metrics.append(metrics)
        print_metrics(metrics)

    _plot_curve(final_metrics)


def _plot_curve(final_metrics: List[RetrievalSummaryEvaluation]):
    x = [item for item in range(len(final_metrics))]
    y1 = [item.average_precision for item in final_metrics]
    y2 = [item.average_recall for item in final_metrics]
    plt.plot(x, y1, label="average precision")
    plt.plot(x, y2, label="average recall")
    plt.xlabel("k")
    plt.ylabel("Average Precision & Recall")
    plt.title("Average Precision & Recall")
    plt.legend(loc="upper left")
    plt.show()


def _log_wandb(summary_evaluation: RetrievalSummaryEvaluation):
    import wandb

    wandb.init(
        # Set the project where this run will be logged
        project="opencopilot-retrieval",
        # Track hyperparameters and run metadata
        config={},
    )
    wandb.log(
        {
            "average_precision": summary_evaluation.average_precision,
            "average_recall": summary_evaluation.average_recall,
        }
    )
    with open(wandb.run.dir + "/evaluations.json", "w") as f:
        json.dump(summary_evaluation.to_dict(), f, indent=4)

    wandb.finish()


def main(
    dataset_path: str, draw_curve: bool, output_path: str = None, limit: int = None
):
    # TODO: document_store.init_document_store()
    if draw_curve:
        _draw_curve(dataset_path, limit=limit)
    else:
        document_retriever = document_store.get_document_store()
        metrics = evaluate_retriever(
            document_retriever.find,
            dataset=dataset_from_file(dataset_path, limit=limit),
            search_type="similarity_search",
            k=4,
        )
        print_metrics(metrics)
        if output_path:
            with open(output_path, "w") as f:
                json.dump(metrics.to_dict(), f, indent=4)
        return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", type=str, help="Dataset path", required=True)
    parser.add_argument(
        "-n",
        "--num_examples",
        type=int,
        default=None,
        help="Limit how many examples are evaluated from dataset. Default: all examples used.",
    )
    parser.add_argument(
        "--draw_curve",
        action="store_true",
        help="Draw precision/recall curve. Disables --wandb and --output.",
    )
    parser.add_argument("--wandb", action="store_true", help="Store results in WANDB")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output file for evaluation results in JSON format.",
    )
    args = parser.parse_args()

    from opencopilot.repository.documents import document_store
    from opencopilot.repository.documents.document_store import WeaviateDocumentStore

    document_store.init_document_store(WeaviateDocumentStore())

    metrics = main(
        args.dataset_path,
        args.draw_curve,
        output_path=args.output,
        limit=args.num_examples,
    )

    if args.wandb and not args.draw_curve:
        print("Logging to WANDB:")
        _log_wandb(metrics)
