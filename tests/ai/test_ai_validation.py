import pytest
from utils.ai_helper import validate_product_response, suggest_test_cases

pytestmark = [
    pytest.mark.regression,
    pytest.mark.ai,
]  # Mark all tests in this file as regression and ai tests


def test_ai_validates_product_data_quality(product_catalogue):
    products = product_catalogue()["products"]

    failed_products = []
    for product in products[:5]:  # Test first 5
        result = validate_product_response(product)

        if result.get("is_valid") is False:
            failed_products.append(
                {"product_id": product["id"], "issues": result.get("issues", [])}
            )

    assert (
        len(failed_products) == 0
    ), f"AI found data quality issues in products: {failed_products}"


@pytest.mark.skip(
    reason=(
        "Requires local Ollama instance and may be flaky due to LLM response variability. "
        "The test is more for manual inspection of AI suggestions rather than automated pass/fail."
    )
)
def test_ai_suggests_test_cases_for_products_endpoint(product_catalogue):
    products = product_catalogue()["products"]  # correct
    sample_product = products[0]  # first product

    suggestions = suggest_test_cases(sample_product)

    assert suggestions != "LLM_TIMEOUT", "LLM timed out"
    assert "LLM_ERROR" not in suggestions, f"LLM error: {suggestions}"
    assert len(suggestions) > 100, "LLM response too short to be useful"

    print("\n--- AI Test Case Suggestions ---")
    print(suggestions)
    print("--------------------------------")


def test_ai_flags_product_with_zero_price():
    fake_product = {
        "id": 999,
        "title": "Test Product",
        "price": 0,
        "rating": 4.5,
        "stock": 10,
        "category": "electronics",
    }
    result = validate_product_response(fake_product)

    # Skip if LLM didn't respond — don't fail for infrastructure issues
    if result.get("is_valid") is None:
        pytest.skip(f"LLM unavailable: {result.get('issues')}")

    # If LLM responded, it must flag zero price
    assert (
        result.get("is_valid") is False
    ), f"AI should flag zero price as invalid. Got: {result}"
    print(f"AI detected issues: {result.get('issues')}")


def test_ai_handles_malformed_product_data():
    malformed_product = {
        "id": 1000,
        "title": "",  # Empty title
        "price": -10,  # Unrealistic price
        # Missing category field
        "rating": 6,  # Invalid rating (assuming max is 5)
        "stock": 5,
    }
    result = validate_product_response(malformed_product)

    if result.get("is_valid") is None:
        pytest.skip(f"LLM unavailable: {result.get('issues')}")

    assert (
        result.get("is_valid") is False
    ), f"AI should flag malformed product as invalid. Got: {result}"
    print(f"AI detected issues: {result.get('issues')}")
