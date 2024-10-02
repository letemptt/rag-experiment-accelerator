from unittest.mock import patch
from pytest import approx

from rag_experiment_accelerator.evaluation.plain_metrics import (
    bleu,
    fuzzy_score,
    levenshtein,
    jaccard,
    hamming,
    jaro_winkler,
    cosine_ochiai,
    rouge_score,
    lcsseq,
    lcsstr,
)


def test_fuzzy_score():
    value1 = "Room, 2 Double Beds (19th to 25th Floors)"
    value2 = "Two Double Beds - Location Room (19th to 25th Floors)"

    assert fuzzy_score(str1=value1, str2=value2) == approx(89, rel=0.5)
    assert fuzzy_score(str1=value1, str2=value2, match_type="partial_token_set_ratio") == approx(100, 0.5)


def test_levenshtein():
    value1 = "party"
    value2 = "park"

    assert levenshtein(value1, value2) == 60


def test_jaccard():
    value1 = ["cat", "dog", "hippo", "monkey"]
    value2 = ["monkey", "rhino", "ostrich", "salmon"]

    assert jaccard(value1, value2) == 14


def test_hamming():
    value1 = "1011101"
    value2 = "1011011"

    assert hamming(value1, value2) == 71


def test_jaro_winkler():
    value1 = "crate"
    value2 = "trace"

    assert jaro_winkler(value1, value2) == 73


def test_cosine_ochiai():
    str1 = "The fox jumped over the high fence"
    str2 = "The quick brown fox jumped over the fence"

    assert cosine_ochiai(str1, str2) == 83


def test_rouge_score():
    str1 = "The fox jumped over the high fence"
    str2 = "The quick brown fox jumped over the fence"

    metrics_to_test = {
        "rouge1_precision": 75,
        "rouge1_recall": 86,
        "rouge1_fmeasure": 80,
        "rouge2_precision": 43,
        "rouge2_recall": 50,
        "rouge2_fmeasure": 46,
        "rougeL_precision": 75,
        "rougeL_recall": 86,
        "rougeL_fmeasure": 80,
    }

    for rouge_metric_name, expected_value in metrics_to_test.items():
        assert round(rouge_score(str1, str2, rouge_metric_name)) == expected_value


def test_lcsseq():
    value1 = "The fox jumped over the high fence"
    value2 = "The quick brown fox jumped over the fence."

    assert lcsseq(value1, value2) == 69


def test_lcsstr():
    value1 = "The fox jumped over the high fence"
    value2 = "The quick brown fox jumped over the fence."

    assert lcsstr(value1, value2) == 50


@patch("rag_experiment_accelerator.evaluation.plain_metrics.evaluate.load")
def test_bleu(mock_evaluate_load):
    mock_evaluate_load.return_value.compute.return_value = {"bleu": 0.5}
    predictions = [
        "Transformers Transformers are fast plus efficient",
        "Good Morning",
        "I am waiting for new Transformers",
    ]
    references = [
        [
            "HuggingFace Transformers are quick, efficient and awesome",
            "Transformers are awesome because they are fast to execute",
        ],
        ["Good Morning Transformers", "Morning Transformers"],
        [
            "People are eagerly waiting for new Transformer models",
            "People are very excited about new Transformers",
        ],
    ]
    score = bleu(predictions, references)
    assert round(score) == 50
