# Specker

The JSON Configuration Validator

- [Specker](#specker)
  - [About](#about)
    - [How does it work?](#how-does-it-work)
  - [Usage](#usage)
    - [Spec Files](#spec-files)
    - [Validation](#validation)
  - [Example](#example)
  - [Utils](#utils)

## About

Specker is a way to validate a configuration (Dictonary, or JSON) against a defined set of rules, while also providing defaults. Additionally, because the configuration is now documented as one of the Spec files, documentation for the specific configuration can be generated from the Spec file!

### How does it work?

Specker uses a dictionary block for each specified parameter in order to validate that it is the correct type, and that it exists, if required. If it is not a required value, a default can also be set. Spec files contain a defined group or configuration file, for example, if we wanted to validate `myconfig.json`, we would create a Spec called `myconfig.json.spec`. This Spec would be loaded, and then the contents of `myconfig.json` would be compared against it.

## Usage

### Spec Files

See `SPECFILES.md` for information on the required values for each entry in a Spec. Spec files must be saved as a `.spec` file. For speed, specs should be kept in their own directory, so no other files need to be searched through.

Spec Files are made up of many blocks of Spec rules which define what a configuration block must look like. Specker is even capable of self-specing itself! You can see the Spec file for all other Spec files by examining the `specs/specker.spec` file.

### Validation

Using Specker is easy! Once you've made your Spec file(s), you only need to load Specker, and your configuration, then compare the two!

`SpeckerLoader.compare()` will return a boolean pass/fail. Failure will occur if any of the spec validation fails. Validation messages are logged in via `logging.*`. This includes having values that are not in the spec file.

```
### Load Your Configuration
import json
try:
    with open("myfile.json", "r", encoding="utf-8") as f:
        config_content = json.loads(f.read())
except BaseException as e:
    print(f"Failed to load myfile, {e}")
    exit(1)

### Load and Use Specker
# Import the Specker Loader
from specker.loader import SpeckerLoader

# Initialize the Loader, and point it to your Spec directory
spec_loader = SpecLoader(Path(__file__).resolve().parent.joinpath("specs")) # This would load `../specs/` from the location where SpecLoader was initialized

# Load `myfile.json.spec` and compare `config_content` against it.
spec_result = spec_loader.compare("myfile.json",config_content)
# Exit based on spec result
if not spec_result:
    exit(1)
exit(0)
```

Specker will only validate one level deep in a dictionary/JSON block. In the example configuration below, you will see how to validate deeper levels of a configuration.

## Example

Spec: `myfile.json.spec`
```
{
    "name": {
        "required": true,
        "default": "",
        "type": "str",
        "comment": "Job Name (Identifier)",
        "example": "myexample"
    },
    "time": {
        "required": true,
        "default": {},
        "type": "dict",
        "comment": "Time Configuration"
    },
    "environment": {
        "required": false,
        "default": {},
        "type": "dict",
        "comment": "Environment Variables to use during Command execution"
    },
    "visibility": {
        "required": false,
        "default": "hidden",
        "type": "str",
        "values": [ "hidden", "visible", "admin", "deleted" ],
        "comment": "Visbility of Command Information"
    }
}
```

Given the above Spec, additional Specs sould be created for `time` and optionally `environment`, Note the `dict` value for `type`. This will validate that `time` is a `dict`, without caring what is in it. For that validation, you need the spec below.

Spec: `myfile.json_time.spec`
```
{
    "minute": {
        "required": true,
        "default": "",
        "type": "str",
        "comment": "Minute(s) to Run at",
        "example": "*/5"
    },
    "hour": {
        "required": true,
        "default": "",
        "type": "str",
        "comment": "Hour(s) to Run at",
        "example": "*/2"
    },
    "day-of-month": {
        "required": true,
        "default": "",
        "type": "str",
        "comment": "Day(s) of Month to Run at",
        "example": "*"
    },
    "month": {
        "required": true,
        "default": "",
        "type": "str",
        "comment": "Month(s) to Run at",
        "example": "*"
    },
    "day-of-week": {
        "required": true,
        "default": "",
        "type": "str",
        "comment": "Day(s) of Week to Run at",
        "example": "1"
    }
}
```

Now that we have our Specs, we can compare them against our configuration file:

```
# Initialize the Loader, and point it to your Spec directory
spec_loader = SpecLoader(Path(__file__).resolve().parent.joinpath("specs")) # This would load `../specs/` from the location where SpecLoader was initialized

# Load `myfile.json.spec` and compare `config_content` against it.
spec_result = spec_loader.compare("myfile.json",config_content)
if not spec_result:
    exit(1)
spec_result = spec_loader.compare("myfile.json_time",config_content["time"])
if not spec_result:
    exit(1)
exit(0)
```

We can additionally Gather any default values the Spec contains, with the `defaults` function:

```
# Initialize the Loader, and point it to your Spec directory
spec_loader = SpecLoader(Path(__file__).resolve().parent.joinpath("specs")) # This would load `../specs/` from the location where SpecLoader was initialized

# Load `myfile.json.spec` and gather any defaults from it
spec_defaults = spec_loader.defaults("myfile.json")
print(json.dumps(spec_defaults))
```

## Utils

To aid in documentation, Specker comes with `generate-spec-docs.py`, a script to generate a .md file from a directory of Spec files. (See `SPECFILES.md`, this is a generated document).

You can additionally validate a Spec file using `validate-spec-file.py`, to ensure that your Spec file is built properly.
