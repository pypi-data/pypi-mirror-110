# clerk-timestamp

A [clerk](https://github.com/josephhaaga/clerk) extension to append timestamps to your journal


## Setup

Install `clerk-timestamp` in the `venv` that `clerk` is installed in

```
$ pipx runpip josephhaaga-clerk install josephhaaga-clerk-timestamp
```

Then, in your `clerk.conf` config file:

```
...

[hooks]
JOURNAL_OPENED =
    timestamp
```

For more information, see `clerk` [hooks documentation](https://github.com/josephhaaga/clerk#hooks)


### Configuration

As of v0.0.3, `clerk-timestamp` supports the following configuration options.

* `format` specifies your timestamp format (used in `datetime.strftime`) 
* `prefix` specifies the timestamp prefix
* `suffix` specifies the timestamp suffix

Add them to your `clerk.conf` config file, as show in this example:
```
[DEFAULT]
...

[hooks]
JOURNAL_OPENED=
    timestamp

[timestamp]
format=%%Y-%%m-%%d %%I:%%M:%%S %%p
prefix=
    [
suffix=] 
```

which results in a newline character, and square brackets around the timestamp in our specified `format` every time a journal is opened

```
# existing journal document <EOF>

[2021-06-22 09:47:23 PM]
```
