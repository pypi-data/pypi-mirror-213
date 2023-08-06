# ustack-logging

Default logging configuration for uStack style Python applications.

## Installation ##

```
pip install ustack-logging
```

## Usage ##

```python
from ustack_logging.logging_configuration import configure_logging


def main():
    configure_logging()

    # Run your application


if __name__ == "__main__":
    main()
```

## Intent ##

This library is intended to codify the standard way uStudio Python
applications log and report errors when running inside Kubernetes. It
takes no configuration because its intent is to enforce a
configuration.

However, it is built on [datadog-logger](https://github.com/ustudio/datadog-logger),
which is configurable. If you need a different configuration, it
should be trivial to implement it using that library directly.

## Configuration ##

The library configures the following things:

It sets up the logging library to log the time, log level, module name
and log message for every message, and it sets the current log level
to `INFO`.

In order to function, it uses a secret named `environment-info` in the
`ustudio-system` namespace. The secret must contain the keys
`environment` and `datadog-api-key`, and the pod must contain a label
named `role`.

If any information is missing or any connections fail it logs a
warning and does not error.

It configures the `datadog-logger` library to send `ERROR` and above
log messages to Datadog as events, with the following tag mapping:

* `environment-info.environment` -> Datadog tag `environment`
* K8s Pod Namespace -> Datadog tag `service`
* K8s Pod Label `role` -> Datadog tag `role`
