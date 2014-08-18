Django and GitHub Webhooks for Continuous Deployment
====================================================

[GitHub Webhooks](https://developer.github.com/webhooks/) are notifications sent by GitHub to
a web server when a monitored event happens in a monitored repository.
Webhooks are used in this sample project to implement a **continuous deployment** process.

Monitorable Events
------------------
Two kinds of events can be monitored:
- [`push`](https://developer.github.com/v3/activity/events/types/#pushevent) to a specific branch;
- creation of new [`release`](https://developer.github.com/v3/activity/events/types/#releaseevent).

Example Scenarios
-----------------
The following scenarios could be implemented:
- when new code is pushed to the `develop` branch, a new deployment to the *staging* website is
 automatically performed;
- when a new release is created, a new deployment to the *live* website is automatically performed.

Docs
----
- GitHub Webhooks: https://developer.github.com/webhooks/
- GitHub event types: https://developer.github.com/v3/activity/events/types/
- Create a release: https://help.github.com/articles/creating-releases