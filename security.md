# Security Considerations
## Intended Users
This repository is intended for students of CSE 3000 including myself, and the professor of CSE 3000. It does not belong in the hands of any other parties.

## Assessment of Security Risks
The repository has undergone careful analysis and the determination is that the security risk is low. Some considerations if this repository were to fall into enemy hands would be the enemy getting access to our hard coded model seeds, small sample datasets (which do not contain real PII, only fake PII), and an understanding of our model construction.

## Steps Taken to Secure the Repository
The repository is secured using GitHub best practices. These include:
- There are no hard-coded secrets or credentials in this repo, and if need be we would gather these through an API call. 
- Write and read access is restricted to the repository owner and the professor, as well as any TAs. 
- Tracking of all historical changes via github allows us to view past security concerns. 

Since the repository contains only class assignments without PII or classified information, security measures such as pull request rules or CODEOWNERS files are not considered necessary.