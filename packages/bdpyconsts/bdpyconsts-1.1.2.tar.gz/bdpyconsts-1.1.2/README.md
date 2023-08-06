# Python constant manager

## New features
```
2023.06.14
1. Support manual constant modification by locking the flag bit with a manual switch

    from bdpyconsts import bdpyconsts as consts

    consts.ABCD = "abcd"

    # one way
    consts.unlock()
    consts.ABCD = "abcd"
    consts.locked()

    # another way
    if not consts.lock:
        onsts.ABCD = "abcd"
```