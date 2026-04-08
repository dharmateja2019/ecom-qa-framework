## 1.what is the difference between asserting expected behaviour vs actual behaviour, and when do you choose each?

First is about asserting expected behaviour, where you have a clear expectation of what the output should be based on the requirements. You choose this when you have well-defined requirements and want to ensure the system behaves as intended.
Second is about asserting actual behaviour, where you observe the system's output without a predefined expectation. You choose this when you want to understand how the system currently behaves, especially in cases where requirements are not clear or when investigating issues.

## 2.why did you check curl AND the browser instead of just trusting the test failure?

Checking both curl and the browser allows you to confirm that the issue is not specific to one method of accessing the API. Curl can help you see the raw response and headers, while the browser can show you how the response is rendered in a user-friendly way. This helps ensure that the bug is consistent across different access methods and provides more context for debugging.

## 3.what would happen to a user on the frontend because of this bug?

A user on the frontend would likely experience a broken or non-functional product listing page. They might see an error message, incomplete data, or no products at all when trying to access the products page. This would lead to a poor user experience and could result in lost sales or decreased trust in the website.

## 4.what are the different types of assertions you can do in API testing, and when would you use each?

- Status code assertions: Used to verify that the API returns the expected HTTP status code (e.g., 200 for success, 400 for bad request). This is a basic check to ensure the API is responding correctly.
- Response body assertions: Used to check that the response contains the expected data or structure. This is important for validating that the API returns the correct information.
- Header assertions: Used to verify that the response headers contain expected values (e.g., content-type, cache-control). This can be important for ensuring proper handling of the response by clients.
- Performance assertions: Used to check that the API responds within an acceptable time frame. This is crucial for ensuring a good user experience and meeting service level agreements (SLAs).
- Error handling assertions: Used to verify that the API returns appropriate error messages and status codes when invalid requests are made. This is important for ensuring that the API handles errors gracefully and provides useful feedback to developers and users.

## 5.why did you choose to use a fixture for the product catalogue API response instead of calling the API directly in each test?

Using a fixture for the product catalogue API response allows you to centralize the setup and teardown of the API call. This promotes code reuse and makes your tests cleaner and more maintainable. It also ensures that all tests that depend on the product catalogue API response are using the same data, which can help reduce variability and improve test reliability. Additionally, if the API response changes or if you need to add additional setup steps (like authentication), you can do it in one place (the fixture) rather than in every test.
Fixtures return data — they are not callable functions inside tests. If you need dynamic input per test, use parametrize with a direct call, not a fixture."

## 6.when should you use autouse=True and when should you not?

You should use autouse=True when you want a fixture to be automatically applied to all tests within a certain scope (e.g., module, session) without needing to explicitly include it in the test function's parameters. This is useful for setup tasks that are required for all tests, such as initializing a database connection or setting up test data.
You should not use autouse=True when the fixture is only relevant for a subset of tests or when it performs actions that are not needed for every test. Using autouse=True in such cases can lead to unnecessary overhead and can make it harder to understand which tests are affected by the fixture. It can also lead to unintended side effects if the fixture modifies shared state or has performance implications.

## 7.should a fixture return a raw response object or parsed data, and why?

A fixture should ideally return parsed data rather than a raw response object. This is because tests typically need to work with the data in a structured format (e.g., a dictionary or list) rather than dealing with the raw response, which may require additional parsing in each test. Returning parsed data from the fixture promotes code reuse and keeps the tests cleaner and more focused on assertions rather than setup. It also abstracts away the details of how the data is retrieved and parsed, allowing tests to be more concise and easier to read.
