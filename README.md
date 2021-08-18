## `(de)specable` me!

**This is a draft of a future project, mostly for discussion. Do not use this in production. File an issue if you have thoughts!**

`specable` is a very small python package that provides a simple interface to initialise objects from `dicts`, and in turn describe objects as `dicts`. While not particularly exciting in isolation, it's *surprisingly* useful when building research software, for example enabling simple plugin systems or non-code specification of objects with many parameters.

`specable` is intended to be used for building other packages and is not usually "user-facing". It's also geared towards research, and probably not suitable for large-scale production use. (Though I'd be happy to be proven wrong!)

### Example

In YAML, a `specable`-style dictionary looks like this:

(We'll use a fictional machine learning library called `hyperdeep` with a NN class called `Minion` as example.)

```yaml

# example.yaml
hyperdeep/minion:
	layers: 250
	width: 1024
	activation: "banana"
```

The `python` equivalent is:
```python
example = {
    "hyperdeep/minion": {
        "layers": 250,
        "width": 1024,
        "activation": "banana",
    }
}
```

If `hyperdeep` uses `specable`, we'll then be able to call `hyperdeep.from_yaml("example.yaml")` (or `hyperdeep.from_dict(example)`) and receive an instance of `Minion`, initialised with our parameters.

On the backend, `specable` simply looks up the module `hyperdeep`, finds the class corresponding to `minion`, and initialises it with the "inner" dictionary.

This means that the model can be specified separately from any executable code: it is cleanly encapsulated in a human-readable file and can be instantiated as required without boilerplate or imports. Since  the `handle` (the first part of the dictionary) contains a module name, the class lookup can accomodate custom, one-off "plugins" for `hyperdeep` without any problems.

### Documentation

#### Terminology

A `spec` is a combination of `handle` and `payload`. `handle` is a `str` of the form `namespace/kind`, where `namespace` corresponds to a module name and `kind` is a string (typically the lowercase version of a class name). The `payload` is a `dict` (or something similar) that can be used to initialise an object, most simply by calling `Class(**payload)`. A `spec dict` is a `dict` of the form `{handle: payload}`.

#### Assumptions

- statelessness, i.e. parameters at initialisation fully determine the object
- small and sane payloads, i.e. objects aren't initialised with huge `numpy` arrays or similar (this is particularly important if `yaml` is used)

#### Overview

Basically, to use `specable`, you have to do the following:

- Decide on a reasonable name for the type of objects that you want to use with `specable` (for example, `models` if you're building a ML library, or `components` for a web library, or `drinks` for a bar); we call this a `collection`,
- Make sure that these classes inherit from `specable.Specable` and implement a `get_dict()` method,
- In the `__init__.py` of your package, have a list with that name, containing the classes.

Then, `specable.Interface("your_package_name", "your_collective_noun)` will give you an interface with suitable `from_dict`, `to_dict` and related methods. It's convenient to "alias" these methods to module-level methods.

To instantiate an object from a `spec dict`, `specable` will then do the following:

- Parse the `dict` into `namespace`, `kind` and `payload` (defaulting to your package name for `namespace`)
- Attempt to import `collection` from `namespace`
- In that list, find a class where `class.get_kind()` matches `kind`
- Return `class(**payload)` (or something custom)

#### Interface

`specable` provides two points of contact: 

1. `Specable` is a mixin class that provides the facilities for `specable` to work. Your class needs to inherit from it, and implement the `get_dict()` method that returns the `payload` `dict`. By default, initialisation is simply `Class(**payload)`, if you need something custom, you need to also implement the `_from_dict` class method. You can also specify `kind` if the lower-case classname is too long or unappealing, and `namespace` if the class is not located in `default_namespace`.
2. `Interface` provides the facilities for (de)-serialisation. You need to import it, and instantiate it with a `default_namespace` (corresponding to the name of your package) and a `collection`.

**The `tests/integration` folder shows a toy example using `specable`, it probably explains how it works much better than I can do here!**

### Why? Huh? What?

In [my work](https://marcel.science), I'm often building custom infrastructure for various experiments where I have to a) work in a "HPC" context (i.e. computations have to be run by a batch script), b) try many variations of parameters for a few classes (settings for machine learning models or computational methods). I've found it useful to separate "input files", i.e. the particular parameters to try, from implementation details, and it seems more reasonable to store such files as a non-executable format. With `specable`, it's easy to build simple command line interfaces of the form `hyperdeep run example.yml` without having to write lots of boilerplate `experiment.py`-type scripts.

`specable` is part of a broader effort to isolate the building blocks of my "one-off" tools, hoping that someone else will get some use out of them! It's essentially a part of [`cmlkit`](https://marcel.science/cmlkit) extracted into its own package for easier use and maintenance.

