# Alexa skill for Nightscout

**NOTE**: a recent
[pull request](https://github.com/nightscout/cgm-remote-monitor/pull/2200)
added built-in (and much more extensive) support for Alexa into Nightscout,
making this project somewhat redundant.  Please see the
[instructions](https://github.com/nightscout/cgm-remote-monitor/blob/dev/lib/plugins/alexa-plugin.md)
for details.

Work in progress!

* `alexa-metadata`: Metadata to be entered in the Alexa Developer Portal.
* `cloudformaton`: CloudFormation templates to deploy the services.
* `link-account-website`: HTML for the "link your account" mini-website.
* `nightscout-alexa-skill`: Lambda function that powers the actual Alexa skill.
* `nightscout-url-token`: Lambda function to create an access token for the
  Nightscout server URL (used by the "link your account" functionality).
