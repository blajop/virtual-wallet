


# <a name="java-team-project"></a>Project Description
<a name="functional-requirements"></a>**Virtual Wallet** is a web application that enables you to continently manage your budget. Every user can send and receive money (user to user) and put money in his **Virtual Wallet** (bank to app). **Virtual Wallet** has a core set of requirements that are absolute must and a variety of optional features.
# Functional Requirements
## Entities
- <a name="countries"></a>Each **user** must have a username, password, email, phone number, credit/debit card. He also could have a photo.
  - Username must be unique and between 2 and 20 symbols.
  - Password must be at least 8 symbols and should contain capital letter, digit and special symbol (+, -, \*, &, ^, …)
  - Email must be valid email and unique in the system.
  - Phone number must be 10 digits and unique in the system.
- **Credit/debit card** must have a number, expiration date, card holder and a check number
  - Card number must be unique and with 16 digits.
  - Card holder must be between 2 and 30 symbols.
  - Check number must be 3 digits.
## <a name="general"></a>Public Part
The public part must be accessible without authentication i.e., for anonymous users. 

Anonymous users must be able to register and login.

Anonymous users must see detailed information about Virtual Wallet and its features.
## <a name="customers"></a>Private part
Accessible only if the user is authenticated.

Users must be able to login/logout, update their profile, manage their credit/debit card, make transfers to other users, and view the history of their transfers.

Users must be able to view and edit their profile information, except their username, which is selected on registration and cannot be changed afterwards. The required fields for registration are username, email, and phone number.

Each user must be able to register one credit or debit card, which is used to transfer money into their **Virtual Wallet**.

*Note: **DO NOT** use actual credit card information!*

Users must be able to transfer money to other users by entering another user's phone number, username or email and desired amount to be transferred. Users can search by phone number, username, or email to select the recipient user for the transfer, but when viewing recipient users only username must be displayed.

Each transfer must go through confirmation step which displays the transfer details and allows either confirming it or editing it.

The receiver of the money must be able to accept or decline the transaction.

Users must be able to view a list of their transactions filtered by period, recipient, and direction (incoming or outgoing) and sort them by amount and date. Transaction list should support pagination.
## <a name="employees"></a>Administrative part
Accessible to users with administrative privileges.

Admin users must be able to see list of all users and search them by phone number, username or email and block or unblock them. User list should support pagination. A blocked user must be able to do everything as normal user, except to make transactions.

Admin users must be able to view a list of all user transactions filtered by period, sender, recipient, and direction (incoming or outgoing) and sort them by amount and date. Transaction list should support pagination.
## Optional features (should)
**Email Verification** – In order for the registration to be completed, the user must verify their email by clicking on a link send to their email by the application. Before verifying their email, users cannot make transactions.

**Email Notification** – When a user is sending money the recipient receives a notification that he should approve or decline a transaction.

**Large Transaction Verification** – In order to complete transactions over a certain amount (up to you), the user is prompted to enter a verification code, sent to their email. The code should be unique for the transaction and have expiration time.

**Refer a Friend** – A user can enter email of people, not yet registered for the application, and invite them to register. The application sends to that email a registration link. If a registration from that email is completed and verified, both users receive a certain amount (up to you) in their virtual wallet. Invitations have an expiration time, and a user can take advantage of that feature a limited number of times (up to you).

**Joint Virtual Wallets** – User can create joint virtual wallets. They function as the regular wallets; however, multiple users can use them. The original creator of the wallet has an administration panel for the wallet, where they can grant or revoke other user’s access to spend or add money to the wallet. When making a transaction or adding money to wallet, users with access to multiple wallets must select, which one to use. The Transaction History Page show which wallet was used for the transaction.

**Recurring Transactions** – Users can set up recurring transactions. When creating a transaction, the user has the option to select an interval of time on which the transaction is repeated automatically. Users have a page, where they can view all their recurring transactions and cancel them. Users must be notified if their transactions failed for some reason.

**Contacts List** – In addition to searching through all the application users, a user can create a contacts list. A user can add another user to their contacts list either from the transaction profile search or from the Transactions History Page. On the Create Transaction Page the user must select if the transaction is from the contacts list or from the application users list. The user has a contact list administration page, where they can remove users from the list.

**Multiple Virtual Wallets** – A user can create more than one wallet. When creating a transaction, the user is prompted to select, which wallet to use. The Transaction History Page show which wallet was used for the transaction. The user can set a default wallet, which is preselected when creating transactions.

