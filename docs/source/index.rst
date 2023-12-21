Forestry Scenario
=================

.. toctree::
    :maxdepth: 2
    :caption: Contents:
    :hidden:

.. contents:: In This Page
    :depth: 2
    :local:
    :backlinks: entry


Overview
--------

The forestry domain consists of several interdependent sub-domains and operates as a set of
systems that are driven by supply and demand.  The challenge is to manage commodity resources
and reserve levels in order to meet demand at a price point where it is profitable to operate.
It is also crucial to consider sustainability and environmental factors that could endanger
the supply including over-production, seasonal climate and global trends, seasonal and market
market purchasing patterns, supplies and human resources.  It is important to understand
the nature of the industry in order to make informed decisions about the architecture of
the various applications used to manage each aspect of the industry.  These aspects can be
categorized according to the workflows and kinds of resources being managed at each phase
of operations.

- Land Resource Management
- Procurement and Inventory Management
- Field Operations and Harvesting
- Transportation and Dispatch
- Manifest Transfer and Reconciliation
- Finished Product Processing, manufacturing and provenance
- Reporting, Integration and Visualization

It is important for businesses in this industry to operate in a responsible and ethical
manner.  This introduces several regulatory compliance constraints that must be built into
the system in order to satisfy an ever-changing set of reporting and fee requirements.  In
addition, these requirements must be applied non-uniformly across the entire market which
means that different rules apply to different parts of the world, countries, states and
municipalities.

A highly complex financial model is required in order to support this landscape of
interconnected and regulated processes.  Ultimately, the final sale of processed goods to
consumers funds the entire operation from the farm to the consumer.  It is not easy to
predict the market factors that set the price to consumer, especially when the prediction
must be made several years in advance of the market.  This means that any business in the
industry will be funded based on estimations of future production and sales and depends
heavily on contracts and careful selection of harvest and production activities that
maintain the balance of supply and demand in order to keep operating and capital costs
below revenue projections.

The application of software to these business processes must make sense across all aspects
of the business.  In order to provide end-to-end solutions, it is not only important to
understand the users and personas and their individual requirements, but also to understand
the workflows, transactions, artifacts and interactions that facilitate the flow of
information, goods, services, and money between the users and personas and how they
change over time.

The following questions were presented as an architectural challenge to design a
multi-tenant, multi-application, multi-region set of microservices capable of facilitating
and automating the forestry industry scenarios above.

.. rubric:: Questions:

- Provide specifications required for the components (with API call examples) for a
  scalable microservices architectures providing REST services for multiple multi-tenant
  web applications.
- Describe how to scale a multi-region system that runs microservices in AWS/Azure,
  containerized or serverless back end services with scaled databases (will support both
  mobile and web-based applications).
- Describe the performance considerations required to make an efficient event based
  architecture utilizing microservices.
- Describe the specifications for an example API design with global data models and
  examples for transformations to convert data to the model.
- Describe how a data feature that includes machine learning or AI functionality would
  consume the data to provide an app layer user ability that would consume the data mode
  via the API.
- Provide a code example (stub code, language of your choice) for a user feature level
  interface of a search engine, recommendation engine, or other user level feature that
  would use a large data set (where an ML or AI model could be applied) that considers
  all of the above that would provide an example for developers to expand on to built out
  an app.

Simple Architecture
-------------------

I would like to begin the discussion with a simple diagram of a full stack application
that uses a REST API to abstract resource management from a web application.

.. uml:: index/simple_app.puml

This representation illustrates at a very high level that a "User" uses some "Client Agent"
to access some "Application" that manages "Data" through an "API".

A key thing to note at this point is that the "microservice" architecture will expand
this pattern and create collections for each base component and further categorize each
component according to its kind.

.. uml:: index/expanded_app.puml

Moving toward a microservice architecture requires modular discipline along loosely
coupled, clearly defined domain boundaries and incurs a complexity penalty that initially
impedes productivity.  Initially, it may be better to build up maturity and rigor around
key practices for supporting microservices and isolate functionality when the boundaries
are more apparent.

Scaling Objectives
------------------

The microservice architecture will address the main concern of deploying single purpose,
cohesive, loosely coupled resource domains in isolation.  This has the secondary effect of
independently scaling the services to meet the load concerns for that domain.  Using
the simple architecture provided, I want to point out the scaling opportunities and
challenges for each component

Multi-Tenant Support
^^^^^^^^^^^^^^^^^^^^

Users must be authenticated using a common authentication provider.  The identity provider
must implement standards, namely OAuth and OpenID in order to provide a common framework
for authentication and authorization across all services.

Scopes and claims identified for each user within the application context should provide
the appropriate boundary information to properly access segregated data based on various
boundary criteria such as organization context, account context, regional context, role
association, etc.

Note that Trimble ID implements the OAuth 2.0 framework and has a fixed set of OpenID
claims provided within a scope.  It will be necessary to supplement the scope context for
authorization in order to fully implement tenancy within the forestry (or any) sector.
For this reason, I would suggest implementing a context provider service as a microservice
with the single responsibility of setting and providing a partial context graph for a user
within the scope of an application.  This "partial graph" should include key user
associations such as organizational and account affiliations as well as application
entitlements (for monetization).  The partial graph should also carry domain specific
information regarding application role membership for workflow activities and granular
access controls for actions and resources within an application and resource domain.

.. rubric:: Setup User Context Within Application Scope

.. uml:: index/context.puml

.. rubric:: Use User Context To Realize Multi-Tenant Requirement

.. uml:: index/multi_tenant.puml

