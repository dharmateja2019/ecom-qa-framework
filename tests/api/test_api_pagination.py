import pytest


@pytest.mark.regression
def test_pagination_first_page(product_catalogue):
    response = product_catalogue({"limit": 10, "skip": 0})
    data = response

    assert len(data["products"]) == 10
    assert data["skip"] == 0
    assert data["limit"] == 10
    assert data["total"] > 0


@pytest.mark.regression
def test_pagination_second_page_has_different_products(product_catalogue):
    response_page1 = product_catalogue({"limit": 5, "skip": 0})
    response_page2 = product_catalogue({"limit": 5, "skip": 5})

    page1_ids = [p["id"] for p in response_page1["products"]]
    page2_ids = [p["id"] for p in response_page2["products"]]

    # No overlap between pages
    assert (
        len(set(page1_ids) & set(page2_ids)) == 0
    ), "Same products appearing on different pages — pagination is broken"


@pytest.mark.regression
def test_pagination_total_matches_actual_count(product_catalogue):
    response = product_catalogue({"limit": 194, "skip": 0})
    data = response

    declared_total = data["total"]
    actual_products = len(data["products"])

    assert (
        actual_products <= declared_total
    ), f"Got {actual_products} products but total says {declared_total}"


@pytest.mark.regression
@pytest.mark.parametrize(
    "limit,skip",
    [
        (5, 0),
        (10, 0),
        (10, 10),
        (20, 20),
    ],
)
def test_pagination_respects_limit_parameter(product_catalogue, limit, skip):
    response = product_catalogue({"limit": limit, "skip": skip})
    products = response["products"]
    assert len(products) <= limit, f"Expected max {limit} products, got {len(products)}"
