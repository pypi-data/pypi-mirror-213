<!-- GitLab Badges -->


ExceptionControl
================
The ExceptionControl class is designed to be a helper class that is inherited
into a class to give it a convenient interface to implement conditional
exception handling options. The purpose of this is to give developers
additional flexibility in how events can be handled and tune the overall
behaviour via parameters while adding minimal additional control code.

In many codes one may wish their code to take a fail fast approach to handling
issues such as unexpected input or other errors. While this method often works
well to rapidly identify problems by causing an application to exit, there are
times when maybe just a warning is sufficient.

ExceptionControl allows us to classify an event based on its severity using a
threshold setting that can be changed. This gives us two degrees of control
over the handling of an event. First, by assigning the level of severity of the
event itself we can direct what happens when the event is triggered. Second,
we can set thresholds that direct the behaviour of the handler when an event
is triggered.


Documentation and User Guide
============================
See the [User Guide][3] for detailed documentation on the package. This includes
the API docs, user guide, and examples.

History
=======
*ExceptionControl* is pulled from [*ConfigParserEnhanced*][3] into its own module
because it is an interesting and useful class. Splitting these up was the intent from
the beginning when it was originally developed.

Updates
=======
See [CHANGELOG][1] for information on changes.


[1]: https://gitlab.com/semantik-software/code/python/ExceptionControl/-/blob/main/CHANGELOG.md
[2]: https://github.com/sandialabs/ConfigParserEnhanced
[3]: https://semantik-software.gitlab.io/code/python/ExceptionControl/