Multi-Client & Multi-Region Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Applications will be implemented as mobile and web applications.  Both types of client
agent will need to be routed to the regional distribution of the application or service
depending on rules configured in the content delivery network.  These rules can be further
enhanced with user preferences provided in the context for the application scope provided
for the user.

.. rubric:: Use AWS CDN to Route to Regional Distributions

.. uml:: index/muti_region.puml

Notes:

The Routing Logic Lambda component in this diagram could determine the best region based
on any number of factors.  It could use Route 53 latency data to route to regions of lower
latency, it could use the clients Geo IP information to route to Geo Isolated regions, it
could even use the context microservice to determine regional routing rules based on
preferences configured in the user's context graph.

The Data layer in this diagram assumes a Command Query Responsibility Segregation (CQRS)
pattern where read data is replicated to localized regions from a write replica of the
source data.

The microservice implementation in this diagram is a serverless implementation that
invokes a lambda based on requests to paths defined in the API Gateway.  The regional
gateway could be replaced with a containerized implementation of the API using ECS
services, Kubernetes Services, or even EC2 depending on the requirements.

Multi-Application/Capability Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ideally, the UI/UX design will be component based and capabilities should be composable
depending on the entitlements and features enabled for the user.  The capabilities should
be rendered as activities, screens, or components that access the various microservice
endpoints and paths.  All applications and capabilities must be context aware and based
on context provided from the context microservice in order to constrain access to attributes
and/or roles defined for the given identity.

Microservice Domains
^^^^^^^^^^^^^^^^^^^^

It is unclear at this point what the demarcation boundaries should be across the forestry
domain.  We should be cautious of the initial assumption that domain boundaries should be
set along business workflow lines.  Although this does seem like a logical separation of
concerns for the cohesion/coupling responsibilities of microservices, inter-service
communication should be minimized based on grouping resources that change together within
that service domain.  Failure to group resource management will result in tightly coupled
microservices and will defeat the purpose of separating the concerns to begin with an create
a "fragile system".  It is also possible to inadvertently create services that are too
small in scope (low cohesion) that will force deployment of multiple dependent services,
thereby creating a "distributed monolith".

Truly identifying single purpose, loosely coupled, highly cohesive microservice domains
will reduce the complexity of inter-service communication.  This has severe performance
implications for the performance of the microservices with regards to the messaging
infrastructure and transaction management for cross-domain transactions.  By localizing
all cohesive transactions within a service domain, transaction locking for multi-resource
updates can be handled efficiently and synchronously in process within the service domain.
This also minimizes transactional integrity problems with concurrency in a
multi-user/multi-tenant environment by delegating the lock and transaction management to
the database subsystem for that domain.

Data Modeling
^^^^^^^^^^^^^

This is an extremely broad topic and requires a non-trivial level of discipline and
governance.  Every API resource will reference components defined in a specification.
It is easy to gloss over the component definition of a resource in an OpenAPI
Specification.  For this reason, I would highly recommend using a tool like Stoplight to
manage and control component libraries for import of common, versioned models.

Additionally, models defined in component libraries should have corresponding versioned
json-schema and, ideally, semantic context defined using json-ld.

By introducing this level of standardization, we can use the features of json-ld to
perform transformations based on semantic context mapping rather than directly mapping
"field-to-field" transformations on a spec-by-spec basis.  The context-based approach of
json-ld allows for flattening and canonizing models.  This is useful for "recomposing" a
model in one context to a semantically equivalent model of another context effectively
creating the basis for data transformation based on semantics rather than schema.  However,
schema is important as well.  Data types defined in the json-schema version for a field in
one context should match the type of the semantic equivalent in another, but this is not
always the case.  In most cases, data type mismatches that occur in contextual mapping can
be handled by coercing the data to the least restrictive data-type (e.g. integer -> string).

Using the semantic context of json-ld also allows us to realize "data mesh" capabilities
for models shared across domains.  An example of this is can be illustrated with user
context.  It is possible to source elements of a user context from a domain service like
the "forestry context service" alluded to in this discussion.  This context can be composed
of domain specific attributes in addition to higher level contexts provided by other context
providers.  Specifically, context provided by corporate services such as Profiles.  Other
areas where this mesh capability is useful is by adding forestry specific context to assets
from other transportation domains such as Routes, Trucks, Equipment in the logistics domain
as well as mapping features and layers for custom roads and alerts in geo data.


Objectives and Key Results
--------------------------

I believe that transitioning to microservice architecture can be measured as an initiative
within the following objective categories.

- Focus on cross-cutting concerns as initial microservices
- Building discipline and rigor on CI/CD practices
- Build/Replace Functionality with respect to Domain Decomposition
- Isolate independent microservices when they are ready


Focus on cross-cutting concerns as initial microservices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Authentication
- Authorization and Context Handling
- Monitoring, Observability, Fault Handling and Logging

Building Discipline and Rigor with CI/CD practices
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build Discipline in continuous integration and deployments

- Regional Routing and Content Delivery
- Feature Flags, Continuous Integration and Continuous Deployment


Build/Replace Functionality with respect to Domain Decomposition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- API Standardization, Tagging, Linting and Maintenance
- Data modeling, semantic, logical and physical (JSON Schema + JSON-LD)

Isolate independent microservices when they are ready
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Build or Replace Functionality based on Domain Decomposition

Decomposition Methods
    By Business Capability (Disadvantages)

    By sub domain (too many microservices and low cohesiveness)

    By Transactions

    Per Team and capability (API negotiation and dependencies)

Strangler Fig (outside-in replacement)
    Transform (create new components on the edges),

    Coexist (intercept outside calls and redirect to new components),

    Eliminate (retire old functionality from monolith)

Branch by Abstraction (inside-out replacement)
    Watch for data consistency issues

    Requires change to existing system (expected and good)
