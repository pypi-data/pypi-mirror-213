# hcs-cli Command Cheatsheet

## Utility Commands

### Profile Commands
* Profile is a configuration for the target HCS environment you want to access, with the API token or client ID/credential for authentication.
* HCS CLI has the "profile" subcommand to manage multiple profiles.
* All HCS CLI commands works with the "current" profile, which can be changed via the profile subcommand.
* Profiles are nothing but files in ~/.hcs/profiles. You may also edit the files directly.

| Example                                | Purpose                                |
|----------------------------------------|----------------------------------------|
| hcs profile init	                     | Initialize a default profile. |
| hcs profile init --name \<name\>   | Initialize a profile with a custom name. | 
| hcs profile list	                     | List existing profiles. |
| hcs profile get	                     | Get content of the current profile. |
| hcs profile get \<name\>	         | Get a profile by name. |
| hcs profile use \<name\>	         | Switch to a profile. |
| hcs profile file \<name\>         | Show the file path of a profile by name. So you can edit the file directly. |
| hcs profile delete \<name\>        | Delete a profile. |

### Auth Commands

| Example                                | Purpose                                |
|----------------------------------------|----------------------------------------|
| hcs auth                               | Get the bearer token that can be used for REST API. |
| hcs auth --details                     | Get auth token details. |

### Context Commands
* Context is a state store backed by disk files. Context is associated with a profile. Different profiles have different contexts. Context is for supporting automation. E.g. the authentication state is cached using context.
* Context is similar to the environment variable, and context template utility is like the envsubst command. The difference is, context is persisted and can be reused.
* Context is internally used to support some complex subcommands which has orchestration and has the need to support break-and-resume.

| Example                                | Purpose                                |
|----------------------------------------|----------------------------------------|
| hcs context clear                      | Delete all context objects, for the current profile.
| hcs context list                       | List all context item names, for the current profile. |
| hcs context get                        | Get data of a specific context object, for the current profile. |
| hcs context set                        | Set a context object by name, for the current profile. |
| hcs context delete                     | Delete a context object by name, for the current profile. |

#### Text Template with Context Variables

The CLI framework provides a utility to facilitate template-based processing, with context variables. So in an automation scenario, downstream operations can easily access results from upstream operations, by sharing the states stored in the context.

There are two scenarios:

In side HCS CLI command implementation, context is accessible.
In a script that uses HCS CLI, the "hcs context" command can be used to access the context values.

Example: WIP

## Service Commands

### Admin
| Example                                | Purpose                                |
|----------------------------------------|----------------------------------------|
| hcs admin edge list | List edges. |
| hcs admin edge get \<id\> | Get a specific edge by ID. |
| hcs admin template list --template-search "providerLocation $eq westus2" | List templates by query. | 
| hcs admin template get \<id\> | Get a template by ID. |

### VmHub
| Example                                | Purpose                                |
|----------------------------------------|----------------------------------------|
|                                        |                                        |


### PKI
| Example                                | Purpose                                |
|----------------------------------------|----------------------------------------|
| hcs pki sign-resource-cert my-res1     | Request a resource certificate. |
| hcs pki get-root-ca                    | Get root CA configured for the target environment. |
| hcs pki get-org-cert                   | Get the org signing CA. |
| hcs pki delete-org-cert                | Delete org signing CA. A new one will be created again when needed. |
### LCM

| Purpose                                                    | Example                                |
|------------------------------------------------------------|----------------------------------------|
| hcs lcm template create --id-only < payload/lcm/zero.json            | Create a zerocloud template for test. |
| hcs lcm template wait \<id\>                  | Wait for template ready. |
| hcs lcm template wait --timeout=1m10s --return-template \<id\>  | Wait for template ready. |
| hcs lcm template list --type ZEROCLOUD \| jq ".\|map(.id)" | List all zerocloud templates, id only. |
| hcs lcm template list --org=all --limit=2000  | List templates from all orgs (requires service global read permission). |
| hcs lcm template get \<id\>                   | Get template by ID. |
| hcs lcm template delete \<id\>                | Delete template by ID. |
| hcs lcm provider list --type ZEROCLOUD                     | List zero providers. |
| hcs lcm provider get \<id\>                   | Get a provider by ID. |
| hcs lcm provider delete \<id\>                | Delete a provider by ID. |
