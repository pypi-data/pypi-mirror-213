# Vessel API Python SDK

The Vessel API Python SDK is a PyPi library for accessing the Vessel API, a Unified CRM API that provides standardized endpoints for performing operations on common CRM Objects.

<!-- Start SDK Installation -->
## SDK Installation

```bash
pip install vesselapi
```
<!-- End SDK Installation -->

## SDK Example Usage
<!-- Start SDK Example Usage -->
```python
import vesselapi
from vesselapi.models import operations

s = vesselapi.VesselAPI(
    security=shared.Security(
        vessel_api_token="",
    ),
)

req = operations.GetBatchCrmAccountRequest(
    access_token='corrupti',
    all_fields=False,
    ids='provident',
)

res = s.accounts.batch(req)

if res.response_body is not None:
    # handle response
```
<!-- End SDK Example Usage -->

## Authentication

To authenticate the Vessel Node SDK you will need to provide a Vessel API Token, along with an Access Token for each request. For more details please see the [Vessel API Documentation](https://docs.vessel.land/authentication-and-security).

<!-- Start SDK Available Operations -->
## Available Resources and Operations


### [accounts](docs/accounts/README.md)

* [batch](docs/accounts/README.md#batch) - Get Batch Accounts
* [create](docs/accounts/README.md#create) - Create Account
* [details](docs/accounts/README.md#details) - Get Account Details
* [find](docs/accounts/README.md#find) - Get Account
* [list](docs/accounts/README.md#list) - Get All Accounts
* [search](docs/accounts/README.md#search) - Search Accounts
* [update](docs/accounts/README.md#update) - Update Account

### [attendees](docs/attendees/README.md)

* [batch](docs/attendees/README.md#batch) - Get Batch Event Attendees
* [create](docs/attendees/README.md#create) - Create Event Attendee
* [details](docs/attendees/README.md#details) - Get Event Attendee Details
* [find](docs/attendees/README.md#find) - Get Event Attendee
* [list](docs/attendees/README.md#list) - Get All Event Attendees
* [search](docs/attendees/README.md#search) - Search Event Attendees
* [update](docs/attendees/README.md#update) - Update Event Attendee

### [calls](docs/calls/README.md)

* [batch](docs/calls/README.md#batch) - Batch Calls
* [create](docs/calls/README.md#create) - Create Call
* [details](docs/calls/README.md#details) - Get Call Details
* [find](docs/calls/README.md#find) - Get Call
* [list](docs/calls/README.md#list) - Get All Calls
* [search](docs/calls/README.md#search) - Search Calls
* [update](docs/calls/README.md#update) - Update Call

### [connections](docs/connections/README.md)

* [delete](docs/connections/README.md#delete) - Delete Connection
* [find](docs/connections/README.md#find) - Get Connection
* [list](docs/connections/README.md#list) - Get All Connections

### [contacts](docs/contacts/README.md)

* [batch](docs/contacts/README.md#batch) - Get Batch Contacts
* [create](docs/contacts/README.md#create) - Create Contact
* [details](docs/contacts/README.md#details) - Get Contact Details
* [find](docs/contacts/README.md#find) - Get Contact
* [list](docs/contacts/README.md#list) - Get All Contacts
* [search](docs/contacts/README.md#search) - Search Contacts
* [update](docs/contacts/README.md#update) - Update Contact

### [deals](docs/deals/README.md)

* [batch](docs/deals/README.md#batch) - Get Batch Deals
* [create](docs/deals/README.md#create) - Create Deal
* [details](docs/deals/README.md#details) - Get Deal Details
* [find](docs/deals/README.md#find) - Get Deal
* [list](docs/deals/README.md#list) - Get All Deals
* [search](docs/deals/README.md#search) - Search Deals
* [update](docs/deals/README.md#update) - Update Deal

### [emails](docs/emails/README.md)

* [batch](docs/emails/README.md#batch) - Get Batch Emails
* [create](docs/emails/README.md#create) - Create Email
* [details](docs/emails/README.md#details) - Get Email Details
* [find](docs/emails/README.md#find) - Get Email
* [list](docs/emails/README.md#list) - Get All Emails
* [search](docs/emails/README.md#search) - Search Emails
* [update](docs/emails/README.md#update) - Update Email

### [events](docs/events/README.md)

* [batch](docs/events/README.md#batch) - Get Batch Events
* [create](docs/events/README.md#create) - Create Event
* [details](docs/events/README.md#details) - Get Event Details
* [find](docs/events/README.md#find) - Get Event
* [list](docs/events/README.md#list) - Get All Events
* [search](docs/events/README.md#search) - Search Events
* [update](docs/events/README.md#update) - Update Event

### [integrations](docs/integrations/README.md)

* [list](docs/integrations/README.md#list) - Get CRM Integrations

### [leads](docs/leads/README.md)

* [batch](docs/leads/README.md#batch) - Get Batch Leads
* [create](docs/leads/README.md#create) - Create Lead
* [details](docs/leads/README.md#details) - Get Lead Details
* [find](docs/leads/README.md#find) - Get Lead
* [list](docs/leads/README.md#list) - Get All Leads
* [search](docs/leads/README.md#search) - Search Leads
* [update](docs/leads/README.md#update) - Update Lead

### [links](docs/links/README.md)

* [create](docs/links/README.md#create) - Exchange Public Token for Access Token

### [notes](docs/notes/README.md)

* [batch](docs/notes/README.md#batch) - Get Batch Notes
* [create](docs/notes/README.md#create) - Create Note
* [details](docs/notes/README.md#details) - Get Note Details
* [find](docs/notes/README.md#find) - Get Note
* [list](docs/notes/README.md#list) - Get All Notes
* [search](docs/notes/README.md#search) - Search Notes
* [update](docs/notes/README.md#update) - Update Note

### [passthrough](docs/passthrough/README.md)

* [create](docs/passthrough/README.md#create) - Passthrough Request

### [tasks](docs/tasks/README.md)

* [batch](docs/tasks/README.md#batch) - Get Batch Tasks
* [create](docs/tasks/README.md#create) - Create Task
* [details](docs/tasks/README.md#details) - Get Task Details
* [find](docs/tasks/README.md#find) - Get Task
* [list](docs/tasks/README.md#list) - Get All Tasks
* [search](docs/tasks/README.md#search) - Search Tasks
* [update](docs/tasks/README.md#update) - Update Task

### [tokens](docs/tokens/README.md)

* [create](docs/tokens/README.md#create) - Create Link Token

### [users](docs/users/README.md)

* [batch](docs/users/README.md#batch) - Get Batch Users
* [details](docs/users/README.md#details) - Get User Details
* [find](docs/users/README.md#find) - Get User
* [list](docs/users/README.md#list) - Get All Users
* [search](docs/users/README.md#search) - Search Users

### [webhooks](docs/webhooks/README.md)

* [create](docs/webhooks/README.md#create) - Create Webhook
* [delete](docs/webhooks/README.md#delete) - Remove Webhook
* [find](docs/webhooks/README.md#find) - Get Webhook
<!-- End SDK Available Operations -->

### SDK Generated by [Speakeasy](https://docs.speakeasyapi.dev/docs/using-speakeasy/client-sdks)
