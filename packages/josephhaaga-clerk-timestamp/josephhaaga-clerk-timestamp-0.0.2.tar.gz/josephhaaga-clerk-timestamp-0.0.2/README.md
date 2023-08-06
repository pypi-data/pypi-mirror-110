# clerk-timestamp

A [clerk](https://github.com/josephhaaga/clerk) extension to append timestamps to your journal


## Setup

```
$ pipx install josephhaaga-clerk-timestamp
```

Then, in your `clerk.conf` config file:

```
...

[hooks]
JOURNAL_OPENED =
    clerk.extensions.timestamp
```
