import json

def test_mock_products_api(page):
    # Step 1: Mock API
    page.route("**/products", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps({
            "products": [
                {"id": 1, "title": "Mocked Product"}
            ]
        })
    ))

    # Step 2: Open blank page
    page.goto("about:blank")

    # Step 3: Trigger API call from browser
    result = page.evaluate("""
        async () => {
            const res = await fetch('https://dummyjson.com/products');
            return await res.json();
        }
    """)

    # Step 4: Validate mocked response
    assert result["products"][0]["title"] == "Mocked Product"

def test_mock_with_ui_render(page):
    import json

    page.route("**/products", lambda route: route.fulfill(
        status=200,
        content_type="application/json",
        body=json.dumps({
            "products": [
                {"id": 1, "title": "Mocked Product"}
            ]
        })
    ))

    page.goto("about:blank")

    # Inject UI rendering
    page.evaluate("""
        async () => {
            const res = await fetch('https://dummyjson.com/products');
            const data = await res.json();

            const div = document.createElement('div');
            div.id = 'product';
            div.innerText = data.products[0].title;
            document.body.appendChild(div);
        }
    """)

    assert page.locator("#product").inner_text() == "Mocked Product"