**Multiple Cards** – A user can register multiple credit and or debit cards, from which to add funds to their accounts. When adding funds to their wallet, the user is prompted to select from which bank account to do so.

**Spending Categories** – When creating a transaction, a user can select a category for the transfer (Rent, Utilities, Eating out etc.). The user has a page to manage their categories. They can add, edit, or delete them. The user also has a reports page where they can select a period and see a breakdown of their spending by category.

**Currency Support** – When creating their Virtual Wallet users, can choose a currency for it. The currency exchange rate is shown on transactions between different currencies. The exchange rate and supported currencies are managed by admin users.

**Easter eggs** – Creativity is always welcome and appreciated. Find a way to add something fun and/or interesting, maybe an Easter egg or two to you project to add some variety. 
## <a name="rest-api"></a>REST API
To provide other developers with your service, you need to develop a REST API. It should leverage HTTP as a transport protocol and clear text JSON for the request and response payloads.

A great API is nothing without a great documentation. The documentation holds the information that is required to successfully consume and integrate with an API. You must use [Swagger](https://swagger.io/) to document yours.

The REST API provides the following capabilities:

1. Users
   1. CRUD Operations (must)
   1. Add/view/update/delete credit/debit card (must)
   1. Block/unblock user (must)
   1. Search by username, email, or phone (must)
1. Transactions
   1. Add money to wallet (must)
   1. Make transaction (must)
   1. Approve/decline transaction (must)
   1. List transactions (must)
   1. Filter by date, sender, recipient, and direction (in/out) (must)
   1. Sort by date or amount (must)
1. Transfers
   1. Withdraw (must)
# <a name="technical-requirements"></a>Technical Requirements
## General
- Follow [KISS](https://en.wikipedia.org/wiki/KISS_principle), [SOLID](https://en.wikipedia.org/wiki/SOLID), [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) principles when coding
- Follow REST API design [best practices](https://blog.florimondmanca.com/restful-api-design-13-best-practices-to-make-your-users-happy) when designing the REST API (see Appendix)
- Use tiered project structure (separate the application in layers)
- The service layer (i.e., "business" functionality) must have at least 80% unit test code coverage
- You should implement proper exception handling and propagation
- Try to think ahead. When developing something, think – “How hard would it be to change/modify this later?”
## <a name="database"></a>Database
The data of the application must be stored in a relational database. You need to identify the core domain objects and model their relationships accordingly. Database structure should avoid data duplication and empty data (normalize your database).

Your repository must include two scripts – one to create the database and one to fill it with data.
## <a name="deliverables"></a><a name="optional-requirements"></a>Git
Commits in the GitLab repository should give a good overview of how the project was developed, which features were created first and the people who contributed. Contributions from all team members must be evident through the git commit history! The repository must contain the complete application source code and any scripts (database scripts, for example).

Provide a link to a GitLab repository with the following information in the README.md file:

- Project description
- Link to the Swagger documentation 
- Link to the hosted project (if hosted online)
- Instructions how to setup and run the project locally 
- Images of the database relations (must)
##
## Optional Requirements
Besides all requirements marked as should and could, here are some more *optional* requirements:

- Use a branching while working with Git.
- Integrate your app with a Continuous Integration server (e.g., GitLab’s own) and configure your unit tests to run on each commit to the master branch.
- Host your application’s backend in a public hosting provider of your choice (e.g., AWS, Azure, Heroku).
# <a name="_hlk78273426"></a><a name="project-defense"></a>Teamwork Guidelines
Please see the Teamwork Guidelines document. 
# <a name="appendix"></a>Appendix
- [Guidelines for designing good REST API](https://blog.florimondmanca.com/restful-api-design-13-best-practices-to-make-your-users-happy)
- [](https://blog.florimondmanca.com/restful-api-design-13-best-practices-to-make-your-users-happy)[Guidelines for URL encoding](http://www.talisman.org/~erlkonig/misc/lunatech%5Ewhat-every-webdev-must-know-about-url-encoding/)[](https://www.vojtechruzicka.com/field-dependency-injection-considered-harmful/)
- [](https://www.vojtechruzicka.com/field-dependency-injection-considered-harmful/)[Git commits - an effective style guide](https://dev.to/pavlosisaris/git-commits-an-effective-style-guide-2kkn)
- [](https://dev.to/pavlosisaris/git-commits-an-effective-style-guide-2kkn)[How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
# Legend
- Must – Implement these first.
- Should – if you have time left, try to implement these.
- Could – only if you are ready with everything else give these a go.
