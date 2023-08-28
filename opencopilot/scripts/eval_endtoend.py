import argparse
import json
import time
from typing import List
from uuid import uuid4

import requests
import tqdm

from opencopilot import settings
from opencopilot.utils.scripting import set_default_settings

set_default_settings("eval_endtoend")

from opencopilot.eval.endtoend import evaluate_endtoend_dataset
from opencopilot.eval.entities import (
    EndToEndDataset,
    EndToEndResult,
    EndToEndSummaryEvaluation,
)


def _get_predictions(
    dataset: EndToEndDataset,
    api_url: str,
) -> List[EndToEndResult]:
    predictions: List[EndToEndResult] = []

    for example in tqdm.tqdm(dataset.examples, desc="Getting predictions..."):
        try:
            data = {"inputs": example.query}
            response = requests.post(
                f"{api_url}/v0/conversation/{str(uuid4())}", json=data
            )
            j = response.json()
            result = j["generated_text"]
            sources = j["sources"]
            predictions.append(EndToEndResult(answer=result, documents=sources))

            time.sleep(1)
        except Exception as e:
            predictions.append(EndToEndResult(answer="UNEXPECTED_ERROR", documents=[]))
    return predictions


def dataset_from_file(dataset_path: str, limit: int = None) -> EndToEndDataset:
    with open(dataset_path, "r") as f:
        dataset_dict = json.load(f)
        if limit:
            dataset_dict["examples"] = dataset_dict["examples"][:limit]
    return EndToEndDataset.from_dict(dataset_dict)


def _print_metrics(evaluations: EndToEndSummaryEvaluation) -> None:
    print("\ne2e evaluation:")
    print(f"    Total: {evaluations.evaluations_count}")
    print(f"    Total score: {evaluations.evaluations_score}%")


def _get_api_url() -> str:
    global url
    base_url = settings.get().API_BASE_URL
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    if ":" in base_url:
        return base_url
    return f"{base_url}:{settings.get().API_PORT}"


def _is_backend_running(api_url: str) -> bool:
    try:
        response = requests.get(api_url)
        return response.status_code == 200
    except:
        return False


def _log_wandb(summary_evaluation: EndToEndSummaryEvaluation) -> None:
    import wandb

    wandb.init(
        # Set the project where this run will be logged
        project="opencopilot-e2e-eval",
        # Track hyperparameters and run metadata
        config={},
    )
    wandb.log(
        {
            "evaluations_count": summary_evaluation.evaluations_count,
            "evaluations_score": summary_evaluation.evaluations_score,
        }
    )
    with open(wandb.run.dir + "/evaluations.json", "w") as f:
        json.dump(summary_evaluation.to_dict(), f, indent=4)

    wandb.finish()


def main(
    dataset_path: str,
    api_url: str,
    wandb: bool,
    output_path: str = None,
    limit: int = None,
) -> None:
    print("e2e evaluation starting!")
    dataset = dataset_from_file(dataset_path, limit=limit)
    predictions = _get_predictions(dataset, api_url)

    summary_evaluation = evaluate_endtoend_dataset(dataset, predictions)

    if output_path:
        with open(output_path, "w") as f:
            json.dump(summary_evaluation.to_dict(), f, indent=4)

    _print_metrics(summary_evaluation)
    if wandb:
        _log_wandb(summary_evaluation)


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
    parser.add_argument("--wandb", action="store_true", help="Store results in WANDB")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Output file for evaluation results in JSON format.",
    )
    args = parser.parse_args()

    url: str = _get_api_url()
    assert _is_backend_running(url), "Backend not running."

    assert settings.get().OPENAI_API_KEY, "OpenAI API key needs to be present"
    main(args.dataset_path, url, args.wandb, limit=args.num_examples)
