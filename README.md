# Sophos Central API - WebControl - allowed site retreival
Script intended to obtain all allowed sites from each tenant.

## Usage
1. Create API client ID + secret from portal
2. Inject them in the main script you want to use.
3. Run the script.

Script supports paging and will loop over all pages.

## Caveat
The script does not support rate limiting backoff timers and 
will crash when it runs out of credits. 

## ToDo
Add backoff timer depending on HTTP code return.
Error handling in no way present today.
