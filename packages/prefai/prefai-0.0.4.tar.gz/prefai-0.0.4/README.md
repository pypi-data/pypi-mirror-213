
# PrefAI Python Library

The PrefAI Python Library enables applications coded in Python to interface with the PrefAI API.

## Installation

Install with:

```bash
pip install prefai
```

## Usage

The library needs an API key, which you get on your [pref.ai developer account](https://pref.ai/dev/account/keys).

```bash
export PREFAI_API_KEY=<YOUR_SECRET_KEY>
```

<!-- You're now ready for your first API request. Let's imagine that our AI service has had the following conversation with a user whose email is `test@pref.ai`:

> User: What's a spicy appetizer you'd recommend for a BBQ with 6 people?
> AI: Sure, a great appetizer for a barbecue is Grilled Jalapeño Poppers. Here's a simple recipe: ...
> User: Thanks but can you give me something without cheese? -->

We can now add a user record like this:

```python
import os
from prefai import prefai_client

prefai_client.api_key = os.getenv("PREFAI_API_KEY")
test_user_email = os.getenv("PREFAI_TEST_USER_EMAIL")

# Add record
prefai_client.add_record(
    user_email = "test@pref.ai",
    user_action = "What's a spicy appetizer you'd recommend for a BBQ with 6 people?",
)
```

For more information and next steps, read the [quickstart](https://pref.ai/dev/docs/quickstart).
