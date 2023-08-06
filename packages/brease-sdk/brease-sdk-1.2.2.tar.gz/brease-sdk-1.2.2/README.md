# brease-sdk

<!-- Start SDK Installation -->
## SDK Installation

```bash
pip install brease-sdk
```
<!-- End SDK Installation -->

## SDK Example Usage
<!-- Start SDK Example Usage -->
```python
import sdk
from sdk.models import operations, shared

s = sdk.SDK()

req = operations.AddRuleRequest(
    add_rule_input=shared.AddRuleInput(
        rule=shared.ModelsRule(
            action='corrupti',
            description='provident',
            expression=shared.ModelsRuleExpression3(
                condition=shared.Condition(
                    base=shared.ConditionBase2(
                        ref=shared.ConditionBaseRef(
                            dst='unde',
                            src='nulla',
                        ),
                    ),
                    parameter=False,
                    type=shared.ConditionType.RGX,
                ),
            ),
            id='69a674e0-f467-4cc8-b96e-d151a05dfc2d',
            target=shared.ModelsTarget(
                target='at',
                target_value='maiores',
                type='molestiae',
            ),
        ),
    ),
    context_id='quod',
)

res = s.context_id.add_rule(req, operations.AddRuleSecurity(
    api_token="",
))

if res.api_add_rule_response is not None:
    # handle response
```
<!-- End SDK Example Usage -->

<!-- Start SDK Available Operations -->
## Available Resources and Operations


### [context_id](docs/contextid/README.md)

* [add_rule](docs/contextid/README.md#add_rule) - Adds a new rule to the context
* [evaluate_rules](docs/contextid/README.md#evaluate_rules) - Evaluate rules within a context on the provided object
* [get_all_rules](docs/contextid/README.md#get_all_rules) - Returns all rules with the context
* [remove_rule](docs/contextid/README.md#remove_rule) - Removes a rule from the context
* [replace_rule](docs/contextid/README.md#replace_rule) - Replaces an existing rule within the context
<!-- End SDK Available Operations -->

### Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

### Contributions

While we value open-source contributions to this SDK, this library is generated programmatically.
Feel free to open a PR or a Github issue as a proof of concept and we'll do our best to include it in a future release !

### SDK Created by [Speakeasy](https://docs.speakeasyapi.dev/docs/using-speakeasy/client-sdks)
