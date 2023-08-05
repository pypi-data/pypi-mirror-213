# Running SpinningBox example

```
source ${BRICK_ROOT}/setup_env.bash
source ${AGX_ROOT}/setup_env.bash
# NOTE: This should not be required! Automatic dependency tracking is used
# brick --log DEBUG build brick/Physics/
brick --log DEBUG build models/examples
agxBrick --log DEBUG models/examples/WrappedAgxScene/SpinningBox.yml
```

## TODO

- Add unittest to SpinningBox when we can capture outputs and analyze / compute expressions.
