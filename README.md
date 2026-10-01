Google Cloud setup
* Create project in Google Cloud
* Enable Vertex AI (Agent Platform) APIs
* Go to IAM & Admin, create a service account.
  * ID/email of the service account can be anything.
  * Give it the "Agent Platform User" role in Permissions.
* Open the service account and go to Keys tab.
* Create a new JSON key and save the JSON file inside this directory as "service-account.json".
* Paste the project ID in the `PROJECT_ID` var in the code.